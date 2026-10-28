from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from enum import Enum
import random
from typing import Iterable

from .clock import Clock
from .deadline import Deadline


class RetrySafety(str, Enum):
    SAFE = "safe"
    IDEMPOTENT = "idempotent"
    IDEMPOTENCY_KEY = "idempotency-key"
    UNSAFE = "unsafe"


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    initial_delay_ms: int = 100
    maximum_delay_ms: int = 2_000
    multiplier: float = 2.0
    jitter: str = "full"

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least one")
        if self.initial_delay_ms < 0 or self.maximum_delay_ms < 0:
            raise ValueError("delays must be non-negative")
        if self.maximum_delay_ms < self.initial_delay_ms:
            raise ValueError("maximum_delay_ms must not be below initial_delay_ms")
        if self.multiplier < 1:
            raise ValueError("multiplier must be at least one")
        if self.jitter not in {"none", "full"}:
            raise ValueError("unsupported jitter strategy")


RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}


def retryable(
    *,
    status: int | None,
    transport_error: bool,
    safety: RetrySafety,
) -> bool:
    if safety is RetrySafety.UNSAFE:
        return False
    if transport_error:
        return True
    return status in RETRYABLE_STATUS


def parse_retry_after_ms(
    value: str | None,
    *,
    now: datetime | None = None,
) -> int | None:
    """Parse Retry-After seconds or an IMF-fixdate into a non-negative delay."""

    if value is None:
        return None
    raw = value.strip()
    if raw.isdigit():
        return int(raw) * 1_000
    try:
        when = parsedate_to_datetime(raw)
    except (TypeError, ValueError, OverflowError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    base = now or datetime.now(timezone.utc)
    return max(0, int((when - base).total_seconds() * 1_000))


def plan_retry_delays(
    policy: RetryPolicy,
    *,
    seed: int = 0,
    server_delay_ms: Iterable[int | None] | None = None,
) -> list[int]:
    """Return delays before attempts 2..N.

    Full jitter selects uniformly from ``[0, capped exponential delay]``. A
    valid Retry-After value acts as a floor. It never extends the operation
    deadline; ``fit_delays_to_deadline`` performs that separate decision.
    """

    rng = random.Random(seed)
    floors = list(server_delay_ms or [])
    delays: list[int] = []
    for retry_index in range(policy.max_attempts - 1):
        cap = min(
            policy.maximum_delay_ms,
            int(policy.initial_delay_ms * (policy.multiplier**retry_index)),
        )
        delay = cap if policy.jitter == "none" else rng.randint(0, cap)
        floor = floors[retry_index] if retry_index < len(floors) else None
        if floor is not None:
            if floor < 0:
                raise ValueError("server delay floor must be non-negative")
            delay = max(delay, floor)
        delays.append(delay)
    return delays


def fit_delays_to_deadline(
    delays: Iterable[int],
    *,
    clock: Clock,
    deadline: Deadline,
    minimum_attempt_ms: int,
) -> list[int]:
    """Select retry delays whose sleep *and* minimum attempt fit the budget.

    This function plans only future retry attempts. For each accepted delay it
    reserves ``delay + minimum_attempt_ms``. Actual execution must re-check the
    remaining deadline because the previous attempt may consume more time.
    """

    if minimum_attempt_ms <= 0:
        raise ValueError("minimum_attempt_ms must be positive")
    remaining = deadline.remaining_ms(clock)
    accepted: list[int] = []
    for delay in delays:
        if delay < 0:
            raise ValueError("retry delay must be non-negative")
        required = delay + minimum_attempt_ms
        if required > remaining:
            break
        accepted.append(delay)
        remaining -= required
    return accepted
