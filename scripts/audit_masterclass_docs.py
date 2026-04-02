#!/usr/bin/env python3
"""Audit course-book and capstone documentation quality gates."""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = REPO_ROOT / "programs"
COURSE_BOOK_GLOB = "*/*/course-book/**/*.md"
CAPSTONE_GLOB = "*/*/capstone/**/*.md"
BANNED_PATH_WORDS = {"phase", "task"}
SKIP_PARTS = {
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "site",
}
SKIP_CAPSTONE_PREFIXES = {
    "publish/",
}


@dataclass(frozen=True)
class AuditRecord:
    path: Path
    kind: str
    diagrams: int
    h1_count: int
    banned_parts: tuple[str, ...]


def iter_markdown(kind: str) -> list[Path]:
    pattern = COURSE_BOOK_GLOB if kind == "course-book" else CAPSTONE_GLOB
    paths = []
    for path in sorted(PROGRAMS_DIR.glob(pattern)):
        rel = path.relative_to(REPO_ROOT)
        rel_str = rel.as_posix()
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if kind == "capstone" and any(rel_str.split("/capstone/", 1)[1].startswith(prefix) for prefix in SKIP_CAPSTONE_PREFIXES):
            continue
        paths.append(path)
    return paths


def count_h1(text: str) -> int:
    count = 0
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("# "):
            count += 1
    return count


def find_banned_parts(path: Path) -> tuple[str, ...]:
    banned = []
    for part in path.parts:
        lowered = part.lower().replace(".md", "")
        tokens = [token for token in re.split(r"[^a-z0-9]+", lowered) if token]
        if any(token in BANNED_PATH_WORDS for token in tokens):
            banned.append(part)
    return tuple(banned)


def audit_path(path: Path, kind: str) -> AuditRecord:
    text = path.read_text(encoding="utf-8")
    diagrams = text.count("```mermaid")
    h1_count = count_h1(text)
    banned_parts = find_banned_parts(path.relative_to(REPO_ROOT))
    return AuditRecord(
        path=path.relative_to(REPO_ROOT),
        kind=kind,
        diagrams=diagrams,
        h1_count=h1_count,
        banned_parts=banned_parts,
    )


def render_summary(records: list[AuditRecord]) -> str:
    by_kind: dict[str, list[AuditRecord]] = defaultdict(list)
    for record in records:
        by_kind[record.kind].append(record)

    lines = []
    for kind in ("course-book", "capstone"):
        items = by_kind[kind]
        diagram_counts = Counter(record.diagrams for record in items)
        lines.append(f"{kind}: {len(items)} files")
        lines.append(f"  diagram distribution: {dict(sorted(diagram_counts.items()))}")
        lines.append(
            "  missing diagram minimum: "
            f"{sum(1 for record in items if record.diagrams < 2)}"
        )
        lines.append(
            "  invalid H1 count: "
            f"{sum(1 for record in items if record.h1_count != 1)}"
        )
        lines.append(
            "  banned path names: "
            f"{sum(1 for record in items if record.banned_parts)}"
        )
    return "\n".join(lines)


def render_failures(records: list[AuditRecord]) -> str:
    lines = []
    for record in records:
        failures = []
        if record.diagrams < 2:
            failures.append(f"diagrams={record.diagrams}")
        if record.h1_count != 1:
            failures.append(f"h1={record.h1_count}")
        if record.banned_parts:
            failures.append(f"banned={','.join(record.banned_parts)}")
        if failures:
            lines.append(f"{record.path.as_posix()}: {'; '.join(failures)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any course-book or capstone guide violates the audit rules.",
    )
    args = parser.parse_args()

    records = []
    for kind in ("course-book", "capstone"):
        for path in iter_markdown(kind):
            records.append(audit_path(path, kind))

    print(render_summary(records))

    failures = render_failures(records)
    if failures:
        print("\nViolations:")
        print(failures)

    if args.strict and failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
