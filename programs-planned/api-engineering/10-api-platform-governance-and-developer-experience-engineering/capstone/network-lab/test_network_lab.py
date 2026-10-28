from __future__ import annotations

import json
from pathlib import Path
import sys
from threading import Thread
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from platform_server import PlatformServer


def request(base: str, path: str, *, method="GET", body=None, headers=None):
    data = None if body is None else json.dumps(body).encode()
    req = Request(base + path, data=data, method=method, headers=headers or {})
    if data is not None:
        req.add_header("Content-Type", "application/json")
        req.add_header("Content-Length", str(len(data)))
    with urlopen(req, timeout=3) as response:
        return response.status, json.loads(response.read())


def test_platform_network_lab():
    server = PlatformServer()
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        status, health = request(base, "/health")
        assert status == 200 and health["status"] == "ok"

        _, entities = request(base, "/entities?kind=api")
        assert len(entities["items"]) == 7
        assert all(item["owner"] for item in entities["items"])

        ref = quote("api:default/platform-catalog", safe="")
        _, product = request(base, f"/apis/{ref}")
        assert product["owner"] == "group:default/api-platform-team"
        assert product["releases"][0]["version"] == "1.0.0"

        _, card = request(base, f"/scorecards/{ref}")
        assert card["status"] == "ready"

        _, results = request(base, "/search?q=sandbox")
        assert results["items"]

        status, session = request(
            base,
            "/sandboxes",
            method="POST",
            body={"nonce": "network-proof"},
            headers={"X-Subject": "course10-network-test"},
        )
        assert status == 201
        assert session["dataClass"] == "synthetic-only"
        assert session["tenant"].startswith("sandbox-")

        _, drift = request(base, "/runtime/drift")
        assert drift["inSync"] is True

        _, support = request(base, "/support/route?category=portal-registry-template")
        assert support["owner"] == "group:default/api-platform-team"

        try:
            request(base, "/search?q=x")
            raise AssertionError("short search query should fail")
        except HTTPError as exc:
            assert exc.code == 400
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
