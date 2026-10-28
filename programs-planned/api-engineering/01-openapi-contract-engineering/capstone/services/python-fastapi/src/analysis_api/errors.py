from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@dataclass
class ApiProblem(Exception):
    status: int
    title: str
    detail: str
    slug: str
    errors: list[dict[str, Any]] | None = None

    def __str__(self) -> str:
        return self.detail


def request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "req_000000000000")


def problem_payload(request: Request, problem: ApiProblem) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": f"https://api.example.test/problems/{problem.slug}",
        "title": problem.title,
        "status": problem.status,
        "detail": problem.detail,
        "instance": request.url.path,
        "requestId": request_id(request),
    }
    if problem.status == 422:
        payload["errors"] = problem.errors or [
            {
                "location": ["body"],
                "message": problem.detail,
                "code": "validation_error",
            }
        ]
    return payload


async def api_problem_handler(request: Request, exc: ApiProblem) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content=problem_payload(request, exc),
        media_type="application/problem+json",
        headers={"X-Request-Id": request_id(request)},
    )


async def validation_problem_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "location": list(error.get("loc", [])),
                "message": str(error.get("msg", "Invalid value")),
                "code": str(error.get("type", "validation_error")),
            }
        )
    payload = {
        "type": "https://api.example.test/problems/validation",
        "title": "Request validation failed",
        "status": 422,
        "detail": "One or more request values are invalid.",
        "instance": request.url.path,
        "requestId": request_id(request),
        "errors": errors,
    }
    return JSONResponse(
        status_code=422,
        content=payload,
        media_type="application/problem+json",
        headers={"X-Request-Id": request_id(request)},
    )
