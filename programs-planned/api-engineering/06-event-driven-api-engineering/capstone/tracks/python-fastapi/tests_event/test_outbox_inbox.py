from __future__ import annotations

from datetime import datetime, timezone
import unittest

from event_engineering.broker import DeterministicBroker
from event_engineering.inbox import TransactionalProjection
from event_engineering.outbox import DomainOutboxStore, OutboxRelay

from helpers import event


class OutboxInboxTests(unittest.TestCase):
    def test_relay_crash_duplicates_publication(self) -> None:
        now = datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc)
        broker = DeterministicBroker(clock=lambda: now)
        broker.create_channel("analysis.events", 2)
        store = DomainOutboxStore()
        value = event("20")
        store.commit(
            aggregate_id="run-001",
            aggregate_state={"status": "completed"},
            channel="analysis.events",
            key="run-001",
            event=value,
        )
        relay = OutboxRelay(store, broker, clock=lambda: now)
        with self.assertRaises(RuntimeError):
            relay.step(crash_after_publish=True)
        self.assertEqual(relay.step(), "published")
        records = broker.records("analysis.events")
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].event.id, records[1].event.id)
        self.assertEqual(records[0].event.canonical_bytes(), records[1].event.canonical_bytes())

    def test_duplicate_delivery_one_effect(self) -> None:
        projection = TransactionalProjection()
        value = event("21")
        mutate = lambda state, _: state.update(
            {"count": int(state.get("count", 0)) + 1}
        )
        first = projection.apply(
            tenant_id="tenant-a",
            consumer="analytics",
            effect_version="v1",
            event=value,
            mutation=mutate,
        )
        second = projection.apply(
            tenant_id="tenant-a",
            consumer="analytics",
            effect_version="v1",
            event=value,
            mutation=mutate,
        )
        self.assertEqual((first.status, second.status), ("applied", "duplicate"))
        self.assertEqual(
            projection.snapshot("tenant-a", "analytics", "v1")["count"], 1
        )

    def test_effect_versions_are_independent(self) -> None:
        projection = TransactionalProjection()
        value = event("22")
        mutate = lambda state, _: state.update({"count": 1})
        for version in ["v1", "v2"]:
            result = projection.apply(
                tenant_id="tenant-a",
                consumer="analytics",
                effect_version=version,
                event=value,
                mutation=mutate,
            )
            self.assertEqual(result.status, "applied")

    def test_tenants_are_independent(self) -> None:
        projection = TransactionalProjection()
        a = event("23", tenant="tenant-a")
        b_data = dict(a.data)
        b = event("23", tenant="tenant-b", data=b_data)
        mutate = lambda state, _: state.update({"count": 1})
        self.assertEqual(
            projection.apply(
                tenant_id="tenant-a", consumer="audit", effect_version="v1", event=a, mutation=mutate
            ).status,
            "applied",
        )
        self.assertEqual(
            projection.apply(
                tenant_id="tenant-b", consumer="audit", effect_version="v1", event=b, mutation=mutate
            ).status,
            "applied",
        )


if __name__ == "__main__":
    unittest.main()
