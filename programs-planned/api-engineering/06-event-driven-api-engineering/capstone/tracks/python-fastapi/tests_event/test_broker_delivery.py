from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest

from event_engineering.broker import BrokerError, DeterministicBroker

from helpers import event


class BrokerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = [datetime(2026, 8, 7, 10, 0, tzinfo=timezone.utc)]
        self.broker = DeterministicBroker(clock=lambda: self.now[0])
        self.broker.create_channel("analysis.events", 4)

    def test_ack_advances_one_group_only(self) -> None:
        self.broker.publish("analysis.events", "run-001", event("10"))
        a = self.broker.poll("analytics", "analysis.events")[0]
        self.broker.ack(a.token)
        self.assertEqual(self.broker.poll("analytics", "analysis.events"), [])
        self.assertEqual(len(self.broker.poll("audit", "analysis.events")), 1)

    def test_expired_ack_redelivers_same_record(self) -> None:
        self.broker.publish("analysis.events", "run-001", event("11"))
        first = self.broker.poll(
            "analytics", "analysis.events", ack_wait=timedelta(seconds=5)
        )[0]
        self.now[0] += timedelta(seconds=6)
        second = self.broker.poll("analytics", "analysis.events")[0]
        self.assertEqual(first.record.event.id, second.record.event.id)
        self.assertEqual(second.attempt, 2)
        self.assertNotEqual(first.token, second.token)

    def test_nack_delays_redelivery(self) -> None:
        self.broker.publish("analysis.events", "run-001", event("12"))
        delivery = self.broker.poll("analytics", "analysis.events")[0]
        self.broker.nack(delivery.token, timedelta(seconds=10))
        self.assertEqual(self.broker.poll("analytics", "analysis.events"), [])
        self.now[0] += timedelta(seconds=10)
        self.assertEqual(self.broker.poll("analytics", "analysis.events")[0].attempt, 2)

    def test_token_settles_once(self) -> None:
        self.broker.publish("analysis.events", "run-001", event("13"))
        delivery = self.broker.poll("analytics", "analysis.events")[0]
        self.broker.ack(delivery.token)
        with self.assertRaises(BrokerError):
            self.broker.ack(delivery.token)

    def test_per_partition_order(self) -> None:
        self.broker.publish("analysis.events", "run-001", event("14"))
        self.broker.publish("analysis.events", "run-001", event("15"))
        first = self.broker.poll("analytics", "analysis.events")[0]
        self.assertEqual(first.record.offset, 0)
        self.assertEqual(self.broker.poll("analytics", "analysis.events"), [])
        self.broker.ack(first.token)
        second = self.broker.poll("analytics", "analysis.events")[0]
        self.assertEqual(second.record.offset, 1)


if __name__ == "__main__":
    unittest.main()
