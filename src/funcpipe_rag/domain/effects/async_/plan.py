"""Module 08: AsyncPlan – deferred, replayable async effects as data (domain).

`AsyncPlan[A]` is a pure *description* of async work. Calling the thunk produces a
fresh coroutine each time (replayability), and awaiting it yields a
`Result[A, ErrInfo]`.

Driving a plan (`await`, `asyncio.run`, task creation) belongs in shells/adapters,
never in the domain core.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeAlias, TypeVar

from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result

A = TypeVar("A")
B = TypeVar("B")

AsyncPlan: TypeAlias = Callable[[], Awaitable[Result[A, ErrInfo]]]
AsyncAction: TypeAlias = AsyncPlan[A]


def async_pure(value: A) -> AsyncPlan[A]:
    async def _coro() -> Result[A, ErrInfo]:
        return Ok(value)

    return lambda: _coro()


def async_from_result(res: Result[A, ErrInfo]) -> AsyncPlan[A]:
    async def _coro() -> Result[A, ErrInfo]:
        return res

    return lambda: _coro()


def async_bind(plan: AsyncPlan[A], f: Callable[[A], AsyncPlan[B]]) -> AsyncPlan[B]:
    async def _coro() -> Result[B, ErrInfo]:
        res = await plan()
        if isinstance(res, Err):
            return Err(res.error)
        return await f(res.value)()

    return lambda: _coro()


def async_map(plan: AsyncPlan[A], f: Callable[[A], B]) -> AsyncPlan[B]:
    return async_bind(plan, lambda x: async_pure(f(x)))


def async_lift(make_coro: Callable[[], Awaitable[Result[A, ErrInfo]]]) -> AsyncPlan[A]:
    """Lift a capability coroutine factory into a replayable AsyncPlan.

    Precondition: `make_coro` must create a fresh coroutine object on each call.
    """

    return make_coro


def async_gather(plans: list[AsyncPlan[A]], *, concurrency: int = 16) -> AsyncPlan[list[A]]:
    """Run independent AsyncPlans with bounded concurrency and preserve list order.

    Semantics:
    - Returns `Ok(list_of_values)` if all plans return Ok.
    - Returns `Err(first_error_by_index)` if any plan returns Err.
    - Exceptions raised by plan coroutines are translated to `ErrInfo`.
    """

    if concurrency < 1:
        raise ValueError("concurrency must be >= 1")

    async def _coro() -> Result[list[A], ErrInfo]:
        n = len(plans)
        if n == 0:
            return Ok([])

        sem = asyncio.Semaphore(concurrency)
        pending: set[asyncio.Task[tuple[int, Result[A, ErrInfo]]]] = set()
        results: list[Result[A, ErrInfo] | None] = [None] * n
        next_idx = 0

        async def worker(i: int, plan: AsyncPlan[A]) -> tuple[int, Result[A, ErrInfo]]:
            try:
                return i, await plan()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # pragma: no cover - defensive
                return i, Err(ErrInfo.from_exception(exc))
            finally:
                sem.release()

        try:
            while next_idx < n and len(pending) < concurrency:
                await sem.acquire()
                pending.add(asyncio.create_task(worker(next_idx, plans[next_idx])))
                next_idx += 1

            while pending:
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    i, res = task.result()
                    results[i] = res

                while next_idx < n and len(pending) < concurrency:
                    await sem.acquire()
                    pending.add(asyncio.create_task(worker(next_idx, plans[next_idx])))
                    next_idx += 1
        finally:
            for task in pending:
                task.cancel()
            if pending:
                _ = await asyncio.gather(*pending, return_exceptions=True)

        first_err: ErrInfo | None = None
        values: list[A] = []
        for item in results:
            assert item is not None
            if isinstance(item, Err):
                if first_err is None:
                    first_err = item.error
            else:
                values.append(item.value)
        if first_err is not None:
            return Err(first_err)
        return Ok(values)

    return lambda: _coro()


__all__ = [
    "AsyncPlan",
    "AsyncAction",
    "async_pure",
    "async_from_result",
    "async_bind",
    "async_map",
    "async_lift",
    "async_gather",
]
