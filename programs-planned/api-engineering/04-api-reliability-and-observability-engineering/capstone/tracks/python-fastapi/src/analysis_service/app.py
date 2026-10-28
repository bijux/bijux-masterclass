"""FastAPI transport adapter for the durable Analysis Runs service."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import json
import re
import secrets
from typing import Annotated, AsyncIterator, Literal

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    Path,
    Query,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import FileResponse, StreamingResponse

from api_reliability.clock import SystemClock
from api_reliability.fastapi_adapter import install_reliability
from api_reliability.health import LifecycleController, LifecyclePhase

from .artifacts import FileSystemArtifactStore
from .auth import Principal, require_scopes
from .config import Settings
from .domain import project_etag
from .failures import ServiceError
from .models import (
    AnalysisRun,
    AnalysisRunCreate,
    AnalysisRunPage,
    AnalysisRunPageV12,
    AnalysisRunV12,
    Artifact,
    ArtifactPage,
    Dataset,
    DatasetCreate,
    DatasetPage,
    Diagnostics,
    DiagnosticsV12,
    Health,
    Project,
    ProjectCreate,
    ProjectPage,
    ProjectPatch,
    UploadReceipt,
    WebhookSubscription,
    WebhookSubscriptionCreate,
)
from .postgres import PostgresRepository
from .problems import install_problem_handlers
from .service import AnalysisService


REQUEST_ID_PATTERN = re.compile(r"^req_[a-f0-9]{12}$")


def build_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    repository = PostgresRepository(
        settings.database_url,
        settings.webhook_encryption_key,
        settings.callback_signing_secret,
        settings.service_release,
    )
    artifact_store = FileSystemArtifactStore(settings.artifact_root)
    service = AnalysisService(
        repository,
        artifact_store,
        settings.upload_limit_bytes,
    )
    reliability_clock = SystemClock()
    lifecycle = LifecycleController()

    run_model = AnalysisRunV12 if settings.exposes_api_1_2 else AnalysisRun
    run_page_model = (
        AnalysisRunPageV12 if settings.exposes_api_1_2 else AnalysisRunPage
    )
    diagnostics_model = (
        DiagnosticsV12 if settings.exposes_api_1_2 else Diagnostics
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            repository.open()
            lifecycle.transition(
                LifecyclePhase.ACCEPTING,
                reason="postgresql-ready",
                timestamp_ms=reliability_clock.now_ms(),
            )
        except Exception:
            lifecycle.transition(
                LifecyclePhase.FAILED,
                reason="startup-failed",
                timestamp_ms=reliability_clock.now_ms(),
            )
            raise
        try:
            yield
        finally:
            if lifecycle.phase in {
                LifecyclePhase.STARTING,
                LifecyclePhase.ACCEPTING,
            }:
                lifecycle.transition(
                    LifecyclePhase.DRAINING,
                    reason="application-shutdown",
                    timestamp_ms=reliability_clock.now_ms(),
                )
            repository.close()
            if lifecycle.phase in {
                LifecyclePhase.DRAINING,
                LifecyclePhase.FAILED,
            }:
                lifecycle.transition(
                    LifecyclePhase.STOPPED,
                    reason="resources-closed",
                    timestamp_ms=reliability_clock.now_ms(),
                )

    app = FastAPI(
        title="Analysis Runs API — durable Python provider",
        version=settings.public_api_version,
        lifespan=lifespan,
    )
    app.state.repository = repository
    app.state.service = service
    app.state.service_release = settings.service_release
    app.state.lifecycle = lifecycle
    install_problem_handlers(app)

    @app.middleware("http")
    async def request_identity(request: Request, call_next):
        supplied = request.headers.get("x-request-id")
        request.state.request_id = (
            supplied
            if supplied and REQUEST_ID_PATTERN.fullmatch(supplied)
            else "req_" + secrets.token_hex(6)
        )
        response = await call_next(request)
        response.headers["X-Request-Id"] = request.state.request_id
        return response

    @app.get(
        "/health",
        response_model=Health,
        operation_id="getHealth",
        tags=["System"],
    )
    async def health() -> Health:
        repository.health()
        return Health(
            version=settings.public_api_version,
            time=datetime.now(timezone.utc),
        )

    @app.get(
        "/projects",
        response_model=ProjectPage,
        operation_id="listProjects",
        tags=["Projects"],
    )
    async def list_projects(
        limit: int = Query(20, ge=1, le=50),
        cursor: str | None = Query(None, pattern=r"^[0-9]+$"),
        name: str | None = Query(None, min_length=1, max_length=80),
        principal: Principal = Depends(require_scopes("projects:read")),
    ) -> ProjectPage:
        items, next_cursor = service.list_projects(
            principal,
            limit,
            cursor,
            name,
        )
        return ProjectPage(items=items, nextCursor=next_cursor)

    @app.post(
        "/projects",
        response_model=Project,
        status_code=201,
        operation_id="createProject",
        tags=["Projects"],
    )
    async def create_project(
        body: ProjectCreate,
        response: Response,
        principal: Principal = Depends(require_scopes("projects:write")),
    ) -> Project:
        project = service.create_project(principal, body)
        response.headers["Location"] = f"/projects/{project.id}"
        response.headers["ETag"] = project_etag(project.id, project.version)
        return project

    @app.get(
        "/projects/{projectId}",
        response_model=Project,
        operation_id="getProject",
        tags=["Projects"],
    )
    async def get_project(
        response: Response,
        project_id: Annotated[
            str,
            Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("projects:read")),
    ) -> Project:
        project = service.get_project(principal, project_id)
        response.headers["ETag"] = project_etag(project.id, project.version)
        return project

    @app.patch(
        "/projects/{projectId}",
        response_model=Project,
        operation_id="updateProject",
        tags=["Projects"],
    )
    async def update_project(
        body: ProjectPatch,
        response: Response,
        project_id: Annotated[
            str,
            Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$"),
        ],
        if_match: str | None = Header(None, alias="If-Match"),
        principal: Principal = Depends(require_scopes("projects:write")),
    ) -> Project:
        project = service.update_project(
            principal,
            project_id,
            if_match,
            body,
        )
        response.headers["ETag"] = project_etag(project.id, project.version)
        return project

    @app.get(
        "/projects/{projectId}/datasets",
        response_model=DatasetPage,
        operation_id="listProjectDatasets",
        tags=["Datasets"],
    )
    async def list_datasets(
        project_id: Annotated[
            str,
            Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$"),
        ],
        limit: int = Query(20, ge=1, le=50),
        cursor: str | None = Query(None, pattern=r"^[0-9]+$"),
        status: Literal["awaiting-upload", "ready"] | None = Query(None),
        principal: Principal = Depends(require_scopes("datasets:read")),
    ) -> DatasetPage:
        items, next_cursor = service.list_datasets(
            principal,
            project_id,
            limit,
            cursor,
            status,
        )
        return DatasetPage(items=items, nextCursor=next_cursor)

    @app.post(
        "/projects/{projectId}/datasets",
        response_model=Dataset,
        status_code=201,
        operation_id="createDataset",
        tags=["Datasets"],
    )
    async def create_dataset(
        body: DatasetCreate,
        response: Response,
        project_id: Annotated[
            str,
            Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("datasets:write")),
    ) -> Dataset:
        dataset = service.create_dataset(principal, project_id, body)
        response.headers["Location"] = f"/datasets/{dataset.id}"
        return dataset

    @app.get(
        "/datasets/{datasetId}",
        response_model=Dataset,
        operation_id="getDataset",
        tags=["Datasets"],
    )
    async def get_dataset(
        dataset_id: Annotated[
            str,
            Path(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("datasets:read")),
    ) -> Dataset:
        return service.get_dataset(principal, dataset_id)

    @app.delete(
        "/datasets/{datasetId}",
        status_code=204,
        response_class=Response,
        operation_id="deleteDataset",
        tags=["Datasets"],
    )
    async def delete_dataset(
        dataset_id: Annotated[
            str,
            Path(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("datasets:write")),
    ) -> Response:
        service.delete_dataset(principal, dataset_id)
        return Response(status_code=204)

    @app.post(
        "/datasets/{datasetId}/content",
        response_model=UploadReceipt,
        status_code=201,
        operation_id="uploadDatasetContent",
        tags=["Datasets"],
    )
    async def upload_dataset(
        dataset_id: Annotated[
            str,
            Path(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$"),
        ],
        file: UploadFile = File(...),
        description: str | None = Form(None, max_length=200),
        principal: Principal = Depends(require_scopes("datasets:write")),
    ) -> UploadReceipt:
        del description
        return await service.upload_dataset(
            principal,
            dataset_id,
            file.file,
            file.content_type or "application/octet-stream",
        )

    @app.get(
        "/analysis-runs",
        response_model=run_page_model,
        operation_id="listAnalysisRuns",
        tags=["Analysis Runs"],
    )
    async def list_runs(
        limit: int = Query(20, ge=1, le=50),
        cursor: str | None = Query(None, pattern=r"^[0-9]+$"),
        status: Literal[
            "queued",
            "running",
            "completed",
            "failed",
            "canceled",
        ]
        | None = Query(None),
        principal: Principal = Depends(require_scopes("runs:read")),
    ):
        items, next_cursor = service.list_runs(
            principal,
            limit,
            cursor,
            status,
        )
        return run_page_model(items=items, nextCursor=next_cursor)

    @app.post(
        "/analysis-runs",
        response_model=run_model,
        status_code=202,
        operation_id="createAnalysisRun",
        tags=["Analysis Runs"],
    )
    async def create_run(
        body: AnalysisRunCreate,
        response: Response,
        idempotency_key: str = Header(
            alias="Idempotency-Key",
            min_length=16,
            max_length=64,
            pattern=r"^[A-Za-z0-9._~-]+$",
        ),
        principal: Principal = Depends(require_scopes("runs:write")),
    ):
        stored = service.create_run(principal, idempotency_key, body)
        for name, value in stored.headers.items():
            response.headers[name] = value
        response.headers["Idempotent-Replay"] = (
            "true" if stored.replay else "false"
        )
        return run_model.model_validate(stored.body)

    @app.get(
        "/analysis-runs/{runId}",
        response_model=run_model,
        operation_id="getAnalysisRun",
        tags=["Analysis Runs"],
    )
    async def get_run(
        run_id: Annotated[
            str,
            Path(alias="runId", pattern=r"^run_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("runs:read")),
    ):
        return service.get_run(principal, run_id)

    @app.post(
        "/analysis-runs/{runId}/cancellation",
        response_model=run_model,
        operation_id="cancelAnalysisRun",
        tags=["Analysis Runs"],
    )
    async def cancel_run(
        run_id: Annotated[
            str,
            Path(alias="runId", pattern=r"^run_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("runs:write")),
    ):
        return service.cancel_run(principal, run_id)

    @app.get(
        "/analysis-runs/{runId}/artifacts",
        response_model=ArtifactPage,
        operation_id="listRunArtifacts",
        tags=["Artifacts"],
    )
    async def list_artifacts(
        run_id: Annotated[
            str,
            Path(alias="runId", pattern=r"^run_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("artifacts:read")),
    ) -> ArtifactPage:
        return ArtifactPage(items=service.list_artifacts(principal, run_id))

    @app.get(
        "/analysis-runs/{runId}/events",
        operation_id="streamAnalysisRunEvents",
        tags=["Analysis Runs"],
    )
    async def stream_events(
        request: Request,
        run_id: Annotated[
            str,
            Path(alias="runId", pattern=r"^run_[0-9]{4,18}$"),
        ],
        accept: str = Header("text/event-stream", alias="Accept"),
        principal: Principal = Depends(require_scopes("runs:read")),
    ) -> StreamingResponse:
        media_type = _select_stream_media_type(accept)
        ndjson = media_type == "application/x-ndjson"

        async def events() -> AsyncIterator[str]:
            after = 0
            idle_iterations = 0
            while not await request.is_disconnected():
                batch = service.events(principal, run_id, after)
                for event in batch:
                    after = int(event.event_id.rsplit("_", 1)[1])
                    data = json.dumps(
                        event.model_dump(by_alias=True, mode="json"),
                        separators=(",", ":"),
                    )
                    if ndjson:
                        yield data + "\n"
                    else:
                        yield (
                            f"id: {event.event_id}\n"
                            "event: progress\n"
                            f"data: {data}\n\n"
                        )
                    if event.status in {"completed", "failed", "canceled"}:
                        return
                idle_iterations += 1
                if idle_iterations % 40 == 0 and not ndjson:
                    yield ": keep-alive\n\n"
                await asyncio.sleep(0.25)

        return StreamingResponse(
            events(),
            media_type=media_type,
            headers={"Cache-Control": "no-cache"},
        )

    @app.get(
        "/artifacts/{artifactId}",
        response_model=Artifact,
        operation_id="getArtifact",
        tags=["Artifacts"],
    )
    async def get_artifact(
        artifact_id: Annotated[
            str,
            Path(alias="artifactId", pattern=r"^art_[0-9]{4,18}$"),
        ],
        principal: Principal = Depends(require_scopes("artifacts:read")),
    ) -> Artifact:
        return service.get_artifact(principal, artifact_id)

    if settings.exposes_api_1_2:

        @app.get(
            "/artifacts/{artifactId}/content",
            operation_id="downloadArtifactContent",
            tags=["Artifacts"],
        )
        async def download_artifact(
            artifact_id: Annotated[
                str,
                Path(alias="artifactId", pattern=r"^art_[0-9]{4,18}$"),
            ],
            if_none_match: str | None = Header(None, alias="If-None-Match"),
            principal: Principal = Depends(require_scopes("artifacts:read")),
        ):
            artifact, path = service.artifact_file(principal, artifact_id)
            etag = f'"sha256:{artifact.checksum_sha256}"'
            if if_none_match == etag:
                return Response(status_code=304, headers={"ETag": etag})
            return FileResponse(
                path,
                media_type=artifact.media_type,
                filename=artifact.name,
                headers={"ETag": etag},
            )

    @app.post(
        "/webhook-subscriptions",
        response_model=WebhookSubscription,
        status_code=201,
        operation_id="createWebhookSubscription",
        tags=["Webhooks"],
    )
    async def create_subscription(
        body: WebhookSubscriptionCreate,
        response: Response,
        principal: Principal = Depends(require_scopes("webhooks:write")),
    ) -> WebhookSubscription:
        subscription = service.create_subscription(principal, body)
        response.headers["Location"] = (
            f"/webhook-subscriptions/{subscription.id}"
        )
        return subscription

    @app.get(
        "/internal/diagnostics",
        response_model=diagnostics_model,
        operation_id="getInternalDiagnostics",
        tags=["Internal"],
    )
    async def diagnostics(
        principal: Principal = Depends(require_scopes("admin")),
    ):
        del principal
        return diagnostics_model.model_validate(repository.diagnostics())

    install_reliability(
        app,
        lifecycle=lifecycle,
        readiness_check=repository.health,
        service_name="analysis-runs-api",
        service_version=settings.service_release,
        environment=settings.environment,
    )

    return app


def _select_stream_media_type(accept: str) -> str:
    accepted = {part.split(";", 1)[0].strip() for part in accept.split(",")}
    if "application/x-ndjson" in accepted:
        return "application/x-ndjson"
    if "text/event-stream" in accepted or "*/*" in accepted:
        return "text/event-stream"
    raise ServiceError(
        406,
        "Not acceptable",
        "Use Accept: text/event-stream or application/x-ndjson.",
        "not-acceptable",
    )


app = build_app()
