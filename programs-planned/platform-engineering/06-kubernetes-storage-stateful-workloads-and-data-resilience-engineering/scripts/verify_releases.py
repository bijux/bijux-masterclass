#!/usr/bin/env python3
from __future__ import annotations

import sys
from common import ROOT, fail, load_json

sys.path.insert(0, str(ROOT / "capstone"))
from atlas_data.release import ReleaseEvaluator

evaluator = ReleaseEvaluator()
classified = {}
for path in sorted((ROOT / "capstone" / "releases").glob("*.json")):
    document = load_json(path)
    actual = evaluator.evaluate(document["evidence"]).decision
    expected = document["expected"]
    if actual != expected:
        fail(f"{path.name}: expected {expected}, got {actual}")
    classified[path.name] = actual
if "accepted" not in classified.values() or "rejected" not in classified.values() or "review-required" not in classified.values():
    fail("release fixtures do not cover accepted, rejected, and review-required")
print(f"PASS storage release classification — {len(classified)} candidates")
