#!/usr/bin/env python3
"""Materialize the derived root configuration from the original catalogue plan."""
from __future__ import annotations
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.catalogue.files import capture_sources, write_configuration
from scripts.catalogue.source_plan import build_plan


def main() -> int:
    plan = build_plan(capture_sources(REPO_ROOT), environment=os.environ)
    write_configuration(plan, REPO_ROOT)
    print("Rendered root MkDocs config to artifacts/mkdocs.root.yml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
