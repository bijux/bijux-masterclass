from __future__ import annotations

import json
import math
from typing import Any

MAX_SAFE_INTEGER = 9_007_199_254_740_991


class CanonicalizationError(ValueError):
    """Raised when a value has no safe cross-language canonical form."""


def _validate(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise CanonicalizationError(f"unsafe integer at {path}")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError(f"non-finite number at {path}")
        raise CanonicalizationError(
            f"floating-point number at {path}; use a scaled integer or decimal string"
        )
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(f"non-string object key at {path}")
            _validate(item, f"{path}.{key}")
        return
    raise CanonicalizationError(
        f"unsupported value {type(value).__name__} at {path}"
    )


def canonical_json(value: Any) -> str:
    """Return deterministic UTF-8 JSON shared by Python and TypeScript."""
    _validate(value)
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")
