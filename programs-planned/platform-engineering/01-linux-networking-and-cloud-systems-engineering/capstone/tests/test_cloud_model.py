from __future__ import annotations

import unittest

from atlas_host.cloud_model import FailureDomainPlan, require_zone_tolerance


class CloudModelTests(unittest.TestCase):
    def test_single_zone_plan_cannot_claim_zone_tolerance(self) -> None:
        plan = FailureDomainPlan(instances=2, zones=1, durable_copies=2, load_balanced=True)
        with self.assertRaises(ValueError):
            require_zone_tolerance(plan)

    def test_multi_zone_plan_can_support_bounded_claim(self) -> None:
        plan = FailureDomainPlan(instances=2, zones=2, durable_copies=2, load_balanced=True)
        require_zone_tolerance(plan)
        self.assertIn("single-zone-failure-tolerance", plan.supported_claims())


if __name__ == "__main__":
    unittest.main()
