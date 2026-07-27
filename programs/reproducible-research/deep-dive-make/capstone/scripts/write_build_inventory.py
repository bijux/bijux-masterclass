#!/usr/bin/env python3
"""Write a stable inventory for declared build artifacts."""

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


def select_paths(root: Path, exact_paths: list[str], patterns: list[str]) -> list[Path]:
    selected: set[Path] = set()
    for relative_name in exact_paths:
        path = root / relative_name
        if not path.is_file():
            raise ValueError(f"declared artifact is missing or not a regular file: {relative_name}")
        selected.add(path)

    for pattern in patterns:
        matches = [path for path in root.glob(pattern) if path.is_file()]
        if not matches:
            raise ValueError(f"artifact pattern matched no regular files: {pattern}")
        selected.update(matches)

    if not selected:
        raise ValueError("artifact inventory must declare at least one path or pattern")
    return sorted(selected, key=lambda path: path.relative_to(root).as_posix())


def build_inventory(root: Path, paths: list[Path]) -> dict[str, object]:
    artifacts: list[dict[str, object]] = []
    identity_lines: list[str] = []
    for path in paths:
        relative_name = path.relative_to(root).as_posix()
        digest = sha256(path)
        size = path.stat().st_size
        artifacts.append({"path": relative_name, "bytes": size, "sha256": digest})
        identity_lines.append(f"{relative_name}\t{size}\t{digest}\n")

    aggregate = hashlib.sha256("".join(identity_lines).encode("utf-8")).hexdigest()
    return {
        "schema": "deep-dive-make/build-artifact-inventory",
        "artifact_count": len(artifacts),
        "aggregate_sha256": aggregate,
        "artifacts": artifacts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--pattern", action="append", default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output)
    try:
        paths = select_paths(root, args.path, args.pattern)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    inventory = build_inventory(root, paths)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
