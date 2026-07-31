from __future__ import annotations

import json

from .dynamic import dynamic_execution_evidence
from .interfaces import interface_evidence
from .patching import patching_evidence
from .selection import selection_evidence
from .tooling import tooling_evidence


def build_evidence() -> dict[str, object]:
    """Build the complete deterministic governance packet for Module 10."""

    return {
        "dynamic_execution": dynamic_execution_evidence(),
        "interface_contracts": interface_evidence(),
        "reversible_patching": patching_evidence(),
        "tooling_boundaries": tooling_evidence(),
        "mechanism_selection": selection_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON for learner inspection and review."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
