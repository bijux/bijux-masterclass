from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .failures import ServiceError

ApiProblem = ServiceError
PROBLEM_MEDIA_TYPE = "application/problem+json"
PROBLEM_BASE = "https://api.example.test/problems"


def request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "req_000000000000")


def problem_payload(
    request: Request,
    error: ServiceError,
) -> dict[str, Any]:
    detail = (
        error.detail
        if error.public
        else "The service could not complete the request."
    )
    body: dict[str, Any] = {
        "type": f"{PROBLEM_BASE}/{error.code}",
        "title": error.title,
        "status": error.status,
        "detail": detail,
        "instance": request.url.path,
        "requestId": request_id(request),
    }
    if error.errors is not None:
        body["errors"] = error.errors
    return body


def problem_response(
    request: Request,
    error: ServiceError,
) -> JSONResponse:
    return JSONResponse(
        problem_payload(request, error),
        status_code=error.status,
        media_type=PROBLEM_MEDIA_TYPE,
    )


def validation_issues(
    error: RequestValidationError,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for item in error.errors():
        location = "/" + "/".join(str(part) for part in item.get("loc", []))
        issues.append(
            {
                "location": location,
                "message": item.get("msg", "Invalid value"),
                "code": item.get("type", "validation"),
            }
        )
    return issues


def install_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def service_error_handler(
        request: Request,
        error: ServiceError,
    ) -> JSONResponse:
        return problem_response(request, error)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        error: RequestValidationError,
    ) -> JSONResponse:
        problem = ServiceError(
            422,
            "Request validation failed",
            "One or more request values are invalid.",
            "validation",
            validation_issues(error),
        )
        return problem_response(request, problem)
