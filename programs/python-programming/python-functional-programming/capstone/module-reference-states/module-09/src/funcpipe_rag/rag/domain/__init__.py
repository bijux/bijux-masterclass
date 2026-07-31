"""Module 05: compositional domain-modeling helpers (end-of-Module-09).

These ADTs are used in the Module 05 "type-driven design" cores:
- independent, immutable subsystem records (`ChunkText`, `ChunkMetadata`, `Embedding`)
- safe assembly into a coherent `Chunk` via applicative `Validation`
- an optional NumPy hybrid path with equivalence tests

This modeling layer is intentionally separate from the main RAG pipeline value
types in `funcpipe_rag.core.rag_types`.
"""

from .chunk import (
    Chunk,
    ChunkId,
    ChunkMetadataV1,
    assemble,
    map_metadata_checked,
    try_set_embedding,
    upcast_metadata_v1,
)
from .embedding import Embedding
from .metadata import ChunkMetadata
from .perf import OBatch, from_optimized_batch, process_batch_hybrid, to_optimized_batch
from .text import ChunkText

__all__ = [
    "ChunkId",
    "ChunkText",
    "ChunkMetadata",
    "Embedding",
    "Chunk",
    "assemble",
    "try_set_embedding",
    "map_metadata_checked",
    "ChunkMetadataV1",
    "upcast_metadata_v1",
    "OBatch",
    "to_optimized_batch",
    "from_optimized_batch",
    "process_batch_hybrid",
]
