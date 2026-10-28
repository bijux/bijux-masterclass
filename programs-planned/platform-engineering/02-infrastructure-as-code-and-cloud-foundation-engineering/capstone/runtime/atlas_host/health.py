from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path


def writable_directory(path: Path) -> tuple[bool, str]:
    fd: int | None = None
    probe: Path | None = None
    try:
        path.mkdir(parents=True, exist_ok=True)
        fd, raw_name = tempfile.mkstemp(prefix=".atlas-ready-", dir=path)
        probe = Path(raw_name)
        os.write(fd, b"ok")
        os.fsync(fd)
        return True, "writable"
    except OSError as exc:
        return False, f"not-writable:{exc.errno}"
    finally:
        if fd is not None:
            os.close(fd)
        if probe is not None:
            probe.unlink(missing_ok=True)


def worker_heartbeat(runtime_dir: Path, max_age_seconds: float = 5.0) -> tuple[bool, str]:
    path = runtime_dir / "worker.heartbeat"
    try:
        age = time.time() - path.stat().st_mtime
    except FileNotFoundError:
        return False, "missing"
    return (age <= max_age_seconds, f"age={age:.3f}")
