from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class IncidentStatus(str, Enum):
    DETECTED = "detected"
    TRIAGED = "triaged"
    CONTAINED = "contained"
    RECOVERED = "recovered"
    CLOSED = "closed"


_ALLOWED = {
    IncidentStatus.DETECTED: {IncidentStatus.TRIAGED},
    IncidentStatus.TRIAGED: {IncidentStatus.CONTAINED},
    IncidentStatus.CONTAINED: {IncidentStatus.RECOVERED},
    IncidentStatus.RECOVERED: {IncidentStatus.CLOSED},
    IncidentStatus.CLOSED: set(),
}


@dataclass(frozen=True, slots=True)
class TimelineEntry:
    at: str
    source: str
    statement: str
    confidence: str


@dataclass(slots=True)
class Incident:
    incident_id: str
    status: IncidentStatus = IncidentStatus.DETECTED
    timeline: list[TimelineEntry] = field(default_factory=list)
    revoked_token_ids: set[str] = field(default_factory=set)
    active_webhook_key: str = "whk-2026-01"
    verification_keys: set[str] = field(default_factory=lambda: {"whk-2026-01"})

    def transition(self, target: IncidentStatus) -> None:
        if target not in _ALLOWED[self.status]:
            raise ValueError(f"illegal incident transition {self.status} -> {target}")
        self.status = target

    def record(self, entry: TimelineEntry) -> None:
        self.timeline.append(entry)

    def revoke_token(self, token_id: str) -> None:
        self.revoked_token_ids.add(token_id)

    def rotate_webhook_key(self, new_key_id: str, *, keep_old_for_verification: bool = True) -> None:
        old = self.active_webhook_key
        self.active_webhook_key = new_key_id
        self.verification_keys.add(new_key_id)
        if not keep_old_for_verification:
            self.verification_keys.discard(old)

    def retire_webhook_key(self, key_id: str) -> None:
        if key_id == self.active_webhook_key:
            raise ValueError("cannot retire the active signing key")
        self.verification_keys.discard(key_id)
