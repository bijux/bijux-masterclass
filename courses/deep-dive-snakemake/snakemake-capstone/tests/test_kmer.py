from __future__ import annotations

from pathlib import Path

from capstone.fastqio import FastqRecord, write_fastq
from capstone.kmer_profile import kmer_counts


def test_kmer_counts_canonical(tmp_path: Path) -> None:
    p = tmp_path / "in.fastq.gz"
    recs = [FastqRecord("@r1", "ACGTACGT", "+", "IIIIIIII")]
    write_fastq(p, iter(recs))
    c = kmer_counts(p, k=3)
    # "ACG" and "CGT" etc (canonical includes revcomp merges)
    assert sum(c.values()) == len("ACGTACGT") - 3 + 1
    assert any(k in c for k in ["ACG", "CGT", "GTA", "TAC"])
