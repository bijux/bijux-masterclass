#!/usr/bin/env python3
"""Audit whether Make rule abstraction preserves an inspectable contract."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, NamedTuple

SCHEMA = "deep-dive-make-abstraction-contract-audit"
EXPECTED_PREREQUISITES = {
    "build/alpha.txt": ["data/alpha.txt", "build/"],
    "build/beta.txt": ["data/beta.txt", "build/"],
}


class CommandResult(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def run_command(command: list[str], *, cwd: Path) -> CommandResult:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def write_trace(path: Path, result: CommandResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"exit={result.returncode}\n--- stdout ---\n{result.stdout}"
        f"--- stderr ---\n{result.stderr}",
        encoding="utf-8",
    )


def rule_prerequisites(database: str, target: str) -> list[str] | None:
    match = re.search(rf"^{re.escape(target)}:\s*(.*)$", database, re.MULTILINE)
    if match is None:
        return None
    prerequisites = match.group(1).split()
    return [item for item in prerequisites if item != "|"]


def target_exists(database: str, target: str) -> bool:
    return re.search(rf"^{re.escape(target)}:", database, re.MULTILINE) is not None


def read_artifacts(workspace: Path) -> dict[str, str]:
    return {
        path.relative_to(workspace).as_posix(): path.read_text(encoding="utf-8")
        for path in sorted((workspace / "build").glob("*.txt"))
    }


def audit_case(
    *,
    model: str,
    specimens: Path,
    workspace: Path,
    traces: Path,
    make: str,
) -> dict[str, Any]:
    model_workspace = workspace / model
    shutil.copytree(specimens / model, model_workspace)

    help_result = run_command([make, "help"], cwd=model_workspace)
    contract_result = run_command([make, "show-contract"], cwd=model_workspace)
    database_result = run_command([make, "-npRr", "all"], cwd=model_workspace)
    build_result = run_command([make, "--trace", "all"], cwd=model_workspace)

    for label, result in (
        ("help", help_result),
        ("contract", contract_result),
        ("database", database_result),
        ("build", build_result),
    ):
        write_trace(traces / f"{model}-{label}.log", result)

    prerequisites = {
        target: rule_prerequisites(database_result.stdout, target)
        for target in EXPECTED_PREREQUISITES
    }
    hidden_targets = [
        target
        for target in ("publish-alpha", "publish-beta")
        if target_exists(database_result.stdout, target)
    ]
    artifacts = read_artifacts(model_workspace)
    modes = sorted(
        {
            line
            for content in artifacts.values()
            for line in content.splitlines()
            if line.startswith("mode=")
        }
    )
    expected_mode = "release" if model == "opaque-macro" else "ordinary"
    expected_hidden = (
        ["publish-alpha", "publish-beta"] if model == "opaque-macro" else []
    )
    expected_macro_calls = model == "bounded-macro"
    macro_calls_visible = (
        "macro-calls=publish_owned_file:alpha publish_owned_file:beta"
        in contract_result.stdout
    )
    help_hides_generated_targets = all(
        target not in help_result.stdout for target in ("publish-alpha", "publish-beta")
    )
    artifact_sources = sorted(
        line
        for content in artifacts.values()
        for line in content.splitlines()
        if line.startswith("source=")
    )

    passed = (
        all(
            result.returncode == 0
            for result in (
                help_result,
                contract_result,
                database_result,
                build_result,
            )
        )
        and prerequisites == EXPECTED_PREREQUISITES
        and hidden_targets == expected_hidden
        and modes == [f"mode={expected_mode}"]
        and macro_calls_visible is expected_macro_calls
        and help_hides_generated_targets
        and sorted(artifacts)
        == ["build/alpha.txt", "build/beta.txt"]
        and artifact_sources
        == ["source=data/alpha.txt", "source=data/beta.txt"]
    )
    findings = {
        "explicit-rules": "EXPLICIT_RULE_CONTRACT_CAPTURED",
        "bounded-macro": "BOUNDED_MACRO_CONTRACT_PRESERVED",
        "opaque-macro": "OPAQUE_MACRO_SIDE_EFFECTS_REPRODUCED",
    }
    return {
        "model": model,
        "result": "PASS" if passed else "FAIL",
        "finding": findings[model],
        "observations": {
            "prerequisites": prerequisites,
            "expected_prerequisites": EXPECTED_PREREQUISITES,
            "hidden_targets": hidden_targets,
            "expected_hidden_targets": expected_hidden,
            "artifact_modes": modes,
            "expected_mode": expected_mode,
            "artifact_sources": artifact_sources,
            "artifact_contents": artifacts,
            "macro_calls_visible": macro_calls_visible,
            "expected_macro_calls_visible": expected_macro_calls,
            "help_hides_generated_targets": help_hides_generated_targets,
        },
        "traces": {
            label: f"{model}-{label}.log"
            for label in ("help", "contract", "database", "build")
        },
    }


def write_summary(path: Path, cases: list[dict[str, Any]]) -> None:
    rows = ["model\tresult\tfinding"]
    rows.extend(
        f"{case['model']}\t{case['result']}\t{case['finding']}" for case in cases
    )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimens", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--make", default="gmake")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    specimens = args.specimens.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    bundle = output.parent
    traces = bundle / "traces"

    if workspace.exists():
        print(f"FAIL: workspace already exists: {workspace}", file=sys.stderr)
        return 2
    if not specimens.is_dir():
        print(f"FAIL: specimens directory does not exist: {specimens}", file=sys.stderr)
        return 2

    bundle.mkdir(parents=True, exist_ok=True)
    traces.mkdir(parents=True, exist_ok=True)
    cases = [
        audit_case(
            model=model,
            specimens=specimens,
            workspace=workspace,
            traces=traces,
            make=args.make,
        )
        for model in ("explicit-rules", "bounded-macro", "opaque-macro")
    ]
    result = "PASS" if all(case["result"] == "PASS" for case in cases) else "FAIL"
    report = {"schema": SCHEMA, "result": result, "cases": cases}
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(bundle / "summary.tsv", cases)

    if result != "PASS":
        print(f"FAIL: abstraction contract mismatch in {output}", file=sys.stderr)
        return 1
    print(f"PASS: verified abstraction contracts in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
