#!/usr/bin/env python3
"""Audit convergence, hidden inputs, and publication failure boundaries."""

from __future__ import annotations

import argparse
import json
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
    expected_codes: set[int],
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
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
    if completed.returncode not in expected_codes:
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


def snakemake_command(binary: str, target: str, *, dry_run: bool = False) -> list[str]:
    command = [
        binary,
        "--snakefile",
        "Snakefile",
        "--cores",
        "1",
    ]
    if dry_run:
        command.extend(["--dry-run", "--printshellcmds"])
    command.append(target)
    return command


def report_threshold(path: Path) -> str:
    values = dict(
        line.split("=", maxsplit=1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if "=" in line
    )
    return values["threshold"]


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
    parser.add_argument("--snakemake", required=True)
    parser.add_argument("--python", required=True)
    parser.add_argument("--poison-writer", type=Path, required=True)
    parser.add_argument("--atomic-writer", type=Path, required=True)
    args = parser.parse_args()

    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    snakemake = str(Path(args.snakemake).resolve())
    python = str(Path(args.python).resolve())
    poison_writer = args.poison_writer.resolve()
    atomic_writer = args.atomic_writer.resolve()

    shutil.rmtree(output.parent, ignore_errors=True)
    output.parent.mkdir(parents=True)
    shutil.copytree(specimen, workspace)
    evidence_dir = output.parent / "evidence"
    evidence_dir.mkdir(parents=True)

    declared_target = "results/declared-report.txt"
    hidden_target = "results/hidden-report.txt"
    run(
        snakemake_command(snakemake, declared_target),
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="declared-baseline-run",
        expected_codes={0},
    )
    run(
        snakemake_command(snakemake, hidden_target),
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="hidden-baseline-run",
        expected_codes={0},
    )
    settled = run(
        snakemake_command(snakemake, declared_target, dry_run=True),
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="declared-settled-dry-run",
        expected_codes={0},
    )

    declared_report = workspace / declared_target
    hidden_report = workspace / hidden_target
    baseline_declared_threshold = report_threshold(declared_report)
    baseline_hidden_threshold = report_threshold(hidden_report)
    policy_path = workspace / "policy" / "threshold.txt"
    policy_path.write_text("20\n", encoding="utf-8")

    declared_plan = run(
        snakemake_command(snakemake, declared_target, dry_run=True),
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="declared-policy-change-dry-run",
        expected_codes={0},
    )
    hidden_plan = run(
        snakemake_command(snakemake, hidden_target, dry_run=True),
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="hidden-policy-change-dry-run",
        expected_codes={0},
    )

    publication_dir = workspace / "publication"
    publication_dir.mkdir()
    unsafe_final = publication_dir / "unsafe-final.txt"
    unsafe_final.write_text("trusted\n", encoding="utf-8")
    unsafe_failure = run(
        [python, str(poison_writer), str(unsafe_final)],
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="in-place-failure",
        expected_codes={13},
    )

    atomic_final = publication_dir / "atomic-final.txt"
    atomic_final.write_text("trusted\n", encoding="utf-8")
    atomic_failure = run(
        [python, str(atomic_writer), str(atomic_final), "--fail-before-rename"],
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="atomic-failure",
        expected_codes={17},
    )
    atomic_temp = atomic_final.with_suffix(atomic_final.suffix + ".tmp")
    atomic_final_after_failure = atomic_final.read_text(encoding="utf-8")
    atomic_temp_after_failure = atomic_temp.read_text(encoding="utf-8")
    atomic_success = run(
        [python, str(atomic_writer), str(atomic_final)],
        cwd=workspace,
        evidence_dir=evidence_dir,
        name="atomic-success",
        expected_codes={0},
    )

    findings = [
        finding(
            "BASELINE_CONVERGES",
            "ACCEPT",
            {
                "declared_report_built": declared_report.is_file(),
                "hidden_report_built": hidden_report.is_file(),
                "baseline_meaning_matches": baseline_declared_threshold
                == baseline_hidden_threshold
                == "10",
                "settled_dry_run_has_no_jobs": "Nothing to be done" in settled.stdout,
            },
            {
                "declared_threshold": baseline_declared_threshold,
                "hidden_threshold": baseline_hidden_threshold,
            },
        ),
        finding(
            "DECLARED_POLICY_CHANGE_PLANS_RERUN",
            "ACCEPT",
            {
                "policy_changed": policy_path.read_text(encoding="utf-8") == "20\n",
                "declared_rule_planned": "declared_report" in declared_plan.stdout,
                "declared_output_still_records_prior_value": report_threshold(
                    declared_report
                )
                == "10",
            },
            {
                "policy_value": "20",
                "stored_report_value": report_threshold(declared_report),
            },
        ),
        finding(
            "HIDDEN_POLICY_CHANGE_MISSES_RERUN",
            "REJECT",
            {
                "hidden_dry_run_has_no_jobs": "Nothing to be done"
                in hidden_plan.stdout,
                "hidden_rule_not_planned": "hidden_report" not in hidden_plan.stdout,
                "hidden_output_is_stale": report_threshold(hidden_report) == "10",
                "policy_and_output_disagree": report_threshold(hidden_report) != "20",
            },
            {
                "policy_value": "20",
                "stored_report_value": report_threshold(hidden_report),
            },
        ),
        finding(
            "IN_PLACE_FAILURE_POISONS_FINAL",
            "REJECT",
            {
                "writer_failed": unsafe_failure.returncode == 13,
                "trusted_final_was_replaced": unsafe_final.read_text(encoding="utf-8")
                == "PARTIAL\n",
            },
            {"final_contents": unsafe_final.read_text(encoding="utf-8").strip()},
        ),
        finding(
            "ATOMIC_FAILURE_PRESERVES_FINAL",
            "ACCEPT",
            {
                "writer_failed": atomic_failure.returncode == 17,
                "trusted_final_survived": atomic_final_after_failure == "trusted\n",
                "scratch_is_separate": atomic_temp_after_failure == "complete\n",
            },
            {
                "final_after_failure": atomic_final_after_failure.strip(),
                "scratch_after_failure": atomic_temp_after_failure.strip(),
            },
        ),
        finding(
            "ATOMIC_SUCCESS_PROMOTES_COMPLETE_OUTPUT",
            "ACCEPT",
            {
                "writer_succeeded": atomic_success.returncode == 0,
                "final_is_complete": atomic_final.read_text(encoding="utf-8")
                == "complete\n",
                "scratch_was_promoted": not atomic_temp.exists(),
            },
            {"final_contents": atomic_final.read_text(encoding="utf-8").strip()},
        ),
    ]
    report = {
        "claim": (
            "declared influences trigger reruns and atomic publication protects the "
            "final path across process failure"
        ),
        "findings": findings,
        "evidence_directory": str(evidence_dir),
    }
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_summary(output.with_name("summary.tsv"), findings)
    if not all(item["result"] == "PASS" for item in findings):
        return 1
    print(f"PASS: audited file contracts in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
