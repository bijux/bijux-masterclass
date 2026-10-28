from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, FrozenSet


class DomainError(RuntimeError):
    """Base class for stable application failures."""


class ValidationError(DomainError):
    pass


class Conflict(DomainError):
    pass


class Unauthorized(DomainError):
    pass


class Unavailable(DomainError):
    pass


class DeadlineExceeded(DomainError):
    pass


class RunState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class RequestContext:
    subject: str
    tenant: str
    workload: str
    scopes: FrozenSet[str]
    deadline_ms: int
    now_ms: int = 0
    trace_id: str = "trace-local"

    @property
    def remaining_ms(self) -> int:
        return max(0, self.deadline_ms - self.now_ms)

    def require(self, scope: str) -> None:
        if scope not in self.scopes:
            raise Unauthorized(f"missing scope: {scope}")

    def child(self, *, elapsed_ms: int, reserve_ms: int = 0) -> "RequestContext":
        now = self.now_ms + max(0, elapsed_ms)
        if self.deadline_ms - now <= reserve_ms:
            raise DeadlineExceeded("no remaining deadline budget")
        return RequestContext(
            subject=self.subject,
            tenant=self.tenant,
            workload=self.workload,
            scopes=self.scopes,
            deadline_ms=self.deadline_ms - reserve_ms,
            now_ms=now,
            trace_id=self.trace_id,
        )


@dataclass
class RunRecord:
    run_id: str
    tenant: str
    owner: str
    dataset_id: str
    attempt_id: str
    state: RunState = RunState.QUEUED
    version: int = 1
    artifact_ids: list[str] = field(default_factory=list)


@dataclass
class ArtifactRecord:
    artifact_id: str
    tenant: str
    run_id: str
    attempt_id: str
    sha256: str
    content: bytes
    version: int = 1
    state: str = "published"


@dataclass
class DeliveryRecord:
    delivery_id: str
    subscription_id: str
    event_id: str
    state: str = "pending"
    attempts: int = 0


@dataclass(frozen=True)
class OperationResult:
    value: Any
    authoritative: bool = True
    partial: bool = False
    warnings: tuple[str, ...] = ()
