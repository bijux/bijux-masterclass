"""funcpipe_rag – end-of-Module-03 codebase.

This package is the consolidated project state at the end of Module 03:
- Immutable domain types
- Pure pipeline stages + canonical structural de-duplication
- Config-as-data + closure-based configurators
- Tiny rules DSLs (data and functions) + safe parsing guard
- Lazy combinators + debugging taps/probes
- Streaming helpers for lazy iteration (Module 03)
- Boundary-friendly Result helpers and thin shells
"""

from __future__ import annotations

# Domain value types – immutable, hashable where needed
from .rag_types import (
    RawDoc,
    CleanDoc,
    ChunkWithoutEmbedding,
    Chunk,
    RagEnv,
)

# Pure pipeline stages – the building blocks
from .pipeline_stages import (
    clean_doc,
    chunk_doc,
    iter_chunk_spans,
    iter_chunk_doc,
    iter_overlapping_chunks_text,
    embed_chunk,
    structural_dedup_chunks,
)
from .core.structural_dedup import DedupIterator, structural_dedup_lazy

# Functional composition helpers (Modules 02–03)
from .fp import (
    FakeTime,
    StageInstrumentation,
    compose,
    flow,
    ffilter,
    flatmap,
    fmap,
    identity,
    instrument_stage,
    pipe,
    probe,
    producer_pipeline,
    tee,
)

# Modules 02–03 public API layer
from .result import Ok, Err, Result, result_map, result_and_then
from .api.clean_cfg import CleanConfig, DEFAULT_CLEAN_CONFIG, make_cleaner
from .api.types import DocRule, RagTaps, DebugConfig, Observations
from .api.types import RagTraceV3, TraceLens
from .core.rules_pred import (
    Pred,
    Eq,
    LenGt,
    StartsWith,
    All,
    AnyOf,
    Not,
    RulesConfig,
    DEFAULT_RULES,
    eval_pred,
)
from .core.rules_dsl import (
    any_doc,
    none_doc,
    category_startswith,
    title_contains,
    abstract_min_len,
    rule_and,
    rule_or,
    rule_not,
    rule_all,
    parse_rule,
)
from .core.rules_lint import SafeVisitor, assert_rule_is_safe_expr
from .api.config import (
    RagConfig,
    RagCoreDeps,
    RagBoundaryDeps,
    Reader,
    get_deps,
    make_rag_fn,
    make_gen_rag_fn,
    boundary_rag_config,
)
from .api.core import (
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
from .shells.rag_api_shell import FSReader, write_chunks_jsonl
from .app_config import AppConfig
from .streaming import (
    Source,
    Transform,
    as_source,
    ensure_contiguous,
    fence_k,
    fork2_lockstep,
    make_chain,
    make_counter,
    make_merge,
    make_peek,
    make_rate_limit,
    make_roundrobin,
    make_sampler_bernoulli,
    make_sampler_periodic,
    make_sampler_stable,
    make_tap,
    make_throttle,
    make_timestamp,
    make_call_gate,
    tap_prefix,
    trace_iter,
    compose2_transforms,
    compose_transforms,
    source_to_transform,
)


__all__ = [
    # Types
    "RawDoc",
    "CleanDoc",
    "ChunkWithoutEmbedding",
    "Chunk",
    "RagEnv",

    # Pure stages
    "clean_doc",
    "chunk_doc",
    "iter_chunk_spans",
    "iter_chunk_doc",
    "iter_overlapping_chunks_text",
    "embed_chunk",
    "structural_dedup_chunks",
    "DedupIterator",
    "structural_dedup_lazy",

    # Functional composition
    "identity",
    "compose",
    "flow",
    "producer_pipeline",
    "pipe",
    "fmap",
    "ffilter",
    "flatmap",
    "tee",
    "probe",
    "StageInstrumentation",
    "instrument_stage",
    "FakeTime",

    # Result + boundary helpers (Modules 02–03)
    "Ok",
    "Err",
    "Result",
    "result_map",
    "result_and_then",

    # Rules (Modules 02–03)
    "DocRule",
    "Pred",
    "Eq",
    "LenGt",
    "StartsWith",
    "All",
    "AnyOf",
    "Not",
    "RulesConfig",
    "DEFAULT_RULES",
    "eval_pred",
    "any_doc",
    "none_doc",
    "category_startswith",
    "title_contains",
    "abstract_min_len",
    "rule_and",
    "rule_or",
    "rule_not",
    "rule_all",
    "parse_rule",
    "SafeVisitor",
    "assert_rule_is_safe_expr",

    # Config + API (Modules 02–03)
    "CleanConfig",
    "DEFAULT_CLEAN_CONFIG",
    "make_cleaner",
    "RagTaps",
    "DebugConfig",
    "Observations",
    "TraceLens",
    "RagTraceV3",
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
    "FSReader",
    "write_chunks_jsonl",
    "AppConfig",

    # Module 03: generic streaming helpers
    "Source",
    "Transform",
    "trace_iter",
    "fence_k",
    "compose2_transforms",
    "compose_transforms",
    "source_to_transform",
    "tap_prefix",
    "make_chain",
    "make_roundrobin",
    "make_merge",
    "fork2_lockstep",
    "make_throttle",
    "make_rate_limit",
    "make_timestamp",
    "make_call_gate",
    "make_tap",
    "make_counter",
    "make_sampler_bernoulli",
    "make_sampler_periodic",
    "make_sampler_stable",
    "make_peek",
    "ensure_contiguous",
    "as_source",
]

__version__ = "0.1.0"
