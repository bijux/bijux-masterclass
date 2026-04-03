#!/usr/bin/env python3
"""Write a compact summary of internal results surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_summary(results_dir: Path, summary_path: Path) -> dict[str, object]:
    published_summary = load_json(summary_path)
    sample_dirs = sorted(path for path in results_dir.iterdir() if path.is_dir())
    per_sample: dict[str, dict[str, object]] = {}

    for sample_dir in sample_dirs:
        sample = sample_dir.name
        files = {
            "qc_raw": sample_dir / "qc_raw.json",
            "trim": sample_dir / "trim.json",
            "qc_trimmed": sample_dir / "qc_trimmed.json",
            "dedup": sample_dir / "dedup.json",
            "kmer": sample_dir / "kmer.json",
            "screen": sample_dir / "screen.json",
        }
        status = {name: path.is_file() for name, path in files.items()}
        highlights = published_summary["units"].get(sample, {}).get("highlights", {})
        top_hit = published_summary["units"].get(sample, {}).get("screen", {}).get("top_hit", {})

        per_sample[sample] = {
            "available_surfaces": status,
            "reads": {
                "raw": highlights.get("reads_raw"),
                "trimmed": highlights.get("reads_trimmed"),
                "dedup": highlights.get("reads_dedup"),
            },
            "top_panel": top_hit.get("panel"),
            "top_panel_overlap": top_hit.get("signature_overlap"),
        }

    return {
        "results_dir": results_dir.resolve().as_posix(),
        "summary_path": summary_path.resolve().as_posix(),
        "sample_count": len(per_sample),
        "samples": per_sample,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(args.results_dir, args.summary_json)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
