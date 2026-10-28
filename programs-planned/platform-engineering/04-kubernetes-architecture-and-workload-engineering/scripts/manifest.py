#!/usr/bin/env python3
from __future__ import annotations
from common import COURSE, sha256, passed
from pathlib import Path
import json
EXCLUDED={"MANIFEST.json","MANIFEST.sha256"}
files=[]
for path in sorted(p for p in COURSE.rglob("*") if p.is_file()):
    rel=path.relative_to(COURSE).as_posix()
    if path.parent == COURSE and path.name in EXCLUDED: continue
    if any(part in {"__pycache__",".pytest_cache","site"} for part in path.parts): continue
    if rel.startswith("capstone/reports/") and path.name not in {"README.md"}: continue
    if path.name=="atlas-controller" and path.parent.name=="controller-go": continue
    files.append({"path":rel,"bytes":path.stat().st_size,"sha256":sha256(path),"mode":oct(path.stat().st_mode & 0o777)})
manifest={"schemaVersion":"1.0","course":"04-kubernetes-architecture-and-workload-engineering","files":files}
raw=json.dumps(manifest,indent=2,sort_keys=True)+"\n"
(COURSE/"MANIFEST.json").write_text(raw)
(COURSE/"MANIFEST.sha256").write_text(sha256(COURSE/"MANIFEST.json")+"  MANIFEST.json\n")
passed(f"course manifest written — {len(files)} files")
