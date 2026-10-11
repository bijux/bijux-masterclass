#!/usr/bin/env python3
"""Materialize the public catalogue from the captured original-source plan."""
from __future__ import annotations
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Keep existing hyperlink callers on the same pure projection implementation.
from scripts.catalogue.links import (
    split_anchor, normalize_catalog_path, rewrite_link_target,
    rewrite_html_hyperlinks, rewrite_markdown_links,
)
from scripts.catalogue.files import capture_sources, write_documents, write_program_documents
from scripts.catalogue.source_plan import build_plan, PlanError


def sync_program_docs(program_dir: Path, target_dir: Path) -> None:
    """Stage one captured course for the shared standalone documentation hook."""
    try:
        program_relative = program_dir.absolute().relative_to(REPO_ROOT).as_posix()
        target_relative = target_dir.absolute().relative_to(REPO_ROOT).as_posix()
    except ValueError as error:
        raise PlanError("program documentation must remain inside its owning repository") from error
    plan = build_plan(capture_sources(REPO_ROOT))
    write_program_documents(plan, REPO_ROOT, program_relative, target_relative)


def main() -> int:
    plan = build_plan(capture_sources(REPO_ROOT))
    write_documents(plan, REPO_ROOT)
    print("Synced docs into docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
