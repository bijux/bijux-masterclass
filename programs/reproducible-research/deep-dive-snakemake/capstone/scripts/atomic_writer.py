#!/usr/bin/env python3
"""Write a final output atomically through a temporary file."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Final output path")
    parser.add_argument(
        "--fail-before-rename",
        action="store_true",
        help="Exit after writing the temporary file but before promotion",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    final_output = args.output
    temp_output = final_output.with_suffix(final_output.suffix + ".tmp")
    final_output.parent.mkdir(parents=True, exist_ok=True)
    temp_output.write_text("complete\n", encoding="utf-8")

    if args.fail_before_rename:
        print("Crashing before rename.", file=sys.stderr)
        return 17

    temp_output.replace(final_output)
    print(f"Wrote {final_output} atomically.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
