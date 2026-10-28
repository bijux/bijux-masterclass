"""Configuration and the course's four-axis release vocabulary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


SERVICE_TO_API_VERSION = {
    "1.0": "1.1.0",
    "1.1": "1.2.0",
}

COURSE_ENCRYPTION_KEY = "course-training-encryption-key"
COURSE_CALLBACK_SECRET = "course-callback-signing-secret"


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str
    artifact_root: Path
    webhook_transport_base: str
    webhook_encryption_key: str
    callback_signing_secret: str
    remote_fixture_root: Path
    worker_id: str
    worker_lease_seconds: int = 15
    upload_limit_bytes: int = 1_048_576
    service_release: str = "1.0"
    environment: str = "development"

    @property
    def public_api_version(self) -> str:
        """Public contract implemented by this executable service release."""

        return SERVICE_TO_API_VERSION[self.service_release]

    @property
    def exposes_api_1_2(self) -> bool:
        return self.service_release == "1.1"

    @classmethod
    def from_env(cls) -> "Settings":
        service_release = os.getenv("SERVICE_RELEASE", "1.0")
        value = cls(
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql://analysis:analysis@127.0.0.1:55432/analysis_python",
            ),
            artifact_root=Path(
                os.getenv("ARTIFACT_ROOT", ".runtime/artifacts")
            ).resolve(),
            webhook_transport_base=os.getenv(
                "WEBHOOK_TRANSPORT_BASE",
                "http://127.0.0.1:58080",
            ).rstrip("/"),
            webhook_encryption_key=os.getenv(
                "WEBHOOK_ENCRYPTION_KEY",
                COURSE_ENCRYPTION_KEY,
            ),
            callback_signing_secret=os.getenv(
                "CALLBACK_SIGNING_SECRET",
                COURSE_CALLBACK_SECRET,
            ),
            remote_fixture_root=Path(
                os.getenv("REMOTE_FIXTURE_ROOT", "fixtures/remote")
            ).resolve(),
            worker_id=os.getenv("WORKER_ID", f"python-worker-{os.getpid()}"),
            worker_lease_seconds=_positive_int("WORKER_LEASE_SECONDS", 15),
            upload_limit_bytes=_positive_int("UPLOAD_LIMIT_BYTES", 1_048_576),
            service_release=service_release,
            environment=os.getenv("APP_ENV", "development"),
        )
        value.validate()
        value.artifact_root.mkdir(parents=True, exist_ok=True)
        value.remote_fixture_root.mkdir(parents=True, exist_ok=True)
        return value

    def validate(self) -> None:
        if self.worker_lease_seconds < 5:
            raise ValueError("WORKER_LEASE_SECONDS must be at least 5")
        if self.upload_limit_bytes != 1_048_576:
            raise ValueError(
                "UPLOAD_LIMIT_BYTES must match the frozen 1 MiB contract"
            )
        if self.service_release not in SERVICE_TO_API_VERSION:
            raise ValueError("SERVICE_RELEASE must be 1.0 or 1.1")
        if len(self.webhook_encryption_key) < 20:
            raise ValueError("WEBHOOK_ENCRYPTION_KEY must contain at least 20 characters")
        if len(self.callback_signing_secret) < 20:
            raise ValueError("CALLBACK_SIGNING_SECRET must contain at least 20 characters")
        if self.environment == "production":
            if self.webhook_encryption_key == COURSE_ENCRYPTION_KEY:
                raise ValueError("the course encryption key is forbidden in production")
            if self.callback_signing_secret == COURSE_CALLBACK_SECRET:
                raise ValueError("the course callback secret is forbidden in production")


def _positive_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value
