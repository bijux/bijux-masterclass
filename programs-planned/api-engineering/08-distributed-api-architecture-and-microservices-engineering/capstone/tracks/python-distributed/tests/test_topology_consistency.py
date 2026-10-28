import unittest
from distributed_api.consistency import VersionedProjection
from distributed_api.model import ValidationError
from distributed_api.topology import (
    DependencyGraph,
    SyncEdge,
    parallel_latency_ms,
    serial_availability,
    serial_latency_ms,
)


class TopologyConsistencyTests(unittest.TestCase):
    def test_acyclic_graph_and_depth(self):
        graph = DependencyGraph([
            SyncEdge("edge-gateway","analysis-control","query",700),
            SyncEdge("analysis-control","artifact-service","lookup",300),
        ])
        self.assertIsNone(graph.cycle())
        self.assertEqual(graph.longest_depth("edge-gateway"), 2)
        graph.validate(max_public_depth=2, forbidden=set())

    def test_cycle_is_rejected(self):
        graph = DependencyGraph([
            SyncEdge("control","artifact","x",100),
            SyncEdge("artifact","control","y",100),
        ])
        self.assertIsNotNone(graph.cycle())
        with self.assertRaises(ValidationError): graph.validate(max_public_depth=2, forbidden=set())

    def test_serial_availability_compounds(self):
        self.assertAlmostEqual(serial_availability([0.99,0.99,0.99]), 0.970299)
        self.assertEqual(serial_latency_ms([10,20,30]), 60)
        self.assertEqual(parallel_latency_ms([10,20,30]), 30)

    def test_projection_classifies_versions(self):
        p = VersionedProjection()
        self.assertEqual(p.apply("r",1,{"state":"queued"},now_ms=0), "apply")
        self.assertEqual(p.apply("r",1,{"state":"queued"},now_ms=1), "duplicate")
        self.assertEqual(p.apply("r",2,{"state":"running"},now_ms=2), "apply")
        self.assertEqual(p.apply("r",1,{"state":"bad"},now_ms=3), "stale")
        self.assertEqual(p.apply("r",4,{"state":"complete"},now_ms=4), "gap")

    def test_projection_rejects_stale_read(self):
        p = VersionedProjection(); p.apply("r",1,1,now_ms=0)
        with self.assertRaises(ValidationError): p.get("r",now_ms=100,max_staleness_ms=10)


if __name__ == "__main__": unittest.main()
