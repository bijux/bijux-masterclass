"""Dependency-light end-to-end tour of the Course 9 semantic gateway."""

from __future__ import annotations

import json
from pathlib import Path

from .cursor import CursorCodec
from .gateway import AnalysisGraphGateway
from .identity import encode_global_id
from .model import Principal, RequestContext
from .persisted import PersistedOperationRegistry
from .services import (
    AnalysisControlClient,
    ArtifactServiceClient,
    NotificationServiceClient,
)


COURSE_PERMISSIONS = frozenset(
    {
        "PROJECT_READ",
        "PROJECT_WRITE",
        "RUN_READ",
        "RUN_WRITE",
        "ARTIFACT_READ",
        "DELIVERY_READ",
    }
)


def build_gateway(root: Path) -> AnalysisGraphGateway:
    """Build the deterministic gateway used by tests and the capstone tour."""

    registry = PersistedOperationRegistry.from_directory(
        root / "capstone/contracts/operations"
    )
    return AnalysisGraphGateway(
        registry=registry,
        analysis=AnalysisControlClient(),
        artifacts=ArtifactServiceClient(),
        notifications=NotificationServiceClient(),
        cursor_codec=CursorCodec(
            b"course-cursor-key-0123456789abcdef"
        ),
    )


def run_tour(root: Path) -> dict[str, object]:
    """Exercise composition, partial data, and idempotent mutation replay."""

    gateway = build_gateway(root)
    context = RequestContext(
        principal=Principal(
            subject="learner",
            tenant_id="tenant-a",
            permissions=COURSE_PERMISSIONS,
        ),
        request_id="tour-1",
    )
    project_id = encode_global_id("Project", "proj-1")

    overview_operation = gateway.registry.by_name("GetProjectOverview")
    overview = gateway.execute(
        overview_operation.sha256,
        {"projectId": project_id, "first": 2},
        context,
    )

    gateway.artifacts.available = False
    run_operation = gateway.registry.by_name("GetRun")
    partial = gateway.execute(
        run_operation.sha256,
        {"runId": encode_global_id("AnalysisRun", "run-1")},
        context,
    )

    mutation_operation = gateway.registry.by_name("StartAnalysis")
    variables = {
        "input": {
            "clientMutationId": "c-1",
            "idempotencyKey": "idem-tour",
            "projectId": project_id,
            "datasetId": "data-3",
            "algorithm": "qc",
        }
    }
    first = gateway.execute(
        mutation_operation.sha256,
        variables,
        context,
    )
    second = gateway.execute(
        mutation_operation.sha256,
        variables,
        context,
    )

    return {
        "overview_errors": len(overview.errors),
        "overview_runs": len(
            overview.data["project"]["analysisRuns"]["edges"]
        ),
        "artifact_batch_calls": overview.extensions["batchCalls"][
            "artifact"
        ],
        "partial_artifacts": partial.data["analysisRun"]["artifacts"],
        "partial_error_code": partial.errors[0].code,
        "mutation_replayed_first": first.data["startAnalysis"][
            "replayed"
        ],
        "mutation_replayed_second": second.data["startAnalysis"][
            "replayed"
        ],
    }


if __name__ == "__main__":
    course_root = Path(__file__).resolve().parents[5]
    print(
        json.dumps(
            run_tour(course_root),
            indent=2,
            sort_keys=True,
        )
    )
