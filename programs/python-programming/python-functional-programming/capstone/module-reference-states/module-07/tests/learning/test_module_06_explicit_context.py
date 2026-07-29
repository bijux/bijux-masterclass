"""Executable learning proofs for the Module 06 explicit-context delta."""

from __future__ import annotations

from funcpipe_rag.core.rag_types import CleanDoc, RawDoc
from funcpipe_rag.rag.stages import clean_doc
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result


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
