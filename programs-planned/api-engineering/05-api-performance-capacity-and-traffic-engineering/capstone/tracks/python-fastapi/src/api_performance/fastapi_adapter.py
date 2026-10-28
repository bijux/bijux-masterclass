"""Illustrative FastAPI adapter for Course 5 controls.

Importing this module requires the pinned FastAPI environment. Core proofs do
not import it; the course first proves the framework-independent mechanism.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from .admission import AdmissionController, AdmissionRejected


def install_performance_boundary(
    app: FastAPI,
    controller: AdmissionController,
) -> None:
    @app.middleware("http")
    async def bounded_request(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        operation = request.scope.get("route")
        operation_id = getattr(operation, "name", None) or request.url.path
        started = time.perf_counter_ns()
        try:
            async with controller.acquire(str(operation_id)):
                response = await call_next(request)
        except AdmissionRejected as exc:
            return JSONResponse(
                status_code=exc.status,
                headers={"Retry-After": str(exc.retry_after_seconds)},
                content={
                    "type": "urn:analysis:problem:overloaded",
                    "title": "Request cannot be admitted now",
                    "status": exc.status,
                },
            )
        elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
        response.headers["Server-Timing"] = f"app;dur={elapsed_ms:.3f}"
        response.headers["X-Performance-Profile"] = "1.0"
        return response
