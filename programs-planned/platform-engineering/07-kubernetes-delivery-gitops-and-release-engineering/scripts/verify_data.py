#!/usr/bin/env python3
from __future__ import annotations
import json, tomllib, yaml
from common import ROOT, fail

def unique_json(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError(f"duplicate key {k}")
        out[k]=v
    return out
class UniqueLoader(yaml.SafeLoader): pass
def construct_mapping(loader,node,deep=False):
    out={}
    for kn,vn in node.value:
        k=loader.construct_object(kn,deep=deep)
        if k in out: raise ValueError(f"duplicate key {k}")
        out[k]=loader.construct_object(vn,deep=deep)
    return out
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,construct_mapping)
counts={'json':0,'yaml':0,'toml':0}
for path in ROOT.rglob('*'):
    if not path.is_file() or any(x in path.parts for x in {'__pycache__','.pytest_cache','site'}): continue
    rel=path.relative_to(ROOT).as_posix()
    if '/charts/' in '/'+rel and '/templates/' in '/'+rel: continue
    try:
        if path.suffix=='.json': json.loads(path.read_text(),object_pairs_hook=unique_json); counts['json']+=1
        elif path.suffix in {'.yaml','.yml'}: list(yaml.load_all(path.read_text(),Loader=UniqueLoader)); counts['yaml']+=1
        elif path.suffix=='.toml': tomllib.loads(path.read_text()); counts['toml']+=1
    except Exception as e: fail(f"{rel}: {e}")
print(f"PASS duplicate-key-aware data parsing — {counts['json']} JSON, {counts['yaml']} YAML, {counts['toml']} TOML")
