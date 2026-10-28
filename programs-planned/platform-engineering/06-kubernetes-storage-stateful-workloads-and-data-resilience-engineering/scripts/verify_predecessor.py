#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, fail, load_json, sha256

base = ROOT / "capstone" / "predecessor" / "handoff"
manifest = load_json(base / "MANIFEST.json")
for entry in manifest["files"]:
    path = base / entry["path"]
    if not path.is_file():
        fail(f"predecessor file missing: {entry['path']}")
    if path.stat().st_size != entry["bytes"]:
        fail(f"predecessor size mismatch: {entry['path']}")
    if sha256(path) != entry["sha256"]:
        fail(f"predecessor digest mismatch: {entry['path']}")
print(f"PASS Course 5 predecessor handoff — {len(manifest['files'])} exact files")
