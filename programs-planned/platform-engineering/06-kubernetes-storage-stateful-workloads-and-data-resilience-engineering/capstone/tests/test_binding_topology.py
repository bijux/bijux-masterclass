import unittest
from atlas_data.binding import Binder, BindingError
from atlas_data.models import Claim, StorageClass, Volume, Node, CapacitySegment
from atlas_data.topology import Scheduler


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.binder = Binder([StorageClass.atlas_default()])

    def test_wait_for_consumer_requires_zone(self):
        claim = Claim("atlas", "db", 20, ("ReadWriteOncePod",), "atlas-rwo-durable")
        with self.assertRaises(BindingError):
            self.binder.bind(claim)

    def test_dynamic_binding_in_selected_zone(self):
        claim = Claim("atlas", "db", 20, ("ReadWriteOncePod",), "atlas-rwo-durable")
        result = self.binder.bind(claim, selected_zone="zone-b")
        self.assertTrue(result.created)
        self.assertEqual(result.volume.zone, "zone-b")
        self.assertEqual(claim.phase, "Bound")

    def test_idempotent_bound_claim(self):
        claim = Claim("atlas", "db", 20, ("ReadWriteOncePod",), "atlas-rwo-durable")
        first = self.binder.bind(claim, selected_zone="zone-a")
        second = self.binder.bind(claim, selected_zone="zone-a")
        self.assertEqual(first.volume.name, second.volume.name)
        self.assertFalse(second.created)

    def test_existing_volume_must_match_mode(self):
        volume = Volume("pv-x", "x", 20, ("ReadWriteOncePod",), "atlas-rwo-durable", "zone-a", "Retain", volume_mode="Block")
        binder = Binder([StorageClass.atlas_default()], [volume])
        claim = Claim("atlas", "db", 20, ("ReadWriteOncePod",), "atlas-rwo-durable", volume_mode="Filesystem")
        result = binder.bind(claim, selected_zone="zone-a")
        self.assertNotEqual(result.volume.name, "pv-x")

    def test_release_preserves_volume_identity(self):
        claim = Claim("atlas", "db", 20, ("ReadWriteOncePod",), "atlas-rwo-durable")
        result = self.binder.bind(claim, selected_zone="zone-a")
        released = self.binder.release(claim)
        self.assertEqual(released.name, result.volume.name)
        self.assertEqual(released.phase, "Released")


class TopologyTests(unittest.TestCase):
    def test_scheduler_preserves_rejection_reasons(self):
        scheduler = Scheduler(
            [Node("a", "zone-a", 1, 1), Node("b", "zone-b", 4, 0)],
            [CapacitySegment("zone-a", "atlas-rwo-durable", 100), CapacitySegment("zone-b", "atlas-rwo-durable", 10)],
        )
        decision = scheduler.place("db", [("data", 20)])
        self.assertIsNone(decision.node)
        self.assertIn("volume attachment limit exceeded", decision.explanations["a"])
        self.assertIn("insufficient accessible storage capacity", decision.explanations["b"])

    def test_scheduler_selects_compatible_node(self):
        scheduler = Scheduler(
            [Node("a", "zone-a", 4, 0), Node("b", "zone-b", 4, 0)],
            [CapacitySegment("zone-a", "atlas-rwo-durable", 100), CapacitySegment("zone-b", "atlas-rwo-durable", 5)],
        )
        decision = scheduler.place("db", [("data", 20)], required_zones={"zone-a"})
        self.assertEqual(decision.node, "a")


if __name__ == "__main__":
    unittest.main()
