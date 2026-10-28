#!/usr/bin/env python3
"""Execute the Course 2 expand/backfill/enforce release matrix.

This proof owns claims that cannot be established by the static compatibility
checker: an old and new service release can use the expanded schema, application
rollback works before enforcement, historic rows are backfilled, and only the
new release remains after the final constraint.

The script requires Docker Compose. It uses isolated course-owned containers and
ports, writes a JSON report, and always attempts cleanup.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COURSE = Path(__file__).resolve().parents[3]
CAPSTONE = COURSE / "capstone"
COMPOSE_FILE = CAPSTONE / "compose.yaml"
PROOF_RUNNER = CAPSTONE / "tests" / "runtime" / "proof_runner.py"
REPORTS = CAPSTONE / "reports"
PROJECT = "cdse-release-proof"


class ReleaseProofFailure(RuntimeError):
    pass


def run(
    command: list[str],
    *,
    env: dict[str, str] | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command), flush=True)
    return subprocess.run(
        command,
        cwd=CAPSTONE,
        env=env,
        check=True,
        text=True,
        capture_output=capture,
    )


def compose(*arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = [
        "docker",
        "compose",
        "-p",
        PROJECT,
        "-f",
        str(COMPOSE_FILE),
        *arguments,
    ]
    return run(command, env=env)


def service_names(track: str) -> tuple[str, str, str, int, str]:
    if track == "python":
        return "python-api", "python-worker", "python-migrate", 8000, "analysis_python"
    if track == "typescript":
        return (
            "typescript-api",
            "typescript-worker",
            "typescript-migrate",
            8001,
            "analysis_typescript",
        )
    raise ReleaseProofFailure("track must be python or typescript")


def wait_for_health(base: str, timeout: float = 120.0) -> None:
    import urllib.request

    deadline = time.monotonic() + timeout
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"{base}/health", timeout=2) as response:
                if response.status == 200:
                    return
        except Exception as exc:  # pragma: no cover - live environment
            last = exc
        time.sleep(0.5)
    raise ReleaseProofFailure(f"provider did not become healthy at {base}: {last}")


def migrate(track: str, migration_service: str, target: str) -> None:
    common = [
        "run",
        "--rm",
        "--no-deps",
        "-e",
        f"MIGRATION_TARGET={target}",
        migration_service,
    ]
    if track == "python":
        compose(
            *common,
            "analysis-migrate",
            "migrate",
            "--migrations",
            "/app/migrations",
            "--target",
            target,
        )
    else:
        compose(*common, "node", "dist/src/migrate.js")


def start_role(
    service: str,
    container: str,
    release: str,
    *,
    host_port: int | None = None,
) -> None:
    arguments = [
        "run",
        "-d",
        "--no-deps",
        "--name",
        container,
        "-e",
        f"SERVICE_RELEASE={release}",
    ]
    if host_port is not None:
        _, _, _, container_port, _ = service_names("python" if service.startswith("python") else "typescript")
        arguments.extend(["-p", f"127.0.0.1:{host_port}:{container_port}"])
    arguments.append(service)
    compose(*arguments)


def remove_container(name: str) -> None:
    subprocess.run(
        ["docker", "rm", "-f", name],
        cwd=CAPSTONE,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def run_provider_proof(track: str, release: str, base: str, command: str) -> None:
    environment = os.environ.copy()
    key = "PYTHON_API_BASE" if track == "python" else "TYPESCRIPT_API_BASE"
    environment[key] = base
    run(
        [
            sys.executable,
            str(PROOF_RUNNER),
            command,
            "--track",
            track,
            "--release",
            release,
        ],
        env=environment,
    )


def scalar(database: str, sql: str) -> str:
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-p",
            PROJECT,
            "-f",
            str(COMPOSE_FILE),
            "exec",
            "-T",
            "postgres",
            "psql",
            "-U",
            "analysis",
            "-d",
            database,
            "-Atc",
            sql,
        ],
        cwd=CAPSTONE,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def execute(track: str) -> dict[str, Any]:
    if shutil.which("docker") is None:
        raise ReleaseProofFailure("Docker is required for the live release proof")

    api_service, worker_service, migration_service, _port, database = service_names(track)
    prefix = f"cdse-release-{track}"
    old_api = f"{prefix}-old-api"
    old_worker = f"{prefix}-old-worker"
    new_api = f"{prefix}-new-api"
    new_worker = f"{prefix}-new-worker"
    old_base = "http://127.0.0.1:58110" if track == "python" else "http://127.0.0.1:58120"
    new_base = "http://127.0.0.1:58111" if track == "python" else "http://127.0.0.1:58121"
    old_port = int(old_base.rsplit(":", 1)[1])
    new_port = int(new_base.rsplit(":", 1)[1])

    phases: dict[str, Any] = {}
    try:
        compose("down", "--volumes", "--remove-orphans")
        compose("up", "-d", "--build", "postgres", "receiver")
        compose("build", api_service, worker_service, migration_service)

        migrate(track, migration_service, "002")
        start_role(api_service, old_api, "1.0", host_port=old_port)
        start_role(worker_service, old_worker, "1.0")
        wait_for_health(old_base)
        run_provider_proof(track, "1.0", old_base, "conformance")
        run_provider_proof(track, "1.0", old_base, "tour")
        baseline_completed = scalar(
            database,
            "SELECT count(*) FROM analysis_runs WHERE status='completed'",
        )
        phases["baseline"] = {"completedRuns": int(baseline_completed)}

        migrate(track, migration_service, "003")
        run_provider_proof(track, "1.0", old_base, "conformance")
        start_role(api_service, new_api, "1.1", host_port=new_port)
        start_role(worker_service, new_worker, "1.1")
        wait_for_health(new_base)
        run_provider_proof(track, "1.1", new_base, "conformance")
        run_provider_proof(track, "1.1", new_base, "tour")
        missing_before = scalar(
            database,
            "SELECT count(*) FROM analysis_runs "
            "WHERE status='completed' AND result_summary IS NULL",
        )
        phases["expanded"] = {"missingSummaries": int(missing_before)}

        migrate(track, migration_service, "004")
        missing_after = scalar(
            database,
            "SELECT count(*) FROM analysis_runs "
            "WHERE status='completed' AND result_summary IS NULL",
        )
        if missing_after != "0":
            raise ReleaseProofFailure(
                f"backfill left {missing_after} completed rows without result_summary"
            )
        migrate(track, migration_service, "004")
        phases["backfilled"] = {"missingSummaries": 0, "rerun": "passed"}

        # Application rollback is proved before final enforcement.
        remove_container(new_worker)
        remove_container(new_api)
        run_provider_proof(track, "1.0", old_base, "conformance")
        phases["rollbackBeforeEnforce"] = "passed"

        start_role(api_service, new_api, "1.1", host_port=new_port)
        start_role(worker_service, new_worker, "1.1")
        wait_for_health(new_base)
        remove_container(old_worker)
        remove_container(old_api)
        migrate(track, migration_service, "005")
        run_provider_proof(track, "1.1", new_base, "final")
        run([sys.executable, str(CAPSTONE / "scripts" / "course_tool.py"), "release-proof"])
        phases["enforced"] = "passed"

        return {
            "track": track,
            "phases": phases,
            "limitations": [
                "single local PostgreSQL primary",
                "controlled Docker network and webhook receiver",
                "sequential traffic checks during the mixed-version window",
            ],
        }
    finally:
        for name in (old_api, old_worker, new_api, new_worker):
            remove_container(name)
        subprocess.run(
            [
                "docker",
                "compose",
                "-p",
                PROJECT,
                "-f",
                str(COMPOSE_FILE),
                "down",
                "--volumes",
                "--remove-orphans",
            ],
            cwd=CAPSTONE,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", choices=["python", "typescript"], required=True)
    args = parser.parse_args()
    REPORTS.mkdir(parents=True, exist_ok=True)
    try:
        details = execute(args.track)
        payload = {
            "name": "live-release-proof",
            "capturedAt": datetime.now(timezone.utc).isoformat(),
            "status": "passed",
            **details,
        }
    except Exception as exc:
        payload = {
            "name": "live-release-proof",
            "capturedAt": datetime.now(timezone.utc).isoformat(),
            "status": "failed",
            "track": args.track,
            "reason": str(exc),
        }
        (REPORTS / f"{args.track}-live-release-proof.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
        print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)
        raise SystemExit(1)

    (REPORTS / f"{args.track}-live-release-proof.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
