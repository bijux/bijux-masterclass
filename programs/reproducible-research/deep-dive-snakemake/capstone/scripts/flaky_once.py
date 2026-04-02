#!/usr/bin/env python3
"""Write an attempt marker and fail on the first Snakemake attempt."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output file to write")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    attempt = int(os.environ.get("SNAKEMAKE_ATTEMPT", "1"))
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"attempt={attempt}\n", encoding="utf-8")

    if attempt == 1:
        print("Failing on attempt 1 (intentional).", file=sys.stderr)
        return 42

    print("Succeeded on attempt >=2.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
