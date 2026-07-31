from __future__ import annotations

import unittest

from labs.study_practice.catalog import STUDY_ROUTES, route_for


class StudyPracticeCatalogTests(unittest.TestCase):
    def test_catalog_covers_substantive_modules_in_order(self) -> None:
        self.assertEqual([route.module for route in STUDY_ROUTES], list(range(1, 11)))

    def test_each_route_starts_with_course_evidence_before_capstone_transfer(self) -> None:
        for route in STUDY_ROUTES:
            with self.subTest(module=route.module):
                self.assertTrue(route.course_command.startswith("make "))
                self.assertTrue(route.focused_test_command.startswith("make "))
                self.assertTrue(route.capstone_command.startswith("make capstone-"))
                self.assertNotEqual(route.course_command, route.capstone_command)

    def test_each_route_preserves_an_earlier_contract_and_names_exit_evidence(self) -> None:
        for route in STUDY_ROUTES:
            with self.subTest(module=route.module):
                self.assertGreater(len(route.preserved_contract), 20)
                self.assertGreater(len(route.exit_evidence), 20)

    def test_route_for_returns_the_exact_catalog_entry(self) -> None:
        self.assertIs(route_for(7), STUDY_ROUTES[6])

    def test_route_for_rejects_orientation_and_unknown_modules(self) -> None:
        for module in (0, 11):
            with self.subTest(module=module):
                with self.assertRaisesRegex(ValueError, "between 1 and 10"):
                    route_for(module)


if __name__ == "__main__":
    unittest.main()
