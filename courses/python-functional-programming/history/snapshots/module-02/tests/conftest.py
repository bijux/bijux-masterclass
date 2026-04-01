"""Shared Hypothesis strategies used across the test suite."""

from __future__ import annotations

import hashlib
import hypothesis.strategies as st
from hypothesis.strategies import SearchStrategy

from funcpipe_rag.rag_types import RawDoc, RagEnv, Chunk


def raw_doc_strategy() -> SearchStrategy[RawDoc]:
    """Strategy producing RawDoc instances with realistic text fields."""
    return st.builds(
        RawDoc,
        doc_id=st.text(
            min_size=1,
            max_size=20,
            alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_",
        ),
        title=st.text(max_size=100),
        abstract=st.text(max_size=2000),
        categories=st.text(max_size=50),
    )


def doc_list_strategy() -> SearchStrategy[list[RawDoc]]:
    """Strategy emitting small batches of RawDoc inputs."""
    return st.lists(raw_doc_strategy(), max_size=50)


def unique_doc_list_strategy() -> SearchStrategy[list[RawDoc]]:
    """Strategy emitting RawDoc lists with unique doc_id values."""
    return st.lists(raw_doc_strategy(), max_size=50, unique_by=lambda d: d.doc_id)


def env_strategy() -> SearchStrategy[RagEnv]:
    """Strategy varying RagEnv.chunk_size in a practical range."""
    return st.builds(RagEnv, chunk_size=st.integers(min_value=128, max_value=1024))


@st.composite
def pipeline_chunk_strategy(draw) -> Chunk:
    """Strategy for Chunk instances respecting the production embedding invariant."""
    text = draw(st.text(min_size=1))
    start = draw(st.integers(min_value=0))
    end = start + len(text)

    # Embedding mirrors the production rule (SHA256 → 16 floats in [0.0, 1.0]).
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    step = 4
    vec = tuple(int(h[i : i + step], 16) / (16**step - 1) for i in range(0, 64, step))

    doc_id = draw(st.text(min_size=1))
    return Chunk(doc_id, text, start, end, vec)
