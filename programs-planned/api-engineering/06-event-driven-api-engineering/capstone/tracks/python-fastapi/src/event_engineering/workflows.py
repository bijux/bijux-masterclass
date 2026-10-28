from __future__ import annotations

from dataclasses import dataclass

from .envelope import EventEnvelope


@dataclass(slots=True)
class RunProcessState:
    run_id: str
    status: str = "new"
    generation: int = 0
    last_event_id: str | None = None
    command_id: str | None = None


class RunProcessManager:
    """Pure process-state transitions; durable adapters own transactions/timers."""

    def apply(self, state: RunProcessState, event: EventEnvelope) -> str:
        if state.last_event_id == event.id:
            return "duplicate"
        event_type = event.type
        if event_type.endswith("run.requested.v1"):
            if state.status == "new":
                state.status = "start-requested"
                state.generation += 1
                state.command_id = f"start:{state.run_id}:{state.generation}"
        elif event_type.endswith("run.started.v1"):
            if state.status in {"start-requested", "requested"}:
                state.status = "running"
            elif state.status not in {"running", "completed", "failed"}:
                raise ValueError("started event violates process state")
        elif event_type.endswith("run.completed.v1"):
            if state.status in {"running", "start-requested"}:
                state.status = "completed"
            elif state.status != "completed":
                raise ValueError("completed event violates process state")
        elif event_type.endswith("run.failed.v1"):
            if state.status not in {"completed", "failed"}:
                state.status = "failed"
        else:
            return "ignored"
        state.last_event_id = event.id
        return "applied"

    def timeout(self, state: RunProcessState, generation: int) -> str:
        if generation != state.generation or state.status in {"completed", "failed"}:
            return "stale"
        if state.status == "start-requested":
            state.status = "reconcile-start"
            return "applied"
        return "ignored"
