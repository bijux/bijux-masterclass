from __future__ import annotations

from dataclasses import dataclass
import re
import secrets

_TRACEPARENT = re.compile(
    r"^(?P<version>[0-9a-f]{2})-(?P<trace>[0-9a-f]{32})-"
    r"(?P<span>[0-9a-f]{16})-(?P<flags>[0-9a-f]{2})$"
)
_HEX_ZERO_32 = "0" * 32
_HEX_ZERO_16 = "0" * 16


class TraceContextError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TraceContext:
    trace_id: str
    span_id: str
    sampled: bool = False
    tracestate: str | None = None
    remote: bool = False

    def traceparent(self) -> str:
        flags = "01" if self.sampled else "00"
        return f"00-{self.trace_id}-{self.span_id}-{flags}"

    def child(self, span_id: str | None = None) -> "TraceContext":
        value = span_id or secrets.token_hex(8)
        _validate_hex(value, 16, "span-id")
        return TraceContext(
            trace_id=self.trace_id,
            span_id=value,
            sampled=self.sampled,
            tracestate=self.tracestate,
            remote=False,
        )


def _validate_hex(value: str, length: int, label: str) -> None:
    if len(value) != length or not re.fullmatch(r"[0-9a-f]+", value):
        raise TraceContextError(f"invalid {label}")
    if set(value) == {"0"}:
        raise TraceContextError(f"zero {label} is invalid")


def parse_traceparent(value: str) -> TraceContext:
    """Parse the course's strict W3C Trace Context version-00 profile.

    The course deliberately does not claim to implement future-version parsing.
    Unknown versions are rejected instead of being silently reinterpreted.
    """

    match = _TRACEPARENT.fullmatch(value.strip())
    if not match:
        raise TraceContextError("malformed traceparent")
    if match.group("version") != "00":
        raise TraceContextError("unsupported traceparent version")
    trace_id = match.group("trace")
    span_id = match.group("span")
    if trace_id == _HEX_ZERO_32 or span_id == _HEX_ZERO_16:
        raise TraceContextError("zero trace or span identifier")
    flags = int(match.group("flags"), 16)
    return TraceContext(
        trace_id=trace_id,
        span_id=span_id,
        sampled=bool(flags & 0x01),
        remote=True,
    )


def new_root(*, sampled: bool = False) -> TraceContext:
    return TraceContext(
        trace_id=secrets.token_hex(16),
        span_id=secrets.token_hex(8),
        sampled=sampled,
    )
