import unittest
from distributed_api.boundary import BoundaryCandidate, decision
from distributed_api.catalog import ServiceCatalog, ServiceDefinition
from distributed_api.model import ValidationError


class BoundaryCatalogTests(unittest.TestCase):
    def test_notification_extraction_has_positive_evidence(self):
        candidate = BoundaryCandidate("notification", 2, 2, 2, 1, 2, 1, 1, 0)
        self.assertEqual(decision(candidate), "extract")

    def test_data_autonomy_blocks_extraction(self):
        candidate = BoundaryCandidate("project-table", 1, 0, 0, 0, 0, 0, 1, 2)
        self.assertEqual(decision(candidate), "reject")

    def test_catalog_requires_one_writer(self):
        catalog = ServiceCatalog()
        catalog.add(ServiceDefinition("control","team-a","business",frozenset({"run"})))
        catalog.add(ServiceDefinition("artifact","team-b","business",frozenset({"artifact"})))
        catalog.validate_single_writers()
        self.assertEqual(catalog.owner_of("run"), "control")

    def test_catalog_rejects_duplicate_writer(self):
        catalog = ServiceCatalog()
        catalog.add(ServiceDefinition("a","one","business",frozenset({"run"})))
        catalog.add(ServiceDefinition("b","two","business",frozenset({"run"})))
        with self.assertRaises(ValidationError):
            catalog.validate_single_writers()

    def test_catalog_rejects_table_service(self):
        catalog = ServiceCatalog()
        catalog.add(ServiceDefinition("project-service","team","business"))
        with self.assertRaises(ValidationError):
            catalog.validate_no_table_services()


if __name__ == "__main__": unittest.main()
