"""Pure local retrieval over the cumulative FuncPipe chunk index."""

from __future__ import annotations

import math
from collections.abc import Iterable

from funcpipe_rag.core.rag_types import Chunk
from funcpipe_rag.rag.domain import Embedding, RankedChunk, SearchQuery
from funcpipe_rag.rag.stages import embed_text

LOCAL_EMBEDDING_MODEL = "local-sha256"


def make_query(text: str, *, top_k: int = 3) -> SearchQuery:
    """Embed query text with the same deterministic model used for local chunks."""

    return SearchQuery(
        text=text,
        embedding=Embedding(vector=embed_text(text), model=LOCAL_EMBEDDING_MODEL),
        top_k=top_k,
    )


def cosine_similarity(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    """Return cosine similarity for two finite, non-zero vectors of equal size."""

    if not left or len(left) != len(right):
        raise ValueError("similarity vectors must have the same non-zero dimension")
    if not all(math.isfinite(value) for value in left + right):
        raise ValueError("similarity vectors must contain only finite values")

    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        raise ValueError("similarity vectors must be non-zero")

    score = sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)
    return max(-1.0, min(1.0, score))


def retrieve(query: SearchQuery, chunks: Iterable[Chunk]) -> tuple[RankedChunk, ...]:
    """Rank chunks by score, then by stable document coordinates for equal scores."""

    scored = (
        (cosine_similarity(query.embedding.vector, chunk.embedding), chunk)
        for chunk in chunks
    )
    ordered = sorted(
        scored,
        key=lambda item: (
            -item[0],
            item[1].doc_id,
            item[1].start,
            item[1].end,
            item[1].text,
        ),
    )
    return tuple(
        RankedChunk(chunk=chunk, score=score, rank=rank)
        for rank, (score, chunk) in enumerate(ordered[: query.top_k], start=1)
    )


__all__ = [
    "LOCAL_EMBEDDING_MODEL",
    "cosine_similarity",
    "make_query",
    "retrieve",
]
