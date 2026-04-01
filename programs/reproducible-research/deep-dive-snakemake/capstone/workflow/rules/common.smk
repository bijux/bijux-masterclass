# workflow/rules/common.smk
from __future__ import annotations

import json
import os
from functools import lru_cache

# Ensure our Python package is importable even when jobs run in shadow dirs.
PYTHONPATH = os.path.join(workflow.basedir, "src")


def setdefault_tree(d: dict, key: str, default: dict) -> None:
    """Set a nested default without clobbering user-provided keys."""
    if key not in d or d[key] is None:
        d[key] = default
        return
    for k, v in default.items():
        d[key].setdefault(k, v)


@lru_cache(maxsize=1)
def discovery_payload() -> dict:
    ck = checkpoints.discover_samples.get().output.json
    with open(ck, encoding="utf-8") as fh:
        return json.load(fh)


def get_samples() -> list[str]:
    """Return stable sample IDs for expansion (currently SE only)."""
    if config.get("use_discovered_samples", False):
        data = discovery_payload()
        return [s for s, info in data["samples"].items() if info["mode"] == "SE"]
    return list(config.get("samples", {}).keys())


def get_raw_fastq(wildcards) -> str:
    """Resolve the raw FASTQ path for a sample (currently SE only)."""
    sample = wildcards.sample
    if config.get("use_discovered_samples", False):
        info = discovery_payload()["samples"][sample]
        if info["mode"] != "SE":
            raise ValueError(f"paired-end mode not supported yet for sample '{sample}'")
        return info["reads"]["SE"]
    return config["samples"][sample]


def file_size_mb(path: str) -> float:
    try:
        return os.path.getsize(str(path)) / (1024 * 1024)
    except OSError:
        return 0.0
