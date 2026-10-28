#!/usr/bin/env python3
from common import ROOT, fail, load_json
base=ROOT/'capstone/shared/vectors'; files=sorted(base.glob('*.json')); cases=0
if len(files)!=5: fail(f"expected 5 vector files, got {len(files)}")
for p in files:
    data=load_json(p)
    if not isinstance(data.get('cases'),list) or not data['cases']: fail(f"invalid vectors {p.name}")
    cases+=len(data['cases'])
print(f"PASS shared vectors — {len(files)} files, {cases} cases")
