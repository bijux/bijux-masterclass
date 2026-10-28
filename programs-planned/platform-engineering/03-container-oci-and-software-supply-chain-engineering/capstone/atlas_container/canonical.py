from __future__ import annotations

import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    """Return one stable JSON representation used by course artifacts.

    OCI itself binds digests to the exact bytes that were stored. It does not
    require this canonicalization. Atlas uses it so independent Python and
    TypeScript examples can construct the same instructional fixtures.
    """
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def parse_json_object(data: bytes) -> dict[str, Any]:
    value = json.loads(data)
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value
