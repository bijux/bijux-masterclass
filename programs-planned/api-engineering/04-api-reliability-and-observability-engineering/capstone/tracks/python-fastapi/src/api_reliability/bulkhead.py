from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from threading import Lock


class BulkheadFull(RuntimeError):
    pass


class _Permit(AbstractContextManager[None]):
    def __init__(self, owner: "Bulkhead") -> None:
        self._owner = owner
        self._released = False

    def __enter__(self) -> None:
        return None

    def __exit__(self, *args: object) -> None:
        self.release()

    def release(self) -> None:
        if not self._released:
            self._released = True
            self._owner._release()


@dataclass(slots=True)
class Bulkhead:
    limit: int
    _in_use: int = field(init=False, default=0)
    _lock: Lock = field(init=False, default_factory=Lock)

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise ValueError("bulkhead limit must be positive")

    @property
    def in_use(self) -> int:
        with self._lock:
            return self._in_use

    def acquire(self) -> _Permit:
        with self._lock:
            if self._in_use >= self.limit:
                raise BulkheadFull("dependency concurrency limit reached")
            self._in_use += 1
        return _Permit(self)

    def _release(self) -> None:
        with self._lock:
            self._in_use -= 1
            if self._in_use < 0:
                raise RuntimeError("bulkhead permit underflow")
