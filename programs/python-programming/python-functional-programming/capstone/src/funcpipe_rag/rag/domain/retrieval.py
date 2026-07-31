"""Module 05 values that make query and ranking states explicit."""

from __future__ import annotations

import math
from dataclasses import dataclass

from funcpipe_rag.core.rag_types import Chunk as IndexedChunk

from .embedding import Embedding


@dataclass(frozen=True, slots=True)
class SearchQuery:
    """A legal retrieval request after query embedding."""

    text: str
    embedding: Embedding
    top_k: int

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("SearchQuery.text must not be blank")
        if type(self.top_k) is not int or self.top_k < 1:
            raise ValueError("SearchQuery.top_k must be a positive integer")
        if self.embedding.dim < 1:
            raise ValueError("SearchQuery.embedding must not be empty")


@dataclass(frozen=True, slots=True)
class RankedChunk:
    """An indexed chunk plus its stable position and similarity score."""

    chunk: IndexedChunk
    score: float
    rank: int

    def __post_init__(self) -> None:
        if not math.isfinite(self.score) or not -1.0 <= self.score <= 1.0:
            raise ValueError("RankedChunk.score must be finite and between -1 and 1")
        if type(self.rank) is not int or self.rank < 1:
            raise ValueError("RankedChunk.rank must be a positive integer")


__all__ = ["RankedChunk", "SearchQuery"]
