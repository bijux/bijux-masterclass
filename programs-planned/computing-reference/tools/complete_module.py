#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from course_validation.completion import CompletionError, complete_module

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and transition one planned module to complete"
    )
    parser.add_argument("module_id", help="canonical identifier such as PLS-001")
    args = parser.parse_args()
    try:
        outcome = complete_module(ROOT, args.module_id)
    except CompletionError as error:
        print(f"FAIL: {error}")
        raise SystemExit(1) from error
    print(f"PASS: {outcome.module_id} transitioned from planned to complete")
    print(f"Chapter: {outcome.chapter_path.relative_to(ROOT)}")
    print(f"Evidence: {outcome.evidence_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
