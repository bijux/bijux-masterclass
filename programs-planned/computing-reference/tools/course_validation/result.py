from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    issues: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues

    def extend(self, *issues: str) -> "ValidationResult":
        return ValidationResult(self.issues + tuple(issue for issue in issues if issue))
