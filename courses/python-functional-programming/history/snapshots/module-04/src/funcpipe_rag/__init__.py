"""funcpipe_rag – end-of-Module-04 codebase.

This package is the consolidated project state at the end of Module 04:
- Immutable domain types
- Pure pipeline stages + canonical structural de-duplication
- Config-as-data + closure-based configurators
- Tiny rules DSLs (data and functions) + safe parsing guard
- Lazy combinators + debugging taps/probes
- Streaming helpers for lazy iteration (Module 03)
- Tree-safe recursion (TreeDoc) with stack-safe flatten + folds (Module 04)
- Result/Option for per-record failures + structured ErrInfo (Module 04)
- Memoization, breakers, retries, resource safety, and error reports (Module 04)
"""

from __future__ import annotations

# Domain value types – immutable, hashable where needed
from .rag_types import (
    RawDoc,
    CleanDoc,
    ChunkWithoutEmbedding,
    Chunk,
    RagEnv,
    TextNode,
    TreeDoc,
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

# Modules 02–04 public API layer (end-of-Module-04)
from .result import (
    Result,
    Ok,
    Err,
    ErrInfo,
    make_errinfo,
    is_ok,
    is_err,
    map_result,
    map_err,
    bind_result,
    recover,
    unwrap_or,
    to_option,
    Option,
    Some,
    Nothing,
    is_some,
    is_nothing,
    map_option,
    bind_option,
    unwrap_or_else,
    map_result_iter,
    filter_ok,
    filter_err,
    partition_results,
    result_map,
    result_and_then,
)
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
    iter_chunks_from_cleaned,
    full_rag_api,
    full_rag_api_docs,
    full_rag_api_path,
)
from .policies.breakers import (
    BreakInfo,
    circuit_breaker_count_emit,
    circuit_breaker_count_truncate,
    circuit_breaker_pred_emit,
    circuit_breaker_pred_truncate,
    circuit_breaker_rate_emit,
    circuit_breaker_rate_truncate,
    short_circuit_on_err_emit,
    short_circuit_on_err_truncate,
)
from .policies.memo import DiskCache, content_hash_key, lru_cache_custom, memoize_keyed
from .policies.reports import ErrGroup, ErrReport, fold_error_counts, fold_error_report, report_to_jsonable
from .policies.resources import auto_close, managed_stream, nested_managed, with_resource_stream
from .policies.retries import (
    RetryCtx,
    RetryDecision,
    exp_policy,
    fixed_policy,
    is_retriable_errinfo,
    restore_input_order,
    retry_map_iter,
)
from .tree import (
    assert_acyclic,
    flatten,
    flatten_via_fold,
    iter_flatten,
    iter_flatten_buffered,
    max_depth,
    recursive_flatten,
)
from .tree import (
    fold_count_length_maxdepth,
    fold_tree,
    fold_tree_buffered,
    fold_tree_no_path,
    linear_accumulate,
    linear_reduce,
    scan_count_length_maxdepth,
    scan_tree,
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
    multicast,
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
    throttle,
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
    "TextNode",
    "TreeDoc",

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

    # Result/Option + structured errors (Module 04; includes legacy aliases)
    "Ok",
    "Err",
    "Result",
    "ErrInfo",
    "make_errinfo",
    "is_ok",
    "is_err",
    "map_result",
    "map_err",
    "bind_result",
    "recover",
    "unwrap_or",
    "to_option",
    "Option",
    "Some",
    "Nothing",
    "is_some",
    "is_nothing",
    "map_option",
    "bind_option",
    "unwrap_or_else",
    "map_result_iter",
    "filter_ok",
    "filter_err",
    "partition_results",
    "result_map",
    "result_and_then",

    # Tree traversal + folds (Module 04)
    "assert_acyclic",
    "flatten",
    "recursive_flatten",
    "iter_flatten",
    "iter_flatten_buffered",
    "flatten_via_fold",
    "max_depth",
    "fold_tree",
    "fold_tree_no_path",
    "fold_tree_buffered",
    "scan_tree",
    "linear_reduce",
    "linear_accumulate",
    "fold_count_length_maxdepth",
    "scan_count_length_maxdepth",

    # Memoization (Module 04)
    "lru_cache_custom",
    "memoize_keyed",
    "DiskCache",
    "content_hash_key",

    # Result stream combinators (Module 04)
    "try_map_iter",
    "par_try_map_iter",
    "tap_ok",
    "tap_err",
    "recover_iter",
    "recover_result_iter",
    "split_results_to_sinks",
    "split_results_to_sinks_guarded",

    # Result stream aggregation (Module 04)
    "ResultsBoth",
    "fold_results_fail_fast",
    "fold_results_collect_errs",
    "fold_results_collect_errs_capped",
    "fold_until_error_rate",
    "all_ok_fail_fast",
    "collect_both",

    # Breakers (Module 04)
    "BreakInfo",
    "short_circuit_on_err_emit",
    "short_circuit_on_err_truncate",
    "circuit_breaker_rate_emit",
    "circuit_breaker_rate_truncate",
    "circuit_breaker_count_emit",
    "circuit_breaker_count_truncate",
    "circuit_breaker_pred_emit",
    "circuit_breaker_pred_truncate",

    # Resource safety (Module 04)
    "with_resource_stream",
    "managed_stream",
    "nested_managed",
    "auto_close",

    # Retries (Module 04)
    "RetryCtx",
    "RetryDecision",
    "retry_map_iter",
    "fixed_policy",
    "exp_policy",
    "is_retriable_errinfo",
    "restore_input_order",

    # Error reporting (Module 04)
    "ErrGroup",
    "ErrReport",
    "fold_error_counts",
    "fold_error_report",
    "report_to_jsonable",

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
