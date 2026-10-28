"""Integer token-bucket traffic policy and atomic reservations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class BucketState:
    tokens: int
    last_ns: int
    remainder: int


@dataclass(frozen=True, slots=True)
class TokenDecision:
    allowed: bool
    remaining: int
    retry_after_ns: int | None
    reason: str


class TokenBucket:
    NANOSECONDS = 1_000_000_000

    def __init__(
        self,
        *,
        capacity: int,
        refill_per_second: int,
        initial_tokens: int | None = None,
        initial_ns: int = 0,
    ) -> None:
        if capacity <= 0 or refill_per_second <= 0:
            raise ValueError("bucket capacity and refill must be positive")
        tokens = capacity if initial_tokens is None else initial_tokens
        if not 0 <= tokens <= capacity:
            raise ValueError("initial tokens out of range")
        if initial_ns < 0:
            raise ValueError("initial time must be non-negative")
        self.capacity = capacity
        self.refill_per_second = refill_per_second
        self._tokens = tokens
        self._last_ns = initial_ns
        self._remainder = 0

    @property
    def state(self) -> BucketState:
        return BucketState(self._tokens, self._last_ns, self._remainder)

    def restore(self, state: BucketState) -> None:
        if not 0 <= state.tokens <= self.capacity:
            raise ValueError("invalid restored token state")
        if state.last_ns < 0 or not 0 <= state.remainder < self.NANOSECONDS:
            raise ValueError("invalid restored time state")
        self._tokens = state.tokens
        self._last_ns = state.last_ns
        self._remainder = state.remainder

    def _refill(self, now_ns: int) -> None:
        if now_ns < self._last_ns:
            raise ValueError("monotonic time moved backward")
        elapsed = now_ns - self._last_ns
        numerator = elapsed * self.refill_per_second + self._remainder
        added, remainder = divmod(numerator, self.NANOSECONDS)
        self._tokens = min(self.capacity, self._tokens + added)
        self._last_ns = now_ns
        self._remainder = 0 if self._tokens == self.capacity else remainder

    def consume(self, now_ns: int, cost: int) -> TokenDecision:
        if cost <= 0:
            raise ValueError("cost must be positive")
        self._refill(now_ns)
        if cost <= self._tokens:
            self._tokens -= cost
            return TokenDecision(
                allowed=True,
                remaining=self._tokens,
                retry_after_ns=None,
                reason="allowed",
            )
        missing = cost - self._tokens
        numerator_needed = missing * self.NANOSECONDS - self._remainder
        retry = max(
            0,
            (numerator_needed + self.refill_per_second - 1)
            // self.refill_per_second,
        )
        return TokenDecision(
            allowed=False,
            remaining=self._tokens,
            retry_after_ns=retry,
            reason="token-budget",
        )


@dataclass(frozen=True, slots=True)
class ReservationDecision:
    allowed: bool
    reason: str
    retry_after_ns: int | None


def reserve_atomically(
    requests: Iterable[tuple[TokenBucket, int]],
    *,
    now_ns: int,
) -> ReservationDecision:
    items = tuple(requests)
    states = tuple(bucket.state for bucket, _ in items)
    retry_values: list[int] = []
    for index, (bucket, cost) in enumerate(items):
        decision = bucket.consume(now_ns, cost)
        if not decision.allowed:
            for (restore_bucket, _), state in zip(items, states):
                restore_bucket.restore(state)
            if decision.retry_after_ns is not None:
                retry_values.append(decision.retry_after_ns)
            return ReservationDecision(
                allowed=False,
                reason=f"budget-{index}",
                retry_after_ns=max(retry_values, default=None),
            )
    return ReservationDecision(True, "allowed", None)


class LimiterRegistry:
    """Bound the number of identity-keyed buckets in one process."""

    def __init__(
        self,
        *,
        max_keys: int,
        idle_ttl_ns: int,
        capacity: int,
        refill_per_second: int,
    ) -> None:
        if max_keys <= 0 or idle_ttl_ns <= 0:
            raise ValueError("registry bounds must be positive")
        self.max_keys = max_keys
        self.idle_ttl_ns = idle_ttl_ns
        self.capacity = capacity
        self.refill_per_second = refill_per_second
        self._entries: dict[str, tuple[TokenBucket, int]] = {}

    def _evict_idle(self, now_ns: int) -> None:
        expired = [
            key
            for key, (_, last_used) in self._entries.items()
            if now_ns - last_used >= self.idle_ttl_ns
        ]
        for key in sorted(expired):
            self._entries.pop(key, None)

    def bucket(self, key: str, *, now_ns: int) -> TokenBucket:
        if not key:
            raise ValueError("limiter key is required")
        self._evict_idle(now_ns)
        existing = self._entries.get(key)
        if existing is not None:
            bucket, _ = existing
            self._entries[key] = (bucket, now_ns)
            return bucket
        if len(self._entries) >= self.max_keys:
            raise RuntimeError("limiter-key-capacity")
        bucket = TokenBucket(
            capacity=self.capacity,
            refill_per_second=self.refill_per_second,
            initial_ns=now_ns,
        )
        self._entries[key] = (bucket, now_ns)
        return bucket

    @property
    def size(self) -> int:
        return len(self._entries)
