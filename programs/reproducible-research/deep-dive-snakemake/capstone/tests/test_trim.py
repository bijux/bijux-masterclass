from __future__ import annotations

from pathlib import Path

from capstone.fastqio import FastqRecord, write_fastq
from capstone.trim_fastq import trim_3prime


def test_trim_3prime() -> None:
    # "!"=0, "I"=40
    r = FastqRecord("@r", "ACGT", "+", "III!")
    t = trim_3prime(r, qmin=20)
    assert t.seq == "ACG"
    assert t.qual == "III"


def test_trim_filters_min_len(tmp_path: Path) -> None:
    from capstone.trim_fastq import pipeline

    p = tmp_path / "in.fastq.gz"
    recs = [
        FastqRecord("@r1", "AAAAA", "+", "!!!!!"),  # will trim to 0
        FastqRecord("@r2", "ACGTACGT", "+", "IIIIIIII"),
    ]
    write_fastq(p, iter(recs))
    stats, it = pipeline(p, qmin=20, min_len=4, max_n_fraction=1.0)
    out = list(it)
    assert stats.reads_in == 2
    assert stats.reads_out == 1
    assert out[0].seq == "ACGTACGT"
