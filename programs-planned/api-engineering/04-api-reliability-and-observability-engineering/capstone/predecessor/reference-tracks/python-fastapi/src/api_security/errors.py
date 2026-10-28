from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SecurityControlError(Exception):
    """Bounded internal security error.

    `code` is stable enough for tests and audit. `detail` must not contain
    credentials, secret values, or reflected hostile bodies.
    """

    code: str
    detail: str
    status: int = 400

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"
