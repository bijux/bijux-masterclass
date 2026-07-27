#!/usr/bin/env python3
"""Advance state for the selftest's deliberately dishonest hidden input."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def advance(path: Path) -> int:
    try:
        current = int(path.read_text(encoding="utf-8").strip())
    except FileNotFoundError:
        current = 0
    except ValueError as error:
        raise ValueError(f"hidden-input state is not an integer: {path}") from error

    value = current + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    candidate = path.with_name(f".{path.name}.candidate")
    candidate.write_text(f"{value}\n", encoding="utf-8")
    os.replace(candidate, path)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        value = advance(Path(args.state))
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print(value)


if __name__ == "__main__":
    main()
