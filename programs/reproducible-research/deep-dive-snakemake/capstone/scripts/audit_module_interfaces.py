#!/usr/bin/env python3
"""Audit explicit and hidden Snakemake module interface contracts."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

MODELS = ("explicit-contract", "hidden-coupling")


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def write_trace(path: Path, result: dict[str, Any]) -> None:
    command = " ".join(str(part) for part in result["command"])
    path.write_text(
        f"$ {command}\n"
        f"returncode={result['returncode']}\n"
        "--- stdout ---\n"
        f"{result['stdout']}"
        "--- stderr ---\n"
        f"{result['stderr']}",
        encoding="utf-8",
    )


def inspect_source(model: Path) -> dict[str, Any]:
    caller = (model / "Snakefile").read_text(encoding="utf-8")
    module = (model / "module" / "Snakefile").read_text(encoding="utf-8")
    return {
        "narrow_module_config": 'config: config["normalize"]' in caller,
        "broad_module_config": any(
            line.strip() == "config: config" for line in caller.splitlines()
        ),
        "caller_binds_input": 'source="data/sample.txt"' in caller,
        "caller_binds_output": 'artifact="build/sample.txt"' in caller,
        "caller_binds_policy": 'prefix=config["normalize"]["prefix"]' in caller,
        "module_reads_private_policy": 'config["private"]["prefix"]' in module,
        "atomic_publication": (
            "'{output.artifact}.candidate'" in module
            and "mv '{output.artifact}.candidate' '{output.artifact}'" in module
        ),
    }


def evaluate_contract(model_name: str, observations: dict[str, Any]) -> tuple[str, list[str]]:
    shared = {
        "rule listing succeeds": observations["list_rules_returncode"] == 0,
        "dry-run succeeds": observations["dryrun_returncode"] == 0,
        "execution succeeds": observations["run_returncode"] == 0,
        "caller binds input": observations["caller_binds_input"],
        "caller binds output": observations["caller_binds_output"],
        "expected rules remain visible": observations["listed_rules"]
        == [
            "all",
            "normalize_sample",
        ],
        "publication is atomic": observations["atomic_publication"],
        "no candidate residue remains": observations["candidate_residue"] == [],
    }

    if model_name == "explicit-contract":
        checks = {
            **shared,
            "module receives narrow config": observations["narrow_module_config"],
            "module does not receive broad config": not observations["broad_module_config"],
            "caller binds policy": observations["caller_binds_policy"],
            "module avoids private policy reads": not observations["module_reads_private_policy"],
            "artifact records caller policy": observations["artifact_lines"]
            == ["reviewed", "sample payload"],
        }
    else:
        checks = {
            **shared,
            "module receives broad config": observations["broad_module_config"],
            "module does not receive narrow config": not observations["narrow_module_config"],
            "caller leaves policy hidden": not observations["caller_binds_policy"],
            "module reads private policy": observations["module_reads_private_policy"],
            "artifact records hidden policy": observations["artifact_lines"]
            == ["inherited", "sample payload"],
        }

    failures = [name for name, passed in checks.items() if not passed]
    return ("PASS" if not failures else "FAIL"), failures


def audit_model(model_name: str, model: Path, traces: Path, snakemake: str) -> dict[str, Any]:
    source_observations = inspect_source(model)
    list_rules = run_command(
        [snakemake, "--snakefile", "Snakefile", "--cores", "1", "--list-rules"],
        model,
    )
    dryrun = run_command(
        [snakemake, "--snakefile", "Snakefile", "--cores", "1", "-n", "-p"],
        model,
    )
    execution = run_command(
        [snakemake, "--snakefile", "Snakefile", "--cores", "1"],
        model,
    )

    write_trace(traces / f"{model_name}-list-rules.txt", list_rules)
    write_trace(traces / f"{model_name}-dryrun.txt", dryrun)
    write_trace(traces / f"{model_name}-run.txt", execution)

    artifact = model / "build" / "sample.txt"
    observations = {
        **source_observations,
        "list_rules_returncode": list_rules["returncode"],
        "dryrun_returncode": dryrun["returncode"],
        "run_returncode": execution["returncode"],
        "listed_rules": sorted(
            line.strip() for line in list_rules["stdout"].splitlines() if line.strip()
        ),
        "artifact_lines": (
            artifact.read_text(encoding="utf-8").splitlines() if artifact.exists() else []
        ),
        "candidate_residue": sorted(
            path.relative_to(model).as_posix() for path in model.rglob("*.candidate")
        ),
    }
    result, failures = evaluate_contract(model_name, observations)
    finding = (
        "EXPLICIT_MODULE_CONTRACT_PRESERVED"
        if model_name == "explicit-contract"
        else "HIDDEN_MODULE_COUPLING_REPRODUCED"
    )
    return {
        "model": model_name,
        "result": result,
        "finding": finding,
        "failures": failures,
        "observations": observations,
        "trace_files": {
            "list_rules": f"traces/{model_name}-list-rules.txt",
            "dryrun": f"traces/{model_name}-dryrun.txt",
            "run": f"traces/{model_name}-run.txt",
        },
    }


def write_summary(path: Path, cases: list[dict[str, Any]]) -> None:
    rows = ["model\tresult\tfinding"]
    rows.extend(f"{case['model']}\t{case['result']}\t{case['finding']}" for case in cases)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


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

    cases: list[dict[str, Any]] = []
    for model_name in MODELS:
        source = specimens / model_name
        target = workspace / model_name
        shutil.copytree(source, target)
        cases.append(audit_model(model_name, target, traces, args.snakemake))

    report = {
        "schema": "deep-dive-snakemake-module-interface-audit",
        "specimens": specimens.as_posix(),
        "workspace": workspace.as_posix(),
        "cases": cases,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(output.parent / "summary.tsv", cases)

    failures = [case["model"] for case in cases if case["result"] != "PASS"]
    if failures:
        print(f"FAIL: module interface audit rejected: {', '.join(failures)}")
        return 1
    print(f"PASS: verified module interfaces in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
