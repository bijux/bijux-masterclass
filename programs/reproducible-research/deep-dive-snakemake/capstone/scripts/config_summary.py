#!/usr/bin/env python3
"""Write a compact summary of the effective workflow configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_scalar(text: str) -> object:
    value = text.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def load_repository_config(path: Path) -> dict[str, object]:
    root: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, root)]

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        key, _, remainder = stripped.partition(":")
        if not _:
            raise ValueError(f"invalid config line: {raw_line!r}")

        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]

        value_text = remainder.strip()
        if value_text:
            current[key] = parse_scalar(value_text)
            continue

        child: dict[str, object] = {}
        current[key] = child
        stack.append((indent, child))

    return root


def build_summary(config_path: Path, provenance_path: Path) -> dict[str, object]:
    repository_config = load_repository_config(config_path)
    provenance = load_json(provenance_path)
    materialized = provenance["config"]
    params = materialized["params"]
    repository_samples = sorted((repository_config.get("samples") or {}).keys())

    return {
        "repository_config_path": config_path.resolve().as_posix(),
        "provenance_path": provenance_path.resolve().as_posix(),
        "repository_config_keys": sorted(repository_config),
        "repository_sample_keys": repository_samples,
        "discovery_mode": "checkpoint" if materialized["use_discovered_samples"] else "manual",
        "materialized_directories": {
            "results_dir": materialized["results_dir"],
            "publish_dir": materialized["publish_dir"],
            "logs_dir": materialized["logs_dir"],
            "benchmarks_dir": materialized["benchmarks_dir"],
        },
        "materialized_params": {
            "raw_dir": params["raw_dir"],
            "raw_glob": params["raw_glob"],
            "allow_paired_end": params["allow_paired_end"],
            "dedup_mode": params["dedup"]["mode"],
            "kmer": params["kmer"],
            "trim": params["trim"],
            "panel_fasta": params["panel"]["fasta"],
            "publish_version": params["publish"]["version"],
        },
        "provenance_identity": {
            "snakemake_version": provenance["snakemake_version"],
            "python_executable": provenance["python_executable"],
            "git_commit": provenance["git_commit"],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(args.config, args.provenance)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
