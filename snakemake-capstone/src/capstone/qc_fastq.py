#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from capstone.fastqio import iter_fastq, phred_scores
except ImportError:  # pragma: no cover
    from fastqio import iter_fastq, phred_scores


def summarize_fastq(path: Path, max_reads: int | None = None) -> dict:
    reads = 0
    bases = 0
    gc = 0
    ns = 0

    qual_sum: list[int] = []
    qual_n: list[int] = []
    len_hist = Counter()

    for rec in iter_fastq(path):
        reads += 1
        L = len(rec.seq)
        bases += L
        len_hist[L] += 1

        seq_u = rec.seq.upper()
        gc += seq_u.count("G") + seq_u.count("C")
        ns += seq_u.count("N")

        qs = phred_scores(rec.qual)
        # extend arrays if needed
        if len(qual_sum) < L:
            qual_sum.extend([0] * (L - len(qual_sum)))
            qual_n.extend([0] * (L - len(qual_n)))
        for i, q in enumerate(qs):
            qual_sum[i] += q
            qual_n[i] += 1

        if max_reads is not None and reads >= max_reads:
            break

    qual_mean = [(qual_sum[i] / qual_n[i]) if qual_n[i] else 0.0 for i in range(len(qual_sum))]
    payload = {
        "path": str(path),
        "reads": reads,
        "bases": bases,
        "mean_read_length": (bases / reads) if reads else 0.0,
        "gc_fraction": (gc / bases) if bases else 0.0,
        "n_fraction": (ns / bases) if bases else 0.0,
        "qual_mean_per_pos": qual_mean,
        "length_hist": dict(sorted(len_hist.items(), key=lambda kv: int(kv[0]))),
    }
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-fastq", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-tsv", required=True)
    ap.add_argument("--max-reads", type=int, default=0, help="0 = no limit")
    args = ap.parse_args()

    in_path = Path(args.in_fastq)
    out_json = Path(args.out_json)
    out_tsv = Path(args.out_tsv)
    max_reads = None if args.max_reads == 0 else args.max_reads

    payload = summarize_fastq(in_path, max_reads=max_reads)

    out_json.parent.mkdir(parents=True, exist_ok=True)

    # Atomic write for JSON
    tmp_json = out_json.with_suffix(".tmp.json")
    tmp_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp_json.replace(out_json)

    # TSV (small, single write – low risk)
    rows = [
        "metric\tvalue",
        f"reads\t{payload['reads']}",
        f"bases\t{payload['bases']}",
        f"mean_read_length\t{payload['mean_read_length']:.6f}",
        f"gc_fraction\t{payload['gc_fraction']:.6f}",
        f"n_fraction\t{payload['n_fraction']:.6f}",
        f"qual_positions\t{len(payload['qual_mean_per_pos'])}",
    ]

    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    out_tsv.write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
