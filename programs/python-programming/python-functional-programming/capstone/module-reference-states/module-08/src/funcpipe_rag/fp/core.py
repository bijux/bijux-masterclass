"""Module 05 core ADTs (products + tagged sums) and stable JSON helpers (end-of-Module-08)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Generic, Literal, Mapping, Sequence, TypeAlias, TypeVar

from .error import ErrorCode
from funcpipe_rag.result.types import (
    Err,
    ErrInfo,
    NoneVal,
    Ok,
    Option,
    Result,
    Some,
    NONE,
    make_errinfo as _make_errinfo,
)

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSON: TypeAlias = JSONPrimitive | Mapping[str, "JSON"] | Sequence["JSON"]
UTC = timezone.utc


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


# State ADTs (C02)
@dataclass(frozen=True, slots=True, kw_only=True)
class EvStart:
    started_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class EvAdvance:
    delta_permille: int


@dataclass(frozen=True, slots=True, kw_only=True)
class EvSucceed:
    completed_at: datetime
    artifact_id: str
    dim: int
    sha256: str


@dataclass(frozen=True, slots=True, kw_only=True)
class EvFail:
    failed_at: datetime
    code: ErrorCode
    msg: str
    attempt: int


Event: TypeAlias = EvStart | EvAdvance | EvSucceed | EvFail


def start_event(*, started_at: datetime) -> EvStart:
    if started_at.tzinfo is None:
        raise ValueError("started_at must be timezone-aware")
    return EvStart(started_at=started_at)


def advance_event(*, delta_permille: int) -> EvAdvance:
    if delta_permille < 0:
        raise ValueError("delta_permille must be ≥0 — progress is monotonic")
    return EvAdvance(delta_permille=delta_permille)


def succeed_event(*, completed_at: datetime, artifact_id: str, dim: int, sha256: str) -> EvSucceed:
    if completed_at.tzinfo is None:
        raise ValueError("completed_at must be timezone-aware")
    return EvSucceed(completed_at=completed_at, artifact_id=artifact_id, dim=dim, sha256=sha256)


def fail_event(*, failed_at: datetime, code: ErrorCode, msg: str, attempt: int) -> EvFail:
    if failed_at.tzinfo is None:
        raise ValueError("failed_at must be timezone-aware")
    if attempt < 1:
        raise ValueError("attempt must be ≥1")
    return EvFail(failed_at=failed_at, code=code, msg=msg, attempt=attempt)


@dataclass(frozen=True, slots=True, kw_only=True)
class Pending:
    kind: Literal["pending"] = "pending"
    queued_at: datetime
    version: Literal[1] = 1


@dataclass(frozen=True, slots=True, kw_only=True)
class Running:
    kind: Literal["running"] = "running"
    started_at: datetime
    progress_permille: int
    version: Literal[1] = 1


@dataclass(frozen=True, slots=True, kw_only=True)
class Done:
    kind: Literal["done"] = "done"
    completed_at: datetime
    artifact_id: str
    dim: int
    sha256: str
    version: Literal[1] = 1


@dataclass(frozen=True, slots=True, kw_only=True)
class Failed:
    kind: Literal["failed"] = "failed"
    failed_at: datetime
    code: ErrorCode
    msg: str
    attempt: int
    version: Literal[1] = 1


ProcessingState: TypeAlias = Pending | Running | Done | Failed


def pending(*, queued_at: datetime) -> Pending:
    if queued_at.tzinfo is None:
        raise ValueError("queued_at must be timezone-aware")
    return Pending(queued_at=queued_at)


def running(*, started_at: datetime, progress_permille: int) -> Running:
    if started_at.tzinfo is None:
        raise ValueError("started_at must be timezone-aware")
    if not 0 <= progress_permille <= 1000:
        raise ValueError("progress_permille must be 0–1000")
    return Running(started_at=started_at, progress_permille=progress_permille)


def done(*, completed_at: datetime, artifact_id: str, dim: int, sha256: str) -> Done:
    if completed_at.tzinfo is None:
        raise ValueError("completed_at must be timezone-aware")
    if dim <= 0:
        raise ValueError("dim must be > 0")
    if len(sha256) != 64 or not all(c in "0123456789abcdefABCDEF" for c in sha256):
        raise ValueError("sha256 must be a 64-hex string")
    return Done(completed_at=completed_at, artifact_id=artifact_id, dim=dim, sha256=sha256)


def failed(*, failed_at: datetime, code: ErrorCode, msg: str, attempt: int) -> Failed:
    if failed_at.tzinfo is None:
        raise ValueError("failed_at must be timezone-aware")
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    return Failed(failed_at=failed_at, code=code, msg=msg, attempt=attempt)


def transition(state: ProcessingState, event: Event) -> ProcessingState:
    match state, event:
        case Pending(), EvStart(started_at=s):
            if s < state.queued_at:
                raise ValueError("started_at cannot be earlier than queued_at")
            return running(started_at=s, progress_permille=0)

        case Running(), EvAdvance(delta_permille=d):
            new_p = min(1000, state.progress_permille + d)
            return running(started_at=state.started_at, progress_permille=new_p)

        case Running(), EvSucceed(completed_at=c, artifact_id=a, dim=d, sha256=h):
            if c < state.started_at:
                raise ValueError("completed_at cannot be earlier than started_at")
            return done(completed_at=c, artifact_id=a, dim=d, sha256=h)

        case Running(), EvFail(failed_at=f, code=c, msg=m, attempt=a):
            if f < state.started_at:
                raise ValueError("failed_at cannot be earlier than started_at")
            return failed(failed_at=f, code=c, msg=m, attempt=a)

        case (Done() | Failed()), _:
            return state

    raise ValueError(f"invalid transition {state.kind} ← {event.__class__.__name__}")


__all__ = [
    # JSON values
    "JSONPrimitive",
    "JSON",
    # Option + Validation ADTs
    "Option",
    "Some",
    "NoneVal",
    "NONE",
    "Validation",
    "VSuccess",
    "VFailure",
    # Result/ErrInfo
    "Result",
    "Ok",
    "Err",
    "ErrInfo",
    "make_errinfo",
    # State machine (C02)
    "UTC",
    "ErrorCode",
    "Event",
    "EvStart",
    "EvAdvance",
    "EvSucceed",
    "EvFail",
    "start_event",
    "advance_event",
    "succeed_event",
    "fail_event",
    "ProcessingState",
    "Pending",
    "Running",
    "Done",
    "Failed",
    "pending",
    "running",
    "done",
    "failed",
    "transition",
]
