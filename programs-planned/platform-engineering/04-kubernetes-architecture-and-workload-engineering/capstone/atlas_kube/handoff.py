from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    files = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "MANIFEST.json"):
        files.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    return {"schemaVersion": "1.0", "files": files}


def write_manifest(root: Path) -> Path:
    target = root / "MANIFEST.json"
    target.write_text(json.dumps(build_manifest(root), indent=2, sort_keys=True) + "\n")
    return target


def verify_manifest(root: Path) -> list[str]:
    manifest = json.loads((root / "MANIFEST.json").read_text())
    errors = []
    for entry in manifest["files"]:
        path = root / entry["path"]
        if not path.is_file():
            errors.append(f"missing {entry['path']}")
        elif path.stat().st_size != entry["bytes"]:
            errors.append(f"size mismatch {entry['path']}")
        elif sha256(path) != entry["sha256"]:
            errors.append(f"digest mismatch {entry['path']}")
    return errors
