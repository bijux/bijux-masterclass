#!/usr/bin/env python3
from __future__ import annotations

import shutil

from common import ROOT

required = ["python3", "go"]
optional = [
    "kubectl",
    "kind",
    "docker",
    "podman",
    "mkdocs",
    "kubeconform",
]
print(f"Course root: {ROOT}")
missing = []
for command in required:
    found = shutil.which(command)
    print(f"required {command}: {found or 'MISSING'}")
    if not found:
        missing.append(command)
for command in optional:
    print(f"optional {command}: {shutil.which(command) or 'not-executed'}")
if missing:
    raise SystemExit(f"required tools missing: {', '.join(missing)}")
print("PASS doctor")
