#!/usr/bin/env python3
from __future__ import annotations
import shutil, subprocess, sys
if len(sys.argv)<2: raise SystemExit('usage: optional_tool.py TOOL [ARGS...]')
tool=sys.argv[1]
if not shutil.which(tool):
    print(f"NOT-EXECUTED optional tool unavailable: {tool}")
    raise SystemExit(2)
r=subprocess.run(sys.argv[1:])
raise SystemExit(r.returncode)
