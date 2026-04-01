"""Module 07 infra: atomic write-if-absent adapter for idempotent writes.

End-of-Module-09 snapshot."""

from __future__ import annotations

import os
from collections.abc import Iterator

from funcpipe_rag.core.rag_types import Chunk
from funcpipe_rag.domain.idempotent import AtomicWriteCap
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result

from .file_storage import FileStorage


class AtomicFileStorage(AtomicWriteCap):
    def __init__(self, *, root: str) -> None:
        self.root = root
        self._storage = FileStorage()

    def write_if_absent(self, key: str, chunks: Iterator[Chunk]) -> Result[bool, ErrInfo]:
        path = os.path.join(self.root, key)
        if os.path.exists(path):
            return Ok(False)
        res = self._storage.write_chunks(path, chunks)
        return Err(res.error) if isinstance(res, Err) else Ok(True)


__all__ = ["AtomicFileStorage"]

