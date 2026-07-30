from __future__ import annotations

import unittest

from labs.runtime_governance.patching import (
    patching_evidence,
    scoped_attribute_patch,
)


class ReversiblePatchingTests(unittest.TestCase):
    def test_replacement_is_visible_only_inside_the_scope(self) -> None:
        class Owner:
            value = "original"

        with scoped_attribute_patch(Owner, "value", "replacement"):
            self.assertEqual(Owner.value, "replacement")

        self.assertEqual(Owner.value, "original")

    def test_original_is_restored_after_body_failure(self) -> None:
        class Owner:
            value = "original"

        with self.assertRaisesRegex(RuntimeError, "body failed"):
            with scoped_attribute_patch(Owner, "value", "replacement"):
                raise RuntimeError("body failed")

        self.assertEqual(Owner.value, "original")

    def test_new_attribute_is_removed_after_scope(self) -> None:
        class Owner:
            pass

        with scoped_attribute_patch(Owner, "value", "replacement") as record:
            self.assertFalse(record.had_original)
            self.assertEqual(Owner.value, "replacement")

        self.assertFalse(hasattr(Owner, "value"))

    def test_dunder_patch_is_refused(self) -> None:
        class Owner:
            pass

        with self.assertRaisesRegex(
            ValueError,
            "must be a non-dunder name",
        ):
            with scoped_attribute_patch(Owner, "__class__", object()):
                pass

    def test_evidence_names_observability_and_concurrency_limit(self) -> None:
        evidence = patching_evidence()

        self.assertTrue(evidence["inside_scope"]["replacement_visible"])  # type: ignore[index]
        self.assertTrue(  # type: ignore[index]
            evidence["after_scope"]["original_identity_restored"],
        )
        self.assertFalse(evidence["boundary"]["concurrency_safe"])  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
