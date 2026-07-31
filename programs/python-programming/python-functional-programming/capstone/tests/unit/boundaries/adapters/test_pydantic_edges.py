from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from funcpipe_rag.boundaries.adapters.pydantic_edges import (
    ChunkModel,
    deserialize_model,
    serialize_model,
)

nonfinite = st.sampled_from([float("nan"), float("inf"), float("-inf")])


@given(
    text=st.text(min_size=1, max_size=1000),
    metadata=st.dictionaries(st.text(), st.integers() | st.text(), max_size=20),
)
def test_chunk_roundtrip(text: str, metadata: dict[str, object]) -> None:
    model = ChunkModel(
        doc_id="doc",
        text=text,
        start=3,
        end=3 + len(text),
        metadata=metadata,  # type: ignore[arg-type]
        embedding=(0.0,) * 16,
    )
    json_str = serialize_model(model)
    assert '"version":1' in json_str
    reloaded = deserialize_model(json_str, ChunkModel)
    assert model == reloaded
    assert reloaded.length == len(text)


@given(bad_value=nonfinite)
def test_nonfinite_embedding_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError):
        ChunkModel(
            doc_id="doc",
            text="x",
            start=0,
            end=1,
            embedding=(bad_value,) + (0.0,) * 15,
        )


@given(size=st.integers(min_value=0, max_value=32).filter(lambda size: size != 16))
def test_wrong_embedding_dimension_rejected(size: int) -> None:
    with pytest.raises(ValueError):
        ChunkModel(doc_id="doc", text="x", start=0, end=1, embedding=(0.0,) * size)


def test_schema_stable(snapshot) -> None:
    assert ChunkModel.model_json_schema() == snapshot
