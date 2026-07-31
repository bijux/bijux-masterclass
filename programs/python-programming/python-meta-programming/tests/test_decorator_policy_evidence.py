from __future__ import annotations

import inspect
import json
import unittest

from labs.decorator_policy import RetryPolicy, retry
from labs.decorator_policy.evidence import build_evidence, render_evidence


class DecoratorPolicyEvidenceTests(unittest.TestCase):
    def test_retry_packet_exposes_captured_policy_and_multiplied_execution(self) -> None:
        packet = build_evidence()["retry"]

        self.assertEqual(
            packet["captured_policy"],
            {
                "exceptions": ["TransientDeliveryError"],
                "max_attempts": 3,
                "backoff_seconds": [0.1, 0.2],
            },
        )
        self.assertEqual(
            packet["events"],
            ["attempt:1", "sleep:0.1", "attempt:2", "sleep:0.2", "attempt:3"],
        )
        self.assertEqual(packet["underlying_execution_count"], 3)
        self.assertEqual(packet["result"], "delivered:INC-42")
        self.assertEqual(packet["visible_signature"], "(incident_id: 'str') -> 'str'")

    def test_exhausted_retry_has_a_finite_rule_and_preserves_final_failure(self) -> None:
        packet = build_evidence()["retry_exhausted"]

        self.assertEqual(packet["attempts"], 2)
        self.assertTrue(packet["same_final_failure_object"])
        self.assertIn("two total attempts", packet["stopping_rule"])

    def test_retry_catches_only_the_configured_exception_types(self) -> None:
        executions = 0

        @retry(
            exceptions=(ConnectionError,),
            max_attempts=2,
            backoff_seconds=(0.0,),
            sleep=lambda _: None,
        )
        def fail() -> None:
            nonlocal executions
            executions += 1
            raise ValueError("not retryable")

        with self.assertRaisesRegex(ValueError, "not retryable"):
            fail()

        self.assertEqual(executions, 1)

    def test_retry_factory_rejects_incoherent_policy_before_decoration(self) -> None:
        invalid_policies = (
            {"exceptions": (), "max_attempts": 1, "backoff_seconds": ()},
            {"exceptions": (Exception,), "max_attempts": 0, "backoff_seconds": ()},
            {"exceptions": (Exception,), "max_attempts": 3, "backoff_seconds": (0.1,)},
            {"exceptions": (Exception,), "max_attempts": 2, "backoff_seconds": (-0.1,)},
        )

        for policy in invalid_policies:
            with self.subTest(policy=policy), self.assertRaises(ValueError):
                retry(**policy)  # type: ignore[arg-type]

    def test_retry_wrapper_exposes_policy_and_preserves_callable_evidence(self) -> None:
        @retry(
            exceptions=(ConnectionError,),
            max_attempts=2,
            backoff_seconds=(0.1,),
            sleep=lambda _: None,
        )
        def deliver(incident_id: str, *, urgent: bool = False) -> str:
            """Deliver one incident."""

            return incident_id

        self.assertEqual(
            deliver.__retry_policy__,
            RetryPolicy(("ConnectionError",), 2, (0.1,)),
        )
        self.assertEqual(deliver.__name__, "deliver")
        self.assertEqual(deliver.__doc__, "Deliver one incident.")
        self.assertEqual(
            str(inspect.signature(deliver)),
            "(incident_id: 'str', *, urgent: 'bool' = False) -> 'str'",
        )
        self.assertIs(inspect.unwrap(deliver), deliver.__wrapped__)

    def test_validation_packet_distinguishes_enforcement_observation_and_refusal(self) -> None:
        packet = build_evidence()["validation"]

        self.assertFalse(packet["strict"]["executed"])
        self.assertIn("argument incident_id=42", packet["strict"]["failure"])
        self.assertTrue(packet["warning"]["executed"])
        self.assertEqual(packet["warning"]["result"], 42)
        self.assertIn("argument incident_id=42", packet["warning"]["message"])
        self.assertEqual(packet["refusal"]["timing"], "decoration")
        self.assertIn("list[int]", packet["refusal"]["message"])

    def test_rendered_evidence_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            ["cache_comparison", "retry", "retry_exhausted", "validation"],
        )

    def test_cache_comparison_exposes_key_policy_hooks_and_reset(self) -> None:
        packet = build_evidence()["cache_comparison"]

        self.assertEqual(
            packet["teaching_cache"]["executions"],
            ["INC-42:critical", "INC-42:critical"],
        )
        self.assertEqual(
            packet["teaching_cache"]["info"],
            {"hits": 1, "misses": 2, "maxsize": 2, "current_size": 2},
        )
        self.assertTrue(
            packet["teaching_cache"]["equivalent_keyword_order_is_one_key"]
        )
        self.assertFalse(
            packet["teaching_cache"]["equivalent_call_styles_are_one_key"]
        )
        self.assertEqual(packet["stdlib_lru_cache"]["executions"], ["int", "float"])
        self.assertEqual(
            packet["stdlib_lru_cache"]["info"],
            {"hits": 1, "misses": 2, "maxsize": 2, "current_size": 2},
        )
        self.assertEqual(
            packet["stdlib_lru_cache"]["parameters"],
            {"maxsize": 2, "typed": True},
        )
        self.assertEqual(
            packet["after_clear"],
            {"teaching_cache_size": 0, "stdlib_cache_size": 0},
        )


if __name__ == "__main__":
    unittest.main()
