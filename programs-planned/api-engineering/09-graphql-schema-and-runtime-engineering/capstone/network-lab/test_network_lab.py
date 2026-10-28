import unittest
from pathlib import Path

from graph_lab.tour import run_tour


ROOT = Path(__file__).resolve().parents[2]


class NetworkLabTests(unittest.TestCase):
    def test_real_loopback_composition_and_partial_failure(self):
        value = run_tour(ROOT)

        self.assertEqual(value["complete_run_count"], 2)
        self.assertEqual(value["complete_errors"], 0)
        self.assertIsNone(value["partial_artifacts"])
        self.assertEqual(
            value["partial_error_path"],
            [
                "project",
                "analysisRuns",
                "edges",
                0,
                "node",
                "artifacts",
            ],
        )
        self.assertEqual(
            value["partial_error_service"],
            "artifact-service",
        )
        self.assertIsNone(value["other_tenant_project"])
