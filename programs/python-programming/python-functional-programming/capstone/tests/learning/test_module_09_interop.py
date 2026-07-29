from __future__ import annotations

from collections.abc import Iterator

from funcpipe_rag.boundaries.web.documents import parse_document_payloads
from funcpipe_rag.interop.dataframes import normalize_records
from funcpipe_rag.interop.stdlib_fp import merge_streams, running_sum
from funcpipe_rag.interop.toolz_compat import compose, curried_filter, curried_map, pipe
from funcpipe_rag.pipelines.configured import (
    PipelineConfig,
    StepConfig,
    build_rag_pipeline,
)
from funcpipe_rag.result.types import Err, Ok


def test_stdlib_interop_defers_source_consumption() -> None:
    pulls: list[tuple[str, int]] = []

    def source(name: str, values: tuple[int, ...]) -> Iterator[int]:
        for value in values:
            pulls.append((name, value))
            yield value

    merged = merge_streams(source("left", (1, 2)), source("right", (3,)))

    assert pulls == []
    assert next(merged) == 1
    assert pulls == [("left", 1)]
    assert list(merged) == [2, 3]
    assert pulls == [("left", 1), ("left", 2), ("right", 3)]


def test_stdlib_running_fold_exposes_each_prefix() -> None:
    totals = running_sum([3, -1, 4])

    assert list(totals) == [3, 2, 6]


def test_optional_helper_facade_preserves_plain_python_semantics() -> None:
    normalize = compose(str.strip, str.lower)
    select_nonempty = curried_filter(bool)
    lengths = curried_map(len)

    result = pipe(
        ["  ALPHA ", " ", "Beta"],
        curried_map(normalize),
        select_nonempty,
        lengths,
        list,
    )

    assert result == [5, 4]


def test_record_adapter_normalizes_without_mutating_boundary_input() -> None:
    rows = [{"doc_id": "paper-1", "abstract": "  Mixed   CASE  ", "categories": "cs.AI"}]
    original = [dict(row) for row in rows]

    once = normalize_records(rows)
    twice = normalize_records(once)

    assert rows == original
    assert once == twice
    assert once[0]["clean_abstract"] == "mixed case"


def test_web_payload_translation_exposes_validation_as_a_value() -> None:
    valid = parse_document_payloads(
        [{"doc_id": "paper-1", "title": "FP", "abstract": "Explicit boundaries"}]
    )
    invalid = parse_document_payloads(
        [{"doc_id": "paper-2", "title": "Bad", "abstract": 42}]
    )

    assert isinstance(valid, Ok)
    assert valid.value[0].categories == ""
    assert isinstance(invalid, Err)
    assert invalid.error.code == "INVALID_DOCUMENT"
    assert invalid.error.stage == "web.parse_document_payloads"


def test_configured_pipeline_rejects_invalid_order_before_consumption() -> None:
    pulls: list[str] = []

    def documents() -> Iterator[object]:
        pulls.append("pulled")
        yield object()

    config = PipelineConfig(steps=(StepConfig("embed"),))

    try:
        build_rag_pipeline(config)
    except TypeError as error:
        assert str(error) == "embed expects ChunkWithoutEmbedding"
    else:
        raise AssertionError("invalid stage order must be rejected")

    assert pulls == []
    assert list(documents())
    assert pulls == ["pulled"]
