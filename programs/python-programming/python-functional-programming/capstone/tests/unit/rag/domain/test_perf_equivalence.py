from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from funcpipe_rag.rag.domain import (
    AssembledChunk,
    ChunkMetadata,
    ChunkText,
    embedding_batches_equivalent,
    process_batch_hybrid,
)

chunk_strat = st.builds(
    AssembledChunk,
    text=st.builds(ChunkText, content=st.text(min_size=1, max_size=100)),
    metadata=st.builds(
        ChunkMetadata,
        source=st.text(max_size=20),
        tags=st.lists(st.text(min_size=1, max_size=10), max_size=5).map(tuple),
        embedding_model=st.none() | st.text(min_size=1, max_size=10),
        expected_dim=st.none(),
    ),
    embedding=st.none(),
)


@given(batch=st.lists(chunk_strat, min_size=1, max_size=50))
def test_pure_vs_hybrid_equivalence(batch: list[AssembledChunk]) -> None:
    pure = process_batch_hybrid(batch, mode="pure")
    hybrid = process_batch_hybrid(batch, mode="hybrid")

    assert embedding_batches_equivalent(pure, hybrid)
