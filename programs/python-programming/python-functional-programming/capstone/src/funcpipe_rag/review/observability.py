"""Immutable observations and pure aggregation for pipeline review."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StageObservation:
    stage: str
    processed: int
    failures: int
    latency_ms: float

    def __post_init__(self) -> None:
        if not self.stage:
            raise ValueError("stage must not be empty")
        if min(self.processed, self.failures) < 0 or self.latency_ms < 0:
            raise ValueError("observation values cannot be negative")
        if self.failures > self.processed:
            raise ValueError("failures cannot exceed processed items")


@dataclass(frozen=True, slots=True)
class ObservationSummary:
    processed: int
    failures: int
    latency_ms: float
    stages: tuple[str, ...]


def summarize_observations(
    observations: tuple[StageObservation, ...],
) -> ObservationSummary:
    """Fold stage observations without logging, timing, or changing control flow."""

    return ObservationSummary(
        processed=sum(item.processed for item in observations),
        failures=sum(item.failures for item in observations),
        latency_ms=sum(item.latency_ms for item in observations),
        stages=tuple(item.stage for item in observations),
    )
