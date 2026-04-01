"""Pure, composable RAG pipeline stages (end-of-Module-05).

These stages are deterministic and side-effect free. Higher-level APIs wire
them together with configuration-as-data, taps/probes, and boundary adapters.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Iterator

from funcpipe_rag.core.rag_types import (
    Chunk,
    ChunkWithoutEmbedding,
    CleanDoc,
    RagEnv,
    RawDoc,
)
from funcpipe_rag.core.structural_dedup import structural_dedup_lazy


def clean_doc(doc: RawDoc) -> CleanDoc:
    """Deterministically normalise whitespace and case in the abstract."""

    abstract = " ".join(doc.abstract.strip().lower().split())
    return CleanDoc(
        doc_id=doc.doc_id,
        title=doc.title,
        abstract=abstract,
        categories=doc.categories,
    )


def chunk_doc(doc: CleanDoc, env: RagEnv) -> list[ChunkWithoutEmbedding]:
    """Split a cleaned document into chunks (eager convenience wrapper)."""

    return list(iter_chunk_doc(doc, env))


def iter_overlapping_chunks_text(
    doc_id: str,
    text: str,
    *,
    k: int,
    o: int = 0,
    tail_policy: str = "emit_short",
) -> Iterator[ChunkWithoutEmbedding]:
    """Yield fixed-size chunks from raw text, with optional overlap and tail policy."""

    if k <= 0 or not 0 <= o < k:
        raise ValueError("invalid chunk/overlap")
    if tail_policy not in {"emit_short", "drop", "pad"}:
        raise ValueError('tail_policy must be one of: "emit_short", "drop", "pad"')

    step = k - o
    n = len(text)
    i = 0
    while i < n:
        j = i + k
        short_tail = j > n
        if short_tail and tail_policy == "drop":
            break

        segment = text[i:j]
        if short_tail and tail_policy == "pad":
            segment = segment + "\0" * (k - len(segment))
            j = i + k

        if segment:
            end = j if tail_policy == "pad" else i + len(segment)
            yield ChunkWithoutEmbedding(doc_id=doc_id, text=segment, start=i, end=end)
        i += step


def iter_chunk_spans(doc: CleanDoc, env: RagEnv) -> Iterator[tuple[int, int]]:
    """Yield (start, end) chunk spans for a document."""

    k = env.chunk_size
    o = env.overlap
    tail_policy = env.tail_policy
    if k <= 0 or not 0 <= o < k:
        raise ValueError("invalid chunk/overlap")

    step = k - o
    n = len(doc.abstract)
    i = 0
    while i < n:
        j = i + k
        if j > n and tail_policy == "drop":
            break
        yield (i, j if tail_policy == "pad" else min(j, n))
        i += step


def iter_chunk_doc(doc: CleanDoc, env: RagEnv) -> Iterator[ChunkWithoutEmbedding]:
    """Yield chunks lazily from a cleaned document."""

    yield from iter_overlapping_chunks_text(
        doc_id=doc.doc_id,
        text=doc.abstract,
        k=env.chunk_size,
        o=env.overlap,
        tail_policy=env.tail_policy,
    )


def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    """Produce a deterministic 16-dimensional embedding from chunk text."""

    digest = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vector = tuple(int(digest[i : i + step], 16) / (16**step - 1) for i in range(0, len(digest), step))[:16]
    return Chunk(
        doc_id=chunk.doc_id,
        text=chunk.text,
        start=chunk.start,
        end=chunk.end,
        metadata=chunk.metadata,
        embedding=vector,
    )


def structural_dedup_chunks(chunks: Iterable[Chunk]) -> list[Chunk]:
    """Canonical deduplication: sort by (doc_id, start) then remove duplicates."""

    ordered = sorted(chunks, key=lambda c: (c.doc_id, c.start))
    return list(structural_dedup_lazy(ordered))


__all__ = [
    "clean_doc",
    "chunk_doc",
    "iter_chunk_spans",
    "iter_overlapping_chunks_text",
    "iter_chunk_doc",
    "embed_chunk",
    "structural_dedup_chunks",
]

