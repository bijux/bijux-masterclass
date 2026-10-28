#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    "__pycache__", ".pytest_cache", "node_modules", "dist", "site", ".tmp",
}
EXCLUDED_ROOT_FILES = {"MANIFEST.json", "MANIFEST.sha256", ".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".log"}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def included(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if rel.as_posix() in EXCLUDED_ROOT_FILES:
        return False
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()

def build(root: Path) -> dict:
    files = []
    for path in sorted(root.rglob("*")):
        if not included(path, root):
            continue
        mode = "0755" if os.access(path, os.X_OK) else "0644"
        files.append({
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": digest(path),
            "mode": mode,
        })
    return {"algorithm":"sha256","files":files}

def write_manifest(root: Path) -> None:
    manifest = build(root)
    body = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    path = root / "MANIFEST.json"
    path.write_text(body)
    (root / "MANIFEST.sha256").write_text(
        f"{hashlib.sha256(body.encode()).hexdigest()}  MANIFEST.json\n"
    )
    print(f"manifested {len(manifest['files'])} files under {root}")

def main() -> None:
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    write_manifest(target)

if __name__ == "__main__":
    main()
