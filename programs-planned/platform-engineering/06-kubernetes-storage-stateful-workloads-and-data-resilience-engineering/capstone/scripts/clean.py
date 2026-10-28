#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in ROOT.rglob("__pycache__"):
    shutil.rmtree(path, ignore_errors=True)
for name in (".pytest_cache", ".mypy_cache", ".ruff_cache"):
    for path in ROOT.rglob(name):
        shutil.rmtree(path, ignore_errors=True)
for path in (ROOT / "reports" / "runtime", ROOT / "site"):
    shutil.rmtree(path, ignore_errors=True)
