"""Small cProfile wrapper that keeps report I/O outside the profiled call."""

from __future__ import annotations

import cProfile
from dataclasses import dataclass
import io
import pstats
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ProfileResult:
    value: object
    report: str
    sort_key: str
    limit: int


def profile_callable(
    operation: Callable[[], T],
    *,
    sort_key: str = "cumulative",
    limit: int = 25,
) -> ProfileResult:
    if limit <= 0:
        raise ValueError("limit must be positive")
    profiler = cProfile.Profile()
    value = profiler.runcall(operation)
    output = io.StringIO()
    stats = pstats.Stats(profiler, stream=output)
    stats.strip_dirs().sort_stats(sort_key).print_stats(limit)
    return ProfileResult(
        value=value,
        report=output.getvalue(),
        sort_key=sort_key,
        limit=limit,
    )


def compare_snapshot_statistics(
    before: object,
    after: object,
    *,
    key_type: str = "lineno",
    limit: int = 20,
) -> tuple[object, ...]:
    # Typed as object to keep tracemalloc's private implementation details out
    # of the public course API while retaining its documented compare_to call.
    comparison = after.compare_to(before, key_type)
    return tuple(comparison[:limit])
