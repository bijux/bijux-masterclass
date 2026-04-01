"""Boundary shells (CLI / filesystem) for the end-of-Module-06 codebase."""

from .rag_api_shell import FSReader, run, write_chunks_jsonl
from .rag_main import boundary_app_config, orchestrate, read_docs, write_chunks

__all__ = [
    "FSReader",
    "write_chunks_jsonl",
    "run",
    "boundary_app_config",
    "read_docs",
    "write_chunks",
    "orchestrate",
]
