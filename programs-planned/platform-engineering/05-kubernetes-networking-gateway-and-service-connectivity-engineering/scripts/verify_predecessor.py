#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json

from common import ROOT, fail

base = ROOT / "capstone" / "predecessor" / "handoff"
manifest = json.loads((base / "MANIFEST.json").read_text(encoding="utf-8"))
for entry in manifest["files"]:
    path = base / entry["path"]
    if not path.is_file():
        fail(f"predecessor file missing: {entry['path']}")
    if path.stat().st_size != entry["bytes"]:
        fail(f"predecessor size mismatch: {entry['path']}")
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
        fail(f"predecessor digest mismatch: {entry['path']}")
print(f"PASS Course 4 predecessor handoff — {len(manifest['files'])} exact files")
