#!/usr/bin/env python3
"""Live endpoint proof for both service tracks and the telemetry topology."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get(url: str) -> tuple[int, bytes, str]:
    request = Request(url, headers={"User-Agent": "course4-live-proof/1.0"})
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, response.read(), response.headers.get("content-type", "")
    except HTTPError as exc:
        return exc.code, exc.read(), exc.headers.get("content-type", "")
    except URLError as exc:
        raise SystemExit(f"cannot reach {url}: {exc}") from exc


def assert_health(base: str, track: str) -> None:
    for route in ["/internal/health/live", "/internal/health/ready"]:
        status, body, content_type = get(base + route)
        if status != 200:
            raise SystemExit(f"{track} {route} returned {status}: {body[:200]!r}")
        if "json" not in content_type:
            raise SystemExit(f"{track} {route} is not JSON")
        payload = json.loads(body)
        if route.endswith("live") and payload.get("live") is not True:
            raise SystemExit(f"{track} is not live: {payload}")
        if route.endswith("ready") and payload.get("ready") is not True:
            raise SystemExit(f"{track} is not ready: {payload}")

    status, body, _ = get(base + "/internal/metrics")
    text = body.decode("utf-8", errors="replace")
    if status != 200 or "analysis_http_requests_total" not in text or "# EOF" not in text:
        raise SystemExit(f"{track} metrics endpoint failed policy: status={status}")


def main() -> None:
    python_base = os.environ.get("PYTHON_API_URL", "http://127.0.0.1:58000")
    typescript_base = os.environ.get("TYPESCRIPT_API_URL", "http://127.0.0.1:58001")
    prometheus = os.environ.get("PROMETHEUS_URL", "http://127.0.0.1:59090")
    collector = os.environ.get("OTEL_COLLECTOR_METRICS_URL", "http://127.0.0.1:8888")

    assert_health(python_base, "python")
    assert_health(typescript_base, "typescript")

    status, body, _ = get(prometheus + "/-/ready")
    if status != 200:
        raise SystemExit(f"Prometheus is not ready: {status} {body[:200]!r}")
    status, body, _ = get(collector + "/metrics")
    if status != 200 or b"otelcol_" not in body:
        raise SystemExit("OpenTelemetry Collector self-metrics are unavailable")

    print(
        "PASS live telemetry proof — both APIs live/ready, bounded metrics exposed, "
        "Prometheus ready, collector self-observability present"
    )


if __name__ == "__main__":
    main()
