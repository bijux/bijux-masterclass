from __future__ import annotations

import sys
from pathlib import Path

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = CAPSTONE_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from audit_software_boundaries import MODEL_CONTRACTS, evaluate_model  # noqa: E402


def test_specimens_cover_three_distinct_source_contracts() -> None:
    assert list(MODEL_CONTRACTS) == [
        "script-directive",
        "hidden-package-source",
        "declared-package-source",
    ]

    specimens = CAPSTONE_ROOT / "repro" / "software-boundaries"
    script_snakefile = (specimens / "script-directive" / "Snakefile").read_text(
        encoding="utf-8"
    )
    hidden_snakefile = (specimens / "hidden-package-source" / "Snakefile").read_text(
        encoding="utf-8"
    )
    declared_snakefile = (specimens / "declared-package-source" / "Snakefile").read_text(
        encoding="utf-8"
    )

    assert 'script:\n        "workflow/scripts/render.py"' in script_snakefile
    assert 'implementation="src/software_specimen/render.py"' not in hidden_snakefile
    assert 'implementation="src/software_specimen/render.py"' in declared_snakefile


def test_accepted_source_contract_requires_observed_rerun() -> None:
    result, failures = evaluate_model(
        baseline_converged=True,
        changed_dryrun_succeeded=True,
        rerun_planned=True,
        changed_execution_succeeded=True,
        artifact_marker="declared-package-source-v2",
        expected_rerun=True,
    )

    assert result == "PASS"
    assert failures == []


def test_hidden_source_contract_requires_stale_artifact_reproduction() -> None:
    result, failures = evaluate_model(
        baseline_converged=True,
        changed_dryrun_succeeded=True,
        rerun_planned=False,
        changed_execution_succeeded=True,
        artifact_marker="hidden-package-source-v1",
        expected_rerun=False,
    )

    assert result == "PASS"
    assert failures == []


def test_audit_rejects_unexpected_planning_behavior() -> None:
    result, failures = evaluate_model(
        baseline_converged=True,
        changed_dryrun_succeeded=True,
        rerun_planned=False,
        changed_execution_succeeded=True,
        artifact_marker="declared-package-source-v1",
        expected_rerun=True,
    )

    assert result == "FAIL"
    assert failures == [
        "source drift has expected planning behavior",
        "artifact reflects planning behavior",
    ]


def test_audit_rejects_nonconverged_baseline() -> None:
    result, failures = evaluate_model(
        baseline_converged=False,
        changed_dryrun_succeeded=True,
        rerun_planned=True,
        changed_execution_succeeded=True,
        artifact_marker="script-directive-v2",
        expected_rerun=True,
    )

    assert result == "FAIL"
    assert failures == ["baseline converges"]
