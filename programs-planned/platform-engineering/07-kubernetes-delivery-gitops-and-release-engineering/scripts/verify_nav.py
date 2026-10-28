#!/usr/bin/env python3
from __future__ import annotations
import yaml
from common import ROOT, fail
config=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
listed=[]
def walk(node):
    if isinstance(node,str): listed.append(node)
    elif isinstance(node,list):
        for x in node: walk(x)
    elif isinstance(node,dict):
        for x in node.values(): walk(x)
walk(config.get('nav',[]))
expected={p.relative_to(ROOT/'course-book').as_posix() for p in (ROOT/'course-book').rglob('*.md')}
actual=set(listed)
if actual!=expected: fail(f"nav mismatch missing={sorted(expected-actual)[:8]} extra={sorted(actual-expected)[:8]}")
if len(listed)!=len(actual): fail('duplicate MkDocs nav path')
print(f"PASS exact MkDocs navigation — {len(actual)} course-book pages")
