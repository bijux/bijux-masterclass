from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class AtomicStoreError(RuntimeError):
    pass


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write_bytes(path: Path, data: bytes, *, mode: int = 0o640) -> None:
    """Publish *data* atomically within one filesystem.

    The function creates the temporary file in the destination directory,
    fsyncs file contents, applies the requested mode, replaces the destination,
    and fsyncs the parent directory. The guarantee remains bounded by the
    filesystem and storage stack beneath the directory.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd: int | None = None
    temp_path: Path | None = None
    try:
        fd, raw_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temp_path = Path(raw_name)
        with os.fdopen(fd, "wb", closefd=True) as handle:
            fd = None
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
            os.fchmod(handle.fileno(), mode)
        os.replace(temp_path, path)
        temp_path = None
        _fsync_directory(path.parent)
    except OSError as exc:
        raise AtomicStoreError(f"failed to publish {path}: {exc}") from exc
    finally:
        if fd is not None:
            os.close(fd)
        if temp_path is not None:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass


def atomic_write_json(path: Path, value: Any, *, mode: int = 0o640) -> None:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    atomic_write_bytes(path, data, mode=mode)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
