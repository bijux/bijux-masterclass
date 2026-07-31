from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DesignPressure(str, Enum):
    NORMALIZE_ONE_ATTRIBUTE = "normalize-one-attribute"
    INVALIDATE_LOCAL_DERIVATION = "invalidate-local-derivation"
    LOAD_ONE_BACKEND_FIELD = "load-one-backend-field"
    COORDINATE_RECORD_WRITES = "coordinate-record-writes"
    GENERATE_CLASS_WIDE_MODEL = "generate-class-wide-model"


@dataclass(frozen=True, slots=True)
class OwnerDecision:
    pressure: DesignPressure
    owner: str
    reason: str
    refused_weaker_owner: str
    refused_stronger_owner: str
    escalation_signal: str

    def manifest(self) -> dict[str, str]:
        return {
            "pressure": self.pressure.value,
            "owner": self.owner,
            "reason": self.reason,
            "refused_weaker_owner": self.refused_weaker_owner,
            "refused_stronger_owner": self.refused_stronger_owner,
            "escalation_signal": self.escalation_signal,
        }


DECISIONS = {
    DesignPressure.NORMALIZE_ONE_ATTRIBUTE: OwnerDecision(
        pressure=DesignPressure.NORMALIZE_ONE_ATTRIBUTE,
        owner="descriptor",
        reason="one attribute owns one assignment boundary",
        refused_weaker_owner="caller convention",
        refused_stronger_owner="model framework",
        escalation_signal="validation begins coordinating multiple fields",
    ),
    DesignPressure.INVALIDATE_LOCAL_DERIVATION: OwnerDecision(
        pressure=DesignPressure.INVALIDATE_LOCAL_DERIVATION,
        owner="coordinated descriptor system",
        reason="one source field can name one local cached dependency",
        refused_weaker_owner="manual caller refresh",
        refused_stronger_owner="shared cache service",
        escalation_signal="freshness must coordinate across instances or processes",
    ),
    DesignPressure.LOAD_ONE_BACKEND_FIELD: OwnerDecision(
        pressure=DesignPressure.LOAD_ONE_BACKEND_FIELD,
        owner="backend-backed descriptor plus explicit store",
        reason="one stable field key maps to one authoritative backend slot",
        refused_weaker_owner="instance dictionary",
        refused_stronger_owner="session and unit of work",
        escalation_signal="transactions or object identity span records",
    ),
    DesignPressure.COORDINATE_RECORD_WRITES: OwnerDecision(
        pressure=DesignPressure.COORDINATE_RECORD_WRITES,
        owner="session or unit of work",
        reason="success and rollback span more than one attribute or record",
        refused_weaker_owner="smart field descriptor",
        refused_stronger_owner="class-creation metaprogramming",
        escalation_signal="class-wide declarations must be generated or registered",
    ),
    DesignPressure.GENERATE_CLASS_WIDE_MODEL: OwnerDecision(
        pressure=DesignPressure.GENERATE_CLASS_WIDE_MODEL,
        owner="explicit class-creation owner",
        reason="the contract must exist when the whole class is created",
        refused_weaker_owner="individual field descriptor",
        refused_stronger_owner="process-wide runtime hooks",
        escalation_signal="behavior must coordinate outside the class hierarchy",
    ),
}


def decide_owner(pressure: DesignPressure) -> OwnerDecision:
    return DECISIONS[pressure]


def boundary_evidence() -> dict[str, object]:
    return {
        "decisions": [
            decide_owner(pressure).manifest()
            for pressure in DesignPressure
        ],
        "selection_rule": "choose the smallest owner that can see the whole invariant",
        "power_is_not_the_goal": True,
    }
