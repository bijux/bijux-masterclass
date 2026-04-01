#!/usr/bin/env python3
from __future__ import annotations

import gzip
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FastqRecord:
    """A single FASTQ record."""

    header: str  # includes leading '@'
    seq: str
    plus: str  # includes leading '+', may optionally repeat header
    qual: str


def _opener(path: Path):
    """Return appropriate open function and mode based on file extension."""
    if str(path).endswith(".gz"):
        return gzip.open, "rt"
    return open, "r"


def iter_fastq(path: Path) -> Iterator[FastqRecord]:
    """
    Iterate over FASTQ records in a file (supports .gz transparently).
    Performs basic validation (header starts with '@', plus line starts with '+',
    sequence and quality strings have equal length).
    """
    opener, mode = _opener(path)
    with opener(path, mode) as handle:  # type: ignore[arg-type]
        while True:
            header = handle.readline().rstrip("\n")
            if not header:
                break  # EOF
            if not header.startswith("@"):
                raise ValueError(f"FASTQ header must start with '@': {header!r}")

            seq = handle.readline().rstrip("\n")
            plus = handle.readline().rstrip("\n")
            qual = handle.readline().rstrip("\n")

            if not plus.startswith("+"):
                raise ValueError(f"Separator line must start with '+': {plus!r}")
            if len(seq) != len(qual):
                raise ValueError(
                    f"Sequence and quality length mismatch in record {header}: "
                    f"{len(seq)} vs {len(qual)}"
                )

            yield FastqRecord(header=header, seq=seq, plus=plus, qual=qual)


def write_fastq(path: Path, records: Iterator[FastqRecord]) -> None:
    """
    Write FASTQ records to a file (supports .gz transparently).
    Preserves exact content of input records.
    """
    opener, mode = _opener(path)
    mode = mode.replace("r", "w")  # switch to write mode
    with opener(path, mode) as handle:  # type: ignore[arg-type]
        for rec in records:
            handle.write(f"{rec.header}\n")
            handle.write(f"{rec.seq}\n")
            handle.write(f"{rec.plus}\n")
            handle.write(f"{rec.qual}\n")


def phred_scores(qual: str) -> list[int]:
    """Convert Phred quality string to list of integer scores (Phred+33 encoding)."""
    return [ord(c) - 33 for c in qual]


_COMPLEMENT = str.maketrans("ACGTacgtNn", "TGCAtgcaNn")


def revcomp(seq: str) -> str:
    """Return reverse complement of a sequence (case-insensitive, N unchanged)."""
    return seq.translate(_COMPLEMENT)[::-1]
