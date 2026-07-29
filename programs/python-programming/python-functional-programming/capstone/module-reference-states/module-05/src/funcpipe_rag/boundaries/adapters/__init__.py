"""Reusable adapters for external data entering or leaving FuncPipe."""

from .pydantic_edges import (
    ChunkModel,
    deserialize_model,
    from_core_chunk,
    serialize_model,
    to_core_chunk,
)

__all__ = [
    "ChunkModel",
    "deserialize_model",
    "from_core_chunk",
    "serialize_model",
    "to_core_chunk",
]
