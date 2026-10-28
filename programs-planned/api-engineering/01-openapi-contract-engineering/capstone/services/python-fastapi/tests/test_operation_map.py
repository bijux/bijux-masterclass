from __future__ import annotations

from analysis_api.app import app


EXPECTED = {
    "getHealth",
    "listProjects",
    "createProject",
    "getProject",
    "updateProject",
    "listProjectDatasets",
    "createDataset",
    "getDataset",
    "deleteDataset",
    "uploadDatasetContent",
    "listAnalysisRuns",
    "createAnalysisRun",
    "getAnalysisRun",
    "cancelAnalysisRun",
    "listRunArtifacts",
    "streamAnalysisRunEvents",
    "getArtifact",
    "createWebhookSubscription",
    "getInternalDiagnostics",
}


def test_operation_id_inventory_is_exact() -> None:
    observed = {
        route.operation_id
        for route in app.routes
        if getattr(route, "operation_id", None) is not None
    }
    assert observed == EXPECTED
