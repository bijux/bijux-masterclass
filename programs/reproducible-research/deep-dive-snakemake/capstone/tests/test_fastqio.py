from __future__ import annotations

from pathlib import Path

from capstone.fastqio import FastqRecord, iter_fastq, phred_scores, revcomp, write_fastq


def test_fastq_roundtrip_gz(tmp_path: Path) -> None:
    p = tmp_path / "x.fastq.gz"
    recs = [
        FastqRecord("@r1", "ACGTN", "+", "IIIII"),
        FastqRecord("@r2", "TTTT", "+", "####"),
    ]
    write_fastq(p, iter(recs))
    out = list(iter_fastq(p))
    assert out == recs


def test_phred_scores() -> None:
    assert phred_scores('!"#') == [0, 1, 2]


def test_revcomp() -> None:
    assert revcomp("ACGTN") == "NACGT"
