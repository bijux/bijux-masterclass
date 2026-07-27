#!/usr/bin/env python3
"""Render a small report whose meaning depends on source and policy files."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = [
        line.strip()
        for line in args.source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    threshold = args.policy.read_text(encoding="utf-8").strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        f"records={','.join(records)}\nthreshold={threshold}\n",
        encoding="utf-8",
    )
    print(f"rendered {args.output} with threshold={threshold}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
