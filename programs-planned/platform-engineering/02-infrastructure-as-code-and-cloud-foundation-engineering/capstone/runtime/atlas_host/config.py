from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    """Raised when the Atlas host configuration is unsafe or inconsistent."""


@dataclass(frozen=True)
class AtlasConfig:
    runtime_dir: Path
    state_dir: Path
    log_dir: Path
    api_host: str = "127.0.0.1"
    api_port: int = 18080
    edge_host: str = "127.0.0.1"
    edge_port: int = 18443
    public_name: str = "atlas.test"
    max_body_bytes: int = 65536
    worker_poll_seconds: float = 0.1
    worker_lease_seconds: float = 30.0

    @property
    def spool_dir(self) -> Path:
        return self.state_dir / "spool"

    @property
    def evidence_file(self) -> Path:
        return self.log_dir / "events.jsonl"

    @classmethod
    def from_json(cls, path: Path) -> "AtlasConfig":
        raw = json.loads(path.read_text(encoding="utf-8"))
        config = cls(
            runtime_dir=Path(raw["runtimeDir"]),
            state_dir=Path(raw["stateDir"]),
            log_dir=Path(raw["logDir"]),
            api_host=str(raw.get("apiHost", "127.0.0.1")),
            api_port=int(raw.get("apiPort", 18080)),
            edge_host=str(raw.get("edgeHost", "127.0.0.1")),
            edge_port=int(raw.get("edgePort", 18443)),
            public_name=str(raw.get("publicName", "atlas.test")),
            max_body_bytes=int(raw.get("maxBodyBytes", 65536)),
            worker_poll_seconds=float(raw.get("workerPollSeconds", 0.1)),
            worker_lease_seconds=float(raw.get("workerLeaseSeconds", 30.0)),
        )
        config.validate()
        return config

    def validate(self) -> None:
        directories = [self.runtime_dir, self.state_dir, self.log_dir]
        if any(not path.is_absolute() for path in directories):
            raise ConfigError("runtimeDir, stateDir, and logDir must be absolute")
        resolved = [path.resolve(strict=False) for path in directories]
        if len(set(resolved)) != len(resolved):
            raise ConfigError("runtime, state, and log directories must be distinct")
        if not (0 <= self.api_port <= 65535 and 0 <= self.edge_port <= 65535):
            raise ConfigError("ports must be in the range 0..65535")
        if self.max_body_bytes <= 0 or self.max_body_bytes > 16 * 1024 * 1024:
            raise ConfigError("maxBodyBytes must be between 1 and 16 MiB")
        if self.worker_poll_seconds <= 0 or self.worker_lease_seconds <= 0:
            raise ConfigError("worker timing values must be positive")
        if not self.public_name or any(ch.isspace() for ch in self.public_name):
            raise ConfigError("publicName must be a non-empty host name")

    def prepare(self) -> None:
        self.validate()
        for path, mode in (
            (self.runtime_dir, 0o2770),
            (self.state_dir, 0o750),
            (self.log_dir, 0o2770),
            (self.spool_dir, 0o2770),
            (self.spool_dir / "queued", 0o2770),
            (self.spool_dir / "processing", 0o2770),
            (self.spool_dir / "results", 0o2770),
            (self.spool_dir / "failed", 0o2770),
        ):
            path.mkdir(parents=True, exist_ok=True)
            # Local tours create and own their directories. A managed host uses
            # tmpfiles.d to create root-owned setgid paths; service processes
            # must not attempt to chmod administrator-owned policy.
            if path.stat().st_uid == os.geteuid():
                path.chmod(mode)
