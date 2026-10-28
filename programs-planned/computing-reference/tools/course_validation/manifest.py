from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def normalized_row(row: dict[str, Any]) -> dict[str, str]:
    return {key: str(value) for key, value in row.items()}


def module_rows(root: Path) -> list[dict[str, str]]:
    return read_csv(root / "manifests" / "modules.csv")


def find_module(root: Path, module_id: str) -> dict[str, str] | None:
    matches = [row for row in module_rows(root) if row["module_id"] == module_id]
    if len(matches) != 1:
        return None
    return matches[0]
