"""Module 07: reusable effect composition helpers."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import TypeVar

from funcpipe_rag.core.rag_types import RawDoc
from funcpipe_rag.result.types import ErrInfo, Ok, Result

from .capabilities import Logger, StorageRead
from funcpipe_rag.domain.effects.io_plan import IOPlan, io_bind, io_delay
from .logging import LogEntry

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def chain_io(
    f: Callable[[A], IOPlan[B]],
    g: Callable[[B], IOPlan[C]],
) -> Callable[[A], IOPlan[C]]:
    return lambda a: io_bind(f(a), g)


def logged_read(storage: StorageRead, logger: Logger) -> Callable[[str], IOPlan[Iterator[Result[RawDoc, ErrInfo]]]]:
    def run(path: str) -> IOPlan[Iterator[Result[RawDoc, ErrInfo]]]:
        def act() -> Result[Iterator[Result[RawDoc, ErrInfo]], ErrInfo]:
            logger.log(LogEntry("INFO", f"read_docs path={path}"))
            return Ok(storage.read_docs(path))

        return io_delay(act)

    return run
