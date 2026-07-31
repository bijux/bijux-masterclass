"""Pure performance-budget decisions over measurements collected at a shell."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PerformanceBudget:
    max_latency_ms: float
    max_peak_memory_mb: float
    min_throughput_per_second: float

    def __post_init__(self) -> None:
        if min(
            self.max_latency_ms,
            self.max_peak_memory_mb,
            self.min_throughput_per_second,
        ) <= 0:
            raise ValueError("performance budget values must be positive")


@dataclass(frozen=True, slots=True)
class PerformanceObservation:
    latency_ms: float
    peak_memory_mb: float
    throughput_per_second: float

    def __post_init__(self) -> None:
        if min(self.latency_ms, self.peak_memory_mb, self.throughput_per_second) < 0:
            raise ValueError("performance observations cannot be negative")


@dataclass(frozen=True, slots=True)
class BudgetDecision:
    within_budget: bool
    violations: tuple[str, ...]


def evaluate_budget(
    budget: PerformanceBudget,
    observation: PerformanceObservation,
) -> BudgetDecision:
    """Evaluate fixed measurements without performing timing or allocation I/O."""

    violations: list[str] = []
    if observation.latency_ms > budget.max_latency_ms:
        violations.append("latency")
    if observation.peak_memory_mb > budget.max_peak_memory_mb:
        violations.append("peak_memory")
    if observation.throughput_per_second < budget.min_throughput_per_second:
        violations.append("throughput")
    return BudgetDecision(within_budget=not violations, violations=tuple(violations))
