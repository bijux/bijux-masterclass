from __future__ import annotations

from dataclasses import dataclass

from .clock import Clock


class DeadlineExceeded(TimeoutError):
    pass


@dataclass(frozen=True, slots=True)
class Deadline:
    expires_at_ms: int

    @classmethod
    def after(cls, clock: Clock, timeout_ms: int) -> "Deadline":
        if timeout_ms <= 0:
            raise ValueError("timeout must be positive")
        return cls(clock.now_ms() + timeout_ms)

    def remaining_ms(self, clock: Clock) -> int:
        return max(0, self.expires_at_ms - clock.now_ms())

    def expired(self, clock: Clock) -> bool:
        return self.remaining_ms(clock) == 0

    def require_remaining(self, clock: Clock, minimum_ms: int = 1) -> int:
        remaining = self.remaining_ms(clock)
        if remaining < minimum_ms:
            raise DeadlineExceeded("operation deadline exhausted")
        return remaining

    def child(self, clock: Clock, maximum_ms: int) -> "Deadline":
        if maximum_ms <= 0:
            raise ValueError("child maximum must be positive")
        return Deadline(min(self.expires_at_ms, clock.now_ms() + maximum_ms))
