#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


files: list[dict[str, object]] = []
for path in sorted(candidate for candidate in ROOT.rglob("*") if candidate.is_file()):
    if excluded(path):
        continue
    files.append(
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mode": oct(path.stat().st_mode & 0o777),
        }
    )

manifest = {
    "schemaVersion": "1.0",
    "course": "platform-engineering-course-05",
    "files": files,
}
raw = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
(ROOT / "MANIFEST.json").write_text(raw, encoding="utf-8")
(ROOT / "MANIFEST.sha256").write_text(
    hashlib.sha256((ROOT / "MANIFEST.json").read_bytes()).hexdigest()
    + "  MANIFEST.json\n",
    encoding="utf-8",
)
print(f"PASS course manifest — {len(files)} files")
