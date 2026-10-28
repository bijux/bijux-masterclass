"""Workload schedules and coverage accounting."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ScheduledArrival:
    sequence: int
    scheduled_ns: int


def open_schedule(
    rate_per_second: float,
    duration_seconds: float,
    *,
    start_ns: int = 0,
) -> tuple[ScheduledArrival, ...]:
    if not math.isfinite(rate_per_second) or rate_per_second <= 0:
        raise ValueError("rate_per_second must be positive and finite")
    if not math.isfinite(duration_seconds) or duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive and finite")
    interval_ns = 1_000_000_000 / rate_per_second
    count = int(math.floor(rate_per_second * duration_seconds + 1e-12))
    return tuple(
        ScheduledArrival(
            sequence=index,
            scheduled_ns=start_ns + round(index * interval_ns),
        )
        for index in range(count)
    )


def estimated_closed_throughput(
    users: int,
    mean_response_seconds: float,
    think_time_seconds: float = 0.0,
) -> float:
    if users <= 0:
        raise ValueError("users must be positive")
    cycle = mean_response_seconds + think_time_seconds
    if not math.isfinite(cycle) or cycle <= 0:
        raise ValueError("cycle time must be positive and finite")
    return users / cycle


@dataclass(frozen=True, slots=True)
class ScheduleCoverage:
    offered: int
    started: int
    delayed: int
    maximum_start_delay_ns: int

    @property
    def fraction_started(self) -> float:
        return self.started / self.offered if self.offered else 1.0


def coverage(
    arrivals: Iterable[ScheduledArrival],
    actual_start_ns: dict[int, int],
    *,
    delay_threshold_ns: int,
) -> ScheduleCoverage:
    scheduled = tuple(arrivals)
    delays = [
        actual_start_ns[arrival.sequence] - arrival.scheduled_ns
        for arrival in scheduled
        if arrival.sequence in actual_start_ns
    ]
    if any(delay < 0 for delay in delays):
        raise ValueError("actual start cannot precede scheduled arrival")
    return ScheduleCoverage(
        offered=len(scheduled),
        started=len(delays),
        delayed=sum(delay > delay_threshold_ns for delay in delays),
        maximum_start_delay_ns=max(delays, default=0),
    )
