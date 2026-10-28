from __future__ import annotations

import hashlib
import re

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def sha256_digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def verify_digest(data: bytes, expected: str) -> None:
    if not _DIGEST.fullmatch(expected):
        raise ValueError(f"unsupported or malformed digest: {expected}")
    actual = sha256_digest(data)
    if actual != expected:
        raise ValueError(f"digest mismatch: expected {expected}, got {actual}")


def digest_hex(value: str) -> str:
    if not _DIGEST.fullmatch(value):
        raise ValueError(f"unsupported or malformed digest: {value}")
    return value.split(":", 1)[1]
