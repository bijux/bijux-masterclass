from __future__ import annotations

import hashlib
import os
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .atomic_store import atomic_write_json, read_json


@dataclass(frozen=True)
class ClaimedJob:
    job_id: str
    worker_id: str
    path: Path
    payload: dict[str, Any]


class FileSpool:
    """A bounded teaching spool that exposes host-level durability mechanics."""

    def __init__(self, root: Path):
        self.root = root
        self.queued = root / "queued"
        self.processing = root / "processing"
        self.results = root / "results"
        self.failed = root / "failed"
        for path in (self.queued, self.processing, self.results, self.failed):
            path.mkdir(parents=True, exist_ok=True)

    def submit(self, payload: dict[str, Any], *, job_id: str | None = None) -> str:
        actual_id = job_id or f"job_{uuid.uuid4().hex[:20]}"
        record = {
            "jobId": actual_id,
            "submittedAtNs": time.time_ns(),
            "payload": payload,
        }
        target = self.queued / f"{actual_id}.json"
        if target.exists() or (self.results / f"{actual_id}.json").exists():
            raise FileExistsError(actual_id)
        atomic_write_json(target, record)
        return actual_id

    def claim(self, worker_id: str) -> ClaimedJob | None:
        for source in sorted(self.queued.glob("job_*.json")):
            job_id = source.stem
            target = self.processing / f"{job_id}.{worker_id}.json"
            try:
                os.replace(source, target)
            except FileNotFoundError:
                continue
            payload = read_json(target)
            return ClaimedJob(job_id=job_id, worker_id=worker_id, path=target, payload=payload)
        return None

    def complete(self, claimed: ClaimedJob, result: dict[str, Any]) -> Path:
        body = {
            "jobId": claimed.job_id,
            "completedAtNs": time.time_ns(),
            "result": result,
        }
        target = self.results / f"{claimed.job_id}.json"
        atomic_write_json(target, body)
        claimed.path.unlink(missing_ok=False)
        return target

    def fail(self, claimed: ClaimedJob, reason: str) -> Path:
        target = self.failed / f"{claimed.job_id}.json"
        atomic_write_json(target, {"jobId": claimed.job_id, "failedAtNs": time.time_ns(), "reason": reason})
        claimed.path.unlink(missing_ok=True)
        return target

    def status(self, job_id: str) -> dict[str, Any] | None:
        result = self.results / f"{job_id}.json"
        if result.exists():
            return {"state": "completed", **read_json(result)}
        failed = self.failed / f"{job_id}.json"
        if failed.exists():
            return {"state": "failed", **read_json(failed)}
        queued = self.queued / f"{job_id}.json"
        if queued.exists():
            return {"state": "queued", **read_json(queued)}
        matches = list(self.processing.glob(f"{job_id}.*.json"))
        if matches:
            return {"state": "processing", **read_json(matches[0])}
        return None

    def recover_expired(self, lease_seconds: float) -> int:
        now = time.time()
        recovered = 0
        for source in self.processing.glob("job_*.json"):
            if now - source.stat().st_mtime < lease_seconds:
                continue
            job_id = source.name.split(".", 1)[0]
            completed = self.results / f"{job_id}.json"
            if completed.exists():
                # A crash after result publication but before processing cleanup
                # must not create a second logical execution.
                source.unlink(missing_ok=True)
                recovered += 1
                continue
            target = self.queued / f"{job_id}.json"
            try:
                os.replace(source, target)
            except FileNotFoundError:
                continue
            recovered += 1
        return recovered

    @staticmethod
    def deterministic_result(payload: dict[str, Any]) -> dict[str, Any]:
        raw = str(payload.get("payload", {}).get("text", "")).encode("utf-8")
        return {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "uppercase": raw.decode("utf-8").upper(),
        }
