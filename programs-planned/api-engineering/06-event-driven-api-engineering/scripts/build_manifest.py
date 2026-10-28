#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_NAMES = {"MANIFEST.json", "MANIFEST.sha256", ".DS_Store"}
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", "node_modules", "dist", ".venv", "venv", "work", "site"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


files = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT)
    if relative.as_posix() in EXCLUDED_NAMES:
        continue
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        continue
    mode = stat.S_IMODE(path.stat().st_mode)
    files.append({
        "path": relative.as_posix(),
        "size": path.stat().st_size,
        "sha256": digest(path),
        "mode": f"{mode:04o}",
    })
manifest = {
    "schema": "bijux-course-manifest-1",
    "course": "06-event-driven-api-engineering",
    "files": files,
}
manifest_path = ROOT / "MANIFEST.json"
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
checksum = digest(manifest_path)
(ROOT / "MANIFEST.sha256").write_text(f"{checksum}  MANIFEST.json\n", encoding="utf-8")
print(f"wrote manifest for {len(files)} files")
