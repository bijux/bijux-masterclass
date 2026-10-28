#!/usr/bin/env python3
from common import ROOT, fail, load_json, sha256
base=ROOT/'capstone/handoff'; manifest=load_json(base/'MANIFEST.json')
for e in manifest['files']:
    p=base/e['path']
    if not p.is_file() or p.stat().st_size!=e['bytes'] or sha256(p)!=e['sha256']: fail(f"handoff mismatch {e['path']}")
if len(manifest['files'])!=11: fail(f"expected 11 handoff payload files, got {len(manifest['files'])}")
print('PASS Course 8 handoff — 11 exact payload files')
