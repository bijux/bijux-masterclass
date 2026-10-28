#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXCLUDED_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "node_modules", "site", "local-store",
}
EXCLUDED_NAMES = {"MANIFEST.json", "MANIFEST.sha256", ".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
TRANSIENT = {"reports/core-proof.json", "reports/doctor.json"}


def payload_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        if any(part in EXCLUDED_DIRS for part in rel_path.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.name.startswith("._"):
            continue
        if path.suffix in EXCLUDED_SUFFIXES or rel in TRANSIENT:
            continue
        yield path, rel


def file_record(root: Path, path: Path, rel: str) -> dict[str, object]:
    raw = path.read_bytes()
    return {
        "path": rel,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "mode": oct(path.stat().st_mode & 0o777),
    }


def record(root: Path) -> dict[str, object]:
    return {
        "schemaVersion": "1.0",
        "root": "03-container-oci-and-software-supply-chain-engineering",
        "files": [file_record(root, p, rel) for p, rel in payload_files(root)],
    }


def write_manifest(root: Path) -> None:
    value = record(root)
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    (root / "MANIFEST.json").write_bytes(raw)
    (root / "MANIFEST.sha256").write_text(
        f"{hashlib.sha256(raw).hexdigest()}  MANIFEST.json\n", encoding="utf-8"
    )
    print(f"wrote course manifest — {len(value['files'])} files")


def verify(root: Path) -> None:
    expected = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    actual = record(root)
    if expected != actual:
        exp = {row["path"]: row for row in expected.get("files", [])}
        act = {row["path"]: row for row in actual.get("files", [])}
        problems = [name for name in sorted(set(exp) | set(act)) if exp.get(name) != act.get(name)]
        raise SystemExit("course manifest mismatch: " + ", ".join(problems[:30]))
    raw = (root / "MANIFEST.json").read_bytes()
    expected_digest = (root / "MANIFEST.sha256").read_text().split()[0]
    if hashlib.sha256(raw).hexdigest() != expected_digest:
        raise SystemExit("MANIFEST.sha256 mismatch")
    print(f"PASS course manifest — {len(actual['files'])} files")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["write", "verify"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.action == "write":
        write_manifest(args.root)
    else:
        verify(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
