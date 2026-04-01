"""Module 09 Core 4: web/service shells (end-of-Module-09).

This package intentionally contains *optional* adapters (e.g., FastAPI) behind
dynamic import guards so the core library remains dependency-light.
"""

from .fastapi_app import create_app

__all__ = ["create_app"]

