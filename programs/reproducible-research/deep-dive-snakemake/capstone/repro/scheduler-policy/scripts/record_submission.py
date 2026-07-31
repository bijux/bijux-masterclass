#!/usr/bin/env python3
"""Render a scheduler request without contacting a scheduler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_RESOURCES = ("mem_mb", "runtime")


def load_mapping(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def rejection(reason: str, *, profile: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "rejected",
        "reason": reason,
        "profile_name": profile.get("name"),
        "job_name": contract.get("job_name"),
    }


def render(profile: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    if profile.get("scheduler") != "slurm":
        return rejection("unsupported scheduler", profile=profile, contract=contract)

    overrides = profile.get("semantic_overrides", {})
    if overrides:
        return rejection(
            "profile changes workflow semantics",
            profile=profile,
            contract=contract,
        )

    resources = dict(contract.get("resources", {}))
    for name in profile.get("drop_resources", []):
        resources.pop(name, None)

    missing = [name for name in REQUIRED_RESOURCES if name not in resources]
    if missing:
        return rejection(
            f"missing required resources: {', '.join(missing)}",
            profile=profile,
            contract=contract,
        )

    declared_memory = int(contract["resources"]["mem_mb"])
    requested_memory = int(resources["mem_mb"] * float(profile.get("memory_scale", 1.0)))
    if requested_memory < declared_memory:
        return rejection(
            "scheduler request under-provisions declared memory",
            profile=profile,
            contract=contract,
        )

    threads = int(contract["threads"])
    runtime = int(resources["runtime"])
    argv = [
        "sbatch",
        f"--job-name={contract['job_name']}",
        f"--cpus-per-task={threads}",
        f"--mem={requested_memory}M",
        f"--time={runtime}",
        "--wrap=snakemake --snakefile Snakefile --cores 1 results/summary.tsv",
    ]
    return {
        "status": "accepted",
        "profile_name": profile["name"],
        "job_name": contract["job_name"],
        "declared": {
            "threads": threads,
            "mem_mb": declared_memory,
            "runtime": runtime,
        },
        "requested": {
            "threads": threads,
            "mem_mb": requested_memory,
            "runtime": runtime,
        },
        "semantic_contract": contract["semantic_contract"],
        "argv": argv,
        "executed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    profile = load_mapping(args.profile)
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    receipt = render(profile, contract)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if receipt["status"] == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
