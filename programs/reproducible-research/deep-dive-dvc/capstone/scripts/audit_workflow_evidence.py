#!/usr/bin/env python3
"""Contrast local repeatability with a team reproducibility claim."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class WorkflowCase:
    name: str
    finding: str
    expected_decision: str
    configure: Callable[[dict[str, object]], None] | None = None
    mutate_after_run: Callable[[Path], None] | None = None


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def configure_local_only(record: dict[str, object]) -> None:
    record["perform_clean_rebuild"] = False


def configure_hidden_threshold(record: dict[str, object]) -> None:
    record["control_source"] = "environment:RISK_THRESHOLD"
    record["use_hidden_threshold"] = True


def configure_manual_preprocessing(record: dict[str, object]) -> None:
    record["use_prepared_input"] = True
    record["influential_files"] = [
        "prepared-observations.csv",
        "params.json",
        "score_incidents.py",
    ]


def configure_missing_runtime(record: dict[str, object]) -> None:
    record["record_runtime"] = False


def configure_unrecoverable_input(record: dict[str, object]) -> None:
    record["input_recoverable"] = False


def mutate_input(case_dir: Path) -> None:
    path = case_dir / "source" / "observations.csv"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("INC-168,0.44,410\n")


def mutate_implementation(case_dir: Path) -> None:
    path = case_dir / "source" / "score_incidents.py"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n# Changed after the recorded result was created.\n")


CASES = (
    WorkflowCase(
        "complete-evidence",
        "COMPLETE_EVIDENCE",
        "ACCEPT_REPRODUCIBILITY_CLAIM",
    ),
    WorkflowCase(
        "same-workspace-rerun",
        "SAME_WORKSPACE_RERUN",
        "REJECT_REPRODUCIBILITY_CLAIM",
        configure_local_only,
    ),
    WorkflowCase(
        "hidden-threshold",
        "HIDDEN_THRESHOLD",
        "REJECT_REPRODUCIBILITY_CLAIM",
        configure_hidden_threshold,
    ),
    WorkflowCase(
        "changed-input-same-path",
        "CHANGED_INPUT_SAME_PATH",
        "REJECT_REPRODUCIBILITY_CLAIM",
        mutate_after_run=mutate_input,
    ),
    WorkflowCase(
        "manual-preprocessing",
        "MANUAL_PREPROCESSING",
        "REJECT_REPRODUCIBILITY_CLAIM",
        configure_manual_preprocessing,
    ),
    WorkflowCase(
        "missing-runtime",
        "MISSING_RUNTIME",
        "REJECT_REPRODUCIBILITY_CLAIM",
        configure_missing_runtime,
    ),
    WorkflowCase(
        "unrecoverable-input",
        "UNRECOVERABLE_INPUT",
        "REJECT_REPRODUCIBILITY_CLAIM",
        configure_unrecoverable_input,
    ),
    WorkflowCase(
        "stale-implementation",
        "STALE_IMPLEMENTATION",
        "REJECT_REPRODUCIBILITY_CLAIM",
        mutate_after_run=mutate_implementation,
    ),
)


def default_record() -> dict[str, object]:
    return {
        "control_source": "params.json",
        "influential_files": [
            "observations.csv",
            "params.json",
            "score_incidents.py",
        ],
        "input_recoverable": True,
        "perform_clean_rebuild": True,
        "record_runtime": True,
        "use_hidden_threshold": False,
        "use_prepared_input": False,
    }


def prepare_case(
    case: WorkflowCase,
    *,
    specimen: Path,
    workspace: Path,
) -> tuple[Path, dict[str, object]]:
    case_dir = workspace / case.name
    source = case_dir / "source"
    shutil.copytree(specimen, source)
    record = default_record()
    if case.configure is not None:
        case.configure(record)

    if record["use_prepared_input"]:
        raw_lines = (source / "observations.csv").read_text(
            encoding="utf-8"
        ).splitlines()
        prepared_lines = [
            line
            for line in raw_lines
            if line.startswith("incident_id") or "INC-142" not in line
        ]
        (source / "prepared-observations.csv").write_text(
            "\n".join(prepared_lines) + "\n",
            encoding="utf-8",
        )

    return case_dir, record


def execute_score(
    *,
    python: Path,
    script: Path,
    input_path: Path,
    output: Path,
    threshold: float,
    hidden_threshold: bool,
) -> dict[str, object]:
    command = [
        str(python),
        str(script),
        "--input",
        str(input_path),
    ]
    environment = os.environ.copy()
    if hidden_threshold:
        environment["RISK_THRESHOLD"] = str(threshold)
    else:
        command.extend(["--threshold", str(threshold)])
    command.extend(["--output", str(output)])
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    return {
        "argv": [
            python.name,
            script.name,
            "--input",
            input_path.name,
            *(
                []
                if hidden_threshold
                else ["--threshold", str(threshold)]
            ),
            "--output",
            output.name,
        ],
        "returncode": completed.returncode,
        "stderr": completed.stderr,
        "stdout": completed.stdout,
    }


def copy_recorded_sources(
    case_dir: Path,
    effective_input: Path,
) -> Path:
    recorded = case_dir / "recorded"
    recorded.mkdir()
    shutil.copy2(
        effective_input,
        recorded / effective_input.name,
    )
    shutil.copy2(
        case_dir / "source" / "score_incidents.py",
        recorded / "score_incidents.py",
    )
    shutil.copy2(
        case_dir / "source" / "params.json",
        recorded / "params.json",
    )
    return recorded


def build_case_evidence(
    case: WorkflowCase,
    *,
    case_dir: Path,
    record: dict[str, object],
    python: Path,
) -> dict[str, object]:
    source = case_dir / "source"
    threshold = float(
        read_json(source / "params.json")["error_rate_threshold"]
    )
    input_name = (
        "prepared-observations.csv"
        if record["use_prepared_input"]
        else "observations.csv"
    )
    effective_input = source / input_name
    script = source / "score_incidents.py"
    evidence = case_dir / "evidence"
    evidence.mkdir()

    local_a = evidence / "local-run-a.json"
    local_b = evidence / "local-run-b.json"
    receipt_a = execute_score(
        python=python,
        script=script,
        input_path=effective_input,
        output=local_a,
        threshold=threshold,
        hidden_threshold=bool(record["use_hidden_threshold"]),
    )
    receipt_b = execute_score(
        python=python,
        script=script,
        input_path=effective_input,
        output=local_b,
        threshold=threshold,
        hidden_threshold=bool(record["use_hidden_threshold"]),
    )
    if receipt_a["returncode"] != 0 or receipt_b["returncode"] != 0:
        raise RuntimeError(f"local score failed for {case.name}")

    recorded = copy_recorded_sources(case_dir, effective_input)
    workflow_record: dict[str, object] = {
        "command_receipts": [receipt_a, receipt_b],
        "control_source": record["control_source"],
        "effective_input": input_name,
        "effective_input_sha256": sha256(effective_input),
        "implementation_sha256": sha256(script),
        "influential_files": record["influential_files"],
        "input_recoverable": record["input_recoverable"],
        "output_sha256": sha256(local_a),
        "runtime": (
            {
                "implementation": sys.implementation.name,
                "python_executable": python.name,
                "python_version": sys.version.split()[0],
            }
            if record["record_runtime"]
            else {}
        ),
        "threshold": threshold,
    }
    write_json(evidence / "workflow-record.json", workflow_record)

    clean_rebuild = evidence / "clean-rebuild.json"
    if record["perform_clean_rebuild"]:
        receipt = execute_score(
            python=python,
            script=recorded / "score_incidents.py",
            input_path=recorded / input_name,
            output=clean_rebuild,
            threshold=threshold,
            hidden_threshold=bool(record["use_hidden_threshold"]),
        )
        if receipt["returncode"] != 0:
            raise RuntimeError(f"clean rebuild failed for {case.name}")
        write_json(evidence / "clean-rebuild-receipt.json", receipt)

    if case.mutate_after_run is not None:
        case.mutate_after_run(case_dir)

    return workflow_record


def assess_case(
    case: WorkflowCase,
    *,
    case_dir: Path,
    record: dict[str, object],
    contract: dict[str, object],
    workflow_record: dict[str, object],
    output_parent: Path,
) -> dict[str, object]:
    source = case_dir / "source"
    evidence = case_dir / "evidence"
    input_name = str(workflow_record["effective_input"])
    effective_input = source / input_name
    script = source / "score_incidents.py"
    local_a = evidence / "local-run-a.json"
    local_b = evidence / "local-run-b.json"
    clean_rebuild = evidence / "clean-rebuild.json"

    declared_inputs = set(contract["declared_inputs"])
    influential_files = set(workflow_record["influential_files"])
    runtime = workflow_record["runtime"]
    assert isinstance(runtime, dict)

    checks = {
        "input_identity_matches": (
            sha256(effective_input)
            == workflow_record["effective_input_sha256"]
        ),
        "implementation_identity_matches": (
            sha256(script) == workflow_record["implementation_sha256"]
        ),
        "controls_are_declared": (
            workflow_record["control_source"] == "params.json"
            and workflow_record["threshold"]
            == contract["declared_controls"]["error_rate_threshold"]["value"]
        ),
        "all_influential_inputs_are_declared": (
            influential_files.issubset(declared_inputs)
        ),
        "runtime_is_recorded": {
            "implementation",
            "python_executable",
            "python_version",
        }.issubset(runtime),
        "clean_rebuild_matches": (
            clean_rebuild.is_file()
            and read_json(clean_rebuild) == read_json(local_a)
        ),
        "input_is_recoverable": bool(
            workflow_record["input_recoverable"]
        ),
    }
    local_repeatability = read_json(local_a) == read_json(local_b)
    failed_checks = [
        name for name, passed in checks.items() if not passed
    ]
    decision = (
        "ACCEPT_REPRODUCIBILITY_CLAIM"
        if all(checks.values())
        else "REJECT_REPRODUCIBILITY_CLAIM"
    )
    relative_case = case_dir.relative_to(output_parent)
    assessment = {
        "checks": checks,
        "decision": decision,
        "expected_decision": case.expected_decision,
        "failed_checks": failed_checks,
        "finding": case.finding,
        "local_repeatability": local_repeatability,
        "result": (
            "PASS" if decision == case.expected_decision else "FAIL"
        ),
        "evidence": {
            "assessment": (
                relative_case / "assessment.json"
            ).as_posix(),
            "clean_rebuild": (
                (relative_case / "evidence" / "clean-rebuild.json").as_posix()
                if clean_rebuild.is_file()
                else None
            ),
            "local_runs": [
                (
                    relative_case / "evidence" / "local-run-a.json"
                ).as_posix(),
                (
                    relative_case / "evidence" / "local-run-b.json"
                ).as_posix(),
            ],
            "workflow_record": (
                relative_case / "evidence" / "workflow-record.json"
            ).as_posix(),
        },
    }
    write_json(case_dir / "assessment.json", assessment)
    return assessment


def run_audit(args: argparse.Namespace) -> dict[str, object]:
    if args.workspace.exists():
        shutil.rmtree(args.workspace)
    args.workspace.mkdir(parents=True)
    contract = read_json(args.specimen / "workflow-contract.json")

    findings = []
    for case in CASES:
        case_dir, record = prepare_case(
            case,
            specimen=args.specimen,
            workspace=args.workspace,
        )
        workflow_record = build_case_evidence(
            case,
            case_dir=case_dir,
            record=record,
            python=args.python,
        )
        findings.append(
            assess_case(
                case,
                case_dir=case_dir,
                record=record,
                contract=contract,
                workflow_record=workflow_record,
                output_parent=args.output.parent,
            )
        )

    return {
        "audit": "workflow_evidence",
        "decision_rule": (
            "Accept a team reproducibility claim only when local reruns agree "
            "and recorded input, implementation, controls, influential files, "
            "runtime, clean rebuild, and recovery evidence all support it."
        ),
        "findings": findings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = run_audit(args)
    write_json(args.output, report)
    if args.check:
        failures = [
            item
            for item in report["findings"]
            if item["result"] != "PASS"
        ]
        if failures:
            names = ", ".join(item["finding"] for item in failures)
            raise SystemExit(f"unexpected workflow evidence decisions: {names}")


if __name__ == "__main__":
    main()
