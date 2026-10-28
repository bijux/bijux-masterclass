from __future__ import annotations

import contextlib
import http.client
import http.server
import json
import socket
import socketserver
import ssl
import struct
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


class BackendHandler(http.server.BaseHTTPRequestHandler):
    backend_name = "backend"
    ready = True

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        if self.path == "/live":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"live")
            return
        if self.path == "/ready":
            self.send_response(200 if self.ready else 503)
            self.end_headers()
            self.wfile.write(b"ready" if self.ready else b"not-ready")
            return
        if self.path.startswith("/api/"):
            body = json.dumps({
                "backend": self.backend_name,
                "forwardedFor": self.headers.get("X-Forwarded-For"),
                "forwardedProto": self.headers.get("X-Forwarded-Proto"),
                "host": self.headers.get("Host"),
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


@dataclass
class Backend:
    name: str
    port: int
    server: ThreadingHTTPServer
    thread: threading.Thread


class ServiceProxyHandler(http.server.BaseHTTPRequestHandler):
    backends: list[Backend] = []
    cursor = 0

    def log_message(self, format: str, *args) -> None:
        return

    @classmethod
    def eligible(cls) -> list[Backend]:
        result = []
        for backend in cls.backends:
            conn = http.client.HTTPConnection("127.0.0.1", backend.port, timeout=1)
            try:
                conn.request("GET", "/ready")
                response = conn.getresponse()
                response.read()
                if response.status == 200:
                    result.append(backend)
            except OSError:
                pass
            finally:
                conn.close()
        return result

    def do_GET(self) -> None:
        eligible = self.eligible()
        if not eligible:
            self.send_response(503)
            self.end_headers()
            return
        backend = eligible[self.__class__.cursor % len(eligible)]
        self.__class__.cursor += 1
        conn = http.client.HTTPConnection("127.0.0.1", backend.port, timeout=2)
        try:
            headers = {
                "Host": self.headers.get("Host", "atlas-api.atlas-system.svc"),
                "X-Forwarded-For": self.headers.get("X-Forwarded-For", self.client_address[0]),
                "X-Forwarded-Proto": self.headers.get("X-Forwarded-Proto", "http"),
            }
            conn.request("GET", self.path, headers=headers)
            response = conn.getresponse()
            body = response.read()
            self.send_response(response.status)
            for key, value in response.getheaders():
                if key.lower() not in {"connection", "transfer-encoding", "server", "date"}:
                    self.send_header(key, value)
            self.send_header("X-Atlas-Endpoint", backend.name)
            self.end_headers()
            self.wfile.write(body)
        finally:
            conn.close()


class GatewayHandler(http.server.BaseHTTPRequestHandler):
    service_port = 0

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        if self.headers.get("Host") not in {"atlas.example.invalid", "atlas.example.invalid:18443"}:
            self.send_response(421)
            self.end_headers()
            return
        if not self.path.startswith("/api/"):
            self.send_response(404)
            self.end_headers()
            return
        conn = http.client.HTTPConnection("127.0.0.1", self.service_port, timeout=2)
        try:
            # Replace, do not append, untrusted forwarding identity.
            headers = {
                "Host": "atlas-api.atlas-system.svc",
                "X-Forwarded-For": self.client_address[0],
                "X-Forwarded-Proto": "https",
            }
            conn.request("GET", self.path, headers=headers)
            response = conn.getresponse()
            body = response.read()
            self.send_response(response.status)
            for key, value in response.getheaders():
                if key.lower() not in {"connection", "transfer-encoding", "server", "date"}:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)
        finally:
            conn.close()


class MinimalDNSServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    daemon_threads = True
    records: dict[str, str] = {}


class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data, sock = self.request
        if len(data) < 12:
            return
        transaction_id = data[:2]
        flags = b"\x81\x80"
        qdcount = data[4:6]
        offset = 12
        labels = []
        while offset < len(data):
            length = data[offset]
            offset += 1
            if length == 0:
                break
            labels.append(data[offset:offset + length].decode("ascii"))
            offset += length
        if offset + 4 > len(data):
            return
        question = data[12:offset + 5]
        name = ".".join(labels).lower()
        address = self.server.records.get(name)
        if address is None:
            header = transaction_id + b"\x81\x83" + qdcount + b"\x00\x00\x00\x00\x00\x00"
            sock.sendto(header + question, self.client_address)
            return
        header = transaction_id + flags + qdcount + b"\x00\x01\x00\x00\x00\x00"
        answer = b"\xc0\x0c" + b"\x00\x01\x00\x01" + struct.pack("!I", 30) + b"\x00\x04" + socket.inet_aton(address)
        sock.sendto(header + question + answer, self.client_address)


def dns_query(server_port: int, name: str) -> tuple[str, tuple[str, ...]]:
    transaction_id = b"\x12\x34"
    labels = b"".join(bytes([len(part)]) + part.encode("ascii") for part in name.rstrip(".").split(".")) + b"\x00"
    query = transaction_id + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + labels + b"\x00\x01\x00\x01"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(query, ("127.0.0.1", server_port))
        response, _ = sock.recvfrom(512)
    rcode = response[3] & 0x0F
    if rcode == 3:
        return "NXDOMAIN", ()
    answer_count = int.from_bytes(response[6:8], "big")
    if answer_count != 1:
        return "NOERROR", ()
    address = socket.inet_ntoa(response[-4:])
    return "NOERROR", (address,)


@contextlib.contextmanager
def run_lab(pki_dir: Path) -> Iterator[dict[str, object]]:
    backends: list[Backend] = []
    for index in range(1, 3):
        handler = type(f"Backend{index}Handler", (BackendHandler,), {"backend_name": f"api-{index}", "ready": True})
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        backends.append(Backend(f"api-{index}", server.server_port, server, thread))

    ServiceProxyHandler.backends = backends
    ServiceProxyHandler.cursor = 0
    service = ThreadingHTTPServer(("127.0.0.1", 0), ServiceProxyHandler)
    service_thread = threading.Thread(target=service.serve_forever, daemon=True)
    service_thread.start()

    GatewayHandler.service_port = service.server_port
    gateway = ThreadingHTTPServer(("127.0.0.1", 0), GatewayHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(pki_dir / "atlas.crt", pki_dir / "atlas.key")
    gateway.socket = context.wrap_socket(gateway.socket, server_side=True)
    gateway_thread = threading.Thread(target=gateway.serve_forever, daemon=True)
    gateway_thread.start()

    dns = MinimalDNSServer(("127.0.0.1", 0), DNSHandler)
    dns.records = {"atlas-api.atlas-system.svc.cluster.local": "127.0.0.1"}
    dns_thread = threading.Thread(target=dns.serve_forever, daemon=True)
    dns_thread.start()

    time.sleep(0.1)
    state = {
        "backends": backends,
        "service": service,
        "gateway": gateway,
        "dns": dns,
        "servicePort": service.server_port,
        "gatewayPort": gateway.server_port,
        "dnsPort": dns.server_address[1],
    }
    try:
        yield state
    finally:
        for server in (dns, gateway, service, *(backend.server for backend in backends)):
            server.shutdown()
            server.server_close()
        for thread in (dns_thread, gateway_thread, service_thread, *(backend.thread for backend in backends)):
            thread.join(timeout=2)
