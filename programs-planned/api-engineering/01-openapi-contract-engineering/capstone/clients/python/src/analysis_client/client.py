from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


@dataclass
class ApiError(RuntimeError):
    status: int
    title: str
    detail: str
    problem_type: str
    request_id: str | None = None

    def __str__(self) -> str:
        suffix = f" [{self.request_id}]" if self.request_id else ""
        return f"{self.status} {self.title}: {self.detail}{suffix}"


class AnalysisClient:
    def __init__(
        self,
        base_url: str,
        *,
        bearer_token: str | None = None,
        api_key: str | None = None,
        timeout: float = 10.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        if bool(bearer_token) == bool(api_key):
            raise ValueError("configure exactly one of bearer_token or api_key")
        headers = (
            {"Authorization": f"Bearer {bearer_token}"}
            if bearer_token
            else {"X-API-Key": str(api_key)}
        )
        self._owns_client = http_client is None
        self.http = http_client or httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=headers,
            timeout=timeout,
        )
        if http_client is not None:
            self.http.headers.update(headers)

    def close(self) -> None:
        if self._owns_client:
            self.http.close()

    def __enter__(self) -> "AnalysisClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @staticmethod
    def _raise_for_problem(response: httpx.Response) -> None:
        if response.is_success:
            return
        content_type = response.headers.get("content-type", "")
        if "application/problem+json" in content_type:
            body = response.json()
            raise ApiError(
                status=int(body.get("status", response.status_code)),
                title=str(body.get("title", "API request failed")),
                detail=str(body.get("detail", response.text)),
                problem_type=str(body.get("type", "about:blank")),
                request_id=body.get("requestId"),
            )
        response.raise_for_status()

    def health(self) -> dict[str, Any]:
        response = self.http.get("/health")
        self._raise_for_problem(response)
        return response.json()

    def create_project(self, name: str, description: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        response = self.http.post("/projects", json=body)
        self._raise_for_problem(response)
        project = response.json()
        project["_etag"] = response.headers.get("etag")
        return project

    def update_project(
        self, project_id: str, etag: str, patch: dict[str, Any]
    ) -> dict[str, Any]:
        response = self.http.patch(
            f"/projects/{project_id}",
            headers={"If-Match": etag, "Content-Type": "application/merge-patch+json"},
            json=patch,
        )
        self._raise_for_problem(response)
        project = response.json()
        project["_etag"] = response.headers.get("etag")
        return project

    def register_local_dataset(
        self,
        project_id: str,
        name: str,
        file_name: str,
        media_type: str = "text/csv",
    ) -> dict[str, Any]:
        response = self.http.post(
            f"/projects/{project_id}/datasets",
            json={
                "name": name,
                "source": {
                    "kind": "local-file",
                    "fileName": file_name,
                    "mediaType": media_type,
                },
            },
        )
        self._raise_for_problem(response)
        return response.json()

    def upload_dataset_content(
        self,
        dataset_id: str,
        content: bytes,
        file_name: str = "dataset.csv",
        media_type: str = "text/csv",
    ) -> dict[str, Any]:
        response = self.http.post(
            f"/datasets/{dataset_id}/content",
            files={"file": (file_name, content, media_type)},
        )
        self._raise_for_problem(response)
        return response.json()

    def start_run(
        self,
        project_id: str,
        dataset_id: str,
        *,
        algorithm: str = "quality-summary",
        idempotency_key: str,
    ) -> dict[str, Any]:
        response = self.http.post(
            "/analysis-runs",
            headers={"Idempotency-Key": idempotency_key},
            json={
                "projectId": project_id,
                "datasetId": dataset_id,
                "parameters": {"algorithm": algorithm, "priority": "normal"},
            },
        )
        self._raise_for_problem(response)
        run = response.json()
        run["_replay"] = response.headers.get("idempotent-replay") == "true"
        run["_location"] = response.headers.get("location")
        return run

    def get_run(self, run_id: str) -> dict[str, Any]:
        response = self.http.get(f"/analysis-runs/{run_id}")
        self._raise_for_problem(response)
        return response.json()

    def wait_for_run(
        self,
        run_id: str,
        *,
        max_polls: int = 10,
        poll_interval: float = 0.0,
    ) -> dict[str, Any]:
        for _ in range(max_polls):
            run = self.get_run(run_id)
            if run["status"] in {"completed", "failed", "canceled"}:
                return run
            if poll_interval:
                time.sleep(poll_interval)
        raise TimeoutError(f"run {run_id} did not reach a terminal state")

    def list_artifacts(self, run_id: str) -> list[dict[str, Any]]:
        response = self.http.get(f"/analysis-runs/{run_id}/artifacts")
        self._raise_for_problem(response)
        return response.json()["items"]

    def complete_workflow(
        self,
        *,
        project_name: str,
        dataset_path: Path,
        idempotency_key: str,
        algorithm: str = "quality-summary",
    ) -> dict[str, Any]:
        project = self.create_project(project_name)
        dataset = self.register_local_dataset(
            project["id"], dataset_path.stem, dataset_path.name
        )
        receipt = self.upload_dataset_content(
            dataset["id"], dataset_path.read_bytes(), dataset_path.name
        )
        accepted = self.start_run(
            project["id"],
            dataset["id"],
            algorithm=algorithm,
            idempotency_key=idempotency_key,
        )
        completed = self.wait_for_run(accepted["id"])
        artifacts = self.list_artifacts(completed["id"])
        return {
            "project": project,
            "dataset": dataset,
            "upload": receipt,
            "run": completed,
            "artifacts": artifacts,
        }
