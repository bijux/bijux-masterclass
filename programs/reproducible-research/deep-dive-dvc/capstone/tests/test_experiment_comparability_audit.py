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
    shutil.copytree(
        capstone_root() / "repro" / "experiment-comparability",
        specimen,
    )
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
        str(
            capstone_root()
            / "scripts"
            / "audit_experiment_comparability.py"
        ),
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
    root = tmp_path_factory.mktemp("experiment-comparability-audit")
    specimen = specimen_copy(root)
    completed, report = run_audit(root / "audit", specimen, check=True)
    assert completed.returncode == 0, completed.stderr
    return report


def test_audit_keeps_only_the_controlled_candidate_for_promotion_review(
    audit: dict[str, object],
) -> None:
    assert [item["decision"] for item in audit["findings"]] == [
        "KEEP_FOR_PROMOTION_REVIEW",
        "BLOCK_COMPARISON",
        "BLOCK_COMPARISON",
        "BLOCK_COMPARISON",
        "BLOCK_COMPARISON",
        "BLOCK_COMPARISON",
        "BLOCK_PROMOTION",
    ]
    assert all(item["result"] == "PASS" for item in audit["findings"])


def test_controlled_candidate_preserves_every_comparison_boundary(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "CONTROLLED_THRESHOLD")

    assert record["changed_paths"] == ["decision.threshold"]
    assert all(record["checks"].values())
    assert record["failed_checks"] == []


def test_mixed_candidate_exposes_the_extra_control_change(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MIXED_CONTROL_CHANGE")

    assert record["changed_paths"] == [
        "decision.review_capacity",
        "decision.threshold",
    ]
    assert record["failed_checks"] == ["changed_controls_are_allowed"]


def test_baseline_contract_mutation_invalidates_the_anchor(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MUTATED_BASELINE_CONTRACT")

    assert record["checks"]["candidate_reproduced"] is True
    assert record["checks"]["baseline_matches_recorded_contract"] is False
    assert record["decision"] == "BLOCK_COMPARISON"


def test_population_drift_blocks_an_otherwise_successful_run(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "POPULATION_DRIFT")

    assert record["checks"]["candidate_reproduced"] is True
    assert record["checks"]["evaluation_population_is_stable"] is False
    assert record["checks"]["metric_schema_is_stable"] is True


def test_metric_schema_drift_is_not_a_rankable_candidate(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "METRIC_SCHEMA_DRIFT")

    assert record["checks"]["metric_schema_is_stable"] is False
    assert "evaluation.metric_schema" in record["changed_paths"]
    assert record["decision"] == "BLOCK_COMPARISON"


def test_missing_intent_blocks_attribution_before_metric_ranking(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "MISSING_CANDIDATE_INTENT")

    assert record["checks"]["candidate_reproduced"] is True
    assert record["checks"]["candidate_intent_present"] is False
    assert record["decision"] == "BLOCK_COMPARISON"


def test_promotion_requires_a_separate_decision_record(
    audit: dict[str, object],
) -> None:
    record = finding(audit, "UNSAFE_PROMOTION_REQUEST")

    comparison_checks = {
        key: value
        for key, value in record["checks"].items()
        if key != "promotion_decision_is_recorded"
    }
    assert all(comparison_checks.values())
    assert record["checks"]["promotion_decision_is_recorded"] is False
    assert record["decision"] == "BLOCK_PROMOTION"


def test_audit_rejects_a_specimen_with_a_false_baseline_claim(
    tmp_path: Path,
) -> None:
    specimen = specimen_copy(tmp_path)
    contract_path = specimen / "experiment-contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["baseline"]["expected_metrics"]["recall"] = 0.9
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
    record = finding(report, "CONTROLLED_THRESHOLD")
    assert record["result"] == "FAIL"
    assert record["decision"] == "BLOCK_COMPARISON"
