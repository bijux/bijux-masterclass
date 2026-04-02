"""Core pipelines for the end-of-Module-03 codebase.

Module 02 established the pure, configurable API shapes.
Module 03 extends the project with streaming helpers (boundedness, grouping,
fan-in/out, time-aware pacing, and tracing) while preserving the Module 02
behaviour when you materialize at the edge.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import dropwhile, groupby, islice
from operator import attrgetter
from typing import TypeVar

from funcpipe_rag.api.types import Observations, TraceLens
from funcpipe_rag.core.rules_dsl import any_doc
from funcpipe_rag.core.rules_pred import eval_pred
from funcpipe_rag.core.structural_dedup import structural_dedup_lazy
from funcpipe_rag.fp import (
    StageInstrumentation,
    ffilter,
    flatmap,
    fmap,
    instrument_stage,
)
from funcpipe_rag.streaming import ensure_contiguous, trace_iter as _trace_iter
from funcpipe_rag.pipeline_stages import (
    embed_chunk,
    iter_chunk_doc,
    iter_chunk_spans,
    iter_overlapping_chunks_text,
    structural_dedup_chunks,
)
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


def gen_chunk_spans(doc: CleanDoc, env: RagEnv) -> Iterator[tuple[int, int]]:
    """Yield chunk spans lazily (zero-copy alternative to ``gen_chunk_doc``)."""

    yield from iter_chunk_spans(doc, env)


def gen_overlapping_chunks(
    doc_id: str,
    text: str,
    *,
    k: int,
    o: int = 0,
    tail_policy: str = "emit_short",
) -> Iterator[ChunkWithoutEmbedding]:
    """Chunk raw text lazily with overlap and a tail policy (Module 03)."""

    yield from iter_overlapping_chunks_text(doc_id, text, k=k, o=o, tail_policy=tail_policy)


def sliding_windows(items: Iterable[T], w: int) -> Iterator[tuple[T, ...]]:
    """Yield a sliding window of size ``w`` over ``items`` using bounded auxiliary space."""

    if w <= 0:
        raise ValueError("window size must be > 0")

    it = iter(items)
    buf: deque[T] = deque(maxlen=w)
    for _ in range(w - 1):
        try:
            buf.append(next(it))
        except StopIteration:
            return
    for x in it:
        buf.append(x)
        yield tuple(buf)


def gen_grouped_chunks(
    chunks: Iterable[ChunkWithoutEmbedding],
) -> Iterator[tuple[str, Iterator[ChunkWithoutEmbedding]]]:
    """Group contiguous chunk runs by ``doc_id`` (Module 03)."""

    guarded = ensure_contiguous(attrgetter("doc_id"))(chunks)
    yield from groupby(guarded, key=attrgetter("doc_id"))


def stream_chunks(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    trace_docs: TraceLens[RawDoc] | None = None,
    trace_cleaned: TraceLens[CleanDoc] | None = None,
    trace_chunks: TraceLens[ChunkWithoutEmbedding] | None = None,
) -> Iterator[ChunkWithoutEmbedding]:
    """Streaming chunks core: filter → clean → chunk (no embedding, no dedup)."""

    stream: Iterable[RawDoc] = docs
    if trace_docs is not None:
        stream = _trace_iter(stream, trace_docs)

    kept = (d for d in stream if eval_pred(d, config.keep.keep_pred))
    cleaned: Iterable[CleanDoc] = (deps.cleaner(d) for d in kept)
    if trace_cleaned is not None:
        cleaned = _trace_iter(cleaned, trace_cleaned)

    chunked: Iterable[ChunkWithoutEmbedding] = (c for cd in cleaned for c in gen_chunk_doc(cd, config.env))
    if trace_chunks is not None:
        chunked = _trace_iter(chunked, trace_chunks)
    yield from chunked


def gen_stream_embedded(
    chunks: Iterable[ChunkWithoutEmbedding],
    embedder: Callable[[ChunkWithoutEmbedding], Chunk],
    *,
    trace_embedded: TraceLens[Chunk] | None = None,
) -> Iterator[Chunk]:
    """Streaming embedding stage: chunk_without_embedding → chunk."""

    embedded: Iterable[Chunk] = (embedder(c) for c in chunks)
    if trace_embedded is not None:
        embedded = _trace_iter(embedded, trace_embedded)
    yield from embedded


def gen_stream_deduped(chunks: Iterable[Chunk]) -> Iterator[Chunk]:
    """Streaming structural dedup stage (order-preserving)."""

    yield from structural_dedup_lazy(chunks)


def gen_bounded_chunks(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    max_chunks: int | None = None,
) -> Iterator[ChunkWithoutEmbedding]:
    """Hard fence on the number of chunks produced (Module 03)."""

    chunked = stream_chunks(docs, config, deps)
    if max_chunks is None:
        yield from chunked
        return
    yield from islice(chunked, max_chunks)


def safe_rag_pipeline(
    docs: Iterable[RawDoc],
    config: RagConfig,
    deps: RagCoreDeps,
    *,
    max_chunks: int = 10_000,
    min_doc_len: int = 500,
) -> Iterator[ChunkWithoutEmbedding]:
    """Defensive streaming pipeline with explicit fences (Module 03)."""

    fenced_docs = dropwhile(lambda d: len(d.abstract) < min_doc_len, docs)
    yield from gen_bounded_chunks(fenced_docs, config, deps, max_chunks=max_chunks)


def multicast(items: Iterable[T], n: int, *, maxlen: int = 1024) -> tuple[Iterator[T], ...]:
    """Bounded multicast: returns ``n`` independent iterators over the same stream.

    Raises BufferError if consumer skew exceeds maxlen.
    """

    if n <= 0:
        raise ValueError("n must be > 0")
    if maxlen <= 0:
        raise ValueError("maxlen must be > 0")

    upstream = iter(items)
    queues: list[deque[object]] = [deque() for _ in range(n)]
    done = False
    sentinel = object()

    def pump_once() -> None:
        nonlocal done
        if done:
            return
        try:
            x: object = next(upstream)
        except StopIteration:
            done = True
            for q in queues:
                q.append(sentinel)
            return
        for q in queues:
            if len(q) >= maxlen:
                raise BufferError(f"multicast buffer exceeded (maxlen={maxlen})")
            q.append(x)

    def sub(i: int) -> Iterator[T]:
        while True:
            if not queues[i]:
                pump_once()
            item = queues[i].popleft()
            if item is sentinel:
                return
            yield item  # type: ignore[misc]

    return tuple(sub(i) for i in range(n))


def throttle(
    items: Iterable[T],
    *,
    min_delta: float,
    clock: Callable[[], float],
    sleeper: Callable[[float], None],
) -> Iterator[T]:
    """Yield items while enforcing a minimum spacing between emissions."""

    if min_delta < 0:
        raise ValueError("min_delta must be >= 0")

    last_emit: float | None = None
    for item in items:
        now = clock()
        if last_emit is not None:
            wait = max(0.0, (last_emit + min_delta) - now)
            if wait > 0:
                sleeper(wait)
                now = clock()
        last_emit = now
        yield item


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
    """Doc-based API shape used across Modules 02–03 cores."""

    return full_rag_api_docs(docs, config, deps)


def full_rag_api_path(
    path: str,
    config: RagConfig,
    deps: RagBoundaryDeps,
) -> Result[tuple[list[Chunk], Observations]]:
    """Boundary API shape (introduced in M02C05): path in, Result out."""

    docs_res = deps.reader.read_docs(path)
    if isinstance(docs_res, Err):
        return docs_res
    chunks, obs = full_rag_api_docs(docs_res.value, config, deps.core)
    return Ok((chunks, obs))


__all__ = [
    "_trace_iter",
    "gen_chunk_doc",
    "gen_chunk_spans",
    "gen_overlapping_chunks",
    "sliding_windows",
    "gen_grouped_chunks",
    "stream_chunks",
    "gen_stream_embedded",
    "gen_stream_deduped",
    "gen_bounded_chunks",
    "safe_rag_pipeline",
    "multicast",
    "throttle",
    "iter_rag",
    "iter_rag_core",
    "iter_chunks_from_cleaned",
    "full_rag_api",
    "full_rag_api_docs",
    "full_rag_api_path",
]
