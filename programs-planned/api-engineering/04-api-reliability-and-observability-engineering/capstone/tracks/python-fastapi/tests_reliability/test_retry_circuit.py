from __future__ import annotations

import unittest

from api_reliability.circuit import CircuitBreaker, CircuitOpen, CircuitState
from api_reliability.clock import ManualClock
from api_reliability.retry import RetryPolicy, RetrySafety, plan_retry_delays, retryable


class RetryCircuitTests(unittest.TestCase):
    def test_full_jitter_is_deterministic_for_fixture_seed(self) -> None:
        policy = RetryPolicy(max_attempts=4, initial_delay_ms=100, maximum_delay_ms=1_000)
        self.assertEqual(plan_retry_delays(policy, seed=7), [41, 38, 202])

    def test_unsafe_operation_is_not_retried(self) -> None:
        self.assertFalse(retryable(status=503, transport_error=False, safety=RetrySafety.UNSAFE))
        self.assertTrue(retryable(status=503, transport_error=False, safety=RetrySafety.IDEMPOTENT))

    def test_circuit_half_open_probe(self) -> None:
        clock = ManualClock()
        breaker = CircuitBreaker(failure_threshold=2, open_duration_ms=100)
        breaker.allow(clock)
        breaker.failure(clock)
        breaker.allow(clock)
        breaker.failure(clock)
        self.assertEqual(breaker.state, CircuitState.OPEN)
        with self.assertRaises(CircuitOpen):
            breaker.allow(clock)
        clock.advance(100)
        breaker.allow(clock)
        self.assertEqual(breaker.state, CircuitState.HALF_OPEN)
        breaker.success()
        self.assertEqual(breaker.state, CircuitState.CLOSED)


if __name__ == "__main__":
    unittest.main()
