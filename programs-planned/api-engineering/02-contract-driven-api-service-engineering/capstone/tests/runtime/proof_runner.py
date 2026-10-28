#!/usr/bin/env python3
"""Black-box and durable proof runner for the Analysis Runs capstone.

The runner deliberately fails when a live prerequisite is unavailable. Static/core
proof is provided elsewhere; this file owns claims that require a live HTTP
provider, PostgreSQL, processes, files, or the controlled receiver.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import random
import string
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

COURSE = Path(__file__).resolve().parents[3]
CAPSTONE = COURSE / "capstone"
REPORTS = CAPSTONE / "reports"
COMPOSE = CAPSTONE / "compose.yaml"


class ProofFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class Track:
    name: str
    api_base: str
    database_url: str
    worker_service: str
    api_service: str


def track_config(name: str) -> Track:
    if name == "python":
        return Track(
            name="python",
            api_base=os.getenv("PYTHON_API_BASE", "http://127.0.0.1:58000"),
            database_url=os.getenv(
                "PYTHON_TEST_DATABASE_URL",
                "postgresql://analysis:analysis@127.0.0.1:55432/analysis_python",
            ),
            worker_service="python-worker",
            api_service="python-api",
        )
    if name == "typescript":
        return Track(
            name="typescript",
            api_base=os.getenv("TYPESCRIPT_API_BASE", "http://127.0.0.1:58001"),
            database_url=os.getenv(
                "TYPESCRIPT_TEST_DATABASE_URL",
                "postgresql://analysis:analysis@127.0.0.1:55432/analysis_typescript",
            ),
            worker_service="typescript-worker",
            api_service="typescript-api",
        )
    raise ProofFailure("track must be python or typescript")


@dataclass
class Response:
    status: int
    headers: dict[str, str]
    body: bytes

    def json(self) -> Any:
        if not self.body:
            return None
        try:
            return json.loads(self.body)
        except json.JSONDecodeError as exc:
            raise ProofFailure(
                f"expected JSON from status {self.status}, received {self.body[:200]!r}"
            ) from exc

    def header(self, name: str) -> str | None:
        return self.headers.get(name.lower())


class HttpClient:
    def __init__(self, base: str, token: str = "learner-write"):
        self.base = base.rstrip("/")
        self.token = token

    def request(
        self,
        method: str,
        path: str,
        *,
        body: bytes | None = None,
        json_body: Any | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        timeout: float = 20.0,
        authenticate: bool = True,
    ) -> Response:
        request_headers = {"Accept": "application/json"}
        if authenticate:
            request_headers["Authorization"] = f"Bearer {token or self.token}"
        if headers:
            request_headers.update(headers)
        if json_body is not None:
            body = json.dumps(json_body, separators=(",", ":")).encode()
            request_headers["Content-Type"] = "application/json"
        target = self.base + path
        request = urllib.request.Request(target, data=body, headers=request_headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return Response(
                    response.status,
                    {k.lower(): v for k, v in response.headers.items()},
                    response.read(),
                )
        except urllib.error.HTTPError as error:
            return Response(
                error.code,
                {k.lower(): v for k, v in error.headers.items()},
                error.read(),
            )
        except Exception as exc:
            raise ProofFailure(f"HTTP {method} {target} failed: {exc}") from exc

    def get(self, path: str, **kwargs: Any) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self.request("DELETE", path, **kwargs)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProofFailure(message)


def require_status(response: Response, expected: int | Iterable[int], label: str) -> None:
    expected_set = {expected} if isinstance(expected, int) else set(expected)
    if response.status not in expected_set:
        detail = response.body[:800].decode(errors="replace")
        raise ProofFailure(
            f"{label}: expected status {sorted(expected_set)}, got {response.status}: {detail}"
        )


def unique(prefix: str) -> str:
    stamp = int(time.time() * 1000) % 10_000_000
    salt = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{prefix}-{stamp}-{salt}"


def auth_headers(token: str = "learner-write") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def multipart_file(
    content: bytes,
    *,
    filename: str = "fixture.csv",
    media_type: str = "text/csv",
    description: str | None = None,
) -> tuple[bytes, str]:
    boundary = "cdse-" + hashlib.sha256(os.urandom(16)).hexdigest()[:24]
    chunks: list[bytes] = []
    if description is not None:
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                b'Content-Disposition: form-data; name="description"\r\n\r\n',
                description.encode(),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode(),
            f"Content-Type: {media_type}\r\n\r\n".encode(),
            content,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def psycopg_modules():
    try:
        import psycopg  # type: ignore
        from psycopg.rows import dict_row  # type: ignore
    except Exception as exc:
        raise ProofFailure(
            "live PostgreSQL proof requires psycopg 3; install the selected Python proof dependencies"
        ) from exc
    return psycopg, dict_row


class Database:
    def __init__(self, url: str):
        self.url = url
        self.psycopg, self.dict_row = psycopg_modules()

    def connection(self, *, autocommit: bool = False):
        return self.psycopg.connect(self.url, autocommit=autocommit, row_factory=self.dict_row)

    def one(self, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
        with self.connection() as connection:
            row = connection.execute(sql, params).fetchone()
        if row is None:
            raise ProofFailure(f"query returned no row: {sql}")
        return dict(row)

    def all(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        with self.connection() as connection:
            return [dict(row) for row in connection.execute(sql, params).fetchall()]

    def scalar(self, sql: str, params: tuple[Any, ...] = ()) -> Any:
        row = self.one(sql, params)
        return next(iter(row.values()))


def report(name: str, track: Track, release: str, claims: dict[str, Any], limitations: list[str] | None = None) -> dict[str, Any]:
    payload = {
        "name": name,
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "status": "passed",
        "track": track.name,
        "release": release,
        "apiBase": track.api_base,
        "claims": claims,
        "limitations": limitations or [
            "single local PostgreSQL primary",
            "controlled local process and receiver topology",
        ],
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"{track.name}-{name}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def wait_for_health(track: Track, timeout: float = 120.0) -> dict[str, Any]:
    client = HttpClient(track.api_base)
    deadline = time.monotonic() + timeout
    last: str | None = None
    while time.monotonic() < deadline:
        try:
            response = client.get("/health", authenticate=False, timeout=3)
            if response.status == 200:
                return response.json()
            last = f"status {response.status}"
        except Exception as exc:
            last = str(exc)
        time.sleep(0.5)
    raise ProofFailure(f"provider did not become healthy within {timeout}s: {last}")


def create_project(client: HttpClient, name: str | None = None) -> tuple[dict[str, Any], str]:
    response = client.post(
        "/projects",
        json_body={"name": name or unique("project"), "description": "proof fixture"},
    )
    require_status(response, 201, "create project")
    body = response.json()
    etag = response.header("etag")
    require(isinstance(etag, str) and etag.startswith('"'), "create project omitted ETag")
    require(response.header("location") == f"/projects/{body['id']}", "project Location mismatch")
    return body, etag


def create_remote_dataset(client: HttpClient, project_id: str, name: str | None = None) -> dict[str, Any]:
    response = client.post(
        f"/projects/{project_id}/datasets",
        json_body={
            "name": name or unique("remote-dataset"),
            "source": {
                "kind": "remote-object",
                "uri": "https://objects.example.test/remote-dataset.json",
            },
        },
    )
    require_status(response, 201, "create remote dataset")
    body = response.json()
    require(body["status"] == "ready", "remote fixture dataset is not ready")
    return body


def create_local_dataset(client: HttpClient, project_id: str, name: str | None = None) -> dict[str, Any]:
    response = client.post(
        f"/projects/{project_id}/datasets",
        json_body={
            "name": name or unique("local-dataset"),
            "source": {
                "kind": "local-file",
                "fileName": "fixture.csv",
                "mediaType": "text/csv",
            },
        },
    )
    require_status(response, 201, "create local dataset")
    body = response.json()
    require(body["status"] == "awaiting-upload", "local dataset should await upload")
    return body


def upload_dataset(client: HttpClient, dataset_id: str, content: bytes) -> dict[str, Any]:
    body, content_type = multipart_file(content)
    response = client.post(
        f"/datasets/{dataset_id}/content",
        body=body,
        headers={"Content-Type": content_type, "Accept": "application/json"},
        timeout=30,
    )
    require_status(response, 201, "upload dataset content")
    receipt = response.json()
    require(receipt["contentLength"] == len(content), "upload receipt length mismatch")
    require(receipt["checksumSha256"] == hashlib.sha256(content).hexdigest(), "upload checksum mismatch")
    return receipt


def run_body(project_id: str, dataset_id: str, *, priority: str = "normal", callback: str | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "projectId": project_id,
        "datasetId": dataset_id,
        "parameters": {
            "algorithm": "line-count",
            "priority": priority,
            "labels": {"proof": "runtime"},
        },
    }
    if callback is not None:
        body["callbackUrl"] = callback
    return body


def create_run(
    client: HttpClient,
    project_id: str,
    dataset_id: str,
    key: str,
    *,
    priority: str = "normal",
    callback: str | None = None,
) -> Response:
    return client.post(
        "/analysis-runs",
        json_body=run_body(project_id, dataset_id, priority=priority, callback=callback),
        headers={"Idempotency-Key": key},
        timeout=30,
    )


def wait_for_run(client: HttpClient, run_id: str, timeout: float = 90.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        response = client.get(f"/analysis-runs/{run_id}")
        require_status(response, 200, "get run while waiting")
        last = response.json()
        if last["status"] in {"completed", "failed", "canceled"}:
            return last
        time.sleep(0.25)
    raise ProofFailure(f"run {run_id} did not become terminal; last={last}")


def wait_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    health = wait_for_health(track, args.timeout)
    return report("wait", track, args.release, {"health": health})


def smoke_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    health = wait_for_health(track, 20)
    client = HttpClient(track.api_base)
    unauthenticated = client.get("/projects", authenticate=False)
    require_status(unauthenticated, 401, "unauthenticated project list")
    require("application/problem+json" in (unauthenticated.header("content-type") or ""), "401 is not problem+json")
    read_only = client.post("/projects", token="learner-read", json_body={"name": "forbidden"})
    require_status(read_only, 403, "read-only create")
    request_id = unauthenticated.header("x-request-id")
    require(bool(request_id and request_id.startswith("req_")), "response omitted stable request ID")
    return report(
        "smoke-proof",
        track,
        args.release,
        {
            "health": health,
            "unauthenticatedStatus": unauthenticated.status,
            "insufficientScopeStatus": read_only.status,
            "requestId": request_id,
        },
    )


def postgres_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    database = Database(track.database_url)
    version = int(database.scalar("SELECT current_setting('server_version_num')::int AS version"))
    require(version >= 180000, f"PostgreSQL 18 or later required, found {version}")
    migrations = database.all("SELECT version,checksum_sha256 FROM schema_migrations ORDER BY version")
    expected = {"001_base.sql", "002_indexes.sql"}
    require(expected.issubset({row["version"] for row in migrations}), "baseline migrations are missing")
    tables = set(
        row["table_name"]
        for row in database.all(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        )
    )
    required_tables = {
        "projects",
        "datasets",
        "analysis_runs",
        "idempotency_records",
        "pagination_cursors",
        "run_jobs",
        "run_events",
        "artifacts",
        "outbox_events",
        "webhook_deliveries",
    }
    require(required_tables.issubset(tables), f"schema missing tables: {sorted(required_tables - tables)}")

    invalid_sqlstate = None
    psycopg, _ = psycopg_modules()
    try:
        with database.connection() as connection:
            with connection.transaction():
                connection.execute(
                    "INSERT INTO projects(owner_id,name) VALUES(%s,%s)",
                    ("x", "invalid owner"),
                )
    except psycopg.Error as exc:  # type: ignore[attr-defined]
        invalid_sqlstate = exc.sqlstate
    require(invalid_sqlstate == "23514", f"database check constraint did not reject invalid owner: {invalid_sqlstate}")

    client = HttpClient(track.api_base)
    project, _ = create_project(client, unique("persistent-project"))
    row = database.one("SELECT id,owner_id,version FROM projects WHERE id=%s", (project["id"],))
    require(row["owner_id"] == "learner" and row["version"] == 1, "HTTP create did not persist expected row")
    return report(
        "postgres-proof",
        track,
        args.release,
        {
            "serverVersionNum": version,
            "migrations": [row["version"] for row in migrations],
            "requiredTables": len(required_tables),
            "invalidRowSqlstate": invalid_sqlstate,
            "persistedProject": project["id"],
        },
    )


def conformance_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    client = HttpClient(track.api_base)

    project, etag = create_project(client)
    project_id = project["id"]

    get_response = client.get(f"/projects/{project_id}")
    require_status(get_response, 200, "get project")
    require(get_response.header("etag") == etag, "GET project ETag differs from create")

    hidden = client.get(f"/projects/{project_id}", token="other-owner")
    require_status(hidden, 404, "cross-owner project concealment")

    missing_precondition = client.patch(
        f"/projects/{project_id}", json_body={"name": unique("no-precondition")}
    )
    require_status(missing_precondition, 428, "missing If-Match")

    updated = client.patch(
        f"/projects/{project_id}",
        json_body={"name": unique("updated")},
        headers={"If-Match": etag},
    )
    require_status(updated, 200, "conditional project update")
    new_etag = updated.header("etag")
    require(new_etag and new_etag != etag, "project update did not advance ETag")

    stale = client.patch(
        f"/projects/{project_id}",
        json_body={"name": unique("stale")},
        headers={"If-Match": etag},
    )
    require_status(stale, 412, "stale project update")

    dataset = create_remote_dataset(client, project_id)
    dataset_id = dataset["id"]
    listed_datasets = client.get(f"/projects/{project_id}/datasets?limit=20")
    require_status(listed_datasets, 200, "list datasets")
    require(any(item["id"] == dataset_id for item in listed_datasets.json()["items"]), "created dataset missing from list")

    subscription = client.post(
        "/webhook-subscriptions",
        json_body={
            "targetUrl": "https://hooks.example.test/proof",
            "eventTypes": ["analysis.completed"],
            "secret": "course-callback-signing-secret",
        },
    )
    require_status(subscription, 201, "create webhook subscription")
    require("secret" not in subscription.json(), "subscription response leaked secret")

    key = unique("conformance-idempotency-key")[:64]
    first = create_run(client, project_id, dataset_id, key)
    require_status(first, 202, "create analysis run")
    first_body = first.json()
    run_id = first_body["id"]
    require(first.header("location") == f"/analysis-runs/{run_id}", "run Location mismatch")
    require(first.header("idempotent-replay") == "false", "first create incorrectly marked replay")

    replay = create_run(client, project_id, dataset_id, key)
    require_status(replay, 202, "idempotent replay")
    require(replay.header("idempotent-replay") == "true", "replay header missing")
    require(replay.json() == first_body, "replay did not return exact stored response body")

    changed = create_run(client, project_id, dataset_id, key, priority="high")
    require_status(changed, 409, "changed-body key reuse")

    terminal = wait_for_run(client, run_id)
    require(terminal["status"] == "completed", f"analysis did not complete: {terminal}")

    run_list = client.get("/analysis-runs?limit=20&status=completed")
    require_status(run_list, 200, "list completed runs")
    require(any(item["id"] == run_id for item in run_list.json()["items"]), "completed run missing from list")

    events = client.get(
        f"/analysis-runs/{run_id}/events",
        headers={"Accept": "application/x-ndjson"},
        timeout=30,
    )
    require_status(events, 200, "NDJSON events")
    lines = [json.loads(line) for line in events.body.splitlines() if line.strip()]
    require(lines and lines[-1]["status"] == "completed", "event stream omitted terminal event")

    artifacts = client.get(f"/analysis-runs/{run_id}/artifacts")
    require_status(artifacts, 200, "list artifacts")
    artifact_items = artifacts.json()["items"]
    require(len(artifact_items) == 1, f"expected one artifact, got {len(artifact_items)}")
    artifact_id = artifact_items[0]["id"]
    artifact = client.get(f"/artifacts/{artifact_id}")
    require_status(artifact, 200, "get artifact metadata")

    local = create_local_dataset(client, project_id, unique("deletable"))
    deleted = client.delete(f"/datasets/{local['id']}")
    require_status(deleted, 204, "delete unused dataset")
    gone = client.get(f"/datasets/{local['id']}")
    require_status(gone, 404, "deleted dataset visibility")

    diagnostics = client.get("/internal/diagnostics", token="admin")
    require_status(diagnostics, 200, "internal diagnostics")

    return report(
        "conformance-proof",
        track,
        args.release,
        {
            "project": project_id,
            "dataset": dataset_id,
            "run": run_id,
            "artifact": artifact_id,
            "eventCount": len(lines),
            "idempotentReplayExact": True,
            "crossOwnerConcealed": True,
            "problemStatuses": [403, 404, 409, 412, 428],
        },
    )


def concurrency_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    client = HttpClient(track.api_base)
    database = Database(track.database_url)
    project, etag = create_project(client, unique("concurrent-project"))
    dataset = create_remote_dataset(client, project["id"], unique("concurrent-dataset"))
    key = unique("concurrency-idempotency-key")[:64]

    def submit(_: int) -> Response:
        return create_run(client, project["id"], dataset["id"], key)

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        responses = list(executor.map(submit, range(args.actors)))
    for index, response in enumerate(responses):
        require_status(response, 202, f"concurrent create {index}")
    ids = {response.json()["id"] for response in responses}
    require(len(ids) == 1, f"concurrent idempotency created multiple run IDs: {sorted(ids)}")
    run_id = next(iter(ids))
    replay_flags = [response.header("idempotent-replay") for response in responses]
    require(replay_flags.count("false") == 1, f"expected one original response, got {replay_flags.count('false')}")

    counts = database.one(
        """SELECT
          (SELECT count(*) FROM analysis_runs WHERE id=%s) AS runs,
          (SELECT count(*) FROM idempotency_records WHERE owner_id='learner' AND operation_id='createAnalysisRun' AND idempotency_key=%s) AS records,
          (SELECT count(*) FROM run_jobs WHERE run_id=%s) AS jobs,
          (SELECT count(*) FROM run_events WHERE run_id=%s AND status='queued') AS queued_events""",
        (run_id, key, run_id, run_id),
    )
    require(counts == {"runs": 1, "records": 1, "jobs": 1, "queued_events": 1}, f"durable idempotency cardinality mismatch: {counts}")

    names = [unique("etag-a"), unique("etag-b")]

    def patch(name: str) -> Response:
        return client.patch(
            f"/projects/{project['id']}",
            json_body={"name": name},
            headers={"If-Match": etag},
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        patch_responses = list(executor.map(patch, names))
    statuses = sorted(response.status for response in patch_responses)
    require(statuses == [200, 412], f"ETag race did not produce one winner: {statuses}")
    durable_project = database.one(
        "SELECT name,version FROM projects WHERE id=%s AND owner_id='learner'", (project["id"],)
    )
    require(durable_project["version"] == 2, f"project version advanced incorrectly: {durable_project}")
    require(durable_project["name"] in names, "project winner is not one submitted value")

    changed = create_run(client, project["id"], dataset["id"], key, priority="high")
    require_status(changed, 409, "post-storm changed-body key reuse")

    return report(
        "concurrency-proof",
        track,
        args.release,
        {
            "actors": args.actors,
            "uniqueRunIds": len(ids),
            "durableCardinality": counts,
            "etagStatuses": statuses,
            "projectVersion": durable_project["version"],
        },
    )


def query_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    client = HttpClient(track.api_base)
    database = Database(track.database_url)
    marker = unique("page-marker")
    created: list[str] = []
    for index in range(args.rows):
        project, _ = create_project(client, f"{marker}-{index:03d}")
        created.append(project["id"])

    seen: list[str] = []
    cursor: str | None = None
    first_cursor: str | None = None
    while True:
        query = {"limit": "17", "name": marker}
        if cursor is not None:
            query["cursor"] = cursor
        response = client.get("/projects?" + urllib.parse.urlencode(query))
        require_status(response, 200, "paged project query")
        body = response.json()
        page_ids = [item["id"] for item in body["items"]]
        require(not (set(page_ids) & set(seen)), "pagination duplicated an item")
        seen.extend(page_ids)
        cursor = body.get("nextCursor")
        first_cursor = first_cursor or cursor
        if cursor is None:
            break
    require(seen == created, f"pagination order/coverage mismatch: expected {len(created)}, got {len(seen)}")
    require(first_cursor is not None, "fixture did not create a continuation cursor")

    wrong_filter = client.get(
        "/projects?" + urllib.parse.urlencode({"limit": 17, "name": marker + "-changed", "cursor": first_cursor})
    )
    require_status(wrong_filter, 422, "cursor replay under changed filter")
    wrong_owner = client.get(
        "/projects?" + urllib.parse.urlencode({"limit": 17, "name": marker, "cursor": first_cursor}),
        token="other-owner",
    )
    require_status(wrong_owner, 422, "cursor replay under another principal")

    plan = database.one(
        "EXPLAIN (FORMAT JSON) SELECT * FROM projects WHERE owner_id=%s AND position>%s ORDER BY position LIMIT 18",
        ("learner", 0),
    )
    plan_json = next(iter(plan.values()))
    cursor_rows = database.scalar(
        "SELECT count(*) FROM pagination_cursors WHERE owner_id='learner' AND operation_id='listProjects'"
    )
    return report(
        "query-proof",
        track,
        args.release,
        {
            "created": len(created),
            "seen": len(seen),
            "unique": len(set(seen)),
            "filterBoundStatus": wrong_filter.status,
            "principalBoundStatus": wrong_owner.status,
            "cursorRows": cursor_rows,
            "planCaptured": bool(plan_json),
        },
        limitations=[
            "forward keyset traversal, not a multi-request snapshot",
            "query plan captured at course fixture cardinality",
        ],
    )


def compose(track: Track, *arguments: str, release: str = "1.0", check: bool = True) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["SERVICE_RELEASE"] = release
    environment["MIGRATION_TARGET"] = "005" if release == "1.1" else "002"
    command = [
        "docker",
        "compose",
        "-f",
        str(COMPOSE),
        "--profile",
        track.name,
        *arguments,
    ]
    try:
        return subprocess.run(command, cwd=CAPSTONE, env=environment, text=True, check=check, capture_output=True)
    except FileNotFoundError as exc:
        raise ProofFailure("Docker Compose is required for process proof") from exc
    except subprocess.CalledProcessError as exc:
        raise ProofFailure(
            f"compose command failed: {' '.join(command)}\nstdout={exc.stdout}\nstderr={exc.stderr}"
        ) from exc


def wait_database_job(database: Database, run_id: str, status: str, timeout: float = 20.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        rows = database.all(
            "SELECT run_id,status,lease_owner,lease_generation,lease_expires_at,attempts FROM run_jobs WHERE run_id=%s",
            (run_id,),
        )
        if rows and rows[0]["status"] == status:
            return rows[0]
        time.sleep(0.1)
    raise ProofFailure(f"job {run_id} did not reach status {status}")


def recovery_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    database = Database(track.database_url)
    client = HttpClient(track.api_base)

    # Stop the real worker so the controlled claimant can own the first generation.
    compose(track, "stop", track.worker_service, release=args.release)
    project, _ = create_project(client, unique("recovery-project"))
    dataset = create_remote_dataset(client, project["id"], unique("recovery-dataset"))
    key = unique("recovery-idempotency-key")[:64]
    response = create_run(client, project["id"], dataset["id"], key)
    require_status(response, 202, "create queued recovery run")
    run_id = response.json()["id"]
    wait_database_job(database, run_id, "queued")

    claimant = CAPSTONE / "tests" / "failure" / "lease_claim_process.py"
    process = subprocess.Popen(
        [sys.executable, "-u", str(claimant), "--database-url", track.database_url, "--run-id", run_id, "--lease-seconds", "5"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        line = process.stdout.readline() if process.stdout else ""
        require(bool(line), f"controlled claimant did not report a claim: {process.stderr.read() if process.stderr else ''}")
        claim = json.loads(line)
        require(claim["runId"] == run_id and claim["generation"] >= 1, f"invalid claim: {claim}")
        process.kill()
        process.wait(timeout=10)
    finally:
        if process.poll() is None:
            process.kill()

    leased = wait_database_job(database, run_id, "leased")
    require(leased["lease_generation"] == claim["generation"], "database generation differs from claimant")
    time.sleep(5.5)
    compose(track, "up", "-d", track.worker_service, release=args.release)
    terminal = wait_for_run(client, run_id, timeout=90)
    require(terminal["status"] == "completed", f"recovered run did not complete: {terminal}")

    final_job = database.one(
        "SELECT status,lease_generation,attempts FROM run_jobs WHERE run_id=%s", (run_id,)
    )
    require(final_job["status"] == "completed", f"job not completed after recovery: {final_job}")
    require(final_job["lease_generation"] > claim["generation"], "recovery did not issue a higher generation")

    with database.connection() as connection:
        stale = connection.execute(
            """UPDATE run_jobs SET last_error='stale write accepted'
               WHERE run_id=%s AND status='leased' AND lease_owner=%s AND lease_generation=%s""",
            (run_id, "proof-crashed-worker", claim["generation"]),
        )
        stale_count = stale.rowcount
    require(stale_count == 0, "stale generation was able to mutate the recovered job")

    artifacts = int(database.scalar("SELECT count(*) FROM artifacts WHERE run_id=%s", (run_id,)))
    terminal_events = int(
        database.scalar(
            "SELECT count(*) FROM run_events WHERE run_id=%s AND status IN ('completed','failed','canceled')",
            (run_id,),
        )
    )
    require(artifacts == 1 and terminal_events == 1, f"duplicate terminal effects: artifacts={artifacts}, events={terminal_events}")

    return report(
        "recovery-proof",
        track,
        args.release,
        {
            "run": run_id,
            "crashedGeneration": claim["generation"],
            "finalGeneration": final_job["lease_generation"],
            "attempts": final_job["attempts"],
            "staleWriteRows": stale_count,
            "artifactCount": artifacts,
            "terminalEventCount": terminal_events,
        },
    )


def artifact_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    client = HttpClient(track.api_base)
    database = Database(track.database_url)
    project, _ = create_project(client, unique("artifact-project"))
    dataset = create_local_dataset(client, project["id"], unique("artifact-dataset"))

    exact = (b"row,value\n" * 104858)[:1_048_576]
    receipt = upload_dataset(client, dataset["id"], exact)
    repeated = upload_dataset(client, dataset["id"], exact)
    require(repeated["checksumSha256"] == receipt["checksumSha256"], "same-content upload was not idempotent")

    too_large_dataset = create_local_dataset(client, project["id"], unique("too-large"))
    body, content_type = multipart_file(b"x" * 1_048_577)
    too_large = client.post(
        f"/datasets/{too_large_dataset['id']}/content",
        body=body,
        headers={"Content-Type": content_type},
        timeout=30,
    )
    require_status(too_large, 413, "limit plus one upload")
    row = database.one(
        "SELECT status,content_path,content_length FROM datasets WHERE id=%s", (too_large_dataset["id"],)
    )
    require(row["status"] == "awaiting-upload" and row["content_path"] is None, "oversize upload changed dataset state")

    key = unique("artifact-run-idempotency")[:64]
    run = create_run(client, project["id"], dataset["id"], key)
    require_status(run, 202, "create artifact run")
    terminal = wait_for_run(client, run.json()["id"])
    require(terminal["status"] == "completed", "artifact run failed")
    items = client.get(f"/analysis-runs/{terminal['id']}/artifacts").json()["items"]
    require(len(items) == 1, "analysis did not publish exactly one artifact")
    artifact = items[0]
    durable = database.one(
        "SELECT storage_key,size,checksum_sha256 FROM artifacts WHERE id=%s", (artifact["id"],)
    )
    require(durable["checksum_sha256"] == artifact["checksumSha256"], "artifact metadata checksum drift")

    download_claim: dict[str, Any]
    if args.release == "1.1":
        download = client.get(f"/artifacts/{artifact['id']}/content")
        require_status(download, 200, "artifact content download")
        require(hashlib.sha256(download.body).hexdigest() == artifact["checksumSha256"], "download checksum mismatch")
        conditional = client.get(
            f"/artifacts/{artifact['id']}/content",
            headers={"If-None-Match": f'"sha256:{artifact["checksumSha256"]}"'},
        )
        require_status(conditional, 304, "conditional artifact download")
        download_claim = {"executed": True, "bytes": len(download.body), "conditionalStatus": 304}
    else:
        download_claim = {
            "executed": False,
            "reason": "artifact content route is introduced by the explicit service 1.1 release",
        }

    staging_count = int(
        database.scalar(
            "SELECT count(*) FROM datasets WHERE id=%s AND content_path IS NOT NULL",
            (too_large_dataset["id"],),
        )
    )
    require(staging_count == 0, "oversize dataset received published metadata")

    return report(
        "artifact-proof",
        track,
        args.release,
        {
            "exactUploadBytes": len(exact),
            "uploadChecksum": receipt["checksumSha256"],
            "limitPlusOneStatus": too_large.status,
            "oversizePublishedRows": staging_count,
            "artifact": artifact["id"],
            "artifactStorageKey": durable["storage_key"],
            "download": download_claim,
        },
        limitations=[
            "filesystem adapter on one local volume",
            "tamper/orphan primitives are additionally covered by dependency-light adapter tests",
        ],
    )


def receiver_request(method: str, path: str = "/deliveries") -> Response:
    client = HttpClient(os.getenv("RECEIVER_BASE", "http://127.0.0.1:58080"))
    return client.request(method, path, authenticate=False)


def webhook_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    reset = receiver_request("DELETE")
    require_status(reset, 204, "reset controlled receiver")
    client = HttpClient(track.api_base)
    database = Database(track.database_url)
    project, _ = create_project(client, unique("webhook-project"))
    dataset = create_remote_dataset(client, project["id"], unique("webhook-dataset"))

    # The secret equals the receiver's course secret so subscription delivery can be verified.
    subscription = client.post(
        "/webhook-subscriptions",
        json_body={
            "targetUrl": "https://hooks.example.test/proof?fail_first=2",
            "eventTypes": ["analysis.completed"],
            "secret": "course-callback-signing-secret",
        },
    )
    require_status(subscription, 201, "create retry subscription")

    key = unique("webhook-idempotency")[:64]
    response = create_run(
        client,
        project["id"],
        dataset["id"],
        key,
        callback="https://hooks.example.test/callback",
    )
    require_status(response, 202, "create webhook run")
    run_id = response.json()["id"]
    terminal = wait_for_run(client, run_id)
    require(terminal["status"] == "completed", "webhook run did not complete")

    deadline = time.monotonic() + 90
    receipts: list[dict[str, Any]] = []
    while time.monotonic() < deadline:
        response = receiver_request("GET")
        require_status(response, 200, "receiver receipts")
        receipts = response.json()["items"]
        if len(receipts) >= 2:
            break
        time.sleep(0.5)
    require(len(receipts) >= 2, f"callback/subscription receipts did not arrive: {receipts}")

    events = database.all(
        "SELECT event_id,event_type,expanded_at FROM outbox_events WHERE run_id=%s", (run_id,)
    )
    require(len(events) == 1 and events[0]["expanded_at"] is not None, f"outbox expansion mismatch: {events}")
    deliveries = database.all(
        "SELECT delivery_kind,target_url,status,attempts,response_status,last_error FROM webhook_deliveries WHERE event_id=%s ORDER BY delivery_kind,target_url",
        (events[0]["event_id"],),
    )
    require(len(deliveries) == 2, f"expected callback and subscription delivery: {deliveries}")
    require(all(row["status"] == "delivered" for row in deliveries), f"delivery not terminal-success: {deliveries}")
    subscription_row = next(row for row in deliveries if row["delivery_kind"] == "subscription")
    require(subscription_row["attempts"] >= 3, f"fail-first retry count not observed: {subscription_row}")
    require(all(item["event_id"] == events[0]["event_id"] for item in receipts), "receiver event identity differs across delivery targets")

    return report(
        "webhook-proof",
        track,
        args.release,
        {
            "run": run_id,
            "event": events[0]["event_id"],
            "deliveryRows": deliveries,
            "receiverReceipts": receipts,
            "subscriptionAttempts": subscription_row["attempts"],
            "outboxAtomicEventCount": len(events),
        },
        limitations=[
            "controlled receiver uses one training verification secret",
            "DNS rebinding and production egress enforcement are outside the local topology",
        ],
    )


def tour_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    wait_for_health(track, 20)
    client = HttpClient(track.api_base)
    project, etag = create_project(client, unique("tour-project"))
    dataset = create_remote_dataset(client, project["id"], unique("tour-dataset"))
    key = unique("tour-idempotency-key")[:64]
    run = create_run(client, project["id"], dataset["id"], key)
    require_status(run, 202, "tour run")
    terminal = wait_for_run(client, run.json()["id"])
    artifacts = client.get(f"/analysis-runs/{terminal['id']}/artifacts").json()["items"]
    return report(
        "capstone-tour",
        track,
        args.release,
        {
            "project": project["id"],
            "projectEtag": etag,
            "dataset": dataset["id"],
            "run": terminal["id"],
            "runStatus": terminal["status"],
            "artifacts": [item["id"] for item in artifacts],
        },
        limitations=["walkthrough only; not concurrency, process-recovery, or release proof"],
    )


def final_command(args: argparse.Namespace, track: Track) -> dict[str, Any]:
    # Run the complete live ladder for the already-started selected release.
    claims: dict[str, Any] = {}
    claims["smoke"] = smoke_command(args, track)["status"]
    claims["postgres"] = postgres_command(args, track)["status"]
    claims["conformance"] = conformance_command(args, track)["status"]
    claims["concurrency"] = concurrency_command(args, track)["status"]
    claims["query"] = query_command(args, track)["status"]
    claims["recovery"] = recovery_command(args, track)["status"]
    claims["artifact"] = artifact_command(args, track)["status"]
    claims["webhook"] = webhook_command(args, track)["status"]
    return report("live-final-proof", track, args.release, claims)


COMMANDS = {
    "wait": wait_command,
    "smoke": smoke_command,
    "postgres": postgres_command,
    "conformance": conformance_command,
    "concurrency": concurrency_command,
    "query": query_command,
    "recovery": recovery_command,
    "artifact": artifact_command,
    "webhook": webhook_command,
    "tour": tour_command,
    "final": final_command,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("--track", choices=["python", "typescript"], required=True)
    parser.add_argument("--release", choices=["1.0", "1.1"], default="1.0")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--actors", type=int, default=100)
    parser.add_argument("--rows", type=int, default=61)
    args = parser.parse_args()
    try:
        COMMANDS[args.command](args, track_config(args.track))
    except ProofFailure as exc:
        payload = {
            "name": args.command,
            "capturedAt": datetime.now(timezone.utc).isoformat(),
            "status": "failed",
            "track": args.track,
            "release": args.release,
            "reason": str(exc),
        }
        REPORTS.mkdir(parents=True, exist_ok=True)
        (REPORTS / f"{args.track}-{args.command}-failed.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
        print(f"PROOF FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
