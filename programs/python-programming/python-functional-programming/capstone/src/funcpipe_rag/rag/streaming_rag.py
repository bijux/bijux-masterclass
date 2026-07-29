"""Streaming RAG helpers (Module 03+; end-of-Module-09).

These functions keep the core pipeline lazy while optionally fencing work,
grouping by doc, and tracing samples.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import dropwhile, groupby, islice
from operator import attrgetter
from typing import Literal, TypeVar

from funcpipe_rag.core.rag_types import Chunk, ChunkWithoutEmbedding, CleanDoc, RawDoc
from funcpipe_rag.core.rules_pred import eval_pred
from funcpipe_rag.core.structural_dedup import structural_dedup_lazy
from funcpipe_rag.streaming import (
    Source,
    TraceLens,
    ensure_contiguous,
    make_chain,
    make_roundrobin,
    trace_iter,
)

from .chunking import gen_chunk_doc
from .config import RagConfig, RagCoreDeps

T = TypeVar("T")
SourceSchedule = Literal["sequential", "round_robin"]


def gen_grouped_chunks(
    chunks: Iterable[ChunkWithoutEmbedding],
) -> Iterator[tuple[str, Iterator[ChunkWithoutEmbedding]]]:
    """Group contiguous chunk runs by ``doc_id`` (Module 03)."""

    guarded = ensure_contiguous(attrgetter("doc_id"))(chunks)
    yield from groupby(guarded, key=attrgetter("doc_id"))


def stream_chunks(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    trace_docs: TraceLens[RawDoc] | None = None,
    trace_cleaned: TraceLens[CleanDoc] | None = None,
    trace_chunks: TraceLens[ChunkWithoutEmbedding] | None = None,
) -> Iterator[ChunkWithoutEmbedding]:
    """Streaming chunks core: filter → clean → chunk (no embedding, no dedup)."""

    stream: Iterable[RawDoc] = docs
    if trace_docs is not None:
        stream = trace_iter(stream, trace_docs)

    kept = (d for d in stream if eval_pred(d, config.keep.keep_pred))
    cleaned: Iterable[CleanDoc] = (deps.cleaner(d) for d in kept)
    if trace_cleaned is not None:
        cleaned = trace_iter(cleaned, trace_cleaned)

    chunked: Iterable[ChunkWithoutEmbedding] = (c for cd in cleaned for c in gen_chunk_doc(cd, config.env))
    if trace_chunks is not None:
        chunked = trace_iter(chunked, trace_chunks)
    yield from chunked


def gen_stream_embedded(
    chunks: Iterable[ChunkWithoutEmbedding],
    embedder: Callable[[ChunkWithoutEmbedding], Chunk],
    *,
    trace_embedded: TraceLens[Chunk] | None = None,
) -> Iterator[Chunk]:
    """Streaming embedding stage: chunk_without_embedding → chunk."""

    embedded: Iterable[Chunk] = (embedder(c) for c in chunks)
    if trace_embedded is not None:
        embedded = trace_iter(embedded, trace_embedded)
    yield from embedded


def gen_stream_deduped(chunks: Iterable[Chunk]) -> Iterator[Chunk]:
    """Streaming structural dedup stage (order-preserving)."""

    yield from structural_dedup_lazy(chunks)


def stream_rag_chunks(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    max_chunks: int | None = None,
) -> Iterator[Chunk]:
    """Compose the complete lazy RAG path and optionally fence unique outputs."""

    if max_chunks is not None and max_chunks < 0:
        raise ValueError("max_chunks must be >= 0")

    chunked = stream_chunks(docs, config, deps)
    embedded = gen_stream_embedded(chunked, deps.embedder)
    deduped = gen_stream_deduped(embedded)
    if max_chunks is None:
        return deduped
    return islice(deduped, max_chunks)


def stream_rag_sources(
    sources: Sequence[Source[RawDoc]],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    schedule: SourceSchedule = "sequential",
    max_chunks: int | None = None,
) -> Iterator[Chunk]:
    """Merge replayable document sources before running the complete lazy RAG path."""

    if schedule == "sequential":
        merged = make_chain(*sources)
    elif schedule == "round_robin":
        merged = make_roundrobin(*sources)
    else:
        raise ValueError(f"unknown source schedule: {schedule}")
    return stream_rag_chunks(merged(), config, deps, max_chunks=max_chunks)


def gen_bounded_chunks(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    max_chunks: int | None = None,
) -> Iterator[ChunkWithoutEmbedding]:
    """Hard fence on the number of chunks produced (Module 03)."""

    chunked = stream_chunks(docs, config, deps)
    if max_chunks is None:
        yield from chunked
        return
    yield from islice(chunked, max_chunks)


def safe_rag_pipeline(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    max_chunks: int = 10_000,
    min_doc_len: int = 500,
) -> Iterator[ChunkWithoutEmbedding]:
    """Defensive streaming pipeline with explicit fences (Module 03)."""

    fenced_docs = dropwhile(lambda d: len(d.abstract) < min_doc_len, docs)
    yield from gen_bounded_chunks(fenced_docs, config, deps, max_chunks=max_chunks)


__all__ = [
    "SourceSchedule",
    "gen_bounded_chunks",
    "gen_grouped_chunks",
    "gen_stream_deduped",
    "gen_stream_embedded",
    "safe_rag_pipeline",
    "stream_chunks",
    "stream_rag_chunks",
    "stream_rag_sources",
]
