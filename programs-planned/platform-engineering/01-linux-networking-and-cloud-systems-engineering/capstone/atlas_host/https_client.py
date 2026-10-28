from __future__ import annotations

import http.client
import socket
import ssl


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    """Connect to one address while authenticating a different logical name.

    This is the programmatic equivalent of curl's --resolve for the local
    course laboratory. It preserves SNI and hostname verification for the
    logical host instead of weakening TLS or relying on workstation DNS.
    """

    def __init__(
        self,
        logical_host: str,
        port: int,
        *,
        connect_host: str,
        context: ssl.SSLContext,
        timeout: float = 3.0,
    ) -> None:
        super().__init__(logical_host, port, context=context, timeout=timeout)
        self.connect_host = connect_host

    def connect(self) -> None:
        raw = socket.create_connection(
            (self.connect_host, self.port),
            self.timeout,
            self.source_address,
        )
        if self._tunnel_host:
            self.sock = raw
            self._tunnel()
            raw = self.sock
        self.sock = self._context.wrap_socket(
            raw,
            server_hostname=self.host,
        )
