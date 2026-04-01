"""Public API types introduced in Module 02."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from funcpipe_rag.rag_types import Chunk, CleanDoc, RawDoc, DocRule

TapDocs = Callable[[tuple[RawDoc, ...]], None]
TapCleaned = Callable[[tuple[CleanDoc, ...]], None]
TapChunks = Callable[[tuple[Chunk, ...]], None]
TapAny = Callable[[tuple[Any, ...]], None]


@dataclass(frozen=True)
class RagTaps:
    """Observation-only hooks for intermediate values.

    Tap handlers must be observational only: they may log or collect metrics,
    but must not mutate inputs or influence returned values.
    """

    docs: TapDocs | None = None
    cleaned: TapCleaned | None = None
    chunks: TapChunks | None = None
    extra: Mapping[str, TapAny] = field(default_factory=dict)


@dataclass(frozen=True)
class DebugConfig:
    trace_docs: bool = False
    trace_kept: bool = False
    trace_clean: bool = False
    trace_chunks: bool = False
    trace_embedded: bool = False
    probe_chunks: bool = False


@dataclass(frozen=True)
class Observations:
    """Deterministic summary for a RAG invocation (end-of-Module 02)."""

    total_docs: int
    total_chunks: int
    kept_docs: int | None = None
    cleaned_docs: int | None = None
    sample_doc_ids: tuple[str, ...] = ()
    sample_chunk_starts: tuple[int, ...] = ()
    extra: tuple[Any, ...] = ()
    warnings: tuple[Any, ...] = ()


__all__ = ["DocRule", "RagTaps", "DebugConfig", "Observations"]
