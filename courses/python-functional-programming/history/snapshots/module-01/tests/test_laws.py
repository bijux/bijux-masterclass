"""Property-based laws for the final Module 01 RAG pipeline.

These tests encode the core guarantees of the module:

- Pure and deterministic behaviour
- Canonical output (independent of input order)
- Idempotent, convergent deduplication
- Functor laws for ``fmap``
- Refactor correctness against the legacy impure implementation
"""

from __future__ import annotations

from hypothesis import given
import hypothesis.strategies as st

from .conftest import (
    doc_list_strategy,
    unique_doc_list_strategy,
    env_strategy,
    pipeline_chunk_strategy,
    raw_doc_strategy,
)
from funcpipe_rag import (
    clean_doc,
    chunk_doc,
    embed_chunk,
    structural_dedup_chunks,
    full_rag,
    docs_to_embedded,
    impure_chunks,
    fmap,
    identity,
)
from funcpipe_rag.rag_types import RawDoc, RagEnv, ChunkWithoutEmbedding


# --------------------------------------------------------------------------- #
# Core purity and determinism
# --------------------------------------------------------------------------- #


@given(docs=doc_list_strategy(), env=env_strategy())
def test_full_rag_is_pure_and_deterministic(docs: list[RawDoc], env: RagEnv) -> None:
    """Running full_rag twice with the same inputs yields identical output."""
    assert full_rag(docs, env) == full_rag(docs, env)


@given(doc=raw_doc_strategy())
def test_clean_doc_is_idempotent(doc: RawDoc) -> None:
    """Cleaning a document twice has the same effect as cleaning it once."""
    assert clean_doc(clean_doc(doc)) == clean_doc(doc)


@given(doc=raw_doc_strategy(), env=env_strategy())
def test_chunk_doc_preserves_text(doc: RawDoc, env: RagEnv) -> None:
    """chunk_doc must partition the cleaned abstract without loss or duplication."""
    cleaned = clean_doc(doc)
    reconstructed = "".join(c.text for c in chunk_doc(cleaned, env))
    assert reconstructed == cleaned.abstract


@given(text=st.text(min_size=1))
def test_embed_chunk_depends_only_on_text(text: str) -> None:
    """Embeddings depend only on the chunk text, not IDs or offsets."""
    c1 = ChunkWithoutEmbedding(doc_id="a", text=text, start=0, end=len(text))
    c2 = ChunkWithoutEmbedding(doc_id="b", text=text, start=999, end=999 + len(text))
    assert embed_chunk(c1).embedding == embed_chunk(c2).embedding


# --------------------------------------------------------------------------- #
# Canonical pipeline behaviour
# --------------------------------------------------------------------------- #


@given(docs=unique_doc_list_strategy(), env=env_strategy())
def test_full_rag_is_canonical(docs: list[RawDoc], env: RagEnv) -> None:
    """Output is independent of input document order."""
    forward = full_rag(docs, env)
    backward = full_rag(list(reversed(docs)), env)
    assert forward == backward


@given(docs=unique_doc_list_strategy(), env=env_strategy())
def test_full_rag_is_idempotent(docs: list[RawDoc], env: RagEnv) -> None:
    """Running the pipeline twice has the same effect as running it once."""
    once = full_rag(docs, env)
    twice = structural_dedup_chunks(once)
    assert once == twice


@given(chunks=st.lists(pipeline_chunk_strategy()))
def test_structural_dedup_is_idempotent(chunks) -> None:
    """Deduplication reaches a fixed point after a single pass."""
    once = structural_dedup_chunks(chunks)
    twice = structural_dedup_chunks(once)
    assert twice == once


@given(chunks=st.lists(pipeline_chunk_strategy()))
def test_structural_dedup_produces_canonical_order(chunks) -> None:
    """Deduplicated chunks are sorted by (doc_id, start)."""
    result = structural_dedup_chunks(chunks)
    expected = sorted(result, key=lambda c: (c.doc_id, c.start))
    assert result == expected


@given(chunks=st.lists(pipeline_chunk_strategy()))
def test_structural_dedup_no_duplicates(chunks):
    """Deduplicated result has no structural duplicates."""
    deduped = structural_dedup_chunks(chunks)
    keys = {(c.doc_id, c.text, c.start, c.end) for c in deduped}
    assert len(deduped) == len(keys)

@given(docs=doc_list_strategy(), env=env_strategy())
def test_full_rag_reaches_fixed_point_in_one_pass(docs: list[RawDoc], env: RagEnv) -> None:
    """Applying structural_dedup_chunks after full_rag does not change the result."""
    chunks = full_rag(docs, env)
    assert structural_dedup_chunks(chunks) == chunks


# --------------------------------------------------------------------------- #
# Functor laws for fmap
# --------------------------------------------------------------------------- #


@given(xs=st.lists(st.integers()))
def test_fmap_identity_law(xs: list[int]) -> None:
    """fmap(identity) == identity for lists."""
    assert fmap(identity)(xs) == xs


@given(xs=st.lists(st.integers()))
def test_fmap_composition_law(xs: list[int]) -> None:
    """fmap(g ∘ f) == fmap(g) ∘ fmap(f) for lists."""

    def inc(x: int) -> int:
        return x + 1

    def double(x: int) -> int:
        return x * 2

    left = fmap(lambda x: double(inc(x)))(xs)
    right = fmap(double)(fmap(inc)(xs))
    assert left == right


# --------------------------------------------------------------------------- #
# Refactor equivalence – legacy vs pure pipeline
# --------------------------------------------------------------------------- #


@given(docs=doc_list_strategy(), env=env_strategy())
def test_refactor_preserves_chunk_structure(docs: list[RawDoc], env: RagEnv) -> None:
    """Pure docs_to_embedded preserves the legacy chunk structure (sans embedding)."""
    legacy = sorted(
        (c["doc_id"], c["text"], c["start"], c["end"])
        for c in impure_chunks(docs, env)
    )
    pure = sorted(
        (c.doc_id, c.text, c.start, c.end)
        for c in docs_to_embedded(docs, env)
    )
    assert legacy == pure
