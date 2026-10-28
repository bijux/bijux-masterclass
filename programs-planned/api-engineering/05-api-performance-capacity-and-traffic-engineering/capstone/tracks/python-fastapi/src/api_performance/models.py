"""Validated data contracts for performance experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Mapping

from .identity import sha256_identity


class ModelError(ValueError):
    """Raised when a performance record is incomplete or contradictory."""


@dataclass(frozen=True, slots=True)
class WorkloadSpec:
    id: str
    model: str
    rate_per_second: float
    duration_seconds: int
    dataset_id: str
    request_mix: Mapping[str, float]
    max_outstanding_per_client: int = 1
    think_time_seconds: float = 0.0
    annotations: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.startswith("WL-"):
            raise ModelError("workload id must start with WL-")
        if self.model not in {"open", "closed", "mixed"}:
            raise ModelError("unsupported workload model")
        if not math.isfinite(self.rate_per_second) or self.rate_per_second <= 0:
            raise ModelError("rate_per_second must be positive and finite")
        if self.duration_seconds <= 0:
            raise ModelError("duration_seconds must be positive")
        if not self.dataset_id:
            raise ModelError("dataset_id is required")
        if self.max_outstanding_per_client <= 0:
            raise ModelError("max_outstanding_per_client must be positive")
        if not math.isfinite(self.think_time_seconds) or self.think_time_seconds < 0:
            raise ModelError("think_time_seconds must be finite and non-negative")
        if not self.request_mix:
            raise ModelError("request_mix is required")
        total = 0.0
        for operation, weight in self.request_mix.items():
            if not operation or not math.isfinite(weight) or weight <= 0:
                raise ModelError("request mix entries must be positive")
            total += weight
        if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise ModelError("request mix weights must sum to 1")

    @property
    def semantic_value(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "model": self.model,
            "ratePerSecond": self.rate_per_second,
            "durationSeconds": self.duration_seconds,
            "datasetId": self.dataset_id,
            "requestMix": dict(self.request_mix),
            "maxOutstandingPerClient": self.max_outstanding_per_client,
            "thinkTimeSeconds": self.think_time_seconds,
        }

    @property
    def identity(self) -> str:
        return sha256_identity(self.semantic_value)


@dataclass(frozen=True, slots=True)
class EnvironmentFingerprint:
    runtime: str
    runtime_version: str
    cpu_logical: int
    memory_limit_bytes: int
    process_count: int
    worker_count: int
    source_revision: str
    dataset_id: str
    database_profile: str
    feature_flags: Mapping[str, bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.runtime or not self.runtime_version:
            raise ModelError("runtime identity is required")
        for name, value in (
            ("cpu_logical", self.cpu_logical),
            ("memory_limit_bytes", self.memory_limit_bytes),
            ("process_count", self.process_count),
            ("worker_count", self.worker_count),
        ):
            if value <= 0:
                raise ModelError(f"{name} must be positive")
        if not self.source_revision or not self.dataset_id:
            raise ModelError("source revision and dataset are required")

    @property
    def semantic_value(self) -> dict[str, Any]:
        return {
            "runtime": self.runtime,
            "runtimeVersion": self.runtime_version,
            "cpuLogical": self.cpu_logical,
            "memoryLimitBytes": str(self.memory_limit_bytes),
            "processCount": self.process_count,
            "workerCount": self.worker_count,
            "sourceRevision": self.source_revision,
            "datasetId": self.dataset_id,
            "databaseProfile": self.database_profile,
            "featureFlags": dict(self.feature_flags),
        }

    @property
    def identity(self) -> str:
        return sha256_identity(self.semantic_value)


@dataclass(frozen=True, slots=True)
class CorrectnessReport:
    passed: bool
    checks: Mapping[str, bool]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.passed != all(self.checks.values()):
            raise ModelError("passed must equal conjunction of checks")


@dataclass(frozen=True, slots=True)
class OutcomeCounts:
    offered: int
    started: int
    admitted: int
    completed: int
    rejected: int
    failed: int
    missing: int

    def __post_init__(self) -> None:
        if any(value < 0 for value in self.as_dict().values()):
            raise ModelError("outcome counts must be non-negative")
        if self.started > self.offered:
            raise ModelError("started cannot exceed offered")
        if self.completed + self.missing > self.started:
            raise ModelError("completed plus missing cannot exceed started")
        if self.admitted > self.started:
            raise ModelError("admitted cannot exceed started")
        if self.rejected + self.failed > self.completed:
            raise ModelError("terminal categories exceed completed")

    def as_dict(self) -> dict[str, int]:
        return {
            "offered": self.offered,
            "started": self.started,
            "admitted": self.admitted,
            "completed": self.completed,
            "rejected": self.rejected,
            "failed": self.failed,
            "missing": self.missing,
        }

    @property
    def schedule_coverage(self) -> float:
        return self.started / self.offered if self.offered else 1.0


@dataclass(frozen=True, slots=True)
class BenchmarkEnvelope:
    profile_version: str
    workload_id: str
    workload_hash: str
    environment_hash: str
    evidence_class: str
    correctness: CorrectnessReport
    outcomes: OutcomeCounts
    summary: Mapping[str, Any]
    source_revision: str
    annotations: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.profile_version != "1.0":
            raise ModelError("unsupported performance profile")
        if not self.workload_hash.startswith("sha256:"):
            raise ModelError("workload hash is required")
        if not self.environment_hash.startswith("sha256:"):
            raise ModelError("environment hash is required")
        if self.evidence_class not in {"A", "B", "C", "D", "E"}:
            raise ModelError("unknown evidence class")
        if self.outcomes.offered == 0:
            raise ModelError("benchmark must offer work")

    @property
    def publishable(self) -> bool:
        return (
            self.correctness.passed
            and self.outcomes.missing == 0
            and self.outcomes.started == self.outcomes.offered
        )
