from __future__ import annotations

import argparse
import os
import signal
import threading
import time
from pathlib import Path

from .atomic_store import atomic_write_bytes, atomic_write_json
from .config import AtlasConfig
from .events import append
from .spool import FileSpool


def run(config: AtlasConfig, *, once: bool = False, worker_id: str | None = None) -> int:
    config.prepare()
    actual_worker = worker_id or f"worker-{os.getpid()}"
    spool = FileSpool(config.spool_dir)
    stop = threading.Event()

    def handle_signal(signum: int, _frame: object) -> None:
        append(config.evidence_file, "worker.signal", signal=signum, worker_id=actual_worker)
        stop.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    atomic_write_json(config.runtime_dir / "worker.json", {"pid": os.getpid(), "workerId": actual_worker}, mode=0o640)
    append(config.evidence_file, "worker.started", worker_id=actual_worker)
    try:
        while True:
            atomic_write_bytes(config.runtime_dir / "worker.heartbeat", f"{time.time_ns()}\n".encode(), mode=0o640)
            recovered = spool.recover_expired(config.worker_lease_seconds)
            if recovered:
                append(config.evidence_file, "worker.recovered", count=recovered, worker_id=actual_worker)
            claimed = spool.claim(actual_worker)
            if claimed is None:
                if once or stop.is_set():
                    break
                stop.wait(config.worker_poll_seconds)
                continue
            append(config.evidence_file, "job.claimed", job_id=claimed.job_id, worker_id=actual_worker)
            try:
                result = spool.deterministic_result(claimed.payload)
                # Graceful termination completes the already claimed unit of work.
                spool.complete(claimed, result)
                append(config.evidence_file, "job.completed", job_id=claimed.job_id, worker_id=actual_worker)
            except Exception as exc:  # course capstone records unexpected failure
                spool.fail(claimed, type(exc).__name__)
                append(config.evidence_file, "job.failed", job_id=claimed.job_id, reason=type(exc).__name__)
            if once or stop.is_set():
                break
    finally:
        append(config.evidence_file, "worker.stopped", worker_id=actual_worker)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--worker-id")
    args = parser.parse_args()
    return run(AtlasConfig.from_json(args.config), once=args.once, worker_id=args.worker_id)


if __name__ == "__main__":
    raise SystemExit(main())
