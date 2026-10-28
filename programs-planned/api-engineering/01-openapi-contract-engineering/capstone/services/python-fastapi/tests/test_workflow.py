from __future__ import annotations

import time

from fastapi.testclient import TestClient

from conftest import create_ready_dataset


def test_complete_analysis_workflow_and_idempotent_replay(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    project_id, dataset_id = create_ready_dataset(client, write_headers)
    body = {
        "projectId": project_id,
        "datasetId": dataset_id,
        "parameters": {"algorithm": "quality-summary", "priority": "normal"},
    }
    headers = {**write_headers, "Idempotency-Key": "analysis-workflow-0001"}

    accepted = client.post("/analysis-runs", headers=headers, json=body)
    assert accepted.status_code == 202
    assert accepted.headers["retry-after"] == "1"
    assert accepted.headers["idempotent-replay"] == "false"
    run_id = accepted.json()["id"]

    replay = client.post("/analysis-runs", headers=headers, json=body)
    assert replay.status_code == 202
    assert replay.json()["id"] == run_id
    assert replay.headers["idempotent-replay"] == "true"

    changed = client.post(
        "/analysis-runs",
        headers=headers,
        json={
            **body,
            "parameters": {"algorithm": "checksum", "priority": "normal"},
        },
    )
    assert changed.status_code == 409
    assert changed.json()["type"].endswith("/idempotency-conflict")

    first_read = client.get(f"/analysis-runs/{run_id}", headers=write_headers)
    second_read = client.get(f"/analysis-runs/{run_id}", headers=write_headers)
    assert first_read.json()["status"] == second_read.json()["status"]

    deadline = time.monotonic() + 2.0
    completed = second_read
    while time.monotonic() < deadline:
        completed = client.get(f"/analysis-runs/{run_id}", headers=write_headers)
        if completed.json()["status"] == "completed":
            break
        time.sleep(0.01)
    assert completed.json()["status"] == "completed"

    artifacts = client.get(
        f"/analysis-runs/{run_id}/artifacts", headers=write_headers
    )
    assert artifacts.status_code == 200
    assert len(artifacts.json()["items"]) == 1
    artifact_id = artifacts.json()["items"][0]["id"]

    artifact = client.get(f"/artifacts/{artifact_id}", headers=write_headers)
    assert artifact.status_code == 200
    assert artifact.json()["runId"] == run_id


def test_artifacts_before_completion_are_a_conflict(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    project_id, dataset_id = create_ready_dataset(client, write_headers)
    accepted = client.post(
        "/analysis-runs",
        headers={**write_headers, "Idempotency-Key": "analysis-workflow-0002"},
        json={
            "projectId": project_id,
            "datasetId": dataset_id,
            "parameters": {"algorithm": "checksum"},
        },
    )
    run_id = accepted.json()["id"]
    response = client.get(f"/analysis-runs/{run_id}/artifacts", headers=write_headers)
    assert response.status_code == 409


def test_cancellation_is_a_state_transition(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    project_id, dataset_id = create_ready_dataset(client, write_headers)
    accepted = client.post(
        "/analysis-runs",
        headers={**write_headers, "Idempotency-Key": "analysis-workflow-0003"},
        json={
            "projectId": project_id,
            "datasetId": dataset_id,
            "parameters": {"algorithm": "line-count"},
        },
    )
    run_id = accepted.json()["id"]
    canceled = client.post(
        f"/analysis-runs/{run_id}/cancellation", headers=write_headers
    )
    assert canceled.status_code == 200
    assert canceled.json()["status"] == "canceled"

    second = client.post(
        f"/analysis-runs/{run_id}/cancellation", headers=write_headers
    )
    assert second.status_code == 409


def test_progress_stream_has_machine_readable_items(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    project_id, dataset_id = create_ready_dataset(client, write_headers)
    accepted = client.post(
        "/analysis-runs",
        headers={**write_headers, "Idempotency-Key": "analysis-workflow-0004"},
        json={
            "projectId": project_id,
            "datasetId": dataset_id,
            "parameters": {"algorithm": "quality-summary"},
        },
    )
    run_id = accepted.json()["id"]

    response = client.get(
        f"/analysis-runs/{run_id}/events",
        headers={**write_headers, "Accept": "application/x-ndjson"},
    )
    assert response.status_code == 200
    lines = [line for line in response.text.splitlines() if line]
    assert len(lines) >= 2
    assert '"status":"completed"' in lines[-1]
