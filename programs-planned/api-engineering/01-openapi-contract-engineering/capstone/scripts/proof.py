#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
REPORTS = CAPSTONE / "reports"

STEPS = [
    "core-proof",
    "python-test",
    "python-check",
    "typescript",
    "lint-contract",
    "clients-generate",
    "python-live",
    "typescript-live",
    "prism-smoke",
    "schemathesis",
    "oasdiff",
    "docs-build",
]


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    results = []
    for target in STEPS:
        command = ["make", "-C", str(CAPSTONE), target]
        completed = subprocess.run(command, text=True, capture_output=True)
        result = {
            "target": target,
            "passed": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-12000:],
            "stderr": completed.stderr[-12000:],
        }
        results.append(result)
        marker = "PASS" if result["passed"] else "FAIL"
        print(f"{marker} {target}")
        if not result["passed"]:
            break
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "passed": len(results) == len(STEPS) and all(item["passed"] for item in results),
        "steps": results,
    }
    output = REPORTS / "proof.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"proof report: {output}")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
