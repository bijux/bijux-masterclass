"""Bounded, cancellation-safe asynchronous admission control."""

from __future__ import annotations

import asyncio
from collections import Counter
from dataclasses import dataclass
from typing import Final


class AdmissionRejected(RuntimeError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True, slots=True)
class AdmissionSnapshot:
    active: int
    waiting: int
    active_by_key: dict[str, int]
    max_active: int
    max_waiters: int


class AdmissionPermit:
    def __init__(self, controller: "FairAdmission", key: str) -> None:
        self._controller = controller
        self.key = key
        self._released = False

    async def release(self) -> None:
        if self._released:
            raise RuntimeError("permit released twice")
        self._released = True
        await self._controller._release(self.key)

    async def __aenter__(self) -> "AdmissionPermit":
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        await self.release()


class FairAdmission:
    """A global cap plus per-key cap with bounded waiters.

    FIFO order is preserved among currently eligible waiters. A waiter whose key
    is at its per-key cap does not block a later waiter from another key.
    """

    def __init__(
        self,
        *,
        max_active: int,
        max_waiters: int,
        max_active_per_key: int,
    ) -> None:
        if min(max_active, max_active_per_key) <= 0 or max_waiters < 0:
            raise ValueError("invalid admission limits")
        if max_active_per_key > max_active:
            raise ValueError("per-key active limit cannot exceed global limit")
        self._max_active: Final = max_active
        self._max_waiters: Final = max_waiters
        self._max_active_per_key: Final = max_active_per_key
        self._condition = asyncio.Condition()
        self._active = 0
        self._active_by_key: Counter[str] = Counter()
        self._waiters: list[tuple[object, str]] = []

    def _first_eligible(self) -> object | None:
        if self._active >= self._max_active:
            return None
        for ticket, key in self._waiters:
            if self._active_by_key[key] < self._max_active_per_key:
                return ticket
        return None

    async def acquire(
        self,
        key: str,
        *,
        timeout_seconds: float | None = None,
    ) -> AdmissionPermit:
        if not key:
            raise ValueError("admission key is required")
        ticket = object()

        async def wait_for_turn() -> AdmissionPermit:
            async with self._condition:
                if (
                    not self._waiters
                    and self._active < self._max_active
                    and self._active_by_key[key] < self._max_active_per_key
                ):
                    self._active += 1
                    self._active_by_key[key] += 1
                    return AdmissionPermit(self, key)
                if len(self._waiters) >= self._max_waiters:
                    raise AdmissionRejected("waiter-capacity")
                self._waiters.append((ticket, key))
                try:
                    await self._condition.wait_for(
                        lambda: self._first_eligible() is ticket
                    )
                    self._waiters = [
                        item for item in self._waiters if item[0] is not ticket
                    ]
                    self._active += 1
                    self._active_by_key[key] += 1
                    self._condition.notify_all()
                    return AdmissionPermit(self, key)
                except BaseException:
                    self._waiters = [
                        item for item in self._waiters if item[0] is not ticket
                    ]
                    self._condition.notify_all()
                    raise

        try:
            if timeout_seconds is None:
                return await wait_for_turn()
            if timeout_seconds <= 0:
                raise AdmissionRejected("admission-timeout")
            return await asyncio.wait_for(wait_for_turn(), timeout_seconds)
        except TimeoutError as exc:
            raise AdmissionRejected("admission-timeout") from exc

    async def _release(self, key: str) -> None:
        async with self._condition:
            if self._active <= 0 or self._active_by_key[key] <= 0:
                raise RuntimeError("admission state underflow")
            self._active -= 1
            self._active_by_key[key] -= 1
            if self._active_by_key[key] == 0:
                del self._active_by_key[key]
            self._condition.notify_all()

    async def snapshot(self) -> AdmissionSnapshot:
        async with self._condition:
            return AdmissionSnapshot(
                active=self._active,
                waiting=len(self._waiters),
                active_by_key=dict(self._active_by_key),
                max_active=self._max_active,
                max_waiters=self._max_waiters,
            )
