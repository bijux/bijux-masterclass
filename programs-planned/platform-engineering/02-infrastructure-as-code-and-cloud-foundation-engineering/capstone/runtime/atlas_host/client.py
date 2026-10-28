from __future__ import annotations

import argparse
import json
import ssl
import time
from pathlib import Path

from .https_client import PinnedHTTPSConnection


def request(
    logical_host: str,
    connect_host: str,
    port: int,
    ca: Path,
    method: str,
    path: str,
    body: dict[str, object] | None = None,
) -> tuple[int, dict[str, object]]:
    context = ssl.create_default_context(cafile=str(ca))
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    conn = PinnedHTTPSConnection(
        logical_host,
        port,
        connect_host=connect_host,
        context=context,
        timeout=3.0,
    )
    payload = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Host": logical_host}
    if payload is not None:
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(payload))
    try:
        conn.request(method, path, body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read()
    finally:
        conn.close()
    return response.status, json.loads(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logical-host", default="atlas.test")
    parser.add_argument("--connect-host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18443)
    parser.add_argument("--ca", type=Path, required=True)
    parser.add_argument("text")
    args = parser.parse_args()
    status, created = request(
        args.logical_host,
        args.connect_host,
        args.port,
        args.ca,
        "POST",
        "/jobs",
        {"text": args.text},
    )
    if status != 202:
        raise SystemExit(f"submit failed: {status} {created}")
    job_id = str(created["jobId"])
    for _ in range(50):
        status, state = request(
            args.logical_host,
            args.connect_host,
            args.port,
            args.ca,
            "GET",
            f"/jobs/{job_id}",
        )
        if status == 200 and state.get("state") in {"completed", "failed"}:
            print(json.dumps(state, indent=2, sort_keys=True))
            return 0 if state.get("state") == "completed" else 1
        time.sleep(0.1)
    raise SystemExit("job did not complete")


if __name__ == "__main__":
    raise SystemExit(main())
