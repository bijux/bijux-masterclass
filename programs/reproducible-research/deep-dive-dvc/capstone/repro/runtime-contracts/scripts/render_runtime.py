#!/usr/bin/env python3
"""Render a tiny result using a declared or process-level runtime policy."""

from __future__ import annotations

import argparse
import os
import platform
from pathlib import Path


def read_contract(path: Path) -> str:
    entries = dict(
        line.split("=", maxsplit=1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    )
    return entries["REPORT_STYLE"]


def render(total: int, style: str) -> str:
    if style == "dot":
        return f"{total:.2f}"
    if style == "comma":
        return f"{total:.2f}".replace(".", ",")
    raise ValueError(f"unsupported REPORT_STYLE: {style}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    policy = parser.add_mutually_exclusive_group(required=True)
    policy.add_argument("--contract", type=Path)
    policy.add_argument("--environment-variable")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    values = [
        int(line)
        for line in args.source.read_text(encoding="utf-8").splitlines()
        if line
    ]
    style = (
        read_contract(args.contract)
        if args.contract
        else os.environ[args.environment_variable]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(
            [
                f"total={sum(values)}",
                f"style={style}",
                f"rendered={render(sum(values), style)}",
                f"python={platform.python_version()}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"rendered {args.output} with REPORT_STYLE={style}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
