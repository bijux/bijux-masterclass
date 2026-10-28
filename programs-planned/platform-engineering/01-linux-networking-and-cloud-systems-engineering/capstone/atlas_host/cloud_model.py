from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FailureDomainPlan:
    instances: int
    zones: int
    durable_copies: int
    load_balanced: bool

    def supported_claims(self) -> set[str]:
        claims = {"single-instance-operation"}
        if self.instances >= 2 and self.load_balanced:
            claims.add("instance-replacement-without-planned-endpoint-change")
        if self.zones >= 2 and self.instances >= 2 and self.durable_copies >= 2:
            claims.add("single-zone-failure-tolerance")
        return claims


def require_zone_tolerance(plan: FailureDomainPlan) -> None:
    if "single-zone-failure-tolerance" not in plan.supported_claims():
        raise ValueError("plan does not support a single-zone failure claim")
