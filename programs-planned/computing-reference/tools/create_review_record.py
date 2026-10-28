#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from course_validation.review import create_review_template

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create one incomplete module review record")
    parser.add_argument("module_id", help="canonical identifier such as PLS-001")
    args = parser.parse_args()
    try:
        path = create_review_template(ROOT, args.module_id)
    except (FileExistsError, OSError, UnicodeError, ValueError) as error:
        print(f"FAIL: {error}")
        raise SystemExit(1) from error
    print(f"CREATED: {path.relative_to(ROOT)}")
    print("INCOMPLETE: record every applicable review outcome before completion")


if __name__ == "__main__":
    main()
