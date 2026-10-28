from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MigrationPhase:
    name: str
    reversible: bool
    requires_fence: bool
    required_evidence: tuple[str, ...]


class MigrationPlan:
    def __init__(self, phases: list[MigrationPhase]):
        self.phases = phases
        self.completed: list[str] = []

    def complete(self, name: str, evidence: set[str]) -> None:
        phase = next((item for item in self.phases if item.name == name), None)
        if phase is None:
            raise KeyError(name)
        if not set(phase.required_evidence).issubset(evidence):
            raise ValueError("migration evidence is incomplete")
        expected = self.phases[len(self.completed)].name
        if name != expected:
            raise ValueError(f"phase {name} cannot precede {expected}")
        self.completed.append(name)

    def rollback_allowed(self) -> bool:
        completed = {item.name for item in self.phases if item.name in self.completed}
        return all(item.reversible for item in self.phases if item.name in completed)
