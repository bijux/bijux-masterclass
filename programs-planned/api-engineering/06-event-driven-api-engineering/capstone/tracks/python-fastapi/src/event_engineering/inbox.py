from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Callable, TypeVar

from .envelope import EventEnvelope

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ProcessResult:
    status: str
    revision: int


class TransactionalProjection:
    """Atomic inbox/effect semantic model."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._seen: dict[tuple[str, str, str, str], int] = {}
        self._state: dict[tuple[str, str], dict[str, object]] = {}
        self._revision = 0

    def apply(
        self,
        *,
        tenant_id: str,
        consumer: str,
        effect_version: str,
        event: EventEnvelope,
        mutation: Callable[[dict[str, object], EventEnvelope], None],
    ) -> ProcessResult:
        identity = (tenant_id, consumer, effect_version, event.id)
        target = (tenant_id, f"{consumer}:{effect_version}")
        with self._lock:
            existing = self._seen.get(identity)
            if existing is not None:
                return ProcessResult("duplicate", existing)
            state = dict(self._state.get(target, {}))
            mutation(state, event)
            self._revision += 1
            revision = self._revision
            self._state[target] = state
            self._seen[identity] = revision
            return ProcessResult("applied", revision)

    def snapshot(self, tenant_id: str, consumer: str, effect_version: str) -> dict[str, object]:
        return dict(self._state.get((tenant_id, f"{consumer}:{effect_version}"), {}))

    @property
    def applied_count(self) -> int:
        return len(self._seen)
