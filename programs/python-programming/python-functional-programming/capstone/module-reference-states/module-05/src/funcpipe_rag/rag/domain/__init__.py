"""Composable RAG domain values introduced in Module 05."""

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
from .text import ChunkText

__all__ = [
    "Chunk",
    "ChunkId",
    "ChunkMetadata",
    "ChunkMetadataV1",
    "ChunkText",
    "Embedding",
    "assemble",
    "map_metadata_checked",
    "try_set_embedding",
    "upcast_metadata_v1",
]
