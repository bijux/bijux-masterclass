from __future__ import annotations

import json
import unittest

from api_reliability.clock import ManualClock
from api_reliability.context import TraceContext
from api_reliability.reconcile import (
    ArtifactRow,
    FindingKind,
    JobRow,
    OutboxRow,
    RunRow,
    Snapshot,
    inspect,
)
from api_reliability.telemetry import InMemoryEventSink, StructuredLogger


class TelemetryReconcileTests(unittest.TestCase):
    def test_logger_redacts_nested_secret(self) -> None:
        sink = InMemoryEventSink()
        logger = StructuredLogger(
            clock=ManualClock(10),
            sink=sink,
            service_name="analysis-runs-api",
            service_version="1.2.0",
        )
        logger.emit(
            "webhook.delivery.failed",
            context=TraceContext("1" * 32, "2" * 16),
            attributes={"nested": {"token": "secret"}},
        )
        payload = json.loads(sink.events[0].to_json())
        self.assertEqual(payload["attributes"]["nested"]["token"], "[REDACTED]")

    def test_reconciliation_finds_cross_table_inconsistency(self) -> None:
        snapshot = Snapshot(
            runs=(RunRow("run_1", "completed"), RunRow("run_2", "running")),
            jobs=(JobRow("run_2", "dead"),),
            artifacts=(),
            outbox=(OutboxRow("run_2", "analysis.failed"),),
        )
        kinds = {item.kind for item in inspect(snapshot)}
        self.assertIn(FindingKind.COMPLETED_RUN_MISSING_ARTIFACT, kinds)
        self.assertIn(FindingKind.TERMINAL_RUN_MISSING_OUTBOX, kinds)
        self.assertIn(FindingKind.TERMINAL_JOB_NONTERMINAL_RUN, kinds)


if __name__ == "__main__":
    unittest.main()
