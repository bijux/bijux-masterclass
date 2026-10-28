from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
import json
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "generated"


def record(value: Any) -> Any:
    """Convert dataclass evidence into JSON-safe values without losing structure."""
    if is_dataclass(value):
        return {key: record(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): record(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [record(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(record(item) for item in value)
    return value


def emit(name: str, obj: Any) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / name
    path.write_text(
        json.dumps(record(obj), indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(path)
    return path
