#!/usr/bin/env python3
"""Execute missing-edge specimens beside their declared-edge repairs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "deep-dive-make-incremental-fault-audit"


@dataclass(frozen=True)
class Specimen:
    name: str
    semantic_input: Path
    old_text: str
    new_text: str
    governed_outputs: tuple[Path, ...]


SPECIMENS = (
    Specimen(
        name="authored-header",
        semantic_input=Path("config.h"),
        old_text='"before"',
        new_text='"after"',
        governed_outputs=(Path("app"),),
    ),
    Specimen(
        name="generated-producer",
        semantic_input=Path("scripts/render_header.py"),
        old_text='"before"',
        new_text='"after"',
        governed_outputs=(Path("generated.h"), Path("app")),
    ),
)

MODELS = ("missing-edge", "declared-edge")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def mutate_input(workspace: Path, specimen: Specimen, newest_output: int) -> None:
    path = workspace / specimen.semantic_input
    source = path.read_text(encoding="utf-8")
    if source.count(specimen.old_text) != 1:
        raise RuntimeError(
            f"{specimen.name}: semantic input must contain one mutation marker"
        )
    path.write_text(
        source.replace(specimen.old_text, specimen.new_text),
        encoding="utf-8",
    )
    current = path.stat()
    advanced = max(time.time_ns(), newest_output + 1)
    os.utime(path, ns=(current.st_atime_ns, advanced))


def run_model(
    *,
    specimen: Specimen,
    model: str,
    specimen_root: Path,
    workspace_root: Path,
    traces: Path,
    make_command: str,
    compiler: str,
    python: str,
) -> dict[str, object]:
    workspace = workspace_root / specimen.name / model
    shutil.copytree(specimen_root / specimen.name, workspace)
    makefile = f"{model}.mk"
    make_base = [
        make_command,
        "--no-print-directory",
        "-f",
        makefile,
        f"CC={compiler}",
        f"PYTHON={python}",
    ]

    initial = run_command([*make_base, "all"], workspace)
    if initial.returncode != 0:
        raise RuntimeError(
            f"{specimen.name}/{model}: initial build failed: "
            f"{initial.stdout}{initial.stderr}"
        )

    before_output = run_command([str(workspace / "app")], workspace)
    if before_output.returncode != 0 or before_output.stdout.strip() != "before":
        raise RuntimeError(
            f"{specimen.name}/{model}: initial binary did not print 'before'"
        )

    before_hashes = {
        path.as_posix(): sha256(workspace / path)
        for path in specimen.governed_outputs
    }
    newest_output = max(
        (workspace / path).stat().st_mtime_ns
        for path in specimen.governed_outputs
    )
    mutate_input(workspace, specimen, newest_output)

    observed = run_command([*make_base, "--trace", "all"], workspace)
    trace_path = traces / f"{specimen.name}-{model}.log"
    trace_path.write_text(
        observed.stdout + observed.stderr,
        encoding="utf-8",
    )

    after_output = run_command([str(workspace / "app")], workspace)
    after_hashes = {
        path.as_posix(): sha256(workspace / path)
        for path in specimen.governed_outputs
    }
    changed_outputs = sorted(
        path for path in before_hashes if before_hashes[path] != after_hashes[path]
    )

    expects_stale = model == "missing-edge"
    expected_output = "before" if expects_stale else "after"
    expected_changed = (
        []
        if expects_stale
        else sorted(path.as_posix() for path in specimen.governed_outputs)
    )
    actual_output = after_output.stdout.strip()
    result = (
        "PASS"
        if observed.returncode == 0
        and after_output.returncode == 0
        and actual_output == expected_output
        and changed_outputs == expected_changed
        else "FAIL"
    )

    return {
        "actual_output": actual_output,
        "changed_outputs": changed_outputs,
        "expected_changed_outputs": expected_changed,
        "expected_output": expected_output,
        "finding": "FAULT_REPRODUCED" if expects_stale else "REPAIR_VERIFIED",
        "initial_output": before_output.stdout.strip(),
        "model": model,
        "observation": "STALE" if actual_output == "before" else "REFRESHED",
        "result": result,
        "semantic_input": specimen.semantic_input.as_posix(),
        "specimen": specimen.name,
        "trace": trace_path.relative_to(traces.parent).as_posix(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimens", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--make", required=True)
    parser.add_argument("--compiler", required=True)
    parser.add_argument("--python", required=True)
    return parser.parse_args()


def write_summary(cases: list[dict[str, object]], output: Path) -> None:
    header = (
        "specimen\tmodel\tfinding\tsemantic_input\tinitial_output\tactual_output"
        "\tchanged_outputs\tresult\ttrace"
    )
    lines = [header]
    for case in cases:
        changed = case["changed_outputs"]
        assert isinstance(changed, list)
        lines.append(
            "\t".join(
                (
                    str(case["specimen"]),
                    str(case["model"]),
                    str(case["finding"]),
                    str(case["semantic_input"]),
                    str(case["initial_output"]),
                    str(case["actual_output"]),
                    ",".join(str(path) for path in changed) or "-",
                    str(case["result"]),
                    str(case["trace"]),
                )
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
        cases = [
            run_model(
                specimen=specimen,
                model=model,
                specimen_root=arguments.specimens,
                workspace_root=arguments.workspace,
                traces=traces,
                make_command=arguments.make,
                compiler=arguments.compiler,
                python=arguments.python,
            )
            for specimen in SPECIMENS
            for model in MODELS
        ]
    except (OSError, RuntimeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    report = {
        "cases": cases,
        "result": "PASS"
        if all(case["result"] == "PASS" for case in cases)
        else "FAIL",
        "schema": SCHEMA,
    }
    arguments.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_summary(cases, arguments.output.with_name("summary.tsv"))
    if report["result"] != "PASS":
        print("FAIL: incremental fault audit did not match expectations", file=sys.stderr)
        return 1
    print(f"PASS: wrote incremental fault evidence to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
