#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from capstone.fastqio import iter_fastq, revcomp
except ImportError:  # pragma: no cover
    from fastqio import iter_fastq, revcomp


def canonical(km: str) -> str:
    rc = revcomp(km)
    return km if km <= rc else rc


def kmer_counts(in_fastq: Path, k: int) -> Counter[str]:
    c = Counter()
    for rec in iter_fastq(in_fastq):
        s = rec.seq.upper()
        # very small, strict filter to keep things deterministic and simple
        if "N" in s:
            # skip kmers spanning Ns
            pass
        for i in range(0, len(s) - k + 1):
            km = s[i : i + k]
            if "N" in km:
                continue
            # enforce A/C/G/T
            if not all(ch in "ACGT" for ch in km):
                continue
            c[canonical(km)] += 1
    return c


def signature_from_kmers(kmers: set[str], signature_size: int) -> list[int]:
    # Deterministic MinHash-like signature using SHA1 on each kmer.
    # We keep the smallest N hashed values.
    vals = []
    for km in kmers:
        h = hashlib.sha1(km.encode("utf-8")).digest()
        vals.append(int.from_bytes(h[:8], "big", signed=False))
    vals.sort()
    return vals[:signature_size]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-fastq", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--signature-size", type=int, required=True)
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    in_fastq = Path(args.in_fastq)
    out_json = Path(args.out_json)

    counts = kmer_counts(in_fastq, k=args.k)
    kmers = set(counts.keys())
    sig = signature_from_kmers(kmers, signature_size=args.signature_size)
    top = counts.most_common(args.top)

    payload = {
        "input": str(in_fastq),
        "k": args.k,
        "signature_size": args.signature_size,
        "unique_kmers": len(kmers),
        "total_kmers": int(sum(counts.values())),
        "signature": sig,
        "top_kmers": [{"kmer": k, "count": int(v)} for k, v in top],
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
