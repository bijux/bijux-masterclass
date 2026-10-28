from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .model import ConflictError, DownstreamUnavailable, PreconditionFailed, Principal


@dataclass
class CallLog:
    calls: list[tuple[str, tuple[str, ...]]]

    def add(self, method: str, *keys: str) -> None:
        self.calls.append((method, tuple(keys)))

    def count(self, method: str) -> int:
        return sum(1 for name, _ in self.calls if name == method)

    def reset(self) -> None:
        self.calls.clear()


class AnalysisControlClient:
    """Deterministic stand-in for the Course 8 Analysis Control service."""

    def __init__(self) -> None:
        self.calls = CallLog([])
        self.projects: dict[str, dict[str, Any]] = {
            "proj-1": {
                "id": "proj-1",
                "tenantId": "tenant-a",
                "name": "Genome Study",
                "version": "3",
            }
        }
        self.runs: dict[str, dict[str, Any]] = {
            "run-1": {
                "id": "run-1",
                "tenantId": "tenant-a",
                "projectId": "proj-1",
                "datasetId": "data-1",
                "status": "COMPLETED",
                "version": "5",
                "createdAt": "2026-08-01T10:00:00Z",
                "resultSummary": "complete",
            },
            "run-2": {
                "id": "run-2",
                "tenantId": "tenant-a",
                "projectId": "proj-1",
                "datasetId": "data-2",
                "status": "RUNNING",
                "version": "2",
                "createdAt": "2026-08-02T10:00:00Z",
                "resultSummary": None,
            },
        }
        self._idempotency: dict[str, tuple[tuple[str, ...], str, str]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {
            "run-1": [
                {"sequence": 4, "status": "RUNNING"},
                {"sequence": 5, "status": "COMPLETED"},
            ],
            "run-2": [
                {"sequence": 1, "status": "QUEUED"},
                {"sequence": 2, "status": "RUNNING"},
            ],
        }

    def get_project(self, principal: Principal, project_id: str) -> dict[str, Any] | None:
        self.calls.add("get_project", project_id)
        value = self.projects.get(project_id)
        if value is None or value["tenantId"] != principal.tenant_id:
            return None
        return deepcopy(value)

    def batch_get_projects(
        self, principal: Principal, project_ids: list[str]
    ) -> dict[str, dict[str, Any]]:
        self.calls.add("batch_get_projects", *project_ids)
        return {
            key: deepcopy(value)
            for key in project_ids
            if (value := self.projects.get(key)) is not None
            and value["tenantId"] == principal.tenant_id
        }

    def get_run(self, principal: Principal, run_id: str) -> dict[str, Any] | None:
        self.calls.add("get_run", run_id)
        value = self.runs.get(run_id)
        if value is None or value["tenantId"] != principal.tenant_id:
            return None
        return deepcopy(value)

    def list_runs(
        self,
        principal: Principal,
        *,
        project_id: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        self.calls.add("list_runs", project_id or "*", status or "*")
        values = [
            deepcopy(value)
            for value in self.runs.values()
            if value["tenantId"] == principal.tenant_id
            and (project_id is None or value["projectId"] == project_id)
            and (status is None or value["status"] == status)
        ]
        return sorted(
            values,
            key=lambda value: (value["createdAt"], value["id"]),
            reverse=True,
        )

    def search(self, principal: Principal, text: str) -> list[dict[str, Any]]:
        self.calls.add("search", text)
        needle = text.casefold()
        results: list[dict[str, Any]] = []
        for project in self.projects.values():
            if project["tenantId"] != principal.tenant_id:
                continue
            haystack = f"{project['id']} {project['name']}".casefold()
            if needle in haystack:
                results.append({"type": "Project", "value": deepcopy(project)})
        for run in self.runs.values():
            if run["tenantId"] != principal.tenant_id:
                continue
            haystack = f"{run['id']} {run['status']} {run['datasetId']}".casefold()
            if needle in haystack:
                results.append({"type": "AnalysisRun", "value": deepcopy(run)})
        return results

    def resolve_external_id(
        self, principal: Principal, external_id: str
    ) -> tuple[str, dict[str, Any]] | None:
        prefix, separator, local_id = external_id.partition("/")
        if not separator:
            return None
        if prefix == "project":
            item = self.get_project(principal, local_id)
            return ("Project", item) if item else None
        if prefix == "run":
            item = self.get_run(principal, local_id)
            return ("AnalysisRun", item) if item else None
        return None

    def create_project(
        self,
        principal: Principal,
        *,
        key: str,
        name: str,
    ) -> tuple[dict[str, Any], bool]:
        fingerprint = (principal.tenant_id, name)
        old = self._idempotency.get(key)
        if old is not None:
            old_fingerprint, object_type, object_id = old
            if old_fingerprint != fingerprint or object_type != "Project":
                raise ConflictError("idempotency conflict")
            return deepcopy(self.projects[object_id]), True

        project_id = f"proj-{len(self.projects) + 1}"
        project = {
            "id": project_id,
            "tenantId": principal.tenant_id,
            "name": name,
            "version": "1",
        }
        self.projects[project_id] = project
        self._idempotency[key] = (fingerprint, "Project", project_id)
        return deepcopy(project), False

    def start_analysis(
        self,
        principal: Principal,
        *,
        key: str,
        project_id: str,
        dataset_id: str,
        algorithm: str,
    ) -> tuple[dict[str, Any], bool]:
        fingerprint = (principal.tenant_id, project_id, dataset_id, algorithm)
        old = self._idempotency.get(key)
        if old is not None:
            old_fingerprint, object_type, object_id = old
            if old_fingerprint != fingerprint or object_type != "AnalysisRun":
                raise ConflictError("idempotency conflict")
            return deepcopy(self.runs[object_id]), True

        if self.get_project(principal, project_id) is None:
            raise KeyError(project_id)

        run_id = f"run-{len(self.runs) + 1}"
        run = {
            "id": run_id,
            "tenantId": principal.tenant_id,
            "projectId": project_id,
            "datasetId": dataset_id,
            "status": "QUEUED",
            "version": "1",
            "createdAt": "2026-08-08T12:00:00Z",
            "resultSummary": None,
        }
        self.runs[run_id] = run
        self.events[run_id] = [{"sequence": 1, "status": "QUEUED"}]
        self._idempotency[key] = (fingerprint, "AnalysisRun", run_id)
        return deepcopy(run), False

    def cancel(
        self,
        principal: Principal,
        *,
        run_id: str,
        expected_version: str,
    ) -> dict[str, Any]:
        run = self.runs.get(run_id)
        if run is None or run["tenantId"] != principal.tenant_id:
            raise KeyError(run_id)
        if run["version"] != expected_version:
            raise PreconditionFailed("stale version")
        if run["status"] in {"COMPLETED", "FAILED", "CANCELLED"}:
            raise ConflictError("terminal run")
        run["status"] = "CANCELLED"
        run["version"] = str(int(run["version"]) + 1)
        return deepcopy(run)

    def updates(
        self, principal: Principal, run_id: str, after: int
    ) -> list[dict[str, Any]]:
        self.calls.add("updates", run_id, str(after))
        run = self.runs.get(run_id)
        if run is None or run["tenantId"] != principal.tenant_id:
            return []
        return [
            dict(event, run=deepcopy(run))
            for event in self.events.get(run_id, [])
            if event["sequence"] > after
        ]


class ArtifactServiceClient:
    def __init__(self) -> None:
        self.calls = CallLog([])
        self.available = True
        self.artifacts: dict[str, list[dict[str, Any]]] = {
            "run-1": [
                {
                    "id": "artifact-1",
                    "tenantId": "tenant-a",
                    "runId": "run-1",
                    "mediaType": "application/json",
                    "size": 128,
                    "sha256": "a" * 64,
                    "downloadUrl": "https://artifacts.invalid/a",
                }
            ]
        }

    def _check(self) -> None:
        if not self.available:
            raise DownstreamUnavailable("artifact-service")

    def batch_by_run(
        self, principal: Principal, run_ids: list[str]
    ) -> dict[str, list[dict[str, Any]]]:
        self._check()
        self.calls.add("batch_by_run", *run_ids)
        return {
            run_id: [
                deepcopy(value)
                for value in self.artifacts.get(run_id, [])
                if value["tenantId"] == principal.tenant_id
            ]
            for run_id in run_ids
        }

    def get(self, principal: Principal, artifact_id: str) -> dict[str, Any] | None:
        self._check()
        self.calls.add("get", artifact_id)
        for values in self.artifacts.values():
            for value in values:
                if (
                    value["id"] == artifact_id
                    and value["tenantId"] == principal.tenant_id
                ):
                    return deepcopy(value)
        return None

    def search(self, principal: Principal, text: str) -> list[dict[str, Any]]:
        self._check()
        self.calls.add("search", text)
        needle = text.casefold()
        results: list[dict[str, Any]] = []
        for values in self.artifacts.values():
            for value in values:
                if value["tenantId"] != principal.tenant_id:
                    continue
                haystack = f"{value['id']} {value['mediaType']} {value['runId']}".casefold()
                if needle in haystack:
                    results.append(deepcopy(value))
        return results

    def resolve_external_id(
        self, principal: Principal, external_id: str
    ) -> dict[str, Any] | None:
        prefix, separator, local_id = external_id.partition("/")
        if separator and prefix == "artifact":
            return self.get(principal, local_id)
        return None


class NotificationServiceClient:
    def __init__(self) -> None:
        self.calls = CallLog([])
        self.available = True
        self.summaries = {
            "run-1": {
                "runId": "run-1",
                "tenantId": "tenant-a",
                "delivered": 1,
                "pending": 0,
                "failed": 0,
                "observedAt": "2026-08-08T11:59:50Z",
                "stalenessSeconds": 10,
            },
            "run-2": {
                "runId": "run-2",
                "tenantId": "tenant-a",
                "delivered": 0,
                "pending": 1,
                "failed": 0,
                "observedAt": "2026-08-08T11:59:45Z",
                "stalenessSeconds": 15,
            },
        }

    def batch_by_run(
        self, principal: Principal, run_ids: list[str]
    ) -> dict[str, dict[str, Any]]:
        if not self.available:
            raise DownstreamUnavailable("notification-service")
        self.calls.add("batch_by_run", *run_ids)
        return {
            key: deepcopy(value)
            for key in run_ids
            if (value := self.summaries.get(key)) is not None
            and value["tenantId"] == principal.tenant_id
        }
