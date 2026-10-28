from __future__ import annotations

import http.client
import json
from pathlib import Path
import socket
import ssl
import unittest

from atlas_net.network_lab import dns_query, run_lab


class NetworkLabTests(unittest.TestCase):
    def test_loopback_dns_service_and_tls_gateway(self) -> None:
        pki = Path(__file__).resolve().parents[1] / "pki"
        with run_lab(pki) as state:
            dns_port = int(state["dnsPort"])
            service_port = int(state["servicePort"])
            gateway_port = int(state["gatewayPort"])

            rcode, values = dns_query(
                dns_port,
                "atlas-api.atlas-system.svc.cluster.local",
            )
            self.assertEqual((rcode, values), ("NOERROR", ("127.0.0.1",)))
            self.assertEqual(
                dns_query(
                    dns_port,
                    "missing.atlas-system.svc.cluster.local",
                )[0],
                "NXDOMAIN",
            )

            context = ssl.create_default_context(cafile=str(pki / "ca.crt"))
            raw_socket = socket.create_connection(("127.0.0.1", gateway_port))
            tls_socket = context.wrap_socket(
                raw_socket,
                server_hostname="atlas.example.invalid",
            )
            request = (
                "GET /api/whoami HTTP/1.1\r\n"
                "Host: atlas.example.invalid\r\n"
                "X-Forwarded-For: 203.0.113.77\r\n"
                "Connection: close\r\n\r\n"
            ).encode("ascii")
            tls_socket.sendall(request)
            raw = b""
            while True:
                chunk = tls_socket.recv(65536)
                if not chunk:
                    break
                raw += chunk
            tls_socket.close()

            self.assertIn(b"200 OK", raw)
            payload = json.loads(raw.split(b"\r\n\r\n", 1)[1])
            self.assertEqual(payload["forwardedFor"], "127.0.0.1")
            self.assertEqual(payload["forwardedProto"], "https")
            self.assertEqual(payload["host"], "atlas-api.atlas-system.svc")

            seen: set[str | None] = set()
            for _ in range(4):
                connection = http.client.HTTPConnection(
                    "127.0.0.1",
                    service_port,
                    timeout=2,
                )
                connection.request("GET", "/api/whoami")
                response = connection.getresponse()
                response.read()
                seen.add(response.getheader("X-Atlas-Endpoint"))
                connection.close()
            self.assertEqual(seen, {"api-1", "api-2"})

            state["backends"][0].server.RequestHandlerClass.ready = False
            selected: set[str | None] = set()
            for _ in range(3):
                connection = http.client.HTTPConnection(
                    "127.0.0.1",
                    service_port,
                    timeout=2,
                )
                connection.request("GET", "/api/whoami")
                response = connection.getresponse()
                response.read()
                selected.add(response.getheader("X-Atlas-Endpoint"))
                connection.close()
            self.assertEqual(selected, {"api-2"})


if __name__ == "__main__":
    unittest.main()
