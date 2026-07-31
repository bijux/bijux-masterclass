from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict

import pytest
from pydantic import ValidationError
from typing_extensions import assert_never

from funcpipe_rag.boundaries.adapters.pydantic_edges import ChunkModel, to_core_chunk
from funcpipe_rag.boundaries.adapters.serde import (
    dec_result,
    enc_result,
    from_json,
    to_json,
)
from funcpipe_rag.core.rag_types import CleanDoc, RawDoc
from funcpipe_rag.fp.core import (
    JSON,
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
from funcpipe_rag.fp.error import ErrorCode
from funcpipe_rag.fp.functor import result_map
from funcpipe_rag.fp.monoid import METRICS, Metrics, fold
from funcpipe_rag.fp.validation import (
    Validation,
    VFailure,
    VSuccess,
    v_failure,
    v_liftA2,
    v_success,
)
from funcpipe_rag.rag.domain import (
    Chunk as ModelChunk,
)
from funcpipe_rag.rag.domain import (
    ChunkMetadata,
    ChunkText,
    Embedding,
    assemble,
    process_batch_hybrid,
)
from funcpipe_rag.rag.stages import clean_doc
from funcpipe_rag.result.types import Err, ErrInfo, Ok


class AcceptedChunkPayload(TypedDict):
    text: str
    metadata: dict[str, JSON]


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


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (success(embedding=(0.25, 0.75), metadata={"model": "local"}), "ready:2"),
        (failure(code="EMBED_FAIL", msg="offline", attempt=2), "failed:EMBED_FAIL:attempt-2"),
    ],
)
def test_pattern_matching_handles_every_chunk_outcome(state: ChunkState, expected: str) -> None:
    assert describe_chunk_outcome(state) == expected


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


def test_monoid_fold_aggregates_chunk_metrics_with_empty_identity() -> None:
    chunks = (
        Metrics(processed=1, succeeded=1, latency_sum_ms=12.5, latency_max_ms=12.5),
        Metrics(processed=1, succeeded=0, latency_sum_ms=8.0, latency_max_ms=8.0),
    )

    assert fold(METRICS, ()) == Metrics()
    assert fold(METRICS, chunks) == Metrics(
        processed=2,
        succeeded=1,
        latency_sum_ms=20.5,
        latency_max_ms=12.5,
    )


def test_pydantic_adapter_rejects_invalid_embedding_before_core_conversion() -> None:
    model = ChunkModel(
        text="validated boundary",
        metadata={"source": "lesson"},
        embedding=[0.25, 0.75],
    )
    core = to_core_chunk(model)

    assert core.text == "validated boundary"
    assert dict(core.metadata) == {"source": "lesson"}
    with pytest.raises(ValidationError, match="must be finite|not finite"):
        ChunkModel(text="invalid", embedding=[float("nan")])


def test_serialization_preserves_result_failure_provenance() -> None:
    failure_value = Err(
        ErrInfo(code="EMBED_FAIL", msg="model offline", stage="embed", path=(2, 4))
    )
    encoded = to_json(failure_value, enc_result())

    assert json.loads(encoded)["payload"]["error"] == {
        "code": "EMBED_FAIL",
        "msg": "model offline",
        "stage": "embed",
        "path": [2, 4],
    }
    assert from_json(encoded, dec_result()) == failure_value


def test_domain_assembly_reports_all_embedding_mismatches() -> None:
    text = ChunkText(content="composable chunk")
    metadata = ChunkMetadata(
        source="lesson",
        tags=("typed", "typed", "rag"),
        embedding_model="expected-model",
        expected_dim=3,
    )
    embedding = Embedding(vector=(0.25, 0.75), model="actual-model")

    result = assemble(text, metadata, embedding)

    assert isinstance(result, VFailure)
    assert tuple(error.code for error in result.errors) == (
        ErrorCode.EMB_MODEL_MISMATCH,
        ErrorCode.EMB_DIM_MISMATCH,
    )


def test_hybrid_embedding_preserves_pure_rag_observables() -> None:
    chunk = ModelChunk(
        text=ChunkText(content="representation proof"),
        metadata=ChunkMetadata(source="lesson", tags=("typed",), embedding_model="local"),
    )
    pure = process_batch_hybrid([chunk], mode="pure")
    hybrid = process_batch_hybrid([chunk], mode="hybrid")

    assert isinstance(pure[0], VSuccess)
    assert isinstance(hybrid[0], VSuccess)
    assert pure[0].value.id == hybrid[0].value.id
    assert pure[0].value.text == hybrid[0].value.text
    assert pure[0].value.metadata == hybrid[0].value.metadata
    assert pure[0].value.embedding is not None
    assert hybrid[0].value.embedding is not None
    assert hybrid[0].value.embedding.vector == pytest.approx(pure[0].value.embedding.vector)


def test_boundary_refactor_preserves_accepted_chunk_values() -> None:
    payload: AcceptedChunkPayload = {
        "text": "accepted input",
        "metadata": {"source": "lesson", "reviewed": True},
    }
    legacy = make_chunk(text=payload["text"], path=(), metadata=payload["metadata"])
    refactored = to_core_chunk(ChunkModel.model_validate(payload))

    assert refactored == legacy
    with pytest.raises(ValidationError, match="at least 1 character"):
        ChunkModel.model_validate({"text": "", "metadata": payload["metadata"]})
