from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_publish_dir(tmp_path: Path) -> Path:
    publish_dir = tmp_path / "publish" / "v1"
    write_json(
        publish_dir / "manifest.json",
        {
            "schema_version": 2,
            "base": publish_dir.as_posix(),
            "files": [
                {"path": "discovered_samples.json", "sha256": "a"},
                {"path": "provenance.json", "sha256": "b"},
                {"path": "report/index.html", "sha256": "c"},
                {"path": "summary.json", "sha256": "d"},
                {"path": "summary.tsv", "sha256": "e"},
            ],
        },
    )
    write_json(
        publish_dir / "discovered_samples.json",
        {
            "schema_version": 2,
            "allow_paired_end": False,
            "glob": "*.fastq.gz",
            "n_files": 1,
            "raw_dir": "data/raw",
            "samples": {
                "sampleA": {"mode": "SE", "reads": {"SE": "data/raw/sampleA.fastq.gz"}},
            },
        },
    )
    write_json(
        publish_dir / "summary.json",
        {
            "schema_version": 2,
            "units": {
                "sampleA": {
                    "highlights": {"reads_raw": 10},
                    "screen": {"top_hit": {"panel": "panelA", "signature_overlap": 1.0}},
                }
            },
        },
    )
    write_json(
        publish_dir / "provenance.json",
        {
            "schema_version": 2,
            "timestamp_utc": "2026-04-02T00:00:00Z",
            "config": {"publish_dir": "publish"},
            "snakemake_version": "9.19.0",
        },
    )
    (publish_dir / "summary.tsv").write_text("unit\treads_raw\nsampleA\t10\n", encoding="utf-8")
    report_dir = publish_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "index.html").write_text("<html><body>ok</body></html>\n", encoding="utf-8")
    return publish_dir


def test_verify_publish_accepts_aligned_publish_surfaces(tmp_path: Path) -> None:
    publish_dir = build_publish_dir(tmp_path)
    report = tmp_path / "verify.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "verify_publish.py"

    subprocess.run(
        [sys.executable, str(script), "--publish", str(publish_dir), "--report", str(report)],
        check=True,
    )

    payload = json.loads(report.read_text(encoding="utf-8"))
    checks = {entry["check"]: entry for entry in payload["checks"]}
    assert checks["manifest"]["paths"] == [
        "discovered_samples.json",
        "provenance.json",
        "report/index.html",
        "summary.json",
        "summary.tsv",
    ]
    assert checks["summary"]["units_match_discovery"] is True
    assert checks["provenance"]["snakemake_version"] == "9.19.0"


def test_verify_publish_rejects_summary_and_discovery_mismatch(tmp_path: Path) -> None:
    publish_dir = build_publish_dir(tmp_path)
    write_json(
        publish_dir / "summary.json",
        {
            "schema_version": 2,
            "units": {
                "sampleB": {
                    "highlights": {"reads_raw": 10},
                    "screen": {"top_hit": {"panel": "panelB", "signature_overlap": 1.0}},
                }
            },
        },
    )
    script = Path(__file__).resolve().parents[1] / "scripts" / "verify_publish.py"

    result = subprocess.run(
        [sys.executable, str(script), "--publish", str(publish_dir)],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "units must match discovered_samples.json" in result.stderr
