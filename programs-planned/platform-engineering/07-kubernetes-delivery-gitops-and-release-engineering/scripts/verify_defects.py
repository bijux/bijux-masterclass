#!/usr/bin/env python3
from common import ROOT, fail, load_json
files=sorted((ROOT/'capstone/planted-defects').glob('DELIVERY-*.json'))
if len(files)!=10: fail(f"expected 10 defects, got {len(files)}")
ids=set()
for p in files:
    d=load_json(p)
    if d['id'] in ids or d.get('expectedDecision')!='rejected' or not d.get('expectedControl'): fail(f"invalid defect {p.name}")
    ids.add(d['id'])
print('PASS ten planted delivery defects with named rejecting controls')
