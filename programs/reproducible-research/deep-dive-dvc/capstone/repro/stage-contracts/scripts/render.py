#!/usr/bin/env python3
"""Render tiny artifacts for stage-contract evidence."""

from __future__ import annotations

import argparse
from pathlib import Path


def source_values(path: Path) -> list[int]:
    return [
        int(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def multiplier(path: Path) -> int:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("multiplier:"):
            return int(line.split(":", maxsplit=1)[1].strip())
    raise ValueError(f"settings.multiplier is missing from {path}")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    input_parser = subparsers.add_parser("input")
    input_parser.add_argument("--source", type=Path, required=True)
    input_parser.add_argument("--policy", type=Path, required=True)
    input_parser.add_argument("--output", type=Path, required=True)

    param_parser = subparsers.add_parser("param")
    param_parser.add_argument("--source", type=Path, required=True)
    param_parser.add_argument("--params", type=Path, required=True)
    param_parser.add_argument("--output", type=Path, required=True)

    sidecar_parser = subparsers.add_parser("sidecar")
    sidecar_parser.add_argument("--source", type=Path, required=True)
    sidecar_parser.add_argument("--output", type=Path, required=True)
    sidecar_parser.add_argument("--sidecar", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    values = source_values(args.source)

    if args.mode == "input":
        threshold = args.policy.read_text(encoding="utf-8").strip()
        write(args.output, f"total={sum(values)}\nthreshold={threshold}\n")
    elif args.mode == "param":
        factor = multiplier(args.params)
        write(args.output, f"total={sum(values)}\nmultiplier={factor}\nscore={sum(values) * factor}\n")
    else:
        write(args.output, f"total={sum(values)}\n")
        write(args.sidecar, f"records={len(values)}\n")

    print(f"rendered {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
