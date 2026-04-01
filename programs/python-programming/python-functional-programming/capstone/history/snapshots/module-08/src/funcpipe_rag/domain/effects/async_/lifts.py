"""Module 08: lifting sync Result functions into AsyncPlan/AsyncGen (domain)."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from concurrent.futures import Executor
from typing import Any, TypeVar

from funcpipe_rag.result.types import Err, ErrInfo, Ok, Result

from .plan import AsyncPlan, async_from_result
from .stream import AsyncGen

T = TypeVar("T")


def lift_sync(f: Callable[..., Result[T, ErrInfo]]) -> Callable[..., AsyncPlan[T]]:
    def lifted(*args: Any, **kwargs: Any) -> AsyncPlan[T]:
        async def _act() -> Result[T, ErrInfo]:
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                return Err(ErrInfo.from_exception(exc))

        return lambda: _act()

    return lifted


def lift_sync_with_executor(
    f: Callable[..., Result[T, ErrInfo]],
    executor: Executor,
) -> Callable[..., AsyncPlan[T]]:
    def lifted(*args: Any, **kwargs: Any) -> AsyncPlan[T]:
        async def _act() -> Result[T, ErrInfo]:
            loop = asyncio.get_running_loop()
            try:
                return await loop.run_in_executor(executor, lambda: f(*args, **kwargs))
            except Exception as exc:
                return Err(ErrInfo.from_exception(exc))

        return lambda: _act()

    return lifted


def lift_sync_gen_with_executor(
    f: Callable[..., Result[list[T], ErrInfo]],
    executor: Executor,
) -> Callable[..., AsyncGen[T]]:
    def lifted(*args: Any, **kwargs: Any) -> AsyncGen[T]:
        async def _gen() -> AsyncIterator[Result[T, ErrInfo]]:
            loop = asyncio.get_running_loop()
            try:
                res = await loop.run_in_executor(executor, lambda: f(*args, **kwargs))
                if isinstance(res, Ok):
                    for item in res.value:
                        yield Ok(item)
                else:
                    yield Err(res.error)
            except Exception as exc:
                yield Err(ErrInfo.from_exception(exc))

        return lambda: _gen()

    return lifted


__all__ = [
    "lift_sync",
    "lift_sync_with_executor",
    "lift_sync_gen_with_executor",
    "async_from_result",
]
