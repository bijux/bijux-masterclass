"""Pure HTTP representation helpers for validators, ranges, and compression."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

_ETAG_RE = re.compile(r'^(W/)?"(?:[\x21\x23-\x7E\x80-\xFF]*)"$')


class HTTPPolicyError(ValueError):
    pass


def parse_etag_list(value: str) -> tuple[str, ...] | str:
    stripped = value.strip()
    if stripped == "*":
        return "*"
    if not stripped:
        raise HTTPPolicyError("empty entity-tag list")
    tags = tuple(part.strip() for part in stripped.split(","))
    if any(not _ETAG_RE.fullmatch(tag) for tag in tags):
        raise HTTPPolicyError("malformed entity tag")
    return tags


def _opaque(tag: str) -> str:
    return tag[2:] if tag.startswith("W/") else tag


def weak_match(left: str, right: str) -> bool:
    if not _ETAG_RE.fullmatch(left) or not _ETAG_RE.fullmatch(right):
        raise HTTPPolicyError("malformed entity tag")
    return _opaque(left) == _opaque(right)


def strong_match(left: str, right: str) -> bool:
    if left.startswith("W/") or right.startswith("W/"):
        return False
    if not _ETAG_RE.fullmatch(left) or not _ETAG_RE.fullmatch(right):
        raise HTTPPolicyError("malformed entity tag")
    return left == right


def if_none_match_matches(header_value: str, current_etag: str) -> bool:
    parsed = parse_etag_list(header_value)
    if parsed == "*":
        return True
    return any(weak_match(tag, current_etag) for tag in parsed)


def if_range_allows_range(header_value: str, current_etag: str) -> bool:
    value = header_value.strip()
    if not value.startswith('"') and not value.startswith('W/"'):
        # This course profile supports the entity-tag form only.
        return False
    return strong_match(value, current_etag)


@dataclass(frozen=True, slots=True)
class RangeSelection:
    start: int
    end_exclusive: int
    complete_length: int

    @property
    def length(self) -> int:
        return self.end_exclusive - self.start

    @property
    def content_range(self) -> str:
        return (
            f"bytes {self.start}-{self.end_exclusive - 1}/"
            f"{self.complete_length}"
        )


class RangeNotSatisfiable(HTTPPolicyError):
    def __init__(self, complete_length: int) -> None:
        self.complete_length = complete_length
        super().__init__(f"bytes */{complete_length}")


def parse_single_range(value: str, complete_length: int) -> RangeSelection:
    if complete_length < 0:
        raise HTTPPolicyError("complete length must be non-negative")
    if not value.startswith("bytes="):
        raise HTTPPolicyError("only bytes ranges are supported")
    spec = value[6:].strip()
    if "," in spec:
        raise HTTPPolicyError("multiple ranges are not supported")
    if "-" not in spec:
        raise HTTPPolicyError("malformed byte range")
    first, last = (part.strip() for part in spec.split("-", 1))
    if complete_length == 0:
        raise RangeNotSatisfiable(complete_length)

    if first == "":
        if not last.isdigit():
            raise HTTPPolicyError("malformed suffix range")
        suffix = int(last)
        if suffix <= 0:
            raise RangeNotSatisfiable(complete_length)
        length = min(suffix, complete_length)
        return RangeSelection(
            start=complete_length - length,
            end_exclusive=complete_length,
            complete_length=complete_length,
        )

    if not first.isdigit():
        raise HTTPPolicyError("malformed range start")
    start = int(first)
    if start >= complete_length:
        raise RangeNotSatisfiable(complete_length)

    if last == "":
        end_exclusive = complete_length
    else:
        if not last.isdigit():
            raise HTTPPolicyError("malformed range end")
        inclusive_end = int(last)
        if inclusive_end < start:
            raise RangeNotSatisfiable(complete_length)
        end_exclusive = min(inclusive_end + 1, complete_length)

    return RangeSelection(start, end_exclusive, complete_length)


_COMPRESSIBLE_PREFIXES = (
    "application/json",
    "application/problem+json",
    "text/",
    "application/xml",
)


def choose_content_encoding(
    *,
    accept_encoding: str,
    media_type: str,
    body_length: int,
    minimum_size: int = 1024,
    range_requested: bool = False,
) -> str:
    if body_length < 0 or minimum_size < 0:
        raise HTTPPolicyError("lengths must be non-negative")
    if range_requested:
        return "identity"
    compressible = any(
        media_type.lower().startswith(prefix)
        for prefix in _COMPRESSIBLE_PREFIXES
    )
    if not compressible or body_length < minimum_size:
        return "identity"
    accepted = {
        item.split(";", 1)[0].strip().lower()
        for item in accept_encoding.split(",")
    }
    return "gzip" if "gzip" in accepted or "*" in accepted else "identity"


def content_chunks(
    data: bytes,
    *,
    start: int = 0,
    length: int | None = None,
    chunk_size: int = 64 * 1024,
) -> Iterable[bytes]:
    if start < 0 or start > len(data):
        raise ValueError("invalid start")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    remaining = len(data) - start if length is None else length
    if remaining < 0 or start + remaining > len(data):
        raise ValueError("invalid length")
    offset = start
    while remaining:
        size = min(chunk_size, remaining)
        yield data[offset : offset + size]
        offset += size
        remaining -= size
