"""funcpipe_rag – end-of-Module-02 codebase.

This package is the consolidated project state at the end of Module 02:
- Immutable domain types
- Pure pipeline stages + canonical structural de-duplication
- Config-as-data + closure-based configurators
- Tiny rules DSLs (data and functions) + safe parsing guard
- Lazy combinators + debugging taps/probes
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
    iter_chunk_doc,
    embed_chunk,
    structural_dedup_chunks,
)

# Functional composition helpers (Module 02)
from .fp import (
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

# Module 02 public API layer
from .result import Ok, Err, Result, result_map, result_and_then
from .api.clean_cfg import CleanConfig, DEFAULT_CLEAN_CONFIG, make_cleaner
from .api.types import DocRule, RagTaps, DebugConfig, Observations
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
    boundary_rag_config,
)
from .api.core import (
    gen_chunk_doc,
    iter_rag,
    iter_rag_core,
    iter_chunks_from_cleaned,
    full_rag_api,
    full_rag_api_docs,
    full_rag_api_path,
)
from .shells.rag_api_shell import FSReader, write_chunks_jsonl
from .app_config import AppConfig


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
    "iter_chunk_doc",
    "embed_chunk",
    "structural_dedup_chunks",

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

    # Result + boundary helpers (Module 02)
    "Ok",
    "Err",
    "Result",
    "result_map",
    "result_and_then",

    # Rules (Module 02)
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

    # Config + API (Module 02)
    "CleanConfig",
    "DEFAULT_CLEAN_CONFIG",
    "make_cleaner",
    "RagTaps",
    "DebugConfig",
    "Observations",
    "RagConfig",
    "RagCoreDeps",
    "Reader",
    "RagBoundaryDeps",
    "get_deps",
    "make_rag_fn",
    "boundary_rag_config",
    "gen_chunk_doc",
    "iter_rag",
    "iter_rag_core",
    "iter_chunks_from_cleaned",
    "full_rag_api",
    "full_rag_api_docs",
    "full_rag_api_path",
    "FSReader",
    "write_chunks_jsonl",
    "AppConfig",
]

__version__ = "0.1.0"
