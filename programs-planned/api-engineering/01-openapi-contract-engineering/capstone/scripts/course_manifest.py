#!/usr/bin/env python3
"""Create or verify the deterministic course payload manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "MANIFEST.json"
CHECKSUM = ROOT / "MANIFEST.sha256"

IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "site",
    ".runtime",
    "dist-core",
}
IGNORED_FILES = {".DS_Store"}


class ManifestError(RuntimeError):
    pass


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def payload_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if relative.as_posix() in {"MANIFEST.json", "MANIFEST.sha256"}:
            continue
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.name in IGNORED_FILES or path.suffix in {".pyc", ".pyo"}:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def mode(path: Path) -> str:
    return format(stat.S_IMODE(path.stat().st_mode), "04o")


def create() -> None:
    files = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "mode": mode(path),
            "sha256": digest(path),
        }
        for path in payload_files()
    ]
    payload = {
        "format": 1,
        "root": ROOT.name,
        "scope": "All distributable payload files except this manifest pair and generated dependency/cache/site directories.",
        "files": files,
    }
    MANIFEST.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    CHECKSUM.write_text(
        f"{digest(MANIFEST)}  MANIFEST.json\n",
        encoding="utf-8",
    )
    print(f"PASS course manifest create — {len(files)} files")


def verify() -> None:
    if not MANIFEST.is_file() or not CHECKSUM.is_file():
        raise ManifestError("course manifest is missing; run manifest-create")
    expected_manifest_digest = CHECKSUM.read_text(encoding="utf-8").split()[0]
    if digest(MANIFEST) != expected_manifest_digest:
        raise ManifestError("MANIFEST.sha256 does not match MANIFEST.json")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {item["path"]: item for item in data["files"]}
    current = {
        path.relative_to(ROOT).as_posix(): {
            "bytes": path.stat().st_size,
            "mode": mode(path),
            "sha256": digest(path),
        }
        for path in payload_files()
    }
    if expected.keys() != current.keys():
        missing = sorted(expected.keys() - current.keys())
        unexpected = sorted(current.keys() - expected.keys())
        raise ManifestError(
            "manifest file set differs: "
            f"missing={missing[:10]}, unexpected={unexpected[:10]}"
        )
    for name, item in expected.items():
        observed = current[name]
        wanted = {
            "bytes": item["bytes"],
            "mode": item["mode"],
            "sha256": item["sha256"],
        }
        if observed != wanted:
            raise ManifestError(f"manifest mismatch: {name}")
    print(f"PASS course manifest proof — {len(expected)} files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["create", "verify"])
    args = parser.parse_args()
    try:
        create() if args.command == "create" else verify()
    except ManifestError as exc:
        print(f"MANIFEST FAILED: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
