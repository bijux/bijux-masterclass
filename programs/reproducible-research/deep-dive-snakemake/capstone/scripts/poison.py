#!/usr/bin/env python3
"""Write a plausible partial output and then fail."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Output file to poison")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("PARTIAL\n", encoding="utf-8")
    print("Wrote PARTIAL then crashing.", file=sys.stderr)
    return 13


if __name__ == "__main__":
    raise SystemExit(main())
