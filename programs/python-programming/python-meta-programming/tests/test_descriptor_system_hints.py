from __future__ import annotations

import unittest
from typing import Annotated

from labs.descriptor_systems.hints import (
    HintField,
    Minimum,
    NonBlank,
    RetryPolicy,
    UnsupportedHint,
    compile_hint,
    hint_evidence,
)


class DescriptorSystemHintTests(unittest.TestCase):
    def test_scalar_values_are_coerced_by_explicit_rules(self) -> None:
        policy = RetryPolicy(
            attempts="3",
            label=" retry ",
            timeout=2,
            enabled="off",
        )

        self.assertEqual(policy.attempts, 3)
        self.assertEqual(policy.label, "retry")
        self.assertEqual(policy.timeout, 2.0)
        self.assertIs(policy.enabled, False)

    def test_optional_hint_accepts_none_without_coercion(self) -> None:
        policy = RetryPolicy(
            attempts=0,
            label="immediate",
            timeout=None,
            enabled=True,
        )

        self.assertIsNone(policy.timeout)
        self.assertEqual(vars(policy)["__hint_trace__"][2]["decision"], "none")

    def test_value_rules_run_after_coercion(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be >= 0"):
            RetryPolicy(
                attempts="-1",
                label="retry",
                timeout=None,
                enabled=True,
            )

    def test_bool_does_not_pass_as_an_integer(self) -> None:
        plan = compile_hint(int)

        with self.assertRaisesRegex(TypeError, "integer coercion"):
            plan.accept(True)

    def test_parameterized_generics_and_unknown_metadata_are_refused(self) -> None:
        with self.assertRaisesRegex(UnsupportedHint, "parameterized generics"):
            compile_hint(list[int])
        with self.assertRaisesRegex(UnsupportedHint, "explicit ValueRule"):
            compile_hint(Annotated[int, "minimum=0"])

    def test_missing_annotation_is_refused_during_name_binding(self) -> None:
        class MissingHint:
            pass

        with self.assertRaisesRegex(TypeError, "requires a type annotation"):
            HintField().__set_name__(MissingHint, "value")

    def test_evidence_publishes_success_and_refusal_surfaces(self) -> None:
        evidence = hint_evidence()

        self.assertEqual(evidence["stored"], {
            "attempts": 3,
            "label": "delivery retry",
            "timeout": 2.0,
            "enabled": True,
        })
        self.assertEqual(
            set(evidence["refused"]),
            {"parameterized_generic", "unknown_metadata", "arbitrary_class"},
        )
        self.assertFalse(evidence["full_runtime_typing"])
        self.assertIn("parameterized generics", evidence["plans"]["attempts"]["refused"])


if __name__ == "__main__":
    unittest.main()
