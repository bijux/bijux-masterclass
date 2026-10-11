#!/usr/bin/env python3
"""Classify performance claims without confusing faster output with preserved meaning."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

VARIANTS = (
    "baseline",
    "honest-tuning",
    "validation-bypass",
    "repeated-scan",
)


@dataclass(frozen=True)
class CommandEvidence:
    argv: list[str]
    returncode: int
    elapsed_seconds: float
    stdout_file: str
    stderr_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snakemake", type=Path, required=True)
    return parser.parse_args()


def run_command(
    argv: list[str],
    *,
    cwd: Path,
    evidence_dir: Path,
    label: str,
) -> CommandEvidence:
    started = time.monotonic()
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    elapsed = time.monotonic() - started
    stdout_path = evidence_dir / f"{label}.stdout.txt"
    stderr_path = evidence_dir / f"{label}.stderr.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    evidence = CommandEvidence(
        argv=argv,
        returncode=completed.returncode,
        elapsed_seconds=round(elapsed, 6),
        stdout_file=stdout_path.name,
        stderr_file=stderr_path.name,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"{label} failed with exit {completed.returncode}; read {stderr_path}")
    return evidence


def load_mapping(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a mapping in {path}")
    return payload


def read_benchmark(path: Path) -> dict[str, float | None]:
    """Retain unavailable sampled telemetry without fabricating measured zeroes."""
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 1:
        raise ValueError(f"expected one benchmark row in {path}, found {len(rows)}")
    row = rows[0]

    def measurement(field: str, *, sampled: bool = False) -> float | None:
        raw = row[field]
        if sampled and raw == "NA":
            return None
        value = float(raw)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"invalid benchmark measurement {field} in {path}: {raw}")
        return value

    return {
        "seconds": measurement("s"),
        "max_rss_mb": measurement("max_rss", sampled=True),
        "io_in_mb": measurement("io_in", sampled=True),
        "io_out_mb": measurement("io_out", sampled=True),
    }


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def collect_variant(
    *,
    name: str,
    specimen: Path,
    workspace: Path,
    snakemake: Path,
) -> dict[str, Any]:
    run_dir = workspace / "runs" / name
    shutil.copytree(specimen, run_dir)
    evidence_dir = workspace / "commands" / name
    evidence_dir.mkdir(parents=True, exist_ok=True)
    config_path = run_dir / "config" / f"{name}.yaml"
    command = [
        str(snakemake),
        "--cores",
        "1",
        "--configfile",
        f"config/{name}.yaml",
    ]
    dry_run = run_command(
        [*command, "--dry-run", "--printshellcmds"],
        cwd=run_dir,
        evidence_dir=evidence_dir,
        label="dry-run",
    )
    execution = run_command(
        command,
        cwd=run_dir,
        evidence_dir=evidence_dir,
        label="execution",
    )

    normalized_text = (run_dir / "results" / "normalized.tsv").read_text(encoding="utf-8")
    metrics = json.loads((run_dir / "evidence" / "metrics.json").read_text(encoding="utf-8"))
    return {
        "config": load_mapping(config_path),
        "artifact": {
            "path": "results/normalized.tsv",
            "sha256": sha256_text(normalized_text),
            "text": normalized_text,
        },
        "metrics": metrics,
        "benchmark": read_benchmark(run_dir / "benchmarks" / "normalize.tsv"),
        "commands": {
            "dry_run": asdict(dry_run),
            "execution": asdict(execution),
        },
    }


def finding(
    name: str,
    decision: str,
    checks: dict[str, bool],
    observations: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "finding": name,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "decision": decision,
        "checks": checks,
    }
    if observations is not None:
        payload["observations"] = observations
    return payload


def baseline_finding(variants: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = variants["baseline"]
    metrics = baseline["metrics"]
    return finding(
        "BASELINE_COST_OBSERVED",
        "REFERENCE",
        {
            "mode_named": metrics["mode"] == "baseline",
            "all_inputs_reach_output": metrics["input_records"] == metrics["output_records"] == 6,
            "all_records_validated": metrics["validation_checks"] == 6,
            "one_scan_pass": metrics["scan_passes"] == 1 and metrics["records_scanned"] == 6,
            "per_record_setup_visible": metrics["setup_cycles"] == 6,
            "cost_units_recorded": metrics["deterministic_cost_units"] == 34,
            "benchmark_recorded": baseline["benchmark"]["seconds"] > 0,
        },
        {
            "benchmark_seconds": baseline["benchmark"]["seconds"],
            "execution_seconds": baseline["commands"]["execution"]["elapsed_seconds"],
        },
    )


def honest_tuning_finding(variants: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = variants["baseline"]
    tuned = variants["honest-tuning"]
    base_metrics = baseline["metrics"]
    tuned_metrics = tuned["metrics"]
    return finding(
        "HONEST_TUNING_ACCEPTED",
        "ACCEPT",
        {
            "mode_named": tuned_metrics["mode"] == "honest-tuning",
            "artifact_bytes_preserved": tuned["artifact"]["sha256"]
            == baseline["artifact"]["sha256"],
            "record_contract_preserved": (
                tuned_metrics["input_records"],
                tuned_metrics["output_records"],
            )
            == (
                base_metrics["input_records"],
                base_metrics["output_records"],
            ),
            "validation_preserved": tuned_metrics["validation_checks"]
            == base_metrics["validation_checks"],
            "scan_contract_preserved": tuned_metrics["scan_passes"] == base_metrics["scan_passes"],
            "setup_work_reduced": tuned_metrics["setup_cycles"] < base_metrics["setup_cycles"],
            "deterministic_cost_reduced": tuned_metrics["deterministic_cost_units"]
            < base_metrics["deterministic_cost_units"],
            "benchmark_recorded": tuned["benchmark"]["seconds"] > 0,
        },
        {
            "baseline_benchmark_seconds": baseline["benchmark"]["seconds"],
            "tuned_benchmark_seconds": tuned["benchmark"]["seconds"],
            "baseline_cost_units": base_metrics["deterministic_cost_units"],
            "tuned_cost_units": tuned_metrics["deterministic_cost_units"],
        },
    )


def validation_bypass_finding(variants: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = variants["baseline"]
    bypass = variants["validation-bypass"]
    metrics = bypass["metrics"]
    return finding(
        "VALIDATION_BYPASS_REJECTED",
        "REJECT",
        {
            "mode_named": metrics["mode"] == "validation-bypass",
            "artifact_bytes_match": bypass["artifact"]["sha256"] == baseline["artifact"]["sha256"],
            "config_disables_validation": bypass["config"]["validate"] is False,
            "validation_evidence_missing": metrics["validation_checks"] == 0,
            "apparent_cost_reduction_visible": metrics["deterministic_cost_units"]
            < baseline["metrics"]["deterministic_cost_units"],
            "benchmark_recorded": bypass["benchmark"]["seconds"] > 0,
        },
        {
            "baseline_benchmark_seconds": baseline["benchmark"]["seconds"],
            "bypass_benchmark_seconds": bypass["benchmark"]["seconds"],
            "reason": "equal output bytes do not preserve the validation guarantee",
        },
    )


def repeated_scan_finding(variants: dict[str, dict[str, Any]]) -> dict[str, Any]:
    tuned = variants["honest-tuning"]
    regression = variants["repeated-scan"]
    tuned_metrics = tuned["metrics"]
    metrics = regression["metrics"]
    return finding(
        "REPEATED_SCAN_REGRESSION_IDENTIFIED",
        "REGRESSION",
        {
            "mode_named": metrics["mode"] == "repeated-scan",
            "artifact_bytes_preserved": regression["artifact"]["sha256"]
            == tuned["artifact"]["sha256"],
            "validation_preserved": metrics["validation_checks"]
            == tuned_metrics["validation_checks"],
            "setup_work_unchanged": metrics["setup_cycles"] == tuned_metrics["setup_cycles"],
            "scan_work_increased": metrics["scan_passes"] > tuned_metrics["scan_passes"]
            and metrics["records_scanned"] > tuned_metrics["records_scanned"],
            "deterministic_cost_increased": metrics["deterministic_cost_units"]
            > tuned_metrics["deterministic_cost_units"],
            "benchmark_recorded": regression["benchmark"]["seconds"] > 0,
        },
        {
            "tuned_benchmark_seconds": tuned["benchmark"]["seconds"],
            "regression_benchmark_seconds": regression["benchmark"]["seconds"],
            "tuned_cost_units": tuned_metrics["deterministic_cost_units"],
            "regression_cost_units": metrics["deterministic_cost_units"],
        },
    )


def write_summary(path: Path, findings: list[dict[str, Any]]) -> None:
    rows = ["finding\tresult\tdecision"]
    rows.extend(f"{item['finding']}\t{item['result']}\t{item['decision']}" for item in findings)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    snakemake = args.snakemake.resolve()

    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    variants = {
        name: collect_variant(
            name=name,
            specimen=specimen,
            workspace=workspace,
            snakemake=snakemake,
        )
        for name in VARIANTS
    }
    findings = [
        baseline_finding(variants),
        honest_tuning_finding(variants),
        validation_bypass_finding(variants),
        repeated_scan_finding(variants),
    ]
    report = {
        "schema": "deep-dive-snakemake-performance-diagnostics-audit",
        "variants": variants,
        "findings": findings,
        "interpretation": {
            "benchmark_role": "observation",
            "acceptance_basis": "artifact contracts and deterministic work counters",
        },
    }
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(output.parent / "summary.tsv", findings)

    failed = [item["finding"] for item in findings if item["result"] != "PASS"]
    if failed:
        raise SystemExit(f"FAIL: performance findings failed: {', '.join(failed)}")
    print(f"PASS: classified performance claims in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
