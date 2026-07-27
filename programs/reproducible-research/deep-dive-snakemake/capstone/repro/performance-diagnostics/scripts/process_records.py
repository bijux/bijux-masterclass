#!/usr/bin/env python3
"""Normalize records while exposing deterministic work and validation counters."""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path

SETUP_SECONDS = 0.05
SCAN_SECONDS = 0.04


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--chunk-size", type=int, required=True)
    parser.add_argument("--scan-passes", type=int, required=True)
    parser.add_argument("--validate", required=True)
    return parser.parse_args()


def read_records(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_records(records: list[dict[str, str]]) -> int:
    for row in records:
        if not row["record_id"].islower() or not row["value"].isdigit():
            raise ValueError(f"invalid record: {row}")
    return len(records)


def normalized_rows(records: list[dict[str, str]]) -> list[tuple[str, int]]:
    return [(row["record_id"], int(row["value"])) for row in records]


def write_output(path: Path, rows: list[tuple[str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("record_id", "value"))
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    if args.chunk_size < 1 or args.scan_passes < 1:
        raise ValueError("chunk size and scan passes must be positive")

    records = read_records(args.input)
    validation_enabled = args.validate.lower() == "true"
    validation_checks = validate_records(records) if validation_enabled else 0
    setup_cycles = math.ceil(len(records) / args.chunk_size)

    for _ in range(setup_cycles):
        time.sleep(SETUP_SECONDS)
    for _ in range(args.scan_passes):
        sum(int(row["value"]) for row in records)
        time.sleep(SCAN_SECONDS)

    rows = normalized_rows(records)
    write_output(args.output, rows)

    metrics = {
        "schema": "performance-diagnostics-metrics",
        "mode": args.mode,
        "input_records": len(records),
        "output_records": len(rows),
        "validation_checks": validation_checks,
        "scan_passes": args.scan_passes,
        "records_scanned": len(records) * args.scan_passes,
        "setup_cycles": setup_cycles,
        "deterministic_cost_units": setup_cycles * 5 + args.scan_passes * 4,
    }
    args.metrics.parent.mkdir(parents=True, exist_ok=True)
    args.metrics.write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
