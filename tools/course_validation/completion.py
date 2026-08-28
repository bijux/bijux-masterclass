from __future__ import annotations

import csv
import io
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .blueprint import validate_blueprint
from .chapter import validate_chapter
from .manifest import find_module, read_csv, read_jsonl
from .review import validate_module_review
from .snippets import verify_chapter_snippets

FRONT_MATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
STATUS_LINE = re.compile(r"^status: draft$", re.MULTILINE)


class CompletionError(RuntimeError):
    """A module cannot make the guarded transition to complete."""


@dataclass(frozen=True)
class CompletionOutcome:
    module_id: str
    chapter_path: Path
    manifest_paths: tuple[Path, Path]
    evidence_path: Path


def _validated_draft(root: Path, module_id: str) -> dict[str, str]:
    blueprint_result, _ = validate_blueprint(root)
    if not blueprint_result.ok:
        raise CompletionError(
            "blueprint validation failed: " + "; ".join(blueprint_result.issues)
        )
    row = find_module(root, module_id)
    if row is None:
        raise CompletionError(f"module ID does not resolve exactly once: {module_id}")
    if row["status"] != "planned":
        raise CompletionError(
            f"{module_id} must be planned before completion, found {row['status']!r}"
        )
    chapter_result = validate_chapter(root, module_id, allow_draft=True)
    if not chapter_result.ok:
        raise CompletionError(
            "draft chapter validation failed: " + "; ".join(chapter_result.issues)
        )
    snippet_result, _, _ = verify_chapter_snippets(root, module_id)
    if not snippet_result.ok:
        raise CompletionError(
            "draft snippet validation failed: " + "; ".join(snippet_result.issues)
        )
    review_result = validate_module_review(root, module_id)
    if not review_result.ok:
        raise CompletionError(
            "module review validation failed: " + "; ".join(review_result.issues)
        )
    return row


def _complete_chapter(text: str) -> str:
    front = FRONT_MATTER.match(text)
    if front is None:
        raise CompletionError("chapter does not begin with valid front matter")
    matches = list(STATUS_LINE.finditer(front.group("body")))
    if len(matches) != 1:
        raise CompletionError("chapter front matter must contain exactly one draft status line")
    completed_front = STATUS_LINE.sub("status: complete", front.group(0), count=1)
    return completed_front + text[front.end():]


def _complete_csv(text: str, module_id: str) -> str:
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = list(reader)
    if reader.fieldnames is None:
        raise CompletionError("module CSV has no header")
    matches = [row for row in rows if row["module_id"] == module_id]
    if len(matches) != 1 or matches[0]["status"] != "planned":
        raise CompletionError("module CSV does not contain one planned target row")
    matches[0]["status"] = "complete"
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=reader.fieldnames,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def _complete_jsonl(text: str, module_id: str) -> str:
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    matches = [row for row in rows if row["module_id"] == module_id]
    if len(matches) != 1 or matches[0]["status"] != "planned":
        raise CompletionError("module JSONL does not contain one planned target row")
    matches[0]["status"] = "complete"
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def _assert_selected_row_only(
    before: list[dict[str, Any]],
    after: list[dict[str, Any]],
    module_id: str,
    source: str,
) -> None:
    if len(before) != len(after):
        raise CompletionError(f"{source} row count changed during completion")
    changed = []
    for old, new in zip(before, after, strict=True):
        if old != new:
            changed.append((old, new))
    if len(changed) != 1:
        raise CompletionError(f"{source} must change exactly one row, changed {len(changed)}")
    old, new = changed[0]
    if old.get("module_id") != module_id or new.get("module_id") != module_id:
        raise CompletionError(f"{source} changed a row other than {module_id}")
    expected = dict(old)
    expected["status"] = "complete"
    if old.get("status") != "planned" or new != expected:
        raise CompletionError(f"{source} changed fields other than the target status")


def _write_candidate(path: Path, text: str) -> Path:
    candidate = path.parent / f".{path.name}.bijux-candidate"
    permissions = path.stat().st_mode & 0o777
    descriptor = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL, permissions)
    try:
        os.fchmod(descriptor, permissions)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        candidate.unlink(missing_ok=True)
        raise
    return candidate


def _replace_contents(contents: dict[Path, str]) -> None:
    candidates: dict[Path, Path] = {}
    try:
        for path, text in contents.items():
            candidates[path] = _write_candidate(path, text)
        for path, candidate in candidates.items():
            candidate.replace(path)
    finally:
        for candidate in candidates.values():
            candidate.unlink(missing_ok=True)


def _write_evidence(root: Path, module_id: str, paths: tuple[Path, ...]) -> Path:
    directory = root / "artifacts" / "modules" / module_id
    directory.mkdir(parents=True, exist_ok=True)
    evidence = {
        "schema_version": 1,
        "module_id": module_id,
        "transition": {"from": "planned", "to": "complete"},
        "validation": {
            "draft_chapter": "passed",
            "draft_snippets": "passed",
            "module_review": "passed",
            "completed_blueprint": "passed",
            "completed_chapter": "passed",
            "completed_snippets": "passed",
        },
        "changed_paths": [str(path.relative_to(root)) for path in paths],
    }
    path = directory / "completion.json"
    candidate = directory / ".completion.json.bijux-candidate"
    candidate.write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    candidate.replace(path)
    return path


def complete_module(root: Path, module_id: str) -> CompletionOutcome:
    root = root.resolve()
    row = _validated_draft(root, module_id)
    chapter_path = root / row["future_path"]
    csv_path = root / "manifests" / "modules.csv"
    jsonl_path = root / "manifests" / "modules.jsonl"
    paths = (chapter_path, csv_path, jsonl_path)
    originals = {path: path.read_text(encoding="utf-8") for path in paths}

    completed = {
        chapter_path: _complete_chapter(originals[chapter_path]),
        csv_path: _complete_csv(originals[csv_path], module_id),
        jsonl_path: _complete_jsonl(originals[jsonl_path], module_id),
    }
    _assert_selected_row_only(
        read_csv(csv_path),
        list(csv.DictReader(io.StringIO(completed[csv_path], newline=""))),
        module_id,
        "module CSV",
    )
    _assert_selected_row_only(
        read_jsonl(jsonl_path),
        [json.loads(line) for line in completed[jsonl_path].splitlines() if line.strip()],
        module_id,
        "module JSONL",
    )

    try:
        _replace_contents(completed)
        blueprint_result, _ = validate_blueprint(root)
        chapter_result = validate_chapter(root, module_id)
        snippet_result, _, _ = verify_chapter_snippets(root, module_id)
        review_result = validate_module_review(root, module_id)
        post_issues = (
            list(blueprint_result.issues)
            + list(chapter_result.issues)
            + list(snippet_result.issues)
            + list(review_result.issues)
        )
        if post_issues:
            raise CompletionError(
                "completed module validation failed: " + "; ".join(post_issues)
            )
        evidence_path = _write_evidence(root, module_id, paths)
    except Exception as error:
        _replace_contents(originals)
        if isinstance(error, CompletionError):
            raise
        raise CompletionError(f"completion transaction failed and was rolled back: {error}") from error

    return CompletionOutcome(
        module_id=module_id,
        chapter_path=chapter_path,
        manifest_paths=(csv_path, jsonl_path),
        evidence_path=evidence_path,
    )
