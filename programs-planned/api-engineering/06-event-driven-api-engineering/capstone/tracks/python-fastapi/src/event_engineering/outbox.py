from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Callable

from .broker import DeterministicBroker
from .envelope import EventEnvelope


@dataclass(frozen=True, slots=True)
class OutboxRow:
    event_id: str
    channel: str
    key: str
    event: EventEnvelope
    state: str = "pending"
    attempts: int = 0
    published_at: datetime | None = None


class DomainOutboxStore:
    """Dependency-light atomic reference store; PostgreSQL is the durable route."""

    def __init__(self) -> None:
        self.domain: dict[str, dict[str, object]] = {}
        self.outbox: dict[str, OutboxRow] = {}

    def commit(
        self,
        *,
        aggregate_id: str,
        aggregate_state: dict[str, object],
        channel: str,
        key: str,
        event: EventEnvelope,
    ) -> None:
        if event.id in self.outbox:
            raise ValueError("duplicate outbox event id")
        # One critical section models one local database transaction.
        self.domain[aggregate_id] = dict(aggregate_state)
        self.outbox[event.id] = OutboxRow(event.id, channel, key, event)

    def pending(self) -> list[OutboxRow]:
        return sorted(
            (row for row in self.outbox.values() if row.state == "pending"),
            key=lambda row: row.event_id,
        )

    def mark_published(self, event_id: str, at: datetime) -> None:
        row = self.outbox[event_id]
        self.outbox[event_id] = replace(
            row,
            state="published",
            attempts=row.attempts + 1,
            published_at=at,
        )

    def mark_attempt(self, event_id: str) -> None:
        row = self.outbox[event_id]
        self.outbox[event_id] = replace(row, attempts=row.attempts + 1)


class OutboxRelay:
    def __init__(
        self,
        store: DomainOutboxStore,
        broker: DeterministicBroker,
        *,
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.store = store
        self.broker = broker
        self.clock = clock

    def step(self, *, crash_after_publish: bool = False) -> str:
        pending = self.store.pending()
        if not pending:
            return "idle"
        row = pending[0]
        self.store.mark_attempt(row.event_id)
        self.broker.publish(row.channel, row.key, row.event)
        if crash_after_publish:
            raise RuntimeError("injected crash after broker acceptance")
        self.store.mark_published(row.event_id, self.clock())
        return "published"
