from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .envelope import EventEnvelope


@dataclass(frozen=True, slots=True)
class ReplayPlan:
    replay_id: str
    consumer: str
    mode: str
    allowed_types: frozenset[str]
    maximum_events: int
    side_effects: str
    tenant_id: str | None = None


@dataclass(frozen=True, slots=True)
class ReplayReport:
    selected: int
    applied: int
    skipped: int
    would_apply: int


def execute_replay(
    plan: ReplayPlan,
    events: Iterable[EventEnvelope],
    handler: Callable[[EventEnvelope, bool], bool],
) -> ReplayReport:
    if plan.mode not in {"dry-run", "apply"}:
        raise ValueError("invalid replay mode")
    if plan.maximum_events <= 0:
        raise ValueError("maximum_events must be positive")
    if plan.side_effects != "disabled":
        raise ValueError("course replay requires side effects disabled")
    selected = applied = skipped = would_apply = 0
    for event in events:
        if event.type not in plan.allowed_types:
            continue
        if plan.tenant_id and event.tenantid != plan.tenant_id:
            continue
        selected += 1
        if selected > plan.maximum_events:
            raise RuntimeError("replay event bound exceeded")
        if plan.mode == "dry-run":
            if handler(event, True):
                would_apply += 1
        elif handler(event, False):
            applied += 1
        else:
            skipped += 1
    return ReplayReport(selected, applied, skipped, would_apply)
