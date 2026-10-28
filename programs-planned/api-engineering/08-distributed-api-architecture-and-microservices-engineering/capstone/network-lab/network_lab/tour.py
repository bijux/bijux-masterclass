from __future__ import annotations

import base64
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .common import mint_request_token, request_json


KEY = b"course-eight-network-lab-key-32b"
SUBJECT = "learner"
TENANT = "tenant-a"
SCOPES = frozenset({"runs:read", "runs:write"})


def free_port() -> int:
    with socket.socket() as candidate:
        candidate.bind(("127.0.0.1", 0))
        return int(candidate.getsockname()[1])


def wait_ready(url: str, *, deadline: float = 8.0) -> None:
    until = time.monotonic() + deadline
    while time.monotonic() < until:
        try:
            status, _ = request_json("GET", f"{url}/health", timeout=0.2)
            if status == 200:
                return
        except Exception:
            pass
        time.sleep(0.05)
    raise RuntimeError(f"service did not become ready: {url}")


def delegated(
    *,
    issuer: str,
    audience: str,
    action: str,
    scopes: frozenset[str],
    jti: str,
) -> str:
    return mint_request_token(
        issuer=issuer,
        audience=audience,
        subject=SUBJECT,
        tenant=TENANT,
        scopes=scopes,
        action=action,
        key=KEY,
        jti=jti,
    )


def run_network_tour() -> dict[str, Any]:
    ports = {
        name: free_port()
        for name in ("control", "artifact", "notification", "worker", "gateway")
    }
    urls = {name: f"http://127.0.0.1:{port}" for name, port in ports.items()}
    env = os.environ.copy()
    env["COURSE8_LAB_KEY"] = KEY.decode()
    env["CONTROL_URL"] = urls["control"]
    env["ARTIFACT_URL"] = urls["artifact"]
    processes: dict[str, subprocess.Popen[bytes]] = {}
    try:
        for role in ("control", "artifact", "notification", "worker", "gateway"):
            processes[role] = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "network_lab.service",
                    role,
                    "--port",
                    str(ports[role]),
                ],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        for url in urls.values():
            wait_ready(url)

        status, _ = request_json(
            "POST",
            f"{urls['artifact']}/artifacts",
            body={
                "capability": "invalid",
                "tenant": TENANT,
                "content_base64": "",
                "now": 1,
            },
        )
        assert status == 403
        unauthenticated_artifact_rejected = True

        write_token = delegated(
            issuer="edge-gateway",
            audience="analysis-control",
            action="runs:write",
            scopes=SCOPES,
            jti="create-run-1",
        )
        status, run = request_json(
            "POST",
            f"{urls['control']}/runs",
            body={"request_id": "request-1", "dataset_id": "dataset-1"},
            token=write_token,
            tenant=TENANT,
        )
        assert status == 201
        run_id = run["run_id"]

        status, run = request_json(
            "POST",
            f"{urls['control']}/runs/{run_id}/start",
            body={},
            token=write_token,
            tenant=TENANT,
        )
        assert status == 200 and run["state"] == "running"

        content = b"course-eight-network-artifact"
        digest = hashlib.sha256(content).hexdigest()
        worker_token = delegated(
            issuer="course-operator",
            audience="worker-plane",
            action="workers:execute",
            scopes=frozenset({"workers:execute"}),
            jti="execute-run-1",
        )
        status, worker_result = request_json(
            "POST",
            f"{urls['worker']}/execute",
            body={
                "run_id": run_id,
                "content_base64": base64.b64encode(content).decode(),
                "now": 100,
            },
            token=worker_token,
            tenant=TENANT,
        )
        assert status == 200
        completion = worker_result["completion"]
        artifact = worker_result["artifact"]
        assert artifact["sha256"] == digest
        assert completion["run"]["state"] == "completed"

        notification_token = delegated(
            issuer="analysis-control",
            audience="notification-service",
            action="notifications:consume",
            scopes=frozenset({"notifications:consume"}),
            jti="notify-1",
        )
        status, consumed = request_json(
            "POST",
            f"{urls['notification']}/events",
            body=completion["event"],
            token=notification_token,
            tenant=TENANT,
        )
        assert status == 202 and consumed["result"] == "accepted"

        client_token = delegated(
            issuer="course-client",
            audience="edge-gateway",
            action="runs:read",
            scopes=frozenset({"runs:read"}),
            jti="client-read-1",
        )
        status, full = request_json(
            "GET",
            f"{urls['gateway']}/runs/{run_id}",
            token=client_token,
            tenant=TENANT,
        )
        assert status == 200 and full["partial"] is False
        assert full["artifacts"][0]["artifact_id"] == artifact["artifact_id"]

        processes["artifact"].terminate()
        processes["artifact"].wait(timeout=3)
        status, degraded = request_json(
            "GET",
            f"{urls['gateway']}/runs/{run_id}",
            token=client_token,
            tenant=TENANT,
        )
        assert status == 200 and degraded["partial"] is True
        assert degraded["warnings"] == ["artifactsUnavailable"]

        foreign_client_token = mint_request_token(
            issuer="course-client",
            audience="edge-gateway",
            subject="foreign-user",
            tenant="tenant-b",
            scopes=frozenset({"runs:read"}),
            action="runs:read",
            key=KEY,
            jti="foreign-read-1",
        )
        status, _ = request_json(
            "GET",
            f"{urls['gateway']}/runs/{run_id}",
            token=foreign_client_token,
            tenant="tenant-b",
        )
        assert status == 403
        cross_tenant_read_rejected = True

        operator_token = delegated(
            issuer="course-operator",
            audience="notification-service",
            action="notifications:read",
            scopes=frozenset({"notifications:read"}),
            jti="operator-read-1",
        )
        status, delivery_state = request_json(
            "GET",
            f"{urls['notification']}/deliveries",
            token=operator_token,
            tenant=TENANT,
        )
        assert status == 200 and len(delivery_state["deliveries"]) == 1

        return {
            "services_started": 5,
            "remote_calls_exercised": True,
            "event_relay_simulated": True,
            "unauthenticated_artifact_rejected": unauthenticated_artifact_rejected,
            "cross_tenant_read_rejected": cross_tenant_read_rejected,
            "run_id": run_id,
            "state": completion["run"]["state"],
            "artifact_id": artifact["artifact_id"],
            "artifact_sha256": artifact["sha256"],
            "notification_deliveries": len(delivery_state["deliveries"]),
            "full_view_partial": full["partial"],
            "degraded_view_partial": degraded["partial"],
            "degraded_warnings": degraded["warnings"],
        }
    finally:
        for process in processes.values():
            if process.poll() is None:
                process.terminate()
        for process in processes.values():
            if process.poll() is None:
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()


def main() -> None:
    print(json.dumps(run_network_tour(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
