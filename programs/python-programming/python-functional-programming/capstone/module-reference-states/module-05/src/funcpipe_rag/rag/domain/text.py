"""Module 05 subsystem ADT: chunk text."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChunkText:
    content: str


__all__ = ["ChunkText"]
