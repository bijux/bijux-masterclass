"""Bounded, content-addressed filesystem storage.

The staging directory is inside the artifact root so publication can use an
atomic hard-link operation.  ``os.replace`` is atomic but can overwrite an
existing object; a content-addressed store must instead publish with
*no-clobber* semantics.
"""

from __future__ import annotations

import asyncio
from hashlib import sha256
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import BinaryIO, Iterable

from .failures import ServiceError
from .ports import StagedFile


CHUNK_SIZE = 64 * 1024


class FileSystemArtifactStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.staging = self.root / ".staging"
        self.staging.mkdir(parents=True, exist_ok=True)

    def _safe(self, key: str) -> Path:
        relative = PurePosixPath(key)
        if relative.is_absolute() or not relative.parts or ".." in relative.parts:
            raise ValueError("unsafe storage key")
        path = (self.root / Path(*relative.parts)).resolve()
        if path != self.root and self.root not in path.parents:
            raise ValueError("storage key escaped root")
        return path

    async def stage_upload(
        self,
        source: BinaryIO,
        media_type: str,
        limit: int,
    ) -> StagedFile:
        descriptor, raw_path = tempfile.mkstemp(
            prefix="upload-",
            dir=self.staging,
        )
        path = Path(raw_path)
        digest = sha256()
        size = 0
        try:
            with os.fdopen(descriptor, "wb") as target:
                while True:
                    block = await asyncio.to_thread(source.read, CHUNK_SIZE)
                    if not block:
                        break
                    size += len(block)
                    if size > limit:
                        raise ServiceError(
                            413,
                            "Payload too large",
                            "The training upload limit is 1 MiB.",
                            "payload-too-large",
                        )
                    digest.update(block)
                    target.write(block)
                target.flush()
                os.fsync(target.fileno())
            if size == 0:
                raise ServiceError(
                    422,
                    "Request validation failed",
                    "The uploaded file is empty.",
                    "validation",
                )
            return StagedFile(path, size, digest.hexdigest(), media_type)
        except BaseException:
            path.unlink(missing_ok=True)
            raise

    def stage_bytes(self, content: bytes, media_type: str) -> StagedFile:
        if not content:
            raise ValueError("artifact cannot be empty")
        descriptor, raw_path = tempfile.mkstemp(
            prefix="artifact-",
            dir=self.staging,
        )
        path = Path(raw_path)
        try:
            with os.fdopen(descriptor, "wb") as target:
                target.write(content)
                target.flush()
                os.fsync(target.fileno())
            return StagedFile(
                path,
                len(content),
                sha256(content).hexdigest(),
                media_type,
            )
        except BaseException:
            path.unlink(missing_ok=True)
            raise

    def publish(self, staged: StagedFile, key: str) -> Path:
        """Publish once without overwriting an existing content object.

        Two workers may race.  Exactly one hard link is created; later workers
        treat an existing object with the same digest as an idempotent success.
        Different bytes for the same key are an integrity failure.
        """

        final = self._safe(key)
        final.parent.mkdir(parents=True, exist_ok=True)
        if final.is_symlink():
            self.discard(staged)
            raise RuntimeError("refusing to publish through a symbolic link")

        try:
            os.link(staged.temporary_path, final)
        except FileExistsError:
            if final.is_symlink() or self._digest(final) != staged.checksum_sha256:
                self.discard(staged)
                raise RuntimeError("idempotent publish found different bytes")
        else:
            self._fsync_directory(final.parent)
        finally:
            staged.temporary_path.unlink(missing_ok=True)
        return final

    def discard(self, staged: StagedFile) -> None:
        staged.temporary_path.unlink(missing_ok=True)

    def path_for(
        self,
        key: str,
        expected_checksum: str | None = None,
    ) -> Path:
        path = self._safe(key)
        if path.is_symlink() or not path.is_file():
            raise FileNotFoundError(key)
        if expected_checksum and self._digest(path) != expected_checksum:
            raise ServiceError(
                500,
                "Artifact integrity failure",
                "Artifact integrity verification failed.",
                "artifact-integrity",
                public=False,
            )
        return path

    def keys(self) -> set[str]:
        return {
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*")
            if path.is_file()
            and not path.is_symlink()
            and self.staging not in path.parents
        }

    def orphan_keys(self, referenced: Iterable[str]) -> set[str]:
        return self.keys() - set(referenced)

    @staticmethod
    def _digest(path: Path) -> str:
        digest = sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(128 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    @staticmethod
    def _fsync_directory(directory: Path) -> None:
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
