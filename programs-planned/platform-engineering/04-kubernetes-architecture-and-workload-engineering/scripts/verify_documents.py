#!/usr/bin/env python3
from __future__ import annotations
from common import COURSE, fail, passed
from pathlib import Path
import ast, json, re, tomllib, yaml

class UniqueKeyLoader(yaml.SafeLoader): pass

def construct_mapping(loader, node, deep=False):
    mapping={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in mapping: raise ValueError(f"duplicate YAML key {key!r}")
        mapping[key]=loader.construct_object(value_node,deep=deep)
    return mapping
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

counts={"json":0,"yaml":0,"toml":0,"python":0,"shell":0}
for path in sorted(COURSE.rglob("*")):
    if not path.is_file(): continue
    if any(part in {".git","__pycache__",".pytest_cache"} for part in path.parts): continue
    try:
        if path.suffix==".json": json.loads(path.read_text()); counts["json"]+=1
        elif path.suffix in {".yaml",".yml"}:
            list(yaml.load_all(path.read_text(), Loader=UniqueKeyLoader)); counts["yaml"]+=1
        elif path.suffix==".toml": tomllib.loads(path.read_text()); counts["toml"]+=1
        elif path.suffix==".py": ast.parse(path.read_text()); counts["python"]+=1
    except Exception as exc: fail(f"parse failure {path.relative_to(COURSE)}: {exc}")
passed("document and Python parsing — "+", ".join(f"{k}={v}" for k,v in counts.items()))
