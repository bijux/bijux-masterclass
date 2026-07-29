"""Executable learning proof for Module 03's demand-driven RAG pipeline."""

from __future__ import annotations

from collections.abc import Iterator
from itertools import islice

import pytest

from funcpipe_rag import (
    DedupIterator,
    FakeTime,
    RagConfig,
    RagEnv,
    RawDoc,
    TraceLens,
    _trace_iter,
    as_source,
    compose_transforms,
    fence_k,
    full_rag_api_docs,
    gen_bounded_chunks,
    gen_overlapping_chunks,
    get_deps,
    make_chain,
    multicast,
    sliding_windows,
    stream_rag_chunks,
    throttle,
)


def test_generator_construction_does_not_request_documents() -> None:
    requested: list[str] = []

    def documents() -> Iterator[RawDoc]:
        for doc_id in ("doc-a", "doc-b"):
            requested.append(doc_id)
            yield RawDoc(doc_id, "title", "x" * 200, "cs.AI")

    config = RagConfig(env=RagEnv(chunk_size=50))
    chunks = gen_bounded_chunks(documents(), config, get_deps(config), max_chunks=1)

    assert requested == []
    assert next(chunks).doc_id == "doc-a"
    assert requested == ["doc-a"]


def test_prefix_fence_does_not_pull_one_item_past_demand() -> None:
    requested = 0

    def source() -> Iterator[int]:
        nonlocal requested
        for value in range(100):
            requested += 1
            yield value

    take_three = compose_transforms(fence_k(3), iter)

    assert list(take_three(source())) == [0, 1, 2]
    assert requested == 3


@pytest.mark.parametrize(
    ("tail_policy", "expected"),
    [
        ("emit_short", [("abcd", 0, 4), ("cdef", 2, 6), ("ef", 4, 6)]),
        ("drop", [("abcd", 0, 4), ("cdef", 2, 6)]),
        ("pad", [("abcd", 0, 4), ("cdef", 2, 6), ("ef\0\0", 4, 8)]),
    ],
)
def test_overlapping_chunks_make_tail_policy_visible(
    tail_policy: str,
    expected: list[tuple[str, int, int]],
) -> None:
    chunks = gen_overlapping_chunks(
        "doc-a",
        "abcdef",
        k=4,
        o=2,
        tail_policy=tail_policy,
    )

    assert [(chunk.text, chunk.start, chunk.end) for chunk in chunks] == expected


def test_sliding_window_retains_only_the_width_needed_for_next_output() -> None:
    requested = 0

    def source() -> Iterator[int]:
        nonlocal requested
        for value in range(100):
            requested += 1
            yield value

    first_two = list(islice(sliding_windows(source(), 4), 2))

    assert first_two == [(0, 1, 2, 3), (1, 2, 3, 4)]
    assert requested == 5


def test_reusable_source_factory_starts_fresh_traversals() -> None:
    merged = make_chain(as_source((1, 2)), as_source((3,)))

    assert list(merged()) == [1, 2, 3]
    assert list(merged()) == [1, 2, 3]


def test_bounded_multicast_skew_error_does_not_consume_upstream() -> None:
    requested: list[int] = []

    def source() -> Iterator[int]:
        for value in range(4):
            requested.append(value)
            yield value

    fast, slow = multicast(source(), 2, maxlen=1)

    assert next(fast) == next(slow) == 0
    assert next(fast) == 1
    with pytest.raises(BufferError):
        next(fast)
    assert requested == [0, 1]


def test_injected_time_turns_pacing_into_deterministic_data() -> None:
    time = FakeTime()

    assert list(
        throttle(
            ("a", "b", "c"),
            min_delta=0.25,
            clock=time.clock,
            sleeper=time.sleep,
        )
    ) == ["a", "b", "c"]
    assert time.sleeps == [0.25, 0.25]
    assert time.clock() == 0.5


def test_custom_dedup_iterator_is_single_pass_and_encounter_ordered() -> None:
    deduped = DedupIterator(
        ["doc-a", "doc-a", "doc-b", "doc-a"],
        key=lambda doc_id: doc_id,
    )

    assert iter(deduped) is deduped
    assert list(deduped) == ["doc-a", "doc-b"]
    assert list(deduped) == []


def test_observation_is_value_neutral_lazy_and_sample_bounded() -> None:
    lens: TraceLens[int] = TraceLens(limit=2)
    observed = _trace_iter(range(10), lens)

    assert lens.count == 0
    assert list(islice(observed, 4)) == [0, 1, 2, 3]
    assert lens.count == 4
    assert lens.samples == [0, 1]


def test_complete_stream_matches_module_02_for_canonical_input_order() -> None:
    docs = (
        RawDoc("doc-a", "title", "A " * 100, "cs.AI"),
        RawDoc("doc-b", "title", "B " * 100, "cs.AI"),
    )
    config = RagConfig(env=RagEnv(chunk_size=50))
    deps = get_deps(config)

    streamed = list(stream_rag_chunks(docs, config, deps))
    eager, _ = full_rag_api_docs(docs, config, deps)

    assert streamed == eager
    assert all(len(chunk.embedding) == 16 for chunk in streamed)


def test_streaming_dedup_preserves_encounter_order_instead_of_sorting() -> None:
    docs = (
        RawDoc("doc-b", "title", "B " * 30, "cs.AI"),
        RawDoc("doc-a", "title", "A " * 30, "cs.AI"),
    )
    config = RagConfig(env=RagEnv(chunk_size=100))
    deps = get_deps(config)

    streamed = list(stream_rag_chunks(docs, config, deps))
    eager, _ = full_rag_api_docs(docs, config, deps)

    assert [chunk.doc_id for chunk in streamed] == ["doc-b", "doc-a"]
    assert [chunk.doc_id for chunk in eager] == ["doc-a", "doc-b"]
    assert sorted(streamed, key=lambda chunk: (chunk.doc_id, chunk.start)) == eager


def test_unique_output_fence_may_pull_duplicates_to_fill_prefix() -> None:
    requested: list[str] = []

    def documents() -> Iterator[RawDoc]:
        for doc_id, abstract in (
            ("duplicate", "same"),
            ("duplicate", "same"),
            ("unique", "other"),
        ):
            requested.append(doc_id)
            yield RawDoc(doc_id, "title", abstract, "cs.AI")

    config = RagConfig(env=RagEnv(chunk_size=100))
    chunks = stream_rag_chunks(
        documents(),
        config,
        get_deps(config),
        max_chunks=2,
    )

    assert requested == []
    assert [chunk.doc_id for chunk in chunks] == ["duplicate", "unique"]
    assert requested == ["duplicate", "duplicate", "unique"]
