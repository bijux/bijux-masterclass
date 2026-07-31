from __future__ import annotations

import json
from typing import TypedDict

import pytest
from funcpipe_rag.boundaries.adapters.pydantic_edges import ChunkModel, to_core_chunk
from funcpipe_rag.boundaries.adapters.serde import (
    dec_result,
    enc_result,
    from_json,
    to_json,
)
from funcpipe_rag.core.rag_types import (
    Chunk,
    ChunkWithoutEmbedding,
    CleanDoc,
    RagEnv,
    RawDoc,
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
from funcpipe_rag.rag.stages import chunk_doc, clean_doc, embed_chunk
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result
from pydantic import ValidationError
from typing_extensions import assert_never


class AcceptedChunkPayload(TypedDict):
    doc_id: str
    text: str
    start: int
    end: int
    metadata: dict[str, object]
    embedding: tuple[float, ...]


def describe_chunk_outcome(outcome: Result[Chunk, ErrInfo]) -> str:
    match outcome:
        case Ok(value=chunk):
            return f"ready:{chunk.doc_id}:{len(chunk.embedding)}"
        case Err(error=error):
            return f"failed:{error.code}:{error.stage}"
        case other:
            assert_never(other)


def test_rag_product_types_keep_chunk_fields_together() -> None:
    prepared = ChunkWithoutEmbedding(
        doc_id="typed-values",
        text="algebraic data",
        start=0,
        end=14,
        metadata={"source": "course-book"},
    )

    assert prepared.doc_id == "typed-values"
    assert prepared.text[prepared.start : prepared.end] == "algebraic data"
    assert dict(prepared.metadata) == {"source": "course-book"}
    with pytest.raises((AttributeError, TypeError)):
        prepared.metadata["source"] = "changed"  # type: ignore[index]


@pytest.mark.parametrize(
    ("outcome", "expected"),
    [
        (
            Ok(
                embed_chunk(
                    ChunkWithoutEmbedding(
                        doc_id="rag-typed",
                        text="sum type",
                        start=0,
                        end=8,
                    )
                )
            ),
            "ready:rag-typed:16",
        ),
        (
            Err(ErrInfo(code="EMBED_FAIL", msg="offline", stage="embed")),
            "failed:EMBED_FAIL:embed",
        ),
    ],
)
def test_result_sum_type_separates_embedding_success_from_failure(
    outcome: Result[Chunk, ErrInfo],
    expected: str,
) -> None:
    assert describe_chunk_outcome(outcome) == expected


def test_rag_stage_types_make_embedding_transition_explicit() -> None:
    raw = RawDoc("rag-stage", "Types", "  Typed   STAGES  ", "fp")
    cleaned = clean_doc(raw)
    prepared = chunk_doc(cleaned, RagEnv(chunk_size=32))[0]
    embedded = embed_chunk(prepared)

    assert isinstance(cleaned, CleanDoc)
    assert isinstance(prepared, ChunkWithoutEmbedding)
    assert not isinstance(prepared, Chunk)
    assert isinstance(embedded, Chunk)
    assert embedded.doc_id == prepared.doc_id
    assert embedded.text == prepared.text
    assert (embedded.start, embedded.end) == (prepared.start, prepared.end)
    assert len(embedded.embedding) == 16
    assert raw.abstract == "  Typed   STAGES  "


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
        return (
            v_success(raw)
            if len(raw.split()) >= 2
            else v_failure(("abstract too short",))
        )

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
        doc_id="boundary",
        text="validated boundary",
        start=0,
        end=18,
        metadata={"source": "lesson"},
        embedding=(0.25, 0.75) + (0.0,) * 14,
    )
    core = to_core_chunk(model)

    assert core.text == "validated boundary"
    assert dict(core.metadata) == {"source": "lesson"}
    with pytest.raises(ValidationError, match="must be finite|not finite"):
        ChunkModel(
            doc_id="boundary",
            text="invalid",
            start=0,
            end=7,
            embedding=(float("nan"),) + (0.0,) * 15,
        )


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
        metadata=ChunkMetadata(
            source="lesson", tags=("typed",), embedding_model="local"
        ),
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
    assert hybrid[0].value.embedding.vector == pytest.approx(
        pure[0].value.embedding.vector
    )


def test_boundary_refactor_preserves_accepted_chunk_values() -> None:
    payload: AcceptedChunkPayload = {
        "doc_id": "accepted",
        "text": "accepted input",
        "start": 0,
        "end": 14,
        "metadata": {"source": "lesson", "reviewed": True},
        "embedding": (0.0,) * 16,
    }
    legacy = Chunk(**payload)
    refactored = to_core_chunk(ChunkModel.model_validate(payload))

    assert refactored == legacy
    with pytest.raises(ValidationError, match="at least 1 character"):
        ChunkModel.model_validate({**payload, "text": "", "end": 0})
