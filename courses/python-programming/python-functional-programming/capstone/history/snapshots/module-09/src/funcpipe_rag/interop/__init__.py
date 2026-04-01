"""Module 09: interop helpers for FP across Python ecosystems (end-of-Module-09).

This package provides:
- stdlib-first functional helpers (itertools/functools/operator/pathlib)
- optional helper-library facades (toolz/returns) with safe fallbacks
- optional data processing adapters (pandas/polars/dask) behind import guards

All interop modules are designed to keep the core package importable without
non-stdlib dependencies; any third-party imports are performed dynamically.
"""

from .stdlib_fp import multicast_stream, merge_streams, running_sum
from .toolz_compat import TOOLZ_AVAILABLE, compose, curried_filter, curried_map, pipe, reduceby
from .returns_compat import RETURNS_AVAILABLE, to_option, to_result

__all__ = [
    # stdlib FP
    "merge_streams",
    "multicast_stream",
    "running_sum",
    # toolz-style (with fallback)
    "TOOLZ_AVAILABLE",
    "pipe",
    "compose",
    "curried_map",
    "curried_filter",
    "reduceby",
    # returns-style (with fallback)
    "RETURNS_AVAILABLE",
    "to_result",
    "to_option",
]
