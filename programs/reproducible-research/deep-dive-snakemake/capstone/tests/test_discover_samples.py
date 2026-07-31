from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from capstone.discover_samples import discover_fastqs, read_arrival_registry


def write_fastq(path: Path, *, sequence: str = "ACGT", quality: str = "IIII") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"@read1\n{sequence}\n+\n{quality}\n", encoding="utf-8")


def test_discover_samples_writes_schema_version_and_sorted_samples(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    write_fastq(raw_dir / "sampleB.fastq.gz")
    write_fastq(raw_dir / "sampleA.fastq.gz")
    registry = tmp_path / "arrivals.tsv"
    registry.write_text("path\nsampleB.fastq.gz\nsampleA.fastq.gz\n", encoding="utf-8")

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
            "--arrival-registry",
            str(registry),
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
    assert payload["arrival_registry"] == str(registry)
    assert len(payload["arrival_registry_sha256"]) == 64


def test_registry_controls_scope_instead_of_ambient_directory_contents(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    write_fastq(raw_dir / "registered.fastq.gz")
    write_fastq(raw_dir / "ambient.fastq.gz")
    registry = tmp_path / "arrivals.tsv"
    registry.write_text("path\nregistered.fastq.gz\n", encoding="utf-8")

    arrivals = read_arrival_registry(registry)
    assert discover_fastqs(raw_dir, "*.fastq.gz", arrivals) == [raw_dir / "registered.fastq.gz"]


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("sample\nsampleA.fastq.gz\n", "header must be exactly"),
        ("path\n", "must list at least one"),
        ("path\n../outside.fastq.gz\n", "must stay inside"),
        ("path\nsampleA.fastq.gz\nsampleA.fastq.gz\n", "duplicate path"),
    ],
)
def test_registry_rejects_ambiguous_membership(tmp_path: Path, contents: str, message: str) -> None:
    registry = tmp_path / "arrivals.tsv"
    registry.write_text(contents, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        read_arrival_registry(registry)


def test_registered_arrival_must_exist_and_match_the_governed_pattern(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    with pytest.raises(ValueError, match="does not match glob"):
        discover_fastqs(raw_dir, "*.fastq.gz", [Path("sampleA.txt")])
    with pytest.raises(ValueError, match="does not exist"):
        discover_fastqs(raw_dir, "*.fastq.gz", [Path("sampleA.fastq.gz")])
