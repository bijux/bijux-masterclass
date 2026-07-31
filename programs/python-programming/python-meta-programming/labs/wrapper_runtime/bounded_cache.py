from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable, Hashable
from dataclasses import dataclass
from functools import wraps
from typing import ParamSpec, Protocol, TypeVar, cast


Parameters = ParamSpec("Parameters")
ResultT = TypeVar("ResultT")
CacheKey = tuple[tuple[object, ...], tuple[tuple[str, object], ...]]


@dataclass(frozen=True, slots=True)
class CacheInfo:
    hits: int
    misses: int
    maxsize: int | None
    current_size: int


class CachedCallable(Protocol[Parameters, ResultT]):
    def __call__(
        self,
        *args: Parameters.args,
        **kwargs: Parameters.kwargs,
    ) -> ResultT: ...

    def cache_clear(self) -> None: ...

    def cache_info(self) -> CacheInfo: ...

    def cache_snapshot(self) -> tuple[CacheKey, ...]: ...


def _call_key(args: tuple[object, ...], kwargs: dict[str, object]) -> CacheKey:
    key = (args, tuple(sorted(kwargs.items())))
    try:
        hash(key)
    except TypeError as error:
        raise TypeError("bounded_cache requires hashable arguments") from error
    return key


def bounded_cache(
    maxsize: int | None = 128,
) -> Callable[
    [Callable[Parameters, ResultT]],
    CachedCallable[Parameters, ResultT],
]:
    """Cache successful calls with visible least-recently-used policy."""

    if maxsize is not None and maxsize < 0:
        raise ValueError("maxsize must be non-negative or None")

    def decorate(
        function: Callable[Parameters, ResultT],
    ) -> CachedCallable[Parameters, ResultT]:
        entries: OrderedDict[CacheKey, ResultT] = OrderedDict()
        hits = 0
        misses = 0

        @wraps(function)
        def wrapped(
            *args: Parameters.args,
            **kwargs: Parameters.kwargs,
        ) -> ResultT:
            nonlocal hits, misses
            key = _call_key(tuple(args), dict(kwargs))
            if key in entries:
                hits += 1
                result = entries.pop(key)
                entries[key] = result
                return result

            misses += 1
            result = function(*args, **kwargs)
            if maxsize == 0:
                return result

            if maxsize is not None and len(entries) >= maxsize:
                entries.popitem(last=False)
            entries[key] = result
            return result

        def cache_clear() -> None:
            nonlocal hits, misses
            entries.clear()
            hits = 0
            misses = 0

        def cache_info() -> CacheInfo:
            return CacheInfo(
                hits=hits,
                misses=misses,
                maxsize=maxsize,
                current_size=len(entries),
            )

        def cache_snapshot() -> tuple[CacheKey, ...]:
            return tuple(entries)

        wrapped.cache_clear = cache_clear  # type: ignore[attr-defined]
        wrapped.cache_info = cache_info  # type: ignore[attr-defined]
        wrapped.cache_snapshot = cache_snapshot  # type: ignore[attr-defined]
        return cast(CachedCallable[Parameters, ResultT], wrapped)

    return decorate
