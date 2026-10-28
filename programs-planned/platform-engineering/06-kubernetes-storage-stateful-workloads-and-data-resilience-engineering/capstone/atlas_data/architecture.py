from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataServiceDecision:
    recommendation: str
    reasons: tuple[str, ...]

    @classmethod
    def evaluate(
        cls,
        workload: str,
        team_operational_expertise: str,
        requires_custom_storage_engine: bool,
        requires_cross_region_recovery: bool,
    ) -> "DataServiceDecision":
        reasons: list[str] = []
        if requires_custom_storage_engine:
            reasons.append("custom engine requires direct operational control")
            return cls("operator-or-direct", tuple(reasons))
        if team_operational_expertise == "limited":
            reasons.append("limited engine operations expertise")
        if requires_cross_region_recovery:
            reasons.append("cross-region recovery is a primary requirement")
        if reasons:
            return cls("managed-service", tuple(reasons))
        return cls("operator", ("team can own engine-specific control plane",))
