from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    policy = read_json(args.policy)
    allowed = {int(value) for value in policy["allowed_severity"]}
    with args.input.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    severities = [int(row["severity"]) for row in rows]
    unexpected = sorted(set(severities) - allowed)
    if unexpected:
        raise ValueError(f"severity values outside policy: {unexpected}")

    summary = {
        "record_count": len(rows),
        "severity_total": sum(severities),
        "weekend_handoffs": sum(
            int(row["weekend_handoff"]) for row in rows
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
