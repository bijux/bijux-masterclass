"""Executable learning proof for Module 02's data-first RAG API."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from funcpipe_rag import (
    All,
    CleanConfig,
    Eq,
    Err,
    Ok,
    RagBoundaryDeps,
    RagConfig,
    RagEnv,
    RagTaps,
    RawDoc,
    RulesConfig,
    StartsWith,
    abstract_min_len,
    boundary_rag_config,
    category_startswith,
    chunk_doc,
    clean_doc,
    embed_chunk,
    eval_pred,
    ffilter,
    flatmap,
    fmap,
    full_rag_api_docs,
    full_rag_api_path,
    get_deps,
    make_cleaner,
    make_rag_fn,
    parse_rule,
    pipe,
    result_and_then,
    result_map,
    rule_and,
    structural_dedup_chunks,
)


def _docs() -> list[RawDoc]:
    return [
        RawDoc("doc-a", "Functional Python", "  A   B  ", "cs.PL"),
        RawDoc("doc-b", "Number Theory", "C D", "math.NT"),
    ]


def test_expression_pipeline_matches_direct_threading() -> None:
    def normalize(values: list[str]) -> list[str]:
        return [value.strip().lower() for value in values]

    def keep_nonempty(values: list[str]) -> list[str]:
        return [value for value in values if value]

    values = [" A ", " ", "B"]

    assert pipe(values, normalize, keep_nonempty) == keep_nonempty(normalize(values))


def test_iterator_combinators_defer_work_and_preserve_stage_order() -> None:
    called: list[tuple[str, int]] = []

    def source() -> Iterator[int]:
        for value in range(4):
            called.append(("source", value))
            yield value

    def is_even(value: int) -> bool:
        called.append(("filter", value))
        return value % 2 == 0

    def duplicate(value: int) -> tuple[int, int]:
        called.append(("expand", value))
        return (value, value)

    stream = flatmap(duplicate)(fmap(lambda value: value + 1)(ffilter(is_even)(source())))

    assert called == []
    assert next(stream) == 1
    assert called == [("source", 0), ("filter", 0), ("expand", 1)]


def test_cleaning_configuration_is_ordered_data() -> None:
    lower_then_upper = make_cleaner(CleanConfig(("strip", "lower", "upper")))
    upper_then_lower = make_cleaner(CleanConfig(("strip", "upper", "lower")))
    doc = RawDoc("doc-a", "title", " MiXeD ", "cs.PL")

    assert lower_then_upper(doc).abstract == "MIXED"
    assert upper_then_lower(doc).abstract == "mixed"


def test_configurator_captures_policy_but_not_input() -> None:
    run = make_rag_fn(
        chunk_size=4,
        clean_cfg=CleanConfig(("strip", "upper")),
    )
    docs = [RawDoc("doc-a", "title", " abcdef ", "cs.PL")]

    first_chunks, first_observations = run(docs)
    second_chunks, second_observations = run(docs)

    assert first_chunks == second_chunks
    assert first_observations == second_observations
    assert [chunk.text for chunk in first_chunks] == ["ABCD", "EF"]


def test_predicate_values_are_inspectable_and_short_circuit() -> None:
    pred = All(
        (
            Eq("categories", "math.NT"),
            StartsWith("unknown-path", "never evaluated"),
        )
    )
    doc = RawDoc("doc-a", "title", "abstract", "cs.PL")

    assert pred.rules[0] == Eq("categories", "math.NT")
    assert not eval_pred(doc, pred)
    with pytest.raises(ValueError, match="Unknown path"):
        eval_pred(
            doc,
            All((Eq("categories", "cs.PL"), StartsWith("unknown-path", "x"))),
        )


def test_function_rules_bind_and_compose_domain_policy() -> None:
    keep = rule_and(category_startswith("cs."), abstract_min_len(4))

    assert keep(RawDoc("doc-a", "title", "long", "cs.PL"))
    assert not keep(RawDoc("doc-b", "title", "long", "math.NT"))
    assert not keep(RawDoc("doc-c", "title", "no", "cs.PL"))


def test_guarded_rule_expression_accepts_only_the_taught_surface() -> None:
    keep = parse_rule('d.categories.startswith("cs.") and len(d.abstract) >= 4')

    assert keep(RawDoc("doc-a", "title", "long", "cs.PL"))
    assert not keep(RawDoc("doc-b", "title", "no", "cs.PL"))
    with pytest.raises(ValueError):
        parse_rule("__import__('os').getcwd()")


def test_boundary_config_returns_validated_data() -> None:
    result = boundary_rag_config(
        {"chunk_size": 4, "clean_rules": ["strip", "upper"]}
    )

    assert isinstance(result, Ok)
    assert result.value.env.chunk_size == 4
    assert result.value.clean == CleanConfig(("strip", "upper"))


def test_boundary_config_rejects_bool_instead_of_treating_it_as_int() -> None:
    result = boundary_rag_config({"chunk_size": True})

    assert isinstance(result, Err)
    assert "bool" in result.error


def test_taps_observe_stage_values_without_changing_api_output() -> None:
    docs = _docs()
    config = RagConfig(env=RagEnv(chunk_size=4))
    baseline = full_rag_api_docs(docs, config, get_deps(config))
    observed: list[tuple[str, int]] = []
    taps = RagTaps(
        docs=lambda values: observed.append(("docs", len(values))),
        cleaned=lambda values: observed.append(("cleaned", len(values))),
        chunks=lambda values: observed.append(("chunks", len(values))),
    )

    with_taps = full_rag_api_docs(docs, config, get_deps(config, taps=taps))

    assert with_taps == baseline
    assert observed == [("docs", 2), ("cleaned", 2), ("chunks", 2)]


def test_reader_failure_short_circuits_the_pure_rag_core() -> None:
    failure = Err("source unavailable")

    class FailingReader:
        def read_docs(self, path: str):
            assert path == "missing.jsonl"
            return failure

    config = RagConfig(env=RagEnv(chunk_size=4))
    deps = RagBoundaryDeps(core=get_deps(config), reader=FailingReader())

    assert full_rag_api_path("missing.jsonl", config, deps) == failure


def test_result_combinators_do_not_run_after_boundary_failure() -> None:
    called = False

    def count_chunks(value: int) -> int:
        nonlocal called
        called = True
        return value + 1

    failure = Err("invalid boundary input")

    assert result_map(failure, count_chunks) == failure
    assert result_and_then(failure, lambda value: Ok(count_chunks(value))) == failure
    assert not called


def test_default_api_preserves_module_01_rag_values() -> None:
    docs = _docs()
    env = RagEnv(chunk_size=4)
    baseline = structural_dedup_chunks(
        embed_chunk(chunk)
        for doc in docs
        for chunk in chunk_doc(clean_doc(doc), env)
    )
    chunks, observations = full_rag_api_docs(
        docs,
        RagConfig(env=env, keep=RulesConfig()),
        get_deps(RagConfig(env=env, keep=RulesConfig())),
    )

    assert chunks == baseline
    assert observations.total_docs == len(docs)
    assert observations.total_chunks == len(chunks)
