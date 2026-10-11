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
from scripts.catalogue.files import capture_sources, write_documents
from scripts.catalogue.source_plan import build_plan


def main() -> int:
    plan = build_plan(capture_sources(REPO_ROOT))
    write_documents(plan, REPO_ROOT)
    print("Synced docs into docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
