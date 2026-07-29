"""Pure structural compatibility decisions for versioned value contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

Compatibility: TypeAlias = Literal[
    "backward-compatible",
    "requires-migration",
    "incompatible",
]


@dataclass(frozen=True, slots=True)
class ContractShape:
    name: str
    fields: frozenset[str]
    required_fields: frozenset[str]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("contract name must not be empty")
        if not self.required_fields <= self.fields:
            raise ValueError("required fields must belong to the contract")


@dataclass(frozen=True, slots=True)
class MigrationAssessment:
    compatibility: Compatibility
    added_fields: tuple[str, ...]
    removed_fields: tuple[str, ...]
    newly_required_fields: tuple[str, ...]


def assess_migration(
    previous: ContractShape,
    current: ContractShape,
) -> MigrationAssessment:
    """Classify field-shape evolution before running a semantic upcaster proof."""

    if previous.name != current.name:
        return MigrationAssessment("incompatible", (), (), ())

    added = current.fields - previous.fields
    removed = previous.fields - current.fields
    newly_required = current.required_fields - previous.fields
    if removed:
        compatibility: Compatibility = "incompatible"
    elif newly_required:
        compatibility = "requires-migration"
    else:
        compatibility = "backward-compatible"
    return MigrationAssessment(
        compatibility=compatibility,
        added_fields=tuple(sorted(added)),
        removed_fields=tuple(sorted(removed)),
        newly_required_fields=tuple(sorted(newly_required)),
    )
