from __future__ import annotations

import json

from .boundaries import boundary_evidence
from .lifecycle import lifecycle_evidence
from .manual import manual_creation_evidence
from .namespace import namespace_evidence
from .registry import registry_evidence
from .resolution import resolution_evidence


def build_evidence() -> dict[str, object]:
    """Build the complete deterministic evidence packet for Module 09."""

    return {
        "manual_construction": manual_creation_evidence(),
        "resolution": resolution_evidence(),
        "lifecycle": lifecycle_evidence(),
        "declaration_namespace": namespace_evidence(),
        "registry": registry_evidence(),
        "boundaries": boundary_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON for command-line inspection and review."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
