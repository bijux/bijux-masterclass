from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable

from . import analysis_pb2
from .errors import FailedPrecondition, InvalidArgument, ResourceExhausted


@dataclass(frozen=True)
class UploadResult:
    parent: str
    request_id: str
    filename: str
    media_type: str
    expected_sha256: str
    expected_size: int
    chunks: list[bytes]


def parse_upload(
    frames: Iterable[analysis_pb2.UploadDatasetRequest],
    *,
    max_chunk_bytes: int = 64 * 1024,
    max_total_bytes: int = 2 * 1024 * 1024,
) -> UploadResult:
    metadata = None
    chunks: list[bytes] = []
    total = 0
    for index, frame in enumerate(frames):
        kind = frame.WhichOneof("frame")
        if index == 0:
            if kind != "metadata":
                raise InvalidArgument("first upload frame must contain metadata")
            metadata = frame.metadata
            continue
        if kind != "chunk":
            raise InvalidArgument("upload data frames must contain chunks")
        if len(frame.chunk) > max_chunk_bytes:
            raise ResourceExhausted("upload chunk exceeds byte budget")
        total += len(frame.chunk)
        if total > max_total_bytes:
            raise ResourceExhausted("upload exceeds total byte budget")
        chunks.append(bytes(frame.chunk))
    if metadata is None:
        raise InvalidArgument("upload metadata is required")
    if metadata.expected_size_bytes not in {0, total}:
        raise FailedPrecondition("upload size does not match metadata")
    digest = sha256(b"".join(chunks)).hexdigest()
    if metadata.sha256 and metadata.sha256.lower() != digest:
        raise FailedPrecondition("upload checksum mismatch")
    return UploadResult(
        parent=metadata.parent,
        request_id=metadata.request_id,
        filename=metadata.filename,
        media_type=metadata.media_type,
        expected_sha256=metadata.sha256,
        expected_size=metadata.expected_size_bytes,
        chunks=chunks,
    )


def chunk_bytes(body: bytes, *, chunk_size: int = 8) -> Iterable[tuple[int, bytes, bool]]:
    if chunk_size <= 0:
        raise ValueError("chunk size must be positive")
    if not body:
        yield 0, b"", True
        return
    for offset in range(0, len(body), chunk_size):
        part = body[offset:offset + chunk_size]
        yield offset, part, offset + len(part) == len(body)
