#!/usr/bin/env python3
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading
import time


class State:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.profile = os.getenv("FAULT_PROFILE", "healthy")
        self.calls = 0

    def update(self, profile: str) -> None:
        if profile not in {"healthy", "slow", "fail", "flaky", "drop"}:
            raise ValueError("unknown profile")
        with self.lock:
            self.profile = profile
            self.calls = 0

    def next(self) -> tuple[str, int]:
        with self.lock:
            self.calls += 1
            return self.profile, self.calls


STATE = State()


class Handler(BaseHTTPRequestHandler):
    server_version = "analysis-fault-injector/1.0"

    def do_GET(self) -> None:
        if self.path == "/health":
            self.respond(200, {"status": "ok"})
            return
        if self.path == "/state":
            profile, calls = STATE.next()
            self.respond(200, {"profile": profile, "calls": calls})
            return
        if self.path == "/dependency":
            profile, calls = STATE.next()
            if profile == "slow":
                time.sleep(2)
            if profile == "fail" or (profile == "flaky" and calls % 2 == 1):
                self.respond(503, {"error": "injected-unavailable", "call": calls})
                return
            if profile == "drop":
                self.connection.close()
                return
            self.respond(200, {"status": "ok", "call": calls})
            return
        self.respond(404, {"error": "not-found"})

    def do_POST(self) -> None:
        if self.path != "/control":
            self.respond(404, {"error": "not-found"})
            return
        if os.getenv("FAULT_CONTROL_ENABLED", "false").lower() != "true":
            self.respond(403, {"error": "fault-control-disabled"})
            return
        length = int(self.headers.get("content-length", "0"))
        try:
            payload = json.loads(self.rfile.read(length))
            STATE.update(str(payload["profile"]))
        except (ValueError, KeyError, json.JSONDecodeError):
            self.respond(422, {"error": "invalid-profile"})
            return
        self.respond(200, {"profile": STATE.profile})

    def respond(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8090), Handler).serve_forever()
