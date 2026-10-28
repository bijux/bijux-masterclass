from __future__ import annotations

from datetime import datetime, timezone

from event_engineering.envelope import build_event


def event(
    suffix: str,
    *,
    event_type: str = "org.bijux.analysis.run.completed.v1",
    tenant: str = "tenant-a",
    run_id: str = "run-001",
    data: dict | None = None,
):
    number = int(suffix)
    return build_event(
        source="urn:bijux:analysis-control",
        event_type=event_type,
        subject=f"analysis-runs/{run_id}",
        dataschema=f"https://schemas.bijux.test/{event_type.rsplit('.', 1)[0]}/v1",
        tenant_id=tenant,
        correlation_id="00000000-0000-4000-8000-000000000010",
        partition_key=run_id,
        data=data
        or {
            "runId": run_id,
            "durationMs": 1000,
            "artifactCount": 1,
            "occurredAt": "2026-08-07T10:00:00Z",
        },
        event_id_factory=lambda: f"00000000-0000-4000-8000-{number:012d}",
        clock=lambda: datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc),
    )
