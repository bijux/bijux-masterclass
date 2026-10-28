from __future__ import annotations

import asyncio
import json
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timezone
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
from fastapi.exceptions import RequestValidationError
from fastapi.responses import StreamingResponse

from . import __version__
from .auth import Principal, require_scopes
from .errors import ApiProblem, api_problem_handler, validation_problem_handler
from .models import (
    AnalysisRun,
    AnalysisRunCreate,
    AnalysisRunPage,
    Artifact,
    ArtifactPage,
    Dataset,
    DatasetCreate,
    DatasetPage,
    Diagnostics,
    Health,
    Project,
    ProjectCreate,
    ProjectPage,
    ProjectPatch,
    UploadReceipt,
    WebhookSubscription,
    WebhookSubscriptionCreate,
)
from .store import store


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    stop = asyncio.Event()

    async def simulate_jobs() -> None:
        while not stop.is_set():
            store.advance_simulation()
            try:
                await asyncio.wait_for(stop.wait(), timeout=0.01)
            except TimeoutError:
                pass

    task = asyncio.create_task(simulate_jobs())
    try:
        yield
    finally:
        stop.set()
        await task


app = FastAPI(
    title="Analysis Runs API — Python provider",
    version=__version__,
    lifespan=lifespan,
    description=(
        "A deterministic implementation used to test the canonical external OpenAPI contract. "
        "The generated framework document is evidence for drift review, not the source of truth."
    ),
)

app.add_exception_handler(ApiProblem, api_problem_handler)
app.add_exception_handler(RequestValidationError, validation_problem_handler)


@app.middleware("http")
async def attach_request_id(request: Request, call_next):
    request.state.request_id = f"req_{secrets.token_hex(6)}"
    response = await call_next(request)
    response.headers.setdefault("X-Request-Id", request.state.request_id)
    return response


def _set_project_headers(response: Response, project: Project) -> None:
    response.headers["ETag"] = store.etag(project)


@app.get(
    "/health",
    response_model=Health,
    operation_id="getHealth",
    tags=["System"],
)
async def get_health() -> Health:
    return Health(version=__version__, time=datetime.now(timezone.utc))


@app.get(
    "/projects",
    response_model=ProjectPage,
    operation_id="listProjects",
    tags=["Projects"],
)
async def list_projects(
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = Query(default=None, pattern=r"^[0-9]+$"),
    name: str | None = Query(default=None, min_length=1, max_length=80),
    principal: Principal = Depends(require_scopes("projects:read")),
) -> ProjectPage:
    items, next_cursor = store.list_projects(
        principal.subject, principal.admin, limit, cursor, name
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
    project = store.create_project(principal.subject, body)
    response.headers["Location"] = f"/projects/{project.id}"
    _set_project_headers(response, project)
    return project


@app.get(
    "/projects/{projectId}",
    response_model=Project,
    operation_id="getProject",
    tags=["Projects"],
)
async def get_project(
    response: Response,
    project_id: Annotated[str, Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("projects:read")),
) -> Project:
    project = store.get_project(project_id, principal.subject, principal.admin)
    _set_project_headers(response, project)
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
    project_id: Annotated[str, Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")],
    if_match: str | None = Header(default=None, alias="If-Match"),
    principal: Principal = Depends(require_scopes("projects:write")),
) -> Project:
    project = store.update_project(
        project_id, principal.subject, principal.admin, if_match, body
    )
    _set_project_headers(response, project)
    return project


@app.get(
    "/projects/{projectId}/datasets",
    response_model=DatasetPage,
    operation_id="listProjectDatasets",
    tags=["Datasets"],
)
async def list_project_datasets(
    project_id: Annotated[str, Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")],
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = Query(default=None, pattern=r"^[0-9]+$"),
    dataset_status: Literal["awaiting-upload", "ready"] | None = Query(
        default=None, alias="status"
    ),
    principal: Principal = Depends(require_scopes("datasets:read")),
) -> DatasetPage:
    items, next_cursor = store.list_datasets(
        project_id,
        principal.subject,
        principal.admin,
        limit,
        cursor,
        dataset_status,
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
    project_id: Annotated[str, Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")],
    body: DatasetCreate,
    response: Response,
    principal: Principal = Depends(require_scopes("datasets:write")),
) -> Dataset:
    dataset = store.create_dataset(project_id, principal.subject, principal.admin, body)
    response.headers["Location"] = f"/datasets/{dataset.id}"
    return dataset


@app.get(
    "/datasets/{datasetId}",
    response_model=Dataset,
    operation_id="getDataset",
    tags=["Datasets"],
)
async def get_dataset(
    dataset_id: Annotated[str, Path(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("datasets:read")),
) -> Dataset:
    return store.get_dataset(dataset_id, principal.subject, principal.admin)


@app.delete(
    "/datasets/{datasetId}",
    status_code=204,
    response_class=Response,
    operation_id="deleteDataset",
    tags=["Datasets"],
)
async def delete_dataset(
    dataset_id: Annotated[str, Path(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("datasets:write")),
) -> Response:
    store.delete_dataset(dataset_id, principal.subject, principal.admin)
    return Response(status_code=204)


@app.post(
    "/datasets/{datasetId}/content",
    response_model=UploadReceipt,
    status_code=201,
    operation_id="uploadDatasetContent",
    tags=["Datasets"],
)
async def upload_dataset_content(
    dataset_id: Annotated[str, Path(alias="datasetId", pattern=r"^dts_[0-9]{4,18}$")],
    file: UploadFile = File(...),
    description: str | None = Form(default=None, max_length=200),
    principal: Principal = Depends(require_scopes("datasets:write")),
) -> UploadReceipt:
    del description
    content = await file.read(1_048_577)
    return store.upload_dataset(
        dataset_id,
        principal.subject,
        principal.admin,
        content,
        file.content_type or "application/octet-stream",
    )


@app.get(
    "/analysis-runs",
    response_model=AnalysisRunPage,
    operation_id="listAnalysisRuns",
    tags=["Analysis Runs"],
)
async def list_analysis_runs(
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = Query(default=None, pattern=r"^[0-9]+$"),
    run_status: Literal["queued", "running", "completed", "failed", "canceled"] | None = Query(
        default=None, alias="status"
    ),
    principal: Principal = Depends(require_scopes("runs:read")),
) -> AnalysisRunPage:
    items, next_cursor = store.list_runs(
        principal.subject, principal.admin, limit, cursor, run_status
    )
    return AnalysisRunPage(items=items, nextCursor=next_cursor)


@app.post(
    "/analysis-runs",
    response_model=AnalysisRun,
    status_code=202,
    operation_id="createAnalysisRun",
    tags=["Analysis Runs"],
)
async def create_analysis_run(
    body: AnalysisRunCreate,
    response: Response,
    idempotency_key: str = Header(
        alias="Idempotency-Key",
        min_length=16,
        max_length=64,
        pattern=r"^[A-Za-z0-9._~-]+$",
    ),
    principal: Principal = Depends(require_scopes("runs:write")),
) -> AnalysisRun:
    run, replay = store.create_run(
        principal.subject, principal.admin, idempotency_key, body
    )
    response.headers["Location"] = f"/analysis-runs/{run.id}"
    response.headers["Retry-After"] = "1"
    response.headers["Idempotent-Replay"] = "true" if replay else "false"
    return run


@app.get(
    "/analysis-runs/{runId}",
    response_model=AnalysisRun,
    operation_id="getAnalysisRun",
    tags=["Analysis Runs"],
)
async def get_analysis_run(
    run_id: Annotated[str, Path(alias="runId", pattern=r"^run_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("runs:read")),
) -> AnalysisRun:
    return store.get_run(run_id, principal.subject, principal.admin)


@app.post(
    "/analysis-runs/{runId}/cancellation",
    response_model=AnalysisRun,
    operation_id="cancelAnalysisRun",
    tags=["Analysis Runs"],
)
async def cancel_analysis_run(
    run_id: Annotated[str, Path(alias="runId", pattern=r"^run_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("runs:write")),
) -> AnalysisRun:
    return store.cancel_run(run_id, principal.subject, principal.admin)


@app.get(
    "/analysis-runs/{runId}/artifacts",
    response_model=ArtifactPage,
    operation_id="listRunArtifacts",
    tags=["Artifacts"],
)
async def list_run_artifacts(
    run_id: Annotated[str, Path(alias="runId", pattern=r"^run_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("artifacts:read")),
) -> ArtifactPage:
    return ArtifactPage(items=store.list_artifacts(run_id, principal.subject, principal.admin))


@app.get(
    "/analysis-runs/{runId}/events",
    operation_id="streamAnalysisRunEvents",
    tags=["Analysis Runs"],
)
async def stream_analysis_run_events(
    run_id: Annotated[str, Path(alias="runId", pattern=r"^run_[0-9]{4,18}$")],
    accept: str = Header(default="text/event-stream", alias="Accept"),
    principal: Principal = Depends(require_scopes("runs:read")),
) -> StreamingResponse:
    # The stream observes simulator-owned transitions; it does not create them.
    async def observed_events():
        emitted = 0
        for _ in range(250):
            events = store.progress_events(
                run_id,
                principal.subject,
                principal.admin,
            )
            for event in events[emitted:]:
                emitted += 1
                yield event
            current = store.get_run(
                run_id,
                principal.subject,
                principal.admin,
            )
            if current.status in {"completed", "failed", "canceled"}:
                return
            await asyncio.sleep(0.01)

    if "application/x-ndjson" in accept:
        async def ndjson_stream():
            async for event in observed_events():
                yield (
                    json.dumps(
                        event.model_dump(by_alias=True, mode="json"),
                        separators=(",", ":"),
                    )
                    + "\n"
                )

        return StreamingResponse(
            ndjson_stream(),
            media_type="application/x-ndjson",
        )

    async def sse_stream():
        async for event in observed_events():
            data = json.dumps(
                event.model_dump(by_alias=True, mode="json"),
                separators=(",", ":"),
            )
            yield (
                f"id: {event.event_id}\n"
                "event: progress\n"
                f"data: {data}\n\n"
            )

    return StreamingResponse(
        sse_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )


@app.get(
    "/artifacts/{artifactId}",
    response_model=Artifact,
    operation_id="getArtifact",
    tags=["Artifacts"],
)
async def get_artifact(
    artifact_id: Annotated[str, Path(alias="artifactId", pattern=r"^art_[0-9]{4,18}$")],
    principal: Principal = Depends(require_scopes("artifacts:read")),
) -> Artifact:
    return store.get_artifact(artifact_id, principal.subject, principal.admin)


@app.post(
    "/webhook-subscriptions",
    response_model=WebhookSubscription,
    status_code=201,
    operation_id="createWebhookSubscription",
    tags=["Webhooks"],
)
async def create_webhook_subscription(
    body: WebhookSubscriptionCreate,
    response: Response,
    principal: Principal = Depends(require_scopes("webhooks:write")),
) -> WebhookSubscription:
    subscription = store.create_subscription(principal.subject, body)
    response.headers["Location"] = f"/webhook-subscriptions/{subscription.id}"
    return subscription


@app.get(
    "/internal/diagnostics",
    response_model=Diagnostics,
    operation_id="getInternalDiagnostics",
    tags=["Internal"],
)
async def get_internal_diagnostics(
    principal: Principal = Depends(require_scopes("admin")),
) -> Diagnostics:
    del principal
    return Diagnostics.model_validate(store.diagnostics())
