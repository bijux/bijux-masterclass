from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from threading import Lock

class Phase(str, Enum):
    STARTING = "starting"
    ACCEPTING = "accepting"
    DRAINING = "draining"
    STOPPING = "stopping"
    STOPPED = "stopped"

@dataclass
class Lifecycle:
    phase: Phase = Phase.STARTING
    active_calls: int = 0

    def __post_init__(self) -> None:
        self._lock = Lock()

    def start(self) -> None:
        with self._lock:
            if self.phase != Phase.STARTING:
                raise RuntimeError("invalid lifecycle transition")
            self.phase = Phase.ACCEPTING

    def admit(self) -> None:
        with self._lock:
            if self.phase != Phase.ACCEPTING:
                raise RuntimeError("server is not accepting")
            self.active_calls += 1

    def release(self) -> None:
        with self._lock:
            if self.active_calls <= 0:
                raise RuntimeError("active call underflow")
            self.active_calls -= 1
            if self.phase == Phase.STOPPING and self.active_calls == 0:
                self.phase = Phase.STOPPED

    def drain(self) -> None:
        with self._lock:
            if self.phase not in {Phase.ACCEPTING, Phase.DRAINING}:
                raise RuntimeError("invalid drain transition")
            self.phase = Phase.DRAINING

    def stop(self) -> None:
        with self._lock:
            self.phase = Phase.STOPPING
            if self.active_calls == 0:
                self.phase = Phase.STOPPED

    def serving(self) -> bool:
        return self.phase == Phase.ACCEPTING
