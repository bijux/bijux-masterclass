#!/usr/bin/env python3
from common import ROOT, fail, load_json, sha256

base = ROOT / "capstone" / "handoff"
manifest = load_json(base / "MANIFEST.json")
for entry in manifest["files"]:
    path = base / entry["path"]
    if not path.is_file():
        fail(f"handoff file missing: {entry['path']}")
    if path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
        fail(f"handoff mismatch: {entry['path']}")
print(f"PASS Course 7 handoff — {len(manifest['files'])} exact files")
