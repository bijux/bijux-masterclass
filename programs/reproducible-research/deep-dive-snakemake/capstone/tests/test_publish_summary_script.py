from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_publish_summary_script_writes_compact_publish_summary(tmp_path: Path) -> None:
    publish_dir = tmp_path / "publish" / "v1"
    write_json(
        publish_dir / "manifest.json",
        {
            "schema_version": 2,
            "files": [
                {"path": "discovered_samples.json", "sha256": "a"},
                {"path": "summary.json", "sha256": "b"},
                {"path": "summary.tsv", "sha256": "c"},
                {"path": "report/index.html", "sha256": "d"},
                {"path": "provenance.json", "sha256": "e"},
            ],
        },
    )
    write_json(
        publish_dir / "discovered_samples.json",
        {
            "schema_version": 2,
            "samples": {
                "sampleA": {"mode": "SE", "reads": {"SE": "data/raw/sampleA.fastq.gz"}},
                "sampleB": {"mode": "SE", "reads": {"SE": "data/raw/sampleB.fastq.gz"}},
            },
        },
    )
    write_json(
        publish_dir / "summary.json",
        {
            "schema_version": 2,
            "units": {
                "sampleA": {
                    "screen": {"top_hit": {"panel": "panel-alpha", "signature_overlap": 0.8}}
                },
                "sampleB": {
                    "screen": {"top_hit": {"panel": "panel-beta", "signature_overlap": 0.6}}
                },
            },
        },
    )
    write_json(
        publish_dir / "provenance.json",
        {
            "schema_version": 2,
            "git_commit": "abc123",
            "snakemake_version": "9.14.0",
        },
    )
    (publish_dir / "summary.tsv").write_text("unit\treads_raw\nsampleA\t10\n", encoding="utf-8")
    report_dir = publish_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "index.html").write_text("<html></html>\n", encoding="utf-8")

    output = tmp_path / "publish-summary.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "publish_summary.py"
    subprocess.run(
        [sys.executable, str(script), "--publish", str(publish_dir), "--out", str(output)],
        check=True,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["sample_count"] == 2
    assert payload["samples"] == ["sampleA", "sampleB"]
    assert payload["sample_modes"] == {"sampleA": "SE", "sampleB": "SE"}
    assert payload["unit_count"] == 2
    assert payload["published_files"] == [
        "discovered_samples.json",
        "summary.json",
        "summary.tsv",
        "report/index.html",
        "provenance.json",
    ]
    assert payload["top_panels"]["sampleA"]["panel"] == "panel-alpha"
    assert payload["report_path"] == "report/index.html"
    assert payload["git_commit"] == "abc123"
