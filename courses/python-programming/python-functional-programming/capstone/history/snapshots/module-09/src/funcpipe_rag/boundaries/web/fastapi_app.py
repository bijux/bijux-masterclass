"""Module 09 Core 4: optional FastAPI adapter (end-of-Module-09).

This file does not import FastAPI at module import time. If FastAPI is not
installed, `create_app()` raises ImportError.
"""

# mypy: ignore-errors

from __future__ import annotations

import importlib
from typing import Any


def create_app() -> Any:
    fastapi = importlib.import_module("fastapi")
    pydantic = importlib.import_module("pydantic")

    FastAPI = fastapi.FastAPI
    APIRouter = fastapi.APIRouter
    HTTPException = fastapi.HTTPException
    Body = fastapi.Body

    BaseModel = pydantic.BaseModel

    class DocIn(BaseModel):  # type: ignore[misc]
        doc_id: str
        title: str
        abstract: str
        categories: str = ""

    router = APIRouter(prefix="/rag")
    app = FastAPI()

    @router.post("/echo")
    async def echo(docs: list[DocIn] = Body(...)) -> list[dict[str, Any]]:
        # A tiny example endpoint; real endpoints should delegate to pure core.
        return [d.model_dump() for d in docs]

    @router.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/error")
    async def error() -> None:
        raise HTTPException(status_code=400, detail={"error": "example"})

    app.include_router(router)
    return app


__all__ = ["create_app"]
