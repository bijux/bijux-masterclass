#!/usr/bin/env python3
"""Materialize program course-book and capstone docs into the root docs tree."""

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


def include_target(text: str) -> str | None:
    match = re.fullmatch(r'\s*{%\s*include\s+"([^"]+)"\s*%}\s*', text)
    return match.group(1) if match else None


def rewrite_included_links(text: str, include_path: str) -> str:
    if include_path != "capstone/README.md":
        return text

    def replacer(match: re.Match[str]) -> str:
        target = match.group(1)
        if "://" in target or target.startswith("#") or target.startswith("/"):
            return match.group(0)
        if not target.endswith(".md"):
            return match.group(0)
        return f"]({ '../capstone/' + target })"

    return re.sub(r"\]\(([^)]+)\)", replacer, text)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def copy_markdown_tree(program_dir: Path, source_dir: Path, target_dir: Path) -> None:
    for source_path in sorted(source_dir.rglob("*.md")):
        if should_skip(source_path.relative_to(program_dir)):
            continue

        relative_path = source_path.relative_to(source_dir)
        target_path = target_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        text = source_path.read_text(encoding="utf-8")
        include_path = include_target(text)
        if include_path is not None:
            text = (program_dir / include_path).read_text(encoding="utf-8")
            text = rewrite_included_links(text, include_path)

        target_path.write_text(text, encoding="utf-8")


def main() -> int:
    shutil.rmtree(TARGET_ROOT, ignore_errors=True)
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)

    for family_dir in sorted(PROGRAMS_DIR.iterdir()):
        if not family_dir.is_dir():
            continue
        for program_dir in sorted(family_dir.iterdir()):
            if not program_dir.is_dir():
                continue
            for docs_name in ("course-book", "capstone"):
                source_dir = program_dir / docs_name
                if not source_dir.exists():
                    continue
                target_dir = TARGET_ROOT / family_dir.name / program_dir.name / docs_name
                copy_markdown_tree(program_dir, source_dir, target_dir)

    print(f"Synced docs into {TARGET_ROOT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
