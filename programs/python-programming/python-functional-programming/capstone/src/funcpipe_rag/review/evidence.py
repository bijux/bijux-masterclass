"""Pure claim-to-evidence decisions for sustainment review."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceClaim:
    name: str
    statement: str
    required_paths: tuple[str, ...]
    command: str

    def __post_init__(self) -> None:
        if not self.name or not self.statement or not self.command:
            raise ValueError("evidence claim fields must not be empty")
        if not self.required_paths:
            raise ValueError("an evidence claim must require at least one path")


@dataclass(frozen=True, slots=True)
class EvidenceAssessment:
    claim: EvidenceClaim
    complete: bool
    missing_paths: tuple[str, ...]


def assess_evidence(
    claim: EvidenceClaim,
    available_paths: frozenset[str],
) -> EvidenceAssessment:
    """Decide completeness from a filesystem observation supplied by a shell."""

    missing = tuple(
        path for path in claim.required_paths if path not in available_paths
    )
    return EvidenceAssessment(
        claim=claim,
        complete=not missing,
        missing_paths=missing,
    )
