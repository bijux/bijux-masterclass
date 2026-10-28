"""Small, explicit consumer helper for the course sandbox."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientConfig:
    base_url: str
    token: str

    def __post_init__(self) -> None:
        if not self.base_url.startswith("https://") and not self.base_url.startswith("http://127.0.0.1"):
            raise ValueError("base_url must be HTTPS outside the loopback laboratory")
        if not self.token:
            raise ValueError("token must be explicit")
