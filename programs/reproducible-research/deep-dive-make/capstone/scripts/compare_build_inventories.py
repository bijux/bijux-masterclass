#!/usr/bin/env python3
"""Compare two build artifact inventories and explain schedule drift."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "deep-dive-make/build-artifact-inventory"


def load_inventory(path: Path) -> dict[str, Any]:
    try:
        inventory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read inventory {path}: {error}") from error
    if inventory.get("schema") != SCHEMA:
        raise ValueError(f"{path}: expected schema {SCHEMA!r}")
    artifacts = inventory.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError(f"{path}: artifacts must be a list")
    return inventory


def artifact_map(inventory: dict[str, Any], source: Path) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for artifact in inventory["artifacts"]:
        if not isinstance(artifact, dict):
            raise ValueError(f"{source}: artifact entries must be objects")
        path = artifact.get("path")
        digest = artifact.get("sha256")
        size = artifact.get("bytes")
        if not isinstance(path, str) or not isinstance(digest, str) or not isinstance(size, int):
            raise ValueError(f"{source}: artifact entries require path, bytes, and sha256")
        if path in mapped:
            raise ValueError(f"{source}: duplicate artifact path: {path}")
        mapped[path] = artifact
    return mapped


def compare(
    baseline_inventory: dict[str, Any],
    candidate_inventory: dict[str, Any],
    baseline_path: Path,
    candidate_path: Path,
) -> dict[str, Any]:
    baseline = artifact_map(baseline_inventory, baseline_path)
    candidate = artifact_map(candidate_inventory, candidate_path)
    missing = sorted(set(baseline) - set(candidate))
    unexpected = sorted(set(candidate) - set(baseline))
    changed = []
    for path in sorted(set(baseline) & set(candidate)):
        before = baseline[path]
        after = candidate[path]
        if before["sha256"] != after["sha256"] or before["bytes"] != after["bytes"]:
            changed.append(
                {
                    "path": path,
                    "baseline": {"bytes": before["bytes"], "sha256": before["sha256"]},
                    "candidate": {"bytes": after["bytes"], "sha256": after["sha256"]},
                }
            )

    result = "PASS" if not missing and not unexpected and not changed else "FAIL"
    return {
        "schema": "deep-dive-make/build-schedule-comparison",
        "result": result,
        "baseline_aggregate_sha256": baseline_inventory.get("aggregate_sha256"),
        "candidate_aggregate_sha256": candidate_inventory.get("aggregate_sha256"),
        "missing_paths": missing,
        "unexpected_paths": unexpected,
        "changed_artifacts": changed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    baseline_path = Path(args.baseline)
    candidate_path = Path(args.candidate)
    output = Path(args.output)
    try:
        report = compare(
            load_inventory(baseline_path),
            load_inventory(candidate_path),
            baseline_path,
            candidate_path,
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report["result"] != "PASS":
        raise SystemExit("build artifact inventories differ; inspect the comparison report")


if __name__ == "__main__":
    main()
