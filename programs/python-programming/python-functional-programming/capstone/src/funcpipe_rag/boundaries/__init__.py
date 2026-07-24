"""Impure edges and boundary adapters (end-of-Module-09).

This package groups the parts of the project that perform I/O or interact with
the outside world (CLI, filesystem, JSON/MessagePack, Pydantic schemas).

Reusable edge adapters live in `funcpipe_rag.boundaries.adapters`.
"""

from .adapters.exception_bridge import (
    UnexpectedFailure,
    result_map_try,
    try_result,
    unexpected_fail,
    v_map_try,
    v_try,
)
from .app_config import AppConfig

__all__ = [
    "AppConfig",
    "UnexpectedFailure",
    "result_map_try",
    "try_result",
    "unexpected_fail",
    "v_map_try",
    "v_try",
]
