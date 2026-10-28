from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Health(ContractModel):
    status: Literal["ok"] = "ok"
    service: Literal["analysis-runs-api"] = "analysis-runs-api"
    version: str = Field(pattern=r"^[0-9]+\.[0-9]+\.[0-9]+$")
    time: datetime


class ProjectCreate(ContractModel):
    name: str = Field(min_length=1, max_length=80, pattern=r"^\S(?:.*\S)?$")
    description: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def reject_explicit_null_description(self) -> "ProjectCreate":
        if "description" in self.model_fields_set and self.description is None:
            raise ValueError("description may be omitted but may not be null")
        return self


class ProjectPatch(ContractModel):
    name: str | None = Field(default=None, min_length=1, max_length=80, pattern=r"^\S(?:.*\S)?$")
    description: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def require_one_field(self) -> "ProjectPatch":
        if not self.model_fields_set:
            raise ValueError("at least one property must be supplied")
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("name may be omitted but may not be null")
        return self


class Project(ContractModel):
    id: str = Field(pattern=r"^prj_[0-9]{4,18}$")
    owner_id: str = Field(alias="ownerId", pattern=r"^[a-z][a-z0-9-]{2,31}$")
    name: str = Field(min_length=1, max_length=80)
    description: str | None = Field(max_length=500)
    version: int = Field(ge=1)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ProjectPage(ContractModel):
    items: list[Project] = Field(max_length=50)
    next_cursor: str | None = Field(alias="nextCursor", default=None, pattern=r"^[0-9]+$")


class LocalFileSource(ContractModel):
    kind: Literal["local-file"]
    file_name: str = Field(alias="fileName", min_length=1, max_length=255)
    media_type: Literal["text/csv", "application/json", "application/octet-stream"] = Field(alias="mediaType")


class RemoteObjectSource(ContractModel):
    kind: Literal["remote-object"]
    uri: str = Field(pattern=r"^https://objects\.example\.test/[^?#\s]+$")
    checksum_sha256: str | None = Field(
        default=None,
        alias="checksumSha256",
        pattern=r"^[a-f0-9]{64}$",
    )

    @model_validator(mode="after")
    def reject_explicit_null_checksum(self) -> "RemoteObjectSource":
        if "checksum_sha256" in self.model_fields_set and self.checksum_sha256 is None:
            raise ValueError("checksumSha256 may be omitted but may not be null")
        return self


DatasetSource = Annotated[LocalFileSource | RemoteObjectSource, Field(discriminator="kind")]


class DatasetCreate(ContractModel):
    name: str = Field(min_length=1, max_length=100)
    source: DatasetSource


class Dataset(ContractModel):
    id: str = Field(pattern=r"^dts_[0-9]{4,18}$")
    project_id: str = Field(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")
    owner_id: str = Field(alias="ownerId", pattern=r"^[a-z][a-z0-9-]{2,31}$")
    name: str = Field(min_length=1, max_length=100)
    source: DatasetSource
    status: Literal["awaiting-upload", "ready", "deleted"]
    content_length: int | None = Field(default=None, alias="contentLength", ge=0)
    checksum_sha256: str | None = Field(default=None, alias="checksumSha256", pattern=r"^[a-f0-9]{64}$")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class DatasetPage(ContractModel):
    items: list[Dataset] = Field(max_length=50)
    next_cursor: str | None = Field(alias="nextCursor", default=None, pattern=r"^[0-9]+$")


class UploadReceipt(ContractModel):
    dataset_id: str = Field(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$")
    content_length: int = Field(alias="contentLength", ge=1, le=1_048_576)
    checksum_sha256: str = Field(alias="checksumSha256", pattern=r"^[a-f0-9]{64}$")
    uploaded_at: datetime = Field(alias="uploadedAt")


class AnalysisParameters(ContractModel):
    algorithm: Literal["quality-summary", "line-count", "checksum"]
    priority: Literal["normal", "high"] = "normal"
    labels: dict[str, str] = Field(default_factory=dict, max_length=10)

    @model_validator(mode="after")
    def validate_labels(self) -> "AnalysisParameters":
        import re

        for key, value in self.labels.items():
            if not re.fullmatch(r"[a-z][a-z0-9_.-]{0,31}", key):
                raise ValueError(f"invalid label key: {key}")
            if len(value) > 80:
                raise ValueError(f"label value too long: {key}")
        return self


class AnalysisRunCreate(ContractModel):
    project_id: str = Field(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")
    dataset_id: str = Field(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$")
    parameters: AnalysisParameters
    callback_url: str | None = Field(
        default=None,
        alias="callbackUrl",
        pattern=r"^https://hooks\.example\.test(?:/[^#\s]*)?$",
    )

    @model_validator(mode="after")
    def reject_explicit_null_callback(self) -> "AnalysisRunCreate":
        if "callback_url" in self.model_fields_set and self.callback_url is None:
            raise ValueError("callbackUrl may be omitted but may not be null")
        return self


RunStatus = Literal["queued", "running", "completed", "failed", "canceled"]


class AnalysisRun(ContractModel):
    id: str = Field(pattern=r"^run_[0-9]{4,18}$")
    project_id: str = Field(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")
    dataset_id: str = Field(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$")
    owner_id: str = Field(alias="ownerId", pattern=r"^[a-z][a-z0-9-]{2,31}$")
    status: RunStatus
    parameters: AnalysisParameters
    progress: int = Field(ge=0, le=100)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    completed_at: datetime | None = Field(alias="completedAt", default=None)
    artifact_ids: list[str] = Field(alias="artifactIds", default_factory=list, max_length=10)


class AnalysisRunPage(ContractModel):
    items: list[AnalysisRun] = Field(max_length=50)
    next_cursor: str | None = Field(alias="nextCursor", default=None, pattern=r"^[0-9]+$")


class Artifact(ContractModel):
    id: str = Field(pattern=r"^art_[0-9]{4,18}$")
    run_id: str = Field(alias="runId", pattern=r"^run_[0-9]{4,18}$")
    owner_id: str = Field(alias="ownerId", pattern=r"^[a-z][a-z0-9-]{2,31}$")
    name: str = Field(min_length=1, max_length=120)
    media_type: Literal["application/json", "text/plain"] = Field(alias="mediaType")
    size: int = Field(ge=1)
    checksum_sha256: str = Field(alias="checksumSha256", pattern=r"^[a-f0-9]{64}$")
    created_at: datetime = Field(alias="createdAt")


class ArtifactPage(ContractModel):
    items: list[Artifact] = Field(max_length=10)


class WebhookSubscriptionCreate(ContractModel):
    target_url: str = Field(alias="targetUrl", pattern=r"^https://hooks\.example\.test(?:/[^#\s]*)?$")
    event_types: list[Literal["analysis.completed", "analysis.failed"]] = Field(
        alias="eventTypes", min_length=1, max_length=2
    )
    secret: str = Field(min_length=16, max_length=128)

    @model_validator(mode="after")
    def unique_events(self) -> "WebhookSubscriptionCreate":
        if len(set(self.event_types)) != len(self.event_types):
            raise ValueError("eventTypes must be unique")
        return self


class WebhookSubscription(ContractModel):
    id: str = Field(pattern=r"^whs_[0-9]{4,18}$")
    owner_id: str = Field(alias="ownerId", pattern=r"^[a-z][a-z0-9-]{2,31}$")
    target_url: str = Field(alias="targetUrl", pattern=r"^https://hooks\.example\.test(?:/[^#\s]*)?$")
    event_types: list[Literal["analysis.completed", "analysis.failed"]] = Field(
        alias="eventTypes", min_length=1, max_length=2
    )
    secret_hint: str = Field(alias="secretHint", pattern=r"^\*{4}.{4}$")
    created_at: datetime = Field(alias="createdAt")


class RunProgressEvent(ContractModel):
    event_id: str = Field(alias="eventId", pattern=r"^evt_[0-9]{4,18}$")
    run_id: str = Field(alias="runId", pattern=r"^run_[0-9]{4,18}$")
    status: RunStatus
    progress: int = Field(ge=0, le=100)
    occurred_at: datetime = Field(alias="occurredAt")


class RunCompletedEvent(ContractModel):
    event_id: str = Field(alias="eventId", pattern=r"^evt_[0-9]{4,18}$")
    event_type: Literal["analysis.completed"] = Field(alias="eventType")
    occurred_at: datetime = Field(alias="occurredAt")
    run: AnalysisRun


class Diagnostics(ContractModel):
    counts: dict[str, int]
    outbound_events: list[RunCompletedEvent] = Field(alias="outboundEvents")
