from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]
EXCLUDED_PARTS = {".venv", "__pycache__", ".pytest_cache", "site", "runtime"}
EXCLUDED_FILES = {"MANIFEST.json", "MANIFEST.sha256"}


def payload_files() -> list[Path]:
    files = []
    for path in COURSE.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(COURSE)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.name in EXCLUDED_FILES:
            continue
        if rel.parts[:2] == ("capstone", "reports") and path.name != ".gitkeep":
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(COURSE).as_posix())


def create() -> int:
    entries = []
    for path in payload_files():
        rel = path.relative_to(COURSE).as_posix()
        entries.append({"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size, "mode": oct(path.stat().st_mode & 0o777)})
    manifest = {"schemaVersion": 1, "course": COURSE.name, "files": entries}
    raw = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (COURSE / "MANIFEST.json").write_text(raw)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    (COURSE / "MANIFEST.sha256").write_text(f"{digest}  MANIFEST.json\n")
    print(f"created manifest for {len(entries)} files")
    return 0


def verify() -> int:
    manifest_path = COURSE / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    expected = {item["path"]: item for item in manifest["files"]}
    actual_paths = {p.relative_to(COURSE).as_posix(): p for p in payload_files()}
    if set(expected) != set(actual_paths):
        missing = sorted(set(expected) - set(actual_paths))
        extra = sorted(set(actual_paths) - set(expected))
        raise SystemExit(f"manifest path mismatch missing={missing[:10]} extra={extra[:10]}")
    for rel, item in expected.items():
        path = actual_paths[rel]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        actual_mode = oct(path.stat().st_mode & 0o777)
        if (
            digest != item["sha256"]
            or path.stat().st_size != item["bytes"]
            or actual_mode != item["mode"]
        ):
            raise SystemExit(f"manifest mismatch: {rel}")
    listed = (COURSE / "MANIFEST.sha256").read_text().split()[0]
    digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if listed != digest:
        raise SystemExit("MANIFEST.sha256 mismatch")
    print(f"verified manifest for {len(expected)} files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "verify"])
    args = parser.parse_args()
    return create() if args.action == "create" else verify()


if __name__ == "__main__":
    raise SystemExit(main())
