from __future__ import annotations

import hashlib
import json
from .capability import CapabilityAuthority
from .model import RequestContext
from .reconciliation import reconcile
from .services import AnalysisControlService, ArtifactService, Gateway, NotificationService


def run_tour() -> dict[str, object]:
    authority = CapabilityAuthority(issuer="analysis-control", key=b"course-eight-capability-key")
    control = AnalysisControlService(authority)
    artifacts = ArtifactService(authority)
    notifications = NotificationService()
    gateway = Gateway(control, artifacts)
    ctx = RequestContext(
        subject="learner", tenant="tenant-a", workload="edge-gateway",
        scopes=frozenset({"runs:read","runs:write"}), deadline_ms=10_000,
    )

    run = control.create_run(ctx, request_id="request-1", dataset_id="dataset-1")
    control.start(run.run_id)
    content = b"course-eight-distributed-artifact"
    digest = hashlib.sha256(content).hexdigest()
    token = control.mint_upload_capability(ctx, run_id=run.run_id, sha256=digest, max_bytes=1024, now=100)
    artifact = artifacts.store(token=token, tenant=ctx.tenant, content=content, now=101)
    control.attach_and_complete(
        run_id=run.run_id, attempt_id=run.attempt_id, artifact_id=artifact.artifact_id,
        event_id=f"completed:{run.run_id}:3",
    )
    completion = next(e for e in control.events if e.get("type") == "AnalysisRunCompleted")
    notifications.consume(completion)
    view = gateway.get_run_view(ctx, run.run_id)
    findings = reconcile(
        control_artifact_refs=control.artifact_refs,
        artifact_ids=set(artifacts.artifacts),
        completed_runs={run.run_id},
        notification_run_ids=notifications.notification_run_ids,
    )
    assert not findings
    assert not view.partial
    return {
        "run_id":run.run_id,
        "state":control.runs[run.run_id].state.value,
        "artifact_id":artifact.artifact_id,
        "artifact_sha256":artifact.sha256,
        "delivery_count":len(notifications.deliveries),
        "reconciliation":findings,
    }


def main() -> None:
    print(json.dumps(run_tour(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
