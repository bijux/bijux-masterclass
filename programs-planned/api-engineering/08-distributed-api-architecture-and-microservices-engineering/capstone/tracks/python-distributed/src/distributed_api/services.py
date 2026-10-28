from __future__ import annotations

import hashlib
from dataclasses import asdict
from .capability import CapabilityAuthority, CapabilityClaims
from .model import (
    ArtifactRecord, Conflict, OperationResult, RequestContext,
    RunRecord, RunState, Unauthorized, ValidationError,
)


class AnalysisControlService:
    def __init__(self, authority: CapabilityAuthority) -> None:
        self.authority = authority
        self.runs: dict[str, RunRecord] = {}
        self.idempotency: dict[tuple[str, str], tuple[str, str]] = {}
        self.events: list[dict[str, object]] = []
        self.artifact_refs: set[str] = set()
        self._counter = 0

    def create_run(self, ctx: RequestContext, *, request_id: str, dataset_id: str) -> RunRecord:
        ctx.require("runs:write")
        fingerprint = hashlib.sha256(f"{ctx.tenant}|{dataset_id}".encode()).hexdigest()
        key = (ctx.tenant, request_id)
        existing = self.idempotency.get(key)
        if existing:
            old_fingerprint, run_id = existing
            if old_fingerprint != fingerprint:
                raise Conflict("idempotency key reused with changed input")
            return self.runs[run_id]
        self._counter += 1
        run_id = f"run-{self._counter}"
        attempt_id = f"attempt-{self._counter}-1"
        run = RunRecord(run_id, ctx.tenant, ctx.subject, dataset_id, attempt_id)
        self.runs[run_id] = run
        self.idempotency[key] = (fingerprint, run_id)
        self.events.append({"type":"AnalysisRunRequested","run_id":run_id,"version":run.version,"tenant":ctx.tenant})
        return run

    def start(self, run_id: str) -> RunRecord:
        run = self.runs[run_id]
        if run.state != RunState.QUEUED:
            raise Conflict("run is not queued")
        run.state = RunState.RUNNING
        run.version += 1
        self.events.append({"type":"AnalysisRunStarted","run_id":run_id,"version":run.version,"tenant":run.tenant})
        return run

    def mint_upload_capability(self, ctx: RequestContext, *, run_id: str, sha256: str, max_bytes: int, now: int) -> str:
        ctx.require("runs:write")
        run = self.runs[run_id]
        if run.tenant != ctx.tenant:
            raise Unauthorized("tenant mismatch")
        if run.state != RunState.RUNNING:
            raise Conflict("artifact upload requires the current running attempt")
        claims = CapabilityClaims(
            jti=f"upload:{run_id}:{run.attempt_id}:{sha256}", issuer=self.authority.issuer,
            audience="artifact-service", subject=ctx.subject, tenant=ctx.tenant,
            resource=run_id, action="artifact:upload", issued_at=now, expires_at=now+300,
            sha256=sha256, max_bytes=max_bytes,
        )
        return self.authority.mint(claims)

    def attach_and_complete(self, *, run_id: str, attempt_id: str, artifact_id: str, event_id: str) -> RunRecord:
        run = self.runs[run_id]
        if run.attempt_id != attempt_id:
            raise Conflict("stale worker attempt")
        if run.state == RunState.COMPLETED:
            if artifact_id in run.artifact_ids:
                return run
            raise Conflict("run completed with another artifact")
        if run.state != RunState.RUNNING:
            raise Conflict("run is not running")
        if artifact_id not in run.artifact_ids:
            run.artifact_ids.append(artifact_id)
            self.artifact_refs.add(artifact_id)
        run.state = RunState.COMPLETED
        run.version += 1
        if not any(e.get("event_id") == event_id for e in self.events):
            self.events.append({
                "event_id":event_id,"type":"AnalysisRunCompleted","run_id":run_id,
                "artifact_id":artifact_id,"version":run.version,"tenant":run.tenant,
            })
        return run

    def get_run(self, ctx: RequestContext, run_id: str) -> RunRecord:
        ctx.require("runs:read")
        run = self.runs[run_id]
        if run.tenant != ctx.tenant:
            raise Unauthorized("resource not visible")
        return run


class ArtifactService:
    def __init__(self, authority: CapabilityAuthority) -> None:
        self.authority = authority
        self.artifacts: dict[str, ArtifactRecord] = {}
        self.by_effect: dict[tuple[str, str, str], str] = {}
        self._counter = 0

    def store(self, *, token: str, tenant: str, content: bytes, now: int) -> ArtifactRecord:
        claims = self.authority.verify(
            token, audience="artifact-service", tenant=tenant,
            action="artifact:upload", now=now, consume_once=False,
        )
        digest = hashlib.sha256(content).hexdigest()
        if claims.sha256 != digest:
            raise ValidationError("artifact checksum mismatch")
        if claims.max_bytes is not None and len(content) > claims.max_bytes:
            raise ValidationError("artifact exceeds capability limit")
        attempt_id = claims.jti.split(":")[2]
        effect = (claims.resource, attempt_id, digest)
        existing = self.by_effect.get(effect)
        if existing:
            return self.artifacts[existing]
        self._counter += 1
        artifact_id = f"artifact-{self._counter}"
        artifact = ArtifactRecord(artifact_id, tenant, claims.resource, attempt_id, digest, content)
        self.artifacts[artifact_id] = artifact
        self.by_effect[effect] = artifact_id
        return artifact

    def mark_orphan(self, artifact_id: str) -> None:
        self.artifacts[artifact_id].state = "orphaned"
        self.artifacts[artifact_id].version += 1

    def get(self, artifact_id: str, *, tenant: str) -> ArtifactRecord:
        artifact = self.artifacts[artifact_id]
        if artifact.tenant != tenant:
            raise Unauthorized("artifact not visible")
        return artifact


class NotificationService:
    def __init__(self) -> None:
        self.inbox: set[str] = set()
        self.notification_run_ids: set[str] = set()
        self.deliveries: list[dict[str, str]] = []

    def consume(self, event: dict[str, object]) -> str:
        event_id = str(event.get("event_id") or f"{event['type']}:{event['run_id']}:{event['version']}")
        if event_id in self.inbox:
            return "duplicate"
        self.inbox.add(event_id)
        if event["type"] not in {"AnalysisRunCompleted", "AnalysisRunFailed"}:
            return "ignored"
        run_id = str(event["run_id"])
        self.notification_run_ids.add(run_id)
        self.deliveries.append({"delivery_id":f"delivery:{event_id}","run_id":run_id,"state":"pending"})
        return "accepted"


class Gateway:
    def __init__(self, control: AnalysisControlService, artifacts: ArtifactService) -> None:
        self.control = control
        self.artifacts = artifacts

    def get_run_view(self, ctx: RequestContext, run_id: str, *, artifact_available: bool = True) -> OperationResult:
        run = self.control.get_run(ctx, run_id)
        payload = asdict(run)
        payload["state"] = run.state.value
        payload["artifacts"] = []
        warnings: list[str] = []
        if artifact_available:
            for artifact_id in run.artifact_ids:
                artifact = self.artifacts.get(artifact_id, tenant=ctx.tenant)
                payload["artifacts"].append({
                    "artifact_id":artifact.artifact_id,"sha256":artifact.sha256,
                    "size":len(artifact.content),"state":artifact.state,
                })
        elif run.artifact_ids:
            warnings.append("artifactsUnavailable")
        return OperationResult(payload, authoritative=True, partial=bool(warnings), warnings=tuple(warnings))
