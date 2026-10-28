import unittest
from atlas_data.architecture import DataServiceDecision
from atlas_data.migration import MigrationPhase, MigrationPlan
from atlas_data.performance import StorageWorkload
from atlas_data.release import ReleaseEvaluator


class ArchitectureTests(unittest.TestCase):
    def test_managed_recommendation(self):
        result = DataServiceDecision.evaluate("db", "limited", False, True)
        self.assertEqual(result.recommendation, "managed-service")

    def test_custom_engine_requires_control(self):
        result = DataServiceDecision.evaluate("engine", "expert", True, False)
        self.assertEqual(result.recommendation, "operator-or-direct")


class PerformanceTests(unittest.TestCase):
    def test_throughput_math(self):
        workload = StorageWorkload(1200, 16, 8, 12)
        self.assertEqual(workload.throughput_mib_s, 18.75)
        self.assertTrue(workload.within_budget(10, 16))

    def test_queue_time(self):
        workload = StorageWorkload(100, 4, 2, 5)
        self.assertEqual(workload.average_outstanding_seconds, 0.05)


class MigrationReleaseTests(unittest.TestCase):
    def test_migration_order_and_evidence(self):
        plan = MigrationPlan([
            MigrationPhase("expand", True, False, ("schema",)),
            MigrationPhase("backfill", True, False, ("counts",)),
            MigrationPhase("contract", False, True, ("old-writers-gone",)),
        ])
        with self.assertRaises(ValueError):
            plan.complete("backfill", {"counts"})
        plan.complete("expand", {"schema"})
        plan.complete("backfill", {"counts"})
        self.assertTrue(plan.rollback_allowed())
        plan.complete("contract", {"old-writers-gone"})
        self.assertFalse(plan.rollback_allowed())

    def test_release_accept_review_reject(self):
        evaluator = ReleaseEvaluator()
        accepted = evaluator.evaluate({
            "predecessor": "pass", "single_writer": "pass",
            "restore_drill": "pass", "migration_compatibility": "pass",
        })
        self.assertEqual(accepted.decision, "accepted")
        review = evaluator.evaluate({
            "predecessor": "pass", "single_writer": "pass",
            "restore_drill": "pass", "migration_compatibility": "pass",
            "native_csi": "not-executed",
        })
        self.assertEqual(review.decision, "review-required")
        rejected = evaluator.evaluate({"predecessor": "pass"})
        self.assertEqual(rejected.decision, "rejected")


if __name__ == "__main__":
    unittest.main()
