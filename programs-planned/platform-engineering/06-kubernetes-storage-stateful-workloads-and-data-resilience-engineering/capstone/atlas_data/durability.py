from __future__ import annotations

import os
from pathlib import Path


def write_atomic(path: str | Path, data: bytes, mode: int = 0o640) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.{os.getpid()}.tmp"
    try:
        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.chmod(mode)
        os.replace(temporary, path)
        descriptor = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        temporary.unlink(missing_ok=True)
