from __future__ import annotations

import http.client
import json
import os
import signal
import ssl
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from atlas_host.https_client import PinnedHTTPSConnection

CAPSTONE = Path(__file__).resolve().parents[1]


def wait_file(path: Path, timeout: float = 5.0) -> dict[str, object]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists():
            return json.loads(path.read_text())
        time.sleep(0.05)
    raise RuntimeError(f"timed out waiting for {path}")


def https_request(port: int, method: str, path: str, body: dict[str, object] | None = None) -> tuple[int, dict[str, object]]:
    context = ssl.create_default_context(cafile=str(CAPSTONE / "pki" / "ca.crt"))
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    conn = PinnedHTTPSConnection(
        "atlas.test",
        port,
        connect_host="127.0.0.1",
        context=context,
        timeout=3,
    )
    payload = None if body is None else json.dumps(body).encode()
    headers = {"Host": "atlas.test"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    try:
        conn.request(method, path, body=payload, headers=headers)
        response = conn.getresponse()
        raw = response.read()
        return response.status, json.loads(raw)
    finally:
        conn.close()


def assert_wrong_name_rejected(port: int) -> None:
    context = ssl.create_default_context(cafile=str(CAPSTONE / "pki" / "ca.crt"))
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    conn = PinnedHTTPSConnection(
        "wrong.test", port, connect_host="127.0.0.1", context=context, timeout=3
    )
    try:
        conn.request("GET", "/health/live", headers={"Host": "wrong.test"})
        conn.getresponse()
    except ssl.SSLCertVerificationError:
        return
    finally:
        conn.close()
    raise RuntimeError("TLS accepted a certificate for the wrong logical host")


def main() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(CAPSTONE)
    procs: list[subprocess.Popen[bytes]] = []
    report: dict[str, object] = {"checks": []}
    with tempfile.TemporaryDirectory(prefix="atlas-tour-") as raw:
        root = Path(raw)
        config_path = root / "atlas.json"
        config = {
            "runtimeDir": str(root / "run"),
            "stateDir": str(root / "state"),
            "logDir": str(root / "log"),
            "apiHost": "127.0.0.1",
            "apiPort": 0,
            "edgeHost": "127.0.0.1",
            "edgePort": 0,
            "publicName": "atlas.test",
            "workerPollSeconds": 0.05,
            "workerLeaseSeconds": 1.0,
        }
        config_path.write_text(json.dumps(config))
        try:
            api = subprocess.Popen([sys.executable, "-m", "atlas_host.api", "--config", str(config_path)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(api)
            api_info = wait_file(root / "run" / "api.json")
            worker = subprocess.Popen([sys.executable, "-m", "atlas_host.worker", "--config", str(config_path), "--worker-id", "tour-worker"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(worker)
            wait_file(root / "run" / "worker.json")
            edge = subprocess.Popen([
                sys.executable, "-m", "atlas_host.proxy", "--config", str(config_path),
                "--cert", str(CAPSTONE / "pki" / "atlas.crt"), "--key", str(CAPSTONE / "pki" / "atlas.key"),
                "--backend", f"127.0.0.1:{api_info['port']}"
            ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(edge)
            edge_info = wait_file(root / "run" / "edge.json")
            port = int(edge_info["port"])

            assert_wrong_name_rejected(port)
            report["checks"].append({"name": "wrong-tls-name-rejected", "logicalHost": "wrong.test"})

            deadline = time.monotonic() + 5
            while True:
                status, ready = https_request(port, "GET", "/health/ready")
                if status == 200:
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError(f"readiness did not become healthy: {status} {ready}")
                time.sleep(0.05)
            report["checks"].append({"name": "https-readiness", "status": status, "body": ready})

            status, created = https_request(port, "POST", "/jobs", {"text": "atlas platform"})
            if status != 202:
                raise RuntimeError(f"job submission failed: {status} {created}")
            job_id = str(created["jobId"])
            report["checks"].append({"name": "submit", "status": status, "jobId": job_id})

            for _ in range(100):
                status, state = https_request(port, "GET", f"/jobs/{job_id}")
                if status == 200 and state.get("state") == "completed":
                    break
                time.sleep(0.05)
            else:
                raise RuntimeError("job did not complete")
            expected = "ATLAS PLATFORM"
            actual = state["result"]["uppercase"]
            if actual != expected:
                raise RuntimeError(f"wrong result: {actual}")
            report["checks"].append({"name": "durable-result", "status": status, "uppercase": actual})

            # A client-supplied forwarding identity is overwritten by the edge.
            context = ssl.create_default_context(cafile=str(CAPSTONE / "pki" / "ca.crt"))
            context.minimum_version = ssl.TLSVersion.TLSv1_3
            conn = PinnedHTTPSConnection(
                "atlas.test", port, connect_host="127.0.0.1", context=context, timeout=3
            )
            conn.request("GET", "/health/live", headers={"Host": "atlas.test", "X-Forwarded-For": "10.0.0.1"})
            response = conn.getresponse(); response.read(); conn.close()
            if response.status != 200:
                raise RuntimeError(f"trusted edge request failed: {response.status}")
            event_rows = [json.loads(line) for line in (root / "log" / "events.jsonl").read_text().splitlines()]
            forwarded = [row for row in event_rows if row.get("name") == "edge.forward"][-1]
            fields = forwarded["fields"]
            if fields.get("forwarded_for") != "127.0.0.1" or not fields.get("discarded_forwarded"):
                raise RuntimeError(f"forwarding identity was not rewritten: {fields}")
            report["checks"].append({
                "name": "forwarding-identity-rewritten",
                "status": response.status,
                "forwardedFor": fields.get("forwarded_for"),
                "discardedClientHeader": fields.get("discarded_forwarded"),
            })

            context = ssl.create_default_context(cafile=str(CAPSTONE / "pki" / "ca.crt"))
            context.minimum_version = ssl.TLSVersion.TLSv1_3
            bad_host = PinnedHTTPSConnection(
                "atlas.test", port, connect_host="127.0.0.1", context=context, timeout=3
            )
            bad_host.request("GET", "/health/live", headers={"Host": "other.test"})
            bad_response = bad_host.getresponse(); bad_response.read(); bad_host.close()
            if bad_response.status != 421:
                raise RuntimeError(f"invalid HTTP authority was not rejected: {bad_response.status}")
            report["checks"].append({"name": "invalid-http-authority-rejected", "status": bad_response.status})

            # Graceful worker termination must exit cleanly after current work.
            worker.send_signal(signal.SIGTERM)
            worker.wait(timeout=5)
            if worker.returncode != 0:
                raise RuntimeError(f"worker exit was not clean: {worker.returncode}")
            report["checks"].append({"name": "graceful-worker-stop", "returnCode": worker.returncode})
        finally:
            for proc in reversed(procs):
                if proc.poll() is None:
                    proc.send_signal(signal.SIGTERM)
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill(); proc.wait(timeout=2)
            report["cleanup"] = {"allProcessesStopped": all(p.poll() is not None for p in procs)}
            events = root / "log" / "events.jsonl"
            report["eventCount"] = len(events.read_text().splitlines()) if events.exists() else 0
    target = CAPSTONE / "reports" / "tour.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
