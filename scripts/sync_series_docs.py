#!/usr/bin/env python3
"""Materialize program course-book and capstone docs into the root docs tree."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Callable
import posixpath


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAMS_DIR = REPO_ROOT / "programs"
TARGET_ROOT = REPO_ROOT / "docs" / "library"
PROJECT_DOCS_DIRNAME = "project-docs"
PROJECT_DOCS_MANIFEST = "project-docs-manifest.txt"
SKIP_PARTS = {
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
}
CAPSTONE_INTERNAL_PARTS = {
    "_history",
    "all-cores",
    "module-reference-states",
}
PROJECT_DOC_SOURCE_PARTS = {
    "docs",
    "workflow",
    "publish",
}
LIBRARY_LINK_ALIASES = {
    "python-programming/python-object-oriented-programming": {
        "capstone/capstone-review-checklist.md": "capstone/capstone-review-worksheet.md",
        "reference/object-design-checklist.md": "reference/review-checklist.md",
    },
    "reproducible-research/deep-dive-dvc": {
        "capstone/experiment-review-guide.md": "project-docs/experiment-guide.md",
        "capstone/recovery-review-guide.md": "project-docs/recovery-guide.md",
        "capstone/release-review-guide.md": "project-docs/release-review-guide.md",
        "reference/authority-map.md": "reference/review-checklist.md",
        "reference/verification-route-guide.md": "project-docs/review-route-guide.md",
    },
    "reproducible-research/deep-dive-make": {
        "capstone/capstone-proof-checklist.md": "project-docs/proof-guide.md",
        "capstone/repro-catalog.md": "project-docs/repro-guide.md",
        "reference/mk-layer-guide.md": "project-docs/target-guide.md",
        "reference/selftest-map.md": "project-docs/selftest-guide.md",
    },
    "reproducible-research/deep-dive-snakemake": {
        "capstone/profile-audit-guide.md": "project-docs/profile-audit-guide.md",
        "capstone/publish-review-guide.md": "project-docs/publish-review-guide.md",
        "reference/boundary-map.md": "reference/boundary-review-prompts.md",
        "reference/repository-layer-guide.md": "project-docs/architecture.md",
    },
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


def should_skip_capstone_path(path: Path) -> bool:
    return should_skip(path) or any(part in CAPSTONE_INTERNAL_PARTS for part in path.parts)


def slugify_path_part(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "doc"


def project_doc_target_path(relative_path: Path) -> Path:
    if relative_path == Path("README.md"):
        return Path(PROJECT_DOCS_DIRNAME) / "index.md"

    parts = list(relative_path.parts)
    if parts and parts[0] in {"docs", PROJECT_DOCS_DIRNAME}:
        parts = parts[1:]

    if not parts:
        return Path(PROJECT_DOCS_DIRNAME) / "index.md"

    target_parts = [slugify_path_part(part) for part in parts[:-1]]
    filename = parts[-1]
    if filename.lower() == "readme.md":
        target_parts.append("index.md")
    else:
        target_parts.append(f"{slugify_path_part(Path(filename).stem)}.md")
    return Path(PROJECT_DOCS_DIRNAME, *target_parts)


def project_doc_sources(capstone_dir: Path) -> list[Path]:
    manifest_path = capstone_dir / PROJECT_DOCS_MANIFEST
    if manifest_path.exists():
        sources: list[Path] = []
        for raw_line in manifest_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue
            source_path = capstone_dir / line
            if source_path.suffix != ".md":
                raise ValueError(f"{manifest_path} must list markdown files only: {line}")
            if not source_path.exists():
                raise FileNotFoundError(f"{manifest_path} references a missing file: {line}")
            sources.append(source_path)
        return sources

    sources: list[Path] = []

    readme_path = capstone_dir / "README.md"
    if readme_path.exists():
        sources.append(readme_path)

    for source_path in sorted(capstone_dir.rglob("*.md")):
        relative_path = source_path.relative_to(capstone_dir)
        if relative_path == Path("README.md"):
            continue
        if relative_path.parts[0] not in PROJECT_DOC_SOURCE_PARTS:
            continue
        sources.append(source_path)

    return sources


def rewrite_markdown_links(
    text: str,
    source_relative_path: Path,
    source_to_target: dict[str, Path],
    target_relative_path: Path,
) -> str:
    def replacer(match: re.Match[str]) -> str:
        raw_target = match.group(1)
        if "://" in raw_target or raw_target.startswith(("#", "/")):
            return match.group(0)

        target_path, fragment = (raw_target.split("#", 1) + [""])[:2]
        if not target_path.endswith(".md"):
            return match.group(0)

        normalized_source = Path(
            posixpath.normpath((source_relative_path.parent / target_path).as_posix())
        )
        rewritten_target = source_to_target.get(normalized_source.as_posix())
        if rewritten_target is None:
            return match.group(0)

        relative_target = Path(
            posixpath.relpath(
                rewritten_target.as_posix(),
                target_relative_path.parent.as_posix() or ".",
            )
        ).as_posix()
        fragment_suffix = f"#{fragment}" if fragment else ""
        return f"]({relative_target}{fragment_suffix})"

    return re.sub(r"\]\(([^)]+)\)", replacer, text)


def rewrite_library_alias_links(
    text: str,
    program_key: str,
    source_relative_path: Path,
) -> str:
    alias_map = LIBRARY_LINK_ALIASES.get(program_key)
    if not alias_map:
        return text

    def replacer(match: re.Match[str]) -> str:
        raw_target = match.group(1)
        if "://" in raw_target or raw_target.startswith(("#", "/")):
            return match.group(0)

        target_path, fragment = (raw_target.split("#", 1) + [""])[:2]
        if not target_path.endswith(".md"):
            return match.group(0)

        normalized_target = Path(
            posixpath.normpath((source_relative_path.parent / target_path).as_posix())
        ).as_posix()
        rewritten_target = alias_map.get(normalized_target)
        if rewritten_target is None:
            return match.group(0)

        relative_target = Path(
            posixpath.relpath(
                rewritten_target,
                source_relative_path.parent.as_posix() or ".",
            )
        ).as_posix()
        fragment_suffix = f"#{fragment}" if fragment else ""
        return f"]({relative_target}{fragment_suffix})"

    return re.sub(r"\]\(([^)]+)\)", replacer, text)


def copy_markdown_tree(
    program_dir: Path,
    source_dir: Path,
    target_dir: Path,
    skip_path: Callable[[Path], bool] | None = None,
) -> None:
    path_filter = skip_path or should_skip
    program_key = str(program_dir.relative_to(PROGRAMS_DIR))
    for source_path in sorted(source_dir.rglob("*.md")):
        if path_filter(source_path.relative_to(program_dir)):
            continue

        relative_path = source_path.relative_to(source_dir)
        target_path = target_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        text = source_path.read_text(encoding="utf-8")
        include_path = include_target(text)
        if include_path is not None:
            text = (program_dir / include_path).read_text(encoding="utf-8")
            text = rewrite_included_links(text, include_path)

        text = rewrite_library_alias_links(text, program_key, relative_path)

        target_path.write_text(text, encoding="utf-8")


def copy_capstone_course_book(program_dir: Path, capstone_dir: Path, target_dir: Path) -> None:
    for source_path in sorted(capstone_dir.glob("*.md")):
        if source_path.name == "README.md":
            continue
        if should_skip_capstone_path(source_path.relative_to(program_dir)):
            continue

        target_path = target_dir / source_path.name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def copy_project_docs(program_dir: Path, capstone_dir: Path, target_dir: Path) -> None:
    source_paths = [
        path
        for path in project_doc_sources(capstone_dir)
        if not should_skip_capstone_path(path.relative_to(program_dir))
    ]
    source_to_target = {
        path.relative_to(capstone_dir).as_posix(): project_doc_target_path(
            path.relative_to(capstone_dir)
        )
        for path in source_paths
    }

    for source_path in source_paths:
        relative_path = source_path.relative_to(capstone_dir)
        target_relative_path = project_doc_target_path(relative_path)
        target_path = target_dir / target_relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        text = source_path.read_text(encoding="utf-8")
        text = rewrite_markdown_links(
            text,
            relative_path,
            source_to_target,
            target_relative_path,
        )
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
            program_target_dir = TARGET_ROOT / family_dir.name / program_dir.name

            course_book_dir = program_dir / "course-book"
            if course_book_dir.exists():
                copy_markdown_tree(program_dir, course_book_dir, program_target_dir)

            capstone_dir = program_dir / "capstone"
            if capstone_dir.exists():
                copy_capstone_course_book(program_dir, capstone_dir, program_target_dir / "capstone")
                copy_project_docs(program_dir, capstone_dir, program_target_dir)

    print(f"Synced docs into {TARGET_ROOT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
