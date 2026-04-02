from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_results_summary_reports_internal_surfaces_and_highlights(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    sample_dir = results_dir / "sampleA"
    for name in ["qc_raw", "trim", "qc_trimmed", "dedup", "kmer", "screen"]:
        write_json(sample_dir / f"{name}.json", {"schema_version": 2})

    summary_path = tmp_path / "summary.json"
    write_json(
        summary_path,
        {
            "schema_version": 2,
            "units": {
                "sampleA": {
                    "highlights": {
                        "reads_raw": 200,
                        "reads_trimmed": 180,
                        "reads_dedup": 12,
                    },
                    "screen": {"top_hit": {"panel": "panel-alpha", "signature_overlap": 0.75}},
                }
            },
        },
    )

    output = tmp_path / "results-summary.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "results_summary.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--results-dir",
            str(results_dir),
            "--summary-json",
            str(summary_path),
            "--out",
            str(output),
        ],
        check=True,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["sample_count"] == 1
    assert payload["samples"]["sampleA"]["available_surfaces"]["screen"] is True
    assert payload["samples"]["sampleA"]["reads"]["dedup"] == 12
    assert payload["samples"]["sampleA"]["top_panel"] == "panel-alpha"

