from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def write_fastq(path: Path, *, sequence: str = "ACGT", quality: str = "IIII") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"@read1\n{sequence}\n+\n{quality}\n", encoding="utf-8")


def test_discover_samples_writes_schema_version_and_sorted_samples(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    write_fastq(raw_dir / "sampleB.fastq.gz")
    write_fastq(raw_dir / "sampleA.fastq.gz")

    output = tmp_path / "discovered_samples.json"
    script = Path(__file__).resolve().parents[1] / "src" / "capstone" / "discover_samples.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--raw-dir",
            str(raw_dir),
            "--glob",
            "*.fastq.gz",
            "--out-json",
            str(output),
        ],
        check=True,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 2
    assert payload["n_files"] == 2
    assert list(payload["samples"]) == ["sampleA", "sampleB"]
    assert payload["samples"]["sampleA"]["mode"] == "SE"
