"""Core domain value types for FuncPipe RAG (end-of-Module-09).

All types are frozen dataclasses → instances are values:
- They support structural equality.
- They are safe to use as dict keys (only `Chunk` opts into `eq=True` for dedup).
- They are safe to share across pure pipeline stages and lazy iterators.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

TailPolicy = str


@dataclass(frozen=True)
class RawDoc:
    """Raw document as read from the source dataset (CSV row)."""

    doc_id: str
    title: str
    abstract: str
    categories: str


DocRule = Callable[[RawDoc], bool]


@dataclass(frozen=True)
class CleanDoc:
    """Document after deterministic text normalisation."""

    doc_id: str
    title: str
    abstract: str
    categories: str


@dataclass(frozen=True)
class ChunkWithoutEmbedding:
    """A slice of a CleanDoc's abstract before embedding."""

    doc_id: str
    text: str
    start: int
    end: int
    metadata: Mapping[str, object] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.start, int) or not isinstance(self.end, int):
            raise ValueError("Chunk offsets must be integers")
        if self.start < 0:
            raise ValueError("Chunk.start must be >= 0")
        if self.end < self.start:
            raise ValueError("Chunk.end must be >= start")
        if not isinstance(self.metadata, Mapping):
            raise ValueError("Chunk.metadata must be a mapping")
        if isinstance(self.metadata, dict):
            object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, eq=True)
class Chunk(ChunkWithoutEmbedding):
    """Final chunk with a deterministic embedding vector."""

    embedding: tuple[float, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if len(self.embedding) != 16:
            raise ValueError("Chunk.embedding must be a 16-dimensional tuple[float, ...]")


@dataclass(frozen=True)
class RagEnv:
    """Immutable configuration for a single pipeline run."""

    chunk_size: int
    sample_size: int = 5
    overlap: int = 0
    tail_policy: TailPolicy = "emit_short"

    def __post_init__(self) -> None:
        if not isinstance(self.chunk_size, int):
            raise ValueError("RagEnv.chunk_size must be an int")
        if self.chunk_size <= 0:
            raise ValueError("RagEnv.chunk_size must be a positive integer")
        if not isinstance(self.sample_size, int):
            raise ValueError("RagEnv.sample_size must be an int")
        if self.sample_size <= 0:
            raise ValueError("RagEnv.sample_size must be a positive integer")
        if not isinstance(self.overlap, int):
            raise ValueError("RagEnv.overlap must be an int")
        if not 0 <= self.overlap < self.chunk_size:
            raise ValueError("RagEnv.overlap must satisfy 0 <= overlap < chunk_size")
        if self.tail_policy not in {"emit_short", "drop", "pad"}:
            raise ValueError('RagEnv.tail_policy must be one of: "emit_short", "drop", "pad"')


@dataclass(frozen=True)
class TextNode:
    """A single text-bearing node in a document hierarchy (Module 04)."""

    text: str
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, Mapping):
            raise ValueError("TextNode.metadata must be a mapping")
        if isinstance(self.metadata, dict):
            object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class TreeDoc:
    """Immutable, recursive document structure (Module 04)."""

    node: TextNode
    children: tuple["TreeDoc", ...] = ()


__all__ = [
    "RawDoc",
    "DocRule",
    "CleanDoc",
    "ChunkWithoutEmbedding",
    "Chunk",
    "TailPolicy",
    "RagEnv",
    "TextNode",
    "TreeDoc",
]
