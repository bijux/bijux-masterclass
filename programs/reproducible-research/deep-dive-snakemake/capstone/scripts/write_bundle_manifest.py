#!/usr/bin/env python3
"""Write a stable inventory for a Snakemake capstone review bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(bundle_dir: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for path in sorted(candidate for candidate in bundle_dir.rglob("*") if candidate.is_file()):
        relative = path.relative_to(bundle_dir)
        files.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return {
        "bundle_dir": bundle_dir.resolve().as_posix(),
        "file_count": len(files),
        "files": files,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bundle_dir = Path(args.bundle_dir)
    output = Path(args.output)
    manifest_text = json.dumps(
        build_manifest(bundle_dir),
        indent=2,
        sort_keys=True,
    )
    output.write_text(f"{manifest_text}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
