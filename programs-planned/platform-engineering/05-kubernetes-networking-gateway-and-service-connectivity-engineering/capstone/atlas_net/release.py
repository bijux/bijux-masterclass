from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Gate:
    name: str
    state: str
    blocker: bool = True


def classify(gates: list[Gate]) -> str:
    """Classify a release without averaging away blocker failures."""

    if any(gate.blocker and gate.state == "fail" for gate in gates):
        return "rejected"
    if any(gate.blocker and gate.state == "not-executed" for gate in gates):
        return "not-executed"
    if any(gate.state == "review" for gate in gates):
        return "review-required"
    return "accepted"
