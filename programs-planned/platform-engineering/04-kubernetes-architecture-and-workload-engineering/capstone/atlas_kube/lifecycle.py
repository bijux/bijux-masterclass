from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProbeKind(str, Enum):
    STARTUP = "startup"
    LIVENESS = "liveness"
    READINESS = "readiness"


@dataclass(slots=True)
class ProbeState:
    failure_threshold: int
    success_threshold: int = 1
    failures: int = 0
    successes: int = 0

    def observe(self, success: bool) -> str:
        if success:
            self.successes += 1
            self.failures = 0
            if self.successes >= self.success_threshold:
                return "succeeded"
            return "pending"
        self.failures += 1
        self.successes = 0
        return "failed" if self.failures >= self.failure_threshold else "pending"


@dataclass(frozen=True, slots=True)
class ShutdownPlan:
    grace_seconds: int
    pre_stop_seconds: int
    drain_seconds: int

    @property
    def feasible(self) -> bool:
        return self.pre_stop_seconds + self.drain_seconds <= self.grace_seconds

    @property
    def remaining_seconds(self) -> int:
        return self.grace_seconds - self.pre_stop_seconds - self.drain_seconds


def restart_backoff_seconds(restarts: int, initial: int = 10, maximum: int = 300) -> int:
    if restarts < 0:
        raise ValueError("restarts must be non-negative")
    return min(maximum, initial * (2 ** restarts))
