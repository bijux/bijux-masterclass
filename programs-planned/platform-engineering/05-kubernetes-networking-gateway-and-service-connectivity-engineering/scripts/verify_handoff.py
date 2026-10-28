#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
from common import ROOT,fail
base=ROOT/'capstone'/'handoff'; manifest=json.loads((base/'MANIFEST.json').read_text())
for entry in manifest['files']:
    path=base/entry['path']
    if not path.is_file() or path.stat().st_size!=entry['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']: fail(f'handoff mismatch {entry["path"]}')
print(f"PASS Course 6 handoff — {len(manifest['files'])} exact files")
