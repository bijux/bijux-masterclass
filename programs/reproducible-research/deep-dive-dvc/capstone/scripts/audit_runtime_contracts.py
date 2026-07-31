#!/usr/bin/env python3
"""Audit declared and hidden runtime influences in isolated DVC workspaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def fingerprint(env: dict[str, str]) -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": sys.platform,
        "machine": platform.machine(),
        "report_style": env.get("REPORT_STYLE", "<unset>"),
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
    baseline_env = os.environ.copy()
    baseline_env["PATH"] = f"{python.parent}{os.pathsep}{baseline_env.get('PATH', '')}"
    baseline_env["REPORT_STYLE"] = "dot"
    drift_env = baseline_env.copy()
    drift_env["REPORT_STYLE"] = "comma"

    shutil.rmtree(output.parent, ignore_errors=True)
    output.parent.mkdir(parents=True)
    workspace.mkdir(parents=True)
    evidence_dir = output.parent / "evidence"
    evidence_dir.mkdir()
    baseline_fingerprint = fingerprint(baseline_env)
    drift_fingerprint = fingerprint(drift_env)
    write_json(evidence_dir / "baseline-fingerprint.json", baseline_fingerprint)
    write_json(evidence_dir / "drift-fingerprint.json", drift_fingerprint)

    baseline, settled = prepare_case(
        "baseline",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=baseline_env,
    )
    baseline_status = status(
        baseline,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="baseline-status",
        env=baseline_env,
    )
    baseline_declared = values(baseline / "results" / "declared.txt")
    baseline_hidden = values(baseline / "results" / "hidden.txt")

    declared_case, _ = prepare_case(
        "declared-change",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=baseline_env,
    )
    (declared_case / "environment" / "runtime.env").write_text(
        "REPORT_STYLE=comma\n", encoding="utf-8"
    )
    declared_status = status(
        declared_case,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="declared-change-status",
        env=baseline_env,
    )
    declared_before = values(declared_case / "results" / "declared.txt")
    run(
        [*dvc, "repro", "declared_runtime"],
        cwd=declared_case,
        evidence_dir=evidence_dir,
        name="declared-change-repro",
        env=baseline_env,
    )
    declared_after = values(declared_case / "results" / "declared.txt")

    hidden_case, _ = prepare_case(
        "hidden-change",
        specimen=specimen,
        workspace=workspace,
        evidence_dir=evidence_dir,
        dvc=dvc,
        env=baseline_env,
    )
    hidden_declaration_before = sha256(hidden_case / "dvc.yaml")
    hidden_lock_before = sha256(hidden_case / "dvc.lock")
    hidden_before = values(hidden_case / "results" / "hidden.txt")
    hidden_status = status(
        hidden_case,
        dvc=dvc,
        evidence_dir=evidence_dir,
        name="hidden-change-status",
        env=drift_env,
    )
    ordinary_repro = run(
        [*dvc, "repro", "hidden_runtime"],
        cwd=hidden_case,
        evidence_dir=evidence_dir,
        name="hidden-change-ordinary-repro",
        env=drift_env,
    )
    hidden_after_ordinary = values(hidden_case / "results" / "hidden.txt")
    run(
        [*dvc, "repro", "--force", "hidden_runtime"],
        cwd=hidden_case,
        evidence_dir=evidence_dir,
        name="hidden-change-forced-repro",
        env=drift_env,
    )
    hidden_after_force = values(hidden_case / "results" / "hidden.txt")
    hidden_declaration_after = sha256(hidden_case / "dvc.yaml")
    hidden_lock_after = sha256(hidden_case / "dvc.lock")

    findings = [
        finding(
            "BASELINE_CONVERGES",
            "ACCEPT",
            {
                "both_stages_skip_on_second_repro": settled.stdout.count(
                    "didn't change, skipping"
                )
                == 2,
                "status_is_empty": baseline_status == {},
                "declared_and_hidden_semantics_match": baseline_declared["rendered"]
                == baseline_hidden["rendered"],
                "baseline_style_is_dot": baseline_declared["style"]
                == baseline_hidden["style"]
                == "dot",
            },
            {
                "status": baseline_status,
                "declared": baseline_declared,
                "hidden": baseline_hidden,
            },
        ),
        finding(
            "DECLARED_RUNTIME_CHANGE_IS_STALE",
            "ACCEPT",
            {
                "declared_stage_is_stale": "declared_runtime" in declared_status,
                "hidden_stage_is_not_stale": "hidden_runtime" not in declared_status,
                "pre_rebuild_value_is_old": declared_before["style"] == "dot",
            },
            {"status": declared_status, "before": declared_before},
        ),
        finding(
            "DECLARED_RUNTIME_REBUILD_ADOPTS_POLICY",
            "ACCEPT",
            {
                "style_is_current": declared_after["style"] == "comma",
                "rendered_value_is_current": declared_after["rendered"] == "8,00",
                "semantic_value_changes": declared_before["rendered"]
                != declared_after["rendered"],
            },
            {"before": declared_before, "after": declared_after},
        ),
        finding(
            "HIDDEN_RUNTIME_CHANGE_IS_INVISIBLE",
            "REJECT",
            {
                "status_is_empty": hidden_status == {},
                "declaration_is_unchanged": hidden_declaration_before
                == hidden_declaration_after,
                "process_fingerprint_changed": baseline_fingerprint["report_style"]
                != drift_fingerprint["report_style"],
            },
            {
                "status": hidden_status,
                "baseline_fingerprint": baseline_fingerprint,
                "drift_fingerprint": drift_fingerprint,
            },
        ),
        finding(
            "ORDINARY_REPRO_PRESERVES_STALE_RUNTIME_MEANING",
            "REJECT",
            {
                "stage_is_skipped": "didn't change, skipping"
                in ordinary_repro.stdout,
                "output_remains_dot": hidden_after_ordinary["style"] == "dot",
                "rendered_value_remains_old": hidden_after_ordinary["rendered"]
                == "8.00",
            },
            {
                "before": hidden_before,
                "after_ordinary_repro": hidden_after_ordinary,
            },
        ),
        finding(
            "FORCED_RUN_CHANGES_OUTPUT_WITH_STABLE_DECLARATION",
            "REJECT",
            {
                "output_adopts_hidden_style": hidden_after_force["style"]
                == "comma",
                "rendered_value_changes": hidden_after_force["rendered"] == "8,00",
                "dvc_yaml_is_stable": hidden_declaration_before
                == hidden_declaration_after,
                "lock_changes_only_after_execution": hidden_lock_before
                != hidden_lock_after,
            },
            {
                "before": hidden_before,
                "after_force": hidden_after_force,
                "declaration_sha256": hidden_declaration_after,
                "lock_before_sha256": hidden_lock_before,
                "lock_after_sha256": hidden_lock_after,
            },
        ),
        finding(
            "FINGERPRINT_EXPOSES_RUNTIME_MISMATCH",
            "ACCEPT",
            {
                "python_is_held_constant": baseline_fingerprint["python"]
                == drift_fingerprint["python"],
                "platform_is_held_constant": baseline_fingerprint["platform"]
                == drift_fingerprint["platform"],
                "report_style_differs": baseline_fingerprint["report_style"]
                != drift_fingerprint["report_style"],
            },
            {
                "baseline": baseline_fingerprint,
                "drift": drift_fingerprint,
            },
        ),
    ]

    report = {
        "specimen": specimen.as_posix(),
        "workspace": workspace.as_posix(),
        "findings": findings,
    }
    write_json(output, report)
    write_summary(output.parent / "summary.tsv", findings)
    failed = [item["finding"] for item in findings if item["result"] != "PASS"]
    if failed:
        print(f"FAIL: runtime contract audit failed: {', '.join(failed)}")
        return 1
    print(f"PASS: audited runtime contracts in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
