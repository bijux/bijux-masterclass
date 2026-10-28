#!/usr/bin/env python3
from __future__ import annotations

import compileall
from pathlib import Path
import subprocess

from common import ROOT, fail

if not compileall.compile_dir(ROOT, quiet=1, force=True):
    fail("Python compilation failed")
python_files = sum(1 for _ in ROOT.rglob("*.py"))

shell_files = sorted(ROOT.rglob("*.sh"))
for path in shell_files:
    result = subprocess.run(
        ["bash", "-n", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(f"shell syntax {path.relative_to(ROOT)}: {result.stderr.strip()}")

print(
    "PASS source syntax — "
    f"{python_files} Python files, {len(shell_files)} shell files"
)
