#!/usr/bin/env python3
"""Write a portable SHA-256 sidecar for one release candidate."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidate = Path(args.candidate)
    output = Path(args.output)
    if not candidate.is_file():
        raise SystemExit(f"candidate is not a regular file: {candidate}")

    output.parent.mkdir(parents=True, exist_ok=True)
    staged_output = output.with_name(f".{output.name}.evidence.{os.getpid()}")
    try:
        staged_output.write_text(
            f"{sha256(candidate)}  {candidate.name}\n", encoding="utf-8"
        )
        os.replace(staged_output, output)
    finally:
        staged_output.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
