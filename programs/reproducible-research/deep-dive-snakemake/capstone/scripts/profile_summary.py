#!/usr/bin/env python3
"""Write a compact comparison of the Snakemake profile surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_scalar(raw: str) -> object:
    text = raw.strip()
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text


def load_profile(path: Path) -> dict[str, object]:
    payload: dict[str, object] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, _, value = stripped.partition(":")
        if not _:
            raise ValueError(f"invalid profile line in {path}: {line!r}")
        payload[key.strip()] = parse_scalar(value)
    return payload


def build_summary(profile_paths: dict[str, Path]) -> dict[str, object]:
    loaded = {
        name: load_profile(path)
        for name, path in sorted(
            profile_paths.items(),
            key=lambda item: item[0],
        )
    }
    keys = sorted({key for payload in loaded.values() for key in payload})

    shared_settings: dict[str, object] = {}
    differing_settings: dict[str, dict[str, object | None]] = {}
    profile_only_settings: dict[str, list[str]] = {}

    for key in keys:
        values = {name: payload.get(key) for name, payload in loaded.items()}
        present_names = [name for name, value in values.items() if value is not None]
        distinct = {json.dumps(value, sort_keys=True) for value in values.values()}
        if len(distinct) == 1:
            shared_settings[key] = next(iter(values.values()))
        else:
            differing_settings[key] = values
        if len(present_names) != len(loaded):
            profile_only_settings[key] = present_names

    return {
        "profiles": {
            name: path.resolve().as_posix()
            for name, path in sorted(profile_paths.items())
        },
        "shared_settings": shared_settings,
        "differing_settings": differing_settings,
        "profile_only_settings": profile_only_settings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=Path, required=True)
    parser.add_argument("--ci", type=Path, required=True)
    parser.add_argument("--slurm", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(
        {
            "local": args.local,
            "ci": args.ci,
            "slurm": args.slurm,
        }
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
