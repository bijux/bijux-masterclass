from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .blueprint import validate_blueprint
from .chapter import validate_chapter
from .manifest import module_rows
from .result import ValidationResult
from .review import validate_module_review
from .snippets import verify_chapter_snippets


@dataclass(frozen=True)
class AuditReport:
    scope: str
    expected_modules: int
    entries: tuple[dict[str, Any], ...]
    issues: tuple[str, ...] = ()

    @property
    def counts(self) -> dict[str, int]:
        counts = {"passed": 0, "failed": 0, "skipped": 0, "unavailable": 0}
        for entry in self.entries:
            counts[entry["status"]] += 1
        return counts

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "scope": self.scope,
            "expected_modules": self.expected_modules,
            "validation_status": "failed" if self.issues else "passed",
            "summary": self.counts,
            "issues": list(self.issues),
            "entries": list(self.entries),
        }


def select_modules(
    rows: list[dict[str, str]],
    *,
    program: str | None = None,
    level: int | None = None,
    module_number: int | None = None,
) -> tuple[str, int, list[dict[str, str]]]:
    selected = rows
    scope_parts: list[str] = []
    expected = 3000
    if module_number is not None:
        selected = [row for row in selected if int(row["module_number"]) == module_number]
        scope_parts.append(f"module-{module_number:03}")
        expected = 30
    if program is not None:
        normalized = program.upper()
        selected = [row for row in selected if row["program_code"] == normalized]
        scope_parts.append(f"program-{normalized.casefold()}")
        expected = 100
    if level is not None:
        selected = [row for row in selected if int(row["level"]) == level]
        scope_parts.append(f"level-{level}")
        expected = 50 if program is not None else 1500
    scope = "-".join(scope_parts) if scope_parts else "corpus"
    return scope, expected, selected


def _write_report(root: Path, report: AuditReport) -> Path:
    directory = root / "artifacts" / "audits" / report.scope
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "report.json"
    candidate = directory / ".report.json.bijux-candidate"
    candidate.write_text(
        json.dumps(report.as_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    candidate.replace(path)
    return path


def audit_modules(
    root: Path,
    *,
    program: str | None = None,
    level: int | None = None,
    module_number: int | None = None,
    require_complete: bool = False,
) -> tuple[ValidationResult, AuditReport, Path]:
    root = root.resolve()
    issues: list[str] = []
    blueprint_result, _ = validate_blueprint(root)
    issues.extend(f"blueprint: {issue}" for issue in blueprint_result.issues)
    rows = module_rows(root) if blueprint_result.ok else []
    scope, expected, selected = select_modules(
        rows,
        program=program,
        level=level,
        module_number=module_number,
    )
    if len(selected) != expected:
        issues.append(f"{scope}: expected {expected} manifest rows, found {len(selected)}")

    entries: list[dict[str, Any]] = []
    for row in selected:
        module_id = row["module_id"]
        if row["status"] == "planned":
            entries.append(
                {
                    "module_id": module_id,
                    "status": "skipped",
                    "reason": "manifest status is planned",
                }
            )
            if require_complete:
                issues.append(f"{module_id}: required module is still planned")
            continue

        chapter_result = validate_chapter(root, module_id)
        snippet_result, snippet_report, _ = verify_chapter_snippets(root, module_id)
        review_result = validate_module_review(root, module_id)
        module_issues = (
            list(chapter_result.issues)
            + list(snippet_result.issues)
            + list(review_result.issues)
        )
        unavailable = bool(
            snippet_report is not None and snippet_report.counts["unavailable"]
        )
        status = "unavailable" if unavailable else "failed" if module_issues else "passed"
        entries.append(
            {
                "module_id": module_id,
                "status": status,
                "checks": {
                    "chapter": "passed" if chapter_result.ok else "failed",
                    "snippets": "passed" if snippet_result.ok else status,
                    "review": "passed" if review_result.ok else "failed",
                },
                "issues": module_issues,
            }
        )
        issues.extend(f"{module_id}: {issue}" for issue in module_issues)

    report = AuditReport(
        scope=scope,
        expected_modules=expected,
        entries=tuple(entries),
        issues=tuple(issues),
    )
    path = _write_report(root, report)
    return ValidationResult(tuple(issues)), report, path
