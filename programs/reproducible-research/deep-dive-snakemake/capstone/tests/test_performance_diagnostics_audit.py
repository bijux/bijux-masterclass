from __future__ import annotations

import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


def source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def specimen_copy(tmp_path: Path) -> Path:
    destination = tmp_path / "specimen"
    shutil.copytree(source_root() / "repro" / "performance-diagnostics", destination)
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
        str(source_root() / "scripts" / "audit_performance_diagnostics.py"),
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


def finding(report: dict[str, object], name: str) -> dict[str, object]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return next(item for item in findings if item["finding"] == name)


def change_config(specimen: Path, name: str, **changes: object) -> None:
    path = specimen / "config" / f"{name}.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    payload.update(changes)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_audit_classifies_reference_accept_reject_and_regression(tmp_path: Path) -> None:
    _, report = run_audit(tmp_path, specimen_copy(tmp_path), check=True)

    assert [item["decision"] for item in report["findings"]] == [
        "REFERENCE",
        "ACCEPT",
        "REJECT",
        "REGRESSION",
    ]
    assert all(item["result"] == "PASS" for item in report["findings"])


def test_audit_replaces_stale_workspace_evidence(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    run_audit(tmp_path, specimen, check=True)
    stale = tmp_path / "audit" / "workspace" / "stale-evidence.txt"
    stale.write_text("must disappear\n", encoding="utf-8")

    run_audit(tmp_path, specimen, check=True)

    assert not stale.exists()


def test_honest_tuning_cannot_disable_validation(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_config(specimen, "honest-tuning", validate=False)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "HONEST_TUNING_ACCEPTED")["checks"]
    assert checks["validation_preserved"] is False


def test_honest_tuning_must_reduce_deterministic_work(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_config(specimen, "honest-tuning", chunk_size=1)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "HONEST_TUNING_ACCEPTED")["checks"]
    assert checks["setup_work_reduced"] is False
    assert checks["deterministic_cost_reduced"] is False


def test_validation_bypass_must_remove_validation_evidence(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_config(specimen, "validation-bypass", validate=True)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "VALIDATION_BYPASS_REJECTED")["checks"]
    assert checks["config_disables_validation"] is False
    assert checks["validation_evidence_missing"] is False


def test_repeated_scan_must_reproduce_extra_work(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    change_config(specimen, "repeated-scan", scan_passes=1)

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "REPEATED_SCAN_REGRESSION_IDENTIFIED")["checks"]
    assert checks["scan_work_increased"] is False
    assert checks["deterministic_cost_increased"] is False


def test_equal_artifact_bytes_remain_part_of_rejection_proof(tmp_path: Path) -> None:
    specimen = specimen_copy(tmp_path)
    script = specimen / "scripts" / "process_records.py"
    source = script.read_text(encoding="utf-8")
    source = source.replace(
        "    rows = normalized_rows(records)\n",
        "    rows = normalized_rows(records)\n"
        '    if args.mode == "validation-bypass":\n'
        "        rows = rows[:-1]\n",
    )
    script.write_text(source, encoding="utf-8")

    completed, report = run_audit(tmp_path, specimen, check=False)

    assert completed.returncode != 0
    checks = finding(report, "VALIDATION_BYPASS_REJECTED")["checks"]
    assert checks["artifact_bytes_match"] is False


@pytest.mark.parametrize("sampled", ["NA", "0", "1.25"])
def test_benchmark_retains_sampled_measurements_and_missing_observations(
    tmp_path: Path, sampled: str
) -> None:
    read_benchmark = runpy.run_path(
        str(source_root() / "scripts" / "audit_performance_diagnostics.py")
    )["read_benchmark"]
    benchmark = tmp_path / "benchmark.tsv"
    benchmark.write_text(
        f"s\tmax_rss\tio_in\tio_out\n0.5\t{sampled}\t{sampled}\t{sampled}\n", encoding="utf-8"
    )
    report = read_benchmark(benchmark)
    assert report["seconds"] == 0.5
    expected = None if sampled == "NA" else float(sampled)
    assert report["max_rss_mb"] == expected
    assert report["io_in_mb"] == expected
    assert report["io_out_mb"] == expected


@pytest.mark.parametrize("field", ["s", "max_rss", "io_in", "io_out"])
@pytest.mark.parametrize("invalid", ["nan", "inf", "-1", "", "unavailable"])
def test_benchmark_rejects_malformed_or_nonfinite_measurements(
    tmp_path: Path, field: str, invalid: str
) -> None:
    read_benchmark = runpy.run_path(
        str(source_root() / "scripts" / "audit_performance_diagnostics.py")
    )["read_benchmark"]
    benchmark = tmp_path / "benchmark.tsv"
    values = dict(s="0.5", max_rss="1", io_in="0", io_out="0")
    values[field] = invalid
    benchmark.write_text(
        "\t".join(values) + "\n" + "\t".join(values.values()) + "\n", encoding="utf-8"
    )
    with pytest.raises(ValueError):
        read_benchmark(benchmark)


def test_benchmark_requires_an_observed_duration(tmp_path: Path) -> None:
    read_benchmark = runpy.run_path(
        str(source_root() / "scripts" / "audit_performance_diagnostics.py")
    )["read_benchmark"]
    benchmark = tmp_path / "benchmark.tsv"
    benchmark.write_text("s\tmax_rss\tio_in\tio_out\nNA\tNA\tNA\tNA\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_benchmark(benchmark)
