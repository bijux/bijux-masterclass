from __future__ import annotations

import unittest

from labs.class_creation.manual import (
    ClassRecipe,
    build_class,
    manual_creation_evidence,
)


class ManualClassCreationTests(unittest.TestCase):
    def test_recipe_inputs_become_class_identity_bases_and_namespace(self) -> None:
        marker = object()
        recipe = ClassRecipe(
            name="AuditedDelivery",
            bases=(object,),
            namespace={"marker": marker},
        )

        created = build_class(recipe)

        self.assertEqual(created.__name__, "AuditedDelivery")
        self.assertEqual(created.__bases__, (object,))
        self.assertIs(created.marker, marker)
        self.assertEqual(created.__module__, "labs.class_creation.manual")

    def test_build_class_copies_the_caller_namespace(self) -> None:
        namespace: dict[str, object] = {"channel": "console"}

        created = build_class(ClassRecipe("Delivery", (), namespace))
        namespace["channel"] = "webhook"

        self.assertEqual(created.channel, "console")

    def test_invalid_class_name_fails_before_type_is_called(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "class name must be an identifier",
        ):
            build_class(ClassRecipe("not a class", (), {}))

    def test_manual_evidence_connects_recipe_result_and_instance(self) -> None:
        evidence = manual_creation_evidence()

        self.assertEqual(evidence["recipe"]["name"], "DeliveryNotice")  # type: ignore[index]
        self.assertEqual(evidence["result"]["metaclass"], "type")  # type: ignore[index]
        self.assertEqual(  # type: ignore[index]
            evidence["result"]["rendered"],
            "DeliveryNotice:console",
        )
        self.assertTrue(  # type: ignore[index]
            evidence["timing"]["instance_type_is_result"],
        )


if __name__ == "__main__":
    unittest.main()
