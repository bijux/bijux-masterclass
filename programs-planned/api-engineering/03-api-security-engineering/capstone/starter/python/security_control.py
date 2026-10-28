from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecurityDecision:
    allowed: bool
    reason: str


def evaluate_untrusted_input(value: object) -> SecurityDecision:
    """Replace with the current module's authoritative control."""
    raise NotImplementedError("implement from the module requirement and tests")
