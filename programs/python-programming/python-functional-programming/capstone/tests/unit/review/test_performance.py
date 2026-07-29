from __future__ import annotations

import pytest
from funcpipe_rag.review.performance import (
    PerformanceBudget,
    PerformanceObservation,
    evaluate_budget,
)


def test_evaluate_budget_reports_every_failed_dimension() -> None:
    budget = PerformanceBudget(
        max_latency_ms=100,
        max_peak_memory_mb=64,
        min_throughput_per_second=20,
    )
    observation = PerformanceObservation(
        latency_ms=120,
        peak_memory_mb=80,
        throughput_per_second=10,
    )

    decision = evaluate_budget(budget, observation)

    assert decision.within_budget is False
    assert decision.violations == ("latency", "peak_memory", "throughput")


def test_evaluate_budget_accepts_values_on_the_declared_boundary() -> None:
    budget = PerformanceBudget(100, 64, 20)

    decision = evaluate_budget(budget, PerformanceObservation(100, 64, 20))

    assert decision.within_budget is True
    assert decision.violations == ()


def test_performance_values_reject_invalid_measurements() -> None:
    with pytest.raises(ValueError, match="positive"):
        PerformanceBudget(0, 64, 20)
    with pytest.raises(ValueError, match="negative"):
        PerformanceObservation(-1, 32, 20)
