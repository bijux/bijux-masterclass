from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .clock import Clock


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"


class CircuitOpen(RuntimeError):
    pass


@dataclass(slots=True)
class CircuitBreaker:
    failure_threshold: int
    open_duration_ms: int
    half_open_max_calls: int = 1
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    opened_at_ms: int | None = None
    half_open_in_flight: int = 0

    def __post_init__(self) -> None:
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold must be positive")
        if self.open_duration_ms < 1:
            raise ValueError("open_duration_ms must be positive")
        if self.half_open_max_calls < 1:
            raise ValueError("half_open_max_calls must be positive")

    def allow(self, clock: Clock) -> None:
        if self.state is CircuitState.OPEN:
            assert self.opened_at_ms is not None
            if clock.now_ms() - self.opened_at_ms < self.open_duration_ms:
                raise CircuitOpen("dependency circuit is open")
            self.state = CircuitState.HALF_OPEN
            self.half_open_in_flight = 0
        if self.state is CircuitState.HALF_OPEN:
            if self.half_open_in_flight >= self.half_open_max_calls:
                raise CircuitOpen("half-open probe already in flight")
            self.half_open_in_flight += 1

    def success(self) -> None:
        self.state = CircuitState.CLOSED
        self.consecutive_failures = 0
        self.opened_at_ms = None
        self.half_open_in_flight = 0

    def failure(self, clock: Clock) -> None:
        if self.state is CircuitState.HALF_OPEN:
            self._open(clock)
            return
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.failure_threshold:
            self._open(clock)

    def abandon_probe(self, clock: Clock) -> None:
        """Reopen after a canceled or abandoned half-open probe.

        Without this explicit path, cancellation can consume the only probe
        permit forever and make the circuit appear permanently unavailable.
        """

        if self.state is CircuitState.HALF_OPEN and self.half_open_in_flight:
            self._open(clock)

    def _open(self, clock: Clock) -> None:
        self.state = CircuitState.OPEN
        self.opened_at_ms = clock.now_ms()
        self.half_open_in_flight = 0
