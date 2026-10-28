from __future__ import annotations

import json
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import ClassVar

from api_security.errors import SecurityControlError
from api_security.secrets import SecretBytes
from api_security.webhooks import MemoryReplayStore, verify_webhook


@dataclass(slots=True)
class ReceiverState:
    keys: dict[str, SecretBytes]
    now: int
    replay: MemoryReplayStore = field(default_factory=MemoryReplayStore)
    accepted: list[dict[str, object]] = field(default_factory=list)


class ReceiverHandler(BaseHTTPRequestHandler):
    state: ClassVar[ReceiverState]

    def do_POST(self) -> None:  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > 1_048_576:
                raise SecurityControlError("body-too-large", "webhook body exceeds receiver limit", 413)
            body = self.rfile.read(length)
            timestamp = int(self.headers["X-Analysis-Timestamp"])
            delivery_id = self.headers["X-Analysis-Delivery"]
            key_id = self.headers["X-Analysis-Key-Id"]
            signature = self.headers["X-Analysis-Signature"]
            verify_webhook(
                body=body,
                timestamp=timestamp,
                delivery_id=delivery_id,
                key_id=key_id,
                signature=signature,
                now=self.state.now,
                keys=self.state.keys,
                replay=self.state.replay,
            )
            event = json.loads(body)
            self.state.accepted.append({"deliveryId": delivery_id, "event": event})
            self.send_response(204)
            self.end_headers()
        except (KeyError, ValueError, json.JSONDecodeError, SecurityControlError) as exc:
            status = exc.status if isinstance(exc, SecurityControlError) else 400
            payload = json.dumps({"type": "urn:analysis-security:webhook-rejected", "title": "Webhook rejected", "status": status}).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/problem+json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(state: ReceiverState, host: str = "127.0.0.1", port: int = 8099) -> None:
    ReceiverHandler.state = state
    ThreadingHTTPServer((host, port), ReceiverHandler).serve_forever()
