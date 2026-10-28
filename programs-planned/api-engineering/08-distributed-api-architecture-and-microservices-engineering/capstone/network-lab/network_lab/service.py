from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
import time
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from distributed_api.capability import CapabilityAuthority
from distributed_api.model import Conflict, Unauthorized, ValidationError
from distributed_api.services import (
    AnalysisControlService,
    ArtifactService,
    NotificationService,
)

from .common import (
    context,
    mint_request_token,
    read_json,
    request_json,
    send_json,
    verify_request_token,
)


_RUN_PATH = re.compile(r"^/runs/([^/]+)$")
_RUN_ACTION = re.compile(r"^/runs/([^/]+)/(start|upload-capability|complete)$")
_ARTIFACT_PATH = re.compile(r"^/artifacts/([^/]+)$")


class CourseServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
        state: object,
    ) -> None:
        super().__init__(address, handler)
        self.state = state


class JsonHandler(BaseHTTPRequestHandler):
    server_version = "Course8Lab/1.0"

    def log_message(self, format: str, *args: object) -> None:
        if os.environ.get("COURSE8_LAB_LOG") == "1":
            super().log_message(format, *args)

    def do_GET(self) -> None:  # noqa: N802
        self._dispatch("GET")

    def do_POST(self) -> None:  # noqa: N802
        self._dispatch("POST")

    def _dispatch(self, method: str) -> None:
        try:
            if self.path == "/health":
                send_json(self, 200, {"status": "ok"})
                return
            self.route(method)
        except Unauthorized as exc:
            send_json(self, 403, {"error": str(exc)})
        except (ValidationError, KeyError, ValueError) as exc:
            send_json(self, 400, {"error": str(exc)})
        except Conflict as exc:
            send_json(self, 409, {"error": str(exc)})
        except Exception as exc:  # pragma: no cover - defensive boundary
            send_json(self, 500, {"error": type(exc).__name__})

    def route(self, method: str) -> None:
        raise NotImplementedError

    @property
    def state(self) -> Any:
        return self.server.state  # type: ignore[attr-defined]


class ControlState:
    def __init__(self, key: bytes) -> None:
        self.key = key
        self.service = AnalysisControlService(
            CapabilityAuthority(issuer="analysis-control", key=key)
        )


class ControlHandler(JsonHandler):
    def _caller(self, action: str, *, issuer: str = "edge-gateway"):
        return verify_request_token(
            self,
            issuer=issuer,
            audience="analysis-control",
            action=action,
            key=self.state.key,
        )

    def route(self, method: str) -> None:
        if method == "POST" and self.path == "/runs":
            caller = self._caller("runs:write")
            body = read_json(self)
            run = self.state.service.create_run(
                context(caller, workload="edge-gateway"),
                request_id=str(body["request_id"]),
                dataset_id=str(body["dataset_id"]),
            )
            send_json(self, 201, run_view(run))
            return

        match = _RUN_ACTION.match(self.path)
        if method == "POST" and match:
            run_id, action = match.groups()
            issuer = "edge-gateway" if action == "start" else "worker-plane"
            caller = self._caller("runs:write", issuer=issuer)
            ctx = context(caller, workload=issuer)
            body = read_json(self)
            if action == "start":
                run = self.state.service.start(run_id)
                send_json(self, 200, run_view(run))
                return
            if action == "upload-capability":
                token = self.state.service.mint_upload_capability(
                    ctx,
                    run_id=run_id,
                    sha256=str(body["sha256"]),
                    max_bytes=int(body["max_bytes"]),
                    now=int(body["now"]),
                )
                run = self.state.service.runs[run_id]
                send_json(self, 200, {"token": token, "attempt_id": run.attempt_id})
                return
            if action == "complete":
                run = self.state.service.attach_and_complete(
                    run_id=run_id,
                    attempt_id=str(body["attempt_id"]),
                    artifact_id=str(body["artifact_id"]),
                    event_id=str(body["event_id"]),
                )
                event = next(
                    item
                    for item in reversed(self.state.service.events)
                    if item.get("event_id") == body["event_id"]
                )
                send_json(self, 200, {"run": run_view(run), "event": event})
                return

        match = _RUN_PATH.match(self.path)
        if method == "GET" and match:
            caller = self._caller("runs:read")
            run = self.state.service.get_run(
                context(caller, workload="edge-gateway"),
                match.group(1),
            )
            send_json(self, 200, run_view(run))
            return
        send_json(self, 404, {"error": "not found"})


class ArtifactState:
    def __init__(self, key: bytes) -> None:
        self.key = key
        self.service = ArtifactService(
            CapabilityAuthority(issuer="analysis-control", key=key)
        )


class ArtifactHandler(JsonHandler):
    def route(self, method: str) -> None:
        if method == "POST" and self.path == "/artifacts":
            caller = verify_request_token(
                self,
                issuer="worker-plane",
                audience="artifact-service",
                action="artifacts:upload",
                key=self.state.key,
            )
            body = read_json(self, maximum=2_097_152)
            if str(body["tenant"]) != caller.tenant:
                raise Unauthorized("workload tenant does not match artifact tenant")
            content = base64.b64decode(str(body["content_base64"]), validate=True)
            artifact = self.state.service.store(
                token=str(body["capability"]),
                tenant=caller.tenant,
                content=content,
                now=int(body["now"]),
            )
            send_json(self, 201, artifact_view(artifact))
            return
        match = _ARTIFACT_PATH.match(self.path)
        if method == "GET" and match:
            caller = verify_request_token(
                self,
                issuer="edge-gateway",
                audience="artifact-service",
                action="artifacts:read",
                key=self.state.key,
            )
            artifact = self.state.service.get(match.group(1), tenant=caller.tenant)
            send_json(self, 200, artifact_view(artifact))
            return
        send_json(self, 404, {"error": "not found"})


class NotificationState:
    def __init__(self, key: bytes) -> None:
        self.key = key
        self.service = NotificationService()


class NotificationHandler(JsonHandler):
    def route(self, method: str) -> None:
        if method == "POST" and self.path == "/events":
            verify_request_token(
                self,
                issuer="analysis-control",
                audience="notification-service",
                action="notifications:consume",
                key=self.state.key,
            )
            result = self.state.service.consume(read_json(self))
            send_json(self, 202, {"result": result})
            return
        if method == "GET" and self.path == "/deliveries":
            verify_request_token(
                self,
                issuer="course-operator",
                audience="notification-service",
                action="notifications:read",
                key=self.state.key,
            )
            send_json(self, 200, {"deliveries": self.state.service.deliveries})
            return
        send_json(self, 404, {"error": "not found"})


class WorkerState:
    def __init__(self, key: bytes, control_url: str, artifact_url: str) -> None:
        self.key = key
        self.control_url = control_url.rstrip("/")
        self.artifact_url = artifact_url.rstrip("/")


class WorkerHandler(JsonHandler):
    def route(self, method: str) -> None:
        if method != "POST" or self.path != "/execute":
            send_json(self, 404, {"error": "not found"})
            return
        caller = verify_request_token(
            self,
            issuer="course-operator",
            audience="worker-plane",
            action="workers:execute",
            key=self.state.key,
        )
        body = read_json(self, maximum=2_097_152)
        run_id = str(body["run_id"])
        content = base64.b64decode(str(body["content_base64"]), validate=True)
        digest = hashlib.sha256(content).hexdigest()
        now = int(body["now"])

        control_token = mint_request_token(
            issuer="worker-plane",
            audience="analysis-control",
            subject=caller.subject,
            tenant=caller.tenant,
            scopes=frozenset({"runs:write"}),
            action="runs:write",
            key=self.state.key,
            now=int(time.time()),
            jti=f"worker-control:{run_id}:{digest}",
        )
        status, capability = request_json(
            "POST",
            f"{self.state.control_url}/runs/{run_id}/upload-capability",
            body={"sha256": digest, "max_bytes": len(content), "now": now},
            token=control_token,
            tenant=caller.tenant,
        )
        if status != 200:
            send_json(self, status, capability)
            return

        artifact_token = mint_request_token(
            issuer="worker-plane",
            audience="artifact-service",
            subject=caller.subject,
            tenant=caller.tenant,
            scopes=frozenset({"artifacts:upload"}),
            action="artifacts:upload",
            key=self.state.key,
            now=int(time.time()),
            jti=f"worker-artifact:{run_id}:{digest}",
        )
        status, artifact = request_json(
            "POST",
            f"{self.state.artifact_url}/artifacts",
            body={
                "capability": capability["token"],
                "tenant": caller.tenant,
                "content_base64": base64.b64encode(content).decode(),
                "now": now + 1,
            },
            token=artifact_token,
            tenant=caller.tenant,
        )
        if status != 201:
            send_json(self, status, artifact)
            return

        event_id = f"completed:{run_id}:3"
        status, completion = request_json(
            "POST",
            f"{self.state.control_url}/runs/{run_id}/complete",
            body={
                "attempt_id": capability["attempt_id"],
                "artifact_id": artifact["artifact_id"],
                "event_id": event_id,
            },
            token=control_token,
            tenant=caller.tenant,
        )
        send_json(self, status, {"completion": completion, "artifact": artifact})


class GatewayState:
    def __init__(self, key: bytes, control_url: str, artifact_url: str) -> None:
        self.key = key
        self.control_url = control_url.rstrip("/")
        self.artifact_url = artifact_url.rstrip("/")


class GatewayHandler(JsonHandler):
    def route(self, method: str) -> None:
        match = _RUN_PATH.match(self.path)
        if method != "GET" or not match:
            send_json(self, 404, {"error": "not found"})
            return
        client = verify_request_token(
            self,
            issuer="course-client",
            audience="edge-gateway",
            action="runs:read",
            key=self.state.key,
        )
        now = int(time.time())
        control_token = mint_request_token(
            issuer="edge-gateway",
            audience="analysis-control",
            subject=client.subject,
            tenant=client.tenant,
            scopes=client.scopes,
            action="runs:read",
            key=self.state.key,
            now=now,
            jti=f"gateway-control:{match.group(1)}:{now}",
        )
        status, run = request_json(
            "GET",
            f"{self.state.control_url}/runs/{match.group(1)}",
            token=control_token,
            tenant=client.tenant,
        )
        if status != 200:
            send_json(self, status, run)
            return

        artifacts: list[object] = []
        warnings: list[str] = []
        artifact_token = mint_request_token(
            issuer="edge-gateway",
            audience="artifact-service",
            subject=client.subject,
            tenant=client.tenant,
            scopes=frozenset({"artifacts:read"}),
            action="artifacts:read",
            key=self.state.key,
            now=now,
            jti=f"gateway-artifact:{match.group(1)}:{now}",
        )
        for artifact_id in run["artifact_ids"]:
            try:
                artifact_status, artifact = request_json(
                    "GET",
                    f"{self.state.artifact_url}/artifacts/{artifact_id}",
                    token=artifact_token,
                    tenant=client.tenant,
                    timeout=0.5,
                )
            except (urllib.error.URLError, TimeoutError, ConnectionError):
                artifact_status, artifact = 503, None
            if artifact_status == 200:
                artifacts.append(artifact)
            else:
                warnings.append("artifactsUnavailable")
                break
        send_json(self, 200, {
            **run,
            "artifacts": artifacts,
            "authoritative": True,
            "partial": bool(warnings),
            "warnings": warnings,
        })


def run_view(run: Any) -> dict[str, object]:
    return {
        "run_id": run.run_id,
        "tenant": run.tenant,
        "owner": run.owner,
        "dataset_id": run.dataset_id,
        "attempt_id": run.attempt_id,
        "state": run.state.value,
        "version": run.version,
        "artifact_ids": list(run.artifact_ids),
    }


def artifact_view(artifact: Any) -> dict[str, object]:
    return {
        "artifact_id": artifact.artifact_id,
        "tenant": artifact.tenant,
        "run_id": artifact.run_id,
        "attempt_id": artifact.attempt_id,
        "sha256": artifact.sha256,
        "size": len(artifact.content),
        "version": artifact.version,
        "state": artifact.state,
    }


def build(role: str, key: bytes) -> tuple[type[JsonHandler], object]:
    if role == "control":
        return ControlHandler, ControlState(key)
    if role == "artifact":
        return ArtifactHandler, ArtifactState(key)
    if role == "notification":
        return NotificationHandler, NotificationState(key)
    if role == "worker":
        return WorkerHandler, WorkerState(
            key,
            os.environ["CONTROL_URL"],
            os.environ["ARTIFACT_URL"],
        )
    if role == "gateway":
        return GatewayHandler, GatewayState(
            key,
            os.environ["CONTROL_URL"],
            os.environ["ARTIFACT_URL"],
        )
    raise ValueError(f"unknown role: {role}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "role",
        choices=["control", "artifact", "notification", "worker", "gateway"],
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    key = os.environ.get(
        "COURSE8_LAB_KEY",
        "course-eight-network-lab-key-32b",
    ).encode()
    handler, state = build(args.role, key)
    server = CourseServer((args.host, args.port), handler, state)
    server.serve_forever()


if __name__ == "__main__":
    main()
