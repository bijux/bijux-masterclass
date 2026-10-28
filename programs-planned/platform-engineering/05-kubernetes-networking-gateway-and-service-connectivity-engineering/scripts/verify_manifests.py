#!/usr/bin/env python3
from __future__ import annotations

import yaml

from common import ROOT, fail

resources: list[dict[str, object]] = []
for path in (ROOT / "capstone" / "manifests").rglob("*.yaml"):
    for document in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if isinstance(document, dict) and document.get("kind"):
            resources.append(document)

kinds = {str(resource["kind"]) for resource in resources}
required = {"Service", "NetworkPolicy", "Gateway", "HTTPRoute"}
missing = required - kinds
if missing:
    fail(f"production-intent manifest kinds missing: {sorted(missing)}")

for resource in resources:
    metadata = resource.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("name"):
        fail(f"resource without metadata.name: {resource.get('kind')}")

print(f"PASS Kubernetes/Gateway manifest inventory — {len(resources)} resources")
