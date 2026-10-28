#!/usr/bin/env python3
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
for p in ROOT.rglob('__pycache__'):
    if p.is_dir(): shutil.rmtree(p)
for p in ROOT.rglob('.pytest_cache'):
    if p.is_dir(): shutil.rmtree(p)
for rel in ['reports/runtime','reports/generated']:
    p=ROOT/rel
    if p.exists(): shutil.rmtree(p)
print('PASS generated course artifacts removed')
