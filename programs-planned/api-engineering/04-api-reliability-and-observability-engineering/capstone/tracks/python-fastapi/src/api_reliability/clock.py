from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Protocol


class Clock(Protocol):
    def now_ms(self) -> int: ...


class SystemClock:
    def now_ms(self) -> int:
        return time.time_ns() // 1_000_000


@dataclass(slots=True)
class ManualClock:
    current_ms: int = 0

    def now_ms(self) -> int:
        return self.current_ms

    def advance(self, milliseconds: int) -> None:
        if milliseconds < 0:
            raise ValueError("clock cannot move backwards")
        self.current_ms += milliseconds

    def set(self, milliseconds: int) -> None:
        if milliseconds < self.current_ms:
            raise ValueError("clock cannot move backwards")
        self.current_ms = milliseconds
