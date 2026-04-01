"""Pure, composable pipeline stages for the FuncPipe RAG implementation.

End-of-Module-02 codebase: these stages are the stable, deterministic core used
by the higher-level APIs (configs, rules, taps/probes, boundary shells).
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


def iter_chunk_doc(doc: CleanDoc, env: RagEnv) -> Iterator[ChunkWithoutEmbedding]:
    """Yield chunks lazily from a cleaned document."""

    text = doc.abstract
    for start in range(0, len(text), env.chunk_size):
        piece = text[start : start + env.chunk_size]
        if piece:
            yield ChunkWithoutEmbedding(
                doc_id=doc.doc_id,
                text=piece,
                start=start,
                end=start + len(piece),
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
    seen: set[tuple[str, str, int, int]] = set()
    result: list[Chunk] = []

    for chunk in sorted(chunks, key=lambda c: (c.doc_id, c.start)):
        key = (chunk.doc_id, chunk.text, chunk.start, chunk.end)
        if key not in seen:
            seen.add(key)
            result.append(chunk)

    return result
