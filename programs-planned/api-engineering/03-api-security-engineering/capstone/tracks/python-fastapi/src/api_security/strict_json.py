from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

from .errors import SecurityControlError

DANGEROUS_KEYS = frozenset({"__proto__", "prototype", "constructor"})


def _reject_constant(value: str) -> None:
    raise SecurityControlError("non-finite", f"JSON constant {value!r} is prohibited")


def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SecurityControlError("duplicate-key", "JSON object contains a duplicate member")
        if key in DANGEROUS_KEYS:
            raise SecurityControlError("dangerous-key", "JSON object contains a prohibited member name")
        result[key] = value
    return result


def _check_depth(value: Any, maximum: int, current: int = 1) -> None:
    if current > maximum:
        raise SecurityControlError("depth", "JSON nesting exceeds the configured maximum")
    if isinstance(value, dict):
        for item in value.values():
            _check_depth(item, maximum, current + 1)
    elif isinstance(value, list):
        for item in value:
            _check_depth(item, maximum, current + 1)


def parse_strict_json(
    raw: bytes,
    *,
    max_bytes: int = 1_048_576,
    max_depth: int = 32,
) -> Any:
    if len(raw) > max_bytes:
        raise SecurityControlError("body-too-large", "JSON body exceeds the configured byte limit", 413)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SecurityControlError("invalid-utf8", "JSON body is not valid UTF-8") from exc

    decoder = json.JSONDecoder(
        object_pairs_hook=_pairs_hook,
        parse_constant=_reject_constant,
    )
    try:
        value, end = decoder.raw_decode(text)
    except SecurityControlError:
        raise
    except json.JSONDecodeError as exc:
        raise SecurityControlError("invalid-json", "JSON syntax is invalid") from exc
    if text[end:].strip():
        raise SecurityControlError("trailing-content", "content follows the JSON value")
    _check_depth(value, max_depth)
    return value
