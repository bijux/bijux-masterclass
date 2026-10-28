#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import yaml

from common import ROOT, fail


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key {key}")
        result[key] = value
    return result


class UniqueLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)
counts = {"json": 0, "yaml": 0}
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    try:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_json)
            counts["json"] += 1
        elif path.suffix in {".yaml", ".yml"}:
            list(yaml.load_all(path.read_text(encoding="utf-8"), Loader=UniqueLoader))
            counts["yaml"] += 1
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
print(f"PASS duplicate-key-aware data parsing — {counts['json']} JSON, {counts['yaml']} YAML")
