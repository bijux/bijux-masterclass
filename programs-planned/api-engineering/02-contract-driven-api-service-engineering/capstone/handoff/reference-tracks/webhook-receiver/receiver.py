from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest, new as hmac_new
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import json
import os
import sqlite3
import time


@dataclass(frozen=True, slots=True)
class Config:
    host: str = os.getenv("RECEIVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("RECEIVER_PORT", "8080"))
    database: Path = Path(os.getenv("RECEIVER_DATABASE", ".runtime/receiver.sqlite3")).resolve()
    default_secret: str = os.getenv("RECEIVER_SECRET", "course-callback-signing-secret")
    maximum_body: int = int(os.getenv("RECEIVER_MAXIMUM_BODY", "1048576"))
    maximum_skew_seconds: int = int(os.getenv("RECEIVER_MAXIMUM_SKEW_SECONDS", "300"))


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute(
                """CREATE TABLE IF NOT EXISTS receipts(
                    event_id TEXT PRIMARY KEY,
                    body_sha256 TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    target_path TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    first_received_at REAL NOT NULL,
                    last_received_at REAL NOT NULL,
                    delivery_count INTEGER NOT NULL
                )"""
            )
            db.execute(
                """CREATE TABLE IF NOT EXISTS attempts(
                    position INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT,
                    body_sha256 TEXT,
                    accepted INTEGER NOT NULL,
                    status INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    occurred_at REAL NOT NULL
                )"""
            )

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path, timeout=10, isolation_level="IMMEDIATE")

    def record_attempt(self, event_id: str | None, digest: str | None, accepted: bool, status: int, reason: str) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO attempts(event_id,body_sha256,accepted,status,reason,occurred_at) VALUES(?,?,?,?,?,?)",
                (event_id, digest, int(accepted), status, reason, time.time()),
            )

    def accept(self, event_id: str, digest: str, signature: str, timestamp: int, path: str, payload: dict) -> tuple[int, str]:
        now = time.time()
        with self.connect() as db:
            current = db.execute(
                "SELECT body_sha256,delivery_count FROM receipts WHERE event_id=?", (event_id,)
            ).fetchone()
            if current:
                if current[0] != digest:
                    return 409, "same event identifier was reused with different bytes"
                db.execute(
                    "UPDATE receipts SET delivery_count=delivery_count+1,last_received_at=? WHERE event_id=?",
                    (now, event_id),
                )
                return 200, "duplicate delivery accepted idempotently"
            db.execute(
                "INSERT INTO receipts VALUES(?,?,?,?,?,?,?,?,1)",
                (
                    event_id,
                    digest,
                    signature,
                    timestamp,
                    path,
                    json.dumps(payload, separators=(",", ":"), sort_keys=True),
                    now,
                    now,
                ),
            )
            return 202, "delivery stored"

    def receipts(self) -> list[dict]:
        with self.connect() as db:
            db.row_factory = sqlite3.Row
            return [
                dict(row)
                for row in db.execute(
                    "SELECT event_id,body_sha256,target_path,first_received_at,last_received_at,delivery_count "
                    "FROM receipts ORDER BY first_received_at"
                )
            ]

    def receipt_count(self, event_id: str) -> int:
        with self.connect() as db:
            row = db.execute("SELECT delivery_count FROM receipts WHERE event_id=?", (event_id,)).fetchone()
            return int(row[0]) if row else 0

    def attempt_count(self, event_id: str) -> int:
        with self.connect() as db:
            row = db.execute("SELECT count(*) FROM attempts WHERE event_id=?", (event_id,)).fetchone()
            return int(row[0])

    def reset(self) -> None:
        with self.connect() as db:
            db.execute("DELETE FROM attempts")
            db.execute("DELETE FROM receipts")


CONFIG = Config()
STORE = Store(CONFIG.database)


def verify_signature(secret: str, timestamp: str, body: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac_new(secret.encode(), timestamp.encode() + b"." + body, "sha256").hexdigest()
    return compare_digest(expected, signature)


class Handler(BaseHTTPRequestHandler):
    server_version = "CDSEWebhookReceiver/1.0"

    def _json(self, status: int, payload: object) -> None:
        data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if status != 204:
            self.wfile.write(data)

    def _body(self) -> bytes:
        raw = self.headers.get("Content-Length")
        if raw is None:
            raise ValueError("Content-Length is required")
        length = int(raw)
        if length < 1 or length > CONFIG.maximum_body:
            raise ValueError("body length is outside receiver limits")
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError("request body ended early")
        return body

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/health":
            self._json(200, {"status": "ok", "service": "course-webhook-receiver"})
            return
        if path == "/deliveries":
            self._json(200, {"items": STORE.receipts()})
            return
        self._json(404, {"error": "not-found"})

    def do_DELETE(self) -> None:
        if urlsplit(self.path).path != "/deliveries":
            self._json(404, {"error": "not-found"})
            return
        STORE.reset()
        self._json(204, {})

    def do_POST(self) -> None:
        parsed = urlsplit(self.path)
        event_id = self.headers.get("X-Event-Id")
        timestamp = self.headers.get("X-Webhook-Timestamp")
        signature = self.headers.get("X-Webhook-Signature")
        try:
            body = self._body()
        except Exception as exc:
            STORE.record_attempt(event_id, None, False, 400, str(exc))
            self._json(400, {"error": str(exc)})
            return
        digest = sha256(body).hexdigest()
        try:
            payload = json.loads(body)
            if not isinstance(payload, dict):
                raise ValueError("webhook body must be a JSON object")
            if not event_id or event_id != payload.get("eventId"):
                raise ValueError("X-Event-Id must equal payload.eventId")
            if not timestamp or abs(int(time.time()) - int(timestamp)) > CONFIG.maximum_skew_seconds:
                raise ValueError("webhook timestamp is missing, invalid, or stale")
            if not signature or not verify_signature(CONFIG.default_secret, timestamp, body, signature):
                raise PermissionError("webhook signature is invalid")
            query = parse_qs(parsed.query)
            fail_first = int(query.get("fail_first", ["0"])[0])
            forced = int(query.get("status", ["0"])[0])
            if STORE.attempt_count(event_id) < fail_first:
                STORE.record_attempt(event_id, digest, False, 503, "planned transient failure")
                self._json(503, {"error": "planned-transient-failure"})
                return
            if forced and not 200 <= forced < 300:
                STORE.record_attempt(event_id, digest, False, forced, "forced status")
                self._json(forced, {"error": "forced-status"})
                return
            status, message = STORE.accept(event_id, digest, signature, int(timestamp), parsed.path, payload)
            STORE.record_attempt(event_id, digest, status < 300, status, message)
            self._json(status, {"eventId": event_id, "message": message})
        except PermissionError as exc:
            STORE.record_attempt(event_id, digest, False, 401, str(exc))
            self._json(401, {"error": str(exc)})
        except Exception as exc:
            STORE.record_attempt(event_id, digest, False, 400, str(exc))
            self._json(400, {"error": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        print(
            json.dumps(
                {
                    "component": "webhook-receiver",
                    "client": self.client_address[0],
                    "message": format % args,
                },
                separators=(",", ":"),
            )
        )


def main() -> None:
    server = ThreadingHTTPServer((CONFIG.host, CONFIG.port), Handler)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
