#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, fail, load_json

files = sorted((ROOT / "capstone" / "shared" / "vectors").glob("*.json"))
if len(files) != 10:
    fail(f"expected 10 vector files, got {len(files)}")
cases = 0
for path in files:
    document = load_json(path)
    if isinstance(document, list):
        cases += len(document)
    elif isinstance(document, dict):
        for value in document.values():
            if isinstance(value, list):
                cases += len(value)
        if not document:
            fail(f"empty vector document {path.name}")
    else:
        fail(f"unsupported vector shape {path.name}")
if cases < 20:
    fail(f"too few shared vector cases: {cases}")
print(f"PASS shared storage vectors — {len(files)} files, {cases} identified cases")
