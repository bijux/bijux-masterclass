# tests/test_workflow_integration.py
"""
Integration tests for the full Snakemake workflow.

These tests are marked with @pytest.mark.integration (see pytest.ini) and are intended
to be run only when explicitly requested (e.g., `pytest -m integration`), as they
execute the real workflow on the small test dataset.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.integration
def test_snakemake_lint() -> None:
    """Ensure `snakemake --lint` reports no issues."""
    if shutil.which("snakemake") is None:
        pytest.skip("snakemake not installed")
    repo_root = Path(__file__).parents[1]
    result = subprocess.run(
        ["snakemake", "--lint"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
    assert result.returncode == 0, "Snakemake lint failed"


@pytest.mark.integration
def test_full_workflow_execution(tmp_path: Path) -> None:
    """
    Run the complete workflow in isolated directories and verify key outputs.
    This confirms end-to-end correctness, including rule execution order,
    script invocation, and published artifact creation.
    """
    repo_root = Path(__file__).parents[1]

    if shutil.which("snakemake") is None:
        pytest.skip("snakemake not installed")

    results_dir = tmp_path / "results"
    publish_dir = tmp_path / "publish"
    logs_dir = tmp_path / "logs"
    benchmarks_dir = tmp_path / "benchmarks"

    cmd = [
        "snakemake",
        "--cores",
        "1",  # single core for reproducibility in test
        "--config",
        f"results_dir={results_dir}",
        f"publish_dir={publish_dir}",
        f"logs_dir={logs_dir}",
        f"benchmarks_dir={benchmarks_dir}",
    ]

    result = subprocess.run(
        cmd,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

    assert result.returncode == 0, "Workflow execution failed"

    version_dir = publish_dir / "v1"

    # Verify key published artifacts exist
    manifest_path = version_dir / "manifest.json"
    assert manifest_path.exists(), "Manifest not created"

    summary_path = version_dir / "summary.json"
    assert summary_path.exists(), "Summary JSON not created"

    report_path = version_dir / "report" / "index.html"
    assert report_path.exists(), "HTML report not created"

    provenance_path = version_dir / "provenance.json"
    assert provenance_path.exists(), "Provenance not created"

    # Basic sanity check on manifest content
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 2
    assert len(manifest["files"]) >= 4  # summary, tsv, report/index.html, provenance
