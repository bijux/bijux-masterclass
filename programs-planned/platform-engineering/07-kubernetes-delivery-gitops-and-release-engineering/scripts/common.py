#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def words(path: Path) -> int:
    return len(path.read_text(encoding='utf-8').split())

def headings(path: Path) -> list[str]:
    return re.findall(r'(?m)^##\s+(\d+\.\s+.+)$', path.read_text(encoding='utf-8'))

def excluded(path: Path) -> bool:
    rel=path.relative_to(ROOT).as_posix()
    if path.parent==ROOT and path.name in {'MANIFEST.json','MANIFEST.sha256'}: return True
    if any(part in {'__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','site'} for part in path.parts): return True
    if rel.startswith('reports/generated/') or rel.startswith('capstone/reports/runtime/'): return True
    return False
