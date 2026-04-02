"""Immutable value types for the FuncPipe RAG pipeline.

All types are frozen dataclasses → instances are values:
- They are hashable when `eq=True` (only Chunk needs it for deduplication)
- They support structural equality
- They are safe to use in sets, as dict keys, or inside other frozen dataclasses
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class RawDoc:
    """Raw document as read from the source dataset (CSV row).

    No normalisation has been applied yet – this is the exact input shape.
    """

    doc_id: str
    title: str
    abstract: str
    categories: str


DocRule = Callable[[RawDoc], bool]


@dataclass(frozen=True)
class CleanDoc:
    """Document after deterministic text normalisation.

    The only field that changes is `abstract` (whitespace collapsed,
    lower-cased, and stripped).  All other fields are carried unchanged.
    """

    doc_id: str
    title: str
    abstract: str          # normalised whitespace, lower-cased
    categories: str


@dataclass(frozen=True)
class ChunkWithoutEmbedding:
    """A slice of a CleanDoc's abstract before embedding.

    Offsets (`start`, `end`) are character indices into `CleanDoc.abstract`.
    """

    doc_id: str
    text: str              # the actual slice of the abstract
    start: int             # inclusive start offset in the original abstract
    end: int               # exclusive end offset in the original abstract


@dataclass(frozen=True, eq=True)
class Chunk(ChunkWithoutEmbedding):
    """Final chunk with a deterministic embedding vector.

    `eq=True` is required so that two chunks with identical content
    (doc_id, text, start, end, embedding) are considered equal and can
    be deduplicated with a simple `set` or the canonical `structural_dedup_chunks`.
    """

    embedding: tuple[float, ...]   # fixed length 16, each value in [0.0, 1.0]


@dataclass(frozen=True)
class RagEnv:
    """Immutable configuration for a single pipeline run."""

    chunk_size: int
    sample_size: int = 5

    def __post_init__(self) -> None:
        if self.chunk_size <= 0:
            raise ValueError("RagEnv.chunk_size must be a positive integer")
        if self.sample_size <= 0:
            raise ValueError("RagEnv.sample_size must be a positive integer")
