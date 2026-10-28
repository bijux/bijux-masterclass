#!/usr/bin/env python3
from common import COURSE, fail, load_json, passed, sha256
manifest=load_json(COURSE/"MANIFEST.json")
listed=set()
for entry in manifest["files"]:
    listed.add(entry["path"]); path=COURSE/entry["path"]
    if not path.is_file(): fail(f"missing manifest file {entry['path']}")
    if path.stat().st_size!=entry["bytes"] or sha256(path)!=entry["sha256"]: fail(f"manifest mismatch {entry['path']}")
    if oct(path.stat().st_mode & 0o777) != entry.get("mode"): fail(f"mode mismatch {entry['path']}")
actual=set()
for path in COURSE.rglob("*"):
    if not path.is_file(): continue
    rel=path.relative_to(COURSE).as_posix()
    if path.parent == COURSE and path.name in {"MANIFEST.json","MANIFEST.sha256"}: continue
    if any(part in {"__pycache__",".pytest_cache","site"} for part in path.parts): continue
    if rel.startswith("capstone/reports/") and path.name not in {"README.md"}: continue
    if path.name=="atlas-controller" and path.parent.name=="controller-go": continue
    actual.add(rel)
if actual!=listed: fail(f"manifest inventory mismatch missing={sorted(actual-listed)} stale={sorted(listed-actual)}")
passed(f"exact course manifest — {len(listed)} files")
