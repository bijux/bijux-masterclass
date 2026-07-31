"""Reusable adapters for external data entering or leaving FuncPipe."""

from .pydantic_edges import (
    ChunkModel,
    deserialize_model,
    from_core_chunk,
    serialize_model,
    to_core_chunk,
)
from .serde import Envelope, from_json, to_json

__all__ = [
    "ChunkModel",
    "Envelope",
    "deserialize_model",
    "from_json",
    "from_core_chunk",
    "serialize_model",
    "to_core_chunk",
    "to_json",
]
