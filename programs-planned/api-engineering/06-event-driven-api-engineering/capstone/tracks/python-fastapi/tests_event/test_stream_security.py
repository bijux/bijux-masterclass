from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest

from event_engineering.security import (
    ProducerGrant,
    SecurityError,
    authorize_message,
    sign_message,
    verify_message,
)
from event_engineering.stream import EventTimeWindows

from helpers import event


class StreamSecurityTests(unittest.TestCase):
    def test_event_time_window_and_duplicate(self) -> None:
        windows = EventTimeWindows(timedelta(minutes=5), timedelta(minutes=10))
        value = event("40")
        first = windows.apply(value)
        duplicate = windows.apply(value)
        self.assertEqual(first.completed, 1)
        self.assertIsNone(duplicate)

    def test_late_event_recorded(self) -> None:
        windows = EventTimeWindows(timedelta(minutes=5), timedelta(minutes=1))
        windows.advance_watermark(datetime(2026, 8, 7, 11, 0, tzinfo=timezone.utc))
        value = event(
            "41",
            data={"runId": "run-001", "durationMs": 1, "artifactCount": 1, "occurredAt": "2026-08-07T10:00:00Z"},
        )
        self.assertIsNone(windows.apply(value))
        self.assertEqual(len(windows.late_events), 1)

    def test_authorization(self) -> None:
        value = event("42")
        grant = ProducerGrant(
            producer_id="control",
            sources=frozenset({value.source}),
            channels=frozenset({"analysis.events"}),
            event_types=frozenset({value.type}),
            tenants=frozenset({"tenant-a"}),
        )
        authorize_message(grant, "analysis.events", value)
        with self.assertRaises(SecurityError):
            authorize_message(grant, "artifact.events", value)

    def test_sensitive_payload_rejected(self) -> None:
        value = event("43", data={"runId": "run-001", "accessToken": "secret"})
        grant = ProducerGrant("control", frozenset({value.source}), frozenset({"analysis.events"}), frozenset({value.type}), frozenset({"tenant-a"}))
        with self.assertRaises(SecurityError):
            authorize_message(grant, "analysis.events", value)

    def test_cross_language_signature_profile(self) -> None:
        value = event("44")
        now = datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc)
        signed = sign_message(value, "key-1", b"fixture-secret", now)
        verify_message(signed, {"key-1": b"fixture-secret"}, now)
        self.assertTrue(signed.signature.startswith("sha256="))

    def test_stale_signature_rejected(self) -> None:
        value = event("45")
        then = datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc)
        signed = sign_message(value, "key-1", b"fixture-secret", then)
        with self.assertRaises(SecurityError):
            verify_message(signed, {"key-1": b"fixture-secret"}, then + timedelta(hours=1))


if __name__ == "__main__":
    unittest.main()
