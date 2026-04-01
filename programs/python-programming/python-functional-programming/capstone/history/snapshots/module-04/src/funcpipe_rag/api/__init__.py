"""Public APIs for the end-of-Module-04 codebase.

Module 03 adds streaming helpers; Module 04 adds tree-safe recursion, Result/Option
per-record failures, memoization, breakers/retries, and structured error reporting.
"""

from .types import DocRule, RagTaps, DebugConfig, Observations, TraceLens, RagTraceV3
from .clean_cfg import CleanConfig, make_cleaner, DEFAULT_CLEAN_CONFIG
from .config import (
    RagConfig,
    RagCoreDeps,
    RagBoundaryDeps,
    Reader,
    get_deps,
    make_rag_fn,
    make_gen_rag_fn,
    boundary_rag_config,
)
from .core import (
    _trace_iter,
    gen_chunk_doc,
    gen_chunk_spans,
    gen_overlapping_chunks,
    iter_rag,
    iter_rag_core,
    stream_chunks,
    gen_stream_embedded,
    gen_stream_deduped,
    sliding_windows,
    gen_grouped_chunks,
    gen_bounded_chunks,
    safe_rag_pipeline,
    multicast,
    throttle,
    iter_chunks_from_cleaned,
    full_rag_api,
    full_rag_api_docs,
    full_rag_api_path,
)

__all__ = [
    "DocRule",
    "RagTaps",
    "DebugConfig",
    "Observations",
    "TraceLens",
    "RagTraceV3",
    "CleanConfig",
    "DEFAULT_CLEAN_CONFIG",
    "make_cleaner",
    "RagConfig",
    "RagCoreDeps",
    "Reader",
    "RagBoundaryDeps",
    "get_deps",
    "make_rag_fn",
    "make_gen_rag_fn",
    "boundary_rag_config",
    "_trace_iter",
    "gen_chunk_doc",
    "gen_chunk_spans",
    "gen_overlapping_chunks",
    "iter_rag",
    "iter_rag_core",
    "stream_chunks",
    "gen_stream_embedded",
    "gen_stream_deduped",
    "sliding_windows",
    "gen_grouped_chunks",
    "gen_bounded_chunks",
    "safe_rag_pipeline",
    "multicast",
    "throttle",
    "iter_chunks_from_cleaned",
    "full_rag_api",
    "full_rag_api_docs",
    "full_rag_api_path",
]
