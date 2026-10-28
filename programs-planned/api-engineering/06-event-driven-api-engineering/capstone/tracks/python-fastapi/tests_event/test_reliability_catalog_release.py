from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest

from event_engineering.broker import DeterministicBroker
from event_engineering.catalog import CatalogEntry, CatalogError, EventCatalog
from event_engineering.release import evaluate_event_release
from event_engineering.reliability import (
    ConsumerRunner,
    DeadLetterStore,
    PermanentMessageError,
    classify_lag,
)

from helpers import event


class ReliabilityCatalogueReleaseTests(unittest.TestCase):
    def test_permanent_failure_dead_letters_immediately(self) -> None:
        broker = DeterministicBroker()
        broker.create_channel("analysis.events", 1)
        broker.publish("analysis.events", "run-001", event("50"))
        dead = DeadLetterStore()
        runner = ConsumerRunner(broker, dead, max_attempts=3)
        result = runner.step(
            "analytics", "analysis.events", lambda _: (_ for _ in ()).throw(PermanentMessageError("bad schema"))
        )
        self.assertEqual(result, "dead-lettered")
        self.assertEqual(len(dead.rows), 1)

    def test_transient_failure_retries_then_dead_letters(self) -> None:
        now = [datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc)]
        broker = DeterministicBroker(clock=lambda: now[0])
        broker.create_channel("analysis.events", 1)
        broker.publish("analysis.events", "run-001", event("51"))
        dead = DeadLetterStore()
        runner = ConsumerRunner(broker, dead, max_attempts=2, retry_delay=lambda _: timedelta(0))
        handler = lambda _: (_ for _ in ()).throw(RuntimeError("database unavailable"))
        self.assertEqual(runner.step("analytics", "analysis.events", handler), "retry")
        self.assertEqual(runner.step("analytics", "analysis.events", handler), "dead-lettered")

    def test_lag_classification_uses_age(self) -> None:
        health = classify_lag(1, 4000, warning_lag=100, critical_lag=1000, warning_age=60, critical_age=3600)
        self.assertEqual(health.state, "critical")

    def test_catalogue_requires_complete_entry(self) -> None:
        entry = CatalogEntry("completed", "org.bijux.analysis.run.completed.v1", "analysis-control", "analysis.events", "https://schemas/x", "runId", "internal", 90, "projection-safe")
        catalog = EventCatalog([entry])
        self.assertEqual(catalog.require(entry.event_type), entry)
        with self.assertRaises(CatalogError):
            catalog.require("missing")

    def test_release_states(self) -> None:
        old = {"type": "object", "properties": {"runId": {"type": "string"}}, "required": ["runId"]}
        additive = {"type": "object", "properties": {"runId": {"type": "string"}, "summary": {"type": "string"}}, "required": ["runId"]}
        breaking = {"type": "object", "properties": {"runId": {"type": "string"}, "region": {"type": "string"}}, "required": ["runId", "region"]}
        self.assertEqual(evaluate_event_release(old, additive, replay_safe=True, catalog_complete=True, contract_valid=True).status, "accepted")
        self.assertEqual(evaluate_event_release(old, breaking, replay_safe=True, catalog_complete=True, contract_valid=True).status, "rejected")
        self.assertEqual(evaluate_event_release(old, additive, replay_safe=False, catalog_complete=True, contract_valid=True).status, "rejected")


if __name__ == "__main__":
    unittest.main()
