#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

COURSE=Path(__file__).resolve().parents[1]

def verify(folder: Path, name: str) -> int:
    data=json.loads((folder/"MANIFEST.json").read_text())
    count=0
    for item in data["files"]:
        path=folder/item["path"]
        raw=path.read_bytes()
        if len(raw)!=item["bytes"] or hashlib.sha256(raw).hexdigest()!=item["sha256"]:
            raise SystemExit(f"{name} mismatch: {item['path']}")
        count+=1
    print(f"PASS {name} — {count} files")
    return count

verify(COURSE/"capstone/predecessor", "Course 2 predecessor")
verify(COURSE/"capstone/handoff", "Course 4 handoff")
