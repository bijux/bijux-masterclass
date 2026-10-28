from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from analysis_api.app import app
from analysis_api.store import store


@pytest.fixture(autouse=True)
def reset_store() -> None:
    store.reset()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as active_client:
        yield active_client


@pytest.fixture
def write_headers() -> dict[str, str]:
    return {"Authorization": "Bearer learner-write"}


@pytest.fixture
def read_headers() -> dict[str, str]:
    return {"Authorization": "Bearer learner-read"}


def create_ready_dataset(client: TestClient, headers: dict[str, str]) -> tuple[str, str]:
    project_response = client.post("/projects", headers=headers, json={"name": "Test project"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    dataset_response = client.post(
        f"/projects/{project_id}/datasets",
        headers=headers,
        json={
            "name": "reads",
            "source": {
                "kind": "local-file",
                "fileName": "reads.csv",
                "mediaType": "text/csv",
            },
        },
    )
    assert dataset_response.status_code == 201
    dataset_id = dataset_response.json()["id"]

    upload_response = client.post(
        f"/datasets/{dataset_id}/content",
        headers=headers,
        files={"file": ("reads.csv", b"sample,value\nA,1\n", "text/csv")},
    )
    assert upload_response.status_code == 201
    return project_id, dataset_id
