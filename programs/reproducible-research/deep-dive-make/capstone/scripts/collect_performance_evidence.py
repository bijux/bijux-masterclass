"""Collect repeatable timing evidence for governed Make scenarios."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

from capture_incremental_work import SCHEMA as INCREMENTAL_SCHEMA
from execution_context import capture_execution_context
from performance_policy import PerformanceScenario, read_performance_policy

SCHEMA = "deep-dive-make-performance-evidence-v2"
TRUSTED_OUTPUTS = (
    Path("all"),
    Path("app"),
    Path("build/bin/dyn1"),
    Path("build/bin/dyn2"),
    Path("build/include/dynamic.h"),
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--make", dest="make_command", required=True)
    parser.add_argument("--compiler", default="cc")
    parser.add_argument("--incremental-evidence", type=Path, required=True)
    parser.add_argument("--runner-label", default="local")
    parser.add_argument("--workspace", type=Path)
    return parser.parse_args()


def run_command(
    command: list[str], *, cwd: Path
) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.perf_counter()
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return result, time.perf_counter() - started


def checked_command(command: list[str], *, cwd: Path, purpose: str) -> None:
    result, _ = run_command(command, cwd=cwd)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            f"{purpose} failed with status {result.returncode}: {detail}"
        )


def scenario_command(make_command: str, scenario: PerformanceScenario) -> list[str]:
    command = [make_command, "--no-print-directory", f"-j{scenario.jobs}"]
    if scenario.route == "dry-run-all":
        command.append("-n")
    command.append("all")
    return command


def establish_state(
    make_command: str, scenario: PerformanceScenario, cwd: Path
) -> None:
    if scenario.state == "clean":
        checked_command(
            [make_command, "--no-print-directory", "clean"],
            cwd=cwd,
            purpose=f"{scenario.name} clean setup",
        )
        return

    checked_command(
        [make_command, "--no-print-directory", "all"],
        cwd=cwd,
        purpose=f"{scenario.name} converged setup",
    )
    checked_command(
        [make_command, "--no-print-directory", "-q", "all"],
        cwd=cwd,
        purpose=f"{scenario.name} convergence precondition",
    )


def trusted_output_inventory(cwd: Path) -> list[dict[str, object]]:
    inventory: list[dict[str, object]] = []
    for relative_path in TRUSTED_OUTPUTS:
        path = cwd / relative_path
        if not path.is_file():
            raise RuntimeError(f"trusted output is missing: {relative_path.as_posix()}")
        inventory.append(
            {
                "path": relative_path.as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "size": path.stat().st_size,
            }
        )
    return inventory


def summarize(samples: list[dict[str, object]]) -> dict[str, float]:
    elapsed: list[float] = []
    for sample in samples:
        value = sample["elapsed_seconds"]
        if not isinstance(value, (int, float)):
            raise TypeError("elapsed_seconds must be numeric")
        elapsed.append(float(value))
    minimum = min(elapsed)
    maximum = max(elapsed)
    return {
        "maximum_seconds": round(maximum, 9),
        "median_seconds": round(statistics.median(elapsed), 9),
        "minimum_seconds": round(minimum, 9),
        "spread_seconds": round(maximum - minimum, 9),
    }


def read_incremental_evidence(path: Path) -> dict[str, object]:
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read incremental evidence: {error}") from error
    if report.get("schema") != INCREMENTAL_SCHEMA:
        raise ValueError("unsupported incremental evidence schema")
    if report.get("result") != "PASS":
        raise ValueError("incremental evidence did not pass")
    try:
        raw_cases = report["cases"]
        if not isinstance(raw_cases, list) or not raw_cases:
            raise ValueError("incremental evidence cases must be a non-empty list")
        semantic_cases = []
        for raw_case in raw_cases:
            if not isinstance(raw_case, dict):
                raise TypeError("incremental evidence case must be an object")
            semantic_cases.append(
                {
                    key: raw_case[key]
                    for key in (
                        "expected_rebuild",
                        "input",
                        "missing_rebuild",
                        "observed_rebuild",
                        "result",
                        "unexpected_rebuild",
                    )
                }
            )
        return {
            "cases": semantic_cases,
            "policy_sha256": report["policy_sha256"],
            "result": report["result"],
            "schema": report["schema"],
        }
    except KeyError as error:
        raise ValueError(f"incremental evidence is missing {error.args[0]}") from error


def collect_scenario(
    make_command: str,
    scenario: PerformanceScenario,
    sample_count: int,
    cwd: Path,
    logs_directory: Path,
) -> dict[str, object]:
    command = scenario_command(make_command, scenario)
    samples: list[dict[str, object]] = []
    transcript: list[str] = []

    for sample_number in range(1, sample_count + 1):
        establish_state(make_command, scenario, cwd)
        result, elapsed_seconds = run_command(command, cwd=cwd)
        transcript.extend(
            [
                f"sample={sample_number}",
                f"command={' '.join(command)}",
                f"exit_status={result.returncode}",
                f"elapsed_seconds={elapsed_seconds:.9f}",
                "[stdout]",
                result.stdout.rstrip(),
                "[stderr]",
                result.stderr.rstrip(),
                "",
            ]
        )
        samples.append(
            {
                "elapsed_seconds": round(elapsed_seconds, 9),
                "exit_status": result.returncode,
            }
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"{scenario.name} sample {sample_number} failed "
                f"with status {result.returncode}"
            )

    checked_command(
        [make_command, "--no-print-directory", "-q", "all"],
        cwd=cwd,
        purpose=f"{scenario.name} convergence proof",
    )
    (logs_directory / f"{scenario.name}.txt").write_text(
        "\n".join(transcript), encoding="utf-8"
    )
    return {
        "convergence": "PASS",
        "inventory": trusted_output_inventory(cwd),
        "jobs": scenario.jobs,
        "route": scenario.route,
        "samples": samples,
        "state": scenario.state,
        "summary": summarize(samples),
    }


def write_summary(evidence: dict[str, object], output: Path) -> None:
    scenarios = evidence["scenarios"]
    assert isinstance(scenarios, dict)
    lines = [
        (
            "scenario\tstate\tjobs\tsamples\tminimum_seconds\tmedian_seconds"
            "\tmaximum_seconds\tspread_seconds\tconvergence"
        )
    ]
    for name, raw_scenario in scenarios.items():
        assert isinstance(raw_scenario, dict)
        summary = raw_scenario["summary"]
        samples = raw_scenario["samples"]
        assert isinstance(summary, dict)
        assert isinstance(samples, list)
        lines.append(
            "\t".join(
                [
                    name,
                    str(raw_scenario["state"]),
                    str(raw_scenario["jobs"]),
                    str(len(samples)),
                    str(summary["minimum_seconds"]),
                    str(summary["median_seconds"]),
                    str(summary["maximum_seconds"]),
                    str(summary["spread_seconds"]),
                    str(raw_scenario["convergence"]),
                ]
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    arguments = parse_arguments()
    if arguments.samples < 3:
        raise SystemExit("--samples must be at least 3")

    capstone = (
        arguments.workspace.resolve()
        if arguments.workspace
        else Path(__file__).resolve().parents[1]
    )
    policy = arguments.policy.resolve()
    output = arguments.output.resolve()
    try:
        incremental_work = read_incremental_evidence(
            arguments.incremental_evidence.resolve()
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error
    logs_directory = output.parent / "logs"
    scenarios = read_performance_policy(policy)
    try:
        context = capture_execution_context(
            workspace=capstone,
            make_command=arguments.make_command,
            compiler_command=arguments.compiler,
            runner_label=arguments.runner_label,
        )
    except ValueError as error:
        raise SystemExit(f"cannot capture execution context: {error}") from error
    output.parent.mkdir(parents=True, exist_ok=True)
    logs_directory.mkdir(parents=True, exist_ok=True)

    evidence: dict[str, object] = {
        "context": context,
        "incremental_work": incremental_work,
        "policy_sha256": hashlib.sha256(policy.read_bytes()).hexdigest(),
        "result": "PASS",
        "sample_count": arguments.samples,
        "scenarios": {},
        "schema": SCHEMA,
    }

    try:
        collected = evidence["scenarios"]
        assert isinstance(collected, dict)
        for scenario in scenarios:
            collected[scenario.name] = collect_scenario(
                arguments.make_command,
                scenario,
                arguments.samples,
                capstone,
                logs_directory,
            )
    except RuntimeError as error:
        evidence["result"] = "FAIL"
        evidence["failure"] = str(error)
        output.write_text(
            json.dumps(evidence, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    output.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_summary(evidence, output.parent / "summary.tsv")
    print(f"PASS: wrote performance evidence to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
