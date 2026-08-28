#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from course_validation.audit import audit_modules

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a canonical module scope")
    selectors = parser.add_mutually_exclusive_group()
    selectors.add_argument("--program", help="program code such as PLS")
    selectors.add_argument(
        "--module-number",
        type=int,
        choices=range(1, 101),
        metavar="1..100",
        help="audit one horizontal set across all 30 programs",
    )
    parser.add_argument("--level", type=int, choices=(1, 2))
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="fail when any selected manifest row remains planned",
    )
    args = parser.parse_args()
    if args.module_number is not None and args.level is not None:
        parser.error("--level cannot be combined with --module-number")

    result, report, path = audit_modules(
        ROOT,
        program=args.program,
        level=args.level,
        module_number=args.module_number,
        require_complete=args.require_complete,
    )
    counts = report.counts
    print(f"Scope: {report.scope}")
    print(f"Expected modules: {report.expected_modules}")
    print(
        "Modules: "
        f"{counts['passed']} passed, {counts['failed']} failed, "
        f"{counts['skipped']} skipped, {counts['unavailable']} unavailable"
    )
    print(f"Report: {path.relative_to(ROOT)}")
    if not result.ok:
        for issue in result.issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
