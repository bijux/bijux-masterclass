#!/usr/bin/env python3
"""Execute concurrency incidents and verify their promised failure signatures."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "deep-dive-make-incident-signature-audit"


@dataclass(frozen=True)
class IncidentCase:
    name: str
    makefile: str
    boundary: str
    finding: str
    expected_exit: str
    inspect: Callable[[Path, Path], tuple[bool, dict[str, object]]]


def inspect_shared_log(
    workspace: Path, evidence_dir: Path
) -> tuple[bool, dict[str, object]]:
    shared_log = workspace / "shared.log"
    lines = (
        shared_log.read_text(encoding="utf-8").splitlines()
        if shared_log.is_file()
        else []
    )
    expected_records = {
        "alpha:start",
        "alpha:end",
        "beta:start",
        "beta:end",
    }
    starts_before_ends = (
        len(lines) == 4
        and all(line.endswith(":start") for line in lines[:2])
        and all(line.endswith(":end") for line in lines[2:])
    )
    signature_matches = set(lines) == expected_records and starts_before_ends
    evidence_dir.mkdir(parents=True, exist_ok=True)
    captured = evidence_dir / "shared.log"
    captured.write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )
    return signature_matches, {
        "artifact": (Path("evidence") / evidence_dir.name / captured.name).as_posix(),
        "observed_records": lines,
        "signature": "both writers start before either writer completes",
    }


def inspect_directory_race(
    workspace: Path, evidence_dir: Path
) -> tuple[bool, dict[str, object]]:
    candidates = (Path("dir/file1"), Path("dir/file2"))
    surviving = [
        path.as_posix() for path in candidates if (workspace / path).is_file()
    ]
    signature_matches = len(surviving) == 1
    evidence_dir.mkdir(parents=True, exist_ok=True)
    captured = evidence_dir / "surviving-files.txt"
    captured.write_text(
        "\n".join(surviving) + ("\n" if surviving else ""),
        encoding="utf-8",
    )
    return signature_matches, {
        "artifact": (Path("evidence") / evidence_dir.name / captured.name).as_posix(),
        "candidate_outputs": [path.as_posix() for path in candidates],
        "signature": "one directory claimant publishes and the other cannot start",
        "surviving_outputs": surviving,
    }


def inspect_staging_collision(
    workspace: Path, evidence_dir: Path
) -> tuple[bool, dict[str, object]]:
    observed = {
        name: (workspace / name).is_file()
        for name in ("shared.staging", "x.out", "y.out")
    }
    signature_matches = observed == {
        "shared.staging": False,
        "x.out": False,
        "y.out": True,
    }
    published_content = (
        (workspace / "y.out").read_text(encoding="utf-8").strip()
        if observed["y.out"]
        else ""
    )
    evidence_dir.mkdir(parents=True, exist_ok=True)
    captured = evidence_dir / "publication-state.json"
    captured.write_text(
        json.dumps(
            {
                "files": observed,
                "published_content": published_content,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return signature_matches, {
        "artifact": (Path("evidence") / evidence_dir.name / captured.name).as_posix(),
        "observed_files": observed,
        "published_content": published_content,
        "signature": "one claimant consumes the shared staging path before the other",
    }


CASES = (
    IncidentCase(
        name="shared-log-interleaving",
        makefile="shared-log-interleaving.mk",
        boundary="publication-ownership",
        finding="SEMANTIC_CORRUPTION_REPRODUCED",
        expected_exit="zero",
        inspect=inspect_shared_log,
    ),
    IncidentCase(
        name="directory-creation-race",
        makefile="directory-creation-race.mk",
        boundary="graph-ownership",
        finding="DIRECTORY_RACE_REPRODUCED",
        expected_exit="nonzero",
        inspect=inspect_directory_race,
    ),
    IncidentCase(
        name="shared-staging-collision",
        makefile="shared-staging-collision.mk",
        boundary="publication-ownership",
        finding="STAGING_COLLISION_REPRODUCED",
        expected_exit="nonzero",
        inspect=inspect_staging_collision,
    ),
)


def run_case(
    *,
    case: IncidentCase,
    repro_dir: Path,
    workspace_root: Path,
    output_root: Path,
    make_command: str,
) -> dict[str, object]:
    workspace = workspace_root / case.name
    workspace.mkdir(parents=True)
    makefile = workspace / "incident.mk"
    shutil.copyfile(repro_dir / case.makefile, makefile)

    command = [
        make_command,
        "--no-print-directory",
        "-f",
        "incident.mk",
        "-j2",
        "all",
    ]
    completed = subprocess.run(
        command,
        cwd=workspace,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    runs = output_root / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    run_log = runs / f"{case.name}.log"
    run_log.write_text(completed.stdout, encoding="utf-8")

    evidence_dir = output_root / "evidence" / case.name
    signature_matches, observation = case.inspect(workspace, evidence_dir)
    exit_matches = (
        completed.returncode == 0
        if case.expected_exit == "zero"
        else completed.returncode != 0
    )
    result = "PASS" if exit_matches and signature_matches else "FAIL"
    return {
        "boundary": case.boundary,
        "case": case.name,
        "command": " ".join(command),
        "exit_matches": exit_matches,
        "exit_status": completed.returncode,
        "expected_exit": case.expected_exit,
        "finding": case.finding,
        "makefile": case.makefile,
        "observation": observation,
        "result": result,
        "run_log": run_log.relative_to(output_root).as_posix(),
        "signature_matches": signature_matches,
    }


def write_summary(results: list[dict[str, object]], output: Path) -> None:
    lines = [
        (
            "case\texpected_exit\texit_status\tfinding\tboundary"
            "\tsignature_matches\tresult\trun_log"
        )
    ]
    for result in results:
        lines.append(
            "\t".join(
                (
                    str(result["case"]),
                    str(result["expected_exit"]),
                    str(result["exit_status"]),
                    str(result["finding"]),
                    str(result["boundary"]),
                    str(result["signature_matches"]).lower(),
                    str(result["result"]),
                    str(result["run_log"]),
                )
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repro-dir", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--make", required=True)
    parser.add_argument(
        "--case",
        choices=("all", *(case.name for case in CASES)),
        default="all",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.workspace.exists():
        print(
            f"FAIL: workspace already exists: {arguments.workspace}",
            file=sys.stderr,
        )
        return 2

    selected = [
        case for case in CASES if arguments.case in ("all", case.name)
    ]
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        results = [
            run_case(
                case=case,
                repro_dir=arguments.repro_dir,
                workspace_root=arguments.workspace,
                output_root=arguments.output.parent,
                make_command=arguments.make,
            )
            for case in selected
        ]
    except OSError as error:
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
            "FAIL: incident observations did not match promised signatures",
            file=sys.stderr,
        )
        return 1
    print(f"PASS: verified incident signatures in {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
