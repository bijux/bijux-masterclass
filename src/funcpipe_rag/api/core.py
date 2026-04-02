"""Module-02 core pipelines (pure, configurable, and mostly lazy)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import TypeVar

from funcpipe_rag.api.types import Observations
from funcpipe_rag.core.rules_dsl import any_doc
from funcpipe_rag.core.rules_pred import eval_pred
from funcpipe_rag.fp import (
    StageInstrumentation,
    ffilter,
    flatmap,
    fmap,
    instrument_stage,
)
from funcpipe_rag.pipeline_stages import embed_chunk, structural_dedup_chunks
from funcpipe_rag.pipeline_stages import iter_chunk_doc
from funcpipe_rag.rag_types import Chunk, ChunkWithoutEmbedding, CleanDoc, DocRule, RawDoc, RagEnv
from funcpipe_rag.result import Err, Ok, Result

from .config import RagBoundaryDeps, RagConfig, RagCoreDeps

T = TypeVar("T")


def _identity_iter(items: Iterable[RawDoc]) -> Iterable[RawDoc]:
    return items


def _tap(items: Sequence[T], handler: Callable[[tuple[T, ...]], None] | None) -> Sequence[T]:
    if handler is not None:
        handler(tuple(items))
    return items


def gen_chunk_doc(doc: CleanDoc, env: RagEnv) -> Iterator[ChunkWithoutEmbedding]:
    """Yield chunk metadata lazily (generator form of ``chunk_doc``)."""
    yield from iter_chunk_doc(doc, env)


def iter_rag(
    docs: Iterable[RawDoc],
    env: RagEnv,
    cleaner: Callable[[RawDoc], CleanDoc],
    *,
    keep: DocRule | None = None,
) -> Iterator[Chunk]:
    """Module-02 lazy core: filter → clean → chunk → embed (no dedup)."""

    rule = keep if keep is not None else any_doc
    kept_docs = (d for d in docs if rule(d))
    cleaned = (cleaner(d) for d in kept_docs)
    chunk_we = (c for cd in cleaned for c in gen_chunk_doc(cd, env))
    embedded = (embed_chunk(c) for c in chunk_we)
    yield from embedded


def iter_rag_core(docs: Iterable[RawDoc], config: RagConfig, deps: RagCoreDeps) -> Iterator[Chunk]:
    """Parametric streaming core: filter (RulesConfig) → clean → chunk → embed."""

    def keep_rule(doc: RawDoc) -> bool:
        return eval_pred(doc, config.keep.keep_pred)

    def check_chunk(chunk: ChunkWithoutEmbedding) -> None:
        if chunk.start < 0 or chunk.end < chunk.start:
            raise ValueError("Invalid chunk offsets")

    def chunker(doc: CleanDoc) -> Iterable[ChunkWithoutEmbedding]:
        return gen_chunk_doc(doc, config.env)

    kept_stage = instrument_stage(
        ffilter(keep_rule),
        stage_name="kept",
        instrumentation=StageInstrumentation(trace=config.debug.trace_kept),
    )
    clean_stage = instrument_stage(
        fmap(deps.cleaner),
        stage_name="clean",
        instrumentation=StageInstrumentation(trace=config.debug.trace_clean),
    )

    chunk_stage = instrument_stage(
        flatmap(chunker),
        stage_name="chunks",
        instrumentation=StageInstrumentation(
            trace=config.debug.trace_chunks,
            probe_fn=check_chunk if config.debug.probe_chunks else None,
        ),
    )
    embed_stage = instrument_stage(
        fmap(deps.embedder),
        stage_name="embedded",
        instrumentation=StageInstrumentation(trace=config.debug.trace_embedded),
    )

    stream: Iterable[RawDoc] = docs
    if config.debug.trace_docs:
        stream = instrument_stage(
            _identity_iter,
            stage_name="docs",
            instrumentation=StageInstrumentation(trace=True),
        )(stream)
    stream_kept = kept_stage(stream)
    stream_cleaned = clean_stage(stream_kept)
    stream_chunked = chunk_stage(stream_cleaned)
    stream_embedded = embed_stage(stream_chunked)
    yield from stream_embedded


def iter_chunks_from_cleaned(
    cleaned: Iterable[CleanDoc],
    config: RagConfig,
    embedder: Callable[[ChunkWithoutEmbedding], Chunk],
) -> Iterator[Chunk]:
    """Streaming sub-core: chunk + embed from cleaned docs."""

    for cd in cleaned:
        for chunk in gen_chunk_doc(cd, config.env):
            yield embedder(chunk)


def full_rag_api_docs(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
) -> tuple[list[Chunk], Observations]:
    """Doc-based API: materializes at the edge for taps/observations."""

    docs_list = list(docs)
    sample_size = config.env.sample_size

    kept_docs = [d for d in docs_list if eval_pred(d, config.keep.keep_pred)]
    _tap(kept_docs, deps.taps.docs if deps.taps else None)

    cleaned = [deps.cleaner(d) for d in kept_docs]
    _tap(cleaned, deps.taps.cleaned if deps.taps else None)

    chunks_pre_dedup = list(iter_chunks_from_cleaned(cleaned, config, deps.embedder))
    _tap(chunks_pre_dedup, deps.taps.chunks if deps.taps else None)

    chunks = structural_dedup_chunks(chunks_pre_dedup)
    obs = Observations(
        total_docs=len(docs_list),
        kept_docs=len(kept_docs),
        cleaned_docs=len(cleaned),
        total_chunks=len(chunks),
        sample_doc_ids=tuple(d.doc_id for d in kept_docs[:sample_size]),
        sample_chunk_starts=tuple(c.start for c in chunks[:sample_size]),
        extra=(),
        warnings=(),
    )
    return chunks, obs


def full_rag_api(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
) -> tuple[list[Chunk], Observations]:
    """Doc-based API shape used across Module 02 cores."""

    return full_rag_api_docs(docs, config, deps)


def full_rag_api_path(
    path: str,
    config: RagConfig,
    deps: RagBoundaryDeps,
) -> Result[tuple[list[Chunk], Observations]]:
    """Boundary API shape (M02C05): path in, Result out."""

    docs_res = deps.reader.read_docs(path)
    if isinstance(docs_res, Err):
        return docs_res
    chunks, obs = full_rag_api_docs(docs_res.value, config, deps.core)
    return Ok((chunks, obs))


__all__ = [
    "gen_chunk_doc",
    "iter_rag",
    "iter_rag_core",
    "iter_chunks_from_cleaned",
    "full_rag_api",
    "full_rag_api_docs",
    "full_rag_api_path",
]
