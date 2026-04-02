"""Module 05 subsystem ADT: chunk metadata (end-of-Module-08; domain-modeling)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChunkMetadata:
    source: str
    tags: tuple[str, ...]
    embedding_model: str | None = None
    expected_dim: int | None = None


__all__ = ["ChunkMetadata"]
