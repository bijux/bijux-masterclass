from __future__ import annotations

import hashlib


def partition_for(key: str, partition_count: int) -> int:
    if not key:
        raise ValueError("partition key cannot be blank")
    if partition_count <= 0:
        raise ValueError("partition count must be positive")
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % partition_count
