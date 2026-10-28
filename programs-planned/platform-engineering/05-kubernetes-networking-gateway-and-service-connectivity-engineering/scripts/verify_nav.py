#!/usr/bin/env python3
import yaml
from common import ROOT,fail
cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
seen=[]
def walk(node):
    if isinstance(node,str): seen.append(node)
    elif isinstance(node,list):
        for x in node: walk(x)
    elif isinstance(node,dict):
        for x in node.values(): walk(x)
walk(cfg['nav'])
missing=[x for x in seen if not (ROOT/'course-book'/x).is_file()]
if missing: fail(f'nav missing files {missing[:5]}')
all_pages={p.relative_to(ROOT/'course-book').as_posix() for p in (ROOT/'course-book').rglob('*.md')}
if set(seen)!=all_pages: fail(f'nav coverage differs: omitted={sorted(all_pages-set(seen))[:5]} extra={sorted(set(seen)-all_pages)[:5]}')
print(f'PASS exact MkDocs navigation — {len(seen)} pages')
