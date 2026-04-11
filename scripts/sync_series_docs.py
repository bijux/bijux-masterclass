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


def family_dirs() -> list[Path]:
    return sorted(path for path in PROGRAMS_DIR.iterdir() if path.is_dir())


def preserve_library_indexes() -> None:
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    expected_families = {family_dir.name for family_dir in family_dirs()}

    for child in sorted(TARGET_ROOT.iterdir()):
        if child.is_file():
            if child.name != "index.md":
                child.unlink()
            continue
        if child.name not in expected_families:
            shutil.rmtree(child)

    for family_name in expected_families:
        family_root = TARGET_ROOT / family_name
        family_root.mkdir(parents=True, exist_ok=True)
        for child in sorted(family_root.iterdir()):
            if child.is_dir():
                shutil.rmtree(child)
            elif child.name != "index.md":
                child.unlink()


def copy_markdown_tree(source_dir: Path, target_dir: Path) -> None:
    for source_path in sorted(source_dir.rglob("*.md")):
        relative_path = source_path.relative_to(source_dir)
        if should_skip(relative_path):
            continue

        target_path = target_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> int:
    preserve_library_indexes()

    required_indexes = [TARGET_ROOT / "index.md"]
    for family_dir in family_dirs():
        required_indexes.append(TARGET_ROOT / family_dir.name / "index.md")

    missing_indexes = [
        path.relative_to(REPO_ROOT)
        for path in required_indexes
        if not path.is_file()
    ]
    if missing_indexes:
        missing = ", ".join(str(path) for path in missing_indexes)
        raise FileNotFoundError(f"missing synced library index source: {missing}")

    for family_dir in family_dirs():
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
