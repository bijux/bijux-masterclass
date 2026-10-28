#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import ROOT, fail


def excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if path.parent == ROOT and path.name in {"MANIFEST.json", "MANIFEST.sha256"}:
        return True
    if any(part in {"__pycache__", ".pytest_cache", "site"} for part in path.parts):
        return True
    if rel.startswith("capstone/reports/generated/"):
        return True
    if path.name in {"atlas-cni-lab", "atlas-netprobe"} and path.parent.name in {
        "atlas-cni-lab",
        "atlas-netprobe",
    }:
        return True
    return False


manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
listed: set[str] = set()
for entry in manifest["files"]:
    listed.add(entry["path"])
    path = ROOT / entry["path"]
    if not path.is_file():
        fail(f"missing manifest file: {entry['path']}")
    if path.stat().st_size != entry["bytes"]:
        fail(f"size mismatch: {entry['path']}")
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
        fail(f"digest mismatch: {entry['path']}")
    if oct(path.stat().st_mode & 0o777) != entry["mode"]:
        fail(f"mode mismatch: {entry['path']}")

actual = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file() and not excluded(path)
}
if actual != listed:
    fail(
        "inventory mismatch "
        f"added={sorted(actual - listed)[:10]} "
        f"missing={sorted(listed - actual)[:10]}"
    )
print(f"PASS exact course manifest — {len(listed)} files")
