"""Pure, composable pipeline stages for the FuncPipe RAG implementation.

Every function in this module is:
- Pure (same inputs → same outputs, no side effects)
- Total (always returns a value, never raises for valid input)
- Referentially transparent
- Designed to be composed with ``fmap``, ``flow``, or ``RagPipe``

This file represents the final state of Module 01: the pipeline is not just pure,
it is **canonical** — repeated application yields a fixed point in one pass.
"""

from __future__ import annotations

import hashlib

from funcpipe_rag.rag_types import (
    RawDoc,
    CleanDoc,
    ChunkWithoutEmbedding,
    Chunk,
    RagEnv,
)


def clean_doc(doc: RawDoc) -> CleanDoc:
    """Deterministically normalise whitespace and case in the abstract.

    The transformation is idempotent: ``clean_doc(clean_doc(doc)) == clean_doc(doc)``.
    """
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
    text = doc.abstract
    return [
        ChunkWithoutEmbedding(
            doc_id=doc.doc_id,
            text=text[i : i + env.chunk_size],
            start=i,
            end=i + len(text[i : i + env.chunk_size]),
        )
        for i in range(0, len(text), env.chunk_size)
    ]


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


def structural_dedup_chunks(chunks: list[Chunk]) -> list[Chunk]:
    """Canonical deduplication: sort by (doc_id, start) then remove structural duplicates.

    This function is:
    - Idempotent: f(f(x)) == f(x)
    - Canonical: output depends only on the set of unique chunks, not input order
    - Convergent: one pass reaches the fixed point

    This is the final lesson of Module 01 – stability under repeated application.
    """
    seen: set[tuple[str, str, int, int]] = set()
    result: list[Chunk] = []

    for chunk in sorted(chunks, key=lambda c: (c.doc_id, c.start)):
        key = (chunk.doc_id, chunk.text, chunk.start, chunk.end)
        if key not in seen:
            seen.add(key)
            result.append(chunk)

    return result


# --------------------------------------------------------------------------- #
# Legacy / pedagogical variants – kept only for teaching, not used in production
# --------------------------------------------------------------------------- #

# These are intentionally left here with clear deprecation notices.
# They exist so students can import and compare against the final versions above.

def _legacy_order_preserving_dedup(chunks: list[Chunk]) -> list[Chunk]:
    """Old version – preserved only for equivalence tests."""
    seen = set()
    result = []
    for c in chunks:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return result