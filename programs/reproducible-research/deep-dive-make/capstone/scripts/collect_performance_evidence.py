#!/usr/bin/env python3
"""Collect repeatable timing evidence for governed Make scenarios."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

from performance_policy import PerformanceScenario, read_performance_policy


SCHEMA = "deep-dive-make-performance-evidence-v1"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--make", dest="make_command", required=True)
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
        raise RuntimeError(f"{purpose} failed with status {result.returncode}: {detail}")


def scenario_command(make_command: str, scenario: PerformanceScenario) -> list[str]:
    command = [make_command, "--no-print-directory", f"-j{scenario.jobs}"]
    if scenario.route == "dry-run-all":
        command.append("-n")
    command.append("all")
    return command


def establish_state(make_command: str, scenario: PerformanceScenario, cwd: Path) -> None:
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

    (logs_directory / f"{scenario.name}.txt").write_text(
        "\n".join(transcript), encoding="utf-8"
    )
    return {
        "jobs": scenario.jobs,
        "route": scenario.route,
        "samples": samples,
        "state": scenario.state,
    }


def main() -> int:
    arguments = parse_arguments()
    if arguments.samples < 3:
        raise SystemExit("--samples must be at least 3")

    capstone = Path(__file__).resolve().parents[1]
    policy = arguments.policy.resolve()
    output = arguments.output.resolve()
    logs_directory = output.parent / "logs"
    output.parent.mkdir(parents=True, exist_ok=True)
    logs_directory.mkdir(parents=True, exist_ok=True)
    scenarios = read_performance_policy(policy)

    make_version = subprocess.run(
        [arguments.make_command, "--version"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()[0]
    evidence: dict[str, object] = {
        "context": {
            "make": make_version,
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
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
    print(f"PASS: wrote performance evidence to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
