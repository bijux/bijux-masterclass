from __future__ import annotations

import unittest

from labs.runtime_governance.dynamic import (
    DynamicExecutionRefused,
    dynamic_execution_evidence,
    evaluate_arithmetic,
)


class DynamicExecutionGovernanceTests(unittest.TestCase):
    def test_bounded_arithmetic_is_evaluated(self) -> None:
        self.assertEqual(evaluate_arithmetic("6 * 7 + 1"), 43)
        self.assertEqual(evaluate_arithmetic("-9 / 2"), -4.5)

    def test_calls_and_names_are_refused_before_execution(self) -> None:
        with self.assertRaisesRegex(
            DynamicExecutionRefused,
            "outside the arithmetic policy",
        ):
            evaluate_arithmetic("__import__('os').getcwd()")

    def test_non_numeric_and_boolean_constants_are_refused(self) -> None:
        for source in ("'text'", "True"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(
                    DynamicExecutionRefused,
                    "constants must be int or float",
                ):
                    evaluate_arithmetic(source)

    def test_source_and_constant_bounds_are_explicit(self) -> None:
        with self.assertRaisesRegex(
            DynamicExecutionRefused,
            "exceeds 120 characters",
        ):
            evaluate_arithmetic("1" * 121)
        with self.assertRaisesRegex(
            DynamicExecutionRefused,
            "must not exceed 1000000",
        ):
            evaluate_arithmetic("1000001")

    def test_evidence_refuses_sandbox_claims(self) -> None:
        evidence = dynamic_execution_evidence()

        self.assertEqual(evidence["accepted"]["result"], 43)  # type: ignore[index]
        self.assertFalse(evidence["refused"]["executed"])  # type: ignore[index]
        self.assertFalse(  # type: ignore[index]
            evidence["trust_boundary"]["ast_validation_is_a_sandbox"],
        )


if __name__ == "__main__":
    unittest.main()
