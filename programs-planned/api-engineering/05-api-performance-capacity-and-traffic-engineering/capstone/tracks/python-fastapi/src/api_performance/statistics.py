"""Deterministic statistical summaries for course benchmark evidence."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from statistics import fmean
from typing import Iterable, Sequence


class StatisticsError(ValueError):
    pass


def _validated(samples: Iterable[float]) -> list[float]:
    values = [float(value) for value in samples]
    if not values:
        raise StatisticsError("at least one sample is required")
    if any(not math.isfinite(value) for value in values):
        raise StatisticsError("samples must be finite")
    return values


def nearest_rank(samples: Iterable[float], quantile: float) -> float:
    values = sorted(_validated(samples))
    if not math.isfinite(quantile) or not 0 < quantile <= 1:
        raise StatisticsError("quantile must be in (0, 1]")
    rank = math.ceil(quantile * len(values))
    return values[rank - 1]


@dataclass(frozen=True, slots=True)
class SampleSummary:
    count: int
    minimum: float
    maximum: float
    mean: float
    p50: float
    p90: float
    p95: float
    p99: float
    quantile_algorithm: str = "nearest-rank"


def summarize(samples: Iterable[float]) -> SampleSummary:
    values = _validated(samples)
    return SampleSummary(
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        mean=fmean(values),
        p50=nearest_rank(values, 0.50),
        p90=nearest_rank(values, 0.90),
        p95=nearest_rank(values, 0.95),
        p99=nearest_rank(values, 0.99),
    )


@dataclass(frozen=True, slots=True)
class Interval:
    lower: float
    estimate: float
    upper: float
    confidence: float


def bootstrap_mean_difference(
    baseline_run_values: Sequence[float],
    candidate_run_values: Sequence[float],
    *,
    resamples: int = 10_000,
    confidence: float = 0.95,
    seed: int = 0,
) -> Interval:
    baseline = _validated(baseline_run_values)
    candidate = _validated(candidate_run_values)
    if resamples <= 0:
        raise StatisticsError("resamples must be positive")
    if not 0 < confidence < 1:
        raise StatisticsError("confidence must be in (0, 1)")
    rng = random.Random(seed)
    differences: list[float] = []
    for _ in range(resamples):
        b = [rng.choice(baseline) for _ in baseline]
        c = [rng.choice(candidate) for _ in candidate]
        differences.append(fmean(c) - fmean(b))
    differences.sort()
    alpha = (1.0 - confidence) / 2.0
    return Interval(
        lower=nearest_rank(differences, alpha),
        estimate=fmean(candidate) - fmean(baseline),
        upper=nearest_rank(differences, 1.0 - alpha),
        confidence=confidence,
    )
