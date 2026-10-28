from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass(slots=True)
class TokenBucket:
    capacity_units: int
    refill_units_per_second: int
    tokens_units: int | None = None
    last_ms: int = 0
    scale: int = 1_000_000
    _capacity: int = field(init=False, repr=False)
    _refill_per_second: int = field(init=False, repr=False)
    _tokens: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity_units <= 0 or self.refill_units_per_second < 0:
            raise ValueError("invalid bucket configuration")
        self._capacity = self.capacity_units * self.scale
        self._refill_per_second = self.refill_units_per_second * self.scale
        self._tokens = self._capacity if self.tokens_units is None else self.tokens_units * self.scale

    def allow(self, *, now_ms: int, cost_units: int = 1) -> bool:
        if now_ms < self.last_ms or cost_units <= 0:
            raise ValueError("invalid token-bucket input")
        elapsed = now_ms - self.last_ms
        refill = (elapsed * self._refill_per_second) // 1000
        self._tokens = min(self._capacity, self._tokens + refill)
        self.last_ms = now_ms
        cost = cost_units * self.scale
        if self._tokens < cost:
            return False
        self._tokens -= cost
        return True


class ConcurrencyLimiter:
    def __init__(self, limit: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        self.limit = limit
        self.in_use = 0
        self._lock = Lock()

    def try_acquire(self) -> "Permit | None":
        with self._lock:
            if self.in_use >= self.limit:
                return None
            self.in_use += 1
            return Permit(self)

    def _release(self) -> None:
        with self._lock:
            if self.in_use <= 0:
                raise RuntimeError("permit accounting underflow")
            self.in_use -= 1


class Permit:
    def __init__(self, limiter: ConcurrencyLimiter) -> None:
        self._limiter = limiter
        self._released = False

    def release(self) -> None:
        if not self._released:
            self._limiter._release()
            self._released = True

    def __enter__(self) -> "Permit":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()
