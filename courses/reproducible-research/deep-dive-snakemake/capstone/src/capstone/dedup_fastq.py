#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections.abc import Iterator
from dataclasses import dataclass
from hashlib import blake2b
from pathlib import Path

try:
    from capstone.fastqio import FastqRecord, iter_fastq, write_fastq
except ImportError:  # pragma: no cover
    from fastqio import FastqRecord, iter_fastq, write_fastq


@dataclass
class DedupStats:
    reads_in: int = 0
    bases_in: int = 0
    reads_out: int = 0
    bases_out: int = 0
    duplicates_dropped: int = 0


def pipeline_dedup(in_fastq: Path) -> tuple[DedupStats, Iterator[FastqRecord]]:
    """Streaming exact deduplication.
    Hashes *sequence only* (quality is ignored) and keeps the first occurrence.
    Deterministic, but memory-heavy for large inputs.
    """
    seen: set[bytes] = set()
    stats = DedupStats()

    def _iter() -> Iterator[FastqRecord]:
        for rec in iter_fastq(in_fastq):
            stats.reads_in += 1
            stats.bases_in += len(rec.seq)
            h = blake2b(rec.seq.encode("utf-8"), digest_size=16).digest()
            if h in seen:
                stats.duplicates_dropped += 1
                continue
            seen.add(h)
            stats.reads_out += 1
            stats.bases_out += len(rec.seq)
            yield rec

    return stats, _iter()


def pipeline_copy(in_fastq: Path) -> tuple[DedupStats, Iterator[FastqRecord]]:
    """Copy-through pipeline that still emits correct stats."""
    stats = DedupStats()

    def _iter() -> Iterator[FastqRecord]:
        for rec in iter_fastq(in_fastq):
            stats.reads_in += 1
            stats.bases_in += len(rec.seq)
            stats.reads_out += 1
            stats.bases_out += len(rec.seq)
            yield rec

    return stats, _iter()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["dedup", "copy"], required=True)
    ap.add_argument("--in-fastq", required=True)
    ap.add_argument("--out-fastq", required=True)
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    in_fastq = Path(args.in_fastq)
    out_fastq = Path(args.out_fastq)
    out_json = Path(args.out_json)

    if args.mode == "dedup":
        stats, it = pipeline_dedup(in_fastq)
    else:
        stats, it = pipeline_copy(in_fastq)

    write_fastq(out_fastq, it)

    payload = {
        "schema_version": 2,
        "input": {"path": str(in_fastq), "reads": stats.reads_in, "bases": stats.bases_in},
        "output": {"path": str(out_fastq), "reads": stats.reads_out, "bases": stats.bases_out},
        "duplicates_dropped": stats.duplicates_dropped,
        "mode": args.mode,
        "dedup_key": "sequence" if args.mode == "dedup" else None,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)

    # Atomic write: temporary file followed by rename
    tmp_json = out_json.with_suffix(".tmp.json")
    tmp_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp_json.replace(out_json)


if __name__ == "__main__":
    main()
