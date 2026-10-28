from __future__ import annotations

import os
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Sequence
from urllib.parse import unquote

from .errors import SecurityControlError

BIDI_CONTROLS = frozenset(chr(x) for x in [0x061C, *range(0x202A, 0x202F), *range(0x2066, 0x206A)])


def validate_filename(value: str, *, max_length: int = 160) -> str:
    if not value or len(value) > max_length:
        raise SecurityControlError("invalid-filename", "filename length is invalid")
    if value in {".", ".."} or "/" in value or "\\" in value or "\x00" in value:
        raise SecurityControlError("invalid-filename", "filename contains a path or control delimiter")
    if any(ch in BIDI_CONTROLS or unicodedata.category(ch).startswith("C") for ch in value):
        raise SecurityControlError("invalid-filename", "filename contains an invisible control character")
    return value


def confined_path(root: Path, value: str, *, percent_decode: bool = True) -> Path:
    decoded = unquote(value) if percent_decode else value
    candidate = Path(decoded)
    if candidate.is_absolute():
        raise SecurityControlError("path-escape", "absolute paths are prohibited")
    root_resolved = root.resolve()
    resolved = (root_resolved / candidate).resolve(strict=False)
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise SecurityControlError("path-escape", "path escapes the configured root")
    return resolved


def reject_symlink(path: Path) -> None:
    current = path
    while True:
        if current.exists() and current.is_symlink():
            raise SecurityControlError("symlink-prohibited", "symbolic links are prohibited")
        if current.parent == current:
            return
        current = current.parent


@dataclass(frozen=True, slots=True)
class ArchiveMember:
    name: str
    size: int
    kind: str = "file"


def validate_archive_members(
    members: Sequence[ArchiveMember],
    *,
    max_members: int = 100,
    max_member_bytes: int = 10_000_000,
    max_total_bytes: int = 50_000_000,
) -> None:
    if len(members) > max_members:
        raise SecurityControlError("archive-limit", "archive member count exceeds the limit")
    total = 0
    for member in members:
        if member.kind != "file":
            raise SecurityControlError("archive-entry", "archive contains a prohibited entry type")
        validate_filename(Path(member.name).name)
        normalized = Path(member.name)
        if normalized.is_absolute() or ".." in normalized.parts:
            raise SecurityControlError("archive-path", "archive member path escapes the root")
        if member.size < 0 or member.size > max_member_bytes:
            raise SecurityControlError("archive-limit", "archive member size exceeds the limit")
        total += member.size
        if total > max_total_bytes:
            raise SecurityControlError("archive-limit", "archive expanded size exceeds the limit")


def copy_bounded(chunks: Iterable[bytes], destination: BinaryIO, *, max_bytes: int) -> int:
    total = 0
    for chunk in chunks:
        if not isinstance(chunk, (bytes, bytearray)):
            raise TypeError("stream chunks must be bytes")
        total += len(chunk)
        if total > max_bytes:
            raise SecurityControlError("upload-too-large", "upload exceeds the configured byte limit", 413)
        destination.write(chunk)
    return total
