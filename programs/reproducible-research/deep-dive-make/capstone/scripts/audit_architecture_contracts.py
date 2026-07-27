#!/usr/bin/env python3
"""Audit paired Make architecture contracts with executable evidence."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, NamedTuple

SCHEMA = "deep-dive-make-architecture-contract-audit"


class CommandResult(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def run_command(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str] | None = None,
) -> CommandResult:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
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


def copy_specimen(source: Path, destination: Path) -> Path:
    shutil.copytree(source, destination)
    return destination


def read_text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def architecture_case(
    *,
    family: str,
    model: str,
    finding: str,
    passed: bool,
    observations: dict[str, Any],
    trace: str,
) -> dict[str, Any]:
    return {
        "family": family,
        "model": model,
        "result": "PASS" if passed else "FAIL",
        "finding": finding,
        "observations": observations,
        "trace": trace,
    }


def audit_public_api(
    *,
    specimens: Path,
    workspace: Path,
    traces: Path,
    make: str,
) -> list[dict[str, Any]]:
    source = specimens / "public-api"
    cases: list[dict[str, Any]] = []
    models = (
        (
            "private-caller",
            "private-caller.mk",
            "automation-private.sh",
            False,
            "PRIVATE_TARGET_DEPENDENCE_REPRODUCED",
        ),
        (
            "declared-caller",
            "declared-caller.mk",
            "automation-declared.sh",
            True,
            "PUBLIC_TARGET_CONTRACT_HONORED",
        ),
    )

    for model, makefile, script, expects_verification, finding in models:
        model_workspace = copy_specimen(source, workspace / "public-api" / model)
        help_result = run_command([make, "-f", makefile, "help"], cwd=model_workspace)
        environment = os.environ.copy()
        environment.update({"MAKE_BIN": make, "MAKEFLAGS": "--trace"})
        caller_result = run_command(
            [f"./{script}"],
            cwd=model_workspace,
            environment=environment,
        )
        help_trace = f"public-api-{model}-help.log"
        caller_trace = f"public-api-{model}-caller.log"
        write_trace(traces / help_trace, help_result)
        write_trace(traces / caller_trace, caller_result)

        application_exists = (model_workspace / "build/application.txt").is_file()
        verification_exists = (model_workspace / "build/verification.txt").is_file()
        help_lists_verify = "verify  build and verify" in help_result.stdout
        help_lists_internal = "internal-build" in help_result.stdout
        passed = (
            help_result.returncode == 0
            and caller_result.returncode == 0
            and help_lists_verify
            and not help_lists_internal
            and application_exists
            and verification_exists is expects_verification
        )
        cases.append(
            architecture_case(
                family="public-api",
                model=model,
                finding=finding,
                passed=passed,
                observations={
                    "caller_exit": caller_result.returncode,
                    "help_lists_verify": help_lists_verify,
                    "help_lists_internal_build": help_lists_internal,
                    "application_exists": application_exists,
                    "verification_exists": verification_exists,
                    "expected_verification": expects_verification,
                    "help_trace": help_trace,
                },
                trace=caller_trace,
            )
        )
    return cases


def audit_include_ownership(
    *,
    specimens: Path,
    workspace: Path,
    traces: Path,
    make: str,
) -> list[dict[str, Any]]:
    source = specimens / "include-ownership"
    cases: list[dict[str, Any]] = []
    models = (
        (
            "global-mutation",
            "flags=-O2 -DRELEASE\n",
            "flags=-O2 -DRELEASE\n",
            "CROSS_LAYER_POLICY_LEAK_REPRODUCED",
        ),
        (
            "target-scoped-policy",
            "flags=-O2\n",
            "flags=-O2 -DRELEASE\n",
            "TARGET_SCOPED_POLICY_PRESERVED",
        ),
    )

    for model, expected_default, expected_release, finding in models:
        model_workspace = copy_specimen(source / model, workspace / "include-ownership" / model)
        result = run_command(
            [make, "--trace", "all", "release"],
            cwd=model_workspace,
        )
        trace = f"include-ownership-{model}.log"
        write_trace(traces / trace, result)
        default_flags = read_text(model_workspace / "build/default.txt")
        release_flags = read_text(model_workspace / "build/release.txt")
        passed = (
            result.returncode == 0
            and default_flags == expected_default
            and release_flags == expected_release
        )
        cases.append(
            architecture_case(
                family="include-ownership",
                model=model,
                finding=finding,
                passed=passed,
                observations={
                    "build_exit": result.returncode,
                    "default_flags": default_flags,
                    "release_flags": release_flags,
                    "expected_default_flags": expected_default,
                    "expected_release_flags": expected_release,
                },
                trace=trace,
            )
        )
    return cases


def audit_output_ownership(
    *,
    specimens: Path,
    workspace: Path,
    traces: Path,
    make: str,
) -> list[dict[str, Any]]:
    source = specimens / "output-ownership"
    cases: list[dict[str, Any]] = []
    models = (
        (
            "flat-output",
            ["build/util.txt"],
            {"owner=cli"},
            "FLAT_OUTPUT_OWNERSHIP_COLLAPSED",
        ),
        (
            "namespaced-output",
            ["build/cli/util.txt", "build/lib/util.txt"],
            {"owner=cli", "owner=lib"},
            "SUBSYSTEM_OUTPUT_OWNERSHIP_PRESERVED",
        ),
    )

    for model, expected_outputs, expected_owners, finding in models:
        model_workspace = copy_specimen(source / model, workspace / "output-ownership" / model)
        map_result = run_command([make, "show-map"], cwd=model_workspace)
        build_result = run_command([make, "--trace", "all"], cwd=model_workspace)
        map_trace = f"output-ownership-{model}-map.log"
        build_trace = f"output-ownership-{model}-build.log"
        write_trace(traces / map_trace, map_result)
        write_trace(traces / build_trace, build_result)

        build_root = model_workspace / "build"
        output_paths = sorted(
            path.relative_to(model_workspace).as_posix()
            for path in build_root.rglob("*.txt")
        )
        output_contents = {
            path.relative_to(model_workspace).as_posix(): path.read_text(encoding="utf-8")
            for path in build_root.rglob("*.txt")
        }
        owners = {
            line
            for content in output_contents.values()
            for line in content.splitlines()
            if line.startswith("owner=")
        }
        passed = (
            map_result.returncode == 0
            and build_result.returncode == 0
            and output_paths == expected_outputs
            and owners == expected_owners
            and "sources=src/cli/util.txt src/lib/util.txt" in map_result.stdout
        )
        cases.append(
            architecture_case(
                family="output-ownership",
                model=model,
                finding=finding,
                passed=passed,
                observations={
                    "map_exit": map_result.returncode,
                    "build_exit": build_result.returncode,
                    "output_paths": output_paths,
                    "expected_output_paths": expected_outputs,
                    "owners": sorted(owners),
                    "expected_owners": sorted(expected_owners),
                    "output_contents": output_contents,
                    "map_trace": map_trace,
                },
                trace=build_trace,
            )
        )
    return cases


def write_summary(path: Path, cases: list[dict[str, Any]]) -> None:
    rows = ["family\tmodel\tresult\tfinding"]
    rows.extend(
        f"{case['family']}\t{case['model']}\t{case['result']}\t{case['finding']}"
        for case in cases
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
        *audit_public_api(
            specimens=specimens,
            workspace=workspace,
            traces=traces,
            make=args.make,
        ),
        *audit_include_ownership(
            specimens=specimens,
            workspace=workspace,
            traces=traces,
            make=args.make,
        ),
        *audit_output_ownership(
            specimens=specimens,
            workspace=workspace,
            traces=traces,
            make=args.make,
        ),
    ]
    result = "PASS" if all(case["result"] == "PASS" for case in cases) else "FAIL"
    report = {"schema": SCHEMA, "result": result, "cases": cases}
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(bundle / "summary.tsv", cases)

    if result != "PASS":
        print(f"FAIL: architecture contract mismatch in {output}", file=sys.stderr)
        return 1
    print(f"PASS: verified architecture contracts in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
