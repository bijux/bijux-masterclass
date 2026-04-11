#!/usr/bin/env python3
"""Sync the public library directly from program course-book trees."""

from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = REPO_ROOT / "programs"
TARGET_ROOT = REPO_ROOT / "docs" / "library"
SKIP_PARTS = {
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def copy_markdown_tree(source_dir: Path, target_dir: Path) -> None:
    for source_path in sorted(source_dir.rglob("*.md")):
        relative_path = source_path.relative_to(source_dir)
        if should_skip(relative_path):
            continue

        target_path = target_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> int:
    shutil.rmtree(TARGET_ROOT, ignore_errors=True)
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)

    for family_dir in sorted(PROGRAMS_DIR.iterdir()):
        if not family_dir.is_dir():
            continue
        for program_dir in sorted(family_dir.iterdir()):
            if not program_dir.is_dir():
                continue

            course_book_dir = program_dir / "course-book"
            if not course_book_dir.exists():
                continue

            program_target_dir = TARGET_ROOT / family_dir.name / program_dir.name
            copy_markdown_tree(course_book_dir, program_target_dir)

    print(f"Synced docs into {TARGET_ROOT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
