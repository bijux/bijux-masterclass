"""Executable learning proofs for the Module 06 explicit-context delta."""

from __future__ import annotations

from funcpipe_rag.core.rag_types import CleanDoc, RagEnv, RawDoc
from funcpipe_rag.rag.stages import clean_doc
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result, liftA2


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
