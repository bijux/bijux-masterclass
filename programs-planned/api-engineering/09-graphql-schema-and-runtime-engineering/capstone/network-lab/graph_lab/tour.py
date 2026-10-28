"""Real loopback composition laboratory for the Course 9 graph gateway.

The laboratory deliberately uses only the Python standard library. Four HTTP
servers run in separate threads and communicate over loopback TCP. This proves
that the gateway composes service-owned capabilities rather than reading a
shared in-process database. It is not presented as a production GraphQL server.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterator
from urllib.error import HTTPError
from urllib.request import Request, urlopen


PROJECT = {
    "id": "proj-1",
    "tenantId": "tenant-a",
    "name": "Genome Study",
    "version": "3",
}

RUNS = [
    {
        "id": "run-1",
        "tenantId": "tenant-a",
        "projectId": "proj-1",
        "status": "COMPLETED",
        "version": "5",
    },
    {
        "id": "run-2",
        "tenantId": "tenant-a",
        "projectId": "proj-1",
        "status": "RUNNING",
        "version": "2",
    },
]

ARTIFACTS = {
    "run-1": [
        {
            "id": "artifact-1",
            "tenantId": "tenant-a",
            "runId": "run-1",
            "mediaType": "application/json",
            "size": 128,
            "sha256": "a" * 64,
        }
    ],
    "run-2": [],
}

DELIVERIES = {
    "run-1": {
        "runId": "run-1",
        "tenantId": "tenant-a",
        "delivered": 1,
        "pending": 0,
        "failed": 0,
        "stalenessSeconds": 10,
    },
    "run-2": {
        "runId": "run-2",
        "tenantId": "tenant-a",
        "delivered": 0,
        "pending": 1,
        "failed": 0,
        "stalenessSeconds": 15,
    },
}


@dataclass
class LabState:
    artifact_available: bool = True
    analysis_calls: int = 0
    artifact_calls: int = 0
    notification_calls: int = 0

    def reset(self) -> None:
        self.artifact_available = True
        self.analysis_calls = 0
        self.artifact_calls = 0
        self.notification_calls = 0


STATE = LabState()


class JsonHandler(BaseHTTPRequestHandler):
    """Shared JSON input/output helpers for the four teaching services."""

    def log_message(self, *args: object) -> None:
        del args

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw)

    def send_json(
        self,
        status: int,
        value: object,
        *,
        content_type: str = "application/json",
    ) -> None:
        raw = json.dumps(
            value,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class AnalysisHandler(JsonHandler):
    """Owner of project and run facts in the loopback laboratory."""

    def do_GET(self) -> None:
        STATE.analysis_calls += 1
        tenant = self.headers.get("X-Tenant")

        if self.path == "/projects/proj-1":
            value = PROJECT if tenant == "tenant-a" else None
            self.send_json(200, value)
            return

        if self.path.startswith("/runs?projectId=proj-1"):
            values = [
                run for run in RUNS if run["tenantId"] == tenant
            ]
            self.send_json(200, values)
            return

        self.send_json(404, {"error": "not-found"})


class ArtifactHandler(JsonHandler):
    """Owner of artifact metadata; can be failed independently."""

    def do_POST(self) -> None:
        STATE.artifact_calls += 1
        if not STATE.artifact_available:
            self.send_json(503, {"error": "unavailable"})
            return

        tenant = self.headers.get("X-Tenant")
        run_ids = self.read_json().get("runIds", [])
        values = {
            run_id: [
                artifact
                for artifact in ARTIFACTS.get(run_id, [])
                if artifact["tenantId"] == tenant
            ]
            for run_id in run_ids
        }
        self.send_json(200, values)


class NotificationHandler(JsonHandler):
    """Owner of delivery summary projections."""

    def do_POST(self) -> None:
        STATE.notification_calls += 1
        tenant = self.headers.get("X-Tenant")
        run_ids = self.read_json().get("runIds", [])
        values: dict[str, object] = {}

        for run_id in run_ids:
            summary = DELIVERIES.get(run_id)
            if summary is not None and summary["tenantId"] == tenant:
                values[run_id] = summary

        self.send_json(200, values)


def get_json(url: str, tenant: str) -> object:
    request = Request(url, headers={"X-Tenant": tenant})
    with urlopen(request, timeout=2) as response:
        return json.loads(response.read())


def post_json(
    url: str,
    tenant: str,
    value: object,
) -> object:
    raw = json.dumps(value).encode("utf-8")
    request = Request(
        url,
        data=raw,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Tenant": tenant,
        },
    )
    with urlopen(request, timeout=2) as response:
        return json.loads(response.read())


class GatewayHandler(JsonHandler):
    """Trusted-operation gateway that composes three remote owners."""

    analysis_url = ""
    artifact_url = ""
    notification_url = ""
    operation_hash = ""

    def do_POST(self) -> None:
        accept = self.headers.get("Accept", "")
        if "application/graphql-response+json" not in accept:
            self.send_json(
                406,
                {"errors": [{"message": "unsupported Accept"}]},
                content_type="application/graphql-response+json",
            )
            return

        body = self.read_json()
        tenant = self.headers.get("X-Tenant", "tenant-a")
        if body.get("id") != self.operation_hash:
            self.send_json(
                400,
                {
                    "errors": [
                        {"message": "unknown persisted operation"}
                    ]
                },
                content_type="application/graphql-response+json",
            )
            return

        project_id = body.get("variables", {}).get("projectId")
        if project_id != "proj-1":
            self._send_graph({"data": {"project": None}})
            return

        project = get_json(
            self.analysis_url + "/projects/proj-1",
            tenant,
        )
        if project is None:
            self._send_graph({"data": {"project": None}})
            return

        runs = get_json(
            self.analysis_url + "/runs?projectId=proj-1",
            tenant,
        )
        run_ids = [run["id"] for run in runs]
        errors: list[dict[str, object]] = []

        try:
            artifacts = post_json(
                self.artifact_url + "/batch",
                tenant,
                {"runIds": run_ids},
            )
        except HTTPError:
            artifacts = None

        deliveries = post_json(
            self.notification_url + "/batch",
            tenant,
            {"runIds": run_ids},
        )

        edges: list[dict[str, object]] = []
        for index, run in enumerate(runs):
            run_artifacts = (
                None
                if artifacts is None
                else artifacts.get(run["id"], [])
            )
            if artifacts is None:
                errors.append(
                    {
                        "message": (
                            "Artifact data is temporarily unavailable"
                        ),
                        "path": [
                            "project",
                            "analysisRuns",
                            "edges",
                            index,
                            "node",
                            "artifacts",
                        ],
                        "extensions": {
                            "code": "DOWNSTREAM_UNAVAILABLE",
                            "service": "artifact-service",
                        },
                    }
                )

            edges.append(
                {
                    "cursor": str(index + 1),
                    "node": {
                        **run,
                        "artifacts": run_artifacts,
                        "deliverySummary": deliveries.get(run["id"]),
                    },
                }
            )

        result: dict[str, object] = {
            "data": {
                "project": {
                    **project,
                    "analysisRuns": {
                        "edges": edges,
                        "pageInfo": {
                            "hasNextPage": False,
                            "endCursor": (
                                edges[-1]["cursor"] if edges else None
                            ),
                        },
                    },
                }
            },
            "extensions": {
                "serviceCalls": {
                    "analysis": 2,
                    "artifact": 1,
                    "notification": 1,
                }
            },
        }
        if errors:
            result["errors"] = errors
        self._send_graph(result)

    def _send_graph(self, value: object) -> None:
        self.send_json(
            200,
            value,
            content_type="application/graphql-response+json",
        )


@contextlib.contextmanager
def server(
    handler: type[BaseHTTPRequestHandler],
) -> Iterator[str]:
    instance = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(
        target=instance.serve_forever,
        daemon=True,
    )
    thread.start()
    try:
        yield f"http://127.0.0.1:{instance.server_port}"
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join(timeout=2)


def run_tour(root: Path) -> dict[str, object]:
    """Run complete, partial-failure, and cross-tenant requests."""

    document = (
        root
        / "capstone/contracts/operations/GetProjectOverview.graphql"
    ).read_text()
    operation_hash = hashlib.sha256(
        document.encode("utf-8")
    ).hexdigest()
    STATE.reset()

    with (
        server(AnalysisHandler) as analysis,
        server(ArtifactHandler) as artifact,
        server(NotificationHandler) as notification,
    ):
        GatewayHandler.analysis_url = analysis
        GatewayHandler.artifact_url = artifact
        GatewayHandler.notification_url = notification
        GatewayHandler.operation_hash = operation_hash

        with server(GatewayHandler) as gateway:

            def call(tenant: str = "tenant-a") -> dict[str, Any]:
                raw = json.dumps(
                    {
                        "id": operation_hash,
                        "variables": {"projectId": "proj-1"},
                    }
                ).encode("utf-8")
                request = Request(
                    gateway + "/graphql",
                    data=raw,
                    method="POST",
                    headers={
                        "Content-Type": "application/json",
                        "Accept": (
                            "application/graphql-response+json"
                        ),
                        "X-Tenant": tenant,
                    },
                )
                with urlopen(request, timeout=3) as response:
                    return json.loads(response.read())

            complete = call()
            STATE.artifact_available = False
            partial = call()
            other_tenant = call("tenant-b")

    return {
        "complete_run_count": len(
            complete["data"]["project"]["analysisRuns"]["edges"]
        ),
        "complete_errors": len(complete.get("errors", [])),
        "partial_artifacts": partial["data"]["project"][
            "analysisRuns"
        ]["edges"][0]["node"]["artifacts"],
        "partial_error_path": partial["errors"][0]["path"],
        "partial_error_service": partial["errors"][0][
            "extensions"
        ]["service"],
        "other_tenant_project": other_tenant["data"]["project"],
        "analysis_calls": STATE.analysis_calls,
        "artifact_calls": STATE.artifact_calls,
        "notification_calls": STATE.notification_calls,
    }


if __name__ == "__main__":
    course_root = Path(__file__).resolve().parents[3]
    print(
        json.dumps(
            run_tour(course_root),
            indent=2,
            sort_keys=True,
        )
    )
