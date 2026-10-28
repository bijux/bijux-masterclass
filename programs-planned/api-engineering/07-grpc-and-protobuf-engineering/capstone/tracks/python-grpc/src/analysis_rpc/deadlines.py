from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Deadline:
    expires_at: float
    clock: Callable[[], float]

    @classmethod
    def after(cls, seconds: float, clock: Callable[[], float]) -> "Deadline":
        if seconds <= 0:
            raise ValueError("deadline duration must be positive")
        return cls(clock() + seconds, clock)

    def remaining(self) -> float:
        return max(0.0, self.expires_at - self.clock())

    def child_timeout(self, *, reserve: float = 0.0, cap: float | None = None) -> float:
        remaining = max(0.0, self.remaining() - reserve)
        return remaining if cap is None else min(remaining, cap)

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int
    initial_backoff: float
    multiplier: float
    max_backoff: float
    retryable_statuses: frozenset[str]

    def delay(self, retry_index: int, jitter: float) -> float:
        raw = min(self.max_backoff, self.initial_backoff * (self.multiplier ** retry_index))
        return raw * max(0.0, min(1.0, jitter))

    def allows(self, *, method: str, status: str, attempt: int, idempotent: bool,
               remaining: float, next_delay: float) -> bool:
        return (
            attempt < self.max_attempts
            and status in self.retryable_statuses
            and (method.startswith("Get") or idempotent)
            and next_delay < remaining
        )
