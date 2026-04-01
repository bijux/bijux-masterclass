"""funcpipe_rag – Pure, canonical RAG pipeline (end of Module 01).

This package is the final state of Module 01: immutable domain types,
a pure canonical RAG pipeline, and a single thin I/O shell.

Key properties:
- All domain types are frozen dataclasses
- Core pipeline is pure and referentially transparent
- Side effects are isolated in a single shell function
- Composition is explicit via small, testable functions
- Output is canonical (independent of input order)
"""

from __future__ import annotations

# Domain value types – immutable, hashable where needed
from .rag_types import (
    RawDoc,
    CleanDoc,
    ChunkWithoutEmbedding,
    Chunk,
    RagEnv,
)

# Pure pipeline stages – the building blocks
from .pipeline_stages import (
    clean_doc,
    chunk_doc,
    embed_chunk,
    structural_dedup_chunks,
)

# Higher-order helpers – the functional toolkit of Module 01
from .fp import identity, flow, fmap

# Fluent OO composition alternative
from .rag_pipe import RagPipe

# Final canonical pipeline
from .full_rag import (
    full_rag,
    docs_to_embedded,
    impure_full_rag,      # legacy – kept for equivalence tests
    impure_chunks,        # legacy – kept for refactor proofs
)

# The one and only impure shell
from .rag_shell import rag_shell


__all__ = [
    # Types
    "RawDoc",
    "CleanDoc",
    "ChunkWithoutEmbedding",
    "Chunk",
    "RagEnv",

    # Pure stages
    "clean_doc",
    "chunk_doc",
    "embed_chunk",
    "structural_dedup_chunks",

    # Functional composition
    "identity",
    "flow",
    "fmap",
    "RagPipe",

    # Final pipeline
    "full_rag",
    "docs_to_embedded",

    # Legacy (only for teaching/tests)
    "impure_full_rag",
    "impure_chunks",

    # Shell
    "rag_shell",
]

__version__ = "0.1.0"