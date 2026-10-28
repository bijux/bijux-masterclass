#!/usr/bin/env python3
"""Dependency-light HTTP benchmark envelope producer."""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

TRACK = Path(__file__).resolve().parents[2] / "tracks" / "python-fastapi" / "src"
sys.path.insert(0, str(TRACK))

from api_performance.models import (  # noqa: E402
    BenchmarkEnvelope,
    CorrectnessReport,
    EnvironmentFingerprint,
    OutcomeCounts,
    WorkloadSpec,
)
from api_performance.statistics import summarize  # noqa: E402


def request_once(base_url: str, path: str) -> tuple[int, bytes, float, dict[str, str]]:
    started = time.perf_counter_ns()
    request = Request(base_url + path, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=2.0) as response:
            body = response.read()
            status = response.status
            headers = {key.lower(): value for key, value in response.headers.items()}
    except HTTPError as error:
        body = error.read()
        status = error.code
        headers = {key.lower(): value for key, value in error.headers.items()}
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
    return status, body, elapsed_ms, headers


def run_closed(base_url: str, *, count: int, concurrency: int) -> dict[str, object]:
    workload = WorkloadSpec(
        id="WL-PROJECT-READ",
        model="closed",
        rate_per_second=float(concurrency),
        duration_seconds=max(1, count // max(1, concurrency)),
        dataset_id="DS-LOCAL-LAB",
        request_mix={"getProject": 1.0},
        max_outstanding_per_client=1,
    )
    environment = EnvironmentFingerprint(
        runtime="python",
        runtime_version=platform.python_version(),
        cpu_logical=1,
        memory_limit_bytes=536_870_912,
        process_count=1,
        worker_count=concurrency,
        source_revision="course5-local-tour",
        dataset_id="DS-LOCAL-LAB",
        database_profile="none-local-http-target",
        feature_flags={"conditionalRequests": True},
    )
    samples: list[float] = []
    failures = 0
    checks = {"status": True, "body": True, "etag": True}
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(request_once, base_url, "/projects/project-1") for _ in range(count)]
        for future in as_completed(futures):
            status, body, elapsed, headers = future.result()
            samples.append(elapsed)
            checks["status"] &= status == 200
            checks["body"] &= b'"id":"project-1"' in body
            checks["etag"] &= headers.get("etag", "").startswith('"sha256-')
            if status != 200:
                failures += 1
    summary = asdict(summarize(samples))
    envelope = BenchmarkEnvelope(
        profile_version="1.0",
        workload_id=workload.id,
        workload_hash=workload.identity,
        environment_hash=environment.identity,
        evidence_class="B",
        correctness=CorrectnessReport(all(checks.values()), checks),
        outcomes=OutcomeCounts(
            offered=count,
            started=count,
            admitted=count,
            completed=count,
            rejected=0,
            failed=failures,
            missing=0,
        ),
        summary={
            "latencyMs": summary,
            "throughputPerSecond": count / max(sum(samples) / 1000 / concurrency, 1e-9),
        },
        source_revision="course5-local-tour",
        annotations={"claimBoundary": "local mechanism evidence; not production capacity"},
    )
    return {
        "profileVersion": envelope.profile_version,
        "workloadId": envelope.workload_id,
        "workloadHash": envelope.workload_hash,
        "environmentHash": envelope.environment_hash,
        "evidenceClass": envelope.evidence_class,
        "correctness": {"passed": envelope.correctness.passed, "checks": dict(envelope.correctness.checks)},
        "outcomes": envelope.outcomes.as_dict(),
        "summary": envelope.summary,
        "sourceRevision": envelope.source_revision,
        "annotations": dict(envelope.annotations),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8085")
    parser.add_argument("--count", type=int, default=48)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.count <= 0 or args.concurrency <= 0:
        raise SystemExit("count and concurrency must be positive")
    result = run_closed(args.base_url, count=args.count, concurrency=args.concurrency)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
