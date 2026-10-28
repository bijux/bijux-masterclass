"""PostgreSQL adapter for application and worker use cases.

One adapter owns transactions that cross projects, runs, jobs, artifacts,
events, and outbox records.  Splitting this into one repository per table would
hide the atomicity boundary the course is trying to teach.
"""

from __future__ import annotations

from contextlib import contextmanager
import json
from typing import Any, Callable, Iterator, TypeVar

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .auth import Principal
from .domain import (
    StoredResponse,
    filter_fingerprint,
    parse_project_etag,
    request_fingerprint,
    retry_delay_seconds,
)
from .failures import LeaseLost, ServiceError
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
    ResultSummary,
    RunProgressEvent,
    UploadReceipt,
    WebhookSubscription,
    WebhookSubscriptionCreate,
)
from .ports import ClaimedDelivery, ClaimedJob, RunRepresentation, StagedFile


T = TypeVar("T")
Row = dict[str, Any]


class PostgresRepository:
    def __init__(
        self,
        database_url: str,
        encryption_key: str,
        callback_signing_secret: str,
        service_release: str = "1.0",
    ) -> None:
        if service_release not in {"1.0", "1.1"}:
            raise ValueError("service_release must be 1.0 or 1.1")
        self.pool = ConnectionPool(
            database_url,
            min_size=1,
            max_size=16,
            open=False,
        )
        self.encryption_key = encryption_key
        self.callback_signing_secret = callback_signing_secret
        self.service_release = service_release

    @property
    def exposes_api_1_2(self) -> bool:
        return self.service_release == "1.1"

    def open(self) -> None:
        self.pool.open(wait=True)

    def close(self) -> None:
        self.pool.close()

    @contextmanager
    def connection(self) -> Iterator[Connection[Row]]:
        with self.pool.connection() as connection:
            connection.row_factory = dict_row
            yield connection

    def health(self) -> None:
        with self.connection() as connection:
            connection.execute("SELECT 1").fetchone()

    # ------------------------------------------------------------------
    # Row mapping and visibility
    # ------------------------------------------------------------------
    @staticmethod
    def _visible(
        principal: Principal,
        alias: str = "",
    ) -> tuple[str, list[Any]]:
        prefix = f"{alias}." if alias else ""
        if principal.admin:
            return "TRUE", []
        return f"{prefix}owner_id=%s", [principal.subject]

    @staticmethod
    def _project(row: Row) -> Project:
        return Project(
            id=row["id"],
            ownerId=row["owner_id"],
            name=row["name"],
            description=row["description"],
            version=row["version"],
            createdAt=row["created_at"],
            updatedAt=row["updated_at"],
        )

    @staticmethod
    def _dataset(row: Row) -> Dataset:
        return Dataset(
            id=row["id"],
            projectId=row["project_id"],
            ownerId=row["owner_id"],
            name=row["name"],
            source=row["source"],
            status=row["status"],
            contentLength=row["content_length"],
            checksumSha256=row["checksum_sha256"],
            createdAt=row["created_at"],
            updatedAt=row["updated_at"],
        )

    @staticmethod
    def _artifact(row: Row) -> Artifact:
        return Artifact(
            id=row["id"],
            runId=row["run_id"],
            ownerId=row["owner_id"],
            name=row["name"],
            mediaType=row["media_type"],
            size=row["size"],
            checksumSha256=row["checksum_sha256"],
            createdAt=row["created_at"],
        )

    def _run(self, row: Row) -> RunRepresentation:
        common = dict(
            id=row["id"],
            projectId=row["project_id"],
            datasetId=row["dataset_id"],
            ownerId=row["owner_id"],
            status=row["status"],
            parameters=row["parameters"],
            progress=row["progress"],
            createdAt=row["created_at"],
            updatedAt=row["updated_at"],
            completedAt=row["completed_at"],
            artifactIds=row.get("artifact_ids") or [],
        )
        if not self.exposes_api_1_2:
            return AnalysisRun(**common)
        raw_summary = row.get("result_summary")
        summary = ResultSummary.model_validate(raw_summary) if raw_summary else None
        return AnalysisRunV12(**common, resultSummary=summary)

    @staticmethod
    def _run_select() -> str:
        return """
            SELECT
                r.*,
                COALESCE(
                    (
                        SELECT array_agg(a.id ORDER BY a.position)
                        FROM artifacts AS a
                        WHERE a.run_id = r.id
                    ),
                    '{}'::text[]
                ) AS artifact_ids
            FROM analysis_runs AS r
        """

    # ------------------------------------------------------------------
    # Opaque, principal-bound, filter-bound, high-water cursors
    # ------------------------------------------------------------------
    def _cursor_window(
        self,
        connection: Connection[Row],
        principal: Principal,
        operation: str,
        handle: int | None,
        filters: dict[str, Any],
        snapshot_sql: str,
        snapshot_args: list[Any],
    ) -> tuple[int, int]:
        if handle is None:
            row = connection.execute(snapshot_sql, snapshot_args).fetchone()
            return 0, int(row["snapshot_position"] or 0)

        fingerprint = filter_fingerprint(
            operation,
            principal.subject,
            filters,
        )
        row = connection.execute(
            """
            SELECT boundary_position, snapshot_position
            FROM pagination_cursors
            WHERE handle = %s
              AND owner_id = %s
              AND operation_id = %s
              AND filter_fingerprint = %s
              AND expires_at > clock_timestamp()
            """,
            (handle, principal.subject, operation, fingerprint),
        ).fetchone()
        if not row:
            raise ServiceError(
                422,
                "Request validation failed",
                (
                    "The cursor is invalid, expired, or belongs to "
                    "another principal or query."
                ),
                "cursor-invalid",
            )
        return int(row["boundary_position"]), int(row["snapshot_position"])

    def _new_cursor(
        self,
        connection: Connection[Row],
        principal: Principal,
        operation: str,
        filters: dict[str, Any],
        boundary: int,
        snapshot: int,
    ) -> str:
        connection.execute(
            "DELETE FROM pagination_cursors "
            "WHERE expires_at <= clock_timestamp()"
        )
        row = connection.execute(
            """
            INSERT INTO pagination_cursors(
                owner_id,
                operation_id,
                filter_fingerprint,
                boundary_position,
                snapshot_position
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING handle
            """,
            (
                principal.subject,
                operation,
                filter_fingerprint(operation, principal.subject, filters),
                boundary,
                snapshot,
            ),
        ).fetchone()
        return str(row["handle"])

    def _page(
        self,
        connection: Connection[Row],
        principal: Principal,
        operation: str,
        filters: dict[str, Any],
        rows: list[Row],
        limit: int,
        snapshot: int,
        mapper: Callable[[Row], T],
    ) -> tuple[list[T], str | None]:
        visible = rows[:limit]
        next_cursor = None
        if len(rows) > limit:
            next_cursor = self._new_cursor(
                connection,
                principal,
                operation,
                filters,
                int(visible[-1]["position"]),
                snapshot,
            )
        return [mapper(row) for row in visible], next_cursor

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------
    def create_project(
        self,
        principal: Principal,
        body: ProjectCreate,
    ) -> Project:
        with self.connection() as connection:
            row = connection.execute(
                """
                INSERT INTO projects(owner_id, name, description)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (principal.subject, body.name, body.description),
            ).fetchone()
        return self._project(row)

    def get_project(
        self,
        principal: Principal,
        project_id: str,
    ) -> Project:
        clause, args = self._visible(principal)
        with self.connection() as connection:
            row = connection.execute(
                f"SELECT * FROM projects WHERE id=%s AND {clause}",
                [project_id, *args],
            ).fetchone()
        if not row:
            raise _not_found("project")
        return self._project(row)

    def list_projects(
        self,
        principal: Principal,
        limit: int,
        cursor: int | None,
        name: str | None,
    ) -> tuple[list[Project], str | None]:
        operation = "listProjects"
        filters = {"name": name}
        clause, args = self._visible(principal)

        base_where = [clause]
        base_values: list[Any] = [*args]
        if name is not None:
            base_where.append("lower(name) LIKE lower(%s)")
            base_values.append(f"%{name}%")

        with self.connection() as connection:
            boundary, snapshot = self._cursor_window(
                connection,
                principal,
                operation,
                cursor,
                filters,
                (
                    "SELECT COALESCE(max(position), 0) AS snapshot_position "
                    f"FROM projects WHERE {' AND '.join(base_where)}"
                ),
                base_values,
            )
            where = [
                *base_where,
                "position > %s",
                "position <= %s",
            ]
            rows = connection.execute(
                (
                    f"SELECT * FROM projects WHERE {' AND '.join(where)} "
                    "ORDER BY position LIMIT %s"
                ),
                [*base_values, boundary, snapshot, limit + 1],
            ).fetchall()
            return self._page(
                connection,
                principal,
                operation,
                filters,
                rows,
                limit,
                snapshot,
                self._project,
            )

    def update_project(
        self,
        principal: Principal,
        project_id: str,
        if_match: str | None,
        patch: ProjectPatch,
    ) -> Project:
        if if_match is None:
            raise ServiceError(
                428,
                "Precondition required",
                "This update requires the latest If-Match entity tag.",
                "precondition-required",
            )
        expected_version = parse_project_etag(if_match, project_id)
        clause, args = self._visible(principal)
        with self.connection() as connection:
            with connection.transaction():
                current = connection.execute(
                    f"""
                    SELECT name, description
                    FROM projects
                    WHERE id=%s AND {clause}
                    FOR UPDATE
                    """,
                    [project_id, *args],
                ).fetchone()
                if not current:
                    raise _not_found("project")
                name = (
                    patch.name
                    if "name" in patch.model_fields_set
                    else current["name"]
                )
                description = (
                    patch.description
                    if "description" in patch.model_fields_set
                    else current["description"]
                )
                row = connection.execute(
                    f"""
                    UPDATE projects
                    SET name=%s,
                        description=%s,
                        version=version+1,
                        updated_at=clock_timestamp()
                    WHERE id=%s
                      AND {clause}
                      AND version=%s
                    RETURNING *
                    """,
                    [
                        name,
                        description,
                        project_id,
                        *args,
                        expected_version,
                    ],
                ).fetchone()
                if not row:
                    raise ServiceError(
                        412,
                        "Precondition failed",
                        "The project changed concurrently.",
                        "precondition-failed",
                    )
        return self._project(row)

    # ------------------------------------------------------------------
    # Datasets and uploaded content
    # ------------------------------------------------------------------
    def create_dataset(
        self,
        principal: Principal,
        project_id: str,
        body: DatasetCreate,
    ) -> Dataset:
        source = body.source.model_dump(by_alias=True, mode="json")
        source_kind = source["kind"]
        status = "awaiting-upload" if source_kind == "local-file" else "ready"
        checksum = source.get("checksumSha256")
        with self.connection() as connection:
            row = connection.execute(
                """
                INSERT INTO datasets(
                    project_id,
                    owner_id,
                    name,
                    source_kind,
                    source,
                    status,
                    checksum_sha256
                )
                SELECT id, owner_id, %s, %s, %s::jsonb, %s, %s
                FROM projects
                WHERE id=%s AND (%s OR owner_id=%s)
                RETURNING *
                """,
                (
                    body.name,
                    source_kind,
                    json.dumps(source),
                    status,
                    checksum,
                    project_id,
                    principal.admin,
                    principal.subject,
                ),
            ).fetchone()
        if not row:
            raise _not_found("project")
        return self._dataset(row)

    def get_dataset(
        self,
        principal: Principal,
        dataset_id: str,
    ) -> Dataset:
        clause, args = self._visible(principal)
        with self.connection() as connection:
            row = connection.execute(
                f"""
                SELECT *
                FROM datasets
                WHERE id=%s
                  AND status <> 'deleted'
                  AND {clause}
                """,
                [dataset_id, *args],
            ).fetchone()
        if not row:
            raise _not_found("dataset")
        return self._dataset(row)

    def list_datasets(
        self,
        principal: Principal,
        project_id: str,
        limit: int,
        cursor: int | None,
        status: str | None,
    ) -> tuple[list[Dataset], str | None]:
        operation = "listProjectDatasets"
        filters = {"projectId": project_id, "status": status}
        project_clause, project_args = self._visible(principal, "p")
        base_where = ["d.project_id=%s", "d.status <> 'deleted'"]
        base_values: list[Any] = [project_id]
        if not principal.admin:
            base_where.append("d.owner_id=%s")
            base_values.append(principal.subject)
        if status:
            base_where.append("d.status=%s")
            base_values.append(status)

        with self.connection() as connection:
            project_exists = connection.execute(
                f"""
                SELECT 1
                FROM projects AS p
                WHERE p.id=%s AND {project_clause}
                """,
                [project_id, *project_args],
            ).fetchone()
            if not project_exists:
                raise _not_found("project")

            boundary, snapshot = self._cursor_window(
                connection,
                principal,
                operation,
                cursor,
                filters,
                (
                    "SELECT COALESCE(max(d.position), 0) AS snapshot_position "
                    f"FROM datasets AS d WHERE {' AND '.join(base_where)}"
                ),
                base_values,
            )
            where = [
                *base_where,
                "d.position > %s",
                "d.position <= %s",
            ]
            rows = connection.execute(
                (
                    "SELECT d.* FROM datasets AS d "
                    f"WHERE {' AND '.join(where)} "
                    "ORDER BY d.position LIMIT %s"
                ),
                [*base_values, boundary, snapshot, limit + 1],
            ).fetchall()
            return self._page(
                connection,
                principal,
                operation,
                filters,
                rows,
                limit,
                snapshot,
                self._dataset,
            )

    def attach_uploaded_content(
        self,
        principal: Principal,
        dataset_id: str,
        staged: StagedFile,
        storage_key: str,
    ) -> UploadReceipt:
        with self.connection() as connection:
            with connection.transaction():
                row = connection.execute(
                    """
                    SELECT *
                    FROM datasets
                    WHERE id=%s
                      AND status <> 'deleted'
                      AND (%s OR owner_id=%s)
                    FOR UPDATE
                    """,
                    (dataset_id, principal.admin, principal.subject),
                ).fetchone()
                if not row:
                    raise _not_found("dataset")
                if row["source_kind"] != "local-file":
                    raise ServiceError(
                        409,
                        "Request conflict",
                        "Remote-object datasets do not accept local uploads.",
                        "conflict",
                    )
                if row["status"] == "ready":
                    if row["checksum_sha256"] == staged.checksum_sha256:
                        return UploadReceipt(
                            datasetId=dataset_id,
                            contentLength=row["content_length"],
                            checksumSha256=row["checksum_sha256"],
                            uploadedAt=row["updated_at"],
                        )
                    raise ServiceError(
                        409,
                        "Request conflict",
                        "This dataset already has different content.",
                        "conflict",
                    )

                updated = connection.execute(
                    """
                    UPDATE datasets
                    SET status='ready',
                        content_path=%s,
                        content_length=%s,
                        checksum_sha256=%s,
                        updated_at=clock_timestamp()
                    WHERE position=%s
                    RETURNING *
                    """,
                    (
                        storage_key,
                        staged.size,
                        staged.checksum_sha256,
                        row["position"],
                    ),
                ).fetchone()
        return UploadReceipt(
            datasetId=dataset_id,
            contentLength=staged.size,
            checksumSha256=staged.checksum_sha256,
            uploadedAt=updated["updated_at"],
        )

    def delete_dataset(
        self,
        principal: Principal,
        dataset_id: str,
    ) -> None:
        with self.connection() as connection:
            with connection.transaction():
                row = connection.execute(
                    """
                    SELECT *
                    FROM datasets
                    WHERE id=%s
                      AND status <> 'deleted'
                      AND (%s OR owner_id=%s)
                    FOR UPDATE
                    """,
                    (dataset_id, principal.admin, principal.subject),
                ).fetchone()
                if not row:
                    raise _not_found("dataset")
                active_run = connection.execute(
                    """
                    SELECT 1
                    FROM analysis_runs
                    WHERE dataset_id=%s
                      AND status IN ('queued', 'running')
                    LIMIT 1
                    """,
                    (dataset_id,),
                ).fetchone()
                if active_run:
                    raise ServiceError(
                        409,
                        "Request conflict",
                        "An active analysis run depends on this dataset.",
                        "conflict",
                    )
                connection.execute(
                    """
                    UPDATE datasets
                    SET status='deleted',
                        deleted_at=clock_timestamp(),
                        updated_at=clock_timestamp()
                    WHERE position=%s
                    """,
                    (row["position"],),
                )

    # ------------------------------------------------------------------
    # Analysis runs and persistent idempotency
    # ------------------------------------------------------------------
    def create_run_idempotently(
        self,
        principal: Principal,
        key: str,
        body: AnalysisRunCreate,
    ) -> StoredResponse:
        operation = "createAnalysisRun"
        request_body: dict[str, Any] = {
            "projectId": body.project_id,
            "datasetId": body.dataset_id,
            "parameters": {
                "algorithm": body.parameters.algorithm,
                "priority": body.parameters.priority,
                "labels": body.parameters.labels,
            },
        }
        if body.callback_url is not None:
            request_body["callbackUrl"] = str(body.callback_url)
        fingerprint = request_fingerprint(
            operation,
            principal.subject,
            request_body,
        )
        with self.connection() as connection:
            with connection.transaction():
                connection.execute(
                    """
                    INSERT INTO idempotency_records(
                        owner_id,
                        operation_id,
                        idempotency_key,
                        request_fingerprint,
                        state
                    )
                    VALUES (%s, %s, %s, %s, 'processing')
                    ON CONFLICT DO NOTHING
                    """,
                    (
                        principal.subject,
                        operation,
                        key,
                        fingerprint,
                    ),
                )
                record = connection.execute(
                    """
                    SELECT *
                    FROM idempotency_records
                    WHERE owner_id=%s
                      AND operation_id=%s
                      AND idempotency_key=%s
                    FOR UPDATE
                    """,
                    (principal.subject, operation, key),
                ).fetchone()
                if record["request_fingerprint"] != fingerprint:
                    raise ServiceError(
                        409,
                        "Request conflict",
                        (
                            "The idempotency key was already used with a "
                            "different request body."
                        ),
                        "idempotency-conflict",
                    )
                if record["state"] == "completed":
                    return StoredResponse(
                        record["response_status"],
                        dict(record["response_headers"]),
                        dict(record["response_body"]),
                        True,
                    )

                source = connection.execute(
                    """
                    SELECT
                        p.id AS project_id,
                        p.owner_id,
                        d.id AS dataset_id,
                        d.status AS dataset_status
                    FROM projects AS p
                    JOIN datasets AS d
                      ON d.project_id=p.id
                     AND d.owner_id=p.owner_id
                    WHERE p.id=%s
                      AND d.id=%s
                      AND (%s OR p.owner_id=%s)
                    FOR UPDATE OF d
                    """,
                    (
                        body.project_id,
                        body.dataset_id,
                        principal.admin,
                        principal.subject,
                    ),
                ).fetchone()
                if not source:
                    raise ServiceError(
                        404,
                        "Resource not found",
                        "The selected project or dataset does not exist.",
                        "not-found",
                    )
                if source["dataset_status"] != "ready":
                    raise ServiceError(
                        409,
                        "Request conflict",
                        "The dataset must be ready before analysis starts.",
                        "conflict",
                    )

                run = connection.execute(
                    """
                    INSERT INTO analysis_runs(
                        project_id,
                        dataset_id,
                        owner_id,
                        status,
                        parameters,
                        callback_url,
                        progress
                    )
                    VALUES (%s, %s, %s, 'queued', %s::jsonb, %s, 0)
                    RETURNING *
                    """,
                    (
                        source["project_id"],
                        source["dataset_id"],
                        source["owner_id"],
                        json.dumps(request_body["parameters"]),
                        body.callback_url,
                    ),
                ).fetchone()
                connection.execute(
                    "INSERT INTO run_jobs(run_id, status) VALUES (%s, 'queued')",
                    (run["id"],),
                )
                self._insert_run_event(
                    connection,
                    run["id"],
                    run["owner_id"],
                    "queued",
                    0,
                )

                response = self._run(
                    {**run, "artifact_ids": []}
                ).model_dump(by_alias=True, mode="json")
                headers = {
                    "Location": f"/analysis-runs/{run['id']}",
                    "Retry-After": "1",
                    "Idempotent-Replay": "false",
                }
                connection.execute(
                    """
                    UPDATE idempotency_records
                    SET state='completed',
                        resource_id=%s,
                        response_status=202,
                        response_headers=%s::jsonb,
                        response_body=%s::jsonb,
                        completed_at=clock_timestamp()
                    WHERE owner_id=%s
                      AND operation_id=%s
                      AND idempotency_key=%s
                    """,
                    (
                        run["id"],
                        json.dumps(headers),
                        json.dumps(response),
                        principal.subject,
                        operation,
                        key,
                    ),
                )
                return StoredResponse(202, headers, response, False)

    def get_run(
        self,
        principal: Principal,
        run_id: str,
    ) -> RunRepresentation:
        clause, args = self._visible(principal, "r")
        with self.connection() as connection:
            row = connection.execute(
                self._run_select() + f" WHERE r.id=%s AND {clause}",
                [run_id, *args],
            ).fetchone()
        if not row:
            raise _not_found("analysis run")
        return self._run(row)

    def list_runs(
        self,
        principal: Principal,
        limit: int,
        cursor: int | None,
        status: str | None,
    ) -> tuple[list[RunRepresentation], str | None]:
        operation = "listAnalysisRuns"
        filters = {"status": status}
        clause, args = self._visible(principal, "r")
        base_where = [clause]
        base_values: list[Any] = [*args]
        if status:
            base_where.append("r.status=%s")
            base_values.append(status)

        with self.connection() as connection:
            boundary, snapshot = self._cursor_window(
                connection,
                principal,
                operation,
                cursor,
                filters,
                (
                    "SELECT COALESCE(max(r.position), 0) AS snapshot_position "
                    f"FROM analysis_runs AS r WHERE {' AND '.join(base_where)}"
                ),
                base_values,
            )
            where = [
                *base_where,
                "r.position > %s",
                "r.position <= %s",
            ]
            rows = connection.execute(
                self._run_select()
                + f" WHERE {' AND '.join(where)}"
                + " ORDER BY r.position LIMIT %s",
                [*base_values, boundary, snapshot, limit + 1],
            ).fetchall()
            return self._page(
                connection,
                principal,
                operation,
                filters,
                rows,
                limit,
                snapshot,
                self._run,
            )

    def cancel_run(
        self,
        principal: Principal,
        run_id: str,
    ) -> RunRepresentation:
        with self.connection() as connection:
            with connection.transaction():
                row = connection.execute(
                    """
                    SELECT *
                    FROM analysis_runs
                    WHERE id=%s AND (%s OR owner_id=%s)
                    FOR UPDATE
                    """,
                    (run_id, principal.admin, principal.subject),
                ).fetchone()
                if not row:
                    raise _not_found("analysis run")
                if row["status"] not in {"queued", "running"}:
                    raise ServiceError(
                        409,
                        "Request conflict",
                        "Only queued or running analysis can be canceled.",
                        "invalid-run-transition",
                    )

                if row["status"] == "queued":
                    row = connection.execute(
                        """
                        UPDATE analysis_runs
                        SET status='canceled',
                            cancellation_requested_at=clock_timestamp(),
                            completed_at=clock_timestamp(),
                            updated_at=clock_timestamp()
                        WHERE position=%s
                        RETURNING *
                        """,
                        (row["position"],),
                    ).fetchone()
                    connection.execute(
                        """
                        UPDATE run_jobs
                        SET status='canceled',
                            lease_owner=NULL,
                            lease_expires_at=NULL,
                            updated_at=clock_timestamp()
                        WHERE run_id=%s
                        """,
                        (run_id,),
                    )
                    self._insert_run_event(
                        connection,
                        run_id,
                        row["owner_id"],
                        "canceled",
                        0,
                    )
                else:
                    row = connection.execute(
                        """
                        UPDATE analysis_runs
                        SET cancellation_requested_at=COALESCE(
                                cancellation_requested_at,
                                clock_timestamp()
                            ),
                            updated_at=clock_timestamp()
                        WHERE position=%s
                        RETURNING *
                        """,
                        (row["position"],),
                    ).fetchone()
        return self._run({**row, "artifact_ids": []})

    # ------------------------------------------------------------------
    # Artifacts, events, subscriptions, diagnostics
    # ------------------------------------------------------------------
    def list_artifacts(
        self,
        principal: Principal,
        run_id: str,
    ) -> list[Artifact]:
        with self.connection() as connection:
            visible = connection.execute(
                """
                SELECT 1
                FROM analysis_runs
                WHERE id=%s AND (%s OR owner_id=%s)
                """,
                (run_id, principal.admin, principal.subject),
            ).fetchone()
            if not visible:
                raise _not_found("analysis run")
            rows = connection.execute(
                """
                SELECT a.*
                FROM artifacts AS a
                JOIN analysis_runs AS r ON r.id=a.run_id
                WHERE a.run_id=%s
                  AND r.status='completed'
                  AND (%s OR r.owner_id=%s)
                ORDER BY a.position
                """,
                (run_id, principal.admin, principal.subject),
            ).fetchall()
        return [self._artifact(row) for row in rows]

    def get_artifact(
        self,
        principal: Principal,
        artifact_id: str,
    ) -> Artifact:
        with self.connection() as connection:
            row = connection.execute(
                """
                SELECT a.*
                FROM artifacts AS a
                JOIN analysis_runs AS r ON r.id=a.run_id
                WHERE a.id=%s
                  AND r.status='completed'
                  AND (%s OR a.owner_id=%s)
                """,
                (artifact_id, principal.admin, principal.subject),
            ).fetchone()
        if not row:
            raise _not_found("artifact")
        return self._artifact(row)

    def artifact_storage_key(
        self,
        principal: Principal,
        artifact_id: str,
    ) -> str:
        with self.connection() as connection:
            row = connection.execute(
                """
                SELECT a.storage_key
                FROM artifacts AS a
                JOIN analysis_runs AS r ON r.id=a.run_id
                WHERE a.id=%s
                  AND r.status='completed'
                  AND (%s OR a.owner_id=%s)
                """,
                (artifact_id, principal.admin, principal.subject),
            ).fetchone()
        if not row:
            raise _not_found("artifact")
        return str(row["storage_key"])

    def referenced_storage_keys(self) -> set[str]:
        with self.connection() as connection:
            rows = connection.execute(
                """
                SELECT content_path AS key
                FROM datasets
                WHERE content_path IS NOT NULL
                UNION
                SELECT storage_key AS key
                FROM artifacts
                """
            ).fetchall()
        return {str(row["key"]) for row in rows}

    def progress_events(
        self,
        principal: Principal,
        run_id: str,
        after: int = 0,
    ) -> list[RunProgressEvent]:
        with self.connection() as connection:
            visible = connection.execute(
                """
                SELECT 1
                FROM analysis_runs
                WHERE id=%s AND (%s OR owner_id=%s)
                """,
                (run_id, principal.admin, principal.subject),
            ).fetchone()
            if not visible:
                raise _not_found("analysis run")
            rows = connection.execute(
                """
                SELECT e.*
                FROM run_events AS e
                JOIN analysis_runs AS r ON r.id=e.run_id
                WHERE e.run_id=%s
                  AND e.position>%s
                  AND (%s OR r.owner_id=%s)
                ORDER BY e.position
                """,
                (run_id, after, principal.admin, principal.subject),
            ).fetchall()
        return [
            RunProgressEvent(
                eventId=row["event_id"],
                runId=row["run_id"],
                status=row["status"],
                progress=row["progress"],
                occurredAt=row["occurred_at"],
            )
            for row in rows
        ]

    def create_subscription(
        self,
        principal: Principal,
        body: WebhookSubscriptionCreate,
    ) -> WebhookSubscription:
        hint = "****" + body.secret[-4:]
        with self.connection() as connection:
            row = connection.execute(
                """
                INSERT INTO webhook_subscriptions(
                    owner_id,
                    target_url,
                    event_types,
                    secret_ciphertext,
                    secret_hint
                )
                VALUES (%s, %s, %s, pgp_sym_encrypt(%s, %s), %s)
                RETURNING *
                """,
                (
                    principal.subject,
                    body.target_url,
                    body.event_types,
                    body.secret,
                    self.encryption_key,
                    hint,
                ),
            ).fetchone()
        return WebhookSubscription(
            id=row["id"],
            ownerId=row["owner_id"],
            targetUrl=row["target_url"],
            eventTypes=row["event_types"],
            secretHint=row["secret_hint"],
            createdAt=row["created_at"],
        )

    def diagnostics(self) -> dict[str, Any]:
        tables = {
            "projects": "projects",
            "datasets": "datasets",
            "runs": "analysis_runs",
            "artifacts": "artifacts",
            "subscriptions": "webhook_subscriptions",
        }
        with self.connection() as connection:
            counts = {
                label: connection.execute(
                    f"SELECT count(*) AS n FROM {table}"
                ).fetchone()["n"]
                for label, table in tables.items()
            }
            rows = connection.execute(
                """
                SELECT payload
                FROM outbox_events
                WHERE event_type='analysis.completed'
                ORDER BY position
                """
            ).fetchall()
        return {
            "counts": counts,
            "outboundEvents": [row["payload"] for row in rows],
        }

    # ------------------------------------------------------------------
    # Durable jobs and lease fencing
    # ------------------------------------------------------------------
    def claim_job(
        self,
        worker_id: str,
        lease_seconds: int,
    ) -> ClaimedJob | None:
        with self.connection() as connection:
            with connection.transaction():
                row = connection.execute(
                    """
                    WITH candidate AS (
                        SELECT j.run_id
                        FROM run_jobs AS j
                        JOIN analysis_runs AS r ON r.id=j.run_id
                        WHERE j.status='queued'
                          AND j.available_at<=clock_timestamp()
                          AND r.status='queued'
                          AND r.cancellation_requested_at IS NULL
                        ORDER BY
                            (r.parameters->>'priority'='high') DESC,
                            j.created_at
                        FOR UPDATE OF j SKIP LOCKED
                        LIMIT 1
                    )
                    UPDATE run_jobs AS j
                    SET status='leased',
                        lease_owner=%s,
                        lease_expires_at=clock_timestamp()
                            + (%s || ' seconds')::interval,
                        lease_generation=lease_generation+1,
                        attempts=attempts+1,
                        updated_at=clock_timestamp()
                    FROM candidate AS c,
                         analysis_runs AS r,
                         datasets AS d
                    WHERE j.run_id=c.run_id
                      AND r.id=j.run_id
                      AND d.id=r.dataset_id
                    RETURNING
                        j.run_id,
                        r.dataset_id,
                        r.owner_id,
                        r.parameters->>'algorithm' AS algorithm,
                        d.source_kind,
                        d.source,
                        d.content_path,
                        d.checksum_sha256,
                        j.attempts,
                        j.lease_generation
                    """,
                    (worker_id, lease_seconds),
                ).fetchone()
        if not row:
            return None
        return ClaimedJob(
            run_id=row["run_id"],
            dataset_id=row["dataset_id"],
            owner_id=row["owner_id"],
            algorithm=row["algorithm"],
            source_kind=row["source_kind"],
            source=dict(row["source"]),
            content_path=row["content_path"],
            expected_checksum=row["checksum_sha256"],
            attempt=row["attempts"],
            lease_owner=worker_id,
            lease_generation=row["lease_generation"],
        )

    def _lock_job(
        self,
        connection: Connection[Row],
        job: ClaimedJob,
    ) -> Row:
        row = connection.execute(
            "SELECT * FROM run_jobs WHERE run_id=%s FOR UPDATE",
            (job.run_id,),
        ).fetchone()
        now = connection.execute(
            "SELECT clock_timestamp() AS now"
        ).fetchone()["now"]
        if (
            not row
            or row["status"] != "leased"
            or row["lease_owner"] != job.lease_owner
            or row["lease_generation"] != job.lease_generation
            or row["lease_expires_at"] <= now
        ):
            raise LeaseLost(job.run_id)
        return row

    def mark_job_running(self, job: ClaimedJob) -> None:
        with self.connection() as connection:
            with connection.transaction():
                self._lock_job(connection, job)
                run = connection.execute(
                    """
                    UPDATE analysis_runs
                    SET status='running',
                        progress=10,
                        updated_at=clock_timestamp()
                    WHERE id=%s AND status='queued'
                    RETURNING *
                    """,
                    (job.run_id,),
                ).fetchone()
                if not run:
                    raise LeaseLost(job.run_id)
                self._insert_run_event(
                    connection,
                    job.run_id,
                    job.owner_id,
                    "running",
                    10,
                )

    def renew_job_lease(
        self,
        job: ClaimedJob,
        lease_seconds: int,
    ) -> None:
        with self.connection() as connection:
            row = connection.execute(
                """
                UPDATE run_jobs
                SET lease_expires_at=clock_timestamp()
                        + (%s || ' seconds')::interval,
                    updated_at=clock_timestamp()
                WHERE run_id=%s
                  AND status='leased'
                  AND lease_owner=%s
                  AND lease_generation=%s
                  AND lease_expires_at>clock_timestamp()
                RETURNING run_id
                """,
                (
                    lease_seconds,
                    job.run_id,
                    job.lease_owner,
                    job.lease_generation,
                ),
            ).fetchone()
        if not row:
            raise LeaseLost(job.run_id)

    def _cancel_locked(
        self,
        connection: Connection[Row],
        job: ClaimedJob,
    ) -> None:
        canceled = connection.execute(
            """
            UPDATE analysis_runs
            SET status='canceled',
                completed_at=clock_timestamp(),
                updated_at=clock_timestamp()
            WHERE id=%s
            RETURNING *
            """,
            (job.run_id,),
        ).fetchone()
        connection.execute(
            """
            UPDATE run_jobs
            SET status='canceled',
                lease_owner=NULL,
                lease_expires_at=NULL,
                updated_at=clock_timestamp()
            WHERE run_id=%s
            """,
            (job.run_id,),
        )
        self._insert_run_event(
            connection,
            job.run_id,
            job.owner_id,
            "canceled",
            canceled["progress"],
        )

    def complete_job(
        self,
        job: ClaimedJob,
        artifact: StagedFile,
        storage_key: str,
        name: str,
        result_summary: dict[str, Any],
    ) -> bool:
        with self.connection() as connection:
            with connection.transaction():
                self._lock_job(connection, job)
                run = connection.execute(
                    "SELECT * FROM analysis_runs WHERE id=%s FOR UPDATE",
                    (job.run_id,),
                ).fetchone()
                if run["cancellation_requested_at"] is not None:
                    self._cancel_locked(connection, job)
                    return False
                if run["status"] != "running":
                    raise LeaseLost(job.run_id)

                existing = connection.execute(
                    """
                    SELECT *
                    FROM artifacts
                    WHERE run_id=%s AND name=%s
                    FOR UPDATE
                    """,
                    (job.run_id, name),
                ).fetchone()
                if (
                    existing
                    and existing["checksum_sha256"]
                    != artifact.checksum_sha256
                ):
                    raise RuntimeError(
                        "duplicate job produced different artifact bytes"
                    )
                artifact_row = existing
                if not artifact_row:
                    artifact_row = connection.execute(
                        """
                        INSERT INTO artifacts(
                            run_id,
                            owner_id,
                            name,
                            media_type,
                            size,
                            checksum_sha256,
                            storage_key
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING *
                        """,
                        (
                            job.run_id,
                            job.owner_id,
                            name,
                            artifact.media_type,
                            artifact.size,
                            artifact.checksum_sha256,
                            storage_key,
                        ),
                    ).fetchone()

                if self.exposes_api_1_2:
                    finished = connection.execute(
                        """
                        UPDATE analysis_runs
                        SET status='completed',
                            progress=100,
                            completed_at=clock_timestamp(),
                            updated_at=clock_timestamp(),
                            result_summary=%s::jsonb
                        WHERE id=%s
                        RETURNING *
                        """,
                        (json.dumps(result_summary), job.run_id),
                    ).fetchone()
                else:
                    finished = connection.execute(
                        """
                        UPDATE analysis_runs
                        SET status='completed',
                            progress=100,
                            completed_at=clock_timestamp(),
                            updated_at=clock_timestamp()
                        WHERE id=%s
                        RETURNING *
                        """,
                        (job.run_id,),
                    ).fetchone()

                connection.execute(
                    """
                    UPDATE run_jobs
                    SET status='completed',
                        lease_owner=NULL,
                        lease_expires_at=NULL,
                        updated_at=clock_timestamp()
                    WHERE run_id=%s
                    """,
                    (job.run_id,),
                )
                self._insert_run_event(
                    connection,
                    job.run_id,
                    job.owner_id,
                    "completed",
                    100,
                )

                run_body = self._run(
                    {
                        **finished,
                        "artifact_ids": [artifact_row["id"]],
                    }
                ).model_dump(by_alias=True, mode="json")
                self._insert_outbox_event(
                    connection,
                    "analysis.completed",
                    job.run_id,
                    job.owner_id,
                    {
                        "eventId": "pending",
                        "eventType": "analysis.completed",
                        "occurredAt": finished["completed_at"].isoformat(),
                        "run": run_body,
                    },
                )
                return True

    def fail_job(
        self,
        job: ClaimedJob,
        code: str,
        detail: str,
        retryable: bool,
    ) -> None:
        with self.connection() as connection:
            with connection.transaction():
                locked_job = self._lock_job(connection, job)
                run = connection.execute(
                    "SELECT * FROM analysis_runs WHERE id=%s FOR UPDATE",
                    (job.run_id,),
                ).fetchone()
                if run["cancellation_requested_at"] is not None:
                    self._cancel_locked(connection, job)
                    return

                if (
                    retryable
                    and locked_job["attempts"] < locked_job["max_attempts"]
                ):
                    connection.execute(
                        """
                        UPDATE run_jobs
                        SET status='queued',
                            available_at=clock_timestamp()
                                + (%s || ' seconds')::interval,
                            lease_owner=NULL,
                            lease_expires_at=NULL,
                            last_error=%s,
                            updated_at=clock_timestamp()
                        WHERE run_id=%s
                        """,
                        (
                            retry_delay_seconds(locked_job["attempts"]),
                            detail,
                            job.run_id,
                        ),
                    )
                    connection.execute(
                        """
                        UPDATE analysis_runs
                        SET status='queued',
                            progress=0,
                            updated_at=clock_timestamp()
                        WHERE id=%s
                        """,
                        (job.run_id,),
                    )
                    self._insert_run_event(
                        connection,
                        job.run_id,
                        job.owner_id,
                        "queued",
                        0,
                    )
                    return

                self._fail_run_locked(
                    connection,
                    job.run_id,
                    job.owner_id,
                    code,
                    detail,
                )

    def recover_expired_jobs(self) -> int:
        recovered = 0
        with self.connection() as connection:
            with connection.transaction():
                rows = connection.execute(
                    """
                    SELECT
                        j.*,
                        r.status AS run_status,
                        r.cancellation_requested_at,
                        r.owner_id,
                        r.progress
                    FROM run_jobs AS j
                    JOIN analysis_runs AS r ON r.id=j.run_id
                    WHERE j.status='leased'
                      AND j.lease_expires_at<clock_timestamp()
                    ORDER BY j.updated_at
                    FOR UPDATE OF j, r SKIP LOCKED
                    """
                ).fetchall()
                for row in rows:
                    if row["cancellation_requested_at"] is not None:
                        connection.execute(
                            """
                            UPDATE analysis_runs
                            SET status='canceled',
                                completed_at=clock_timestamp(),
                                updated_at=clock_timestamp()
                            WHERE id=%s
                            """,
                            (row["run_id"],),
                        )
                        connection.execute(
                            """
                            UPDATE run_jobs
                            SET status='canceled',
                                lease_owner=NULL,
                                lease_expires_at=NULL,
                                last_error='lease expired after cancellation',
                                updated_at=clock_timestamp()
                            WHERE run_id=%s
                            """,
                            (row["run_id"],),
                        )
                        self._insert_run_event(
                            connection,
                            row["run_id"],
                            row["owner_id"],
                            "canceled",
                            row["progress"],
                        )
                    elif row["attempts"] >= row["max_attempts"]:
                        self._fail_run_locked(
                            connection,
                            row["run_id"],
                            row["owner_id"],
                            "lease-exhausted",
                            "worker lease expired too many times",
                        )
                    else:
                        connection.execute(
                            """
                            UPDATE run_jobs
                            SET status='queued',
                                lease_owner=NULL,
                                lease_expires_at=NULL,
                                available_at=clock_timestamp(),
                                last_error='lease expired',
                                updated_at=clock_timestamp()
                            WHERE run_id=%s
                            """,
                            (row["run_id"],),
                        )
                        connection.execute(
                            """
                            UPDATE analysis_runs
                            SET status='queued',
                                progress=0,
                                updated_at=clock_timestamp()
                            WHERE id=%s AND status='running'
                            """,
                            (row["run_id"],),
                        )
                        self._insert_run_event(
                            connection,
                            row["run_id"],
                            row["owner_id"],
                            "queued",
                            0,
                        )
                    recovered += 1
        return recovered

    def _fail_run_locked(
        self,
        connection: Connection[Row],
        run_id: str,
        owner_id: str,
        code: str,
        detail: str,
    ) -> None:
        failed = connection.execute(
            """
            UPDATE analysis_runs
            SET status='failed',
                completed_at=clock_timestamp(),
                failure_code=%s,
                failure_detail=%s,
                updated_at=clock_timestamp()
            WHERE id=%s
            RETURNING *
            """,
            (code, detail, run_id),
        ).fetchone()
        connection.execute(
            """
            UPDATE run_jobs
            SET status='dead',
                lease_owner=NULL,
                lease_expires_at=NULL,
                last_error=%s,
                updated_at=clock_timestamp()
            WHERE run_id=%s
            """,
            (detail, run_id),
        )
        self._insert_run_event(
            connection,
            run_id,
            owner_id,
            "failed",
            failed["progress"],
        )
        self._insert_outbox_event(
            connection,
            "analysis.failed",
            run_id,
            owner_id,
            {
                "eventId": "pending",
                "eventType": "analysis.failed",
                "occurredAt": failed["completed_at"].isoformat(),
                "runId": run_id,
                "failureCode": code,
            },
        )

    @staticmethod
    def _insert_run_event(
        connection: Connection[Row],
        run_id: str,
        owner_id: str,
        status: str,
        progress: int,
    ) -> None:
        connection.execute(
            """
            INSERT INTO run_events(run_id, owner_id, status, progress)
            VALUES (%s, %s, %s, %s)
            """,
            (run_id, owner_id, status, progress),
        )

    @staticmethod
    def _insert_outbox_event(
        connection: Connection[Row],
        event_type: str,
        run_id: str,
        owner_id: str,
        payload: dict[str, Any],
    ) -> str:
        row = connection.execute(
            """
            INSERT INTO outbox_events(
                event_type,
                run_id,
                owner_id,
                payload
            )
            VALUES (%s, %s, %s, %s::jsonb)
            RETURNING event_id, occurred_at
            """,
            (event_type, run_id, owner_id, json.dumps(payload)),
        ).fetchone()
        payload["eventId"] = row["event_id"]
        payload["occurredAt"] = row["occurred_at"].isoformat()
        connection.execute(
            "UPDATE outbox_events SET payload=%s::jsonb WHERE event_id=%s",
            (json.dumps(payload), row["event_id"]),
        )
        return str(row["event_id"])

    # ------------------------------------------------------------------
    # Transactional outbox expansion and signed delivery leases
    # ------------------------------------------------------------------
    def expand_outbox(self) -> int:
        with self.connection() as connection:
            with connection.transaction():
                events = connection.execute(
                    """
                    SELECT *
                    FROM outbox_events
                    WHERE expanded_at IS NULL
                    ORDER BY position
                    FOR UPDATE SKIP LOCKED
                    LIMIT 20
                    """
                ).fetchall()
                for event in events:
                    # A per-run callback is defined by Course 1 as a completion
                    # callback.  Failure delivery is available through an
                    # explicit subscription, not through this callback URL.
                    if event["event_type"] == "analysis.completed":
                        run = connection.execute(
                            "SELECT callback_url FROM analysis_runs WHERE id=%s",
                            (event["run_id"],),
                        ).fetchone()
                        if run and run["callback_url"]:
                            connection.execute(
                                """
                                INSERT INTO webhook_deliveries(
                                    event_id,
                                    delivery_kind,
                                    target_url,
                                    status
                                )
                                VALUES (%s, 'callback', %s, 'pending')
                                ON CONFLICT DO NOTHING
                                """,
                                (event["event_id"], run["callback_url"]),
                            )

                    subscriptions = connection.execute(
                        """
                        SELECT id, target_url
                        FROM webhook_subscriptions
                        WHERE owner_id=%s
                          AND enabled
                          AND %s=ANY(event_types)
                        """,
                        (event["owner_id"], event["event_type"]),
                    ).fetchall()
                    for subscription in subscriptions:
                        connection.execute(
                            """
                            INSERT INTO webhook_deliveries(
                                event_id,
                                subscription_id,
                                delivery_kind,
                                target_url,
                                status
                            )
                            VALUES (%s, %s, 'subscription', %s, 'pending')
                            ON CONFLICT DO NOTHING
                            """,
                            (
                                event["event_id"],
                                subscription["id"],
                                subscription["target_url"],
                            ),
                        )
                    connection.execute(
                        """
                        UPDATE outbox_events
                        SET expanded_at=clock_timestamp()
                        WHERE event_id=%s
                        """,
                        (event["event_id"],),
                    )
                return len(events)

    def claim_delivery(
        self,
        worker_id: str,
        lease_seconds: int,
    ) -> ClaimedDelivery | None:
        with self.connection() as connection:
            with connection.transaction():
                row = connection.execute(
                    """
                    WITH candidate AS (
                        SELECT id
                        FROM webhook_deliveries
                        WHERE status='pending'
                          AND available_at<=clock_timestamp()
                        ORDER BY position
                        FOR UPDATE SKIP LOCKED
                        LIMIT 1
                    )
                    UPDATE webhook_deliveries AS d
                    SET status='leased',
                        lease_owner=%s,
                        lease_expires_at=clock_timestamp()
                            + (%s || ' seconds')::interval,
                        lease_generation=lease_generation+1,
                        attempts=attempts+1,
                        updated_at=clock_timestamp()
                    FROM candidate AS c,
                         outbox_events AS o
                    WHERE d.id=c.id
                      AND o.event_id=d.event_id
                    RETURNING
                        d.id,
                        d.event_id,
                        d.delivery_kind,
                        d.target_url,
                        d.attempts,
                        d.lease_generation,
                        o.payload,
                        CASE
                            WHEN d.subscription_id IS NULL THEN %s
                            ELSE (
                                SELECT pgp_sym_decrypt(
                                    secret_ciphertext,
                                    %s
                                )
                                FROM webhook_subscriptions AS s
                                WHERE s.id=d.subscription_id
                            )
                        END AS secret
                    """,
                    (
                        worker_id,
                        lease_seconds,
                        self.callback_signing_secret,
                        self.encryption_key,
                    ),
                ).fetchone()
        if not row:
            return None
        return ClaimedDelivery(
            delivery_id=row["id"],
            event_id=row["event_id"],
            delivery_kind=row["delivery_kind"],
            target_url=row["target_url"],
            payload=dict(row["payload"]),
            secret=row["secret"],
            attempt=row["attempts"],
            lease_owner=worker_id,
            lease_generation=row["lease_generation"],
        )

    @staticmethod
    def _delivery_identity(
        delivery: ClaimedDelivery,
    ) -> tuple[str, str, int]:
        return (
            delivery.delivery_id,
            delivery.lease_owner,
            delivery.lease_generation,
        )

    def record_delivery_success(
        self,
        delivery: ClaimedDelivery,
        status: int,
    ) -> None:
        with self.connection() as connection:
            row = connection.execute(
                """
                UPDATE webhook_deliveries
                SET status='delivered',
                    delivered_at=clock_timestamp(),
                    response_status=%s,
                    lease_owner=NULL,
                    lease_expires_at=NULL,
                    updated_at=clock_timestamp()
                WHERE id=%s
                  AND status='leased'
                  AND lease_owner=%s
                  AND lease_generation=%s
                RETURNING id
                """,
                (status, *self._delivery_identity(delivery)),
            ).fetchone()
        if not row:
            raise LeaseLost(delivery.delivery_id)

    def record_delivery_failure(
        self,
        delivery: ClaimedDelivery,
        error: str,
        retryable: bool,
    ) -> None:
        with self.connection() as connection:
            with connection.transaction():
                row = connection.execute(
                    """
                    SELECT *
                    FROM webhook_deliveries
                    WHERE id=%s
                      AND status='leased'
                      AND lease_owner=%s
                      AND lease_generation=%s
                    FOR UPDATE
                    """,
                    self._delivery_identity(delivery),
                ).fetchone()
                if not row:
                    raise LeaseLost(delivery.delivery_id)
                if retryable and row["attempts"] < row["max_attempts"]:
                    connection.execute(
                        """
                        UPDATE webhook_deliveries
                        SET status='pending',
                            available_at=clock_timestamp()
                                + (%s || ' seconds')::interval,
                            lease_owner=NULL,
                            lease_expires_at=NULL,
                            last_error=%s,
                            updated_at=clock_timestamp()
                        WHERE id=%s
                        """,
                        (
                            retry_delay_seconds(row["attempts"]),
                            error,
                            delivery.delivery_id,
                        ),
                    )
                else:
                    connection.execute(
                        """
                        UPDATE webhook_deliveries
                        SET status='dead',
                            lease_owner=NULL,
                            lease_expires_at=NULL,
                            last_error=%s,
                            updated_at=clock_timestamp()
                        WHERE id=%s
                        """,
                        (error, delivery.delivery_id),
                    )

    def recover_expired_deliveries(self) -> int:
        recovered = 0
        with self.connection() as connection:
            with connection.transaction():
                rows = connection.execute(
                    """
                    SELECT *
                    FROM webhook_deliveries
                    WHERE status='leased'
                      AND lease_expires_at<clock_timestamp()
                    ORDER BY position
                    FOR UPDATE SKIP LOCKED
                    """
                ).fetchall()
                for row in rows:
                    if row["attempts"] >= row["max_attempts"]:
                        connection.execute(
                            """
                            UPDATE webhook_deliveries
                            SET status='dead',
                                lease_owner=NULL,
                                lease_expires_at=NULL,
                                last_error='lease expired after final attempt',
                                updated_at=clock_timestamp()
                            WHERE id=%s
                            """,
                            (row["id"],),
                        )
                    else:
                        connection.execute(
                            """
                            UPDATE webhook_deliveries
                            SET status='pending',
                                lease_owner=NULL,
                                lease_expires_at=NULL,
                                available_at=clock_timestamp(),
                                last_error='lease expired',
                                updated_at=clock_timestamp()
                            WHERE id=%s
                            """,
                            (row["id"],),
                        )
                    recovered += 1
        return recovered


def _not_found(resource: str) -> ServiceError:
    return ServiceError(
        404,
        "Resource not found",
        f"The requested {resource} does not exist.",
        "not-found",
    )
