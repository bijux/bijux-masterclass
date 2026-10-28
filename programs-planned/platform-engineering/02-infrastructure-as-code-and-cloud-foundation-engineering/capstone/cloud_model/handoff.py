from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .identity import digest_file


def build_manifest(root: Path, *, exclude: set[str] | None = None) -> dict[str, Any]:
    exclude = exclude or set()
    files: list[dict[str, Any]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        if rel in exclude:
            continue
        files.append({"path": rel, "sha256": digest_file(path), "bytes": path.stat().st_size})
    return {"schemaVersion": "1.0", "files": files}


def verify_manifest(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {row["path"]: row for row in manifest.get("files", [])}
    for rel, row in expected.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"missing: {rel}")
            continue
        if digest_file(path) != row["sha256"]:
            errors.append(f"digest mismatch: {rel}")
    return errors


def write_manifest(root: Path, path: Path) -> None:
    path.write_text(json.dumps(build_manifest(root, exclude={path.name}), indent=2, sort_keys=True) + "\n")
