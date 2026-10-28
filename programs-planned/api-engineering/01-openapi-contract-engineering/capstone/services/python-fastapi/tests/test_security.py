from __future__ import annotations

from fastapi.testclient import TestClient

from conftest import create_ready_dataset


def test_read_token_cannot_write(client: TestClient, read_headers: dict[str, str]) -> None:
    response = client.post("/projects", headers=read_headers, json={"name": "Denied"})
    assert response.status_code == 403
    assert "projects:write" in response.json()["detail"]


def test_scope_does_not_replace_ownership(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    project_id, _ = create_ready_dataset(client, write_headers)
    other = {"Authorization": "Bearer other-owner"}
    response = client.get(f"/projects/{project_id}", headers=other)
    assert response.status_code == 404


def test_api_key_exercises_alternative_security_requirement(client: TestClient) -> None:
    response = client.post(
        "/projects",
        headers={"X-API-Key": "demo-api-key"},
        json={"name": "API key project"},
    )
    assert response.status_code == 201


def test_internal_diagnostics_requires_admin(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    denied = client.get("/internal/diagnostics", headers=write_headers)
    assert denied.status_code == 403

    allowed = client.get(
        "/internal/diagnostics", headers={"Authorization": "Bearer admin"}
    )
    assert allowed.status_code == 200
    assert allowed.json()["counts"]["projects"] == 0


def test_webhook_destination_is_constrained(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    rejected = client.post(
        "/webhook-subscriptions",
        headers=write_headers,
        json={
            "targetUrl": "https://attacker.example/collect",
            "eventTypes": ["analysis.completed"],
            "secret": "training-secret-0001",
        },
    )
    assert rejected.status_code == 422

    accepted = client.post(
        "/webhook-subscriptions",
        headers=write_headers,
        json={
            "targetUrl": "https://hooks.example.test/team-a",
            "eventTypes": ["analysis.completed"],
            "secret": "training-secret-0001",
        },
    )
    assert accepted.status_code == 201
    assert "secret" not in accepted.json()
    assert accepted.json()["secretHint"] == "****0001"
