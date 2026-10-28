"""Focused runtime measurements with explicit scope and units."""

from __future__ import annotations

from dataclasses import dataclass
import time
import tracemalloc
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class RuntimeSample:
    wall_ns: int
    cpu_ns: int
    allocated_current_bytes: int | None = None
    allocated_peak_bytes: int | None = None


def measure_callable(
    operation: Callable[[], T],
    *,
    measure_python_allocations: bool = False,
) -> tuple[T, RuntimeSample]:
    if measure_python_allocations:
        tracemalloc.start()
    wall_start = time.perf_counter_ns()
    cpu_start = time.process_time_ns()
    try:
        value = operation()
    finally:
        cpu_end = time.process_time_ns()
        wall_end = time.perf_counter_ns()
    current: int | None = None
    peak: int | None = None
    if measure_python_allocations:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    return value, RuntimeSample(
        wall_ns=wall_end - wall_start,
        cpu_ns=cpu_end - cpu_start,
        allocated_current_bytes=current,
        allocated_peak_bytes=peak,
    )


def cpu_fraction(sample: RuntimeSample) -> float:
    if sample.wall_ns <= 0:
        raise ValueError("wall time must be positive")
    return sample.cpu_ns / sample.wall_ns
