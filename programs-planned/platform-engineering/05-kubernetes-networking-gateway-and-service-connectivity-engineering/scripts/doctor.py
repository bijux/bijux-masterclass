#!/usr/bin/env python3
from pathlib import Path
import shutil,sys
from common import ROOT
required=['python3','go','openssl']; optional=['kubectl','kind','docker','mkdocs','kubeconform','cilium']
print(f'Course root: {ROOT}')
for cmd in required:
    path=shutil.which(cmd); print(f"required {cmd}: {path or 'MISSING'}")
    if not path: raise SystemExit(1)
for cmd in optional: print(f"optional {cmd}: {shutil.which(cmd) or 'not-executed'}")
print('PASS doctor')
