from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


def source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def specimen_copy(tmp_path: Path) -> Path:
    destination = tmp_path / "specimen"
    shutil.copytree(source_root() / "repro" / "context-invariance", destination)
    return destination


def snakemake_binary() -> str:
    discovered = shutil.which("snakemake")
    if discovered is None:
        raise RuntimeError("snakemake must be on PATH for the context-invariance tests")
    return discovered


def run_audit(
    tmp_path: Path,
    specimen: Path,
    *,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = tmp_path / "audit" / "report.json"
    command = [
        sys.executable,
        str(source_root() / "scripts" / "audit_context_invariance.py"),
        "--specimen",
        str(specimen),
        "--workspace",
        str(tmp_path / "audit" / "workspace"),
        "--output",
        str(output),
        "--snakemake",
        snakemake_binary(),
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=check,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def write_profile(path: Path, payload: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


def test_audit_distinguishes_policy_from_two_semantic_leaks(tmp_path: Path) -> None:
    _, report = run_audit(tmp_path, specimen_copy(tmp_path), check=True)

    assert [item["finding"] for item in report["findings"]] == [
        "CONTEXT_POLICY_PRESERVED",
        "TRUSTED_PATH_LEAK_REPRODUCED",
        "SAMPLE_SCOPE_LEAK_REPRODUCED",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])


def test_audit_replaces_stale_workspace_evidence(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    run_audit(tmp_path, specimen, check=True)
    stale = tmp_path / "audit" / "workspace" / "stale-evidence.txt"
    stale.write_text("must disappear\n", encoding="utf-8")

    run_audit(tmp_path, specimen, check=True)

    assert not stale.exists()


def test_preserving_profile_rejects_semantic_config(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    profile_path = specimen / "profiles" / "ci" / "config.yaml"
    payload = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    payload["config"] = {"publish_root": "publish/ci"}
    write_profile(profile_path, payload)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    assert finding(report, "CONTEXT_POLICY_PRESERVED")["result"] == "FAIL"


def test_preserving_profile_rejects_sample_scope_change(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    profile_path = specimen / "profiles" / "scheduler" / "config.yaml"
    payload = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    payload["config"] = {"samples": ["alpha"]}
    write_profile(profile_path, payload)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "CONTEXT_POLICY_PRESERVED")["comparisons"]["scheduler"]
    assert checks["policy_only_profile"] is False
    assert checks["same_semantic_plan"] is False


def test_trusted_path_specimen_must_change_the_contract_path(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    profile_path = specimen / "profiles" / "trusted-path-leak" / "config.yaml"
    payload = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    payload.pop("config")
    write_profile(profile_path, payload)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    assert finding(report, "TRUSTED_PATH_LEAK_REPRODUCED")["result"] == "FAIL"


def test_sample_scope_specimen_must_remove_beta(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    profile_path = specimen / "profiles" / "sample-scope-leak" / "config.yaml"
    payload = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    payload["config"] = {"samples": ["alpha", "beta"]}
    write_profile(profile_path, payload)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    assert finding(report, "SAMPLE_SCOPE_LEAK_REPRODUCED")["result"] == "FAIL"


def test_sample_scope_specimen_cannot_substitute_a_path_leak(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    profile_path = specimen / "profiles" / "sample-scope-leak" / "config.yaml"
    payload = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    payload["config"] = {"publish_root": "publish/wrong-lesson"}
    write_profile(profile_path, payload)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "SAMPLE_SCOPE_LEAK_REPRODUCED")["checks"]
    assert checks["trusted_path_unchanged"] is False
    assert checks["beta_removed_from_plan"] is False
