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
    shutil.copytree(capstone_root() / "repro" / "runtime-contracts", specimen)
    return specimen


def run_audit(
    output_root: Path,
    specimen: Path,
    *,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = output_root / "report.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(capstone_root() / "scripts" / "audit_runtime_contracts.py"),
            "--specimen",
            str(specimen),
            "--workspace",
            str(output_root / "workspace"),
            "--output",
            str(output),
            "--python",
            sys.executable,
        ],
        check=check,
        text=True,
        capture_output=True,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


@pytest.fixture(scope="module")
def audit(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, dict[str, object]]:
    root = tmp_path_factory.mktemp("runtime-contract-audit")
    specimen = specimen_copy(root)
    _, report = run_audit(root / "audit", specimen, check=True)
    return root, report


def test_audit_classifies_declared_and_hidden_runtime_contracts(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit

    assert [item["decision"] for item in report["findings"]] == [
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "REJECT",
        "REJECT",
        "REJECT",
        "ACCEPT",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])


def test_declared_runtime_file_must_remain_a_dependency(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    pipeline = specimen / "dvc.yaml"
    pipeline.write_text(
        pipeline.read_text(encoding="utf-8").replace(
            "      - environment/runtime.env\n", "", 1
        ),
        encoding="utf-8",
    )

    completed, report = run_audit(tmp_path / "audit", specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "DECLARED_RUNTIME_CHANGE_IS_STALE")["checks"]
    assert checks["declared_stage_is_stale"] is False


def test_declared_rebuild_adopts_current_runtime_policy(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    checks = finding(report, "DECLARED_RUNTIME_REBUILD_ADOPTS_POLICY")["checks"]

    assert checks["style_is_current"] is True
    assert checks["rendered_value_is_current"] is True
    assert checks["semantic_value_changes"] is True


def test_hidden_runtime_change_is_absent_from_status(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    finding_record = finding(report, "HIDDEN_RUNTIME_CHANGE_IS_INVISIBLE")

    assert finding_record["decision"] == "REJECT"
    assert finding_record["checks"]["status_is_empty"] is True
    assert finding_record["checks"]["process_fingerprint_changed"] is True


def test_ordinary_repro_preserves_stale_runtime_meaning(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    record = finding(report, "ORDINARY_REPRO_PRESERVES_STALE_RUNTIME_MEANING")

    assert record["checks"]["stage_is_skipped"] is True
    assert record["evidence"]["after_ordinary_repro"]["rendered"] == "8.00"


def test_force_changes_output_without_repairing_declaration(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    record = finding(report, "FORCED_RUN_CHANGES_OUTPUT_WITH_STABLE_DECLARATION")

    assert record["checks"]["output_adopts_hidden_style"] is True
    assert record["checks"]["dvc_yaml_is_stable"] is True
    assert record["checks"]["lock_changes_only_after_execution"] is True


def test_fingerprint_isolates_the_changed_runtime_fact(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    record = finding(report, "FINGERPRINT_EXPOSES_RUNTIME_MISMATCH")

    assert record["checks"] == {
        "platform_is_held_constant": True,
        "python_is_held_constant": True,
        "report_style_differs": True,
    }


def test_audit_replaces_stale_workspace_evidence(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    output_root = tmp_path / "audit"
    run_audit(output_root, specimen, check=True)
    stale = output_root / "workspace" / "stale-evidence.txt"
    stale.write_text("must disappear\n", encoding="utf-8")

    run_audit(output_root, specimen, check=True)

    assert not stale.exists()
