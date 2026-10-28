from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

GateStatus = Literal["pass", "fail", "review", "not-executed"]
Decision = Literal["accepted", "rejected", "review-required", "not-executed"]


@dataclass(frozen=True)
class ArtifactSet:
    image_digests: tuple[str, ...]
    chart_digest: str | None = None
    source_artifact_digest: str | None = None


@dataclass(frozen=True)
class DesiredRevision:
    release_id: str
    environment: str
    commit: str
    renderer: str
    renderer_version: str
    render_digest: str
    artifacts: ArtifactSet
    predecessor: str | None


@dataclass(frozen=True)
class EvidenceGate:
    name: str
    status: GateStatus
    subject: str
    reason: str
    blocker: bool = True
    expires_at: str | None = None


@dataclass
class ReleaseCandidate:
    revision: DesiredRevision
    gates: list[EvidenceGate] = field(default_factory=list)
    approvals: list[str] = field(default_factory=list)
    protected_deletions: list[str] = field(default_factory=list)
    rollback_frontier: str = "traffic-and-manifest"


@dataclass(frozen=True)
class Drift:
    identity: str
    category: str
    action: str
    details: str


@dataclass
class ReconcileReport:
    source_revision: str
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    blocked_prune: list[str] = field(default_factory=list)
    preserved_external: list[str] = field(default_factory=list)
    drift: list[Drift] = field(default_factory=list)
    writes: int = 0
    source_available: bool = True


@dataclass(frozen=True)
class MetricObservation:
    name: str
    candidate_samples: int
    stable_samples: int
    candidate_value: float | None
    stable_value: float | None
    absolute_limit: float
    relative_margin: float
    required: bool = True


@dataclass(frozen=True)
class SegmentObservation:
    name: str
    samples: int
    failures: int
    max_failure_rate: float
