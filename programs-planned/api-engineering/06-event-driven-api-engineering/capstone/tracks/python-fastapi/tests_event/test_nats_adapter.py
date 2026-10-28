from __future__ import annotations

import unittest

from event_engineering.nats_adapter import to_nats_request

from helpers import event


class NatsAdapterTests(unittest.TestCase):
    def test_request_preserves_structured_event_and_message_identity(self) -> None:
        value = event("64")
        request = to_nats_request("analysis.events.run.lifecycle.v1", value)
        self.assertEqual(request.message_id, value.id)
        self.assertEqual(request.headers["Content-Type"], "application/cloudevents+json")
        self.assertIn(value.id.encode(), request.payload)

    def test_invalid_subject_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            to_nats_request("analysis events", event("65"))


if __name__ == "__main__":
    unittest.main()
