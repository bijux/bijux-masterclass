#!/usr/bin/env python3
from common import ROOT, fail, load_json

items = load_json(ROOT / "capstone" / "planted-defects" / "defects.json")["defects"]
if len(items) != 10 or len({item["id"] for item in items}) != 10:
    fail("expected ten unique planted defects")
if any(not item.get("proof") for item in items):
    fail("planted defect lacks a rejecting proof")
for item in items:
    if not (ROOT / "capstone" / "planted-defects" / f"{item['id'].lower()}.json").is_file():
        fail(f"missing individual defect fixture {item['id']}")
print("PASS planted data defects — 10 mapped to rejecting proofs")
