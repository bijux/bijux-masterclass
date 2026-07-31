from __future__ import annotations

import unittest

from labs.descriptor_systems.external import (
    CountingStore,
    ExternalField,
    StoreUnavailable,
    external_storage_evidence,
)


class DescriptorSystemExternalTests(unittest.TestCase):
    def test_write_uses_a_stable_record_and_field_key(self) -> None:
        store = CountingStore()

        class Record:
            title = ExternalField(store, namespace="incident")

            def __init__(self, record_id: int) -> None:
                self.record_id = record_id

        record = Record(9)
        record.title = "triage"

        self.assertEqual(Record.title.key_for(record), "incident:Record:9:title")
        self.assertEqual(store.events[-1], {
            "operation": "write",
            "key": "incident:Record:9:title",
        })

    def test_second_instance_reads_the_authoritative_backend_value(self) -> None:
        store = CountingStore()

        class Record:
            status = ExternalField(store, namespace="incident")

            def __init__(self, record_id: int) -> None:
                self.record_id = record_id

        Record(4).status = {"state": "open"}
        observer = Record(4)

        self.assertEqual(observer.status, {"state": "open"})
        self.assertEqual(store.events[-1]["operation"], "read")
        self.assertTrue(Record.status.evidence(observer)["cached"])

    def test_local_cache_remains_stale_until_explicit_invalidation(self) -> None:
        evidence = external_storage_evidence()

        self.assertEqual(evidence["observed"], {
            "first": "investigating",
            "after_backend_change_without_invalidation": "investigating",
            "after_invalidation": "resolved",
        })
        self.assertEqual(evidence["authoritative_value"], "resolved")

    def test_missing_identity_is_refused_before_backend_access(self) -> None:
        store = CountingStore()

        class Record:
            title = ExternalField(store, namespace="incident")

        with self.assertRaisesRegex(ValueError, "record_id must exist"):
            Record().title = "cannot be keyed"
        self.assertEqual(store.events, [])

    def test_backend_failure_is_visible_on_an_uncached_read(self) -> None:
        store = CountingStore()

        class Record:
            title = ExternalField(store, namespace="incident")

            def __init__(self, record_id: int) -> None:
                self.record_id = record_id

        store.available = False
        with self.assertRaisesRegex(StoreUnavailable, "backend unavailable during read"):
            _ = Record(5).title

    def test_evidence_refuses_transaction_and_identity_map_claims(self) -> None:
        evidence = external_storage_evidence()

        self.assertFalse(evidence["transaction_support"])
        self.assertFalse(evidence["identity_map"])
        self.assertTrue(evidence["field"]["hidden_io"])
        self.assertEqual(evidence["field"]["serialization"], "JSON text")


if __name__ == "__main__":
    unittest.main()
