from __future__ import annotations

import unittest

from labs.study_practice.reentry import build_reentry_plan


class StudyPracticeReentryTests(unittest.TestCase):
    def test_new_learner_starts_with_orientation_then_module_one_course_evidence(self) -> None:
        plan = build_reentry_plan(0)

        self.assertIsNone(plan.refresh)
        self.assertEqual(plan.continue_with.module, 1)
        self.assertEqual(plan.order[0], "read the Module 00 study contract")
        self.assertEqual(plan.order[-1], "make capstone-manifest")

    def test_returning_learner_reproves_last_trusted_contract_before_continuing(self) -> None:
        plan = build_reentry_plan(4)

        self.assertEqual(plan.refresh.module, 4)  # type: ignore[union-attr]
        self.assertEqual(plan.continue_with.module, 5)
        self.assertLess(
            plan.order.index("make wrapper-lab-test"),
            plan.order.index("make decorator-policy-lab"),
        )
        self.assertLess(
            plan.order.index("make decorator-policy-lab-test"),
            plan.order.index("make capstone-check-action"),
        )

    def test_mastery_return_repeats_governance_before_application_transfer(self) -> None:
        plan = build_reentry_plan(10)

        self.assertEqual(plan.refresh.module, 10)  # type: ignore[union-attr]
        self.assertEqual(plan.continue_with.module, 10)
        self.assertLess(
            plan.order.index("make runtime-governance-lab-test"),
            plan.order.index("make capstone-governance"),
        )

    def test_reentry_plan_defers_the_broad_gate(self) -> None:
        self.assertTrue(build_reentry_plan(7).broad_gate_deferred)

    def test_unknown_boundaries_are_refused(self) -> None:
        for module in (-1, 11):
            with self.subTest(module=module):
                with self.assertRaisesRegex(ValueError, "between 0 and 10"):
                    build_reentry_plan(module)


if __name__ == "__main__":
    unittest.main()
