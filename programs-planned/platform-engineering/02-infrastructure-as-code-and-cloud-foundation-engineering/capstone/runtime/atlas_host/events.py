from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, TextIO


@dataclass(frozen=True)
class Event:
    name: str
    timestamp_ns: int
    pid: int
    fields: dict[str, Any]


def _event(name: str, fields: dict[str, Any]) -> Event:
    return Event(name=name, timestamp_ns=time.time_ns(), pid=os.getpid(), fields=fields)


def _line(event: Event) -> bytes:
    return (json.dumps(asdict(event), sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def emit(name: str, *, stream: TextIO = sys.stdout, **fields: Any) -> Event:
    event = _event(name, fields)
    stream.write(_line(event).decode("utf-8"))
    stream.flush()
    return event


def append(path: Path, name: str, **fields: Any) -> Event:
    """Append one complete local-filesystem event record.

    O_APPEND makes offset selection and the single write one kernel operation on
    the local course filesystem. This is not a claim about remote filesystems or
    a replacement for a maintained log transport.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    event = _event(name, fields)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o660)
    try:
        os.write(fd, _line(event))
        os.fsync(fd)
    finally:
        os.close(fd)
    return event
