from __future__ import annotations

import json

from .boundaries import boundary_evidence
from .cache import cache_evidence
from .composition import composition_evidence
from .external import external_storage_evidence
from .hints import hint_evidence
from .relational import relational_model_evidence


def build_evidence() -> dict[str, object]:
    return {
        "cache_invalidation": cache_evidence(),
        "external_storage": external_storage_evidence(),
        "composition": composition_evidence(),
        "hint_policy": hint_evidence(),
        "record_model": relational_model_evidence(),
        "architecture_boundary": boundary_evidence(),
    }


def render_evidence() -> str:
    return json.dumps(build_evidence(), indent=2, sort_keys=True)
