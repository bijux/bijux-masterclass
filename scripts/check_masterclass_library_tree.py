#!/usr/bin/env python3
"""Check the generated public docs tree depth and capstone-doc export contract."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = REPO_ROOT / "programs"
DOCS_ROOT = REPO_ROOT / "docs"
FAMILY_ROOTS = ("python-programming", "reproducible-research")


def fail(message: str) -> None:
    raise AssertionError(message)


def check_max_depth() -> None:
    nested_dirs = []
    for family_name in FAMILY_ROOTS:
        family_root = DOCS_ROOT / family_name
        nested_dirs.extend(
            sorted(
                path.relative_to(family_root)
                for path in family_root.rglob("*")
                if path.is_dir() and len(path.relative_to(family_root).parts) > 2
            )
        )
    if nested_dirs:
        fail(f"unexpected nested public docs directories: {nested_dirs[0]}")


def check_capstone_docs_exports() -> None:
    for course_book_dir in sorted(PROGRAMS_DIR.glob("*/*/course-book")):
        program_slug = course_book_dir.parent.relative_to(PROGRAMS_DIR)
        program_root = course_book_dir.parent
        docs_program_dir = DOCS_ROOT / program_slug
        source_capstone_docs_index = program_root / "capstone" / "docs" / "index.md"
        capstone_docs_index = docs_program_dir / "capstone-docs" / "index.md"
        legacy_overview = docs_program_dir / "capstone" / "project-overview.md"
        legacy_project_docs_dir = docs_program_dir / "project-docs"

        if source_capstone_docs_index.exists() and not capstone_docs_index.exists():
            fail(f"missing capstone docs index for {program_slug}")
        if legacy_overview.exists():
            fail(f"legacy capstone project overview still exported for {program_slug}")
        if legacy_project_docs_dir.exists():
            fail(f"legacy project-docs directory still exported for {program_slug}")


def main() -> int:
    check_max_depth()
    check_capstone_docs_exports()
    print("public docs tree checks passed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
