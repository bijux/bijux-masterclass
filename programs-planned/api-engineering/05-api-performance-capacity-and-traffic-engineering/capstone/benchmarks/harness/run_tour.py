#!/usr/bin/env python3
"""Run the deterministic local performance tour in one process."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from lab_server import ARTIFACT, ETAG, create_server
from local_benchmark import run_closed


def fetch(url: str, headers: dict[str, str] | None = None) -> tuple[int, bytes, dict[str, str]]:
    request = Request(url, headers=headers or {})
    try:
        with urlopen(request, timeout=2) as response:
            return response.status, response.read(), {k.lower(): v for k, v in response.headers.items()}
    except HTTPError as error:
        return error.code, error.read(), {k.lower(): v for k, v in error.headers.items()}


def main() -> None:
    server = create_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        envelope = run_closed(base, count=36, concurrency=3)
        status, body, headers = fetch(base + "/projects/project-1")
        conditional, conditional_body, _ = fetch(
            base + "/projects/project-1", {"If-None-Match": headers["etag"]}
        )
        range_status, range_body, range_headers = fetch(
            base + "/artifacts/artifact-1/content", {"Range": "bytes=10-29"}
        )
        artifact_status, artifact_body, artifact_headers = fetch(
            base + "/artifacts/artifact-1/content"
        )
        artifact_conditional, artifact_conditional_body, _ = fetch(
            base + "/artifacts/artifact-1/content", {"If-None-Match": ETAG}
        )
        checks = {
            "benchmarkPublishable": envelope["correctness"]["passed"] and envelope["outcomes"]["missing"] == 0,
            "projectRead": status == 200 and b"project-1" in body,
            "projectConditional": conditional == 304 and conditional_body == b"",
            "artifactRange": range_status == 206 and range_body == ARTIFACT[10:30] and range_headers.get("content-range", "").startswith("bytes 10-29/"),
            "artifactFull": artifact_status == 200 and artifact_body == ARTIFACT and artifact_headers.get("etag") == ETAG,
            "artifactConditional": artifact_conditional == 304 and artifact_conditional_body == b"",
        }
        result = {"checks": checks, "passed": all(checks.values()), "envelope": envelope}
        output = Path(__file__).resolve().parents[2] / "reports" / "capstone-tour.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        if not result["passed"]:
            raise SystemExit("capstone tour failed")
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


if __name__ == "__main__":
    main()
