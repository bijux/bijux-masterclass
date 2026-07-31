from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def specimen_copy(tmp_path: Path) -> Path:
    destination = tmp_path / "specimen"
    shutil.copytree(source_root() / "repro" / "scheduler-policy", destination)
    return destination


def snakemake_binary() -> str:
    discovered = shutil.which("snakemake")
    if discovered is not None:
        return discovered
    environment_binary = Path(sys.executable).with_name("snakemake")
    if environment_binary.is_file():
        return str(environment_binary)
    raise RuntimeError(
        "snakemake must be on PATH or installed beside the active Python interpreter"
    )


def run_audit(
    tmp_path: Path,
    specimen: Path,
    *,
    check: bool,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    output = tmp_path / "audit" / "report.json"
    command = [
        sys.executable,
        str(source_root() / "scripts" / "audit_scheduler_policy.py"),
        "--specimen",
        str(specimen),
        "--workspace",
        str(tmp_path / "audit" / "workspace"),
        "--output",
        str(output),
        "--snakemake",
        snakemake_binary(),
        "--python",
        sys.executable,
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=check,
    )
    return completed, json.loads(output.read_text(encoding="utf-8"))


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


def change_json(path: Path, **changes: object) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.update(changes)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_audit_accepts_mapping_and_rejects_three_policy_faults(tmp_path: Path) -> None:
    _, report = run_audit(tmp_path, specimen_copy(tmp_path), check=True)

    assert [item["decision"] for item in report["findings"]] == [
        "ACCEPT",
        "REJECT",
        "REJECT",
        "REJECT",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])
    assert report["scheduler_contacted"] is False


def test_audit_removes_stale_receipts(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    run_audit(tmp_path, specimen, check=True)
    stale = tmp_path / "audit" / "workspace" / "stale-receipt.json"
    stale.write_text("{}\n", encoding="utf-8")

    run_audit(tmp_path, specimen, check=True)

    assert not stale.exists()


def test_accepted_mapping_must_preserve_declared_threads(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_json(specimen / "job-contract.json", threads=6)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "SCHEDULER_MAPPING_RECORDED")["checks"]
    assert checks["threads_preserved"] is False


def test_missing_memory_case_must_remove_memory(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_json(specimen / "config" / "missing-memory.yaml", drop_resources=[])

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "MISSING_MEMORY_REJECTED")["checks"]
    assert checks["adapter_rejected"] is False


def test_underprovisioning_case_must_request_less_memory(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_json(
        specimen / "config" / "underprovisioned-memory.yaml",
        memory_scale=1.0,
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "UNDERPROVISIONING_REJECTED")["checks"]
    assert checks["adapter_rejected"] is False


def test_semantic_leak_case_must_change_workflow_meaning(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_json(
        specimen / "config" / "semantic-leak.yaml",
        semantic_overrides={},
    )

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "SEMANTIC_PROFILE_LEAK_REJECTED")["checks"]
    assert checks["adapter_rejected"] is False


def test_receipt_explicitly_denies_scheduler_execution(tmp_path: Path) -> None:
    _, report = run_audit(tmp_path, specimen_copy(tmp_path), check=True)

    receipt = report["receipts"]["accepted"]
    assert receipt["executed"] is False
    assert receipt["argv"][0] == "sbatch"
