"""Core pipelines for the end-of-Module-09 codebase.

Module 02 established the pure, configurable API shapes.
Module 03 extends the project with streaming helpers (boundedness, grouping,
fan-in/out, time-aware pacing, and tracing) while preserving the Module 02
behaviour when you materialize at the edge.

Module 04 adds stack-safe tree traversal + folds, richer Result/Option types,
memoization, per-record error handling, breakers, retries, resource safety, and
structured error reporting for streaming pipelines.

Module 05 introduces a type-driven toolkit (`funcpipe_rag.fp`) alongside
this RAG-focused package (`funcpipe_rag.rag`).
"""

from __future__ import annotations

from funcpipe_rag.policies.breakers import (
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
from funcpipe_rag.policies.memo import DiskCache, content_hash_key, lru_cache_custom, memoize_keyed
from funcpipe_rag.policies.reports import (
    ErrGroup,
    ErrReport,
    fold_error_counts,
    fold_error_report,
    report_to_jsonable,
)
from funcpipe_rag.policies.resources import auto_close, managed_stream, nested_managed, with_resource_stream
from funcpipe_rag.streaming import multicast, throttle, trace_iter as _trace_iter
from funcpipe_rag.result import (
    Err,
    ErrInfo,
    NoneVal,
    NONE,
    Ok,
    Option,
    Result,
    Some,
    bind_option,
    bind_result,
    filter_err,
    filter_ok,
    is_err,
    is_none,
    is_ok,
    is_some,
    make_errinfo,
    map_err,
    map_option,
    map_result,
    map_result_iter,
    partition_results,
    recover,
    result_and_then,
    result_map,
    to_option,
    unwrap_or,
    unwrap_or_else,
    option_from_nullable,
    option_to_nullable,
)
from funcpipe_rag.result import (
    ResultsBoth,
    all_ok_fail_fast,
    collect_both,
    fold_results_collect_errs,
    fold_results_collect_errs_capped,
    fold_results_fail_fast,
    fold_until_error_rate,
    par_try_map_iter,
    recover_iter,
    recover_result_iter,
    split_results_to_sinks,
    split_results_to_sinks_guarded,
    tap_err,
    tap_ok,
    try_map_iter,
)
from funcpipe_rag.policies.retries import (
    RetryCtx,
    RetryDecision,
    exp_policy,
    fixed_policy,
    is_retriable_errinfo,
    restore_input_order,
    retry_map_iter,
)
from funcpipe_rag.tree import (
    assert_acyclic,
    flatten,
    flatten_via_fold,
    iter_flatten,
    iter_flatten_buffered,
    max_depth,
    recursive_flatten,
)
from funcpipe_rag.tree import (
    fold_count_length_maxdepth,
    fold_tree,
    fold_tree_buffered,
    fold_tree_no_path,
    linear_accumulate,
    linear_reduce,
    scan_count_length_maxdepth,
    scan_tree,
)
from .chunking import gen_chunk_doc, gen_chunk_spans, gen_overlapping_chunks, sliding_windows
from .rag_api import (
    full_rag_api,
    full_rag_api_docs,
    full_rag_api_path,
    iter_chunks_from_cleaned,
    iter_rag,
    iter_rag_core,
)
from .streaming_rag import (
    gen_bounded_chunks,
    gen_grouped_chunks,
    gen_stream_deduped,
    gen_stream_embedded,
    safe_rag_pipeline,
    stream_chunks,
)


__all__ = [
    # Module 04: Tree traversal + folds
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

    # Module 04: Result/Option + structured errors
    "Result",
    "Ok",
    "Err",
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
    "NoneVal",
    "NONE",
    "is_some",
    "is_none",
    "map_option",
    "bind_option",
    "unwrap_or_else",
    "option_from_nullable",
    "option_to_nullable",
    "map_result_iter",
    "filter_ok",
    "filter_err",
    "partition_results",
    "result_map",
    "result_and_then",

    # Module 04: Result streaming combinators
    "try_map_iter",
    "par_try_map_iter",
    "tap_ok",
    "tap_err",
    "recover_iter",
    "recover_result_iter",
    "split_results_to_sinks",
    "split_results_to_sinks_guarded",

    # Module 04: Aggregation
    "ResultsBoth",
    "fold_results_fail_fast",
    "fold_results_collect_errs",
    "fold_results_collect_errs_capped",
    "fold_until_error_rate",
    "all_ok_fail_fast",
    "collect_both",

    # Module 04: Breakers
    "BreakInfo",
    "short_circuit_on_err_emit",
    "short_circuit_on_err_truncate",
    "circuit_breaker_rate_emit",
    "circuit_breaker_rate_truncate",
    "circuit_breaker_count_emit",
    "circuit_breaker_count_truncate",
    "circuit_breaker_pred_emit",
    "circuit_breaker_pred_truncate",

    # Module 04: Resource safety
    "with_resource_stream",
    "managed_stream",
    "nested_managed",
    "auto_close",

    # Module 04: Retries
    "RetryCtx",
    "RetryDecision",
    "retry_map_iter",
    "fixed_policy",
    "exp_policy",
    "is_retriable_errinfo",
    "restore_input_order",

    # Module 04: Memoization
    "lru_cache_custom",
    "memoize_keyed",
    "DiskCache",
    "content_hash_key",

    # Module 04: Reports
    "ErrGroup",
    "ErrReport",
    "fold_error_counts",
    "fold_error_report",
    "report_to_jsonable",

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
