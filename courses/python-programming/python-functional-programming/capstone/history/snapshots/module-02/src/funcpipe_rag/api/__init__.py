"""Public APIs for the end-of-Module-02 codebase."""

from .types import DocRule, RagTaps, DebugConfig, Observations
from .clean_cfg import CleanConfig, make_cleaner, DEFAULT_CLEAN_CONFIG
from .config import RagConfig, RagCoreDeps, RagBoundaryDeps, Reader, get_deps, make_rag_fn, boundary_rag_config
from .core import (
    gen_chunk_doc,
    iter_rag,
    iter_rag_core,
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
    "CleanConfig",
    "DEFAULT_CLEAN_CONFIG",
    "make_cleaner",
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
]
