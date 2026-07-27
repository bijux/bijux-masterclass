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
    shutil.copytree(capstone_root() / "repro" / "metric-contracts", specimen)
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
        str(capstone_root() / "scripts" / "audit_metric_contracts.py"),
        "--specimen",
        str(specimen),
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
    root = tmp_path_factory.mktemp("metric-contract-audit")
    specimen = specimen_copy(root)
    completed, report = run_audit(root / "audit", specimen, check=True)
    assert completed.returncode == 0, completed.stderr
    return report


def test_audit_classifies_compatible_and_incompatible_metric_claims(
    audit: dict[str, object],
) -> None:
    assert [item["decision"] for item in audit["findings"]] == [
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "REJECT",
        "REJECT",
        "REJECT",
        "REJECT",
        "REJECT",
    ]
    assert all(item["result"] == "PASS" for item in audit["findings"])


def test_comparable_candidate_supports_a_bounded_improvement_claim(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "COMPARABLE_CANDIDATE")

    assert record["values"]["delta"] == 0.0458
    assert all(record["checks"].values())


def test_additive_metric_preserves_the_primary_contract(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "ADDITIVE_METRIC")

    assert record["decision"] == "ACCEPT"
    assert record["metric_keys"]["added"] == [
        "false_positive_rate_at_fixed_threshold"
    ]
    assert record["metric_keys"]["removed"] == []


def test_equal_row_counts_do_not_hide_population_identity_drift(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "POPULATION_DRIFT")

    assert record["checks"]["population_rows_same"] is True
    assert record["checks"]["population_identity_same"] is False
    assert record["decision"] == "REJECT"


def test_familiar_metric_name_does_not_hide_unit_drift(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "UNIT_DRIFT")

    assert record["checks"]["metric_name_same"] is True
    assert record["checks"]["metric_unit_same"] is False
    assert record["values"]["delta"] == 77.5241


def test_parameter_control_drift_changes_the_metric_claim(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "CONTROL_DRIFT")

    assert record["checks"]["decision_threshold_same"] is False
    assert record["values"]["delta"] == 0.0458
    assert record["decision"] == "REJECT"


def test_dvc_reports_numeric_movement_for_every_rejected_case(
    audit: dict[str, object],
) -> None:
    rejected = [
        record
        for record in audit["findings"]
        if record["decision"] == "REJECT"
    ]

    assert rejected
    assert all(
        record["checks"]["dvc_reports_primary_value_change"] is True
        for record in rejected
    )


def test_audit_fails_when_expected_population_drift_is_removed(
    tmp_path: Path,
) -> None:
    specimen = specimen_copy(tmp_path)
    baseline = json.loads(
        (specimen / "cases" / "baseline.json").read_text(encoding="utf-8")
    )
    population_case_path = specimen / "cases" / "population-drift.json"
    population_case = json.loads(
        population_case_path.read_text(encoding="utf-8")
    )
    population_case["population"]["identity"] = baseline["population"]["identity"]
    population_case_path.write_text(
        json.dumps(population_case, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    completed, report = run_audit(
        tmp_path / "audit",
        specimen,
        check=True,
    )

    assert completed.returncode != 0
    record = finding(report, "POPULATION_DRIFT")
    assert record["result"] == "FAIL"
    assert record["decision"] == "ACCEPT"
