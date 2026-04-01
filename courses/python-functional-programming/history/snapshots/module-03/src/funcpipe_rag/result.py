"""Minimal Result type for boundary-safe APIs (Modules 02–03).

Introduced in Module 02 and used throughout Module 03: a small
``Result[T] = Ok[T] | Err`` union to make failure explicit at boundaries
(I/O, parsing) without raising exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T


@dataclass(frozen=True)
class Err:
    error: str


Result = Union[Ok[T], Err]


def result_map(res: Result[T], fn: Callable[[T], U]) -> Result[U]:
    if isinstance(res, Err):
        return res
    return Ok(fn(res.value))


def result_and_then(res: Result[T], fn: Callable[[T], Result[U]]) -> Result[U]:
    if isinstance(res, Err):
        return res
    return fn(res.value)


__all__ = ["Ok", "Err", "Result", "result_map", "result_and_then"]
