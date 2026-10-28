#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(x for x in ROOT.rglob("*") if x.is_file()):
    rel=p.relative_to(ROOT).as_posix()
    if p.parent == ROOT and p.name in {"MANIFEST.json","MANIFEST.sha256"}: continue
    if any(part in {"__pycache__",".pytest_cache","site","site-program"} for part in p.parts): continue
    if rel.startswith("04-kubernetes-architecture-and-workload-engineering/capstone/reports/") and p.name!="README.md": continue
    if p.name=="atlas-controller" and p.parent.name=="controller-go": continue
    files.append({"path":rel,"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"mode":oct(p.stat().st_mode&0o777)})
raw=json.dumps({"schemaVersion":"1.0","program":"platform-engineering-course-04-overlay","files":files},indent=2,sort_keys=True)+"\n"
(ROOT/"MANIFEST.json").write_text(raw)
(ROOT/"MANIFEST.sha256").write_text(hashlib.sha256((ROOT/"MANIFEST.json").read_bytes()).hexdigest()+"  MANIFEST.json\n")
print(f"PASS program overlay manifest — {len(files)} files")
