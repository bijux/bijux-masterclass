#!/usr/bin/env python3
"""Dependency-light loopback server for Analysis Platform API concepts.

This is an executable teaching adapter, not an operated platform service. It
exercises real HTTP parsing and response behavior while delegating governance
semantics to the readable Python core.
"""
from __future__ import annotations

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, unquote, urlparse

CAP = Path(__file__).resolve().parents[1]
PY_SRC = CAP / "tracks/python-platform/src"
sys.path.insert(0, str(PY_SRC))

from analysis_platform.catalog import Catalog, CatalogError
from analysis_platform.portal import build_search_index, search
from analysis_platform.registry import ContractRegistry
from analysis_platform.runtime import route_drift
from analysis_platform.sandbox import create_session
from analysis_platform.scorecards import scorecard
from analysis_platform.support import route_ticket


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PlatformState:
    def __init__(self, capstone: Path = CAP):
        self.capstone = capstone
        self.catalog = Catalog.from_records(read_json(capstone / "catalog/entities.json")["entities"])
        self.registry = ContractRegistry.from_records(read_json(capstone / "registry/releases.json")["releases"])
        self.evidence = read_json(capstone / "governance/evidence-ledger.json")["evidence"]
        self.search_index = build_search_index(capstone / "docs/source")
        self.sandbox_profile = read_json(capstone / "sandbox/profile.json")
        self.support_routes = read_json(capstone / "support/routes.json")["routes"]


class Handler(BaseHTTPRequestHandler):
    server_version = "AnalysisPlatformLab/1.0"

    @property
    def state(self) -> PlatformState:
        return self.server.state  # type: ignore[attr-defined]

    def log_message(self, format: str, *args) -> None:
        return

    def _json(self, status: int, payload) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self, limit: int = 4096):
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ValueError("content-length-required")
        length = int(raw_length)
        if length < 0 or length > limit:
            raise ValueError("body-too-large")
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/health":
            self._json(200, {"status": "ok", "profile": "dependency-light-lab"})
            return
        if parsed.path == "/entities":
            kind = query.get("kind", [None])[0]
            owner = query.get("owner", [None])[0]
            items = []
            for ref, entity in sorted(self.state.catalog.entities.items()):
                if kind and entity.kind != kind.lower():
                    continue
                if owner and entity.owner != owner:
                    continue
                items.append({
                    "ref": ref, "kind": entity.kind, "name": entity.name,
                    "title": entity.title, "owner": entity.owner,
                    "lifecycle": entity.lifecycle,
                })
            self._json(200, {"items": items})
            return
        if parsed.path.startswith("/apis/"):
            api_ref = unquote(parsed.path[len("/apis/"):])
            try:
                entity = self.state.catalog.get(api_ref)
            except CatalogError:
                self._json(404, {"code": "api-not-found"})
                return
            if entity.kind != "api":
                self._json(404, {"code": "api-not-found"})
                return
            releases = [
                {"version": release.version, "protocol": release.protocol,
                 "sha256": release.sha256, "lifecycle": release.lifecycle}
                for (ref, _), release in sorted(self.state.registry.releases.items())
                if ref == api_ref
            ]
            self._json(200, {"apiRef": api_ref, "owner": entity.owner, "releases": releases})
            return
        if parsed.path.startswith("/scorecards/"):
            entity_ref = unquote(parsed.path[len("/scorecards/"):])
            self._json(200, scorecard(entity_ref, self.state.evidence))
            return
        if parsed.path == "/search":
            term = query.get("q", [""])[0].strip()
            if len(term) < 2:
                self._json(400, {"code": "invalid-query"})
                return
            results = search(self.state.search_index, term)[:50]
            self._json(200, {"items": [{"path": x["path"], "title": x["title"]} for x in results]})
            return
        if parsed.path == "/runtime/drift":
            desired = read_json(self.state.capstone / "runtime/desired-routes.json")["routes"]
            current = read_json(self.state.capstone / "runtime/current-routes.json")["routes"]
            self._json(200, route_drift(desired, current))
            return
        if parsed.path == "/support/route":
            category = query.get("category", [""])[0]
            try:
                owner = route_ticket(
                    category,
                    self.state.support_routes,
                    catalog_owner="group:default/analysis-control-team",
                )
            except ValueError as exc:
                self._json(400, {"code": str(exc)})
                return
            self._json(200, {"owner": owner})
            return
        self._json(404, {"code": "route-not-found"})

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/sandboxes":
            self._json(404, {"code": "route-not-found"})
            return
        try:
            payload = self._read_json()
            nonce = str(payload["nonce"])
            if not nonce or len(nonce) > 128:
                raise ValueError("invalid-nonce")
            subject = self.headers.get("X-Subject", "network-lab-consumer")
            session = create_session(
                subject=subject,
                nonce=nonce,
                now=datetime(2026, 8, 8, 10, 0, tzinfo=timezone.utc),
                profile=self.state.sandbox_profile,
            )
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            self._json(400, {"code": str(exc)})
            return
        self._json(201, {
            "id": session.id,
            "tenant": session.tenant,
            "expiresAt": session.expires_at.isoformat(),
            "credentialExpiresAt": session.credential_expires_at.isoformat(),
            "dataClass": session.data_class,
        })


class PlatformServer(ThreadingHTTPServer):
    def __init__(self, address=("127.0.0.1", 0), state: PlatformState | None = None):
        super().__init__(address, Handler)
        self.state = state or PlatformState()


def main() -> None:
    server = PlatformServer(("127.0.0.1", 8787))
    print("Analysis Platform lab listening on http://127.0.0.1:8787")
    server.serve_forever()


if __name__ == "__main__":
    main()
