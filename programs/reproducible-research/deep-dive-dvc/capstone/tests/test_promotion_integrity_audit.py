from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def capstone_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_audit(
    output_root: Path,
    *,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    specimen = output_root / "specimen"
    shutil.copytree(
        capstone_root() / "repro" / "promotion-integrity",
        specimen,
    )
    output = output_root / "report.json"
    command = [
        sys.executable,
        str(capstone_root() / "scripts" / "audit_promotion_integrity.py"),
        "--specimen",
        str(specimen),
        "--publish",
        str(capstone_root() / "publish" / "v1"),
        "--lock-file",
        str(capstone_root() / "dvc.lock"),
        "--workspace",
        str(output_root / "workspace"),
        "--output",
        str(output),
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
    root = tmp_path_factory.mktemp("promotion-integrity-audit")
    completed, report = run_audit(root, check=True)
    assert completed.returncode == 0, completed.stderr
    return report


def test_audit_accepts_only_the_complete_promotion(
    audit: dict[str, object],
) -> None:
    assert [item["decision"] for item in audit["findings"]] == [
        "ACCEPT",
        "BLOCK",
        "BLOCK",
        "BLOCK",
        "BLOCK",
        "BLOCK",
        "BLOCK",
    ]
    assert all(item["result"] == "PASS" for item in audit["findings"])


def test_complete_promotion_satisfies_every_gate(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_PROMOTION")

    assert all(record["checks"].values())
    assert record["failed_checks"] == []


def test_manifest_digest_detects_post_approval_tampering(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "TAMPERED_ARTIFACT")

    assert record["failed_checks"] == [
        "artifact_integrity_matches_manifest"
    ]


def test_exact_inventory_rejects_unlisted_candidate_files(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "UNLISTED_ARTIFACT")

    assert record["checks"]["artifact_integrity_matches_manifest"] is True
    assert record["failed_checks"] == ["inventory_matches_contract"]


def test_rehashed_params_cannot_hide_promoted_claim_drift(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "THRESHOLD_DRIFT")

    assert record["checks"]["artifact_integrity_matches_manifest"] is True
    assert record["failed_checks"] == ["promoted_claims_agree"]


def test_mutable_registry_alias_cannot_identify_a_release(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MUTABLE_REGISTRY_REFERENCE")

    assert record["checks"]["decision_matches_candidate"] is True
    assert record["failed_checks"] == [
        "registry_reference_is_immutable"
    ]


def test_approval_for_another_source_revision_blocks_promotion(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "STALE_SOURCE_APPROVAL")

    assert record["checks"]["source_lock_matches_contract"] is True
    assert record["failed_checks"] == ["decision_matches_candidate"]


def test_required_review_role_cannot_be_inferred(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MISSING_REQUIRED_REVIEW")

    assert record["checks"]["decision_matches_candidate"] is True
    assert record["failed_checks"] == [
        "required_review_roles_approved"
    ]


def test_audit_preserves_case_assessments(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_PROMOTION")

    assert record["evidence"].endswith(
        "complete-promotion/assessment.json"
    )
