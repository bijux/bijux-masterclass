"""Pure, composable pipeline stages for the FuncPipe RAG implementation.

End-of-Module-03 codebase: these stages remain the stable, deterministic core
used by the higher-level APIs (configs, rules, taps/probes, boundary shells),
with Module 03 extending chunking with overlap and tail policies.
"""

from __future__ import annotations

import hashlib

from collections.abc import Iterable, Iterator

from funcpipe_rag.rag_types import (
    RawDoc,
    CleanDoc,
    ChunkWithoutEmbedding,
    Chunk,
    RagEnv,
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
    """Split a cleaned document into fixed-size, non-overlapping chunks.

    The result is order-preserving and covers the entire abstract without gaps
    or overlaps (except possibly a shorter final chunk).
    """
    return list(iter_chunk_doc(doc, env))


def iter_overlapping_chunks_text(
    doc_id: str,
    text: str,
    *,
    k: int,
    o: int = 0,
    tail_policy: str = "emit_short",
) -> Iterator[ChunkWithoutEmbedding]:
    """Yield fixed-size chunks from raw text, with optional overlap and tail policy.

    Args:
        doc_id: Identifier to attach to each chunk.
        text: Indexable string.
        k: Chunk size (> 0).
        o: Overlap size (0 <= o < k). Step = k - o.
        tail_policy:
            - "emit_short": emit a final shorter chunk if needed
            - "drop": drop a final shorter tail
            - "pad": right-pad final chunk with NUL ("\\0") to length k, and set end=i+k
              (note: end may exceed len(text) under "pad")
    """

    # Module 03 extension: with the default settings (o=0, tail_policy="emit_short"),
    # this is equivalent to the Module 01/02 non-overlapping chunking semantics.

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
            yield ChunkWithoutEmbedding(doc_id=doc_id, text=segment, start=i, end=j if tail_policy == "pad" else i + len(segment))
        i += step


def iter_chunk_spans(doc: CleanDoc, env: RagEnv) -> Iterator[tuple[int, int]]:
    """Yield (start, end) chunk spans for a document.

    Spans follow the same overlap/tail_policy semantics as ``iter_chunk_doc``.
    """

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
    """Produce a deterministic 16-dimensional embedding from chunk text.

    The embedding depends only on ``chunk.text`` and is stable across runs.
    """
    digest = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    step = 4
    vector = tuple(
        int(digest[i: i + step], 16) / (16 ** step - 1)
        for i in range(0, len(digest), step)
    )[:16]  # first 16 components of the SHA256-derived vector
    return Chunk(
        doc_id=chunk.doc_id,
        text=chunk.text,
        start=chunk.start,
        end=chunk.end,
        embedding=vector,
    )


def structural_dedup_chunks(chunks: Iterable[Chunk]) -> list[Chunk]:
    """Canonical deduplication: sort by (doc_id, start) then remove structural duplicates.

    This function is:
    - Idempotent: f(f(x)) == f(x)
    - Canonical: output depends only on the set of unique chunks, not input order
    - Convergent: one pass reaches the fixed point

    """
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
