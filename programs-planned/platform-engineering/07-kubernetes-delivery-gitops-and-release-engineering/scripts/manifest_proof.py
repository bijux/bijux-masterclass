#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from common import ROOT, excluded, fail, load_json
manifest=load_json(ROOT/'MANIFEST.json'); listed=set()
for e in manifest['files']:
    listed.add(e['path']); p=ROOT/e['path']
    if not p.is_file() or p.stat().st_size!=e['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256'] or oct(p.stat().st_mode&0o777)!=e['mode']:
        fail(f"manifest mismatch: {e['path']}")
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and not excluded(p)}
if actual!=listed: fail(f"inventory mismatch added={sorted(actual-listed)[:8]} missing={sorted(listed-actual)[:8]}")
print(f"PASS exact course manifest — {len(listed)} files")
