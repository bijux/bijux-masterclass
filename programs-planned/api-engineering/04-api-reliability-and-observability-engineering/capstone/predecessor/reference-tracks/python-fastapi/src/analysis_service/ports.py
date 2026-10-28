"""Application-owned ports.

The Protocols make dependencies visible without forcing a ceremonial class per
SQL table.  Cross-table transactions remain inside one repository adapter,
which is the correct boundary for this compact service.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Protocol

from .auth import Principal
from .domain import StoredResponse
from .models import (
    AnalysisRun,
    AnalysisRunCreate,
    AnalysisRunV12,
    Artifact,
    Dataset,
    DatasetCreate,
    Project,
    ProjectCreate,
    ProjectPatch,
    RunProgressEvent,
    UploadReceipt,
    WebhookSubscription,
    WebhookSubscriptionCreate,
)


@dataclass(frozen=True, slots=True)
class StagedFile:
    temporary_path: Path
    size: int
    checksum_sha256: str
    media_type: str


@dataclass(frozen=True, slots=True)
class ClaimedJob:
    run_id: str
    dataset_id: str
    owner_id: str
    algorithm: str
    source_kind: str
    source: dict[str, Any]
    content_path: str | None
    expected_checksum: str | None
    attempt: int
    lease_owner: str
    lease_generation: int


@dataclass(frozen=True, slots=True)
class ClaimedDelivery:
    delivery_id: str
    event_id: str
    delivery_kind: str
    target_url: str
    payload: dict[str, Any]
    secret: str
    attempt: int
    lease_owner: str
    lease_generation: int


RunRepresentation = AnalysisRun | AnalysisRunV12


class Repository(Protocol):
    # Application-facing operations.
    def health(self) -> None: ...

    def create_project(self, principal: Principal, body: ProjectCreate) -> Project: ...

    def get_project(self, principal: Principal, project_id: str) -> Project: ...

    def list_projects(
        self,
        principal: Principal,
        limit: int,
        cursor: int | None,
        name: str | None,
    ) -> tuple[list[Project], str | None]: ...

    def update_project(
        self,
        principal: Principal,
        project_id: str,
        if_match: str | None,
        patch: ProjectPatch,
    ) -> Project: ...

    def create_dataset(
        self,
        principal: Principal,
        project_id: str,
        body: DatasetCreate,
    ) -> Dataset: ...

    def get_dataset(self, principal: Principal, dataset_id: str) -> Dataset: ...

    def list_datasets(
        self,
        principal: Principal,
        project_id: str,
        limit: int,
        cursor: int | None,
        status: str | None,
    ) -> tuple[list[Dataset], str | None]: ...

    def attach_uploaded_content(
        self,
        principal: Principal,
        dataset_id: str,
        staged: StagedFile,
        storage_key: str,
    ) -> UploadReceipt: ...

    def delete_dataset(self, principal: Principal, dataset_id: str) -> None: ...

    def create_run_idempotently(
        self,
        principal: Principal,
        key: str,
        body: AnalysisRunCreate,
    ) -> StoredResponse: ...

    def get_run(
        self,
        principal: Principal,
        run_id: str,
    ) -> RunRepresentation: ...

    def list_runs(
        self,
        principal: Principal,
        limit: int,
        cursor: int | None,
        status: str | None,
    ) -> tuple[list[RunRepresentation], str | None]: ...

    def cancel_run(
        self,
        principal: Principal,
        run_id: str,
    ) -> RunRepresentation: ...

    def list_artifacts(
        self,
        principal: Principal,
        run_id: str,
    ) -> list[Artifact]: ...

    def get_artifact(
        self,
        principal: Principal,
        artifact_id: str,
    ) -> Artifact: ...

    def artifact_storage_key(
        self,
        principal: Principal,
        artifact_id: str,
    ) -> str: ...

    def progress_events(
        self,
        principal: Principal,
        run_id: str,
        after: int = 0,
    ) -> list[RunProgressEvent]: ...

    def create_subscription(
        self,
        principal: Principal,
        body: WebhookSubscriptionCreate,
    ) -> WebhookSubscription: ...

    def diagnostics(self) -> dict[str, Any]: ...

    # Worker-facing operations.
    def claim_job(self, worker_id: str, lease_seconds: int) -> ClaimedJob | None: ...

    def mark_job_running(self, job: ClaimedJob) -> None: ...

    def renew_job_lease(self, job: ClaimedJob, lease_seconds: int) -> None: ...

    def complete_job(
        self,
        job: ClaimedJob,
        artifact: StagedFile,
        storage_key: str,
        name: str,
        result_summary: dict[str, Any],
    ) -> bool: ...

    def fail_job(
        self,
        job: ClaimedJob,
        code: str,
        detail: str,
        retryable: bool,
    ) -> None: ...

    def recover_expired_jobs(self) -> int: ...

    def expand_outbox(self) -> int: ...

    def claim_delivery(
        self,
        worker_id: str,
        lease_seconds: int,
    ) -> ClaimedDelivery | None: ...

    def record_delivery_success(
        self,
        delivery: ClaimedDelivery,
        status: int,
    ) -> None: ...

    def record_delivery_failure(
        self,
        delivery: ClaimedDelivery,
        error: str,
        retryable: bool,
    ) -> None: ...

    def recover_expired_deliveries(self) -> int: ...


class ArtifactStore(Protocol):
    async def stage_upload(
        self,
        source: BinaryIO,
        media_type: str,
        limit: int,
    ) -> StagedFile: ...

    def stage_bytes(self, content: bytes, media_type: str) -> StagedFile: ...

    def publish(self, staged: StagedFile, key: str) -> Path: ...

    def discard(self, staged: StagedFile) -> None: ...

    def path_for(
        self,
        key: str,
        expected_checksum: str | None = None,
    ) -> Path: ...


class OutboundTransport(Protocol):
    def post(
        self,
        url: str,
        body: bytes,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> int: ...
