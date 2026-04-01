from __future__ import annotations

from funcpipe_rag.core.rag_types import ChunkWithoutEmbedding
from funcpipe_rag.domain.effects import perform
from funcpipe_rag.domain.facades import Keyed, deterministic_embedder_port
from funcpipe_rag.rag.stages import embed_chunk
from funcpipe_rag.result.types import Ok


def test_facade_returns_description_not_effect() -> None:
    calls = 0

    def embed_one(_c: ChunkWithoutEmbedding):
        nonlocal calls
        calls += 1
        return embed_chunk(_c)

    port = deterministic_embedder_port(embed_one=embed_one)
    plan = port.embed_batch([Keyed(key="k", value=ChunkWithoutEmbedding("d", "x", 0, 1))])
    assert calls == 0
    _ = perform(plan)
    assert calls == 1


def test_facade_interpretation_produces_ok() -> None:
    port = deterministic_embedder_port()
    plan = port.embed_batch([Keyed(key="k", value=ChunkWithoutEmbedding("d", "x", 0, 1))])
    res = perform(plan)
    assert isinstance(res, Ok)
    assert res.value[0].key == "k"
