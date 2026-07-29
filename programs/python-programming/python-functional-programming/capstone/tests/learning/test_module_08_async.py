"""Executable learning proofs for the Module 08 async coordination delta."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from funcpipe_rag.domain.effects.async_ import (
    AsyncGen,
    AsyncPlan,
    BackpressurePolicy,
    async_gen_bounded_map,
    async_gen_from_list,
    async_gen_map,
    async_lift,
)
from funcpipe_rag.result.types import ErrInfo, Ok, Result


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


def test_async_stream_pulls_only_what_the_consumer_requests() -> None:
    """A stream description stays lazy when it is transformed and consumed."""

    pulled: list[int] = []

    async def source_items() -> AsyncIterator[Result[int, ErrInfo]]:
        for value in (1, 2, 3):
            pulled.append(value)
            yield Ok(value)

    source: AsyncGen[int] = source_items
    doubled = async_gen_map(source, lambda value: value * 2)

    assert pulled == []

    async def consume_prefix() -> None:
        iterator = doubled()
        assert await anext(iterator) == Ok(2)
        assert await anext(iterator) == Ok(4)
        await iterator.aclose()

    asyncio.run(consume_prefix())

    assert pulled == [1, 2]


def test_bounded_map_caps_in_flight_work_and_preserves_order() -> None:
    """The policy is observable as a concurrency bound and an ordering law."""

    active = 0
    maximum_active = 0

    def multiply(value: int) -> AsyncPlan[int]:
        async def run() -> Ok[int]:
            nonlocal active, maximum_active
            active += 1
            maximum_active = max(maximum_active, active)
            await asyncio.sleep(0)
            active -= 1
            return Ok(value * 10)

        return run

    source = async_gen_from_list([1, 2, 3, 4])
    bounded = async_gen_bounded_map(
        source,
        multiply,
        BackpressurePolicy(max_concurrent=2, ordered=True),
    )

    async def consume() -> list[Result[int, ErrInfo]]:
        return [item async for item in bounded()]

    assert asyncio.run(consume()) == [Ok(10), Ok(20), Ok(30), Ok(40)]
    assert maximum_active == 2
