#!/usr/bin/env python3
"""Write a compact summary of the Snakemake publish boundary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_summary(publish_dir: Path) -> dict[str, object]:
    manifest = load_json(publish_dir / "manifest.json")
    discovered = load_json(publish_dir / "discovered_samples.json")
    summary = load_json(publish_dir / "summary.json")
    provenance = load_json(publish_dir / "provenance.json")

    units = summary["units"]
    samples = discovered["samples"]

    return {
        "publish_dir": publish_dir.resolve().as_posix(),
        "sample_count": len(samples),
        "samples": sorted(samples),
        "sample_modes": {
            sample: info["mode"]
            for sample, info in sorted(
                samples.items(),
                key=lambda item: item[0],
            )
        },
        "unit_count": len(units),
        "published_files": [entry["path"] for entry in manifest["files"]],
        "top_panels": {
            unit: {
                "panel": payload["screen"]["top_hit"].get("panel"),
                "signature_overlap": payload["screen"]["top_hit"].get("signature_overlap", 0.0),
            }
            for unit, payload in sorted(units.items(), key=lambda item: item[0])
        },
        "report_path": "report/index.html",
        "git_commit": provenance.get("git_commit"),
        "snakemake_version": provenance.get("snakemake_version"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(args.publish)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
