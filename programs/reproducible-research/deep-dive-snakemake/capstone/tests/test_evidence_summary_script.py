from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_evidence_summary_reports_logs_benchmarks_and_provenance(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    benchmarks_dir = tmp_path / "benchmarks"
    (logs_dir / "sampleA").mkdir(parents=True, exist_ok=True)
    benchmarks_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "sampleA" / "trim.log").write_text("ok\n", encoding="utf-8")
    (logs_dir / "report.log").write_text("done\n", encoding="utf-8")
    (benchmarks_dir / "trim_sampleA.txt").write_text(
        "s\th:m:s\tmax_rss\tmax_vms\tmax_uss\tmax_pss\tio_in\tio_out\tmean_load\tcpu_time\n"
        "0.10\t0:00:00\t0\t0\t0\t0\t0.00\t0.00\t0.00\t0\n",
        encoding="utf-8",
    )
    provenance = tmp_path / "provenance.json"
    manifest = tmp_path / "manifest.json"
    write_json(
        provenance,
        {
            "snakemake_version": "9.19.0",
            "python_executable": "/tmp/python",
            "git_commit": "abc123",
            "timestamp_utc": "2026-04-02T00:00:00Z",
        },
    )
    write_json(
        manifest,
        {
            "files": [
                {"path": "discovered_samples.json", "sha256": "a"},
                {"path": "summary.json", "sha256": "b"},
            ]
        },
    )

    output = tmp_path / "evidence-summary.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "evidence_summary.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--logs-dir",
            str(logs_dir),
            "--benchmarks-dir",
            str(benchmarks_dir),
            "--provenance",
            str(provenance),
            "--manifest",
            str(manifest),
            "--out",
            str(output),
        ],
        check=True,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["log_count"] == 2
    assert payload["benchmark_count"] == 1
    assert payload["benchmarks"]["trim_sampleA"]["seconds"] == 0.10
    assert payload["provenance_identity"]["snakemake_version"] == "9.19.0"
    assert payload["published_paths"] == ["discovered_samples.json", "summary.json"]
