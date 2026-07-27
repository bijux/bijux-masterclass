"""Classify a GNU Make trace as bounded, attributable planning evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


UPDATE_PATTERN = re.compile(
    r"^(?P<rule>[^:\n]+:\d+): update target '(?P<target>[^']+)' due to:"
)


def analyze(trace: str, *, route: str, state: str, focus: str, maximum: int) -> dict[str, object]:
    lines = trace.splitlines()
    updates = [match.groupdict() for line in lines if (match := UPDATE_PATTERN.match(line))]
    focus_updates = [update for update in updates if update["target"] == focus]
    checks = {
        "bounded_volume": len(lines) <= maximum,
        "focus_target_visible": bool(focus_updates),
        "rule_locations_visible": bool(updates),
    }
    return {
        "checks": checks,
        "focus_target": focus,
        "line_count": len(lines),
        "maximum_lines": maximum,
        "planned_targets": [update["target"] for update in updates],
        "result": "PASS" if all(checks.values()) else "FAIL",
        "route": route,
        "rule_locations": sorted({update["rule"] for update in updates}),
        "state": state,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--route", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--focus", required=True)
    parser.add_argument("--maximum-lines", type=int, required=True)
    arguments = parser.parse_args()
    report = analyze(
        arguments.trace.read_text(encoding="utf-8"),
        route=arguments.route,
        state=arguments.state,
        focus=arguments.focus,
        maximum=arguments.maximum_lines,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if report["result"] != "PASS":
        print("FAIL: trace evidence is incomplete or unbounded", file=sys.stderr)
        return 1
    print(f"PASS: wrote trace evidence to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
