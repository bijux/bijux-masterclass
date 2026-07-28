from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def capstone_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_audit(
    output_root: Path,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = output_root / "report.json"
    command = [
        sys.executable,
        str(capstone_root() / "scripts" / "audit_boundary_migration.py"),
        "--specimen",
        str(capstone_root() / "repro" / "boundary-migration"),
        "--publish",
        str(capstone_root() / "publish" / "v1"),
        "--workspace",
        str(output_root / "workspace"),
        "--output",
        str(output),
        "--evaluation-date",
        "2026-07-28",
        "--check",
    ]
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


@pytest.fixture(scope="module")
def audit(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    root = tmp_path_factory.mktemp("boundary-migration-audit")
    completed, report = run_audit(root)
    assert completed.returncode == 0, completed.stderr
    return report


def test_audit_approves_only_the_complete_cutover(
    audit: dict[str, object],
) -> None:
    assert [item["decision"] for item in audit["findings"]] == [
        "APPROVE_CUTOVER",
        "BLOCK_CUTOVER",
        "BLOCK_CUTOVER",
        "BLOCK_CUTOVER",
        "BLOCK_CUTOVER",
        "BLOCK_CUTOVER",
        "BLOCK_CUTOVER",
        "BLOCK_CUTOVER",
    ]
    assert all(item["result"] == "PASS" for item in audit["findings"])


def test_complete_cutover_satisfies_every_governance_check(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_CUTOVER")

    assert all(record["checks"].values())
    assert record["source_inventory"] == record["target_inventory"]
    assert record["failed_checks"] == []


@pytest.mark.parametrize(
    ("finding_name", "failed_check"),
    [
        ("PARTIAL_COPY", "target_matches_source"),
        ("UNBOUNDED_CHANGE", "one_boundary_changes"),
        ("NO_ROLLBACK", "rollback_is_ready"),
        ("UNVERIFIED_CONSUMER", "consumer_cutover_is_verified"),
        ("OWNERLESS_TARGET", "responsibilities_have_owners"),
        ("STALE_EXCEPTION", "exception_is_current"),
        ("TOOL_OWNERSHIP_OVERREACH", "tool_boundaries_match_policy"),
    ],
)
def test_each_blocked_cutover_isolates_one_failed_contract(
    audit: dict[str, object],
    finding_name: str,
    failed_check: str,
) -> None:
    record = finding(audit, finding_name)

    assert record["decision"] == "BLOCK_CUTOVER"
    assert record["failed_checks"] == [failed_check]
    assert record["checks"][failed_check] is False


def test_partial_copy_records_the_missing_target_artifact(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "PARTIAL_COPY")

    assert "report.md" in record["source_inventory"]
    assert "report.md" not in record["target_inventory"]


def test_decisions_preserve_a_reviewable_assessment(
    audit: dict[str, object],
) -> None:
    for record in audit["findings"]:
        evidence = record["evidence"]
        assert evidence.startswith("workspace/")
        assert evidence.endswith("/assessment.json")
