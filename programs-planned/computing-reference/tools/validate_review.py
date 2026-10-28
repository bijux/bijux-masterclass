#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from course_validation.review import validate_module_review

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate one module review record")
    parser.add_argument("module_id", help="canonical identifier such as PLS-001")
    args = parser.parse_args()
    result = validate_module_review(ROOT, args.module_id)
    if not result.ok:
        for issue in result.issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print(f"PASS: {args.module_id} review evidence")


if __name__ == "__main__":
    main()
