#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, shutil, subprocess, sys
from common import ROOT
print(f"Python: {sys.version.split()[0]}")
print(f"Git: {shutil.which('git') or 'missing'}")
print(f"Go: {shutil.which('go') or 'missing'}")
print(f"PyYAML: {'available' if importlib.util.find_spec('yaml') else 'missing'}")
for tool in ['kustomize','helm','argocd','flux','kind','kubectl','mkdocs']:
    print(f"{tool}: {shutil.which(tool) or 'not installed (optional lane)'}")
if not shutil.which('git') or not shutil.which('go') or not importlib.util.find_spec('yaml'):
    raise SystemExit('FAIL required dependency missing')
print(f"Course root: {ROOT}")
print('PASS dependency-light doctor')
