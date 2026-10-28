#!/usr/bin/env python3
"""Build an exact SHA-256 manifest for a course directory or handoff."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "__pycache__",
    "node_modules", "dist", "site", ".tmp",
}
ROOT_MANIFEST_NAMES = {"MANIFEST.json", "MANIFEST.sha256"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def eligible(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
        return False
    if len(relative.parts) == 1 and path.name in ROOT_MANIFEST_NAMES:
        return False
    return path.is_file()


def build(root: Path) -> dict[str, object]:
    files = []
    for path in sorted(root.rglob("*")):
        if eligible(path, root):
            files.append({
                "path": path.relative_to(root).as_posix(),
                "size": path.stat().st_size,
                "sha256": sha256(path),
            })
    return {
        "format": "bijux-course-manifest-v1",
        "root": root.name,
        "file_count": len(files),
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifest = build(root)
    manifest_path = root / "MANIFEST.json"
    digest_path = root / "MANIFEST.sha256"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    digest_path.write_text(f"{sha256(manifest_path)}  MANIFEST.json\n")
    print(f"wrote {manifest_path} — {manifest['file_count']} files")


if __name__ == "__main__":
    main()
