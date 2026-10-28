from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def headings(path: Path, prefix: str = "## ") -> list[str]:
    return [
        line[len(prefix):].strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith(prefix)
    ]


def words(path: Path) -> int:
    return len(re.findall(r"\b\w[\w'’.-]*\b", path.read_text(encoding="utf-8")))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
