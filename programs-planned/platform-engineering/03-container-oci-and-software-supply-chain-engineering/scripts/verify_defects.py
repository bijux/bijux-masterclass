#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

COURSE=Path(__file__).resolve().parents[1]
files=sorted((COURSE/"capstone/planted-defects").glob("*.json"))
if len(files)!=10: raise SystemExit(f"expected 10 defects, got {len(files)}")
required={"id","title","expectedGate"}
for path in files:
    value=json.loads(path.read_text())
    missing=required-set(value)
    if missing: raise SystemExit(f"{path.name} missing {sorted(missing)}")
    if not value.get("expectedDecision") in {"rejected","review-required"}:
        raise SystemExit(f"{path.name} lacks rejecting decision")
print("PASS planted defects — 10 declared rejecting or review gates")
