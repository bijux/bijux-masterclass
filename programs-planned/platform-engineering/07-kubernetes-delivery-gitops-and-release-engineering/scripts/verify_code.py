#!/usr/bin/env python3
from __future__ import annotations
import py_compile, subprocess
from common import ROOT, fail
py=[p for p in ROOT.rglob('*.py') if not any(x in p.parts for x in {'__pycache__','.pytest_cache'})]
for p in py:
    try: py_compile.compile(str(p),doraise=True)
    except py_compile.PyCompileError as e: fail(f"Python syntax {p.relative_to(ROOT)}: {e.msg}")
sh=list(ROOT.rglob('*.sh'))
for p in sh:
    r=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True)
    if r.returncode: fail(f"shell syntax {p.relative_to(ROOT)}: {r.stderr.strip()}")
print(f"PASS source syntax — {len(py)} Python and {len(sh)} shell files")
