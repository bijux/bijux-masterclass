#!/usr/bin/env python3
"""Create a deterministic incident risk summary from declared inputs."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path


def effective_threshold(cli_value: float | None) -> float:
    if cli_value is not None:
        return cli_value
    hidden_value = os.environ.get("RISK_THRESHOLD")
    if hidden_value is None:
        raise SystemExit(
            "provide --threshold or set RISK_THRESHOLD for the hidden-control "
            "teaching case"
        )
    return float(hidden_value)


def score(input_path: Path, threshold: float) -> dict[str, object]:
    with input_path.open(newline="", encoding="utf-8") as handle:
        observations = list(csv.DictReader(handle))

    high_risk = sorted(
        row["incident_id"]
        for row in observations
        if float(row["error_rate"]) >= threshold
    )
    return {
        "error_rate_threshold": threshold,
        "high_risk_incidents": high_risk,
        "observation_count": len(observations),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--threshold", type=float)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = score(args.input, effective_threshold(args.threshold))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
