"""Final pure RAG pipeline implementations – end of Module 01.

This file contains:
- Legacy impure implementations (preserved only for equivalence testing)
- The canonical pure pipeline using explicit, composable stages
- A deliberate absence of a global point-free version

Everything here is referentially transparent, deterministic, and canonical.
The output of `full_rag` is fully independent of input document order.
"""

from __future__ import annotations

from typing import TypedDict

from funcpipe_rag.pipeline_stages import (
    clean_doc,
    chunk_doc,
    embed_chunk,
    structural_dedup_chunks,
)
from funcpipe_rag.rag_types import RawDoc, Chunk, RagEnv


# --------------------------------------------------------------------------- #
# Legacy impure implementations – kept only for teaching and testing
# --------------------------------------------------------------------------- #

class LegacyEmbeddedChunk(TypedDict):
    """Shape used in the original imperative script."""
    doc_id: str        # includes offset suffix, e.g. "arxiv:1234_512"
    text: str
    embedding: tuple[float, ...]


class LegacyChunkMetadata(TypedDict):
    """Metadata-only shape used in early refactor equivalence tests."""
    doc_id: str
    text: str
    start: int
    end: int


def impure_full_rag(docs: list[RawDoc], env: RagEnv) -> list[LegacyEmbeddedChunk]:
    """Original monolithic antipattern – dictionary-based, derived IDs."""
    import hashlib

    result: list[LegacyEmbeddedChunk] = []
    for doc in docs:
        text = " ".join(doc.abstract.strip().lower().split())
        for i in range(0, len(text), env.chunk_size):
            chunk_text = text[i:i + env.chunk_size]
            h = hashlib.sha256(chunk_text.encode()).hexdigest()
            step = 4
            vec = tuple(int(h[j:j + step], 16) / (16**step - 1) for j in range(0, 64, step))
            result.append({
                "doc_id": f"{doc.doc_id}_{i}",
                "text": chunk_text,
                "embedding": vec,
            })
    return result


def impure_chunks(docs: list[RawDoc], env: RagEnv) -> list[LegacyChunkMetadata]:
    """Legacy chunking logic – returns only metadata (no embedding)."""
    result: list[LegacyChunkMetadata] = []
    for doc in docs:
        text = " ".join(doc.abstract.strip().lower().split())
        for i in range(0, len(text), env.chunk_size):
            result.append({
                "doc_id": doc.doc_id,
                "text": text[i:i + env.chunk_size],
                "start": i,
                "end": i + len(text[i:i + env.chunk_size]),
            })
    return result


# --------------------------------------------------------------------------- #
# Final pure pipeline – explicit, readable, canonical
# --------------------------------------------------------------------------- #

def docs_to_embedded(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    """Clean → chunk → embed, returning a flat list of embedded chunks."""
    cleaned = [clean_doc(doc) for doc in docs]
    chunked = [c for doc in cleaned for c in chunk_doc(doc, env)]
    embedded = [embed_chunk(c) for c in chunked]
    return embedded


def full_rag(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    """The definitive, canonical RAG pipeline at the end of Module 01.

    Properties:
    - Pure and referentially transparent
    - Output order depends only on (doc_id, start), not input order
    - `full_rag(full_rag(x)) == full_rag(x)` (idempotent)
    - Fixed point reached in a single pass
    """
    return structural_dedup_chunks(docs_to_embedded(docs, env))


# --------------------------------------------------------------------------- #
# Point-free composition – intentionally omitted in Module 01
# --------------------------------------------------------------------------- #
#
# A global `full_rag_point_free(docs, env)` is awkward with `flow` alone
# because `chunk_doc` needs `env`. We could cheat with closures/partial, but
# both are introduced in later modules.
#
# The absence of a point-free variant is deliberate: explicit parameters are
# perfectly acceptable, and often clearer. The canonical reference for Module 01
# is `full_rag(docs, env)`; `RagPipe` shows the same idea in OO style.
