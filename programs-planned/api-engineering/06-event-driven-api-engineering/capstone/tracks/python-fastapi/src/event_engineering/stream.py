from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .envelope import EventEnvelope


@dataclass(frozen=True, slots=True)
class WindowResult:
    tenant_id: str
    start: datetime
    end: datetime
    completed: int
    failed: int
    duration_ms: int
    revision: int


@dataclass(frozen=True, slots=True)
class LateEvent:
    event_id: str
    tenant_id: str
    event_time: datetime
    watermark: datetime
    reason: str


class EventTimeWindows:
    def __init__(self, width: timedelta, allowed_lateness: timedelta) -> None:
        if width.total_seconds() <= 0 or allowed_lateness.total_seconds() < 0:
            raise ValueError("invalid window policy")
        self.width = width
        self.allowed_lateness = allowed_lateness
        self.watermark = datetime.min.replace(tzinfo=timezone.utc)
        self._windows: dict[tuple[str, datetime], dict[str, int]] = {}
        self._seen: set[str] = set()
        self.late_events: list[LateEvent] = []

    @staticmethod
    def _parse_time(event: EventEnvelope) -> datetime:
        value = event.data.get("occurredAt", event.time)
        if not isinstance(value, str):
            raise ValueError("event time field must be text")
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("event time must include an offset")
        return parsed.astimezone(timezone.utc)

    def advance_watermark(self, value: datetime) -> None:
        if value.tzinfo is None:
            raise ValueError("watermark must be timezone-aware")
        normalized = value.astimezone(timezone.utc)
        if normalized < self.watermark:
            raise ValueError("watermark cannot move backwards")
        self.watermark = normalized

    def _window_start(self, value: datetime) -> datetime:
        seconds = int(value.timestamp())
        width = int(self.width.total_seconds())
        return datetime.fromtimestamp(seconds - (seconds % width), tz=timezone.utc)

    def apply(self, event: EventEnvelope) -> WindowResult | None:
        if event.id in self._seen:
            return None
        event_time = self._parse_time(event)
        threshold = (
            self.watermark - self.allowed_lateness
            if self.watermark.year > 1
            else self.watermark
        )
        if event_time < threshold:
            self.late_events.append(
                LateEvent(
                    event.id,
                    event.tenantid,
                    event_time,
                    self.watermark,
                    "beyond-allowed-lateness",
                )
            )
            self._seen.add(event.id)
            return None
        start = self._window_start(event_time)
        identity = (event.tenantid, start)
        row = self._windows.setdefault(
            identity,
            {"completed": 0, "failed": 0, "duration": 0, "revision": 0},
        )
        if event.type.endswith("run.completed.v1"):
            row["completed"] += 1
            row["duration"] += int(event.data.get("durationMs", 0))
        elif event.type.endswith("run.failed.v1"):
            row["failed"] += 1
        else:
            return None
        row["revision"] += 1
        self._seen.add(event.id)
        return WindowResult(
            event.tenantid,
            start,
            start + self.width,
            row["completed"],
            row["failed"],
            row["duration"],
            row["revision"],
        )

    def snapshot(self) -> list[WindowResult]:
        results: list[WindowResult] = []
        for (tenant, start), row in sorted(self._windows.items()):
            results.append(
                WindowResult(
                    tenant,
                    start,
                    start + self.width,
                    row["completed"],
                    row["failed"],
                    row["duration"],
                    row["revision"],
                )
            )
        return results
