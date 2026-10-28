from __future__ import annotations

from pathlib import Path
import unittest

import jsonschema

from event_engineering.contracts import load_schema, validate_payload

from helpers import event


SCHEMA = (
    Path(__file__).resolve().parents[3]
    / "contracts/components/schemas/analysis-run-completed.v1.schema.json"
)


class ContractTests(unittest.TestCase):
    def test_completed_payload_satisfies_schema_and_formats(self) -> None:
        validate_payload(event("66"), load_schema(SCHEMA))

    def test_invalid_event_time_inside_data_is_rejected(self) -> None:
        value = event(
            "67",
            data={
                "runId": "run-001",
                "durationMs": 1000,
                "artifactCount": 1,
                "occurredAt": "not-a-time",
            },
        )
        with self.assertRaises(jsonschema.ValidationError):
            validate_payload(value, load_schema(SCHEMA))

    def test_unknown_public_payload_property_is_rejected(self) -> None:
        value = event(
            "68",
            data={
                "runId": "run-001",
                "durationMs": 1000,
                "artifactCount": 1,
                "occurredAt": "2026-08-07T10:00:00Z",
                "leaseToken": "private",
            },
        )
        with self.assertRaises(jsonschema.ValidationError):
            validate_payload(value, load_schema(SCHEMA))


class CanonicalExampleParityTests(unittest.TestCase):
    def test_examples_match_published_canonical_hashes(self) -> None:
        import hashlib
        import json

        root = Path(__file__).resolve().parents[3]
        vector = json.loads(
            (root / "shared/vectors/envelope.json").read_text(encoding="utf-8")
        )
        examples = root / "contracts/examples"
        from event_engineering.envelope import EventEnvelope

        for row in vector["canonicalExamples"]:
            event_value = json.loads((examples / row["file"]).read_text(encoding="utf-8"))
            event = EventEnvelope(**event_value)
            self.assertEqual(hashlib.sha256(event.canonical_bytes()).hexdigest(), row["sha256"])


if __name__ == "__main__":
    unittest.main()
