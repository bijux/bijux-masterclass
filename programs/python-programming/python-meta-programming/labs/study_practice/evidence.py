from __future__ import annotations

import json

from .catalog import STUDY_ROUTES
from .reentry import build_reentry_plan


def build_study_evidence(*, last_trusted_module: int = 0) -> dict[str, object]:
    """Publish the course-first study contract as deterministic evidence."""

    return {
        "primary_product": "course website and runnable course material",
        "integration_surface": "incident-plugin capstone",
        "study_cycle": [
            "state the module question and prerequisite contract",
            "read the core and predict the runtime behavior",
            "run the focused course evidence",
            "complete the exercise before opening its answer",
            "compare reasoning, wrong turns, proof, and non-claims",
            "transfer the settled concept into one capstone route",
            "run the broad gate only at a release or mastery boundary",
        ],
        "proof_order": ["course command", "focused tests", "capstone transfer"],
        "routes": [route.evidence() for route in STUDY_ROUTES],
        "reentry": build_reentry_plan(last_trusted_module).evidence(),
    }


def render_study_evidence(*, last_trusted_module: int = 0) -> str:
    """Render stable JSON for learners and documentation checks."""

    return json.dumps(
        build_study_evidence(last_trusted_module=last_trusted_module),
        indent=2,
        sort_keys=True,
    )
