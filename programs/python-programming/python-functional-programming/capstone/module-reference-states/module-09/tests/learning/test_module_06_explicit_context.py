"""Executable learning proofs for the Module 06 explicit-context delta."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from hypothesis import given
from hypothesis import strategies as st

from funcpipe_rag.boundaries.adapters.exception_bridge import try_result
from funcpipe_rag.core.rag_types import CleanDoc, RagEnv, RawDoc
from funcpipe_rag.fp.effects import (
    Reader,
    State,
    asks,
    run_state,
    run_writer,
    tell,
    transpose_option_result,
    transpose_result_option,
    writer_pure,
)
from funcpipe_rag.rag.stages import clean_doc, iter_chunk_doc
from funcpipe_rag.result.types import (
    Err,
    ErrInfo,
    NoneVal,
    Ok,
    Option,
    Result,
    Some,
    liftA2,
)


def test_result_chain_short_circuits_before_rag_cleaning() -> None:
    """A failed prerequisite prevents the dependent cleaning stage."""

    events: list[str] = []

    def require_abstract(doc: RawDoc) -> Result[RawDoc, ErrInfo]:
        if not doc.abstract.strip():
            return Err(ErrInfo(code="EMPTY_ABSTRACT", msg="abstract is required"))
        return Ok(doc)

    def clean_checked(doc: RawDoc) -> Result[CleanDoc, ErrInfo]:
        events.append(f"clean:{doc.doc_id}")
        return Ok(clean_doc(doc))

    missing = RawDoc(doc_id="missing", title="Missing", abstract=" ", categories="fp")
    invalid: Result[RawDoc, ErrInfo] = Ok(missing)

    assert invalid.and_then(require_abstract).and_then(clean_checked) == Err(
        ErrInfo(code="EMPTY_ABSTRACT", msg="abstract is required")
    )
    assert events == []

    present = RawDoc(
        doc_id="present",
        title="Present",
        abstract="  Functional   Flow  ",
        categories="fp",
    )
    valid: Result[RawDoc, ErrInfo] = Ok(present)

    assert valid.and_then(require_abstract).and_then(clean_checked) == Ok(
        CleanDoc(
            doc_id="present",
            title="Present",
            abstract="functional flow",
            categories="fp",
        )
    )
    assert events == ["clean:present"]


def test_liftA2_combines_independent_rag_config_fields() -> None:
    """Applicative lifting combines independent successes and keeps error order."""

    def make_env(chunk_size: int, overlap: int) -> RagEnv:
        return RagEnv(chunk_size=chunk_size, overlap=overlap)

    chunk_size: Result[int, ErrInfo] = Ok(8)
    overlap: Result[int, ErrInfo] = Ok(2)

    assert liftA2(make_env, chunk_size, overlap) == Ok(
        RagEnv(chunk_size=8, overlap=2)
    )

    chunk_error = ErrInfo(code="CHUNK_SIZE", msg="must be positive")
    bad_chunk_size: Result[int, ErrInfo] = Err(chunk_error)
    bad_overlap: Result[int, ErrInfo] = Err(
        ErrInfo(code="OVERLAP", msg="must be non-negative")
    )

    failed = liftA2(make_env, bad_chunk_size, bad_overlap)
    assert isinstance(failed, Err)
    assert failed.error == chunk_error


@given(
    abstract=st.text(
        alphabet=" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        max_size=60,
    )
)
def test_result_map_composition_preserves_rag_cleaning(abstract: str) -> None:
    """Two lawful map groupings retain the same normalized RAG text."""

    doc = RawDoc(doc_id="law", title="Law", abstract=abstract, categories="fp")
    source: Result[RawDoc, ErrInfo] = Ok(doc)

    separate = source.map(clean_doc).map(lambda cleaned: cleaned.abstract)
    composed = source.map(lambda raw: clean_doc(raw).abstract)

    assert separate == composed


def test_reader_runs_same_rag_chunk_program_with_explicit_env() -> None:
    """One pure chunk program receives its read-only environment at run time."""

    doc = CleanDoc(
        doc_id="reader",
        title="Reader",
        abstract="abcdefghij",
        categories="fp",
    )
    program: Reader[RagEnv, list[str]] = asks(
        lambda env: [chunk.text for chunk in iter_chunk_doc(doc, env)]
    )

    assert program.run(RagEnv(chunk_size=4)) == ["abcd", "efgh", "ij"]
    assert program.run(RagEnv(chunk_size=6)) == ["abcdef", "ghij"]


def test_state_threads_rag_chunk_progress_without_global_mutation() -> None:
    """State returns progress explicitly while preserving the initial value."""

    @dataclass(frozen=True)
    class Progress:
        chunks: int = 0
        characters: int = 0

    doc = CleanDoc(
        doc_id="state",
        title="State",
        abstract="abcdefghij",
        categories="fp",
    )
    chunks = list(iter_chunk_doc(doc, RagEnv(chunk_size=4)))

    def account(text: str) -> State[Progress, str]:
        return State(
            lambda progress: (
                text,
                Progress(
                    chunks=progress.chunks + 1,
                    characters=progress.characters + len(text),
                ),
            )
        )

    program = (
        account(chunks[0].text)
        .and_then(lambda _: account(chunks[1].text))
        .and_then(lambda _: account(chunks[2].text))
    )
    initial = Progress()

    assert run_state(program, initial) == ("ij", Progress(chunks=3, characters=10))
    assert initial == Progress()


def test_exception_bridge_types_expected_config_failure_only() -> None:
    """A boundary converts its named input error and lets a bug propagate."""

    def parse_chunk_size(raw: str) -> Result[int, ErrInfo]:
        return try_result(
            lambda: int(raw),
            lambda error: ErrInfo(code="CONFIG_PARSE", msg=str(error)),
            exc_type=ValueError,
        )

    assert parse_chunk_size("8") == Ok(8)
    assert parse_chunk_size("eight") == Err(
        ErrInfo(
            code="CONFIG_PARSE",
            msg="invalid literal for int() with base 10: 'eight'",
        )
    )

    def broken_parser() -> int:
        raise RuntimeError("parser invariant broken")

    with pytest.raises(RuntimeError, match="parser invariant broken"):
        try_result(
            broken_parser,
            lambda error: ErrInfo(code="CONFIG_PARSE", msg=str(error)),
            exc_type=ValueError,
        )


def test_layer_order_distinguishes_missing_document_from_retrieval_failure() -> None:
    """Result outside Option preserves the difference between error and absence."""

    doc = CleanDoc(
        doc_id="found",
        title="Found",
        abstract="retrieved",
        categories="fp",
    )
    found: Result[Option[CleanDoc], ErrInfo] = Ok(Some(doc))
    missing: Result[Option[CleanDoc], ErrInfo] = Ok(NoneVal())
    retrieval_error = ErrInfo(code="RETRIEVAL", msg="index unavailable")
    failed: Result[Option[CleanDoc], ErrInfo] = Err(retrieval_error)

    assert transpose_result_option(found) == Some(Ok(doc))
    assert transpose_result_option(missing) == NoneVal()
    assert transpose_result_option(failed) == Some(Err(retrieval_error))

    assert transpose_option_result(transpose_result_option(found)) == found
    assert transpose_option_result(transpose_result_option(missing)) == missing
    assert transpose_option_result(transpose_result_option(failed)) == failed


def test_writer_preserves_rag_chunk_while_accumulating_trace() -> None:
    """Writer keeps the RAG value unchanged and appends ordered trace data."""

    doc = CleanDoc(
        doc_id="writer",
        title="Writer",
        abstract="abcdefghij",
        categories="fp",
    )
    chunk = next(iter_chunk_doc(doc, RagEnv(chunk_size=4)))
    program = writer_pure(chunk).and_then(
        lambda current: tell(
            f"chunk:{current.doc_id}:{current.start}-{current.end}"
        ).map(lambda _: current)
    ).and_then(
        lambda current: tell(f"characters:{len(current.text)}").map(
            lambda _: current
        )
    )

    value, entries = run_writer(program)

    assert value == chunk
    assert entries == ("chunk:writer:0-4", "characters:4")
