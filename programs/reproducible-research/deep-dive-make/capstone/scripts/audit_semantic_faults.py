#!/usr/bin/env python3
"""Execute paired Make models for state, edge, and rule-selection semantics."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCHEMA = "deep-dive-make-semantic-fault-audit"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def write_trace(
    *,
    traces: Path,
    name: str,
    completed: subprocess.CompletedProcess[str],
) -> str:
    trace = traces / f"{name}.log"
    trace.write_text(completed.stdout, encoding="utf-8")
    return trace.relative_to(traces.parent).as_posix()


def require_success(
    completed: subprocess.CompletedProcess[str], label: str
) -> None:
    if completed.returncode != 0:
        raise RuntimeError(f"{label}: command failed:\n{completed.stdout}")


def audit_clock_state(
    *,
    specimens: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
    python: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    models = (
        ("clock-derived", False, "CLOCK_STATE_DRIFT_REPRODUCED"),
        ("declared-state", True, "DECLARED_STATE_STABLE"),
    )
    for model, expected_equal, finding in models:
        runs: list[dict[str, str]] = []
        for run_name in ("first", "second"):
            workspace = workspace_root / "clock-state" / model / run_name
            shutil.copytree(specimens / "clock-state", workspace)
            completed = run_command(
                [
                    make_command,
                    "--no-print-directory",
                    "-f",
                    f"{model}.mk",
                    f"PYTHON={python}",
                    "all",
                ],
                workspace,
            )
            require_success(completed, f"clock-state/{model}/{run_name}")
            artifact = workspace / "artifact.txt"
            runs.append(
                {
                    "artifact": artifact.read_text(encoding="utf-8"),
                    "sha256": sha256(artifact),
                    "trace": write_trace(
                        traces=traces,
                        name=f"clock-state-{model}-{run_name}",
                        completed=completed,
                    ),
                }
            )
            time.sleep(0.001)

        hashes_equal = runs[0]["sha256"] == runs[1]["sha256"]
        result = "PASS" if hashes_equal == expected_equal else "FAIL"
        results.append(
            {
                "finding": finding,
                "model": model,
                "observation": {
                    "expected_hashes_equal": expected_equal,
                    "first_artifact": runs[0]["artifact"].splitlines(),
                    "first_sha256": runs[0]["sha256"],
                    "hashes_equal": hashes_equal,
                    "second_artifact": runs[1]["artifact"].splitlines(),
                    "second_sha256": runs[1]["sha256"],
                },
                "result": result,
                "specimen": "clock-state",
                "traces": [runs[0]["trace"], runs[1]["trace"]],
            }
        )
    return results


def mutate_order_input(workspace: Path, newest_output: int) -> None:
    semantic_input = workspace / "input.txt"
    source = semantic_input.read_text(encoding="utf-8")
    if source != "before\n":
        raise RuntimeError("order-only-edge: input must contain the initial value")
    semantic_input.write_text("after\n", encoding="utf-8")
    current = semantic_input.stat()
    advanced = max(time.time_ns(), newest_output + 1)
    os.utime(semantic_input, ns=(current.st_atime_ns, advanced))


def audit_order_only_edge(
    *,
    specimens: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    models = (
        ("order-only", "before", "ORDER_ONLY_STALENESS_REPRODUCED"),
        ("semantic-edge", "after", "SEMANTIC_EDGE_REFRESHED"),
    )
    for model, expected_output, finding in models:
        workspace = workspace_root / "order-only-edge" / model
        shutil.copytree(specimens / "order-only-edge", workspace)
        make_base = [
            make_command,
            "--no-print-directory",
            "-f",
            f"{model}.mk",
        ]
        initial = run_command([*make_base, "all"], workspace)
        require_success(initial, f"order-only-edge/{model}/initial")
        output = workspace / "output.txt"
        initial_output = output.read_text(encoding="utf-8").strip()
        mutate_order_input(workspace, output.stat().st_mtime_ns)
        observed = run_command([*make_base, "--trace", "all"], workspace)
        require_success(observed, f"order-only-edge/{model}/mutated")
        actual_output = output.read_text(encoding="utf-8").strip()
        result = (
            "PASS"
            if initial_output == "before" and actual_output == expected_output
            else "FAIL"
        )
        results.append(
            {
                "finding": finding,
                "model": model,
                "observation": {
                    "actual_output": actual_output,
                    "expected_output": expected_output,
                    "initial_output": initial_output,
                    "semantic_input": "after",
                },
                "result": result,
                "specimen": "order-only-edge",
                "traces": [
                    write_trace(
                        traces=traces,
                        name=f"order-only-edge-{model}",
                        completed=observed,
                    )
                ],
            }
        )
    return results


def read_pattern_outputs(workspace: Path, model: str) -> dict[str, str]:
    paths: tuple[Path, ...]
    if model == "namespaced-targets":
        paths = (
            Path("build/root/a.choice"),
            Path("build/generated/a.choice"),
        )
    else:
        paths = (Path("build/a.choice"),)
    return {
        path.as_posix(): (workspace / path).read_text(encoding="utf-8").strip()
        for path in paths
    }


def audit_pattern_selection(
    *,
    specimens: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    models = (
        (
            "generated-rule-first",
            {"build/a.choice": "selected=generated"},
            "FIRST_OVERLAPPING_RULE_SELECTED",
        ),
        (
            "root-rule-first",
            {"build/a.choice": "selected=root"},
            "REORDERED_RULE_CHANGED_SELECTION",
        ),
        (
            "namespaced-targets",
            {
                "build/generated/a.choice": "selected=generated",
                "build/root/a.choice": "selected=root",
            },
            "NAMESPACED_SELECTION_EXPLICIT",
        ),
    )
    for model, expected_outputs, finding in models:
        workspace = workspace_root / "pattern-selection" / model
        shutil.copytree(specimens / "pattern-selection", workspace)
        completed = run_command(
            [
                make_command,
                "--no-print-directory",
                "-f",
                f"{model}.mk",
                "--trace",
                "all",
            ],
            workspace,
        )
        require_success(completed, f"pattern-selection/{model}")
        actual_outputs = read_pattern_outputs(workspace, model)
        results.append(
            {
                "finding": finding,
                "model": model,
                "observation": {
                    "actual_outputs": actual_outputs,
                    "expected_outputs": expected_outputs,
                },
                "result": (
                    "PASS" if actual_outputs == expected_outputs else "FAIL"
                ),
                "specimen": "pattern-selection",
                "traces": [
                    write_trace(
                        traces=traces,
                        name=f"pattern-selection-{model}",
                        completed=completed,
                    )
                ],
            }
        )
    return results


def observation_summary(result: dict[str, object]) -> str:
    observation = result["observation"]
    assert isinstance(observation, dict)
    specimen = result["specimen"]
    if specimen == "clock-state":
        return f"hashes_equal={str(observation['hashes_equal']).lower()}"
    if specimen == "order-only-edge":
        return f"output={observation['actual_output']}"
    outputs = observation["actual_outputs"]
    assert isinstance(outputs, dict)
    return ",".join(f"{path}:{outputs[path]}" for path in sorted(outputs))


def write_summary(results: list[dict[str, object]], output: Path) -> None:
    lines = ["specimen\tmodel\tfinding\tobservation\tresult\ttraces"]
    for result in results:
        traces = result["traces"]
        assert isinstance(traces, list)
        lines.append(
            "\t".join(
                (
                    str(result["specimen"]),
                    str(result["model"]),
                    str(result["finding"]),
                    observation_summary(result),
                    str(result["result"]),
                    ",".join(str(trace) for trace in traces),
                )
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimens", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--make", required=True)
    parser.add_argument("--python", required=True)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.workspace.exists():
        print(
            f"FAIL: workspace already exists: {arguments.workspace}",
            file=sys.stderr,
        )
        return 2
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    traces = arguments.output.parent / "traces"
    traces.mkdir(parents=True, exist_ok=True)

    try:
        results = [
            *audit_clock_state(
                specimens=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
                python=arguments.python,
            ),
            *audit_order_only_edge(
                specimens=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
            ),
            *audit_pattern_selection(
                specimens=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
            ),
        ]
    except (OSError, RuntimeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    report = {
        "cases": results,
        "result": (
            "PASS"
            if all(result["result"] == "PASS" for result in results)
            else "FAIL"
        ),
        "schema": SCHEMA,
    }
    arguments.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_summary(results, arguments.output.with_name("summary.tsv"))
    if report["result"] != "PASS":
        print(
            "FAIL: semantic observations did not match model contracts",
            file=sys.stderr,
        )
        return 1
    print(f"PASS: verified semantic fault models in {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
