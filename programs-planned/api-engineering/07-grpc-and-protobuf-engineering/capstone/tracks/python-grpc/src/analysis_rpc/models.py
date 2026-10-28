from __future__ import annotations
from dataclasses import dataclass, replace
from enum import IntEnum
from hashlib import sha256
import json

class State(IntEnum):
    UNSPECIFIED = 0
    QUEUED = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5

@dataclass(frozen=True)
class Principal:
    subject: str
    tenant: str
    scopes: frozenset[str]
    workload: str = "gateway"

@dataclass(frozen=True)
class Run:
    name: str
    project_name: str
    dataset_name: str
    state: State
    progress_percent: int
    revision: int
    result_summary: str | None = None
    failure_code: str | None = None

    @property
    def etag(self) -> str:
        return f'"run-{self.revision}"'

@dataclass(frozen=True)
class Event:
    event_id: str
    run_name: str
    sequence: int
    type: str
    snapshot: Run

@dataclass(frozen=True)
class Assignment:
    assignment_id: str
    run_name: str
    algorithm: str
    dataset_name: str
    worker_id: str
    lease_generation: int
    lease_expires_unix_ms: int

def request_fingerprint(*, parent: str, dataset_name: str, algorithm: str, principal: Principal) -> str:
    payload = {
        "algorithm": algorithm,
        "dataset_name": dataset_name,
        "parent": parent,
        "subject": principal.subject,
        "tenant": principal.tenant,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()

def advance(run: Run, *, state: State, progress: int, result: str | None = None,
            failure: str | None = None) -> Run:
    if progress < run.progress_percent or not 0 <= progress <= 100:
        raise ValueError("progress must be monotonic and between 0 and 100")
    if run.state in {State.COMPLETED, State.FAILED, State.CANCELLED}:
        raise ValueError("terminal run cannot advance")
    if state == State.COMPLETED and progress != 100:
        raise ValueError("completed run requires 100 percent")
    if state == State.FAILED and not failure:
        raise ValueError("failed run requires a failure code")
    return replace(
        run,
        state=state,
        progress_percent=progress,
        revision=run.revision + 1,
        result_summary=result,
        failure_code=failure,
    )
