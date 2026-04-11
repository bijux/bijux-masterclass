#!/usr/bin/env python3
"""Check the public docs library depth and capstone-doc export contract."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = REPO_ROOT / "programs"
LIBRARY_ROOT = REPO_ROOT / "docs" / "library"


def fail(message: str) -> None:
    raise AssertionError(message)


def check_max_depth() -> None:
    nested_dirs = sorted(
        path.relative_to(LIBRARY_ROOT)
        for path in LIBRARY_ROOT.rglob("*")
        if path.is_dir() and len(path.relative_to(LIBRARY_ROOT).parts) > 3
    )
    if nested_dirs:
        fail(f"unexpected nested public docs directories: {nested_dirs[0]}")


def check_capstone_docs_exports() -> None:
    for course_book_dir in sorted(PROGRAMS_DIR.glob("*/*/course-book")):
        program_slug = course_book_dir.parent.relative_to(PROGRAMS_DIR)
        library_program_dir = LIBRARY_ROOT / program_slug
        source_capstone_docs_index = course_book_dir / "capstone-docs" / "index.md"
        capstone_docs_index = library_program_dir / "capstone-docs" / "index.md"
        legacy_overview = library_program_dir / "capstone" / "project-overview.md"
        legacy_project_docs_dir = library_program_dir / "project-docs"

        if source_capstone_docs_index.exists() and not capstone_docs_index.exists():
            fail(f"missing capstone docs index for {program_slug}")
        if legacy_overview.exists():
            fail(f"legacy capstone project overview still exported for {program_slug}")
        if legacy_project_docs_dir.exists():
            fail(f"legacy project-docs directory still exported for {program_slug}")


def main() -> int:
    check_max_depth()
    check_capstone_docs_exports()
    print("library tree checks passed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
