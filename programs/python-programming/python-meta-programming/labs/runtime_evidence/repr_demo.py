from __future__ import annotations

import json

from .safe_repr import SignatureGuidedRepr, stored_state


class IncidentRecord(SignatureGuidedRepr):
    def __init__(self, incident_id: str, severity: str = "warning") -> None:
        self.severity = severity
        self.incident_id = incident_id
        self.owner = "platform"


class SlottedIncident(SignatureGuidedRepr):
    __slots__ = ("incident_id", "severity", "property_reads")

    def __init__(self, incident_id: str, severity: str = "warning") -> None:
        self.severity = severity
        self.incident_id = incident_id
        self.property_reads = 0

    @property
    def risk_score(self) -> int:
        self.property_reads += 1
        return 7


def build_demo() -> dict[str, object]:
    regular = IncidentRecord("INC-42")
    slotted = SlottedIncident("INC-43", "critical")
    slotted_rendered = repr(slotted)
    return {
        "regular": repr(regular),
        "slotted": slotted_rendered,
        "slotted_state": stored_state(slotted),
        "property_reads_after_repr": slotted.property_reads,
        "evidence": {
            "ordering": "constructor-signature",
            "values": "instance-storage",
            "dynamic_member_lookup": False,
            "frame_inspection": False,
        },
    }


def main() -> int:
    print(json.dumps(build_demo(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
