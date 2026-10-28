#!/usr/bin/env python3
from __future__ import annotations

import yaml
from common import ROOT, fail

resources = []
for path in (ROOT / "capstone" / "manifests").rglob("*.yaml"):
    for document in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if isinstance(document, dict) and document.get("kind"):
            resources.append((path, document))
kinds = {str(item[1]["kind"]) for item in resources}
required = {
    "StorageClass", "PersistentVolumeClaim", "StatefulSet", "Service",
    "PodDisruptionBudget", "CronJob", "NetworkPolicy", "CSIDriver",
    "CSIStorageCapacity", "VolumeSnapshotClass", "VolumeSnapshot",
}
missing = required - kinds
if missing:
    fail(f"required storage resources missing: {sorted(missing)}")
for path, resource in resources:
    metadata = resource.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("name"):
        fail(f"resource without metadata.name in {path.relative_to(ROOT)}")
for path, resource in resources:
    if resource.get("kind") == "StorageClass":
        if resource.get("volumeBindingMode") != "WaitForFirstConsumer" and "immediate-binding" not in path.name:
            fail(f"production StorageClass lacks WaitForFirstConsumer: {path.relative_to(ROOT)}")
    if resource.get("kind") == "StatefulSet":
        templates = resource.get("spec", {}).get("volumeClaimTemplates", [])
        if not templates:
            fail("StatefulSet has no volumeClaimTemplates")
print(f"PASS Kubernetes storage manifest inventory — {len(resources)} resources")
