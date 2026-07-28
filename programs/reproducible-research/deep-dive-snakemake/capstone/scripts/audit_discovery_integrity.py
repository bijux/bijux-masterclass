#!/usr/bin/env python3
"""Audit whether changing sample membership creates an observable invalidation event."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

MODELS = ("governed-registry", "ambient-scan")


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def write_trace(path: Path, result: dict[str, Any]) -> None:
    path.write_text(
        f"$ {' '.join(result['command'])}\n"
        f"returncode={result['returncode']}\n"
        "--- stdout ---\n"
        f"{result['stdout']}"
        "--- stderr ---\n"
        f"{result['stderr']}",
        encoding="utf-8",
    )


def materialized_samples(model: Path) -> list[str]:
    return sorted(path.stem for path in (model / "build").glob("*.txt"))


def add_arrivals(model: Path, governed: bool) -> None:
    raw_dir = model / "data" / "raw"
    for sample in ("beta", "gamma"):
        (raw_dir / f"{sample}.fastq").write_text(f"@{sample}\nACGT\n+\nIIII\n", encoding="utf-8")
    if governed:
        registry = model / "data" / "arrivals.tsv"
        registry.write_text("alpha\nbeta\n", encoding="utf-8")


def evaluate(model_name: str, observations: dict[str, Any]) -> tuple[str, list[str]]:
    shared = {
        "baseline execution succeeds": observations["baseline_returncode"] == 0,
        "baseline contains only alpha": observations["baseline_samples"] == ["alpha"],
        "change dry-run succeeds": observations["dryrun_returncode"] == 0,
        "change execution succeeds": observations["change_returncode"] == 0,
        "forced reevaluation succeeds": observations["forced_returncode"] == 0,
    }
    if model_name == "governed-registry":
        checks = {
            **shared,
            "checkpoint declares registry input": observations["declares_registry_input"],
            "registry change schedules discovery": observations["dryrun_schedules_discovery"],
            "registered beta enters the DAG": observations["change_samples"] == ["alpha", "beta"],
            "unregistered gamma stays outside scope": observations["forced_samples"]
            == ["alpha", "beta"],
        }
    else:
        checks = {
            **shared,
            "checkpoint has no declared input": not observations["declares_checkpoint_input"],
            "ambient arrivals leave the plan stale": observations["dryrun_nothing_to_do"],
            "normal execution stays stale": observations["change_samples"] == ["alpha"],
            "forced reevaluation reveals hidden arrivals": observations["forced_samples"]
            == ["alpha", "beta", "gamma"],
        }
    failures = [label for label, passed in checks.items() if not passed]
    return ("PASS" if not failures else "FAIL"), failures


def audit_model(model_name: str, model: Path, traces: Path, snakemake: str) -> dict[str, Any]:
    source = (model / "Snakefile").read_text(encoding="utf-8")
    base_command = [snakemake, "--snakefile", "Snakefile", "--cores", "1"]

    baseline = run(base_command, model)
    baseline_samples = materialized_samples(model)
    add_arrivals(model, governed=model_name == "governed-registry")

    dryrun = run([*base_command, "-n", "-p"], model)
    changed = run(base_command, model)
    change_samples = materialized_samples(model)
    forced = run([*base_command, "--forcerun", "discover"], model)
    forced_samples = materialized_samples(model)

    for label, result in (
        ("baseline", baseline),
        ("change-dryrun", dryrun),
        ("change-run", changed),
        ("forced-run", forced),
    ):
        write_trace(traces / f"{model_name}-{label}.txt", result)

    checkpoint_block = source.split("checkpoint discover:", 1)[1].split(
        "def discovered_outputs", 1
    )[0]
    observations = {
        "declares_registry_input": 'registry="data/arrivals.tsv"' in checkpoint_block,
        "declares_checkpoint_input": "input:" in checkpoint_block,
        "baseline_returncode": baseline["returncode"],
        "baseline_samples": baseline_samples,
        "dryrun_returncode": dryrun["returncode"],
        "dryrun_schedules_discovery": "checkpoint discover:" in dryrun["stdout"],
        "dryrun_nothing_to_do": "Nothing to be done" in dryrun["stdout"],
        "change_returncode": changed["returncode"],
        "change_samples": change_samples,
        "forced_returncode": forced["returncode"],
        "forced_samples": forced_samples,
    }
    result, failures = evaluate(model_name, observations)
    finding = (
        "DECLARED_DISCOVERY_INVALIDATION_PRESERVED"
        if model_name == "governed-registry"
        else "AMBIENT_DISCOVERY_STALENESS_REPRODUCED"
    )
    return {
        "model": model_name,
        "result": result,
        "finding": finding,
        "failures": failures,
        "observations": observations,
        "trace_files": {
            "baseline": f"traces/{model_name}-baseline.txt",
            "change_dryrun": f"traces/{model_name}-change-dryrun.txt",
            "change_run": f"traces/{model_name}-change-run.txt",
            "forced_run": f"traces/{model_name}-forced-run.txt",
        },
    }


def write_summary(path: Path, cases: list[dict[str, Any]]) -> None:
    lines = ["model\tresult\tfinding\tplanned_after_arrival\tnormal_samples\tforced_samples"]
    for case in cases:
        observations = case["observations"]
        planned = (
            observations["dryrun_schedules_discovery"]
            if case["model"] == "governed-registry"
            else not observations["dryrun_nothing_to_do"]
        )
        lines.append(
            "\t".join(
                (
                    case["model"],
                    case["result"],
                    case["finding"],
                    str(planned).lower(),
                    ",".join(observations["change_samples"]),
                    ",".join(observations["forced_samples"]),
                )
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimens", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snakemake", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    specimens = args.specimens.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    traces = output.parent / "traces"

    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    traces.mkdir(parents=True, exist_ok=True)

    cases = []
    for model_name in MODELS:
        model = workspace / model_name
        shutil.copytree(specimens / model_name, model)
        cases.append(audit_model(model_name, model, traces, args.snakemake))

    report = {
        "schema": "deep-dive-snakemake-discovery-integrity-audit",
        "specimens": specimens.as_posix(),
        "workspace": workspace.as_posix(),
        "cases": cases,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(output.parent / "summary.tsv", cases)

    failures = [case["model"] for case in cases if case["result"] != "PASS"]
    if failures:
        print(f"FAIL: discovery integrity audit rejected: {', '.join(failures)}")
        return 1
    print(f"PASS: verified discovery invalidation in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
