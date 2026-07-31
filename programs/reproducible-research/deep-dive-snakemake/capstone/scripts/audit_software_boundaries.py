#!/usr/bin/env python3
"""Audit whether Snakemake can observe changes to executed software."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

MODEL_CONTRACTS = {
    "script-directive": {
        "software": Path("workflow/scripts/render.py"),
        "finding": "SCRIPT_DIRECTIVE_DRIFT_PLANS_RERUN",
        "decision": "ACCEPT",
        "expected_rerun": True,
    },
    "hidden-package-source": {
        "software": Path("src/software_specimen/render.py"),
        "finding": "HIDDEN_PACKAGE_DRIFT_MISSES_RERUN",
        "decision": "REJECT",
        "expected_rerun": False,
    },
    "declared-package-source": {
        "software": Path("src/software_specimen/render.py"),
        "finding": "DECLARED_PACKAGE_SOURCE_PLANS_RERUN",
        "decision": "ACCEPT",
        "expected_rerun": True,
    },
}


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


def change_software_marker(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    if "-v1" not in source:
        raise ValueError(f"missing software marker in {path}")
    path.write_text(source.replace("-v1", "-v2"), encoding="utf-8")


def planned_render(result: dict[str, Any]) -> bool:
    output = f"{result['stdout']}\n{result['stderr']}"
    return "rule render:" in output


def evaluate_model(
    *,
    baseline_converged: bool,
    changed_dryrun_succeeded: bool,
    rerun_planned: bool,
    changed_execution_succeeded: bool,
    artifact_marker: str,
    expected_rerun: bool,
) -> tuple[str, list[str]]:
    checks = {
        "baseline converges": baseline_converged,
        "changed dry-run succeeds": changed_dryrun_succeeded,
        "source drift has expected planning behavior": rerun_planned == expected_rerun,
        "changed execution succeeds": changed_execution_succeeded,
        "artifact reflects planning behavior": (
            artifact_marker.endswith("-v2") if expected_rerun else artifact_marker.endswith("-v1")
        ),
    }
    failures = [name for name, passed in checks.items() if not passed]
    return ("PASS" if not failures else "FAIL"), failures


def audit_model(
    model_name: str,
    model: Path,
    traces: Path,
    snakemake: str,
) -> dict[str, Any]:
    contract = MODEL_CONTRACTS[model_name]
    command = [snakemake, "--snakefile", "Snakefile", "--cores", "1"]

    initial_execution = run_command(command, model)
    baseline_dryrun = run_command([*command, "-n", "-p"], model)
    change_software_marker(model / contract["software"])
    changed_dryrun = run_command([*command, "-n", "-p"], model)
    changed_execution = run_command(command, model)

    for label, result in (
        ("initial-run", initial_execution),
        ("baseline-dryrun", baseline_dryrun),
        ("changed-dryrun", changed_dryrun),
        ("changed-run", changed_execution),
    ):
        write_trace(traces / f"{model_name}-{label}.txt", result)

    artifact = model / "build" / "rendered.txt"
    artifact_lines = artifact.read_text(encoding="utf-8").splitlines() if artifact.exists() else []
    observations = {
        "initial_execution_returncode": initial_execution["returncode"],
        "baseline_dryrun_returncode": baseline_dryrun["returncode"],
        "baseline_converged": not planned_render(baseline_dryrun),
        "changed_dryrun_returncode": changed_dryrun["returncode"],
        "rerun_planned_after_source_change": planned_render(changed_dryrun),
        "changed_execution_returncode": changed_execution["returncode"],
        "artifact_lines": artifact_lines,
        "software_path_declared_as_input": (
            'implementation="src/software_specimen/render.py"'
            in (model / "Snakefile").read_text(encoding="utf-8")
        ),
        "uses_script_directive": (
            'script:\n        "workflow/scripts/render.py"'
            in (model / "Snakefile").read_text(encoding="utf-8")
        ),
    }
    artifact_marker = artifact_lines[0] if artifact_lines else ""
    result, failures = evaluate_model(
        baseline_converged=(
            observations["baseline_dryrun_returncode"] == 0 and observations["baseline_converged"]
        ),
        changed_dryrun_succeeded=observations["changed_dryrun_returncode"] == 0,
        rerun_planned=observations["rerun_planned_after_source_change"],
        changed_execution_succeeded=observations["changed_execution_returncode"] == 0,
        artifact_marker=artifact_marker,
        expected_rerun=bool(contract["expected_rerun"]),
    )
    return {
        "model": model_name,
        "result": result,
        "finding": contract["finding"],
        "decision": contract["decision"],
        "failures": failures,
        "observations": observations,
    }


def write_summary(path: Path, cases: list[dict[str, Any]]) -> None:
    rows = ["model\tresult\tdecision\tfinding"]
    rows.extend(
        f"{case['model']}\t{case['result']}\t{case['decision']}\t{case['finding']}"
        for case in cases
    )
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

    cases = []
    for model_name in MODEL_CONTRACTS:
        model = workspace / model_name
        shutil.copytree(specimens / model_name, model)
        cases.append(audit_model(model_name, model, traces, args.snakemake))

    report = {
        "schema": "deep-dive-snakemake-software-boundary-audit",
        "specimens": specimens.as_posix(),
        "workspace": workspace.as_posix(),
        "cases": cases,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(output.parent / "summary.tsv", cases)

    failures = [case["model"] for case in cases if case["result"] != "PASS"]
    if failures:
        print(f"FAIL: software boundary audit rejected: {', '.join(failures)}")
        return 1
    print(f"PASS: verified software boundaries in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
