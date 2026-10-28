from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_is_anonymous_and_correlated(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"].startswith("req_")


def test_missing_authentication_uses_problem_details(client: TestClient) -> None:
    response = client.get("/projects")
    assert response.status_code == 401
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert body["status"] == 401
    assert body["type"].endswith("/unauthorized")
    assert body["requestId"] == response.headers["x-request-id"]


def test_create_get_and_conditionally_update_project(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    created = client.post(
        "/projects",
        headers=write_headers,
        json={"name": "Summer cohort", "description": "Initial"},
    )
    assert created.status_code == 201
    project_id = created.json()["id"]
    first_etag = created.headers["etag"]
    assert created.headers["location"] == f"/projects/{project_id}"

    fetched = client.get(f"/projects/{project_id}", headers=write_headers)
    assert fetched.status_code == 200
    assert fetched.headers["etag"] == first_etag

    stale = client.patch(
        f"/projects/{project_id}",
        headers={**write_headers, "If-Match": '"prj_0001:99"'},
        json={"description": "wrong"},
    )
    assert stale.status_code == 412

    missing_precondition = client.patch(
        f"/projects/{project_id}",
        headers=write_headers,
        json={"description": "wrong"},
    )
    assert missing_precondition.status_code == 428

    updated = client.patch(
        f"/projects/{project_id}",
        headers={**write_headers, "If-Match": first_etag},
        json={"description": None},
    )
    assert updated.status_code == 200
    assert updated.json()["version"] == 2
    assert updated.json()["description"] is None
    assert updated.headers["etag"] != first_etag


def test_validation_response_does_not_leak_framework_shape(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    response = client.post("/projects", headers=write_headers, json={"name": ""})
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert set(body) == {
        "type",
        "title",
        "status",
        "detail",
        "instance",
        "requestId",
        "errors",
    }
    assert body["errors"][0]["location"][:1] == ["body"]


def test_cursor_pagination_is_deterministic(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    for index in range(3):
        response = client.post(
            "/projects", headers=write_headers, json={"name": f"Project {index}"}
        )
        assert response.status_code == 201

    first = client.get("/projects?limit=2", headers=write_headers)
    assert first.status_code == 200
    assert [item["id"] for item in first.json()["items"]] == ["prj_0001", "prj_0002"]
    assert first.json()["nextCursor"] == "2"

    second = client.get("/projects?limit=2&cursor=2", headers=write_headers)
    assert second.status_code == 200
    assert [item["id"] for item in second.json()["items"]] == ["prj_0003"]
    assert second.json()["nextCursor"] is None


def test_optional_request_fields_are_not_implicitly_nullable(
    client: TestClient, write_headers: dict[str, str]
) -> None:
    created = client.post(
        "/projects", headers=write_headers, json={"name": "valid", "description": None}
    )
    assert created.status_code == 422

    project = client.post(
        "/projects", headers=write_headers, json={"name": "valid"}
    ).json()
    response = client.patch(
        f"/projects/{project['id']}",
        headers={**write_headers, "If-Match": '"prj_0001:1"'},
        json={"name": None},
    )
    assert response.status_code == 422
