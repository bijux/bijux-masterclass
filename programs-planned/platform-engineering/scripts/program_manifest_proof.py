#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def excluded(p):
    rel=p.relative_to(ROOT).as_posix()
    if p.parent==ROOT and p.name in {"MANIFEST.json","MANIFEST.sha256"}: return True
    if any(part in {"__pycache__",".pytest_cache","site","site-program"} for part in p.parts): return True
    if rel.startswith("04-kubernetes-architecture-and-workload-engineering/capstone/reports/") and p.name!="README.md": return True
    if p.name=="atlas-controller" and p.parent.name=="controller-go": return True
    return False
manifest=json.loads((ROOT/"MANIFEST.json").read_text())
listed=set()
for e in manifest["files"]:
    listed.add(e["path"]); p=ROOT/e["path"]
    if not p.is_file() or p.stat().st_size!=e["bytes"] or hashlib.sha256(p.read_bytes()).hexdigest()!=e["sha256"] or oct(p.stat().st_mode&0o777)!=e.get("mode"):
        print("FAIL",e["path"]); sys.exit(1)
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and not excluded(p)}
if actual!=listed:
    print("FAIL inventory",sorted(actual-listed),sorted(listed-actual));sys.exit(1)
print(f"PASS exact program overlay manifest — {len(listed)} files")
