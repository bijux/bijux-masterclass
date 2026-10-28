from __future__ import annotations

import json
import os
import signal
import ssl
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
RUNTIME = CAPSTONE / "runtime"
for value in (str(CAPSTONE), str(RUNTIME)):
    if value not in sys.path:
        sys.path.insert(0, value)

from atlas_host.https_client import PinnedHTTPSConnection
from cloud_model.backup import create_manifest, materialize_backup, restore_backup
from cloud_model.compute import validate_image_release, validate_launch_contract
from cloud_model.cost_quota import evaluate_cost_profile, evaluate_quotas
from cloud_model.iam import evaluate_policy
from cloud_model.network import trace_path, validate_network_plan
from cloud_model.organization import validate_organization
from cloud_model.plan import build_plan, plan_summary
from cloud_model.release import evaluate_candidate
from cloud_model.state_backend import validate_backend_profile


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text(encoding="utf-8"))


def wait_file(path: Path, timeout: float = 5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists():
            return json.loads(path.read_text())
        time.sleep(0.05)
    raise RuntimeError(f"timed out waiting for {path}")


def https_request(port: int, method: str, path: str, body=None):
    context = ssl.create_default_context(cafile=str(RUNTIME / "pki" / "ca.crt"))
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    conn = PinnedHTTPSConnection(
        "atlas.test", port, connect_host="127.0.0.1", context=context, timeout=3
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


def wrong_name_rejected(port: int) -> bool:
    context = ssl.create_default_context(cafile=str(RUNTIME / "pki" / "ca.crt"))
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    conn = PinnedHTTPSConnection(
        "wrong.test", port, connect_host="127.0.0.1", context=context, timeout=3
    )
    try:
        conn.request("GET", "/health/live", headers={"Host": "wrong.test"})
        conn.getresponse()
    except ssl.SSLCertVerificationError:
        return True
    finally:
        conn.close()
    return False


def semantic_checks() -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []

    actions = build_plan(
        load("fixtures/plan/config-v2-intended.json")["resources"],
        load("fixtures/plan/state-v1.json")["resources"],
    )
    summary = plan_summary(actions)
    assert summary["counts"]["create"] == 1
    assert not summary["destructiveAddresses"]
    checks.append({"name": "semantic-plan", "counts": summary["counts"]})

    backend_errors = validate_backend_profile(load("fixtures/state/backend-safe.json"))
    assert not backend_errors
    checks.append({"name": "state-backend-profile", "errors": backend_errors})

    organization_errors = validate_organization(load("fixtures/organization/organization-small.json"))
    assert not organization_errors
    checks.append({"name": "organization-boundaries", "errors": organization_errors})

    network = load("fixtures/network/network-plan-safe.json")
    network_errors = validate_network_plan(network)
    assert not network_errors
    path = trace_path(network, source_subnet="private-b", destination_ip="1.1.1.1")
    assert path["target"] == "nat-b"
    checks.append({"name": "network-path", "path": path})

    policy = load("fixtures/identity/atlas-instance-policy.json")
    for vector in load("fixtures/identity/atlas-instance-vectors.json"):
        result = evaluate_policy(
            policy,
            action=vector["action"],
            resource=vector["resource"],
            context=vector.get("context", {}),
        )
        assert result["decision"] == vector["expected"]
    checks.append({"name": "runtime-authority-vectors", "cases": 6})

    image = load("fixtures/compute/image-release-v1.json")
    launch = load("fixtures/compute/launch-template-v1.json")
    compute_errors = validate_image_release(image) + validate_launch_contract(launch, image)
    assert not compute_errors
    checks.append({"name": "compute-contract", "errors": compute_errors})

    cost = evaluate_cost_profile(load("fixtures/economics/cost-profile.json"))
    quota = evaluate_quotas(load("fixtures/economics/quota-profile.json"))
    assert cost["withinBudget"] and quota["allSufficient"]
    checks.append({"name": "cost-quota-preflight", "cost": cost, "quota": quota})

    release = evaluate_candidate(load("releases/accepted/candidate.json"))
    assert release["decision"] == "dependency-light-only"
    checks.append({"name": "release-classification", "decision": release["decision"]})
    return checks


def runtime_and_recovery() -> tuple[list[dict[str, object]], dict[str, object]]:
    checks: list[dict[str, object]] = []
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(RUNTIME), str(CAPSTONE)])
    procs: list[subprocess.Popen[bytes]] = []
    cleanup = {"allProcessesStopped": False}
    with tempfile.TemporaryDirectory(prefix="atlas-cloud-tour-") as raw:
        temp_root = Path(raw)
        config_path = temp_root / "atlas.json"
        config = {
            "runtimeDir": str(temp_root / "run"),
            "stateDir": str(temp_root / "state"),
            "logDir": str(temp_root / "log"),
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
            api = subprocess.Popen(
                [sys.executable, "-m", "atlas_host.api", "--config", str(config_path)],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            procs.append(api)
            api_info = wait_file(temp_root / "run" / "api.json")
            worker = subprocess.Popen(
                [sys.executable, "-m", "atlas_host.worker", "--config", str(config_path), "--worker-id", "cloud-tour-worker"],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            procs.append(worker)
            wait_file(temp_root / "run" / "worker.json")
            edge = subprocess.Popen(
                [
                    sys.executable, "-m", "atlas_host.proxy", "--config", str(config_path),
                    "--cert", str(RUNTIME / "pki" / "atlas.crt"),
                    "--key", str(RUNTIME / "pki" / "atlas.key"),
                    "--backend", f"127.0.0.1:{api_info['port']}",
                ],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            procs.append(edge)
            edge_info = wait_file(temp_root / "run" / "edge.json")
            port = int(edge_info["port"])

            assert wrong_name_rejected(port)
            checks.append({"name": "wrong-tls-name-rejected"})

            deadline = time.monotonic() + 5
            while True:
                status, ready = https_request(port, "GET", "/health/ready")
                if status == 200:
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError(f"readiness failed: {status} {ready}")
                time.sleep(0.05)
            checks.append({"name": "edge-readiness", "status": status})

            status, created = https_request(port, "POST", "/jobs", {"text": "atlas cloud foundation"})
            assert status == 202
            job_id = str(created["jobId"])
            for _ in range(100):
                status, state = https_request(port, "GET", f"/jobs/{job_id}")
                if status == 200 and state.get("state") == "completed":
                    break
                time.sleep(0.05)
            else:
                raise RuntimeError("job did not complete")
            assert state["result"]["uppercase"] == "ATLAS CLOUD FOUNDATION"
            checks.append({"name": "durable-job", "jobId": job_id, "result": state["result"]})

            # Stop processes before the consistency point used by this small file backup.
            worker.send_signal(signal.SIGTERM)
            worker.wait(timeout=5)
            edge.send_signal(signal.SIGTERM)
            edge.wait(timeout=5)
            api.send_signal(signal.SIGTERM)
            api.wait(timeout=5)

            source = temp_root / "state"
            backup = temp_root / "backup"
            restore = temp_root / "restore"
            manifest = create_manifest(
                source,
                release="atlas-cloud-foundation-1.0",
                consistency_point=f"completed:{job_id}",
            )
            materialize_backup(source, backup, manifest)
            restored = restore_backup(backup, restore)
            result_file = restore / "spool" / "results" / f"{job_id}.json"
            if not result_file.exists():
                # FileSpool stores results directly under state/results in some profiles.
                candidates = list(restore.rglob(f"{job_id}.json"))
                if not candidates:
                    raise RuntimeError("restored result file is missing")
                result_file = candidates[0]
            restored_result = json.loads(result_file.read_text())
            assert restored_result["result"]["uppercase"] == "ATLAS CLOUD FOUNDATION"
            checks.append({
                "name": "restore-to-empty",
                "files": len(restored["restored"]),
                "resultPath": result_file.relative_to(restore).as_posix(),
            })
        finally:
            for proc in reversed(procs):
                if proc.poll() is None:
                    proc.send_signal(signal.SIGTERM)
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait(timeout=2)
            cleanup = {"allProcessesStopped": all(proc.poll() is not None for proc in procs)}
    return checks, cleanup


def main() -> int:
    report = {
        "profile": "atlas-cloud-foundation-1.0",
        "evidenceClass": "dependency-light-and-local-process",
        "checks": semantic_checks(),
        "limitations": [
            "No AWS API was called.",
            "No real S3 backend or provider lock was exercised.",
            "No cloud instance, ALB, EBS, KMS, IAM, or Route 53 behavior was proved.",
            "The local backup is a filesystem consistency exercise, not an EBS/S3 durability claim.",
        ],
    }
    runtime_checks, cleanup = runtime_and_recovery()
    report["checks"].extend(runtime_checks)
    report["cleanup"] = cleanup
    report["passed"] = cleanup["allProcessesStopped"] and len(report["checks"]) >= 12
    target = CAPSTONE / "reports" / "capstone-tour.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
