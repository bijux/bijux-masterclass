#!/usr/bin/env python3
from common import CAPSTONE, fail, load_json, passed, sha256
root=CAPSTONE/"predecessor"
manifest=load_json(root/"MANIFEST.json")
for entry in manifest["files"]:
    path=root/entry["path"]
    if not path.is_file(): fail(f"missing predecessor file {entry['path']}")
    if path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
        fail(f"predecessor mismatch {entry['path']}")
passed(f"Course 3 predecessor integrity — {len(manifest['files'])} files")
