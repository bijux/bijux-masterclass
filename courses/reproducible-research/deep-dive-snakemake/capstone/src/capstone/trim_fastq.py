#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

try:
    from capstone.fastqio import FastqRecord, iter_fastq, phred_scores, write_fastq
except ImportError:  # pragma: no cover
    from fastqio import FastqRecord, iter_fastq, phred_scores, write_fastq


def trim_3prime(rec: FastqRecord, qmin: int) -> FastqRecord:
    qs = phred_scores(rec.qual)
    cut = len(qs)
    # Trim from 3' until base qualities are >= qmin.
    while cut > 0 and qs[cut - 1] < qmin:
        cut -= 1
    if cut == len(qs):
        return rec
    return FastqRecord(header=rec.header, seq=rec.seq[:cut], plus=rec.plus, qual=rec.qual[:cut])


def _parse_fasta_sequences(path: Path) -> list[str]:
    seqs: list[str] = []
    buf: list[str] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith(">"):
            if buf:
                seqs.append("".join(buf).upper())
                buf = []
            continue
        buf.append(ln)
    if buf:
        seqs.append("".join(buf).upper())
    return [s for s in seqs if s]


def trim_adapters_naive_3prime(
    rec: FastqRecord, adapters: list[str], min_overlap: int
) -> tuple[FastqRecord, bool]:
    """Naive adapter clipping (educational).

    - looks for an exact match of the first `min_overlap` bases of any adapter
    - trims at the earliest hit position
    """
    if not adapters or min_overlap <= 0:
        return rec, False

    s = rec.seq.upper()
    best: int | None = None
    for a in adapters:
        if len(a) < min_overlap:
            continue
        seed = a[:min_overlap]
        pos = s.find(seed)
        if pos != -1:
            best = pos if best is None else min(best, pos)

    if best is None:
        return rec, False

    if best <= 0:
        return FastqRecord(header=rec.header, seq="", plus=rec.plus, qual=""), True
    return FastqRecord(
        header=rec.header, seq=rec.seq[:best], plus=rec.plus, qual=rec.qual[:best]
    ), True


def trim_poly_run_3prime(rec: FastqRecord, min_run: int) -> tuple[FastqRecord, bool]:
    if min_run <= 0 or not rec.seq:
        return rec, False
    s = rec.seq.upper()
    last = s[-1]
    if last not in {"A", "T"}:
        return rec, False

    cut = len(s)
    i = cut - 1
    while i >= 0 and s[i] == last:
        i -= 1
    run_len = cut - (i + 1)
    if run_len < min_run:
        return rec, False

    new_cut = i + 1
    return FastqRecord(
        header=rec.header, seq=rec.seq[:new_cut], plus=rec.plus, qual=rec.qual[:new_cut]
    ), True


@dataclass
class TrimStats:
    reads_in: int = 0
    bases_in: int = 0
    reads_out: int = 0
    bases_out: int = 0

    reads_quality_clipped: int = 0
    bases_quality_clipped: int = 0

    reads_adapter_clipped: int = 0
    bases_adapter_clipped: int = 0

    reads_poly_clipped: int = 0
    bases_poly_clipped: int = 0

    reads_clipped_any: int = 0


def pipeline(
    in_fastq: Path,
    qmin: int,
    min_len: int,
    max_n_fraction: float,
    adapters_fasta: Path | None = None,
    adapter_min_overlap: int = 12,
    poly_run_min: int = 0,
) -> tuple[TrimStats, Iterator[FastqRecord]]:
    """Streaming trimming pipeline.

    Returns a mutable stats object updated while the iterator is consumed.
    """
    stats = TrimStats()

    adapters: list[str] = []
    if adapters_fasta is not None and adapters_fasta.exists():
        adapters = _parse_fasta_sequences(adapters_fasta)

    def _iter() -> Iterator[FastqRecord]:
        for rec in iter_fastq(in_fastq):
            stats.reads_in += 1
            stats.bases_in += len(rec.seq)

            clipped_any = False

            before = len(rec.seq)
            r = trim_3prime(rec, qmin=qmin)
            after = len(r.seq)
            if after < before:
                clipped_any = True
                stats.reads_quality_clipped += 1
                stats.bases_quality_clipped += before - after

            before = len(r.seq)
            r, clipped = trim_adapters_naive_3prime(
                r, adapters=adapters, min_overlap=adapter_min_overlap
            )
            after = len(r.seq)
            if clipped and after < before:
                clipped_any = True
                stats.reads_adapter_clipped += 1
                stats.bases_adapter_clipped += before - after

            before = len(r.seq)
            r, poly = trim_poly_run_3prime(r, min_run=poly_run_min)
            after = len(r.seq)
            if poly and after < before:
                clipped_any = True
                stats.reads_poly_clipped += 1
                stats.bases_poly_clipped += before - after

            if clipped_any:
                stats.reads_clipped_any += 1

            if len(r.seq) < min_len:
                continue

            if max_n_fraction > 0.0 and len(r.seq) > 0:
                n = r.seq.upper().count("N")
                if (n / len(r.seq)) > max_n_fraction:
                    continue

            stats.reads_out += 1
            stats.bases_out += len(r.seq)
            yield r

    return stats, _iter()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-fastq", required=True)
    ap.add_argument("--out-fastq", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--min-len", type=int, required=True)
    ap.add_argument("--max-n-fraction", type=float, default=0.0)
    ap.add_argument("--adapters-fasta", default=None)
    ap.add_argument("--adapter-min-overlap", type=int, default=12)
    ap.add_argument("--poly-run-min", type=int, default=0)
    args = ap.parse_args()

    in_fastq = Path(args.in_fastq)
    out_fastq = Path(args.out_fastq)
    out_json = Path(args.out_json)
    adapters_fasta = Path(args.adapters_fasta) if args.adapters_fasta else None

    stats, it = pipeline(
        in_fastq=in_fastq,
        qmin=args.q,
        min_len=args.min_len,
        max_n_fraction=args.max_n_fraction,
        adapters_fasta=adapters_fasta,
        adapter_min_overlap=args.adapter_min_overlap,
        poly_run_min=args.poly_run_min,
    )

    write_fastq(out_fastq, it)

    payload = {
        "schema_version": 2,
        "input": {"path": str(in_fastq), "reads": stats.reads_in, "bases": stats.bases_in},
        "output": {"path": str(out_fastq), "reads": stats.reads_out, "bases": stats.bases_out},
        "params": {
            "q": args.q,
            "min_len": args.min_len,
            "max_n_fraction": args.max_n_fraction,
            "adapters_fasta": str(adapters_fasta) if adapters_fasta else None,
            "adapter_min_overlap": args.adapter_min_overlap,
            "poly_run_min": args.poly_run_min,
        },
        "clipping": {
            "reads_any": stats.reads_clipped_any,
            "quality": {"reads": stats.reads_quality_clipped, "bases": stats.bases_quality_clipped},
            "adapter": {"reads": stats.reads_adapter_clipped, "bases": stats.bases_adapter_clipped},
            "poly": {"reads": stats.reads_poly_clipped, "bases": stats.bases_poly_clipped},
        },
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
