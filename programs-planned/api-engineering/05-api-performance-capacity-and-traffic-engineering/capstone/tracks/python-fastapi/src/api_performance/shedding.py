"""Deterministic load-shedding policy for course scenarios."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceSignals:
    database_pool_fraction: float
    durable_job_fraction: float
    stream_permit_fraction: float
    storage_available: bool
    durable_database_available: bool

    def __post_init__(self) -> None:
        for value in (
            self.database_pool_fraction,
            self.durable_job_fraction,
            self.stream_permit_fraction,
        ):
            if not 0 <= value <= 1:
                raise ValueError("resource fractions must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class SheddingDecision:
    stage: int
    allowed_operations: frozenset[str]
    reason: str


_CONTROL = frozenset({"getRun", "cancelRun", "health", "reconcile"})
_READS = _CONTROL | frozenset({"getProject", "listRuns"})
_ARTIFACT = _READS | frozenset({"downloadArtifact"})
_ALL = _ARTIFACT | frozenset({"submitRun", "uploadDataset", "diagnostics"})


def choose_shedding(signals: ResourceSignals) -> SheddingDecision:
    if not signals.durable_database_available:
        return SheddingDecision(5, _CONTROL - {"reconcile"}, "database-unavailable")
    if not signals.storage_available:
        return SheddingDecision(4, _READS, "storage-unavailable")
    if signals.durable_job_fraction >= 0.95:
        return SheddingDecision(3, _ARTIFACT, "job-capacity")
    if signals.stream_permit_fraction >= 0.95:
        return SheddingDecision(
            2,
            _READS | frozenset({"submitRun"}),
            "stream-capacity",
        )
    if signals.database_pool_fraction >= 0.85:
        return SheddingDecision(1, _ALL - {"diagnostics"}, "database-pressure")
    return SheddingDecision(0, _ALL, "normal")
