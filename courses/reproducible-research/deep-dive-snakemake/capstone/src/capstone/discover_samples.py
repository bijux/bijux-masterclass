#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

_FASTQ_SUFFIXES = (".fastq.gz", ".fq.gz", ".fastq", ".fq")


def _strip_fastq_suffix(name: str) -> str:
    for suf in _FASTQ_SUFFIXES:
        if name.endswith(suf):
            return name[: -len(suf)]
    # fall back: keep stem-ish behavior
    return Path(name).stem


@dataclass(frozen=True)
class ParsedName:
    sample: str
    mate: str  # "SE", "R1", "R2"


_MATE_SUFFIXES = (
    ("_R1", "R1"),
    ("_R2", "R2"),
    ("-R1", "R1"),
    ("-R2", "R2"),
    (".R1", "R1"),
    (".R2", "R2"),
    ("_1", "R1"),
    ("_2", "R2"),
    ("-1", "R1"),
    ("-2", "R2"),
    (".1", "R1"),
    (".2", "R2"),
)


def parse_sample_and_mate(path: Path) -> ParsedName:
    base = _strip_fastq_suffix(path.name)

    # Common PE conventions put mate at the end.
    for suf, mate in _MATE_SUFFIXES:
        if base.endswith(suf):
            sample = base[: -len(suf)]
            if not sample:
                break
            return ParsedName(sample=sample, mate=mate)

    return ParsedName(sample=base, mate="SE")


def discover_fastqs(raw_dir: Path, glob_pat: str) -> list[Path]:
    # Deterministic: sorted by name.
    files = sorted((p for p in raw_dir.glob(glob_pat) if p.is_file()), key=lambda p: p.name)
    # Deduplicate if glob expands oddly.
    return sorted(set(files), key=lambda p: p.name)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Discover samples from a raw FASTQ directory (deterministic)."
    )
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--glob", default="*.fastq.gz", help="Glob pattern relative to raw-dir.")
    ap.add_argument(
        "--allow-paired-end", action="store_true", help="Allow paired-end naming conventions."
    )
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    raw_dir = Path(args.raw_dir)
    out_json = Path(args.out_json)

    if not raw_dir.exists():
        raise SystemExit(f"raw dir does not exist: {raw_dir}")

    fastqs = discover_fastqs(raw_dir, args.glob)

    by_sample: dict[str, dict[str, str]] = {}

    for p in fastqs:
        parsed = parse_sample_and_mate(p)

        if parsed.mate in ("R1", "R2"):
            if not args.allow_paired_end:
                raise SystemExit(
                    f"paired-end file detected ({p.name}) but --allow-paired-end not set"
                )

        by_sample.setdefault(parsed.sample, {})
        if parsed.mate in by_sample[parsed.sample]:
            msg = (
                f"naming collision: sample '{parsed.sample}' has multiple files "
                f"for mate '{parsed.mate}'"
            )
            raise SystemExit(msg)
        by_sample[parsed.sample][parsed.mate] = str(p)

    # Validate PE completeness if any PE detected.
    samples: dict[str, dict] = {}
    for sample in sorted(by_sample.keys()):
        mates = by_sample[sample]
        if "SE" in mates and (("R1" in mates) or ("R2" in mates)):
            raise SystemExit(f"mixed SE+PE naming for sample '{sample}': {mates}")

        if "SE" in mates:
            samples[sample] = {"mode": "SE", "reads": {"SE": mates["SE"]}}
            continue

        if ("R1" in mates) or ("R2" in mates):
            missing = [m for m in ("R1", "R2") if m not in mates]
            if missing:
                raise SystemExit(
                    f"paired-end sample '{sample}' missing mates: {missing} (found: {mates})"
                )
            samples[sample] = {"mode": "PE", "reads": {"R1": mates["R1"], "R2": mates["R2"]}}
            continue

        # no recognized files (shouldn't happen)
        raise SystemExit(f"no FASTQ files recognized for sample '{sample}'")

    payload = {
        "raw_dir": str(raw_dir),
        "glob": args.glob,
        "n_files": len(fastqs),
        "allow_paired_end": bool(args.allow_paired_end),
        "samples": samples,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
