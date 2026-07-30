from __future__ import annotations

import unittest

from labs.descriptor_systems.cache import (
    CachedComputation,
    Document,
    InvalidatingField,
    cache_evidence,
)


class DescriptorSystemCacheTests(unittest.TestCase):
    def test_repeated_read_reuses_one_per_instance_computation(self) -> None:
        document = Document("one careful cache")

        self.assertEqual(document.word_count, 3)
        self.assertEqual(document.word_count, 3)
        self.assertEqual(Document.word_count.evidence(document)["computations"], 1)

    def test_dependency_assignment_invalidates_before_the_next_read(self) -> None:
        document = Document("old value")
        self.assertEqual(document.word_count, 2)

        document.text = "a replacement with four words"

        self.assertFalse(Document.word_count.evidence(document)["cached"])
        self.assertEqual(document.word_count, 5)
        self.assertEqual(Document.word_count.evidence(document)["computations"], 2)

    def test_cached_state_is_isolated_per_instance(self) -> None:
        first = Document("one")
        second = Document("two separate")

        self.assertEqual(first.word_count, 1)
        self.assertEqual(second.word_count, 2)
        self.assertIn(Document.word_count.cache_name, vars(first))
        self.assertIn(Document.word_count.cache_name, vars(second))
        self.assertEqual(Document.word_count.evidence(first)["computations"], 1)
        self.assertEqual(Document.word_count.evidence(second)["computations"], 1)

    def test_invalidating_field_rejects_a_non_cache_target(self) -> None:
        with self.assertRaisesRegex(TypeError, "is not a CachedComputation"):

            class BrokenDocument:
                text = InvalidatingField(invalidates=("summary",))
                summary = "plain class state"

            BrokenDocument().text = "cannot invalidate a string"

    def test_cached_computation_requires_a_named_dependency(self) -> None:
        with self.assertRaisesRegex(ValueError, "must name at least one dependency"):
            CachedComputation(lambda value: value, depends_on=())

    def test_evidence_names_freshness_owner_and_bypass_limit(self) -> None:
        evidence = cache_evidence()

        self.assertEqual(evidence["reads"], {
            "first": 3,
            "second": 3,
            "after_dependency_change": 5,
        })
        self.assertEqual(evidence["invalidation_owner"], "Document.text assignment")
        self.assertIn("bypasses", evidence["bypass_limit"])
        self.assertFalse(evidence["cross_instance_coherence"])


if __name__ == "__main__":
    unittest.main()
