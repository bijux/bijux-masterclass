"""Bounded streaming helpers for byte sources."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


def iter_file_range(
    path: Path,
    *,
    start: int = 0,
    length: int | None = None,
    chunk_size: int = 64 * 1024,
) -> Iterator[bytes]:
    if start < 0:
        raise ValueError("start must be non-negative")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    size = path.stat().st_size
    if start > size:
        raise ValueError("start exceeds file size")
    remaining = size - start if length is None else length
    if remaining < 0 or start + remaining > size:
        raise ValueError("invalid length")
    with path.open("rb") as handle:
        handle.seek(start)
        while remaining:
            chunk = handle.read(min(chunk_size, remaining))
            if not chunk:
                raise IOError("unexpected end of file")
            remaining -= len(chunk)
            yield chunk


def estimated_application_buffer_bytes(
    *,
    active_streams: int,
    chunk_size: int,
    buffers_per_stream: int,
) -> int:
    if min(active_streams, chunk_size, buffers_per_stream) < 0:
        raise ValueError("buffer inputs must be non-negative")
    return active_streams * chunk_size * buffers_per_stream
