#!/usr/bin/env python3
"""Write a compact summary of executed workflow evidence."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_benchmark(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        row = next(reader, None)
    if row is None:
        return {"path": path.as_posix(), "has_measurements": False}
    return {
        "path": path.as_posix(),
        "has_measurements": True,
        "seconds": float(row["s"]),
        "max_rss": row["max_rss"],
        "io_in": row["io_in"],
        "io_out": row["io_out"],
    }


def build_summary(
    logs_dir: Path,
    benchmarks_dir: Path,
    provenance_path: Path,
    manifest_path: Path,
) -> dict[str, object]:
    log_paths = sorted(path.relative_to(logs_dir).as_posix() for path in logs_dir.rglob("*.log"))
    benchmark_paths = sorted(path for path in benchmarks_dir.rglob("*.txt"))
    provenance = load_json(provenance_path)
    manifest = load_json(manifest_path)

    benchmark_summary = {path.stem: parse_benchmark(path) for path in benchmark_paths}

    return {
        "logs_dir": logs_dir.resolve().as_posix(),
        "benchmarks_dir": benchmarks_dir.resolve().as_posix(),
        "log_count": len(log_paths),
        "logs": log_paths,
        "benchmark_count": len(benchmark_paths),
        "benchmarks": benchmark_summary,
        "provenance_identity": {
            "snakemake_version": provenance["snakemake_version"],
            "python_executable": provenance["python_executable"],
            "git_commit": provenance["git_commit"],
            "timestamp_utc": provenance["timestamp_utc"],
        },
        "published_paths": [entry["path"] for entry in manifest["files"]],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs-dir", type=Path, required=True)
    parser.add_argument("--benchmarks-dir", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(
        args.logs_dir,
        args.benchmarks_dir,
        args.provenance,
        args.manifest,
    )
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
