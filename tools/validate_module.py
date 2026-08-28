#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from course_validation.blueprint import validate_blueprint
from course_validation.chapter import validate_chapter

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate one canonical course module")
    parser.add_argument("module_id", help="canonical identifier such as PLS-001")
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="validate a draft against a planned manifest row",
    )
    args = parser.parse_args()
    blueprint_result, _ = validate_blueprint(ROOT)
    if not blueprint_result.ok:
        for issue in blueprint_result.issues:
            print(f"FAIL: blueprint: {issue}")
        raise SystemExit(1)
    result = validate_chapter(ROOT, args.module_id, allow_draft=args.allow_draft)
    if not result.ok:
        for issue in result.issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print(f"PASS: {args.module_id}")


if __name__ == "__main__":
    main()
