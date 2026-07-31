from __future__ import annotations

from collections.abc import Iterator

from funcpipe_rag.boundaries.web.documents import parse_document_payloads
from funcpipe_rag.core.rag_types import Chunk, ChunkWithoutEmbedding
from funcpipe_rag.domain.effects import perform
from funcpipe_rag.domain.facades import Keyed, deterministic_embedder_port
from funcpipe_rag.interop.dataframes import normalize_records
from funcpipe_rag.interop.stdlib_fp import merge_streams, running_sum
from funcpipe_rag.interop.toolz_compat import compose, curried_filter, curried_map, pipe
from funcpipe_rag.pipelines.cli import apply_step_params, parse_override
from funcpipe_rag.pipelines.configured import (
    PipelineConfig,
    StepConfig,
    build_rag_pipeline,
)
from funcpipe_rag.pipelines.distributed import backend_statuses
from funcpipe_rag.pipelines.specs import (
    OperatorSpec,
    PipelineSpec,
    reconstruct_pipeline,
    spec_hash,
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


def test_cli_override_rejects_a_misspelled_stage_without_mutation() -> None:
    config = PipelineConfig(
        steps=(
            StepConfig("clean"),
            StepConfig("chunk", {"chunk_size": 512}),
            StepConfig("embed"),
        )
    )

    override = parse_override("chunk.chunk_size=256")
    changed = apply_step_params(config, "chunk", override["chunk"])

    assert config.steps[1].params["chunk_size"] == 512
    assert changed.steps[1].params["chunk_size"] == 256
    try:
        apply_step_params(config, "chnuk", {"chunk_size": 256})
    except ValueError as error:
        assert str(error) == "unknown pipeline step: chnuk"
    else:
        raise AssertionError("a misspelled target must not be ignored")


def test_distributed_status_does_not_confuse_installation_with_implementation() -> None:
    statuses = backend_statuses()

    assert [status.name for status in statuses] == ["dask", "beam"]
    assert all(isinstance(status.installed, bool) for status in statuses)
    assert all(status.compiler_shipped is False for status in statuses)


def test_facade_defers_client_failure_and_returns_it_as_data() -> None:
    calls = 0

    def failing_embedder(_chunk: ChunkWithoutEmbedding) -> Chunk:
        nonlocal calls
        calls += 1
        raise ConnectionError("embedding service unavailable")

    port = deterministic_embedder_port(embed_one=failing_embedder)
    plan = port.embed_batch(
        [Keyed(key="paper-1:0", value=ChunkWithoutEmbedding("paper-1", "text", 0, 4))]
    )

    assert calls == 0
    result = perform(plan)
    assert calls == 1
    assert isinstance(result, Err)
    assert result.error.stage == "facade.embed_batch"


def test_pipeline_spec_is_hashed_and_allow_listed_before_execution() -> None:
    calls = 0

    def untrusted_operator(value: int) -> int:
        nonlocal calls
        calls += 1
        return value + 1

    collected = PipelineSpec((OperatorSpec("Map", "untrusted", "collect"),))
    fail_fast = PipelineSpec((OperatorSpec("Map", "untrusted", "fail_fast"),))

    result = reconstruct_pipeline(
        collected,
        {"untrusted": untrusted_operator},
        allow_list=set(),
    )

    assert isinstance(result, Err)
    assert result.error.code == "DISALLOWED"
    assert calls == 0
    assert spec_hash(collected) != spec_hash(fail_fast)


def test_module_09_boundaries_converge_on_one_rag_pipeline() -> None:
    translated = parse_document_payloads(
        [
            {
                "doc_id": "paper-1",
                "title": "Boundary discipline",
                "abstract": "Adapters translate while the core decides.",
                "categories": "cs.SE",
            }
        ]
    )
    assert isinstance(translated, Ok)

    base = PipelineConfig(
        steps=(
            StepConfig("clean"),
            StepConfig("chunk", {"chunk_size": 512}),
            StepConfig("embed"),
        )
    )
    config = apply_step_params(base, "chunk", {"chunk_size": 16})
    pipeline = build_rag_pipeline(config)

    results = list(pipeline(iter(translated.value)))

    assert len(results) == 3
    assert all(isinstance(result, Ok) for result in results)
    assert [result.value.start for result in results if isinstance(result, Ok)] == [0, 16, 32]
