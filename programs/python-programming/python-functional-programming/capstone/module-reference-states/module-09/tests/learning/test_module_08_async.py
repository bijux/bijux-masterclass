"""Executable learning proofs for the Module 08 async coordination delta."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from funcpipe_rag.domain.effects.async_ import (
    AsyncGen,
    AsyncPlan,
    BackpressurePolicy,
    ChunkPolicy,
    FairnessPolicy,
    FakeClock,
    FakeSleeper,
    RetryPolicy,
    TimeoutPolicy,
    async_gen_bounded_map,
    async_gen_chunk,
    async_gen_from_list,
    async_gen_fair_merge,
    async_gen_map,
    async_gen_using,
    async_lift,
    async_with_resilience,
    lift_sync,
    make_fake_timeout_ctx,
    make_test_resilience_env,
)
from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result


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


def test_retry_policy_records_bounded_attempts_and_backoff() -> None:
    """Injected sleep turns exponential retry behavior into inspectable evidence."""

    attempts = 0
    delays: list[float] = []

    async def flaky_step() -> Result[int, ErrInfo]:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            return Err(ErrInfo(code="TRANSIENT", msg="try again"))
        return Ok(42)

    async def record_sleep(seconds: float) -> None:
        delays.append(seconds)
        await asyncio.sleep(0)

    resilient = async_with_resilience(
        flaky_step,
        RetryPolicy(
            max_attempts=3,
            backoff_base_ms=10,
            max_backoff_ms=100,
            jitter_factor=0,
        ),
        env=make_test_resilience_env(sleep=record_sleep),
    )

    assert attempts == 0
    assert asyncio.run(resilient()) == Ok(42)
    assert attempts == 3
    assert delays == [0.01, 0.02]


def test_fake_clock_replays_the_same_timeout_decision() -> None:
    """Logical time makes a timeout branch fast, repeatable, and inspectable."""

    def run_once() -> tuple[Result[int, ErrInfo], float]:
        clock = FakeClock()

        async def step() -> Result[int, ErrInfo]:
            clock.advance_s(0.051)
            return Ok(42)

        plan = async_with_resilience(
            step,
            RetryPolicy(max_attempts=1),
            TimeoutPolicy(timeout_ms=50),
            env=make_test_resilience_env(clock=clock),
            timeout_ctx=make_fake_timeout_ctx(clock),
        )
        return asyncio.run(plan()), clock.now_s()

    first = run_once()
    second = run_once()

    assert first == second
    result, elapsed = first
    assert isinstance(result, Err)
    assert result.error.code == "TIMEOUT"
    assert elapsed == 0.051


def test_weighted_fair_merge_makes_each_share_observable() -> None:
    """A two-to-one policy gives both ready streams progress in every cycle."""

    def tagged_stream(tag: str) -> AsyncGen[str]:
        async def generate() -> AsyncIterator[Result[str, ErrInfo]]:
            index = 0
            while True:
                yield Ok(f"{tag}-{index}")
                index += 1

        return generate

    merged = async_gen_fair_merge(
        [tagged_stream("A"), tagged_stream("B")],
        FairnessPolicy(weights={0: 2, 1: 1}, max_buffer_per_stream=2),
    )

    async def consume_prefix() -> list[Result[str, ErrInfo]]:
        iterator = merged()
        prefix = [await anext(iterator) for _ in range(6)]
        await iterator.aclose()
        return prefix

    results = asyncio.run(consume_prefix())
    tags = [item.value.split("-")[0] for item in results if isinstance(item, Ok)]

    assert tags == ["A", "B", "A", "A", "B", "A"]
    assert tags.count("A") == 4
    assert tags.count("B") == 2


def test_sync_lift_defers_work_and_translates_exceptions() -> None:
    """The adapter protects a synchronous core from async and exception creep."""

    calls = 0

    def parse_positive(value: int) -> Result[int, ErrInfo]:
        nonlocal calls
        calls += 1
        if value < 0:
            raise ValueError("negative input")
        return Ok(value)

    lifted_parse = lift_sync(parse_positive)
    plan = lifted_parse(-1)

    assert calls == 0

    result = asyncio.run(plan())

    assert calls == 1
    assert isinstance(result, Err)
    assert result.error.code == "UNEXPECTED"
    assert result.error.msg == "negative input"


def test_service_stream_releases_resource_after_partial_consumption() -> None:
    """Closing a consumer prefix exits the service resource exactly once."""

    events: list[str] = []

    @asynccontextmanager
    async def service_session() -> AsyncIterator[str]:
        events.append("enter")
        try:
            yield "embedding-service"
        finally:
            events.append("exit")

    def responses(service: str) -> AsyncGen[str]:
        async def generate() -> AsyncIterator[Result[str, ErrInfo]]:
            for index in range(3):
                events.append(f"pull:{index}")
                yield Ok(f"{service}:{index}")

        return generate

    stream = async_gen_using(service_session, responses)

    assert events == []

    async def consume_one() -> Result[str, ErrInfo]:
        iterator = stream()
        first = await anext(iterator)
        await iterator.aclose()
        return first

    assert asyncio.run(consume_one()) == Ok("embedding-service:0")
    assert events == ["enter", "pull:0", "exit"]


def test_chunk_policy_flushes_values_before_an_error() -> None:
    """A typed stream error is a boundary, not a reason to lose buffered values."""

    failure = ErrInfo(code="SOURCE", msg="malformed record")

    async def source_items() -> AsyncIterator[Result[int, ErrInfo]]:
        yield Ok(1)
        yield Ok(2)
        yield Err(failure)
        yield Ok(3)

    source: AsyncGen[int] = source_items
    chunked = async_gen_chunk(
        source,
        ChunkPolicy[int](max_units=10, max_delay_ms=0, flush_on_err=True),
    )(FakeSleeper())

    async def consume() -> list[Result[list[int], ErrInfo]]:
        return [item async for item in chunked()]

    assert asyncio.run(consume()) == [Ok([1, 2]), Err(failure), Ok([3])]
