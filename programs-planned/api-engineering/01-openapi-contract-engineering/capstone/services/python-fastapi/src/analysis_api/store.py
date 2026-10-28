from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from threading import RLock
from time import monotonic
from typing import Any

from .errors import ApiProblem
from .models import (
    AnalysisRun,
    AnalysisRunCreate,
    Artifact,
    Dataset,
    DatasetCreate,
    LocalFileSource,
    Project,
    ProjectCreate,
    ProjectPatch,
    RunCompletedEvent,
    RunProgressEvent,
    UploadReceipt,
    WebhookSubscription,
    WebhookSubscriptionCreate,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _cursor_slice(values: list[Any], cursor: str | None, limit: int) -> tuple[list[Any], str | None]:
    start = int(cursor or "0")
    page = values[start : start + limit]
    next_cursor = str(start + limit) if start + limit < len(values) else None
    return page, next_cursor


class InMemoryStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.projects: dict[str, Project] = {}
            self.datasets: dict[str, Dataset] = {}
            self.dataset_content: dict[str, bytes] = {}
            self.runs: dict[str, AnalysisRun] = {}
            self.run_callbacks: dict[str, str | None] = {}
            self.artifacts: dict[str, Artifact] = {}
            self.subscriptions: dict[str, WebhookSubscription] = {}
            self.outbound_events: list[RunCompletedEvent] = []
            self.progress_by_run: dict[str, list[RunProgressEvent]] = {}
            self.run_due_at: dict[str, float] = {}
            self.idempotency: dict[tuple[str, str], tuple[str, str]] = {}
            self.counters = {
                "project": 0,
                "dataset": 0,
                "run": 0,
                "artifact": 0,
                "subscription": 0,
                "event": 0,
            }

    def _id(self, kind: str, prefix: str) -> str:
        self.counters[kind] += 1
        return f"{prefix}_{self.counters[kind]:04d}"

    @staticmethod
    def etag(project: Project) -> str:
        return f'"{project.id}:{project.version}"'

    @staticmethod
    def _visible(owner: str, actual_owner: str, admin: bool) -> bool:
        return admin or owner == actual_owner

    def create_project(self, owner: str, body: ProjectCreate) -> Project:
        with self._lock:
            now = utcnow()
            project = Project(
                id=self._id("project", "prj"),
                ownerId=owner,
                name=body.name,
                description=body.description,
                version=1,
                createdAt=now,
                updatedAt=now,
            )
            self.projects[project.id] = project
            return project

    def get_project(self, project_id: str, owner: str, admin: bool = False) -> Project:
        project = self.projects.get(project_id)
        if project is None or not self._visible(owner, project.owner_id, admin):
            raise ApiProblem(404, "Resource not found", "The requested project does not exist.", "not-found")
        return project

    def list_projects(
        self, owner: str, admin: bool, limit: int, cursor: str | None, name: str | None
    ) -> tuple[list[Project], str | None]:
        values = [
            project
            for project in self.projects.values()
            if self._visible(owner, project.owner_id, admin)
            and (name is None or name.lower() in project.name.lower())
        ]
        values.sort(key=lambda item: item.id)
        return _cursor_slice(values, cursor, limit)

    def update_project(
        self,
        project_id: str,
        owner: str,
        admin: bool,
        if_match: str | None,
        patch: ProjectPatch,
    ) -> Project:
        with self._lock:
            project = self.get_project(project_id, owner, admin)
            if if_match is None:
                raise ApiProblem(
                    428,
                    "Precondition required",
                    "This update requires the latest If-Match entity tag.",
                    "precondition-required",
                )
            if if_match != self.etag(project):
                raise ApiProblem(
                    412,
                    "Precondition failed",
                    "The supplied entity tag is stale.",
                    "precondition-failed",
                )
            update: dict[str, Any] = {"version": project.version + 1, "updated_at": utcnow()}
            if "name" in patch.model_fields_set:
                update["name"] = patch.name
            if "description" in patch.model_fields_set:
                update["description"] = patch.description
            revised = project.model_copy(update=update)
            self.projects[project_id] = revised
            return revised

    def create_dataset(
        self, project_id: str, owner: str, admin: bool, body: DatasetCreate
    ) -> Dataset:
        with self._lock:
            project = self.get_project(project_id, owner, admin)
            now = utcnow()
            local = isinstance(body.source, LocalFileSource)
            dataset = Dataset(
                id=self._id("dataset", "dts"),
                projectId=project.id,
                ownerId=project.owner_id,
                name=body.name,
                source=body.source,
                status="awaiting-upload" if local else "ready",
                contentLength=None,
                checksumSha256=getattr(body.source, "checksum_sha256", None),
                createdAt=now,
                updatedAt=now,
            )
            self.datasets[dataset.id] = dataset
            return dataset

    def get_dataset(self, dataset_id: str, owner: str, admin: bool = False) -> Dataset:
        dataset = self.datasets.get(dataset_id)
        if (
            dataset is None
            or dataset.status == "deleted"
            or not self._visible(owner, dataset.owner_id, admin)
        ):
            raise ApiProblem(404, "Resource not found", "The requested dataset does not exist.", "not-found")
        return dataset

    def list_datasets(
        self,
        project_id: str,
        owner: str,
        admin: bool,
        limit: int,
        cursor: str | None,
        status: str | None,
    ) -> tuple[list[Dataset], str | None]:
        self.get_project(project_id, owner, admin)
        values = [
            dataset
            for dataset in self.datasets.values()
            if dataset.project_id == project_id
            and dataset.status != "deleted"
            and self._visible(owner, dataset.owner_id, admin)
            and (status is None or dataset.status == status)
        ]
        values.sort(key=lambda item: item.id)
        return _cursor_slice(values, cursor, limit)

    def upload_dataset(
        self, dataset_id: str, owner: str, admin: bool, content: bytes, media_type: str
    ) -> UploadReceipt:
        with self._lock:
            dataset = self.get_dataset(dataset_id, owner, admin)
            if not isinstance(dataset.source, LocalFileSource):
                raise ApiProblem(
                    409,
                    "Request conflict",
                    "Remote-object datasets do not accept local uploads.",
                    "conflict",
                )
            allowed = {"text/csv", "application/json", "application/octet-stream"}
            normalized = media_type.split(";", 1)[0].strip().lower()
            if normalized not in allowed:
                raise ApiProblem(
                    415,
                    "Unsupported media type",
                    f"Unsupported uploaded media type: {normalized or '<missing>'}.",
                    "unsupported-media-type",
                )
            if not content:
                raise ApiProblem(422, "Request validation failed", "The uploaded file is empty.", "validation")
            if len(content) > 1_048_576:
                raise ApiProblem(
                    413,
                    "Payload too large",
                    "The training upload limit is 1 MiB.",
                    "payload-too-large",
                )
            digest = hashlib.sha256(content).hexdigest()
            now = utcnow()
            self.dataset_content[dataset_id] = content
            revised = dataset.model_copy(
                update={
                    "status": "ready",
                    "content_length": len(content),
                    "checksum_sha256": digest,
                    "updated_at": now,
                }
            )
            self.datasets[dataset_id] = revised
            return UploadReceipt(
                datasetId=dataset_id,
                contentLength=len(content),
                checksumSha256=digest,
                uploadedAt=now,
            )

    def delete_dataset(self, dataset_id: str, owner: str, admin: bool) -> None:
        with self._lock:
            dataset = self.get_dataset(dataset_id, owner, admin)
            if any(
                run.dataset_id == dataset_id and run.status in {"queued", "running"}
                for run in self.runs.values()
            ):
                raise ApiProblem(
                    409,
                    "Request conflict",
                    "An active analysis run depends on this dataset.",
                    "conflict",
                )
            self.datasets[dataset_id] = dataset.model_copy(
                update={"status": "deleted", "updated_at": utcnow()}
            )
            self.dataset_content.pop(dataset_id, None)

    @staticmethod
    def fingerprint(body: AnalysisRunCreate) -> str:
        canonical = json.dumps(
            body.model_dump(by_alias=True, mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        return hashlib.sha256(canonical).hexdigest()

    def create_run(
        self,
        owner: str,
        admin: bool,
        idempotency_key: str,
        body: AnalysisRunCreate,
    ) -> tuple[AnalysisRun, bool]:
        with self._lock:
            project = self.get_project(body.project_id, owner, admin)
            dataset = self.get_dataset(body.dataset_id, owner, admin)
            if dataset.project_id != project.id:
                raise ApiProblem(
                    409,
                    "Request conflict",
                    "The dataset does not belong to the selected project.",
                    "conflict",
                )
            if dataset.status != "ready":
                raise ApiProblem(
                    409,
                    "Request conflict",
                    "The dataset must be ready before analysis starts.",
                    "conflict",
                )
            fingerprint = self.fingerprint(body)
            key = (owner, idempotency_key)
            if key in self.idempotency:
                previous_fingerprint, run_id = self.idempotency[key]
                if previous_fingerprint != fingerprint:
                    raise ApiProblem(
                        409,
                        "Request conflict",
                        "The idempotency key was already used with a different request body.",
                        "idempotency-conflict",
                    )
                return self.runs[run_id], True

            now = utcnow()
            run = AnalysisRun(
                id=self._id("run", "run"),
                projectId=project.id,
                datasetId=dataset.id,
                ownerId=project.owner_id,
                status="queued",
                parameters=body.parameters,
                progress=0,
                createdAt=now,
                updatedAt=now,
                completedAt=None,
                artifactIds=[],
            )
            self.runs[run.id] = run
            self.run_callbacks[run.id] = body.callback_url
            self.progress_by_run[run.id] = [
                RunProgressEvent(
                    eventId=self._id("event", "evt"),
                    runId=run.id,
                    status="queued",
                    progress=0,
                    occurredAt=now,
                )
            ]
            # Course 1 uses an application-owned simulator so reads remain
            # observational. Course 2 replaces this timer with a durable worker.
            self.run_due_at[run.id] = monotonic() + 0.04
            self.idempotency[key] = (fingerprint, run.id)
            return run, False

    def _artifact_for(self, run: AnalysisRun) -> Artifact:
        payload = json.dumps(
            {
                "runId": run.id,
                "algorithm": run.parameters.algorithm,
                "status": "completed",
            },
            sort_keys=True,
        ).encode()
        now = utcnow()
        return Artifact(
            id=self._id("artifact", "art"),
            runId=run.id,
            ownerId=run.owner_id,
            name=f"{run.parameters.algorithm}.json",
            mediaType="application/json",
            size=len(payload),
            checksumSha256=hashlib.sha256(payload).hexdigest(),
            createdAt=now,
        )

    def _complete(self, run: AnalysisRun) -> AnalysisRun:
        artifact = self._artifact_for(run)
        self.artifacts[artifact.id] = artifact
        now = utcnow()
        completed = run.model_copy(
            update={
                "status": "completed",
                "progress": 100,
                "updated_at": now,
                "completed_at": now,
                "artifact_ids": [artifact.id],
            }
        )
        self.runs[run.id] = completed
        event = RunCompletedEvent(
            eventId=self._id("event", "evt"),
            eventType="analysis.completed",
            occurredAt=now,
            run=completed,
        )
        self.outbound_events.append(event)
        return completed

    def get_run(
        self,
        run_id: str,
        owner: str,
        admin: bool = False,
    ) -> AnalysisRun:
        """Return current state without causing a state transition."""
        with self._lock:
            run = self.runs.get(run_id)
            if run is None or not self._visible(owner, run.owner_id, admin):
                raise ApiProblem(
                    404,
                    "Resource not found",
                    "The requested run does not exist.",
                    "not-found",
                )
            return run

    def advance_simulation(self) -> int:
        """Advance due instructional jobs outside every read operation.

        This is intentionally a simulator, not a durability mechanism. Its only
        purpose is to let Course 1 exercise asynchronous HTTP behavior without
        teaching that polling mutates server state.
        """
        changed = 0
        with self._lock:
            now_clock = monotonic()
            for run_id, due_at in list(self.run_due_at.items()):
                if now_clock < due_at:
                    continue
                run = self.runs.get(run_id)
                if run is None or run.status not in {"queued", "running"}:
                    self.run_due_at.pop(run_id, None)
                    continue
                if run.status == "queued":
                    event_time = utcnow()
                    running = run.model_copy(
                        update={
                            "status": "running",
                            "progress": 50,
                            "updated_at": event_time,
                        }
                    )
                    self.runs[run_id] = running
                    self.progress_by_run.setdefault(run_id, []).append(
                        RunProgressEvent(
                            eventId=self._id("event", "evt"),
                            runId=run_id,
                            status="running",
                            progress=50,
                            occurredAt=event_time,
                        )
                    )
                    self.run_due_at[run_id] = now_clock + 0.04
                else:
                    completed = self._complete(run)
                    self.progress_by_run.setdefault(run_id, []).append(
                        RunProgressEvent(
                            eventId=self._id("event", "evt"),
                            runId=run_id,
                            status="completed",
                            progress=100,
                            occurredAt=completed.updated_at,
                        )
                    )
                    self.run_due_at.pop(run_id, None)
                changed += 1
        return changed

    def list_runs(
        self, owner: str, admin: bool, limit: int, cursor: str | None, status: str | None
    ) -> tuple[list[AnalysisRun], str | None]:
        values = [
            run
            for run in self.runs.values()
            if self._visible(owner, run.owner_id, admin)
            and (status is None or run.status == status)
        ]
        values.sort(key=lambda item: item.id)
        return _cursor_slice(values, cursor, limit)

    def cancel_run(self, run_id: str, owner: str, admin: bool) -> AnalysisRun:
        with self._lock:
            run = self.get_run(run_id, owner, admin)
            if run.status not in {"queued", "running"}:
                raise ApiProblem(
                    409,
                    "Request conflict",
                    f"A {run.status} run cannot be canceled.",
                    "conflict",
                )
            canceled = run.model_copy(
                update={"status": "canceled", "updated_at": utcnow(), "completed_at": utcnow()}
            )
            self.runs[run_id] = canceled
            self.run_due_at.pop(run_id, None)
            self.progress_by_run.setdefault(run_id, []).append(
                RunProgressEvent(
                    eventId=self._id("event", "evt"),
                    runId=run_id,
                    status="canceled",
                    progress=canceled.progress,
                    occurredAt=canceled.updated_at,
                )
            )
            return canceled

    def list_artifacts(self, run_id: str, owner: str, admin: bool) -> list[Artifact]:
        run = self.get_run(run_id, owner, admin)
        if run.status != "completed":
            raise ApiProblem(
                409,
                "Request conflict",
                "Artifacts are available only after completion.",
                "conflict",
            )
        return [self.artifacts[artifact_id] for artifact_id in run.artifact_ids]

    def get_artifact(self, artifact_id: str, owner: str, admin: bool) -> Artifact:
        artifact = self.artifacts.get(artifact_id)
        if artifact is None or not self._visible(owner, artifact.owner_id, admin):
            raise ApiProblem(404, "Resource not found", "The requested artifact does not exist.", "not-found")
        return artifact

    def progress_events(
        self,
        run_id: str,
        owner: str,
        admin: bool,
    ) -> list[RunProgressEvent]:
        with self._lock:
            self.get_run(run_id, owner, admin)
            return list(self.progress_by_run.get(run_id, ()))

    def create_subscription(
        self, owner: str, body: WebhookSubscriptionCreate
    ) -> WebhookSubscription:
        with self._lock:
            subscription = WebhookSubscription(
                id=self._id("subscription", "whs"),
                ownerId=owner,
                targetUrl=body.target_url,
                eventTypes=body.event_types,
                secretHint=f"****{body.secret[-4:]}",
                createdAt=utcnow(),
            )
            self.subscriptions[subscription.id] = subscription
            return subscription

    def diagnostics(self) -> dict[str, Any]:
        return {
            "counts": {
                "projects": len(self.projects),
                "datasets": len([d for d in self.datasets.values() if d.status != "deleted"]),
                "runs": len(self.runs),
                "artifacts": len(self.artifacts),
                "subscriptions": len(self.subscriptions),
            },
            "outboundEvents": self.outbound_events,
        }


store = InMemoryStore()
