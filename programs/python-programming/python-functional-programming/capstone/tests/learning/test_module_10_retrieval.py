from __future__ import annotations

import pytest

from funcpipe_rag.core.rag_types import Chunk, ChunkWithoutEmbedding, RagEnv, RawDoc
from funcpipe_rag.rag import (
    LOCAL_EMBEDDING_MODEL,
    cosine_similarity,
    make_query,
    retrieve,
)
from funcpipe_rag.rag.domain import Embedding, RankedChunk, SearchQuery
from funcpipe_rag.rag.rag_api import iter_rag
from funcpipe_rag.rag.stages import clean_doc, embed_chunk, embed_text


def test_query_and_chunk_text_share_one_embedding_contract() -> None:
    chunk = ChunkWithoutEmbedding(
        doc_id="rag-embedding",
        text="one local vector contract",
        start=0,
        end=25,
    )

    vector = embed_text(chunk.text)

    assert len(vector) == 16
    assert vector == embed_text(chunk.text)
    assert embed_chunk(chunk).embedding == vector


def test_retrieval_values_reject_ambiguous_query_and_rank_states() -> None:
    indexed = embed_chunk(
        ChunkWithoutEmbedding(
            doc_id="rag-values",
            text="retrieval values",
            start=0,
            end=16,
        )
    )
    query = SearchQuery(
        text="typed retrieval",
        embedding=Embedding(vector=embed_text("typed retrieval"), model=LOCAL_EMBEDDING_MODEL),
        top_k=3,
    )
    hit = RankedChunk(chunk=indexed, score=0.75, rank=1)

    assert query.embedding.dim == len(indexed.embedding)
    assert (hit.chunk.doc_id, hit.score, hit.rank) == ("rag-values", 0.75, 1)
    with pytest.raises(ValueError, match="must not be blank"):
        SearchQuery(text=" ", embedding=query.embedding, top_k=3)
    with pytest.raises(ValueError, match="positive integer"):
        SearchQuery(text="typed retrieval", embedding=query.embedding, top_k=0)
    with pytest.raises(ValueError, match="must not be empty"):
        SearchQuery(
            text="typed retrieval",
            embedding=Embedding(vector=(), model=LOCAL_EMBEDDING_MODEL),
            top_k=3,
        )
    with pytest.raises(ValueError, match="between -1 and 1"):
        RankedChunk(chunk=indexed, score=float("nan"), rank=1)
    with pytest.raises(ValueError, match="positive integer"):
        RankedChunk(chunk=indexed, score=0.75, rank=0)


def test_retrieval_ranks_by_score_then_stable_chunk_coordinates() -> None:
    exact_vector = (1.0,) + (0.0,) * 15
    lower_vector = (0.0, 1.0) + (0.0,) * 14
    tie_b = Chunk("b", "later tie", 0, 9, embedding=exact_vector)
    lower = Chunk("c", "lower score", 0, 11, embedding=lower_vector)
    tie_a = Chunk("a", "earlier tie", 0, 11, embedding=exact_vector)
    query = SearchQuery(
        text="stable ranking",
        embedding=Embedding(vector=exact_vector, model=LOCAL_EMBEDDING_MODEL),
        top_k=2,
    )

    hits = retrieve(query, (tie_b, lower, tie_a))

    assert tuple(hit.chunk.doc_id for hit in hits) == ("a", "b")
    assert tuple(hit.rank for hit in hits) == (1, 2)
    assert tuple(hit.score for hit in hits) == pytest.approx((1.0, 1.0))
    with pytest.raises(ValueError, match="same non-zero dimension"):
        cosine_similarity((1.0,), (1.0, 0.0))
    with pytest.raises(ValueError, match="must be non-zero"):
        cosine_similarity((0.0, 0.0), (1.0, 0.0))


def test_live_rag_flow_indexes_then_retrieves_an_exact_local_match() -> None:
    docs = (
        RawDoc("other", "Effects", "boundary effects", "fp"),
        RawDoc("exact", "Retrieval", "typed retrieval", "fp"),
    )
    chunks = tuple(iter_rag(docs, RagEnv(chunk_size=80), clean_doc))

    hits = retrieve(make_query("typed retrieval", top_k=1), chunks)

    assert len(chunks) == 2
    assert len(hits) == 1
    assert hits[0].chunk.doc_id == "exact"
    assert hits[0].chunk.text == "typed retrieval"
    assert hits[0].score == pytest.approx(1.0)
