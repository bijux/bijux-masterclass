from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from .model import Conflict, ValidationError


class SagaState(str, Enum):
    NEW = "new"
    ARTIFACT_STORED = "artifact-stored"
    COMPLETED = "completed"
    COMPENSATION_REQUIRED = "compensation-required"
    COMPENSATED = "compensated"
    FAILED = "failed"


@dataclass
class ArtifactCompletionSaga:
    saga_id: str
    run_id: str
    attempt_id: str
    state: SagaState = SagaState.NEW
    artifact_id: str | None = None
    processed: set[str] = field(default_factory=set)
    history: list[str] = field(default_factory=list)

    def record_artifact(self, *, event_id: str, artifact_id: str, attempt_id: str) -> str:
        if event_id in self.processed:
            return "duplicate"
        self.processed.add(event_id)
        if attempt_id != self.attempt_id:
            self.state = SagaState.COMPENSATION_REQUIRED
            self.artifact_id = artifact_id
            self.history.append("stale-artifact")
            return "compensate"
        if self.state not in {SagaState.NEW, SagaState.ARTIFACT_STORED}:
            raise Conflict(f"cannot record artifact in {self.state}")
        if self.artifact_id and self.artifact_id != artifact_id:
            raise Conflict("saga already bound to another artifact")
        self.artifact_id = artifact_id
        self.state = SagaState.ARTIFACT_STORED
        self.history.append("artifact-stored")
        return "stored"

    def complete(self, *, command_id: str, current_attempt_id: str) -> str:
        if command_id in self.processed:
            return "duplicate"
        self.processed.add(command_id)
        if self.state == SagaState.COMPLETED:
            return "duplicate"
        if self.state != SagaState.ARTIFACT_STORED or not self.artifact_id:
            raise Conflict("artifact must be stored before completion")
        if current_attempt_id != self.attempt_id:
            self.state = SagaState.COMPENSATION_REQUIRED
            self.history.append("stale-completion")
            return "compensate"
        self.state = SagaState.COMPLETED
        self.history.append("run-completed")
        return "completed"

    def compensate(self, *, action_id: str) -> str:
        if action_id in self.processed:
            return "duplicate"
        self.processed.add(action_id)
        if self.state != SagaState.COMPENSATION_REQUIRED:
            raise ValidationError("compensation is not required")
        self.state = SagaState.COMPENSATED
        self.history.append("artifact-orphaned")
        return "compensated"
