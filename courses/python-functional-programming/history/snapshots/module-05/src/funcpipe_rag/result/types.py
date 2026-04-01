"""Result/Option containers for pure, streaming-friendly error handling (end-of-Module-05)."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Generic, Mapping, NamedTuple, TypeAlias, TypeGuard, TypeVar

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
F = TypeVar("F")


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    def map(self, f: Callable[[T], U]) -> "Ok[U]":
        return Ok(f(self.value))

    def map_err(self, f: Callable[[E], F]) -> "Ok[T]":
        _ = f
        return self

    def bind(self, f: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return f(self.value)

    def recover(self, f: Callable[[E], T]) -> "Ok[T]":
        _ = f
        return self

    def unwrap_or(self, default: T) -> T:
        _ = default
        return self.value

    def to_option(self) -> "Option[T]":
        return Some(self.value)


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E

    def map(self, f: Callable[[T], U]) -> "Err[E]":
        _ = f
        return self

    def map_err(self, f: Callable[[E], F]) -> "Err[F]":
        return Err(f(self.error))

    def bind(self, f: Callable[[T], "Result[U, E]"]) -> "Err[E]":
        _ = f
        return self

    def recover(self, f: Callable[[E], T]) -> Ok[T]:
        return Ok(f(self.error))

    def unwrap_or(self, default: T) -> T:
        return default

    def to_option(self) -> "Option[T]":
        return Nothing()


Result: TypeAlias = Ok[T] | Err[E]


def is_ok(r: Result[T, E]) -> TypeGuard[Ok[T]]:
    return isinstance(r, Ok)


def is_err(r: Result[T, E]) -> TypeGuard[Err[E]]:
    return isinstance(r, Err)


def map_result(f: Callable[[T], U], r: Result[T, E]) -> Result[U, E]:
    return r.map(f)


def map_err(f: Callable[[E], F], r: Result[T, E]) -> Result[T, F]:
    return r.map_err(f)


def bind_result(f: Callable[[T], Result[U, E]], r: Result[T, E]) -> Result[U, E]:
    return r.bind(f)


def recover(f: Callable[[E], T], r: Result[T, E]) -> Result[T, E]:
    return r.recover(f)


def unwrap_or(r: Result[T, E], default: T) -> T:
    return r.unwrap_or(default)


@dataclass(frozen=True)
class Some(Generic[T]):
    value: T

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("Some(None) forbidden – use Nothing()")

    def map(self, f: Callable[[T], U]) -> "Option[U]":
        return Some(f(self.value))

    def bind(self, f: Callable[[T], "Option[U]"]) -> "Option[U]":
        return f(self.value)

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        _ = default
        return self.value


@dataclass(frozen=True)
class Nothing(Generic[T]):
    def map(self, f: Callable[[T], U]) -> "Option[U]":
        _ = f
        return Nothing()

    def bind(self, f: Callable[[T], "Option[U]"]) -> "Option[U]":
        _ = f
        return Nothing()

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return default()


Option: TypeAlias = Some[T] | Nothing[T]


def to_option(r: Result[T, E]) -> Option[T]:
    return r.to_option()


def is_some(o: Option[T]) -> TypeGuard[Some[T]]:
    return isinstance(o, Some)


def is_nothing(o: Option[T]) -> TypeGuard[Nothing[T]]:
    return isinstance(o, Nothing)


def map_option(f: Callable[[T], U], o: Option[T]) -> Option[U]:
    return o.map(f)


def bind_option(f: Callable[[T], Option[U]], o: Option[T]) -> Option[U]:
    return o.bind(f)


def unwrap_or_else(o: Option[T], default: Callable[[], T]) -> T:
    return o.unwrap_or_else(default)


class ErrInfo(NamedTuple):
    """Structured error provenance for per-record failures."""

    code: str
    msg: str
    stage: str = ""
    path: tuple[int, ...] = ()
    cause: BaseException | None = None
    ctx: Mapping[str, object] | None = None


def make_errinfo(
    code: str,
    msg: str,
    stage: str = "",
    path: tuple[int, ...] = (),
    cause: BaseException | None = None,
    ctx: Mapping[str, object] | None = None,
    *,
    exc: BaseException | None = None,
    meta: Mapping[str, object] | None = None,
) -> ErrInfo:
    if cause is not None and exc is not None:
        raise ValueError("Provide only one of: cause, exc")
    if ctx is not None and meta is not None:
        raise ValueError("Provide only one of: ctx, meta")
    if exc is not None:
        cause = exc
    if meta is not None:
        ctx = meta
    if ctx is not None:
        if not isinstance(ctx, Mapping):
            raise ValueError("ErrInfo.ctx must be a mapping when provided")
        if isinstance(ctx, dict):
            ctx = MappingProxyType(dict(ctx))
    return ErrInfo(code=code, msg=msg, stage=stage, path=path, cause=cause, ctx=ctx)


# Module 02 legacy names (kept for boundary/shell style)
def result_map(res: Result[T, E], fn: Callable[[T], U]) -> Result[U, E]:
    return map_result(fn, res)


def result_and_then(res: Result[T, E], fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
    return bind_result(fn, res)


__all__ = [
    "Result",
    "Ok",
    "Err",
    "ErrInfo",
    "make_errinfo",
    "is_ok",
    "is_err",
    "map_result",
    "map_err",
    "bind_result",
    "recover",
    "unwrap_or",
    "to_option",
    "Option",
    "Some",
    "Nothing",
    "is_some",
    "is_nothing",
    "map_option",
    "bind_option",
    "unwrap_or_else",
    "result_map",
    "result_and_then",
]
