from __future__ import annotations

import argparse
import json
import signal
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .atomic_store import atomic_write_json
from .config import AtlasConfig
from .events import append
from .health import worker_heartbeat, writable_directory
from .spool import FileSpool


class AtlasHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], config: AtlasConfig):
        self.config = config
        self.spool = FileSpool(config.spool_dir)
        super().__init__(address, AtlasHandler)


class AtlasHandler(BaseHTTPRequestHandler):
    server: AtlasHTTPServer
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: object) -> None:
        append(self.server.config.evidence_file, "http.access", client=self.client_address[0], message=format % args)

    def _json(self, status: int, body: dict[str, object]) -> None:
        data = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health/live":
            self._json(HTTPStatus.OK, {"status": "live"})
            return
        if path == "/health/ready":
            writable, storage_detail = writable_directory(self.server.config.spool_dir)
            worker_ok, worker_detail = worker_heartbeat(self.server.config.runtime_dir)
            ready = writable and worker_ok
            self._json(
                HTTPStatus.OK if ready else HTTPStatus.SERVICE_UNAVAILABLE,
                {
                    "status": "ready" if ready else "not-ready",
                    "checks": {"storage": storage_detail, "worker": worker_detail},
                },
            )
            return
        if path.startswith("/jobs/"):
            job_id = path.rsplit("/", 1)[-1]
            state = self.server.spool.status(job_id)
            if state is None:
                self._json(HTTPStatus.NOT_FOUND, {"error": "job-not-found"})
            else:
                self._json(HTTPStatus.OK, state)
            return
        self._json(HTTPStatus.NOT_FOUND, {"error": "not-found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/jobs":
            self._json(HTTPStatus.NOT_FOUND, {"error": "not-found"})
            return
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "content-type"})
            return
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if length < 0 or length > self.server.config.max_body_bytes:
            self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "body-size"})
            return
        try:
            body = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid-json"})
            return
        if not isinstance(body, dict) or not isinstance(body.get("text"), str):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid-job"})
            return
        job_id = self.server.spool.submit({"text": body["text"]})
        append(self.server.config.evidence_file, "job.submitted", job_id=job_id)
        self._json(HTTPStatus.ACCEPTED, {"jobId": job_id, "statusUrl": f"/jobs/{job_id}"})


def run(config: AtlasConfig) -> int:
    config.prepare()
    server = AtlasHTTPServer((config.api_host, config.api_port), config)
    port = int(server.server_address[1])
    atomic_write_json(config.runtime_dir / "api.json", {"pid": __import__("os").getpid(), "host": config.api_host, "port": port}, mode=0o640)
    stop = threading.Event()

    def handle_signal(signum: int, _frame: object) -> None:
        append(config.evidence_file, "api.signal", signal=signum)
        stop.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    server.timeout = 0.25
    append(config.evidence_file, "api.started", host=config.api_host, port=port)
    try:
        while not stop.is_set():
            server.handle_request()
    finally:
        server.server_close()
        append(config.evidence_file, "api.stopped")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    return run(AtlasConfig.from_json(args.config))


if __name__ == "__main__":
    raise SystemExit(main())
