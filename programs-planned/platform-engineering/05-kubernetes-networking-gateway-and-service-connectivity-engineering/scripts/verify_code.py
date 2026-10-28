#!/usr/bin/env python3
from __future__ import annotations

import py_compile
import subprocess
from pathlib import Path

from common import ROOT, fail

python_files = [
    path
    for path in ROOT.rglob("*.py")
    if not any(part in {"__pycache__", ".pytest_cache"} for part in path.parts)
]
for path in python_files:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        fail(f"Python syntax: {path.relative_to(ROOT)}: {exc.msg}")

shell_files = [
    path
    for path in ROOT.rglob("*.sh")
    if path.is_file()
]
for path in shell_files:
    result = subprocess.run(
        ["bash", "-n", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(f"shell syntax: {path.relative_to(ROOT)}: {result.stderr.strip()}")

print(
    f"PASS source syntax — {len(python_files)} Python, "
    f"{len(shell_files)} shell files"
)
