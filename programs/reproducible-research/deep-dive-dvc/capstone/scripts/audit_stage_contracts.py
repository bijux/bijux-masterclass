#!/usr/bin/env python3
"""Audit declared and hidden DVC stage influences with isolated workspaces."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def run(
    argv: list[str],
    *,
    cwd: Path,
    evidence_dir: Path,
    name: str,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        capture_output=True,
    )
    (evidence_dir / f"{name}.stdout.txt").write_text(
        completed.stdout, encoding="utf-8"
    )
    (evidence_dir / f"{name}.stderr.txt").write_text(
        completed.stderr, encoding="utf-8"
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{name} returned {completed.returncode}; inspect {evidence_dir}"
        )
    return completed


def finding(
    name: str,
    decision: str,
    checks: dict[str, bool],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "finding": name,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "decision": decision,
        "checks": checks,
        "evidence": evidence,
    }


def values(path: Path) -> dict[str, str]:
    return dict(
        line.split("=", maxsplit=1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if "=" in line
    )


def prepare_case(
    name: str,
    *,
    specimen: Path,
    workspace: Path,
    evidence_dir: Path,
    dvc: list[str],
    env: dict[str, str],
) -> tuple[Path, subprocess.CompletedProcess[str]]:
    case = workspace / name
    shutil.copytree(specimen, case)
    run(
        [*dvc, "init", "--no-scm", "-q"],
        cwd=case,
        evidence_dir=evidence_dir,
        name=f"{name}-init",
        env=env,
    )
    run(
        [*dvc, "repro"],
        cwd=case,
        evidence_dir=evidence_dir,
        name=f"{name}-baseline-repro",
        env=env,
    )
    settled = run(
        [*dvc, "repro"],
        cwd=case,
        evidence_dir=evidence_dir,
        name=f"{name}-settled-repro",
        env=env,
    )
    return case, settled


def status(
    case: Path,
    *,
    dvc: list[str],
    evidence_dir: Path,
    name: str,
    env: dict[str, str],
) -> dict[str, Any]:
    completed = run(
        [*dvc, "status", "--json"],
        cwd=case,
        evidence_dir=evidence_dir,
        name=name,
        env=env,
    )
    return json.loads(completed.stdout)


def write_summary(path: Path, findings: list[dict[str, Any]]) -> None:
    rows = ["finding\tresult\tdecision"]
    rows.extend(
        f"{item['finding']}\t{item['result']}\t{item['decision']}"
        for item in findings
    )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    args = parser.parse_args()

    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    python = args.python.absolute()
    dvc = [str(python), "-m", "dvc"]
    env = os.environ.copy()
    env["PATH"] = f"{python.parent}{os.pathsep}{env.get('PATH', '')}"

    shutil.rmtree(output.parent, ignore_errors=True)
    output.parent.mkdir(parents=True)
    workspace.mkdir(parents=True)
    evidence_dir = output.parent / "evidence"
    evidence_dir.mkdir()

    baseline, settled = prepare_case(
        "baseline",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    baseline_status = status(
        baseline,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="baseline-status",
        env=env,
    )

    input_case, _ = prepare_case(
        "input-change",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    (input_case / "policy" / "threshold.txt").write_text("20\n", encoding="utf-8")
    input_status = status(
        input_case,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="input-change-status",
        env=env,
    )
    declared_input_before = values(input_case / "results" / "declared-input.txt")
    hidden_input_before = values(input_case / "results" / "hidden-input.txt")
    run(
        [*dvc, "repro", "declared_input"],
        cwd=input_case,
        evidence_dir=evidence_dir,
        name="declared-input-repro",
        env=env,
    )
    declared_input_after = values(input_case / "results" / "declared-input.txt")
    hidden_input_after = values(input_case / "results" / "hidden-input.txt")

    param_case, _ = prepare_case(
        "param-change",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    (param_case / "params.yaml").write_text(
        "settings:\n  multiplier: 3\n", encoding="utf-8"
    )
    param_status = status(
        param_case,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="param-change-status",
        env=env,
    )
    declared_param_before = values(param_case / "results" / "declared-param.txt")
    hidden_param_before = values(param_case / "results" / "hidden-param.txt")
    run(
        [*dvc, "repro", "declared_param"],
        cwd=param_case,
        evidence_dir=evidence_dir,
        name="declared-param-repro",
        env=env,
    )
    declared_param_after = values(param_case / "results" / "declared-param.txt")
    hidden_param_after = values(param_case / "results" / "hidden-param.txt")

    output_case, _ = prepare_case(
        "output-loss",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=env,
    )
    sidecar = output_case / "results" / "undeclared-receipt.txt"
    sidecar.unlink()
    output_status = status(
        output_case,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="output-loss-status",
        env=env,
    )
    output_repro = run(
        [*dvc, "repro", "undeclared_sidecar"],
        cwd=output_case,
        evidence_dir=evidence_dir,
        name="output-loss-repro",
        env=env,
    )

    findings = [
        finding(
            "BASELINE_CONVERGES",
            "ACCEPT",
            {
                "second_repro_skips_all_stages": settled.stdout.count(
                    "didn't change, skipping"
                )
                == 5,
                "status_is_empty": baseline_status == {},
                "declared_and_hidden_input_values_match": values(
                    baseline / "results" / "declared-input.txt"
                )
                == values(baseline / "results" / "hidden-input.txt"),
                "declared_and_hidden_param_values_match": values(
                    baseline / "results" / "declared-param.txt"
                )
                == values(baseline / "results" / "hidden-param.txt"),
            },
            {"status": baseline_status},
        ),
        finding(
            "DECLARED_INPUT_CHANGE_IS_STALE",
            "ACCEPT",
            {
                "declared_stage_is_stale": "declared_input" in input_status,
                "hidden_stage_is_not_stale": "hidden_input" not in input_status,
                "both_outputs_still_hold_prior_value": declared_input_before[
                    "threshold"
                ]
                == hidden_input_before["threshold"]
                == "10",
            },
            {"status": input_status},
        ),
        finding(
            "DECLARED_INPUT_REBUILDS_CURRENT_VALUE",
            "ACCEPT",
            {
                "declared_output_records_current_value": declared_input_after[
                    "threshold"
                ]
                == "20",
                "hidden_output_remains_prior_value": hidden_input_after["threshold"]
                == "10",
            },
            {
                "declared_threshold": declared_input_after["threshold"],
                "hidden_threshold": hidden_input_after["threshold"],
            },
        ),
        finding(
            "HIDDEN_INPUT_CHANGE_IS_INVISIBLE",
            "REJECT",
            {
                "hidden_stage_is_absent_from_status": "hidden_input"
                not in input_status,
                "hidden_output_is_semantically_stale": hidden_input_after["threshold"]
                != "20",
            },
            {
                "policy_value": "20",
                "hidden_threshold": hidden_input_after["threshold"],
            },
        ),
        finding(
            "DECLARED_PARAM_CHANGE_IS_STALE",
            "ACCEPT",
            {
                "declared_stage_is_stale": "declared_param" in param_status,
                "hidden_stage_is_not_stale": "hidden_param" not in param_status,
                "both_outputs_still_hold_prior_value": declared_param_before[
                    "multiplier"
                ]
                == hidden_param_before["multiplier"]
                == "2",
            },
            {"status": param_status},
        ),
        finding(
            "DECLARED_PARAM_REBUILDS_CURRENT_VALUE",
            "ACCEPT",
            {
                "declared_output_records_current_value": declared_param_after[
                    "multiplier"
                ]
                == "3",
                "declared_score_uses_current_value": declared_param_after["score"]
                == "24",
                "hidden_output_remains_prior_value": hidden_param_after["multiplier"]
                == "2",
            },
            {
                "declared_multiplier": declared_param_after["multiplier"],
                "hidden_multiplier": hidden_param_after["multiplier"],
            },
        ),
        finding(
            "HIDDEN_PARAM_CHANGE_IS_INVISIBLE",
            "REJECT",
            {
                "hidden_stage_is_absent_from_status": "hidden_param"
                not in param_status,
                "hidden_output_is_semantically_stale": hidden_param_after["multiplier"]
                != "3",
            },
            {
                "parameter_value": "3",
                "hidden_multiplier": hidden_param_after["multiplier"],
            },
        ),
        finding(
            "UNDECLARED_OUTPUT_LOSS_IS_INVISIBLE",
            "REJECT",
            {
                "stage_is_absent_from_status": "undeclared_sidecar"
                not in output_status,
                "repro_skips_stage": "didn't change, skipping" in output_repro.stdout,
                "lost_sidecar_is_not_restored": not sidecar.exists(),
            },
            {
                "status": output_status,
                "sidecar_exists_after_repro": sidecar.exists(),
            },
        ),
    ]
    report = {
        "claim": (
            "DVC can react only to declared file, parameter, and output boundaries; "
            "successful baseline execution does not prove those boundaries are complete"
        ),
        "findings": findings,
        "evidence_directory": str(evidence_dir),
    }
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_summary(output.with_name("summary.tsv"), findings)
    if not all(item["result"] == "PASS" for item in findings):
        return 1
    print(f"PASS: audited stage contracts in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
