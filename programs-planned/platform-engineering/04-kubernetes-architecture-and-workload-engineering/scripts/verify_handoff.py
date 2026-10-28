#!/usr/bin/env python3
from common import CAPSTONE, fail, load_json, passed, sha256
root=CAPSTONE/"handoff"
manifest=load_json(root/"MANIFEST.json")
for entry in manifest["files"]:
    path=root/entry["path"]
    if not path.is_file(): fail(f"missing handoff file {entry['path']}")
    if path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
        fail(f"handoff mismatch {entry['path']}")
passed(f"Course 5 handoff integrity — {len(manifest['files'])} files")
