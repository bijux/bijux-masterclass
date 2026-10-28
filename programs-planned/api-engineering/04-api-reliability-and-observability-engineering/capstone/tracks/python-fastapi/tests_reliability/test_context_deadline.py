from __future__ import annotations

import unittest

from api_reliability.clock import ManualClock
from api_reliability.context import TraceContextError, parse_traceparent
from api_reliability.deadline import Deadline, DeadlineExceeded


class ContextDeadlineTests(unittest.TestCase):
    def test_traceparent_round_trip(self) -> None:
        value = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
        context = parse_traceparent(value)
        self.assertTrue(context.sampled)
        self.assertEqual(context.traceparent(), value)

    def test_zero_trace_id_rejected(self) -> None:
        with self.assertRaises(TraceContextError):
            parse_traceparent("00-00000000000000000000000000000000-00f067aa0ba902b7-01")

    def test_deadline_child_cannot_extend_parent(self) -> None:
        clock = ManualClock(1_000)
        parent = Deadline.after(clock, 500)
        child = parent.child(clock, 2_000)
        self.assertEqual(child.expires_at_ms, parent.expires_at_ms)
        clock.advance(500)
        with self.assertRaises(DeadlineExceeded):
            child.require_remaining(clock)


if __name__ == "__main__":
    unittest.main()
