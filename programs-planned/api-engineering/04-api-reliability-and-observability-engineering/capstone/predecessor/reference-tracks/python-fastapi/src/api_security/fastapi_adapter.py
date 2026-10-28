from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .errors import SecurityControlError
from .strict_json import parse_strict_json


class StrictJsonMiddleware:
    """Own JSON bytes before FastAPI/Pydantic parses them.

    The middleware consumes the ASGI body under a hard limit, validates the
    strict JSON profile, then replays the original bytes. It does not modify
    Starlette private request attributes.
    """

    def __init__(self, app: Callable[..., Awaitable[None]], max_bytes: int = 1_048_576) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: dict[str, Any], receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = {k.decode("latin1").lower(): v.decode("latin1") for k, v in scope.get("headers", [])}
        content_type = headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if content_type not in {"application/json", "application/problem+json"}:
            await self.app(scope, receive, send)
            return
        body = bytearray()
        more = True
        while more:
            message = await receive()
            if message["type"] != "http.request":
                continue
            body.extend(message.get("body", b""))
            if len(body) > self.max_bytes:
                await _problem(send, 413, "body-too-large", "JSON body exceeds the configured limit")
                return
            more = bool(message.get("more_body", False))
        try:
            parsed = parse_strict_json(bytes(body), max_bytes=self.max_bytes)
        except SecurityControlError as exc:
            await _problem(send, exc.status, exc.code, exc.detail)
            return
        scope.setdefault("state", {})["strict_json"] = parsed
        replayed = False

        async def replay_receive():
            nonlocal replayed
            if replayed:
                return {"type": "http.request", "body": b"", "more_body": False}
            replayed = True
            return {"type": "http.request", "body": bytes(body), "more_body": False}

        await self.app(scope, replay_receive, send)


async def _problem(send, status: int, code: str, detail: str) -> None:
    body = (f'{{"type":"urn:analysis-security:{code}","title":"Request rejected","status":{status},"detail":{detail!r}}}').encode("utf-8")
    # Use JSONResponse serialization for normal endpoints; this narrow ASGI
    # path avoids reflecting the hostile body and keeps a bounded message.
    import json
    payload = json.dumps({"type": f"urn:analysis-security:{code}", "title": "Request rejected", "status": status, "detail": detail}).encode("utf-8")
    await send({"type": "http.response.start", "status": status, "headers": [(b"content-type", b"application/problem+json"), (b"content-length", str(len(payload)).encode("ascii"))]})
    await send({"type": "http.response.body", "body": payload})


def create_security_demo_app() -> FastAPI:
    app = FastAPI(title="Analysis Runs Security Adapter", version="1.0.0")
    app.add_middleware(StrictJsonMiddleware)

    @app.get("/security/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/security/strict-json")
    async def strict_json_echo(request: Request) -> JSONResponse:
        value = request.scope.get("state", {}).get("strict_json")
        return JSONResponse({"accepted": True, "value": value})

    return app
