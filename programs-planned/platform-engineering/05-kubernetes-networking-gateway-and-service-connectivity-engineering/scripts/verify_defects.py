#!/usr/bin/env python3
import json
from common import ROOT,fail
items=json.loads((ROOT/'capstone'/'planted-defects'/'defects.json').read_text())['defects']
if len(items)!=10 or len({x['id'] for x in items})!=10: fail('expected ten unique planted defects')
if any(not x.get('proof') for x in items): fail('defect without proof')
print('PASS planted defect map — 10 defects')
