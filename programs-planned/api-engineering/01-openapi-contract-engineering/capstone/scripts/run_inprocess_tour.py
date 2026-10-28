#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

CAPSTONE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAPSTONE / "services/python-fastapi/src"))

from analysis_api.app import app  # noqa: E402


def expect(response, status: int, label: str):
    if response.status_code != status:
        raise RuntimeError(f"{label}: expected {status}, got {response.status_code}: {response.text}")
    print(f"PASS {label:<34} {response.status_code}")
    return response


def main() -> int:
    writer = {"Authorization": "Bearer learner-write"}
    reader = {"Authorization": "Bearer learner-read"}
    with TestClient(app) as client:
        expect(client.get("/health"), 200, "anonymous health")
        project_response = expect(
            client.post("/projects", headers=writer, json={"name": "Evidence tour"}),
            201,
            "create project",
        )
        project = project_response.json()
        dataset = expect(
            client.post(
                f"/projects/{project['id']}/datasets",
                headers=writer,
                json={
                    "name": "tour-data",
                    "source": {
                        "kind": "local-file",
                        "fileName": "tour.csv",
                        "mediaType": "text/csv",
                    },
                },
            ),
            201,
            "register dataset",
        ).json()
        expect(
            client.post(
                f"/datasets/{dataset['id']}/content",
                headers=writer,
                files={"file": ("tour.csv", b"sample,value\nA,1\n", "text/csv")},
            ),
            201,
            "upload multipart content",
        )
        run_response = expect(
            client.post(
                "/analysis-runs",
                headers={**writer, "Idempotency-Key": "evidence-tour-0001"},
                json={
                    "projectId": project["id"],
                    "datasetId": dataset["id"],
                    "parameters": {"algorithm": "quality-summary"},
                },
            ),
            202,
            "accept asynchronous run",
        )
        run = run_response.json()
        observed = [run["status"]]
        deadline = time.monotonic() + 2.0
        completed = None
        while time.monotonic() < deadline:
            current_response = client.get(
                f"/analysis-runs/{run['id']}", headers=reader
            )
            if current_response.status_code != 200:
                raise RuntimeError(
                    "poll run status: expected 200, got "
                    f"{current_response.status_code}: {current_response.text}"
                )
            current = current_response.json()
            observed.append(current["status"])
            if current["status"] == "completed":
                completed = current
                break
            time.sleep(0.01)
        if completed is None or "running" not in observed:
            raise RuntimeError(f"run did not traverse queued → running → completed: {observed}")
        print(f"PASS observe asynchronous progression   {' → '.join(observed)}")
        artifacts = expect(
            client.get(f"/analysis-runs/{run['id']}/artifacts", headers=reader),
            200,
            "retrieve artifacts",
        ).json()["items"]
    summary = {
        "projectId": project["id"],
        "datasetId": dataset["id"],
        "runId": completed["id"],
        "status": completed["status"],
        "artifactIds": [item["id"] for item in artifacts],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
