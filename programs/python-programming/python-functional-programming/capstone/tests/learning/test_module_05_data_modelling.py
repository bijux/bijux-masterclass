from __future__ import annotations

from typing_extensions import assert_never

from funcpipe_rag.fp.core import (
    ChunkState,
    Failure,
    Success,
    chunk_from_dict,
    chunk_state_from_dict,
    chunk_state_to_dict,
    chunk_to_dict,
    failure,
    make_chunk,
    success,
)


def describe_chunk_outcome(state: ChunkState) -> str:
    match state:
        case Success(embedding=embedding):
            return f"ready:{len(embedding)}"
        case Failure(code=code, attempt=attempt):
            return f"failed:{code}:attempt-{attempt}"
        case other:
            assert_never(other)


def test_product_and_sum_types_make_chunk_outcomes_explicit() -> None:
    prepared = make_chunk(
        text="typed values",
        path=(0, 2),
        metadata={"source": "guide", "reviewed": True},
    )
    ready = success(embedding=(0.25, 0.75), metadata={"model": "local"})
    rejected = failure(code="EMBED_FAIL", msg="model unavailable", attempt=2)

    assert chunk_from_dict(chunk_to_dict(prepared)) == prepared
    assert chunk_state_from_dict(chunk_state_to_dict(ready)) == ready
    assert chunk_state_from_dict(chunk_state_to_dict(rejected)) == rejected
    assert [describe_chunk_outcome(state) for state in (ready, rejected)] == [
        "ready:2",
        "failed:EMBED_FAIL:attempt-2",
    ]
