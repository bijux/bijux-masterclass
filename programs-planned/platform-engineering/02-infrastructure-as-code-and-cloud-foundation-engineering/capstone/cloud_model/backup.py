from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
from typing import Any

from .identity import digest_file, digest_object


class BackupError(ValueError):
    pass


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    size: int
    sha256: str
    mode: str


def _safe_relative(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    if any(part in {"..", ""} for part in relative.parts):
        raise BackupError(f"unsafe path: {path}")
    return relative.as_posix()


def create_manifest(source: Path, *, release: str, consistency_point: str) -> dict[str, Any]:
    if not source.is_dir():
        raise BackupError("backup source must be a directory")
    entries: list[dict[str, Any]] = []
    for path in sorted(p for p in source.rglob("*") if p.is_file() and not p.is_symlink()):
        stat = path.stat()
        entry = ManifestEntry(
            path=_safe_relative(path, source),
            size=stat.st_size,
            sha256=digest_file(path),
            mode=oct(stat.st_mode & 0o777),
        )
        entries.append(entry.__dict__)
    payload: dict[str, Any] = {
        "schemaVersion": "1.0",
        "release": release,
        "consistencyPoint": consistency_point,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    payload["manifestDigest"] = digest_object({k: v for k, v in payload.items() if k != "createdAt"})
    return payload


def materialize_backup(source: Path, destination: Path, manifest: dict[str, Any]) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise BackupError("backup destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    for entry in manifest.get("entries", []):
        source_path = source / entry["path"]
        target = destination / entry["path"]
        if source_path.is_symlink():
            raise BackupError("symlinks are not accepted in the course backup profile")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target)
        os.chmod(target, int(entry["mode"], 8))
    (destination / "backup-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def restore_backup(backup: Path, destination: Path) -> dict[str, Any]:
    if destination.exists() and any(destination.iterdir()):
        raise BackupError("restore destination must be empty")
    manifest_path = backup / "backup-manifest.json"
    if not manifest_path.is_file():
        raise BackupError("backup manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    destination.mkdir(parents=True, exist_ok=True)
    restored: list[dict[str, Any]] = []
    for entry in manifest.get("entries", []):
        rel = Path(entry["path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise BackupError("unsafe path in backup manifest")
        source = backup / rel
        target = destination / rel
        if source.is_symlink() or not source.is_file():
            raise BackupError(f"backup entry is not a regular file: {rel}")
        if source.stat().st_size != int(entry["size"]):
            raise BackupError(f"size mismatch: {rel}")
        if digest_file(source) != entry["sha256"]:
            raise BackupError(f"checksum mismatch: {rel}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        os.chmod(target, int(entry["mode"], 8))
        restored.append({"path": rel.as_posix(), "sha256": entry["sha256"]})
    return {"restored": restored, "release": manifest["release"], "verified": True}
