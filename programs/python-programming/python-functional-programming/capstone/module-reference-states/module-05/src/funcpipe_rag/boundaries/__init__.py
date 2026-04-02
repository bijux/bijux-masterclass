"""Impure edges and boundary adapters (end-of-Module-05).

This package groups the parts of the project that perform I/O or interact with
the outside world (CLI, filesystem, JSON/MessagePack, Pydantic schemas).
"""

from .app_config import AppConfig

__all__ = ["AppConfig"]
