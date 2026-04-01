# tests/test_dedup_fastq.py
"""Additional unit tests for dedup_fastq.py (expanding coverage)."""

from __future__ import annotations

from pathlib import Path

from capstone.dedup_fastq import pipeline_copy, pipeline_dedup
from capstone.fastqio import FastqRecord, write_fastq


def test_dedup_exact_duplicates(tmp_path: Path) -> None:
    """Test exact sequence deduplication (keeps first occurrence)."""
    in_path = tmp_path / "input.fastq.gz"

    records = [
        FastqRecord("@read1", "ACGTACGT", "+", "IIIIIIII"),
        FastqRecord("@read2", "ACGTACGT", "+", "IIIIIIII"),  # duplicate seq
        FastqRecord("@read3", "TTTTTTTT", "+", "HHHHHHHH"),
        FastqRecord("@read4", "ACGTACGT", "+", "IIIIIIII"),  # another duplicate
    ]

    write_fastq(in_path, records)

    stats, iterator = pipeline_dedup(in_path)
    output_records = list(iterator)

    assert stats.reads_in == 4
    assert stats.reads_out == 2
    assert stats.duplicates_dropped == 2

    assert len(output_records) == 2
    assert output_records[0].seq == "ACGTACGT"
    assert output_records[1].seq == "TTTTTTTT"


def test_copy_mode_passthrough(tmp_path: Path) -> None:
    """Test copy mode preserves all records and reports correct stats."""
    in_path = tmp_path / "input.fastq.gz"

    records = [
        FastqRecord("@read1", "ACGT", "+", "IIII"),
        FastqRecord("@read2", "ACGT", "+", "IIII"),
    ]

    write_fastq(in_path, records)

    stats, iterator = pipeline_copy(in_path)
    output_records = list(iterator)

    assert stats.reads_in == 2
    assert stats.reads_out == 2
    assert stats.duplicates_dropped == 0

    assert output_records == records
