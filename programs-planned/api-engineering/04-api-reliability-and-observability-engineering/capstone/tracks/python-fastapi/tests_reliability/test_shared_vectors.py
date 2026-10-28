from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import unittest

from api_reliability.alerts import BurnRateAlert, evaluate_burn_rate_alert
from api_reliability.clock import ManualClock
from api_reliability.context import TraceContextError, parse_traceparent
from api_reliability.deadline import Deadline
from api_reliability.http import classify_http_outcome
from api_reliability.health import ComponentHealth, HealthEvaluator, LifecyclePhase
from api_reliability.reconcile import (
    ArtifactRow,
    EventRow,
    JobRow,
    OutboxRow,
    RunRow,
    Snapshot,
    inspect,
)
from api_reliability.retry import (
    RetrySafety,
    fit_delays_to_deadline,
    parse_retry_after_ms,
    retryable,
)
from api_reliability.slo import SLODefinition, SLOWindow, burn_rate
from api_reliability.telemetry import redact


VECTORS = Path(__file__).resolve().parents[3] / "shared" / "vectors"


class SharedVectorTests(unittest.TestCase):
    def load(self, name: str) -> dict:
        return json.loads((VECTORS / name).read_text(encoding="utf-8"))

    def test_trace_context_vectors(self) -> None:
        for case in self.load("trace-context.json")["cases"]:
            with self.subTest(case=case["id"]):
                if case["valid"]:
                    self.assertEqual(
                        parse_traceparent(case["value"]).sampled,
                        case["sampled"],
                    )
                else:
                    with self.assertRaises(TraceContextError):
                        parse_traceparent(case["value"])

    def test_retry_vectors(self) -> None:
        vectors = self.load("retries.json")
        for case in vectors["classificationCases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(
                    retryable(
                        status=case.get("status"),
                        transport_error=case["transportError"],
                        safety=RetrySafety(case["safety"]),
                    ),
                    case["retry"],
                )
        for case in vectors["fitCases"]:
            result = fit_delays_to_deadline(
                case["delays"],
                clock=ManualClock(case["nowMs"]),
                deadline=Deadline(case["deadlineMs"]),
                minimum_attempt_ms=case["minimumAttemptMs"],
            )
            self.assertEqual(result, case["expected"], case["id"])
        for case in vectors["retryAfterCases"]:
            now = datetime.fromisoformat(case["now"]) if "now" in case else None
            self.assertEqual(
                parse_retry_after_ms(case["value"], now=now),
                case["expectedMs"],
                case["id"],
            )

    def test_http_outcome_vectors(self) -> None:
        for case in self.load("http-outcomes.json")["cases"]:
            result = classify_http_outcome(case["operation"], case["status"])
            self.assertEqual(
                (result.eligibility, result.outcome),
                (case["eligibility"], case["outcome"]),
                case["id"],
            )

    def test_health_vectors(self) -> None:
        for case in self.load("health.json")["cases"]:
            components = [
                ComponentHealth(
                    value["name"],
                    value["requiredForReadiness"],
                    value["available"],
                )
                for value in case["components"]
            ]
            snapshot = HealthEvaluator().evaluate(
                phase=LifecyclePhase(case["phase"]),
                startup_complete=case["startupComplete"],
                event_loop_progressing=case["eventLoopProgressing"],
                components=components,
            )
            self.assertEqual(
                (snapshot.live, snapshot.ready),
                (case["live"], case["ready"]),
                case["id"],
            )

    def test_slo_vectors(self) -> None:
        for case in self.load("slo.json")["cases"]:
            value = burn_rate(
                SLODefinition(case["id"], case["objective"], 28 * 24 * 3600),
                SLOWindow(case["good"], case["total"]),
            )
            if case["burnRate"] is None:
                self.assertIsNone(value)
            else:
                self.assertAlmostEqual(value or 0, case["burnRate"], places=8)

    def test_alert_vectors(self) -> None:
        for case in self.load("alerts.json")["cases"]:
            result = evaluate_burn_rate_alert(
                SLODefinition(case["id"], case["objective"], 28 * 24 * 3600),
                BurnRateAlert(
                    case["id"],
                    "page",
                    3600,
                    300,
                    case["threshold"],
                    case["minimumEvents"],
                ),
                long_window=SLOWindow(**case["long"]),
                short_window=SLOWindow(**case["short"]),
            )
            self.assertEqual(result.firing, case["firing"], case["id"])
            if "reason" in case:
                self.assertEqual(result.reason, case["reason"])

    def test_reconciliation_vectors(self) -> None:
        for case in self.load("reconciliation.json")["cases"]:
            value = case["snapshot"]
            snapshot = Snapshot(
                runs=tuple(
                    RunRow(row["runId"], row["status"])
                    for row in value["runs"]
                ),
                jobs=tuple(
                    JobRow(row["runId"], row["status"])
                    for row in value["jobs"]
                ),
                artifacts=tuple(
                    ArtifactRow(row["runId"], row["artifactId"])
                    for row in value["artifacts"]
                ),
                outbox=tuple(
                    OutboxRow(row["runId"], row["eventType"])
                    for row in value["outbox"]
                ),
                events=tuple(
                    EventRow(row["runId"], row["status"])
                    for row in value.get("events", [])
                ),
            )
            self.assertEqual(
                sorted(item.kind.value for item in inspect(snapshot)),
                sorted(case["findings"]),
                case["id"],
            )

    def test_telemetry_redaction_vectors(self) -> None:
        for case in self.load("telemetry.json")["cases"]:
            if "attributes" in case:
                self.assertEqual(redact(case["attributes"]), case["expected"])


if __name__ == "__main__":
    unittest.main()
