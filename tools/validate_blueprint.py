#!/usr/bin/env python3
from pathlib import Path

from course_validation.blueprint import validate_blueprint

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    result, summary = validate_blueprint(ROOT)
    if not result.ok:
        for issue in result.issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print("PASS")
    print(f"Programs: {summary['programs']}")
    print(f"Modules: {summary['modules']}")
    print(f"Planned modules: {summary['planned_modules']}")
    print(f"Complete modules: {summary['complete_modules']}")

if __name__ == "__main__":
    main()
