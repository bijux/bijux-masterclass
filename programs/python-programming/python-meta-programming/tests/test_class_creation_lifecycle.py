from __future__ import annotations

import unittest

from labs.class_creation.lifecycle import lifecycle_evidence


class MetaclassLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence = lifecycle_evidence()

    def test_successful_class_creation_has_an_exact_hook_order(self) -> None:
        successful = self.evidence["successful_class"]

        self.assertEqual(  # type: ignore[index]
            successful["events"],
            [
                "prepare:DeliveryNotice",
                "body:DeliveryNotice",
                "new:DeliveryNotice",
                "init:DeliveryNotice",
            ],
        )

    def test_new_shapes_the_class_and_init_records_it(self) -> None:
        successful = self.evidence["successful_class"]

        self.assertEqual(successful["creation_owner"], "LifecycleMeta")  # type: ignore[index]
        self.assertEqual(  # type: ignore[index]
            successful["registered_names"],
            ["DeliveryNotice"],
        )

    def test_instance_construction_does_not_repeat_class_creation_hooks(self) -> None:
        instance = self.evidence["instance"]

        self.assertEqual(instance["type"], "DeliveryNotice")  # type: ignore[index]
        self.assertFalse(instance["metaclass_hooks_reran"])  # type: ignore[index]

    def test_new_failure_prevents_metaclass_init(self) -> None:
        rejected = self.evidence["rejected_class"]

        self.assertEqual(rejected["events"], ["new:MissingChannel"])  # type: ignore[index]
        self.assertEqual(rejected["message"], "MissingChannel must declare channel")  # type: ignore[index]
        self.assertFalse(rejected["init_ran"])  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
