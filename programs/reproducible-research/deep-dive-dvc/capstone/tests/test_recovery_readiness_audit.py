from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def capstone_root() -> Path:
    return Path(__file__).resolve().parents[1]


def specimen_copy(destination: Path) -> Path:
    specimen = destination / "specimen"
    shutil.copytree(capstone_root() / "repro" / "recovery-readiness", specimen)
    return specimen


def run_audit(
    output_root: Path,
    specimen: Path,
    *,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = output_root / "report.json"
    command = [
        sys.executable,
        str(capstone_root() / "scripts" / "audit_recovery_readiness.py"),
        "--specimen",
        str(specimen),
        "--workspace",
        str(output_root / "workspace"),
        "--output",
        str(output),
        "--dvc",
        str(Path(sys.executable).with_name("dvc")),
    ]
    if check:
        command.append("--check")
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
    root = tmp_path_factory.mktemp("recovery-readiness-audit")
    specimen = specimen_copy(root)
    completed, report = run_audit(root / "audit", specimen, check=True)
    assert completed.returncode == 0, completed.stderr
    return report


def revision(
    record: dict[str, object],
    revision_name: str,
) -> dict[str, object]:
    evidence = record["revision_evidence"]
    assert isinstance(evidence, list)
    return next(
        item for item in evidence if item["revision"] == revision_name
    )


def test_audit_accepts_only_complete_protected_history(
    audit: dict[str, object],
) -> None:
    assert [item["decision"] for item in audit["findings"]] == [
        "ACCEPT",
        "BLOCK",
        "BLOCK",
        "BLOCK",
        "BLOCK",
        "BLOCK",
    ]
    assert all(item["result"] == "PASS" for item in audit["findings"])


def test_complete_migration_restores_both_protected_revisions(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_MIGRATION")

    assert all(record["checks"].values())
    assert revision(record, "release-2025-q1")["content_claim_matches"]
    assert revision(record, "main")["content_claim_matches"]


def test_current_workspace_success_does_not_prove_release_recovery(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "CURRENT_ONLY_COPY")

    assert revision(record, "main")["restored"] is True
    assert revision(record, "release-2025-q1")["restored"] is False
    assert record["decision"] == "BLOCK"


def test_release_copy_without_current_state_blocks_cutover(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "RELEASE_ONLY_COPY")

    assert revision(record, "release-2025-q1")["restored"] is True
    assert revision(record, "main")["restored"] is False
    assert record["decision"] == "BLOCK"


def test_restore_success_cannot_rescue_a_stale_content_claim(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "STALE_RELEASE_CLAIM")
    released = revision(record, "release-2025-q1")

    assert released["restored"] is True
    assert released["content_claim_matches"] is False
    assert record["failed_checks"] == ["all_content_claims_match"]


def test_recovery_evidence_cannot_depend_on_remote_mutation(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MUTATING_RECOVERY_ROUTE")

    assert record["checks"]["all_protected_revisions_restored"] is True
    assert record["checks"]["recovery_route_is_read_only"] is False
    assert record["decision"] == "BLOCK"


def test_recovery_time_must_be_a_declared_objective(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MISSING_TIME_OBJECTIVE")

    assert record["checks"]["all_protected_revisions_restored"] is True
    assert record["checks"]["time_objective_declared"] is False
    assert record["checks"]["all_restores_within_objective"] is False


def test_audit_preserves_revision_evidence_and_command_receipts(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_MIGRATION")
    evidence = record["evidence"]

    assert evidence["revision_evidence"].endswith("revision-evidence.json")
    assert evidence["receipts"].endswith("receipts.json")
