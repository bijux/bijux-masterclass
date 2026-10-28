#!/usr/bin/env python3
import json
from common import ROOT,fail
from pathlib import Path
import sys
sys.path.insert(0,str(ROOT/'capstone'))
from atlas_net.release import Gate,classify
for path in sorted((ROOT/'capstone'/'releases').glob('*.json')):
    data=json.loads(path.read_text()); gates=[Gate(g['name'],g['state'],g.get('blocker',True)) for g in data['gates']]
    actual=classify(gates)
    if actual!=data['expected']: fail(f'{path.name}: expected {data["expected"]}, got {actual}')
print('PASS release classification — accepted, rejected, not-executed')
