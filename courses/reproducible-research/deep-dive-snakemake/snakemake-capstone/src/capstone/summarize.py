#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--unit",
        action="append",
        required=True,
        help="Unit id (e.g., sample.SE or sample.R1). Order matters.",
    )
    ap.add_argument("--qc-raw", action="append", required=True)
    ap.add_argument("--trim-json", action="append", required=True)
    ap.add_argument("--qc-trimmed", action="append", required=True)
    ap.add_argument("--dedup-json", action="append", required=True)
    ap.add_argument("--kmer-json", action="append", required=True)
    ap.add_argument("--screen-json", action="append", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-tsv", required=True)
    args = ap.parse_args()

    n = len(args.unit)
    for key in ["qc_raw", "trim_json", "qc_trimmed", "dedup_json", "kmer_json", "screen_json"]:
        if len(getattr(args, key)) != n:
            raise SystemExit(
                f"inputs must align in length/order across --unit and --{key.replace('_', '-')}"
            )

    units: dict[str, dict] = {}
    for uid, p_raw, p_trim, p_qt, p_dd, p_km, p_sc in zip(
        args.unit,
        args.qc_raw,
        args.trim_json,
        args.qc_trimmed,
        args.dedup_json,
        args.kmer_json,
        args.screen_json,
        strict=False,
    ):
        raw = load(Path(p_raw))
        tr = load(Path(p_trim))
        qt = load(Path(p_qt))
        dd = load(Path(p_dd))
        km = load(Path(p_km))
        sc = load(Path(p_sc))

        top_panel = (
            sc["scores"][0] if sc.get("scores") else {"panel": None, "signature_overlap": 0.0}
        )

        units[uid] = {
            "raw_qc": raw,
            "trim": tr,
            "trimmed_qc": qt,
            "dedup": dd,
            "kmer": {
                "k": km["k"],
                "unique_kmers": km["unique_kmers"],
                "total_kmers": km["total_kmers"],
                "signature_size": km["signature_size"],
            },
            "screen": {"top_hit": top_panel, "scores": sc.get("scores", [])},
            "highlights": {
                "reads_raw": int(raw["reads"]),
                "reads_trimmed": int(qt["reads"]),
                "reads_dedup": int(dd["output"]["reads"]),
                "mean_q_raw": float(mean(list(map(float, raw["qual_mean_per_pos"])))),
                "mean_q_trimmed": float(mean(list(map(float, qt["qual_mean_per_pos"])))),
            },
        }

    payload = {"schema_version": 2, "units": dict(sorted(units.items(), key=lambda kv: kv[0]))}
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    header = [
        "unit",
        "reads_raw",
        "reads_trimmed",
        "reads_dedup",
        "gc_raw",
        "gc_trimmed",
        "mean_q_raw",
        "mean_q_trimmed",
        "top_panel",
        "top_panel_overlap",
        "unique_kmers",
    ]
    rows = ["\t".join(header)]
    for uid, d in payload["units"].items():
        h = d["highlights"]
        rows.append(
            "\t".join(
                [
                    uid,
                    str(h["reads_raw"]),
                    str(h["reads_trimmed"]),
                    str(h["reads_dedup"]),
                    f"{float(d['raw_qc']['gc_fraction']):.6f}",
                    f"{float(d['trimmed_qc']['gc_fraction']):.6f}",
                    f"{float(h['mean_q_raw']):.3f}",
                    f"{float(h['mean_q_trimmed']):.3f}",
                    str(d["screen"]["top_hit"].get("panel")),
                    f"{float(d['screen']['top_hit'].get('signature_overlap', 0.0)):.3f}",
                    str(int(d["kmer"]["unique_kmers"])),
                ]
            )
        )

    out_tsv = Path(args.out_tsv)
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    out_tsv.write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
