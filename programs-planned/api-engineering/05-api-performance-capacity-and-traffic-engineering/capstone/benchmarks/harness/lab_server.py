#!/usr/bin/env python3
"""Small bounded HTTP target for Course 5 mechanism experiments.

This server is not the predecessor service. It exists so a clean checkout can
exercise validators, ranges, payload size, outcome accounting, and offered-load
scheduling without FastAPI, PostgreSQL, Docker, or network installation.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ARTIFACT = (b"analysis-result-line\n" * 8192)
ETAG = '"sha256-' + hashlib.sha256(ARTIFACT).hexdigest() + '"'
_RANGE = re.compile(r"^bytes=(\d*)-(\d*)$")


def _range(value: str | None, length: int) -> tuple[int, int] | None:
    if value is None:
        return None
    match = _RANGE.fullmatch(value.strip())
    if not match or "," in value:
        raise ValueError("unsupported range")
    first, last = match.groups()
    if first == "" and last == "":
        raise ValueError("empty range")
    if first == "":
        suffix = int(last)
        if suffix <= 0:
            raise ValueError("invalid suffix")
        return max(0, length - suffix), length - 1
    start = int(first)
    end = length - 1 if last == "" else int(last)
    if start >= length or end < start:
        raise ValueError("unsatisfiable range")
    return start, min(end, length - 1)


class Handler(BaseHTTPRequestHandler):
    server_version = "course5-lab/1.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def _json(self, status: int, value: object, *, extra: dict[str, str] | None = None) -> None:
        body = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for key, item in (extra or {}).items():
            self.send_header(key, item)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json(HTTPStatus.OK, {"status": "ok"})
            return
        if parsed.path == "/projects/project-1":
            payload = {"id": "project-1", "name": "Performance Lab", "version": 7}
            body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
            etag = '"sha256-' + hashlib.sha256(body).hexdigest() + '"'
            if self.headers.get("If-None-Match") == etag:
                self.send_response(HTTPStatus.NOT_MODIFIED)
                self.send_header("ETag", etag)
                self.send_header("Cache-Control", "private, max-age=0, must-revalidate")
                self.end_headers()
                return
            self._json(
                HTTPStatus.OK,
                payload,
                extra={"ETag": etag, "Cache-Control": "private, max-age=0, must-revalidate"},
            )
            return
        if parsed.path == "/analysis-runs":
            query = parse_qs(parsed.query)
            limit = min(100, max(1, int(query.get("limit", ["20"])[0])))
            items = [
                {"id": f"run-{index:05d}", "status": "completed", "progress": 100}
                for index in range(limit)
            ]
            self._json(HTTPStatus.OK, {"items": items, "nextCursor": None})
            return
        if parsed.path == "/artifacts/artifact-1/content":
            if self.headers.get("If-None-Match") == ETAG:
                self.send_response(HTTPStatus.NOT_MODIFIED)
                self.send_header("ETag", ETAG)
                self.end_headers()
                return
            try:
                selected = _range(self.headers.get("Range"), len(ARTIFACT))
            except ValueError:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{len(ARTIFACT)}")
                self.end_headers()
                return
            start, end = selected if selected is not None else (0, len(ARTIFACT) - 1)
            body = ARTIFACT[start : end + 1]
            self.send_response(
                HTTPStatus.PARTIAL_CONTENT if selected is not None else HTTPStatus.OK
            )
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("ETag", ETAG)
            if selected is not None:
                self.send_header("Content-Range", f"bytes {start}-{end}/{len(ARTIFACT)}")
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/slow":
            delay = min(0.25, max(0.0, float(parse_qs(parsed.query).get("delay", ["0.02"])[0])))
            time.sleep(delay)
            self._json(HTTPStatus.OK, {"delaySeconds": delay})
            return
        self._json(HTTPStatus.NOT_FOUND, {"type": "about:blank", "status": 404})


def create_server(host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    server = create_server(port=8085)
    print("Course 5 lab server listening on http://127.0.0.1:8085", flush=True)
    server.serve_forever()
