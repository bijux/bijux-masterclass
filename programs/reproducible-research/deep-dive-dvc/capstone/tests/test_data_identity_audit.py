from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def capstone_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_audit(output_root: Path) -> dict[str, object]:
    output = output_root / "report.json"
    subprocess.run(
        [
            sys.executable,
            str(capstone_root() / "scripts" / "audit_data_identity.py"),
            "--specimen",
            str(capstone_root() / "repro" / "data-identity"),
            "--workspace",
            str(output_root / "workspace"),
            "--output",
            str(output),
            "--python",
            sys.executable,
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


@pytest.fixture(scope="module")
def audit(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, dict[str, object]]:
    root = tmp_path_factory.mktemp("data-identity-audit")
    return root, run_audit(root)


def test_audit_classifies_identity_and_recovery_boundaries(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit

    assert [item["decision"] for item in report["findings"]] == [
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "ACCEPT",
        "REJECT",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])


def test_pointer_names_matching_cache_bytes(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    checks = finding(report, "POINTER_NAMES_CACHED_CONTENT")["checks"]

    assert checks == {
        "cache_bytes_match_workspace": True,
        "cache_object_exists": True,
        "pointer_has_content_id": True,
        "pointer_size_matches_workspace": True,
    }


def test_paths_do_not_define_content_identity(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    same = finding(report, "SAME_BYTES_SHARE_IDENTITY")
    changed = finding(report, "CHANGED_BYTES_CHANGE_IDENTITY")

    assert same["checks"]["paths_differ"] is True
    assert same["checks"]["pointer_ids_match"] is True
    assert changed["checks"]["workspace_path_is_stable"] is True
    assert changed["checks"]["pointer_id_changes"] is True


def test_local_cache_restores_workspace_projection(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    checks = finding(report, "CACHE_RESTORES_WORKSPACE")["checks"]

    assert checks["workspace_is_restored"] is True
    assert checks["restored_bytes_match_source"] is True
    assert checks["pointer_identity_is_unchanged"] is True


def test_remote_recovery_repopulates_cache_without_changing_identity(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    recovery = finding(report, "REMOTE_RESTORES_AFTER_CACHE_LOSS")
    identity = finding(report, "REMOTE_RECOVERY_PRESERVES_IDENTITY")

    assert recovery["checks"]["cache_is_repopulated"] is True
    assert recovery["checks"]["restored_bytes_match_source"] is True
    assert identity["checks"]["pointer_id_matches_baseline"] is True
    assert identity["checks"]["restored_sha256_matches_baseline"] is True


def test_pointer_only_failure_is_preserved_as_evidence(
    audit: tuple[Path, dict[str, object]],
) -> None:
    root, report = audit
    rejected = finding(report, "POINTER_ONLY_IS_NOT_RECOVERABLE")
    stderr = (root / "evidence" / "pointer-only-checkout.stderr.txt").read_text(
        encoding="utf-8"
    )

    assert rejected["decision"] == "REJECT"
    assert rejected["checks"]["checkout_fails"] is True
    assert rejected["checks"]["workspace_remains_absent"] is True
    assert "checkout failed" in stderr.lower()
    assert "cache up to date" in stderr.lower()


def test_audit_replaces_stale_workspace_evidence(tmp_path: Path) -> None:
    run_audit(tmp_path)
    stale = tmp_path / "workspace" / "stale-evidence.txt"
    stale.write_text("must disappear\n", encoding="utf-8")

    run_audit(tmp_path)

    assert not stale.exists()


def test_source_specimen_remains_immutable(
    audit: tuple[Path, dict[str, object]],
) -> None:
    _, report = audit
    source = capstone_root() / "repro" / "data-identity" / "source" / "observations.csv"
    pointer_evidence = finding(report, "POINTER_NAMES_CACHED_CONTENT")["evidence"]

    assert source.read_text(encoding="utf-8") == (
        "record_id,signal\nalpha,3\nbeta,5\ngamma,8\n"
    )
    assert pointer_evidence["sha256"]
