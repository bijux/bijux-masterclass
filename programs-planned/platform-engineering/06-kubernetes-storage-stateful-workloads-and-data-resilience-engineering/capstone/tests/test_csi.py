import unittest
from atlas_data.csi import SemanticCSI, CSIError


class CSITests(unittest.TestCase):
    def setUp(self):
        self.driver = SemanticCSI("csi.atlas.example.invalid")
        self.volume = self.driver.create_volume("pvc-1", 20, "zone-a")

    def test_create_replay_returns_same_volume(self):
        replay = self.driver.create_volume("pvc-1", 20, "zone-a")
        self.assertIs(self.volume, replay)
        self.assertEqual(len(self.driver._by_id), 1)

    def test_create_conflict_is_rejected(self):
        with self.assertRaises(CSIError):
            self.driver.create_volume("pvc-1", 30, "zone-a")

    def test_lifecycle_requires_order(self):
        with self.assertRaises(CSIError):
            self.driver.node_stage(self.volume.id, "node-a")
        self.driver.controller_publish(self.volume.id, "node-a")
        self.driver.node_stage(self.volume.id, "node-a")
        self.driver.node_publish(self.volume.id, "node-a", "pod/db")
        self.assertEqual(self.driver.volume(self.volume.id).published_targets, {"pod/db"})

    def test_multi_attach_is_rejected(self):
        self.driver.controller_publish(self.volume.id, "node-a")
        with self.assertRaises(CSIError):
            self.driver.controller_publish(self.volume.id, "node-b")

    def test_safe_reverse_lifecycle(self):
        self.driver.controller_publish(self.volume.id, "node-a")
        self.driver.node_stage(self.volume.id, "node-a")
        self.driver.node_publish(self.volume.id, "node-a", "pod/db")
        with self.assertRaises(CSIError):
            self.driver.node_unstage(self.volume.id, "node-a")
        self.driver.node_unpublish(self.volume.id, "pod/db")
        self.driver.node_unstage(self.volume.id, "node-a")
        self.driver.controller_unpublish(self.volume.id, "node-a")
        self.driver.delete_volume(self.volume.id)
        with self.assertRaises(CSIError):
            self.driver.volume(self.volume.id)

    def test_expand_does_not_shrink(self):
        self.driver.expand(self.volume.id, 40)
        self.assertEqual(self.driver.volume(self.volume.id).capacity_gib, 40)
        with self.assertRaises(CSIError):
            self.driver.expand(self.volume.id, 10)


if __name__ == "__main__":
    unittest.main()
