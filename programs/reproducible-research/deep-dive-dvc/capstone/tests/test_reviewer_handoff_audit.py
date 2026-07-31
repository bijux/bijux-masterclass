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
    shutil.copytree(capstone_root() / "repro" / "reviewer-handoff", specimen)
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
        str(capstone_root() / "scripts" / "audit_reviewer_handoffs.py"),
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
    root = tmp_path_factory.mktemp("reviewer-handoff-audit")
    specimen = specimen_copy(root)
    completed, report = run_audit(root / "audit", specimen, check=True)
    assert completed.returncode == 0, completed.stderr
    return report


def test_audit_accepts_only_the_complete_handoff(
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


def test_complete_handoff_passes_every_independent_review_check(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPLETE_HANDOFF")

    assert all(record["checks"].values())
    assert record["failed_checks"] == []


def test_missing_remote_object_blocks_recovery_and_reproduction(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MISSING_REMOTE_OBJECT")

    assert record["checks"]["remote_discoverable"] is True
    assert record["checks"]["pull_succeeded"] is False
    assert record["checks"]["repro_succeeded"] is False


def test_local_remote_configuration_is_not_a_handoff(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "UNDISCOVERABLE_REMOTE")

    assert record["checks"]["remote_discoverable"] is False
    assert record["checks"]["pull_succeeded"] is False


def test_untracked_stage_dependency_breaks_the_clean_reviewer(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "UNTRACKED_STAGE_DEPENDENCY")

    assert record["checks"]["pull_succeeded"] is True
    assert record["checks"]["recorded_state_clean_before_repro"] is False
    assert record["checks"]["repro_succeeded"] is False


def test_successful_reproduction_does_not_repair_a_stale_handoff_claim(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "STALE_EXECUTION_RECORD")

    assert record["checks"]["pull_succeeded"] is True
    assert record["checks"]["recorded_state_clean_before_repro"] is False
    assert record["checks"]["repro_succeeded"] is True
    assert record["checks"]["result_matches_claim"] is False


def test_review_route_must_not_require_remote_mutation(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MUTATING_REVIEW_ROUTE")

    assert record["failed_checks"] == [
        "review_route_avoids_remote_mutation"
    ]


def test_executable_state_without_a_result_contract_still_blocks(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MISSING_RESULT_CONTRACT")

    assert record["checks"]["pull_succeeded"] is True
    assert record["checks"]["repro_succeeded"] is True
    assert record["checks"]["result_contract_present"] is False


def test_audit_rejects_a_complete_specimen_without_its_claim(
    tmp_path: Path,
) -> None:
    specimen = specimen_copy(tmp_path)
    contract_path = specimen / "handoff-contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract.pop("claim")
    contract_path.write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    completed, report = run_audit(
        tmp_path / "audit",
        specimen,
        check=True,
    )

    assert completed.returncode != 0
    record = finding(report, "COMPLETE_HANDOFF")
    assert record["result"] == "FAIL"
    assert record["decision"] == "BLOCK"
