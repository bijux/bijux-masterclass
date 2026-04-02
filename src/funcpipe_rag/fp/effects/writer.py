"""Module 06: Writer – accumulate logs/metrics as pure data (effects)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Tuple, TypeVar

from funcpipe_rag.result.types import Err, Ok, Result

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")

LogEntry = str
Log = Tuple[LogEntry, ...]


@dataclass(frozen=True)
class Writer(Generic[T]):
    run: Callable[[], Tuple[T, Log]]

    def map(self, f: Callable[[T], U]) -> "Writer[U]":
        def _run() -> Tuple[U, Log]:
            value, log = self.run()
            return f(value), log

        return Writer(_run)

    def and_then(self, f: Callable[[T], "Writer[U]"]) -> "Writer[U]":
        def _run() -> Tuple[U, Log]:
            value, log1 = self.run()
            next_value, log2 = f(value).run()
            return next_value, log1 + log2

        return Writer(_run)


def pure(x: T) -> Writer[T]:
    return Writer(lambda: (x, ()))


def tell(entry: LogEntry) -> Writer[None]:
    return Writer(lambda: (None, (entry,)))


def tell_many(entries: Log) -> Writer[None]:
    return Writer(lambda: (None, entries))


def listen(p: Writer[T]) -> Writer[Tuple[T, Log]]:
    def _run() -> Tuple[Tuple[T, Log], Log]:
        value, log = p.run()
        return (value, log), log

    return Writer(_run)


def censor(f: Callable[[Log], Log], p: Writer[T]) -> Writer[T]:
    def _run() -> Tuple[T, Log]:
        value, log = p.run()
        return value, f(log)

    return Writer(_run)


def run_writer(p: Writer[T]) -> Tuple[T, Log]:
    return p.run()


def wr_pure(x: T) -> Writer[Result[T, E]]:
    return Writer(lambda: (Ok(x), ()))


def wr_map(p: Writer[Result[T, E]], f: Callable[[T], U]) -> Writer[Result[U, E]]:
    def _run() -> Tuple[Result[U, E], Log]:
        r, log = p.run()
        return r.map(f), log

    return Writer(_run)


def wr_and_then(p: Writer[Result[T, E]], k: Callable[[T], Writer[Result[U, E]]]) -> Writer[Result[U, E]]:
    def _run() -> Tuple[Result[U, E], Log]:
        r, log1 = p.run()
        if isinstance(r, Err):
            return Err(r.error), log1
        next_r, log2 = k(r.value).run()
        return next_r, log1 + log2

    return Writer(_run)


__all__ = [
    "LogEntry",
    "Log",
    "Writer",
    "pure",
    "tell",
    "tell_many",
    "listen",
    "censor",
    "run_writer",
    "wr_pure",
    "wr_map",
    "wr_and_then",
]
