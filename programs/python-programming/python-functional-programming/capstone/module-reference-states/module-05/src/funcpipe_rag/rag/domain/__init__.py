"""Composable RAG domain values introduced in Module 05."""

from .chunk import (
    AssembledChunk,
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
    "AssembledChunk",
    "ChunkId",
    "ChunkMetadata",
    "ChunkMetadataV1",
    "ChunkText",
    "Embedding",
    "OBatch",
    "assemble",
    "from_optimized_batch",
    "map_metadata_checked",
    "process_batch_hybrid",
    "to_optimized_batch",
    "try_set_embedding",
    "upcast_metadata_v1",
]
