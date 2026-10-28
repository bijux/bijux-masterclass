from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from analysis_client import AnalysisClient, ApiError


def test_complete_workflow_follows_contract_links(tmp_path: Path) -> None:
    observed: list[tuple[str, str]] = []
    poll = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal poll
        observed.append((request.method, request.url.path))
        if request.method == "POST" and request.url.path == "/projects":
            return httpx.Response(
                201,
                json={
                    "id": "prj_0001",
                    "ownerId": "learner",
                    "name": "Demo",
                    "description": None,
                    "version": 1,
                    "createdAt": "2026-08-05T10:00:00Z",
                    "updatedAt": "2026-08-05T10:00:00Z",
                },
                headers={"ETag": '"prj_0001:1"', "Location": "/projects/prj_0001"},
            )
        if request.method == "POST" and request.url.path == "/projects/prj_0001/datasets":
            return httpx.Response(
                201,
                json={
                    "id": "dts_0001",
                    "projectId": "prj_0001",
                    "ownerId": "learner",
                    "name": "dataset",
                    "source": {
                        "kind": "local-file",
                        "fileName": "dataset.csv",
                        "mediaType": "text/csv",
                    },
                    "status": "awaiting-upload",
                    "contentLength": None,
                    "checksumSha256": None,
                    "createdAt": "2026-08-05T10:00:00Z",
                    "updatedAt": "2026-08-05T10:00:00Z",
                },
            )
        if request.method == "POST" and request.url.path == "/datasets/dts_0001/content":
            return httpx.Response(
                201,
                json={
                    "datasetId": "dts_0001",
                    "contentLength": 17,
                    "checksumSha256": "a" * 64,
                    "uploadedAt": "2026-08-05T10:01:00Z",
                },
            )
        if request.method == "POST" and request.url.path == "/analysis-runs":
            assert request.headers["idempotency-key"] == "python-client-test-0001"
            return httpx.Response(
                202,
                json={
                    "id": "run_0001",
                    "projectId": "prj_0001",
                    "datasetId": "dts_0001",
                    "ownerId": "learner",
                    "status": "queued",
                    "parameters": {
                        "algorithm": "quality-summary",
                        "priority": "normal",
                        "labels": {},
                    },
                    "progress": 0,
                    "createdAt": "2026-08-05T10:02:00Z",
                    "updatedAt": "2026-08-05T10:02:00Z",
                    "completedAt": None,
                    "artifactIds": [],
                },
                headers={
                    "Location": "/analysis-runs/run_0001",
                    "Idempotent-Replay": "false",
                },
            )
        if request.method == "GET" and request.url.path == "/analysis-runs/run_0001":
            poll += 1
            status = "running" if poll == 1 else "completed"
            return httpx.Response(
                200,
                json={
                    "id": "run_0001",
                    "projectId": "prj_0001",
                    "datasetId": "dts_0001",
                    "ownerId": "learner",
                    "status": status,
                    "parameters": {
                        "algorithm": "quality-summary",
                        "priority": "normal",
                        "labels": {},
                    },
                    "progress": 50 if status == "running" else 100,
                    "createdAt": "2026-08-05T10:02:00Z",
                    "updatedAt": "2026-08-05T10:03:00Z",
                    "completedAt": None if status == "running" else "2026-08-05T10:03:00Z",
                    "artifactIds": [] if status == "running" else ["art_0001"],
                },
            )
        if request.method == "GET" and request.url.path == "/analysis-runs/run_0001/artifacts":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": "art_0001",
                            "runId": "run_0001",
                            "ownerId": "learner",
                            "name": "quality-summary.json",
                            "mediaType": "application/json",
                            "size": 80,
                            "checksumSha256": "b" * 64,
                            "createdAt": "2026-08-05T10:03:00Z",
                        }
                    ]
                },
            )
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    source = tmp_path / "dataset.csv"
    source.write_text("sample,value\nA,1\n", encoding="utf-8")
    transport = httpx.MockTransport(handler)
    http = httpx.Client(base_url="https://api.example.test", transport=transport)

    client = AnalysisClient(
        "https://api.example.test",
        bearer_token="learner-write",
        http_client=http,
    )
    result = client.complete_workflow(
        project_name="Demo",
        dataset_path=source,
        idempotency_key="python-client-test-0001",
    )

    assert result["run"]["status"] == "completed"
    assert result["artifacts"][0]["id"] == "art_0001"
    assert observed[-1] == ("GET", "/analysis-runs/run_0001/artifacts")
    assert http.headers["authorization"] == "Bearer learner-write"


def test_problem_details_becomes_typed_exception() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409,
            json={
                "type": "https://api.example.test/problems/conflict",
                "title": "Request conflict",
                "status": 409,
                "detail": "The run is already complete.",
                "instance": request.url.path,
                "requestId": "req_012345abcdef",
            },
            headers={"Content-Type": "application/problem+json"},
        )

    http = httpx.Client(
        base_url="https://api.example.test",
        transport=httpx.MockTransport(handler),
    )
    client = AnalysisClient(
        "https://api.example.test",
        bearer_token="learner-write",
        http_client=http,
    )
    with pytest.raises(ApiError) as captured:
        client.list_artifacts("run_0001")
    assert captured.value.status == 409
    assert captured.value.request_id == "req_012345abcdef"


def test_exactly_one_authentication_mode_is_required() -> None:
    with pytest.raises(ValueError):
        AnalysisClient("https://api.example.test", bearer_token=None, api_key=None)
    with pytest.raises(ValueError):
        AnalysisClient(
            "https://api.example.test",
            bearer_token="learner-write",
            api_key="demo-api-key",
        )
