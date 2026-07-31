"""Module 05 Pydantic-at-the-edges models and codecs (end-of-Module-08; adapters)."""

from __future__ import annotations

import math
from typing import Any, Literal, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    computed_field,
    model_validator,
)

from funcpipe_rag.core.rag_types import Chunk

T = TypeVar("T")

StrictConfig = ConfigDict(
    strict=True,
    frozen=True,
    extra="forbid",
    populate_by_name=True,
)


class ChunkModel(BaseModel):
    model_config = StrictConfig

    version: Literal[1] = 1
    doc_id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=200_000)
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: tuple[float, ...]

    @model_validator(mode="after")
    def _validate_chunk(self) -> ChunkModel:
        if self.end - self.start != len(self.text):
            raise ValueError("offset span must equal text length")
        if len(self.embedding) != 16:
            raise ValueError("embedding must contain 16 values")
        for i, v in enumerate(self.embedding):
            if not math.isfinite(v):
                raise ValueError(f"embedding[{i}] not finite")
        return self

    @computed_field
    def length(self) -> int:
        return len(self.text)


def to_core_chunk(model: ChunkModel) -> Chunk:
    return Chunk(
        doc_id=model.doc_id,
        text=model.text,
        start=model.start,
        end=model.end,
        metadata=model.metadata,
        embedding=model.embedding,
    )


def from_core_chunk(core: Chunk) -> ChunkModel:
    return ChunkModel(
        doc_id=core.doc_id,
        text=core.text,
        start=core.start,
        end=core.end,
        metadata=dict(core.metadata),
        embedding=core.embedding,
    )


def serialize_model(model: BaseModel) -> str:
    computed = getattr(model.__class__, "model_computed_fields", {})
    exclude = set(computed.keys()) if isinstance(computed, dict) else set()
    return model.model_dump_json(by_alias=True, exclude_unset=True, exclude=exclude)


def deserialize_model(json_str: str, typ: type[T]) -> T:
    return TypeAdapter(typ).validate_json(json_str)


__all__ = [
    "ChunkModel",
    "deserialize_model",
    "from_core_chunk",
    "serialize_model",
    "to_core_chunk",
]
