from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from threading import RLock
import time
from uuid import uuid4

from .errors import (
    Aborted, AlreadyExists, FailedPrecondition, InvalidArgument, NotFound,
    ResourceExhausted,
)
from .models import Assignment, Event, Principal, Run, State, advance, request_fingerprint


@dataclass(frozen=True)
class IdempotencyRecord:
    fingerprint: str
    run_name: str


class InMemoryAnalysisStore:
    """Thread-safe teaching store with the same public invariants as the DB design.

    It is not presented as a production persistence substitute. The database
    migrations and Course 2 handoff remain the durable implementation profile.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._runs: dict[str, Run] = {}
        self._requests: dict[tuple[str, str], IdempotencyRecord] = {}
        self._events: dict[str, list[Event]] = {}
        self._datasets: dict[str, bytes] = {}
        self._artifacts: dict[str, bytes] = {
            "artifacts/a-1": b"analysis-artifact\n",
        }
        self._assignments: dict[str, Assignment] = {}

    def create_run(
        self,
        *,
        parent: str,
        request_id: str,
        dataset_name: str,
        algorithm: str,
        principal: Principal,
    ) -> Run:
        if not parent.startswith("projects/"):
            raise InvalidArgument("invalid parent resource", field="parent")
        if not dataset_name.startswith("datasets/"):
            raise InvalidArgument("invalid dataset resource", field="dataset_name")
        if algorithm not in {"qc", "align", "summarize"}:
            raise InvalidArgument("unsupported algorithm", field="algorithm")
        if not request_id or len(request_id) > 128:
            raise InvalidArgument("invalid request identifier", field="request_id")

        fingerprint = request_fingerprint(
            parent=parent,
            dataset_name=dataset_name,
            algorithm=algorithm,
            principal=principal,
        )
        key = (principal.subject, request_id)
        with self._lock:
            existing = self._requests.get(key)
            if existing is not None:
                if existing.fingerprint != fingerprint:
                    raise AlreadyExists(
                        "request identifier is bound to different input"
                    )
                return self._runs[existing.run_name]

            digest = sha256(
                f"{principal.subject}:{request_id}:{fingerprint}".encode()
            ).hexdigest()[:16]
            name = f"{parent}/runs/r-{digest}"
            run = Run(
                name=name,
                project_name=parent,
                dataset_name=dataset_name,
                state=State.QUEUED,
                progress_percent=0,
                revision=1,
            )
            self._runs[name] = run
            self._requests[key] = IdempotencyRecord(fingerprint, name)
            self._append_event(run, "queued")
            return run

    def get_run(self, name: str, principal: Principal) -> Run:
        with self._lock:
            run = self._runs.get(name)
            if run is None or (
                principal.tenant == "tenant-b"
            ) != run.project_name.startswith("projects/p-b-"):
                raise NotFound("run not found")
            return run

    def cancel_run(
        self,
        *,
        name: str,
        etag: str,
        request_id: str,
        principal: Principal,
    ) -> Run:
        if not request_id:
            raise InvalidArgument("request identifier is required", field="request_id")
        with self._lock:
            run = self.get_run(name, principal)
            if run.etag != etag:
                raise Aborted("stale run version")
            if run.state in {State.COMPLETED, State.FAILED, State.CANCELLED}:
                if run.state == State.CANCELLED:
                    return run
                raise FailedPrecondition("terminal run cannot be cancelled")
            updated = advance(run, state=State.CANCELLED, progress=run.progress_percent)
            self._runs[name] = updated
            self._append_event(updated, "cancelled")
            return updated

    def advance_run(
        self,
        name: str,
        *,
        state: State,
        progress: int,
        result: str | None = None,
        failure: str | None = None,
    ) -> Run:
        with self._lock:
            run = self._runs.get(name)
            if run is None:
                raise NotFound("run not found")
            updated = advance(
                run,
                state=state,
                progress=progress,
                result=result,
                failure=failure,
            )
            self._runs[name] = updated
            self._append_event(updated, state.name.lower())
            return updated

    def watch(self, name: str, after: int, principal: Principal) -> list[Event]:
        self.get_run(name, principal)
        with self._lock:
            events = self._events.get(name, [])
            if after < 0:
                raise InvalidArgument(
                    "resume sequence cannot be negative",
                    field="resume_after_sequence",
                )
            if events and after > events[-1].sequence:
                raise FailedPrecondition("resume sequence is ahead of the stream")
            return [event for event in events if event.sequence > after]

    def upload(
        self,
        *,
        parent: str,
        request_id: str,
        filename: str,
        expected_sha256: str,
        expected_size: int,
        chunks: list[bytes],
        max_bytes: int,
    ) -> tuple[str, int, str]:
        if not parent.startswith("projects/"):
            raise InvalidArgument("invalid parent resource", field="parent")
        if "/" in filename or "\\" in filename or filename in {"", ".", ".."}:
            raise InvalidArgument("invalid filename", field="filename")
        total = sum(len(c) for c in chunks)
        if total > max_bytes:
            raise ResourceExhausted("upload exceeds byte budget")
        if expected_size not in {0, total}:
            raise FailedPrecondition("upload size does not match metadata")
        body = b"".join(chunks)
        digest = sha256(body).hexdigest()
        if expected_sha256 and digest != expected_sha256.lower():
            raise FailedPrecondition("upload checksum mismatch")
        name = f"datasets/d-{digest[:16]}"
        with self._lock:
            self._datasets.setdefault(name, body)
        return name, total, digest

    def download(self, name: str, *, offset: int, limit: int) -> tuple[bytes, str]:
        if offset < 0 or limit < 0:
            raise InvalidArgument("offset and limit must be non-negative")
        with self._lock:
            body = self._artifacts.get(name)
            if body is None:
                raise NotFound("artifact not found")
            selected = body[offset:] if limit == 0 else body[offset:offset + limit]
            return selected, sha256(selected).hexdigest()

    def assign(self, worker_id: str, tenant: str, max_concurrency: int) -> Assignment | None:
        if max_concurrency <= 0:
            raise InvalidArgument("worker concurrency must be positive")
        with self._lock:
            candidates = [
                run for run in self._runs.values()
                if run.state == State.QUEUED
                and (tenant == "tenant-b") == run.project_name.startswith("projects/p-b-")
            ]
            if not candidates:
                return None
            run = sorted(candidates, key=lambda r: r.name)[0]
            generation = run.revision
            assignment = Assignment(
                assignment_id=f"assign-{uuid4().hex[:12]}",
                run_name=run.name,
                algorithm="qc",
                dataset_name=run.dataset_name,
                worker_id=worker_id,
                lease_generation=generation,
                lease_expires_unix_ms=int(time.time() * 1000) + 30_000,
            )
            self._assignments[assignment.assignment_id] = assignment
            return assignment

    def complete_assignment(
        self,
        *,
        assignment_id: str,
        worker_id: str,
        generation: int,
        success: bool,
        result_summary: str,
        failure_code: str,
    ) -> Run:
        with self._lock:
            assignment = self._assignments.get(assignment_id)
            if (
                assignment is None
                or assignment.worker_id != worker_id
                or assignment.lease_generation != generation
            ):
                raise FailedPrecondition("stale or foreign assignment")
            run = self._runs[assignment.run_name]
            if generation != run.revision:
                raise FailedPrecondition("stale lease generation")
            updated = advance(
                run,
                state=State.COMPLETED if success else State.FAILED,
                progress=100 if success else run.progress_percent,
                result=result_summary if success else None,
                failure=failure_code if not success else None,
            )
            self._runs[run.name] = updated
            self._append_event(updated, "completed" if success else "failed")
            del self._assignments[assignment_id]
            return updated

    def _append_event(self, run: Run, event_type: str) -> None:
        events = self._events.setdefault(run.name, [])
        sequence = len(events) + 1
        events.append(
            Event(
                event_id=f"evt-{sha256(f'{run.name}:{sequence}'.encode()).hexdigest()[:16]}",
                run_name=run.name,
                sequence=sequence,
                type=event_type,
                snapshot=run,
            )
        )
