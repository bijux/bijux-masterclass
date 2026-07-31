"""Bounded asynchronous coordination for the FuncPipe indexing path."""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from typing import TypeAlias

from funcpipe_rag.core.rag_types import (
    Chunk,
    ChunkWithoutEmbedding,
    CleanDoc,
    DocRule,
    RagEnv,
    RawDoc,
)
from funcpipe_rag.domain.effects.async_ import (
    AsyncGen,
    AsyncPlan,
    BackpressurePolicy,
    async_gen_and_then,
    async_gen_bounded_map,
)
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result

from .chunking import gen_chunk_doc

AsyncChunkEmbedder: TypeAlias = Callable[[ChunkWithoutEmbedding], AsyncPlan[Chunk]]


def async_rag_chunks(
    docs: AsyncGen[RawDoc],
    env: RagEnv,
    cleaner: Callable[[RawDoc], CleanDoc],
    embedder: AsyncChunkEmbedder,
    policy: BackpressurePolicy,
    *,
    keep: DocRule | None = None,
) -> AsyncGen[Chunk]:
    """Describe filter-clean-chunk-embed with bounded asynchronous embedding.

    Document preparation remains synchronous and demand-driven. Only the
    injected embedding plan is scheduled concurrently. Source and preparation
    validation failures stay in the stream as ``Err`` values.
    """

    def prepare_document(doc: RawDoc) -> AsyncGen[ChunkWithoutEmbedding]:
        async def generate() -> AsyncIterator[Result[ChunkWithoutEmbedding, ErrInfo]]:
            try:
                if keep is not None and not keep(doc):
                    return
                cleaned = cleaner(doc)
                for chunk in gen_chunk_doc(cleaned, env):
                    yield Ok(chunk)
            except (TypeError, ValueError) as exc:
                yield Err(ErrInfo.from_exception(exc))

        return generate

    prepared = async_gen_and_then(docs, prepare_document)
    return async_gen_bounded_map(prepared, embedder, policy)


__all__ = ["AsyncChunkEmbedder", "async_rag_chunks"]
