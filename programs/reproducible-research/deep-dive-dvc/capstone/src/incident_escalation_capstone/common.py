from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable

FEATURE_NAMES = (
    "backlog_days",
    "reopened_count",
    "integration_touchpoints",
    "customer_tier",
    "weekend_handoff",
    "severity_score",
)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: object) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_bucket(value: str, seed: int, modulus: int) -> int:
    digest = hashlib.sha256(f"{seed}:{value}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % modulus


def as_int(raw: str, field_name: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an integer, got {raw!r}") from exc


def as_float(raw: str, field_name: str) -> float:
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a float, got {raw!r}") from exc


def load_params(path: Path) -> dict[str, object]:
    import yaml

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
