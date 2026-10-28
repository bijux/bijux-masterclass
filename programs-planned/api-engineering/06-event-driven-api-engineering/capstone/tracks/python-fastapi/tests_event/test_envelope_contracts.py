from __future__ import annotations

import math
import unittest

from event_engineering.canonical import CanonicalizationError, canonical_json
from event_engineering.envelope import EnvelopeError, EventEnvelope
from event_engineering.partitioning import partition_for

from helpers import event


class EnvelopeTests(unittest.TestCase):
    def test_canonical_key_order(self) -> None:
        self.assertEqual(canonical_json({"b": 1, "a": 2}), '{"a":2,"b":1}')

    def test_rejects_nonfinite_and_unsafe_integer(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({"x": math.nan})
        with self.assertRaises(CanonicalizationError):
            canonical_json({"x": 9_007_199_254_740_992})
        with self.assertRaises(CanonicalizationError):
            canonical_json({"x": 1.5})

    def test_valid_event_is_deterministic(self) -> None:
        first = event("1")
        second = event("1")
        self.assertEqual(first.canonical_bytes(), second.canonical_bytes())

    def test_invalid_type_rejected(self) -> None:
        value = event("2").to_dict()
        value["type"] = "AnalysisCompleted"
        with self.assertRaises(EnvelopeError):
            EventEnvelope(**value)

    def test_invalid_causation_identity_is_rejected(self) -> None:
        value = event("3").to_dict()
        value["causationid"] = "not-a-uuid"
        with self.assertRaises(EnvelopeError):
            EventEnvelope(**value)

    def test_partition_is_stable(self) -> None:
        self.assertEqual(partition_for("run-001", 8), partition_for("run-001", 8))
        self.assertGreaterEqual(partition_for("run-001", 8), 0)
        self.assertLess(partition_for("run-001", 8), 8)


if __name__ == "__main__":
    unittest.main()
