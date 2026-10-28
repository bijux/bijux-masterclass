#!/usr/bin/env python3
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=["python", "typescript"], required=True)
    parser.add_argument("--release", choices=["1.0", "1.1"], default="1.0")
    args = parser.parse_args()
    runner = ROOT / "capstone" / "tests" / "runtime" / "proof_runner.py"
    raise SystemExit(
        subprocess.call(
            [sys.executable, str(runner), "postgres", "--track", args.track, "--release", args.release]
        )
    )


if __name__ == "__main__":
    main()
