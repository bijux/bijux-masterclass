#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable

import httpx


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


class Evidence:
    def __init__(self, provider: str, base_url: str) -> None:
        self.provider = provider
        self.base_url = base_url
        self.checks: list[Check] = []

    def check(self, name: str, condition: bool, detail: str) -> None:
        self.checks.append(Check(name, condition, detail))
        if not condition:
            raise AssertionError(f"{name}: {detail}")

    def payload(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "baseUrl": self.base_url,
            "passed": all(item.passed for item in self.checks),
            "checks": [asdict(item) for item in self.checks],
        }


def _problem(response: httpx.Response, status: int) -> dict[str, Any]:
    assert response.status_code == status, response.text
    assert "application/problem+json" in response.headers.get("content-type", "")
    body = response.json()
    assert body["status"] == status
    assert body["type"].startswith("https://api.example.test/problems/")
    assert body["requestId"].startswith("req_")
    return body


def run(base_url: str, provider: str) -> dict[str, Any]:
    evidence = Evidence(provider, base_url)
    writer = {"Authorization": "Bearer learner-write"}
    reader = {"Authorization": "Bearer learner-read"}
    other = {"Authorization": "Bearer other-owner"}
    admin = {"Authorization": "Bearer admin"}

    with httpx.Client(base_url=base_url.rstrip("/"), timeout=10.0) as client:
        response = client.get("/health")
        evidence.check("anonymous health", response.status_code == 200, response.text)
        evidence.check(
            "health identity",
            response.json().get("service") == "analysis-runs-api",
            json.dumps(response.json()),
        )

        missing = client.get("/projects")
        _problem(missing, 401)
        evidence.check("protected route rejects anonymous", True, "401 Problem Details")

        forbidden = client.post("/projects", headers=reader, json={"name": "No write scope"})
        _problem(forbidden, 403)
        evidence.check("scope enforcement", True, "reader cannot create")

        created = client.post(
            "/projects",
            headers=writer,
            json={"name": f"Conformance {provider}", "description": "provider-neutral evidence"},
        )
        evidence.check("project status", created.status_code == 201, created.text)
        project = created.json()
        project_id = project["id"]
        etag = created.headers.get("etag")
        evidence.check("project Location", created.headers.get("location") == f"/projects/{project_id}", str(created.headers))
        evidence.check("project ETag", bool(etag and etag.startswith('"prj_')), str(created.headers))
        evidence.check("request correlation", created.headers.get("x-request-id", "").startswith("req_"), str(created.headers))

        no_precondition = client.patch(
            f"/projects/{project_id}",
            headers={**writer, "Content-Type": "application/merge-patch+json"},
            json={"name": "Missing precondition"},
        )
        _problem(no_precondition, 428)
        stale = client.patch(
            f"/projects/{project_id}",
            headers={**writer, "If-Match": '"prj_9999:99"', "Content-Type": "application/merge-patch+json"},
            json={"name": "Stale precondition"},
        )
        _problem(stale, 412)
        updated = client.patch(
            f"/projects/{project_id}",
            headers={**writer, "If-Match": str(etag), "Content-Type": "application/merge-patch+json"},
            json={"name": f"Conformance {provider} revised"},
        )
        evidence.check("conditional update", updated.status_code == 200 and updated.json()["version"] == 2, updated.text)

        registered = client.post(
            f"/projects/{project_id}/datasets",
            headers=writer,
            json={
                "name": "measurements",
                "source": {"kind": "local-file", "fileName": "measurements.csv", "mediaType": "text/csv"},
            },
        )
        evidence.check("dataset registration", registered.status_code == 201, registered.text)
        dataset_id = registered.json()["id"]

        empty = client.post(
            f"/datasets/{dataset_id}/content",
            headers=writer,
            files={"file": ("empty.csv", b"", "text/csv")},
        )
        empty_problem = _problem(empty, 422)
        evidence.check("empty upload has validation issues", bool(empty_problem.get("errors")), empty.text)

        uploaded = client.post(
            f"/datasets/{dataset_id}/content",
            headers=writer,
            files={"file": ("measurements.csv", b"sample,value\nA,1\n", "text/csv")},
        )
        evidence.check("multipart upload", uploaded.status_code == 201 and uploaded.json()["contentLength"] == 17, uploaded.text)

        key = f"conformance-{provider}-0001"
        request_body = {
            "projectId": project_id,
            "datasetId": dataset_id,
            "parameters": {"algorithm": "quality-summary", "priority": "normal", "labels": {"suite": "live"}},
        }
        accepted = client.post(
            "/analysis-runs",
            headers={**writer, "Idempotency-Key": key},
            json=request_body,
        )
        evidence.check("run accepted", accepted.status_code == 202, accepted.text)
        run_id = accepted.json()["id"]
        evidence.check("run status monitor", accepted.headers.get("location") == f"/analysis-runs/{run_id}", str(accepted.headers))
        evidence.check("first idempotency result", accepted.headers.get("idempotent-replay") == "false", str(accepted.headers))

        replay = client.post(
            "/analysis-runs",
            headers={**writer, "Idempotency-Key": key},
            json=request_body,
        )
        evidence.check(
            "idempotent replay",
            replay.status_code == 202
            and replay.json()["id"] == run_id
            and replay.headers.get("idempotent-replay") == "true",
            replay.text,
        )
        changed = dict(request_body)
        changed["parameters"] = {"algorithm": "checksum", "priority": "normal", "labels": {}}
        conflict = client.post(
            "/analysis-runs",
            headers={**writer, "Idempotency-Key": key},
            json=changed,
        )
        _problem(conflict, 409)
        evidence.check("idempotency body binding", True, "changed body rejected")

        observed_statuses = [accepted.json()["status"]]
        deadline = time.monotonic() + 2.0
        completed_poll = None
        while time.monotonic() < deadline:
            poll = client.get(f"/analysis-runs/{run_id}", headers=reader)
            if poll.status_code != 200:
                evidence.check("run polling response", False, poll.text)
            observed_statuses.append(poll.json()["status"])
            if poll.json()["status"] == "completed":
                completed_poll = poll
                break
            time.sleep(0.01)
        evidence.check(
            "run progression",
            completed_poll is not None
            and observed_statuses[0] == "queued"
            and "running" in observed_statuses
            and observed_statuses[-1] == "completed",
            json.dumps(observed_statuses),
        )

        page = client.get(f"/analysis-runs/{run_id}/artifacts", headers=reader)
        evidence.check("artifact materialization", page.status_code == 200 and len(page.json()["items"]) == 1, page.text)
        artifact_id = page.json()["items"][0]["id"]
        hidden = client.get(f"/artifacts/{artifact_id}", headers=other)
        _problem(hidden, 404)
        evidence.check("ownership concealment", True, "other owner receives 404")

        sse = client.get(f"/analysis-runs/{run_id}/events", headers={**reader, "Accept": "text/event-stream"})
        evidence.check("SSE stream", sse.status_code == 200 and "event: progress" in sse.text, sse.text[:500])
        ndjson = client.get(f"/analysis-runs/{run_id}/events", headers={**reader, "Accept": "application/x-ndjson"})
        lines = [json.loads(line) for line in ndjson.text.splitlines() if line.strip()]
        evidence.check("NDJSON stream", ndjson.status_code == 200 and len(lines) >= 1 and lines[-1]["progress"] == 100, ndjson.text[:500])

        bad_hook = client.post(
            "/webhook-subscriptions",
            headers=writer,
            json={"targetUrl": "https://169.254.169.254/latest", "eventTypes": ["analysis.completed"], "secret": "0123456789abcdef"},
        )
        _problem(bad_hook, 422)
        hook = client.post(
            "/webhook-subscriptions",
            headers=writer,
            json={"targetUrl": "https://hooks.example.test/analysis", "eventTypes": ["analysis.completed"], "secret": "0123456789abcdef"},
        )
        evidence.check("constrained webhook", hook.status_code == 201 and "secret" not in hook.json(), hook.text)

        diagnostics_forbidden = client.get("/internal/diagnostics", headers=writer)
        _problem(diagnostics_forbidden, 403)
        diagnostics = client.get("/internal/diagnostics", headers=admin)
        evidence.check("admin diagnostics", diagnostics.status_code == 200 and diagnostics.json()["counts"]["runs"] >= 1, diagnostics.text)

    return evidence.payload()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run provider-neutral Analysis Runs API conformance")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        payload = run(args.base_url, args.provider)
    except Exception as exc:
        payload = {
            "provider": args.provider,
            "baseUrl": args.base_url,
            "passed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2), file=sys.stderr)
        return 1
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
