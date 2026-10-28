from __future__ import annotations

import json
import socket
import ssl

from atlas_net.gateway import retry_allowed
from atlas_net.localnet import start_backend, start_tls_gateway
from common import ROOT, emit, record


def request_over_verified_tls(
    host: str,
    port: int,
    server_hostname: str,
    authority: str,
    ca_file: str,
) -> tuple[int, dict[str, object]]:
    """Send one HTTP/1.1 request over a verified TLS socket.

    The TCP destination is pinned to loopback while SNI and certificate hostname
    verification use ``server_hostname``. This separates name verification from
    local DNS without disabling either TLS check.
    """
    context = ssl.create_default_context(cafile=ca_file)
    with socket.create_connection((host, port), timeout=3) as raw:
        with context.wrap_socket(raw, server_hostname=server_hostname) as tls:
            request = (
                "GET /ready HTTP/1.1\r\n"
                f"Host: {authority}\r\n"
                "X-Forwarded-For: untrusted\r\n"
                "Connection: close\r\n\r\n"
            ).encode("ascii")
            tls.sendall(request)
            chunks: list[bytes] = []
            while True:
                chunk = tls.recv(65536)
                if not chunk:
                    break
                chunks.append(chunk)
    head, body = b"".join(chunks).split(b"\r\n\r\n", 1)
    status = int(head.split(b"\r\n", 1)[0].split()[1])
    return status, json.loads(body)


pki = ROOT / "pki"
backends = [start_backend(f"api-{suffix}") for suffix in "abc"]
gateway = None
try:
    gateway = start_tls_gateway(
        backends,
        str(pki / "atlas.crt"),
        str(pki / "atlas.key"),
    )

    wrong_hostname_rejected = False
    wrong_context = ssl.create_default_context(cafile=str(pki / "ca.crt"))
    try:
        with socket.create_connection(
            ("127.0.0.1", gateway.server.server_port), timeout=3
        ) as raw:
            with wrong_context.wrap_socket(raw, server_hostname="wrong.test"):
                pass
    except ssl.SSLCertVerificationError:
        wrong_hostname_rejected = True

    status, body = request_over_verified_tls(
        "127.0.0.1",
        gateway.server.server_port,
        "atlas.test",
        "atlas.test",
        str(pki / "ca.crt"),
    )

    emit(
        "module-08-tls-gateway.json",
        {
            "wrongHostnameRejected": wrong_hostname_rejected,
            "verifiedHostnameAccepted": True,
            "status": status,
            "backend": body,
            "retryWithoutKey": record(
                retry_allowed("POST", None, True, 500)
            ),
            "retryWithKey": record(
                retry_allowed("POST", "idem-1", True, 500)
            ),
            "evidenceBoundary": (
                "The successful request pinned the TCP destination to loopback "
                "while preserving CA-chain verification, SNI, certificate hostname "
                "verification for atlas.test, and HTTP authority enforcement."
            ),
        },
    )
finally:
    if gateway is not None:
        gateway.stop()
    for backend in backends:
        backend.stop()
