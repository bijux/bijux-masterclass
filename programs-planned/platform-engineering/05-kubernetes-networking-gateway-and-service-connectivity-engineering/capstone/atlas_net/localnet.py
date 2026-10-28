from __future__ import annotations

import http.client
import http.server
import json
import socketserver
import ssl
import threading
from dataclasses import dataclass

from .gateway import canonical_forwarded


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Small HTTP server used only by the dependency-light network laboratory."""

    daemon_threads = True


@dataclass
class RunningServer:
    """Own a server and its serving thread so cleanup remains explicit."""

    server: ThreadingHTTPServer
    thread: threading.Thread

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)


def start_backend(name: str, port: int = 0) -> RunningServer:
    """Start one loopback backend and return its lifecycle handle."""

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            payload = {
                "backend": name,
                "path": self.path,
                "forwarded": self.headers.get("Forwarded"),
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return RunningServer(server=server, thread=thread)


def start_tls_gateway(
    backends: list[RunningServer],
    certfile: str,
    keyfile: str,
    expected_host: str = "atlas.test",
    port: int = 0,
) -> RunningServer:
    """Start a verified-TLS teaching gateway over a bounded backend set."""

    if not backends:
        raise ValueError("at least one backend is required")

    counter = {"value": 0}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            authority = self.headers.get("Host", "").split(":", 1)[0]
            if authority != expected_host:
                self.send_error(421, "Misdirected Request")
                return

            backend = backends[counter["value"] % len(backends)]
            counter["value"] += 1
            headers = canonical_forwarded(
                self.client_address[0],
                "https",
                authority,
                dict(self.headers),
            )

            connection = http.client.HTTPConnection(
                "127.0.0.1",
                backend.server.server_port,
                timeout=2,
            )
            try:
                connection.request("GET", self.path, headers=headers)
                response = connection.getresponse()
                body = response.read()
            finally:
                connection.close()

            self.send_response(response.status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return RunningServer(server=server, thread=thread)
