from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Callable
from uuid import uuid4

from .broker import DeterministicBroker
from .envelope import EventEnvelope


@dataclass(frozen=True, slots=True)
class DeadLetter:
    id: str
    tenant_id: str
    consumer: str
    original_event: EventEnvelope
    channel: str
    partition: int
    offset: int
    attempts: int
    failure_code: str
    safe_detail: str


class DeadLetterStore:
    def __init__(self) -> None:
        self.rows: list[DeadLetter] = []

    def append(self, row: DeadLetter) -> None:
        self.rows.append(row)


class PermanentMessageError(ValueError):
    pass


class ConsumerRunner:
    def __init__(
        self,
        broker: DeterministicBroker,
        dead_letters: DeadLetterStore,
        *,
        max_attempts: int = 3,
        retry_delay: Callable[[int], timedelta] | None = None,
    ) -> None:
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        self.broker = broker
        self.dead_letters = dead_letters
        self.max_attempts = max_attempts
        self.retry_delay = retry_delay or (
            lambda attempt: timedelta(seconds=attempt)
        )

    def step(
        self,
        group: str,
        channel: str,
        handler: Callable[[EventEnvelope], None],
    ) -> str:
        deliveries = self.broker.poll(
            group, channel, max_messages=1, ack_wait=timedelta(seconds=10)
        )
        if not deliveries:
            return "idle"
        delivery = deliveries[0]
        try:
            handler(delivery.record.event)
        except Exception as exc:
            permanent = isinstance(exc, PermanentMessageError)
            if permanent or delivery.attempt >= self.max_attempts:
                self.dead_letters.append(
                    DeadLetter(
                        id=str(uuid4()),
                        tenant_id=delivery.record.event.tenantid,
                        consumer=group,
                        original_event=delivery.record.event,
                        channel=channel,
                        partition=delivery.record.partition,
                        offset=delivery.record.offset,
                        attempts=delivery.attempt,
                        failure_code=type(exc).__name__,
                        safe_detail=str(exc)[:256],
                    )
                )
                self.broker.term(delivery.token)
                return "dead-lettered"
            self.broker.nack(
                delivery.token, self.retry_delay(delivery.attempt)
            )
            return "retry"
        self.broker.ack(delivery.token)
        return "acked"


@dataclass(frozen=True, slots=True)
class LagHealth:
    state: str
    lag: int
    oldest_age_seconds: int


def classify_lag(
    lag: int,
    oldest_age_seconds: int,
    *,
    warning_lag: int,
    critical_lag: int,
    warning_age: int,
    critical_age: int,
) -> LagHealth:
    values = [
        lag,
        oldest_age_seconds,
        warning_lag,
        critical_lag,
        warning_age,
        critical_age,
    ]
    if min(values) < 0:
        raise ValueError("lag values cannot be negative")
    if critical_lag < warning_lag or critical_age < warning_age:
        raise ValueError("critical thresholds must be >= warning thresholds")
    if lag >= critical_lag or oldest_age_seconds >= critical_age:
        state = "critical"
    elif lag >= warning_lag or oldest_age_seconds >= warning_age:
        state = "warning"
    else:
        state = "healthy"
    return LagHealth(state, lag, oldest_age_seconds)
