"""Framework-independent application use cases."""

from __future__ import annotations

from typing import BinaryIO

from .auth import Principal
from .domain import parse_cursor
from .failures import ServiceError
from .models import (
    AnalysisRunCreate,
    DatasetCreate,
    ProjectCreate,
    ProjectPatch,
    WebhookSubscriptionCreate,
)
from .ports import ArtifactStore, Repository
from .webhooks import validate_destination


ALLOWED_UPLOAD_MEDIA_TYPES = frozenset(
    {
        "text/csv",
        "application/json",
        "application/octet-stream",
    }
)


class AnalysisService:
    def __init__(
        self,
        repository: Repository,
        artifacts: ArtifactStore,
        upload_limit: int,
    ) -> None:
        self.repository = repository
        self.artifacts = artifacts
        self.upload_limit = upload_limit

    def list_projects(
        self,
        principal: Principal,
        limit: int,
        cursor: str | None,
        name: str | None,
    ):
        return self.repository.list_projects(
            principal,
            limit,
            parse_cursor(cursor),
            name,
        )

    def create_project(self, principal: Principal, body: ProjectCreate):
        return self.repository.create_project(principal, body)

    def get_project(self, principal: Principal, project_id: str):
        return self.repository.get_project(principal, project_id)

    def update_project(
        self,
        principal: Principal,
        project_id: str,
        if_match: str | None,
        body: ProjectPatch,
    ):
        return self.repository.update_project(
            principal,
            project_id,
            if_match,
            body,
        )

    def list_datasets(
        self,
        principal: Principal,
        project_id: str,
        limit: int,
        cursor: str | None,
        status: str | None,
    ):
        return self.repository.list_datasets(
            principal,
            project_id,
            limit,
            parse_cursor(cursor),
            status,
        )

    def create_dataset(
        self,
        principal: Principal,
        project_id: str,
        body: DatasetCreate,
    ):
        return self.repository.create_dataset(principal, project_id, body)

    def get_dataset(self, principal: Principal, dataset_id: str):
        return self.repository.get_dataset(principal, dataset_id)

    def delete_dataset(self, principal: Principal, dataset_id: str) -> None:
        self.repository.delete_dataset(principal, dataset_id)

    async def upload_dataset(
        self,
        principal: Principal,
        dataset_id: str,
        source: BinaryIO,
        media_type: str,
    ):
        normalized_media_type = media_type.split(";", 1)[0].strip().lower()
        if normalized_media_type not in ALLOWED_UPLOAD_MEDIA_TYPES:
            raise ServiceError(
                415,
                "Unsupported media type",
                (
                    "Unsupported uploaded media type: "
                    f"{normalized_media_type or '<missing>'}."
                ),
                "unsupported-media-type",
            )

        staged = await self.artifacts.stage_upload(
            source,
            normalized_media_type,
            self.upload_limit,
        )
        storage_key = (
            f"datasets/{staged.checksum_sha256[:2]}/"
            f"{staged.checksum_sha256}"
        )

        # Publication precedes the database reference.  A crash between the two
        # can create an unreferenced content-addressed object, never a dangling
        # database pointer.  The orphan audit/collector is the compensating
        # mechanism and is safer than deleting a key another request may share.
        self.artifacts.publish(staged, storage_key)
        return self.repository.attach_uploaded_content(
            principal,
            dataset_id,
            staged,
            storage_key,
        )

    def list_runs(
        self,
        principal: Principal,
        limit: int,
        cursor: str | None,
        status: str | None,
    ):
        return self.repository.list_runs(
            principal,
            limit,
            parse_cursor(cursor),
            status,
        )

    def create_run(
        self,
        principal: Principal,
        key: str,
        body: AnalysisRunCreate,
    ):
        if body.callback_url is not None:
            validate_destination(body.callback_url)
        return self.repository.create_run_idempotently(principal, key, body)

    def get_run(self, principal: Principal, run_id: str):
        return self.repository.get_run(principal, run_id)

    def cancel_run(self, principal: Principal, run_id: str):
        return self.repository.cancel_run(principal, run_id)

    def list_artifacts(self, principal: Principal, run_id: str):
        return self.repository.list_artifacts(principal, run_id)

    def get_artifact(self, principal: Principal, artifact_id: str):
        return self.repository.get_artifact(principal, artifact_id)

    def artifact_file(self, principal: Principal, artifact_id: str):
        artifact = self.repository.get_artifact(principal, artifact_id)
        key = self.repository.artifact_storage_key(principal, artifact_id)
        path = self.artifacts.path_for(key, artifact.checksum_sha256)
        return artifact, path

    def events(
        self,
        principal: Principal,
        run_id: str,
        after: int = 0,
    ):
        return self.repository.progress_events(principal, run_id, after)

    def create_subscription(
        self,
        principal: Principal,
        body: WebhookSubscriptionCreate,
    ):
        validate_destination(body.target_url)
        return self.repository.create_subscription(principal, body)
