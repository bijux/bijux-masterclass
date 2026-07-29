"""Executable learning proof for Module 04's resilient RAG stream."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterator
from itertools import islice

from funcpipe_rag import ChunkWithoutEmbedding, TextNode, TreeDoc
from funcpipe_rag.policies.breakers import (
    BreakInfo,
    circuit_breaker_count_emit,
    short_circuit_on_err_emit,
)
from funcpipe_rag.policies.memo import content_hash_key, memoize_keyed
from funcpipe_rag.policies.reports import fold_error_report, report_to_jsonable
from funcpipe_rag.policies.resources import managed_stream
from funcpipe_rag.policies.retries import (
    fixed_policy,
    is_retriable_errinfo,
    retry_map_iter,
)
from funcpipe_rag.result import (
    Err,
    ErrInfo,
    Ok,
    Result,
    Some,
    fold_results_collect_errs_capped,
    fold_results_fail_fast,
    is_some,
    make_errinfo,
    to_option,
    try_map_iter,
)
from funcpipe_rag.tree import (
    flatten,
    fold_count_length_maxdepth,
    fold_tree_no_path,
)


def _chunk(text: str, start: int) -> ChunkWithoutEmbedding:
    return ChunkWithoutEmbedding(
        doc_id="doc-1",
        text=text,
        start=start,
        end=start + len(text),
    )


def _document_tree() -> TreeDoc:
    return TreeDoc(
        TextNode("root", {"id": "root"}),
        (
            TreeDoc(TextNode("a", {"id": "a"})),
            TreeDoc(
                TextNode("b", {"id": "b"}),
                (TreeDoc(TextNode("c", {"id": "c"})),),
            ),
        ),
    )


def test_hierarchical_document_traversal_is_stack_safe_lazy_and_ordered() -> None:
    tree = TreeDoc(TextNode("leaf", {"id": "leaf"}))
    for index in range(1_200):
        tree = TreeDoc(TextNode(f"node-{index}", {"id": str(index)}), (tree,))

    first_three = list(islice(flatten(tree), 3))

    assert [chunk.text for chunk in first_three] == [
        "node-1199",
        "node-1198",
        "node-1197",
    ]
    assert [chunk.metadata["path"] for chunk in first_three] == [
        (),
        (0,),
        (0, 0),
    ]


def test_fused_tree_fold_preserves_separate_observations() -> None:
    tree = _document_tree()

    fused = fold_count_length_maxdepth(tree)
    separate = (
        fold_tree_no_path(tree, 0, lambda count, _node, _depth: count + 1),
        fold_tree_no_path(
            tree,
            0,
            lambda length, node, _depth: length + len(node.node.text),
        ),
        fold_tree_no_path(tree, 0, lambda depth, _node, current: max(depth, current)),
    )

    assert fused == separate == (4, 7, 2)


def test_semantic_memo_key_avoids_equivalent_embedding_work() -> None:
    calls = 0

    def normalized_text_key(chunk: ChunkWithoutEmbedding) -> str:
        return content_hash_key(chunk)

    @memoize_keyed(normalized_text_key)
    def deterministic_embedding(chunk: ChunkWithoutEmbedding) -> tuple[int, ...]:
        nonlocal calls
        calls += 1
        normalized = " ".join(chunk.text.strip().lower().split())
        return tuple(len(token) for token in normalized.split())

    spaced = _chunk("  Functional   Python ", 0)
    normalized = _chunk("functional python", 30)

    assert content_hash_key(spaced) == content_hash_key(normalized)
    assert deterministic_embedding(spaced) == deterministic_embedding(normalized)
    assert calls == 1


def test_option_absence_and_result_failure_remain_distinct() -> None:
    failure: Result[str, ErrInfo] = Err(
        make_errinfo("DOC/MISSING", "document was not read", "read", (7,))
    )
    transformed = False

    def normalize(value: str) -> str:
        nonlocal transformed
        transformed = True
        return value.strip().lower()

    unchanged = failure.map(normalize)
    absent = to_option(failure)
    present = Some("document")

    assert unchanged == failure
    assert not transformed
    assert not is_some(absent)
    assert is_some(present)


def test_result_stream_keeps_failure_position_and_bounds_demand() -> None:
    requested = 0

    def source() -> Iterator[tuple[int, str]]:
        nonlocal requested
        for item in enumerate(("first", "bad", "unrequested")):
            requested += 1
            yield item

    def embed(item: tuple[int, str]) -> str:
        _, text = item
        if text == "bad":
            raise ValueError("invalid embedding input")
        return text.upper()

    observed = list(
        islice(
            try_map_iter(
                embed,
                source(),
                stage="embed",
                key_path=lambda item: (item[0],),
                code="EMBED/INVALID",
            ),
            2,
        )
    )

    assert observed[0] == Ok("FIRST")
    assert isinstance(observed[1], Err)
    assert observed[1].error.code == "EMBED/INVALID"
    assert observed[1].error.stage == "embed"
    assert observed[1].error.path == (1,)
    assert requested == 2


def test_error_fold_makes_fail_fast_and_bounded_collection_observable() -> None:
    requested = 0

    def results() -> Iterator[Result[int, str]]:
        nonlocal requested
        for result in (Ok(2), Ok(3), Err("bad"), Ok(100)):
            requested += 1
            yield result

    failed = fold_results_fail_fast(results(), 0, lambda total, value: total + value)
    collected = fold_results_collect_errs_capped(
        (Err("first"), Ok(4), Err("second"), Err("overflow")),
        0,
        lambda total, value: total + value,
        max_errs=2,
    )

    assert failed == Err("bad")
    assert requested == 3
    assert collected == Err((["first", "second"], True))


def test_emitting_breaker_preserves_reason_and_closes_upstream() -> None:
    closed = False

    def source() -> Iterator[Result[int, str]]:
        nonlocal closed
        try:
            yield Ok(1)
            yield Err("unavailable")
            yield Ok(2)
        finally:
            closed = True

    observed = list(short_circuit_on_err_emit(source()))

    assert observed[:2] == [Ok(1), Err("unavailable")]
    assert isinstance(observed[-1], Err)
    assert isinstance(observed[-1].error, BreakInfo)
    assert observed[-1].error.code == "BREAK/FIRST_ERR"
    assert observed[-1].error.total == 2
    assert closed


def test_managed_stream_closes_after_partial_consumption() -> None:
    entered = False
    closed = False

    def source() -> Iterator[ChunkWithoutEmbedding]:
        nonlocal entered, closed
        entered = True
        try:
            yield _chunk("first", 0)
            yield _chunk("second", 10)
        finally:
            closed = True

    manager = managed_stream(source)
    assert not entered

    with manager as chunks:
        assert next(chunks).text == "first"

    assert entered
    assert closed


def test_retry_classification_bounds_attempts_and_exposes_completion_order() -> None:
    attempts: defaultdict[str, int] = defaultdict(int)

    def embed(text: str) -> Result[str, ErrInfo]:
        attempts[text] += 1
        if text == "transient" and attempts[text] == 1:
            return Err(
                make_errinfo(
                    "EMBED/UNAVAILABLE",
                    "try again",
                    "embed",
                    (0,),
                )
            )
        if text == "permanent":
            return Err(
                make_errinfo(
                    "EMBED/INVALID",
                    "do not retry",
                    "embed",
                    (2,),
                )
            )
        return Ok(text.upper())

    observed = list(
        retry_map_iter(
            embed,
            ("transient", "stable", "permanent"),
            classifier=is_retriable_errinfo,
            policy=fixed_policy(3),
            stage="embed",
            max_attempts=3,
            inflight_cap=3,
        )
    )

    assert [result.value for result in observed if isinstance(result, Ok)] == [
        "STABLE",
        "TRANSIENT",
    ]
    assert attempts == {"transient": 2, "stable": 1, "permanent": 1}
    permanent = next(result for result in observed if isinstance(result, Err))
    assert permanent.error.code == "EMBED/INVALID"
    assert permanent.error.ctx["attempt"] == 1


def test_retry_breaker_and_report_form_one_bounded_rag_failure_route() -> None:
    attempts: defaultdict[str, int] = defaultdict(int)

    def embed(chunk: ChunkWithoutEmbedding) -> Result[str, ErrInfo]:
        attempts[chunk.text] += 1
        if chunk.text == "flaky" and attempts[chunk.text] == 1:
            return Err(
                make_errinfo(
                    "EMBED/UNAVAILABLE",
                    "transient service failure",
                    "embed",
                    (chunk.start,),
                )
            )
        if chunk.text.startswith("bad"):
            return Err(
                make_errinfo(
                    "EMBED/INVALID",
                    "invalid chunk",
                    "embed",
                    (chunk.start,),
                )
            )
        return Ok(chunk.text.upper())

    chunks = (
        _chunk("flaky", 0),
        _chunk("bad-a", 10),
        _chunk("bad-b", 20),
        _chunk("unreached", 30),
    )
    retried = retry_map_iter(
        embed,
        chunks,
        classifier=is_retriable_errinfo,
        policy=fixed_policy(2),
        stage="embed",
        max_attempts=2,
        inflight_cap=2,
    )
    guarded = circuit_breaker_count_emit(retried, max_errs=1)
    observed = list(guarded)
    report = fold_error_report(observed, max_samples=1)
    payload = report_to_jsonable(report)

    assert attempts == {"flaky": 2, "bad-a": 1, "bad-b": 1}
    assert [result.value for result in observed if isinstance(result, Ok)] == [
        "FLAKY"
    ]
    assert report.total_items == 4
    assert report.total_errs == 3
    assert report.by_code["EMBED/INVALID"].count == 2
    assert len(report.by_code["EMBED/INVALID"].samples) == 1
    assert report.by_code["BREAK/ERR_COUNT"].count == 1
    assert payload["error_rate"] == 0.75
    json.dumps(payload)
