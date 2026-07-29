"""Executable learning proof for Module 01's pure RAG foundations."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from funcpipe_rag import (
    Chunk,
    ChunkWithoutEmbedding,
    RagEnv,
    RawDoc,
    chunk_doc,
    clean_doc,
    embed_chunk,
    structural_dedup_chunks,
)


def _docs() -> list[RawDoc]:
    return [
        RawDoc("doc-b", "B", "  Local   Reasoning  ", "cs.PL"),
        RawDoc("doc-a", "A", "Pure values compose", "cs.PL"),
    ]


def _run_pure_core(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    return structural_dedup_chunks(
        [
            embed_chunk(chunk)
            for doc in docs
            for chunk in chunk_doc(clean_doc(doc), env)
        ]
    )


def test_configuration_requires_an_exact_positive_integer() -> None:
    with pytest.raises((TypeError, ValueError), match="chunk_size must be an int"):
        RagEnv(chunk_size=True)
    with pytest.raises(ValueError, match="positive integer"):
        RagEnv(chunk_size=0)


def test_frozen_inputs_cannot_be_changed_in_place() -> None:
    doc = _docs()[0]

    with pytest.raises(FrozenInstanceError):
        doc.abstract = "changed"  # type: ignore[misc]


def test_cleaning_is_deterministic_and_reaches_a_fixed_point() -> None:
    doc = _docs()[0]
    cleaned = clean_doc(doc)

    assert cleaned.abstract == "local reasoning"
    assert clean_doc(doc) == cleaned
    assert clean_doc(cleaned) == cleaned


def test_chunk_offsets_reconstruct_the_cleaned_abstract() -> None:
    cleaned = clean_doc(_docs()[1])
    chunks = chunk_doc(cleaned, RagEnv(chunk_size=5))

    assert "".join(chunk.text for chunk in chunks) == cleaned.abstract
    assert [(chunk.start, chunk.end) for chunk in chunks] == [
        (0, 5),
        (5, 10),
        (10, 15),
        (15, 19),
    ]


def test_embedding_depends_on_text_not_identity_or_position() -> None:
    first = ChunkWithoutEmbedding("doc-a", "same", 0, 4)
    second = ChunkWithoutEmbedding("doc-b", "same", 100, 104)

    assert embed_chunk(first).embedding == embed_chunk(second).embedding


def test_pure_core_preserves_inputs_and_canonicalizes_output() -> None:
    docs = _docs()
    before = list(docs)
    env = RagEnv(chunk_size=6)

    forward = _run_pure_core(docs, env)
    backward = _run_pure_core(list(reversed(docs)), env)

    assert docs == before
    assert forward == backward
    assert structural_dedup_chunks(forward) == forward
