#!/usr/bin/env python3
"""Combine candidate and install evidence into one bounded acceptance record."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def read_passing_report(path: Path) -> dict[str, object]:
    report = json.loads(path.read_text(encoding="utf-8"))
    checks = report.get("checks")
    if not isinstance(checks, dict) or not checks or set(checks.values()) != {"PASS"}:
        raise ValueError(f"report contains an incomplete gate: {path}")
    return report


def write_report(output: Path, report: dict[str, object]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    staged_output = output.with_name(f".{output.name}.evidence.{os.getpid()}")
    try:
        staged_output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        os.replace(staged_output, output)
    finally:
        staged_output.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-report", required=True)
    parser.add_argument("--install-report", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    candidate_report = read_passing_report(Path(args.candidate_report))
    install_report = read_passing_report(Path(args.install_report))

    candidate_identity = (
        candidate_report.get("candidate"),
        candidate_report.get("sha256"),
    )
    install_identity = (
        install_report.get("candidate"),
        install_report.get("sha256"),
    )
    if candidate_identity != install_identity:
        raise ValueError("candidate and install reports name different bytes")

    write_report(
        Path(args.output),
        {
            "candidate": candidate_identity[0],
            "checks": {
                "candidate_contract": "PASS",
                "contained_install": "PASS",
                "install_convergence": "PASS",
            },
            "publication": "NOT_ATTEMPTED",
            "scope": "internal capstone transfer and install rehearsal",
            "sha256": candidate_identity[1],
        },
    )


def main() -> int:
    try:
        run()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1
    print("PASS: release acceptance is bound to candidate and install evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
