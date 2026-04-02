from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_config_summary_reports_repository_and_materialized_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "use_discovered_samples: true\nsamples:\n  sampleA: data/raw/sampleA.fastq.gz\n",
        encoding="utf-8",
    )
    provenance_path = tmp_path / "provenance.json"
    write_json(
        provenance_path,
        {
            "config": {
                "results_dir": "results",
                "publish_dir": "publish",
                "logs_dir": "logs",
                "benchmarks_dir": "benchmarks",
                "use_discovered_samples": True,
                "params": {
                    "raw_dir": "data/raw",
                    "raw_glob": "*.fastq.gz",
                    "allow_paired_end": False,
                    "dedup": {"mode": "dedup"},
                    "kmer": {"k": 21, "signature_size": 1000, "top": 25},
                    "trim": {"q": 20, "min_len": 20, "max_n_fraction": 0.05},
                    "panel": {"fasta": "data/panel/panel.fasta"},
                    "publish": {"version": "v1"},
                },
            },
            "snakemake_version": "9.19.0",
            "python_executable": "/tmp/python",
            "git_commit": "abc123",
        },
    )

    output = tmp_path / "config-summary.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "config_summary.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--config",
            str(config_path),
            "--provenance",
            str(provenance_path),
            "--out",
            str(output),
        ],
        check=True,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["repository_config_keys"] == ["samples", "use_discovered_samples"]
    assert payload["repository_sample_keys"] == ["sampleA"]
    assert payload["discovery_mode"] == "checkpoint"
    assert payload["materialized_directories"]["publish_dir"] == "publish"
    assert payload["materialized_params"]["publish_version"] == "v1"
    assert payload["provenance_identity"]["snakemake_version"] == "9.19.0"

