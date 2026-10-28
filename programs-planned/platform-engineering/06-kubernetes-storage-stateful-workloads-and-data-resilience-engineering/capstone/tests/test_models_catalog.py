import unittest
from atlas_data.catalog import atlas_catalog, catalogue_document
from atlas_data.models import DataClass, FailureDomain, StorageClass, Claim


class ModelTests(unittest.TestCase):
    def test_catalogue_has_distinct_data_classes(self):
        catalog = atlas_catalog()
        self.assertEqual(set(catalog), {"run-state", "artifacts", "worker-scratch", "read-cache", "recovery-evidence"})
        self.assertTrue(catalog["run-state"].authoritative)
        self.assertEqual(catalog["worker-scratch"].maximum_loss, FailureDomain.POD)

    def test_catalogue_document_serializes_enum(self):
        document = catalogue_document()
        self.assertEqual(document["schemaVersion"], "1.0")
        self.assertEqual(len(document["dataClasses"]), 5)

    def test_invalid_recovery_objective_is_rejected(self):
        item = DataClass("bad", True, FailureDomain.NODE, -1, 0, 1)
        with self.assertRaises(ValueError):
            item.validate()

    def test_storage_class_validation(self):
        StorageClass.atlas_default().validate()
        with self.assertRaises(ValueError):
            StorageClass("x", "driver", binding_mode="Later").validate()

    def test_claim_validation(self):
        claim = Claim("ns", "data", 1, ("ReadWriteOncePod",), "atlas-rwo-durable")
        claim.validate()
        claim.requested_gib = 0
        with self.assertRaises(ValueError):
            claim.validate()


if __name__ == "__main__":
    unittest.main()
