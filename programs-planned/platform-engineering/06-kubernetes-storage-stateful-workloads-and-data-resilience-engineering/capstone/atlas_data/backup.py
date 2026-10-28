from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import time

from .durability import write_atomic


@dataclass(frozen=True)
class BackupManifest:
    id: str
    logical_name: str
    generation: int
    created_ns: int
    files: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class RestoreResult:
    verified: bool
    generation: int
    files: int
    elapsed_ms: float


class BackupRepository:
    """Content-addressed educational backup repository.

    It demonstrates inventory, immutable object identity, manifest identity,
    empty-destination restore, and end-to-end digest verification. It is not a
    replacement for an operated backup product or independent failure domain.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.objects = self.root / "objects"
        self.manifests = self.root / "manifests"
        self.objects.mkdir(parents=True, exist_ok=True)
        self.manifests.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe_relative(path: Path, source: Path) -> str:
        relative = path.relative_to(source).as_posix()
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError("unsafe backup path")
        return relative

    def _store_object(self, data: bytes) -> str:
        digest = hashlib.sha256(data).hexdigest()
        target = self.objects / digest
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                raise ValueError("existing backup object is corrupt")
            return digest
        temporary = self.objects / f".{digest}.{os.getpid()}.tmp"
        try:
            with temporary.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(temporary, target)
            except FileExistsError:
                pass
            directory_fd = os.open(self.objects, os.O_DIRECTORY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            temporary.unlink(missing_ok=True)
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError("published backup object is corrupt")
        return digest

    def backup_directory(
        self,
        source: str | Path,
        logical_name: str,
        generation: int,
    ) -> BackupManifest:
        source = Path(source)
        if not source.is_dir():
            raise ValueError("backup source must be a directory")
        entries: list[dict[str, object]] = []
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError("symlinks are not accepted in backup source")
            if not path.is_file():
                continue
            data = path.read_bytes()
            digest = self._store_object(data)
            entries.append(
                {
                    "path": self._safe_relative(path, source),
                    "sha256": digest,
                    "bytes": len(data),
                    "mode": oct(path.stat().st_mode & 0o777),
                }
            )
        body = {
            "logicalName": logical_name,
            "generation": generation,
            "files": entries,
        }
        canonical = json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        manifest_id = hashlib.sha256(canonical).hexdigest()
        target = self.manifests / f"{manifest_id}.json"
        if target.exists():
            existing = json.loads(target.read_text(encoding="utf-8"))
            created_ns = int(existing["createdNs"])
        else:
            created_ns = time.time_ns()
            document = {"id": manifest_id, "createdNs": created_ns, **body}
            write_atomic(
                target,
                json.dumps(document, indent=2, sort_keys=True).encode("utf-8")
                + b"\n",
            )
        return BackupManifest(
            id=manifest_id,
            logical_name=logical_name,
            generation=generation,
            created_ns=created_ns,
            files=tuple(entries),
        )

    def load(self, manifest_id: str) -> BackupManifest:
        path = self.manifests / f"{manifest_id}.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        body = {
            "logicalName": document["logicalName"],
            "generation": document["generation"],
            "files": document["files"],
        }
        canonical = json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        if hashlib.sha256(canonical).hexdigest() != manifest_id:
            raise ValueError("backup manifest identity mismatch")
        return BackupManifest(
            id=document["id"],
            logical_name=document["logicalName"],
            generation=int(document["generation"]),
            created_ns=int(document["createdNs"]),
            files=tuple(document["files"]),
        )

    def restore(self, manifest_id: str, destination: str | Path) -> RestoreResult:
        started = time.monotonic()
        destination = Path(destination)
        if destination.exists() and any(destination.iterdir()):
            raise ValueError("restore destination must be empty")
        destination.mkdir(parents=True, exist_ok=True)
        manifest = self.load(manifest_id)
        restored = 0
        for entry in manifest.files:
            relative = PurePosixPath(str(entry["path"]))
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("unsafe path in manifest")
            source = self.objects / str(entry["sha256"])
            if not source.is_file():
                raise FileNotFoundError(
                    f"missing backup object {entry['sha256']}"
                )
            data = source.read_bytes()
            if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise ValueError("backup object digest mismatch")
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            write_atomic(target, data, int(str(entry["mode"]), 8))
            restored += 1
        verified = all(
            (destination / str(entry["path"])).is_file()
            and hashlib.sha256(
                (destination / str(entry["path"])).read_bytes()
            ).hexdigest()
            == entry["sha256"]
            for entry in manifest.files
        )
        elapsed = (time.monotonic() - started) * 1000.0
        return RestoreResult(
            verified=verified,
            generation=manifest.generation,
            files=restored,
            elapsed_ms=elapsed,
        )
