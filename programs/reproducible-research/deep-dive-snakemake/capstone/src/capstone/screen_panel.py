#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from capstone.fastqio import revcomp
except ImportError:  # pragma: no cover
    from fastqio import revcomp


def canonical(km: str) -> str:
    rc = revcomp(km)
    return km if km <= rc else rc


def parse_fasta(path: Path) -> list[tuple[str, str]]:
    records = []
    name = None
    seq = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith(">"):
            if name is not None:
                records.append((name, "".join(seq)))
            name = ln[1:].strip()
            seq = []
        else:
            seq.append(ln)
    if name is not None:
        records.append((name, "".join(seq)))
    return records


def kmers_from_seq(seq: str, k: int) -> set[str]:
    s = seq.upper()
    out: set[str] = set()
    for i in range(0, len(s) - k + 1):
        km = s[i : i + k]
        if "N" in km:
            continue
        if not all(ch in "ACGT" for ch in km):
            continue
        out.add(canonical(km))
    return out


def signature_from_kmers(kmers: set[str], signature_size: int) -> list[int]:
    vals = []
    for km in kmers:
        h = hashlib.sha1(km.encode("utf-8")).digest()
        vals.append(int.from_bytes(h[:8], "big", signed=False))
    vals.sort()
    return vals[:signature_size]


def signature_overlap_coefficient(sig_a: list[int], sig_b: list[int]) -> float:
    """Overlap coefficient on hashed-signature sets.

    This is *not* the classic MinHash Jaccard estimator. We intentionally use a
    simpler overlap coefficient (|A∩B| / min(|A|,|B|)) on the *signature sets*
    to keep behavior deterministic and easy to explain.
    """
    a = set(sig_a)
    b = set(sig_b)
    if not a or not b:
        return 0.0
    inter = len(a & b)
    denom = min(len(a), len(b))
    return inter / denom if denom else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-kmer-json", required=True)
    ap.add_argument("--panel-fasta", required=True)
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    sample_json = Path(args.sample_kmer_json)
    panel_fasta = Path(args.panel_fasta)
    out_json = Path(args.out_json)

    sample = json.loads(sample_json.read_text(encoding="utf-8"))
    k = int(sample["k"])
    sig_size = int(sample["signature_size"])
    sample_sig = list(map(int, sample["signature"]))

    panel_records = parse_fasta(panel_fasta)
    panel = []
    for name, seq in panel_records:
        km = kmers_from_seq(seq, k=k)
        sig = signature_from_kmers(km, signature_size=sig_size)
        panel.append({"name": name, "signature": sig, "unique_kmers": len(km)})

    scores = []
    for p in panel:
        sim = signature_overlap_coefficient(sample_sig, p["signature"])
        scores.append(
            {
                "panel": p["name"],
                "signature_overlap": float(sim),
                "panel_unique_kmers": int(p["unique_kmers"]),
            }
        )

    scores.sort(key=lambda d: (-d["signature_overlap"], d["panel"]))

    payload = {
        "sample_kmer_json": str(sample_json),
        "panel_fasta": str(panel_fasta),
        "k": k,
        "signature_size": sig_size,
        "score_type": "signature_overlap_coefficient",
        "scores": scores,
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
