#!/usr/bin/env python3
"""Audit scheduler resource translation without scheduler access."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

PROFILE_NAMES = (
    "accepted",
    "missing-memory",
    "underprovisioned-memory",
    "semantic-leak",
)


def run(
    argv: list[str],
    *,
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
    expected_codes: set[int],
) -> int:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    if completed.returncode not in expected_codes:
        raise RuntimeError(f"command returned {completed.returncode}; read {stderr_path}")
    return completed.returncode


def finding(
    name: str,
    decision: str,
    checks: dict[str, bool],
) -> dict[str, Any]:
    return {
        "finding": name,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "decision": decision,
        "checks": checks,
    }


def collect_receipts(
    *,
    specimen: Path,
    workspace: Path,
    python: str,
) -> dict[str, dict[str, Any]]:
    receipts: dict[str, dict[str, Any]] = {}
    for profile_name in PROFILE_NAMES:
        run_dir = workspace / "profiles" / profile_name
        run_dir.mkdir(parents=True, exist_ok=True)
        receipt_path = run_dir / "receipt.json"
        return_code = run(
            [
                python,
                "scripts/record_submission.py",
                "--profile",
                f"config/{profile_name}.yaml",
                "--contract",
                "job-contract.json",
                "--output",
                str(receipt_path),
            ],
            cwd=specimen,
            stdout_path=run_dir / "stdout.txt",
            stderr_path=run_dir / "stderr.txt",
            expected_codes={0, 2},
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["return_code"] = return_code
        receipts[profile_name] = receipt
    return receipts


def classify(
    receipts: dict[str, dict[str, Any]],
    dry_run: str,
) -> list[dict[str, Any]]:
    accepted = receipts["accepted"]
    missing = receipts["missing-memory"]
    under = receipts["underprovisioned-memory"]
    semantic = receipts["semantic-leak"]

    return [
        finding(
            "SCHEDULER_MAPPING_RECORDED",
            "ACCEPT",
            {
                "dry_run_declares_memory": "mem_mb=8000" in dry_run,
                "dry_run_declares_runtime": "runtime=30" in dry_run,
                "receipt_accepted": accepted["status"] == "accepted",
                "receipt_not_executed": accepted["executed"] is False,
                "threads_preserved": accepted["requested"]["threads"] == 4,
                "memory_preserved": accepted["requested"]["mem_mb"] == 8000,
                "runtime_preserved": accepted["requested"]["runtime"] == 30,
                "command_is_reviewable": accepted["argv"][:2]
                == ["sbatch", "--job-name=summarize_records"],
            },
        ),
        finding(
            "MISSING_MEMORY_REJECTED",
            "REJECT",
            {
                "adapter_rejected": missing["status"] == "rejected",
                "nonzero_exit": missing["return_code"] == 2,
                "reason_names_memory": "mem_mb" in missing.get("reason", ""),
            },
        ),
        finding(
            "UNDERPROVISIONING_REJECTED",
            "REJECT",
            {
                "adapter_rejected": under["status"] == "rejected",
                "nonzero_exit": under["return_code"] == 2,
                "reason_names_underprovisioning": "under-provisions"
                in under.get("reason", ""),
            },
        ),
        finding(
            "SEMANTIC_PROFILE_LEAK_REJECTED",
            "REJECT",
            {
                "adapter_rejected": semantic["status"] == "rejected",
                "nonzero_exit": semantic["return_code"] == 2,
                "reason_names_semantics": "semantics"
                in semantic.get("reason", ""),
            },
        ),
    ]


def write_summary(path: Path, findings: list[dict[str, Any]]) -> None:
    rows = ["finding\tresult\tdecision"]
    rows.extend(f"{item['finding']}\t{item['result']}\t{item['decision']}" for item in findings)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--snakemake", required=True)
    parser.add_argument("--python", required=True)
    args = parser.parse_args()

    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    snakemake = str(Path(args.snakemake).resolve())
    python = str(Path(args.python).resolve())
    shutil.rmtree(workspace, ignore_errors=True)
    workspace.mkdir(parents=True)

    dry_run_dir = workspace / "dry-run"
    dry_run_dir.mkdir()
    run(
        [
            snakemake,
            "--snakefile",
            "Snakefile",
            "--cores",
            "1",
            "--dry-run",
            "--printshellcmds",
        ],
        cwd=specimen,
        stdout_path=dry_run_dir / "stdout.txt",
        stderr_path=dry_run_dir / "stderr.txt",
        expected_codes={0},
    )
    dry_run = (dry_run_dir / "stdout.txt").read_text(encoding="utf-8")
    receipts = collect_receipts(
        specimen=specimen,
        workspace=workspace,
        python=python,
    )
    findings = classify(receipts, dry_run)
    report = {
        "claim": (
            "scheduler profiles translate declared resources without changing workflow semantics"
        ),
        "scheduler_contacted": False,
        "findings": findings,
        "receipts": receipts,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_summary(args.output.with_name("summary.tsv"), findings)
    if not all(item["result"] == "PASS" for item in findings):
        return 1
    print(f"PASS: audited scheduler policy in {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
