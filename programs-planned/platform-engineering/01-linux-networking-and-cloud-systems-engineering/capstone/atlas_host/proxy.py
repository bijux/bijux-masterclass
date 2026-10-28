from __future__ import annotations

import argparse
import http.client
import json
import signal
import ssl
import threading
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .atomic_store import atomic_write_json
from .config import AtlasConfig
from .events import append

HOP_BY_HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"}
FORWARDED = {"forwarded", "x-forwarded-for", "x-forwarded-host", "x-forwarded-proto", "x-real-ip"}


@dataclass(frozen=True)
class Backend:
    host: str
    port: int


class EdgeServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], config: AtlasConfig, backends: list[Backend]):
        self.config = config
        self.backends = backends
        self.cursor = 0
        super().__init__(address, EdgeHandler)

    def next_backends(self) -> list[Backend]:
        if not self.backends:
            return []
        start = self.cursor % len(self.backends)
        self.cursor += 1
        return self.backends[start:] + self.backends[:start]


class EdgeHandler(BaseHTTPRequestHandler):
    server: EdgeServer
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: object) -> None:
        append(self.server.config.evidence_file, "edge.access", client=self.client_address[0], message=format % args)

    def _problem(self, status: int, code: str) -> None:
        body = json.dumps({"error": code}, separators=(",", ":")).encode() + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def _forward(self) -> None:
        host_header = self.headers.get("Host", "").split(":", 1)[0].lower()
        allowed = {self.server.config.public_name.lower(), "localhost", "127.0.0.1", "::1"}
        if host_header not in allowed:
            self._problem(HTTPStatus.MISDIRECTED_REQUEST, "host-not-allowed")
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._problem(HTTPStatus.BAD_REQUEST, "invalid-content-length")
            return
        if content_length > self.server.config.max_body_bytes:
            self._problem(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "body-size")
            return
        body = self.rfile.read(content_length) if content_length else None
        headers: dict[str, str] = {}
        for name, value in self.headers.items():
            low = name.lower()
            if low in HOP_BY_HOP or low in FORWARDED or low in {"host", "content-length"}:
                continue
            headers[name] = value
        headers["Host"] = self.server.config.public_name
        headers["X-Forwarded-For"] = self.client_address[0]
        headers["X-Forwarded-Proto"] = "https"
        append(
            self.server.config.evidence_file,
            "edge.forward",
            client=self.client_address[0],
            forwarded_for=headers["X-Forwarded-For"],
            discarded_forwarded=any(name.lower() in FORWARDED for name in self.headers),
            method=self.command,
            request_path=urlsplit(self.path).path,
        )
        if body is not None:
            headers["Content-Length"] = str(len(body))

        retryable = self.command in {"GET", "HEAD"}
        candidates = self.server.next_backends()
        attempts = candidates if retryable else candidates[:1]
        for backend in attempts:
            conn = http.client.HTTPConnection(backend.host, backend.port, timeout=2.0)
            try:
                conn.request(self.command, self.path, body=body, headers=headers)
                response = conn.getresponse()
                data = response.read()
            except OSError as exc:
                append(self.server.config.evidence_file, "edge.backend_failure", backend=f"{backend.host}:{backend.port}", error=type(exc).__name__)
                continue
            finally:
                conn.close()
            self.send_response(response.status)
            for name, value in response.getheaders():
                if name.lower() in HOP_BY_HOP or name.lower() == "server":
                    continue
                self.send_header(name, value)
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)
            return
        self._problem(HTTPStatus.SERVICE_UNAVAILABLE, "backend-unavailable")

    do_GET = _forward  # type: ignore[assignment]
    do_POST = _forward  # type: ignore[assignment]
    do_HEAD = _forward  # type: ignore[assignment]


def run(config: AtlasConfig, cert: Path, key: Path, backends: list[Backend]) -> int:
    config.prepare()
    server = EdgeServer((config.edge_host, config.edge_port), config, backends)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(certfile=cert, keyfile=key)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    port = int(server.server_address[1])
    atomic_write_json(config.runtime_dir / "edge.json", {"pid": __import__("os").getpid(), "host": config.edge_host, "port": port}, mode=0o640)
    stop = threading.Event()

    def handle_signal(signum: int, _frame: object) -> None:
        append(config.evidence_file, "edge.signal", signal=signum)
        stop.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    server.timeout = 0.25
    append(config.evidence_file, "edge.started", host=config.edge_host, port=port)
    try:
        while not stop.is_set():
            server.handle_request()
    finally:
        server.server_close()
        append(config.evidence_file, "edge.stopped")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--backend", action="append", required=True, help="host:port")
    args = parser.parse_args()
    backends = [Backend(host=value.rsplit(":", 1)[0], port=int(value.rsplit(":", 1)[1])) for value in args.backend]
    return run(AtlasConfig.from_json(args.config), args.cert, args.key, backends)


if __name__ == "__main__":
    raise SystemExit(main())
