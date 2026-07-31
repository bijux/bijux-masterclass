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
        str(capstone_root() / "scripts" / "audit_workflow_evidence.py"),
        "--specimen",
        str(capstone_root() / "repro" / "workflow-evidence"),
        "--workspace",
        str(output_root / "workspace"),
        "--output",
        str(output),
        "--python",
        sys.executable,
        "--check",
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


@pytest.fixture(scope="module")
def audit(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    root = tmp_path_factory.mktemp("workflow-evidence-audit")
    completed, report = run_audit(root)
    assert completed.returncode == 0, completed.stderr
    return report


def test_only_complete_evidence_supports_the_reproducibility_claim(
    audit: dict[str, object],
) -> None:
    assert [item["decision"] for item in audit["findings"]] == [
        "ACCEPT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
        "REJECT_REPRODUCIBILITY_CLAIM",
    ]
    assert all(item["result"] == "PASS" for item in audit["findings"])


def test_every_case_is_locally_repeatable(
    audit: dict[str, object],
) -> None:
    assert all(item["local_repeatability"] for item in audit["findings"])


def test_complete_evidence_satisfies_every_required_check(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_EVIDENCE")

    assert all(record["checks"].values())
    assert record["failed_checks"] == []
    assert record["evidence"]["clean_rebuild"].endswith(
        "clean-rebuild.json"
    )


@pytest.mark.parametrize(
    ("finding_name", "failed_check"),
    [
        ("SAME_WORKSPACE_RERUN", "clean_rebuild_matches"),
        ("HIDDEN_THRESHOLD", "controls_are_declared"),
        ("CHANGED_INPUT_SAME_PATH", "input_identity_matches"),
        (
            "MANUAL_PREPROCESSING",
            "all_influential_inputs_are_declared",
        ),
        ("MISSING_RUNTIME", "runtime_is_recorded"),
        ("UNRECOVERABLE_INPUT", "input_is_recoverable"),
        ("STALE_IMPLEMENTATION", "implementation_identity_matches"),
    ],
)
def test_each_rejected_claim_isolates_one_evidence_gap(
    audit: dict[str, object],
    finding_name: str,
    failed_check: str,
) -> None:
    record = finding(audit, finding_name)

    assert record["failed_checks"] == [failed_check]
    assert record["checks"][failed_check] is False


def test_same_workspace_rerun_has_no_clean_rebuild_receipt(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "SAME_WORKSPACE_RERUN")

    assert record["local_repeatability"] is True
    assert record["evidence"]["clean_rebuild"] is None


def test_every_decision_preserves_a_reviewable_assessment(
    audit: dict[str, object],
) -> None:
    for record in audit["findings"]:
        evidence = record["evidence"]
        assert evidence["assessment"].endswith("assessment.json")
        assert len(evidence["local_runs"]) == 2
        assert evidence["workflow_record"].endswith(
            "workflow-record.json"
        )
