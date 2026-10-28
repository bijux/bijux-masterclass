import tempfile
import unittest
from pathlib import Path
from atlas_data.fencing import FenceRegistry
from atlas_data.ledger import DurableLedger
from atlas_data.stateful import StatefulSetPlanner


class StatefulTests(unittest.TestCase):
    def test_stable_identity(self):
        planner = StatefulSetPlanner("atlas-db", "atlas-system", "atlas-db", ("data", "wal"))
        identity = planner.identity(2)
        self.assertEqual(identity.pod_name, "atlas-db-2")
        self.assertEqual(identity.pvc_names, ("data-atlas-db-2", "wal-atlas-db-2"))
        self.assertEqual(identity.dns_name, "atlas-db-2.atlas-db.atlas-system.svc.cluster.local")

    def test_ordered_update_descends(self):
        planner = StatefulSetPlanner("db", "ns", "db", ("data",))
        self.assertEqual(planner.ordered_update(4, partition=1), (3, 2, 1))

    def test_fencing_rejects_stale_writer(self):
        registry = FenceRegistry()
        old = registry.acquire("db")
        new = registry.acquire("db")
        registry.write("db", new, "x", "new")
        with self.assertRaises(PermissionError):
            registry.write("db", old, "x", "old")
        self.assertEqual(registry.read("db", "x"), "new")

    def test_durable_ledger_persists_and_fences(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = FenceRegistry()
            first = registry.acquire("db")
            ledger = DurableLedger(directory)
            ledger.commit(first, "sentinel", "one")
            second = registry.acquire("db")
            ledger.commit(second, "sentinel", "two")
            with self.assertRaises(PermissionError):
                ledger.commit(first, "sentinel", "stale")
            reopened = DurableLedger(directory)
            self.assertEqual(reopened.read("sentinel"), "two")
            self.assertEqual(reopened.generation(), 2)


if __name__ == "__main__":
    unittest.main()
