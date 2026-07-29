"""Executable learning proofs for the Module 08 async coordination delta."""

from __future__ import annotations

import asyncio

from funcpipe_rag.domain.effects.async_ import async_lift
from funcpipe_rag.result.types import Ok


def test_async_plan_is_deferred_and_creates_fresh_awaitables() -> None:
    """Building a plan does nothing; each call describes a fresh execution."""

    calls = 0

    async def read_sequence() -> Ok[int]:
        nonlocal calls
        calls += 1
        return Ok(calls)

    plan = async_lift(read_sequence)

    assert calls == 0

    async def run() -> None:
        first = await plan()
        second = await plan()

        assert first == Ok(1)
        assert second == Ok(2)

    asyncio.run(run())
