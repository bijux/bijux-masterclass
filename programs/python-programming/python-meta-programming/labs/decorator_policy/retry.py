from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import ParamSpec, Protocol, TypeVar, cast


Parameters = ParamSpec("Parameters")
ResultT = TypeVar("ResultT")


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """The public stopping and waiting rules captured by ``retry``."""

    exception_names: tuple[str, ...]
    max_attempts: int
    backoff_seconds: tuple[float, ...]


class RetryingCallable(Protocol[Parameters, ResultT]):
    __retry_policy__: RetryPolicy

    def __call__(
        self,
        *args: Parameters.args,
        **kwargs: Parameters.kwargs,
    ) -> ResultT: ...


def retry(
    *,
    exceptions: tuple[type[Exception], ...],
    max_attempts: int,
    backoff_seconds: tuple[float, ...] = (),
    sleep: Callable[[float], None] = time.sleep,
) -> Callable[
    [Callable[Parameters, ResultT]],
    RetryingCallable[Parameters, ResultT],
]:
    """Retry named failures with a finite, inspectable stopping rule."""

    if not exceptions:
        raise ValueError("exceptions must name at least one retryable failure")
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if len(backoff_seconds) != max_attempts - 1:
        raise ValueError("backoff_seconds must contain one delay between each attempt")
    if any(delay < 0 for delay in backoff_seconds):
        raise ValueError("backoff_seconds cannot contain negative delays")

    policy = RetryPolicy(
        exception_names=tuple(error.__name__ for error in exceptions),
        max_attempts=max_attempts,
        backoff_seconds=backoff_seconds,
    )

    def decorate(
        function: Callable[Parameters, ResultT],
    ) -> RetryingCallable[Parameters, ResultT]:
        @wraps(function)
        def wrapped(
            *args: Parameters.args,
            **kwargs: Parameters.kwargs,
        ) -> ResultT:
            for attempt_index in range(policy.max_attempts):
                try:
                    return function(*args, **kwargs)
                except exceptions:
                    if attempt_index == policy.max_attempts - 1:
                        raise
                    sleep(policy.backoff_seconds[attempt_index])
            raise AssertionError("finite retry loop ended without returning or raising")

        wrapped.__retry_policy__ = policy  # type: ignore[attr-defined]
        return cast(RetryingCallable[Parameters, ResultT], wrapped)

    return decorate
