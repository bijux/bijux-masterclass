#!/usr/bin/env python3
"""Audit or normalize Markdown math so repository chapters render on GitHub."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from course_validation.markdown import (
    github_math_diagnostics,
    github_math_issues,
    normalize_github_math,
    normalize_parenthetical_math,
)
from course_validation.review import chapter_digest, review_path

ROOT = Path(__file__).resolve().parents[1]


def markdown_paths(root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in root.rglob("*.md")
            if "artifacts" not in path.parts and ".git" not in path.parts
        )
    )


def complete_module_paths(root: Path) -> dict[Path, str]:
    with (root / "manifests" / "modules.csv").open(encoding="utf-8", newline="") as handle:
        return {
            (root / row["future_path"]).resolve(): row["module_id"]
            for row in csv.DictReader(handle)
            if row["status"] == "complete"
        }


def refresh_review_digest(root: Path, module_id: str, chapter_text: str) -> None:
    path = review_path(root, module_id)
    if not path.is_file():
        raise FileNotFoundError(f"missing review evidence for {module_id}: {path.relative_to(root)}")
    record = json.loads(path.read_text(encoding="utf-8"))
    record["chapter_digest"] = chapter_digest(chapter_text)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write safe rendering normalizations")
    parser.add_argument(
        "--parenthetical-math",
        action="store_true",
        help="normalize conservative legacy parenthetical notation as math",
    )
    args = parser.parse_args()

    complete_paths = complete_module_paths(ROOT)
    changed: list[Path] = []
    issues: list[tuple[Path, tuple[str, ...]]] = []
    diagnostics: list[tuple[Path, tuple[str, ...]]] = []
    for path in markdown_paths(ROOT):
        original = path.read_text(encoding="utf-8")
        normalized = normalize_github_math(original)
        if args.parenthetical_math:
            normalized = normalize_parenthetical_math(normalized)
        if normalized != original:
            changed.append(path)
            if args.apply:
                path.write_text(normalized, encoding="utf-8")
                module_id = complete_paths.get(path.resolve())
                if module_id is not None:
                    refresh_review_digest(ROOT, module_id, normalized)
        inspected = normalized if args.apply else original
        found = github_math_issues(inspected)
        if found:
            issues.append((path, found))
        remaining = github_math_diagnostics(inspected)
        if remaining:
            diagnostics.append((path, remaining))

    action = "normalized" if args.apply else "would normalize"
    print(f"Markdown files checked: {len(markdown_paths(ROOT))}")
    print(f"Files {action}: {len(changed)}")
    for path, found in issues:
        print(f"FAIL: {path.relative_to(ROOT)}: {'; '.join(found)}")
    for path, found in diagnostics:
        print(f"WARN: {path.relative_to(ROOT)}: {'; '.join(found)}")
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
