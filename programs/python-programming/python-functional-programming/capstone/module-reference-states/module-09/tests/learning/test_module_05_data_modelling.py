from __future__ import annotations

from datetime import datetime

import pytest
from funcpipe_rag.core.rag_types import CleanDoc, RawDoc
from funcpipe_rag.fp.core import (
    UTC,
    ChunkState,
    Done,
    Failure,
    Running,
    Success,
    advance_event,
    chunk_from_dict,
    chunk_state_from_dict,
    chunk_state_to_dict,
    chunk_to_dict,
    failure,
    make_chunk,
    pending,
    start_event,
    succeed_event,
    success,
    transition,
)
from funcpipe_rag.fp.functor import result_map
from funcpipe_rag.fp.validation import (
    Validation,
    VFailure,
    VSuccess,
    v_failure,
    v_liftA2,
    v_success,
)
from funcpipe_rag.rag.stages import clean_doc
from funcpipe_rag.result.types import Err, ErrInfo, Ok
from typing_extensions import assert_never


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


def test_processing_state_allows_only_declared_rag_transitions() -> None:
    queued_at = datetime(2026, 1, 2, 9, tzinfo=UTC)
    initial = pending(queued_at=queued_at)
    running = transition(initial, start_event(started_at=queued_at))
    completed = transition(
        running,
        succeed_event(
            completed_at=datetime(2026, 1, 2, 10, tzinfo=UTC),
            artifact_id="chunk-index",
            dim=2,
            sha256="a" * 64,
        ),
    )

    assert isinstance(running, Running)
    assert isinstance(completed, Done)
    assert transition(completed, advance_event(delta_permille=1)) is completed
    assert initial == pending(queued_at=queued_at)
    with pytest.raises(ValueError, match="invalid transition"):
        transition(initial, advance_event(delta_permille=1))


def test_result_functor_transforms_success_without_running_failure_work() -> None:
    calls: list[str] = []

    def count_words(doc: CleanDoc) -> int:
        calls.append(doc.doc_id)
        return len(doc.abstract.split())

    cleaned = clean_doc(RawDoc("rag-1", "Types", " One  TWO three ", "fp"))
    unavailable = Err(ErrInfo(code="SOURCE_DOWN", msg="read failed", stage="read"))

    assert result_map(count_words)(Ok(cleaned)) == Ok(3)
    assert result_map(count_words)(unavailable) is unavailable
    assert calls == ["rag-1"]


def test_applicative_validation_accumulates_independent_chunk_errors() -> None:
    def title(raw: str) -> Validation[str, str]:
        return v_success(raw) if raw.strip() else v_failure(("title required",))

    def abstract(raw: str) -> Validation[str, str]:
        return v_success(raw) if len(raw.split()) >= 2 else v_failure(("abstract too short",))

    def build(good_title: str, good_abstract: str) -> RawDoc:
        return RawDoc("rag-2", good_title, good_abstract, "fp")

    invalid = v_liftA2(build, title(" "), abstract("brief"))
    valid = v_liftA2(build, title("ADTs"), abstract("typed values"))

    assert invalid == VFailure(("title required", "abstract too short"))
    assert valid == VSuccess(RawDoc("rag-2", "ADTs", "typed values", "fp"))
