from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from .model import ValidationError


class ExtractionPhase(str, Enum):
    LEGACY = "legacy"
    SHADOW = "shadow"
    CANARY = "canary"
    CUTOVER = "cutover"
    DECOMMISSIONED = "decommissioned"


_ALLOWED: dict[ExtractionPhase, set[ExtractionPhase]] = {
    ExtractionPhase.LEGACY: {ExtractionPhase.SHADOW},
    ExtractionPhase.SHADOW: {ExtractionPhase.LEGACY, ExtractionPhase.CANARY},
    ExtractionPhase.CANARY: {ExtractionPhase.SHADOW, ExtractionPhase.CUTOVER},
    ExtractionPhase.CUTOVER: {
        ExtractionPhase.SHADOW,
        ExtractionPhase.CANARY,
        ExtractionPhase.DECOMMISSIONED,
    },
    ExtractionPhase.DECOMMISSIONED: set(),
}


@dataclass(frozen=True)
class Comparison:
    same: bool
    legacy: Any
    candidate: Any
    explanation: str = ""


class StranglerRouter:
    def __init__(self, legacy: Callable[..., Any], candidate: Callable[..., Any]) -> None:
        self.legacy = legacy
        self.candidate = candidate
        self.phase = ExtractionPhase.LEGACY
        self.canary_fraction = 0.0
        self.rollback_available = True
        self.comparisons: list[Comparison] = []

    def transition(
        self,
        phase: ExtractionPhase,
        *,
        canary_fraction: float = 0.0,
    ) -> None:
        if phase not in _ALLOWED[self.phase]:
            raise ValidationError(
                f"invalid extraction transition: {self.phase.value}->{phase.value}"
            )
        if phase in {ExtractionPhase.CANARY, ExtractionPhase.CUTOVER}:
            if not self.shadow_clean():
                raise ValidationError("promotion requires a clean shadow comparison")
        if phase == ExtractionPhase.CANARY and not 0 < canary_fraction < 1:
            raise ValidationError("canary fraction must be between zero and one")
        if phase in {
            ExtractionPhase.LEGACY,
            ExtractionPhase.SHADOW,
            ExtractionPhase.CANARY,
        } and self.phase in {ExtractionPhase.CANARY, ExtractionPhase.CUTOVER}:
            if not self.rollback_available:
                raise ValidationError("rollback target unavailable")
        if phase == ExtractionPhase.CUTOVER and not self.rollback_available:
            raise ValidationError("cutover requires rollback target")
        self.phase = phase
        self.canary_fraction = canary_fraction

    def call(self, key: str, *args: Any, **kwargs: Any) -> Any:
        if self.phase == ExtractionPhase.LEGACY:
            return self.legacy(*args, **kwargs)
        if self.phase == ExtractionPhase.SHADOW:
            old = self.legacy(*args, **kwargs)
            new = self.candidate(*args, **kwargs)
            self.comparisons.append(Comparison(old == new, old, new))
            return old
        if self.phase == ExtractionPhase.CANARY:
            bucket = sum(key.encode("utf-8")) % 10_000
            if bucket < int(self.canary_fraction * 10_000):
                return self.candidate(*args, **kwargs)
            return self.legacy(*args, **kwargs)
        return self.candidate(*args, **kwargs)

    def shadow_clean(self) -> bool:
        return bool(self.comparisons) and all(item.same for item in self.comparisons)
