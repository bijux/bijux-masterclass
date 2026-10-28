"""Queueing relationships used for model checks, not universal prediction."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class LittleLawResult:
    throughput_per_second: float
    mean_time_seconds: float
    mean_in_system: float
    unit: str


def little_law(
    *,
    throughput_per_second: float,
    mean_time_seconds: float,
    unit: str = "work-items",
) -> LittleLawResult:
    for name, value in (
        ("throughput_per_second", throughput_per_second),
        ("mean_time_seconds", mean_time_seconds),
    ):
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and non-negative")
    if not unit:
        raise ValueError("unit is required")
    return LittleLawResult(
        throughput_per_second=throughput_per_second,
        mean_time_seconds=mean_time_seconds,
        mean_in_system=throughput_per_second * mean_time_seconds,
        unit=unit,
    )


def mean_time_from_little_law(
    *,
    mean_in_system: float,
    throughput_per_second: float,
) -> float:
    if not math.isfinite(mean_in_system) or mean_in_system < 0:
        raise ValueError("mean_in_system must be finite and non-negative")
    if not math.isfinite(throughput_per_second) or throughput_per_second <= 0:
        raise ValueError("throughput must be positive and finite")
    return mean_in_system / throughput_per_second


@dataclass(frozen=True, slots=True)
class MM1Approximation:
    arrival_rate: float
    service_rate: float
    utilization: float
    mean_time_seconds: float
    mean_in_system: float


def mm1_approximation(
    *,
    arrival_rate: float,
    service_rate: float,
) -> MM1Approximation:
    if (
        not math.isfinite(arrival_rate)
        or not math.isfinite(service_rate)
        or arrival_rate < 0
        or service_rate <= 0
    ):
        raise ValueError("rates must be finite and valid")
    if arrival_rate >= service_rate:
        raise ValueError("M/M/1 steady state requires arrival < service")
    utilization = arrival_rate / service_rate
    mean_time = 1.0 / (service_rate - arrival_rate)
    return MM1Approximation(
        arrival_rate=arrival_rate,
        service_rate=service_rate,
        utilization=utilization,
        mean_time_seconds=mean_time,
        mean_in_system=arrival_rate * mean_time,
    )
