from __future__ import annotations

from dataclasses import dataclass
from .model import ValidationError


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int

    @classmethod
    def parse(cls, value: str) -> "Version":
        try:
            major, minor = value.split(".")
            return cls(int(major), int(minor))
        except Exception as exc:
            raise ValidationError(f"invalid version: {value}") from exc


class VersionPolicy:
    def classify(self, consumer: str, provider: str) -> str:
        c = Version.parse(consumer)
        p = Version.parse(provider)
        if c.major != p.major:
            return "reject"
        if c.minor <= p.minor:
            return "compatible"
        if c.minor == p.minor + 1:
            return "compatible-with-feature-disabled"
        return "reject"

    def require_matrix(self, pairs: list[tuple[str, str]]) -> None:
        rejected = [pair for pair in pairs if self.classify(*pair) == "reject"]
        if rejected:
            raise ValidationError(f"unsupported version skew: {rejected}")
