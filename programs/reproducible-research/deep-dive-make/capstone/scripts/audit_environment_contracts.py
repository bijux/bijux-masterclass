#!/usr/bin/env python3
"""Verify non-file state, recursive boundaries, and required-tool contracts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

SCHEMA = "deep-dive-make-environment-contract-audit"
MISSING_TOOL = "bijux-missing-tool"


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


def read_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if not separator or not key:
            raise RuntimeError(f"{path}: expected KEY=value lines")
        values[key] = value
    return values


def audit_non_file_state(
    *,
    specimens: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    models = (
        (
            "stale-manifest",
            "release",
            False,
            "STALE_NON_FILE_STATE_REPRODUCED",
        ),
        (
            "reevaluated-manifest",
            "debug",
            True,
            "NON_FILE_STATE_REFRESHED",
        ),
    )
    for model, expected_mode, expected_rebuild, finding in models:
        workspace = workspace_root / "non-file-state" / model
        shutil.copytree(specimens / "non-file-state", workspace)
        make_base = [
            make_command,
            "--no-print-directory",
            "-f",
            f"{model}.mk",
        ]
        initial = run_command([*make_base, "MODE=release", "all"], workspace)
        require_success(initial, f"non-file-state/{model}/release")
        manifest = workspace / "build" / "environment.manifest"
        artifact = workspace / "build" / "artifact.txt"
        initial_manifest_sha256 = sha256(manifest)
        initial_artifact_sha256 = sha256(artifact)

        changed = run_command(
            [*make_base, "MODE=debug", "--trace", "all"],
            workspace,
        )
        require_success(changed, f"non-file-state/{model}/debug")
        changed_manifest = read_key_values(manifest)
        changed_artifact = read_key_values(artifact)
        changed_manifest_sha256 = sha256(manifest)
        changed_artifact_sha256 = sha256(artifact)
        artifact_rebuilt = "update target 'build/artifact.txt'" in changed.stdout

        equal = run_command(
            [*make_base, "MODE=debug", "--trace", "all"],
            workspace,
        )
        require_success(equal, f"non-file-state/{model}/debug-repeat")
        equal_artifact_sha256 = sha256(artifact)
        artifact_rebuilt_for_equal_mode = (
            "update target 'build/artifact.txt'" in equal.stdout
        )

        actual_mode = changed_manifest.get("MODE", "")
        artifact_manifest = changed_artifact.get("manifest", "")
        expected_manifest_change = model == "reevaluated-manifest"
        manifest_changed = initial_manifest_sha256 != changed_manifest_sha256
        artifact_changed = initial_artifact_sha256 != changed_artifact_sha256
        result = (
            "PASS"
            if (
                actual_mode == expected_mode
                and artifact_manifest == f"MODE={expected_mode}"
                and artifact_rebuilt == expected_rebuild
                and manifest_changed == expected_manifest_change
                and artifact_changed == expected_rebuild
                and not artifact_rebuilt_for_equal_mode
                and equal_artifact_sha256 == changed_artifact_sha256
            )
            else "FAIL"
        )
        results.append(
            {
                "finding": finding,
                "model": model,
                "observation": {
                    "actual_mode": actual_mode,
                    "artifact_manifest": artifact_manifest,
                    "artifact_rebuilt_after_mode_change": artifact_rebuilt,
                    "artifact_rebuilt_for_equal_mode": (
                        artifact_rebuilt_for_equal_mode
                    ),
                    "changed_artifact_sha256": changed_artifact_sha256,
                    "changed_manifest_sha256": changed_manifest_sha256,
                    "expected_mode": expected_mode,
                    "initial_artifact_sha256": initial_artifact_sha256,
                    "initial_manifest_sha256": initial_manifest_sha256,
                    "requested_mode": "debug",
                },
                "result": result,
                "specimen": "non-file-state",
                "traces": [
                    write_trace(
                        traces=traces,
                        name=f"non-file-state-{model}-mode-change",
                        completed=changed,
                    ),
                    write_trace(
                        traces=traces,
                        name=f"non-file-state-{model}-equal-mode",
                        completed=equal,
                    ),
                ],
            }
        )
    return results


def audit_recursive_boundary(
    *,
    specimens: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    models = (
        (
            "literal-recursion",
            False,
            "LITERAL_RECURSION_HIDES_CHILD_PLAN",
        ),
        (
            "declared-recursion",
            True,
            "DECLARED_RECURSION_EXPOSES_CHILD_PLAN",
        ),
    )
    for model, expected_plan_visible, finding in models:
        workspace = workspace_root / "recursive-boundary" / model
        shutil.copytree(specimens / "recursive-boundary", workspace)
        make_base = [
            make_command,
            "--no-print-directory",
            "-f",
            f"{model}.mk",
            f"MAKE_BIN={make_command}",
        ]
        dry_run = run_command([*make_base, "-n", "all"], workspace)
        require_success(dry_run, f"recursive-boundary/{model}/dry-run")
        child_output = workspace / "child" / "child.out"
        dry_run_published_output = child_output.exists()
        child_plan_visible = "child-plan: publish child.out" in dry_run.stdout

        actual = run_command([*make_base, "-j2", "all"], workspace)
        require_success(actual, f"recursive-boundary/{model}/actual")
        child_state = read_key_values(child_output)
        makelevel = child_state.get("MAKELEVEL", "")
        makeflags = child_state.get("MAKEFLAGS", "")
        budget_visible = "-j2" in makeflags or "jobserver" in makeflags
        result = (
            "PASS"
            if (
                child_plan_visible == expected_plan_visible
                and not dry_run_published_output
                and makelevel == "1"
                and (model == "literal-recursion" or budget_visible)
            )
            else "FAIL"
        )
        results.append(
            {
                "finding": finding,
                "model": model,
                "observation": {
                    "budget_visible_in_actual_run": budget_visible,
                    "child_plan_visible_in_dry_run": child_plan_visible,
                    "dry_run_published_output": dry_run_published_output,
                    "expected_child_plan_visible": expected_plan_visible,
                    "makeflags": makeflags,
                    "makelevel": makelevel,
                },
                "result": result,
                "specimen": "recursive-boundary",
                "traces": [
                    write_trace(
                        traces=traces,
                        name=f"recursive-boundary-{model}-dry-run",
                        completed=dry_run,
                    ),
                    write_trace(
                        traces=traces,
                        name=f"recursive-boundary-{model}-actual",
                        completed=actual,
                    ),
                ],
            }
        )
    return results


def tool_residue(workspace: Path) -> dict[str, object]:
    version = workspace / "build" / "tool-version.txt"
    result = workspace / "build" / "result.txt"
    return {
        "result_exists": result.is_file(),
        "tool_version_bytes": version.stat().st_size if version.is_file() else None,
        "tool_version_exists": version.is_file(),
    }


def audit_required_tool(
    *,
    specimens: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
    python: str,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    cases = (
        (
            "late-tool-check",
            "late-tool-check.mk",
            MISSING_TOOL,
            False,
            "LATE_TOOL_FAILURE_LEFT_RESIDUE",
        ),
        (
            "contract-gate-missing",
            "contract-gate.mk",
            MISSING_TOOL,
            False,
            "REQUIRED_TOOL_REJECTED_EARLY",
        ),
        (
            "contract-gate-available",
            "contract-gate.mk",
            python,
            True,
            "REQUIRED_TOOL_ACCEPTED",
        ),
    )
    for model, makefile, required_tool, expected_success, finding in cases:
        workspace = workspace_root / "required-tool" / model
        shutil.copytree(specimens / "required-tool", workspace)
        completed = run_command(
            [
                make_command,
                "--no-print-directory",
                "-f",
                makefile,
                f"REQUIRED_TOOL={required_tool}",
                "all",
            ],
            workspace,
        )
        succeeded = completed.returncode == 0
        residue = tool_residue(workspace)
        deliberate_message = (
            f"contract: missing required tool {MISSING_TOOL}"
            in completed.stdout
        )
        if model == "late-tool-check":
            signature_matches = (
                not succeeded
                and residue["tool_version_exists"] is True
                and residue["tool_version_bytes"] == 0
                and residue["result_exists"] is False
                and not deliberate_message
            )
        elif model == "contract-gate-missing":
            signature_matches = (
                not succeeded
                and residue["tool_version_exists"] is False
                and residue["result_exists"] is False
                and deliberate_message
            )
        else:
            version = workspace / "build" / "tool-version.txt"
            result_file = workspace / "build" / "result.txt"
            signature_matches = (
                succeeded
                and residue["tool_version_exists"] is True
                and residue["result_exists"] is True
                and "Python " in version.read_text(encoding="utf-8")
                and result_file.read_text(encoding="utf-8")
                == "result=complete\n"
            )
        results.append(
            {
                "finding": finding,
                "model": model,
                "observation": {
                    "contract_message_visible": deliberate_message,
                    "exit_status": completed.returncode,
                    "expected_success": expected_success,
                    **residue,
                },
                "result": "PASS" if signature_matches else "FAIL",
                "specimen": "required-tool",
                "traces": [
                    write_trace(
                        traces=traces,
                        name=f"required-tool-{model}",
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
    if specimen == "non-file-state":
        return (
            f"mode={observation['actual_mode']},"
            f"rebuilt={str(observation['artifact_rebuilt_after_mode_change']).lower()}"
        )
    if specimen == "recursive-boundary":
        return (
            "child_plan_visible="
            f"{str(observation['child_plan_visible_in_dry_run']).lower()},"
            f"makelevel={observation['makelevel']}"
        )
    return (
        f"exit={observation['exit_status']},"
        f"version_file={str(observation['tool_version_exists']).lower()},"
        f"result={str(observation['result_exists']).lower()}"
    )


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
            *audit_non_file_state(
                specimens=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
            ),
            *audit_recursive_boundary(
                specimens=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
            ),
            *audit_required_tool(
                specimens=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
                python=arguments.python,
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
            "FAIL: environment observations did not match contracts",
            file=sys.stderr,
        )
        return 1
    print(f"PASS: verified environment contracts in {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
