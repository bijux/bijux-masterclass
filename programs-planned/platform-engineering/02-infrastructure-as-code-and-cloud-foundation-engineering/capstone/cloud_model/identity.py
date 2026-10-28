from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> bytes:
    """Return the course canonical JSON representation.

    The profile rejects NaN/Infinity and uses UTF-8, sorted keys, and compact
    separators. It is intended for evidence identity, not as a universal
    cryptographic canonicalization standard.
    """

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_object(value: Any) -> str:
    return digest_bytes(canonical_json(value))


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()
