"""Fan-out helpers for splitting streams (Module 03)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from itertools import islice, tee
from typing import TypeVar

from .types import Transform

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def tap_prefix(items: Iterable[T], k: int, hook: Callable[[tuple[T, ...]], None]) -> Iterator[T]:
    """Bounded side-effect tap: observe up to k items, then yield the full stream."""

    it = iter(items)
    head = tuple(islice(it, k))
    hook(head)
    yield from head
    yield from it


def fork2_lockstep(t: Transform[A, B], u: Transform[A, C]) -> Transform[A, tuple[B, C]]:
    """Strict 1:1 fan-out for transforms.

    Raises ValueError with the mismatch index if one branch produces more items
    than the other.
    """

    def stage(items: Iterable[A]) -> Iterator[tuple[B, C]]:
        a, b = tee(items, 2)
        it1 = iter(t(a))
        it2 = iter(u(b))
        i = 0
        while True:
            try:
                v1 = next(it1)
            except StopIteration:
                try:
                    extra = next(it2)
                except StopIteration:
                    return
                raise ValueError(f"fork2_lockstep mismatch at index={i}: second branch has extra item {extra!r}")

            try:
                v2 = next(it2)
            except StopIteration:
                raise ValueError(f"fork2_lockstep mismatch at index={i}: second branch exhausted early")

            yield (v1, v2)
            i += 1

    return stage


__all__ = ["tap_prefix", "fork2_lockstep"]

