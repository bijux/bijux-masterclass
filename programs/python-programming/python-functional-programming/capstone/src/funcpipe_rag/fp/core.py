"""Shared functional containers and error helpers in the complete capstone."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Generic, TypeAlias, TypeVar

from funcpipe_rag.result.types import (
    NONE,
    Err,
    ErrInfo,
    NoneVal,
    Ok,
    Option,
    Result,
    Some,
)
from funcpipe_rag.result.types import (
    make_errinfo as _make_errinfo,
)

from .error import ErrorCode

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSON: TypeAlias = JSONPrimitive | Mapping[str, "JSON"] | Sequence["JSON"]


#
# Option is re-exported from `funcpipe_rag.result.types` so the codebase uses a
# single Option encoding everywhere.


@dataclass(frozen=True, slots=True)
class VSuccess(Generic[T, E]):
    value: T


@dataclass(frozen=True, slots=True)
class VFailure(Generic[E]):
    errors: tuple[E, ...]


Validation: TypeAlias = VSuccess[T, E] | VFailure[E]


def make_errinfo(
    *,
    code: str | ErrorCode,
    msg: str,
    stage: str = "",
    path: tuple[int, ...] = (),
    exc: BaseException | None = None,
    meta: Mapping[str, object] | None = None,
) -> ErrInfo:
    return _make_errinfo(code=str(code), msg=msg, stage=stage, path=path, cause=exc, ctx=meta)


__all__ = [
    "JSON",
    "NONE",
    "Err",
    "ErrInfo",
    "JSONPrimitive",
    "NoneVal",
    "Ok",
    "Option",
    "Result",
    "Some",
    "VFailure",
    "VSuccess",
    "Validation",
    "make_errinfo",
]
