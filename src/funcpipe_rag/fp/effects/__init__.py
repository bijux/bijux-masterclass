"""Module 06: effect-encoding utilities (end-of-Module-09).

This subpackage groups the "small monads" and effect helpers introduced in
Module 06:
- Reader: explicit, injectable configuration
- State: explicit threaded state
- Writer: pure log/metrics accumulation
- Layering helpers (no monad transformers)
- Runtime-configurable pipeline toggles

Note: Module 07 introduces `IOPlan` and IOPlan-specific wrappers, but in this codebase they
live under `funcpipe_rag.domain.effects` as domain-owned effect interfaces.
"""

from .configurable import toggle_logging, toggle_metrics, toggle_validation
from .layering import transpose_option_result, transpose_result_option
from .reader import Reader, ask, asks, local, pure as reader_pure
from .state import State, get, modify, put, pure as state_pure, run_state
from .writer import (
    Writer,
    censor,
    listen,
    pure as writer_pure,
    run_writer,
    tell,
    tell_many,
    wr_and_then,
    wr_map,
    wr_pure,
)
__all__ = [
    # Reader
    "Reader",
    "reader_pure",
    "ask",
    "asks",
    "local",
    # State
    "State",
    "state_pure",
    "get",
    "put",
    "modify",
    "run_state",
    # Writer
    "Writer",
    "writer_pure",
    "tell",
    "tell_many",
    "listen",
    "censor",
    "run_writer",
    "wr_pure",
    "wr_map",
    "wr_and_then",
    # Layering helpers
    "transpose_result_option",
    "transpose_option_result",
    # Configurable pipelines
    "toggle_validation",
    "toggle_logging",
    "toggle_metrics",
]
