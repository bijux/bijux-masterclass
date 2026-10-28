from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from .broker import DeterministicBroker
from .envelope import build_event
from .inbox import TransactionalProjection
from .outbox import DomainOutboxStore, OutboxRelay


def run_demo() -> dict[str, object]:
    now = datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc)
    current = [now]
    broker = DeterministicBroker(clock=lambda: current[0])
    broker.create_channel("analysis.events", 4)
    event = build_event(
        source="urn:bijux:analysis-control",
        event_type="org.bijux.analysis.run.completed.v1",
        subject="analysis-runs/run-001",
        dataschema="https://schemas.bijux.test/analysis-run-completed/v1",
        tenant_id="tenant-a",
        correlation_id="00000000-0000-4000-8000-000000000010",
        partition_key="run-001",
        data={
            "runId": "run-001",
            "durationMs": 8421,
            "artifactCount": 2,
            "occurredAt": "2026-08-07T09:59:59Z",
        },
        event_id_factory=lambda: "00000000-0000-4000-8000-000000000011",
        clock=lambda: now,
    )
    store = DomainOutboxStore()
    store.commit(
        aggregate_id="run-001",
        aggregate_state={"status": "completed"},
        channel="analysis.events",
        key="run-001",
        event=event,
    )
    relay = OutboxRelay(store, broker, clock=lambda: current[0])
    try:
        relay.step(crash_after_publish=True)
    except RuntimeError:
        pass
    relay.step()
    projection = TransactionalProjection()
    deliveries = []
    for _ in range(2):
        delivery = broker.poll("analytics-v1", "analysis.events")[0]
        deliveries.append(delivery.attempt)
        projection.apply(
            tenant_id="tenant-a",
            consumer="analytics",
            effect_version="v1",
            event=delivery.record.event,
            mutation=lambda state, _: state.update(
                {"completed": int(state.get("completed", 0)) + 1}
            ),
        )
        broker.ack(delivery.token)
    return {
        "brokerRecords": len(broker.records("analysis.events")),
        "deliveryAttempts": deliveries,
        "projection": projection.snapshot("tenant-a", "analytics", "v1"),
        "effects": projection.applied_count,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, sort_keys=True))
