"""Module 07 infra: in-memory storage adapter (test double)."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator

from funcpipe_rag.core.rag_types import Chunk, RawDoc
from funcpipe_rag.domain.capabilities import Storage
from funcpipe_rag.result.types import ErrInfo, Ok, Result


class InMemoryStorage(Storage):
    def __init__(self, *, preload: dict[str, list[RawDoc]] | None = None) -> None:
        self.docs: dict[str, list[RawDoc]] = dict(preload or {})
        self.written: dict[str, list[Chunk]] = defaultdict(list)

    def read_docs(self, path: str) -> Iterator[Result[RawDoc, ErrInfo]]:
        for doc in self.docs.get(path, []):
            yield Ok(doc)

    def write_chunks(self, path: str, chunks: Iterator[Chunk]) -> Result[None, ErrInfo]:
        self.written[path].extend(list(chunks))
        return Ok(None)


__all__ = ["InMemoryStorage"]

