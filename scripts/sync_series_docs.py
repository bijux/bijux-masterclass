#!/usr/bin/env python3
"""Sync the public library directly from program README and course-book trees."""

from __future__ import annotations

import re
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
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def family_dirs() -> list[Path]:
    return sorted(path for path in PROGRAMS_DIR.iterdir() if path.is_dir())


def reset_target_root() -> None:
    if TARGET_ROOT.exists():
        shutil.rmtree(TARGET_ROOT)
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)


def split_anchor(target: str) -> tuple[str, str]:
    if "#" not in target:
        return target, ""
    path, anchor = target.split("#", 1)
    return path, f"#{anchor}"


def normalize_catalog_path(target: str) -> str:
    path, anchor = split_anchor(target)
    path = path.replace("/course-book/", "/")
    if path.startswith("course-book/"):
        path = path.removeprefix("course-book/")
    if path == "README.md":
        path = "index.md"
    elif path.endswith("/README.md"):
        path = f"{path[:-len('README.md')]}index.md"
    return f"{path}{anchor}"


def rewrite_link_target(target: str) -> str:
    if "://" in target or target.startswith(("mailto:", "#")):
        return target
    return normalize_catalog_path(target)


def rewrite_markdown_links(content: str) -> str:
    return MARKDOWN_LINK_RE.sub(
        lambda match: (
            f"{match.group(1)}{rewrite_link_target(match.group(2))}{match.group(3)}"
        ),
        content,
    )


def copy_markdown_file(
    source_path: Path,
    target_path: Path,
    *,
    rewrite_links: bool = False,
) -> None:
    content = source_path.read_text(encoding="utf-8")
    if rewrite_links:
        content = rewrite_markdown_links(content)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")


def copy_markdown_tree(source_dir: Path, target_dir: Path) -> None:
    for source_path in sorted(source_dir.rglob("*.md")):
        relative_path = source_path.relative_to(source_dir)
        if should_skip(relative_path):
            continue

        target_path = target_dir / relative_path
        copy_markdown_file(source_path, target_path)


def library_index_sources() -> list[tuple[Path, Path]]:
    sources = [(PROGRAMS_DIR / "README.md", TARGET_ROOT / "index.md")]
    for family_dir in family_dirs():
        sources.append((family_dir / "README.md", TARGET_ROOT / family_dir.name / "index.md"))
    return sources


def main() -> int:
    index_sources = library_index_sources()
    missing_sources = [
        source_path.relative_to(REPO_ROOT)
        for source_path, _ in index_sources
        if not source_path.is_file()
    ]
    if missing_sources:
        missing = ", ".join(str(path) for path in missing_sources)
        raise FileNotFoundError(f"missing library README source: {missing}")

    reset_target_root()

    for source_path, target_path in index_sources:
        copy_markdown_file(source_path, target_path, rewrite_links=True)

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
