"""Bounded async single-flight for cache fills."""

from __future__ import annotations

import asyncio
from collections import Counter
from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class SingleFlightRejected(RuntimeError):
    pass


class SingleFlight(Generic[T]):
    def __init__(
        self,
        *,
        max_concurrent_fills: int,
        max_waiters_per_key: int,
    ) -> None:
        if min(max_concurrent_fills, max_waiters_per_key) <= 0:
            raise ValueError("single-flight bounds must be positive")
        self._max_fills = max_concurrent_fills
        self._max_waiters_per_key = max_waiters_per_key
        self._lock = asyncio.Lock()
        self._tasks: dict[str, asyncio.Task[T]] = {}
        self._waiters: Counter[str] = Counter()

    async def _execute(
        self,
        key: str,
        factory: Callable[[], Awaitable[T]],
    ) -> T:
        try:
            return await factory()
        finally:
            async with self._lock:
                current = self._tasks.get(key)
                if current is asyncio.current_task():
                    self._tasks.pop(key, None)

    async def do(
        self,
        key: str,
        factory: Callable[[], Awaitable[T]],
        *,
        timeout_seconds: float | None = None,
    ) -> T:
        if not key:
            raise ValueError("single-flight key is required")
        async with self._lock:
            task = self._tasks.get(key)
            if task is None:
                if len(self._tasks) >= self._max_fills:
                    raise SingleFlightRejected("fill-capacity")
                task = asyncio.create_task(self._execute(key, factory))
                self._tasks[key] = task
            if self._waiters[key] >= self._max_waiters_per_key:
                raise SingleFlightRejected("waiter-capacity")
            self._waiters[key] += 1
        try:
            awaitable = asyncio.shield(task)
            if timeout_seconds is None:
                return await awaitable
            if timeout_seconds <= 0:
                raise SingleFlightRejected("waiter-timeout")
            try:
                return await asyncio.wait_for(awaitable, timeout_seconds)
            except TimeoutError as exc:
                raise SingleFlightRejected("waiter-timeout") from exc
        finally:
            async with self._lock:
                self._waiters[key] -= 1
                if self._waiters[key] == 0:
                    del self._waiters[key]

    async def snapshot(self) -> dict[str, object]:
        async with self._lock:
            return {
                "fills": len(self._tasks),
                "waiters": dict(self._waiters),
                "maxFills": self._max_fills,
                "maxWaitersPerKey": self._max_waiters_per_key,
            }
