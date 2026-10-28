from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class LifecyclePhase(str, Enum):
    STARTING = "starting"
    ACCEPTING = "accepting"
    DRAINING = "draining"
    STOPPED = "stopped"
    FAILED = "failed"


_ALLOWED_TRANSITIONS: dict[LifecyclePhase, frozenset[LifecyclePhase]] = {
    LifecyclePhase.STARTING: frozenset(
        {LifecyclePhase.ACCEPTING, LifecyclePhase.DRAINING, LifecyclePhase.FAILED}
    ),
    LifecyclePhase.ACCEPTING: frozenset(
        {LifecyclePhase.DRAINING, LifecyclePhase.FAILED}
    ),
    LifecyclePhase.DRAINING: frozenset(
        {LifecyclePhase.STOPPED, LifecyclePhase.FAILED}
    ),
    LifecyclePhase.FAILED: frozenset({LifecyclePhase.STOPPED}),
    LifecyclePhase.STOPPED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class LifecycleTransition:
    from_phase: LifecyclePhase
    to_phase: LifecyclePhase
    reason: str
    timestamp_ms: int


@dataclass(slots=True)
class LifecycleController:
    phase: LifecyclePhase = LifecyclePhase.STARTING
    history: list[LifecycleTransition] = field(default_factory=list)

    def transition(
        self,
        to_phase: LifecyclePhase,
        *,
        reason: str,
        timestamp_ms: int,
    ) -> LifecycleTransition:
        if not reason or len(reason) > 120:
            raise ValueError("transition reason must contain 1..120 characters")
        if to_phase not in _ALLOWED_TRANSITIONS[self.phase]:
            raise ValueError(
                f"invalid lifecycle transition {self.phase.value}->{to_phase.value}"
            )
        item = LifecycleTransition(self.phase, to_phase, reason, timestamp_ms)
        self.phase = to_phase
        self.history.append(item)
        return item


@dataclass(frozen=True, slots=True)
class ComponentHealth:
    name: str
    required_for_readiness: bool
    available: bool
    detail: str = ""


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    live: bool
    ready: bool
    startup_complete: bool
    phase: LifecyclePhase
    reasons: tuple[str, ...] = field(default_factory=tuple)


class HealthEvaluator:
    def evaluate(
        self,
        *,
        phase: LifecyclePhase,
        startup_complete: bool,
        event_loop_progressing: bool,
        components: list[ComponentHealth],
    ) -> HealthSnapshot:
        reasons: list[str] = []
        live = (
            phase not in {LifecyclePhase.STOPPED, LifecyclePhase.FAILED}
            and event_loop_progressing
        )
        if not live:
            reasons.append("process-cannot-make-progress")
        if phase is LifecyclePhase.FAILED:
            reasons.append("lifecycle-failed")
        if not startup_complete:
            reasons.append("startup-incomplete")
        unavailable = [
            item.name
            for item in components
            if item.required_for_readiness and not item.available
        ]
        reasons.extend(
            f"required-component-unavailable:{name}" for name in unavailable
        )
        ready = (
            live
            and startup_complete
            and phase is LifecyclePhase.ACCEPTING
            and not unavailable
        )
        if phase is LifecyclePhase.DRAINING:
            reasons.append("draining")
        return HealthSnapshot(
            live=live,
            ready=ready,
            startup_complete=startup_complete,
            phase=phase,
            reasons=tuple(reasons),
        )
