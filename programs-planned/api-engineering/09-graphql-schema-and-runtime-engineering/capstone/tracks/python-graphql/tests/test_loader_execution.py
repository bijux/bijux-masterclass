import unittest
from graph_api.execution import GraphError, TypeRef, complete_object
from graph_api.loader import BatchLoader

class LoaderExecutionTests(unittest.TestCase):
    def test_loader_collapses_duplicate_keys(self):
        calls=[]
        def batch(keys): calls.append(list(keys)); return {key:key.upper() for key in keys}
        loader=BatchLoader(batch); a=loader.load("run-1"); b=loader.load("run-1"); c=loader.load("run-2"); loader.dispatch()
        self.assertIs(a,b); self.assertEqual(a.get(),"RUN-1"); self.assertEqual(c.get(),"RUN-2"); self.assertEqual(calls,[["run-1","run-2"]])
    def test_request_scoped_cache_does_not_cross_requests(self):
        calls=[]
        for _ in range(2):
            loader=BatchLoader(lambda keys:(calls.append(keys) or {key:key for key in keys})); loader.load("x"); loader.dispatch()
        self.assertEqual(len(calls),2)
    def test_nullable_failure_stays_at_field(self):
        error=GraphError("down",("run","artifacts"),"DOWNSTREAM_UNAVAILABLE")
        result=complete_object({"id":("1",TypeRef("ID",True),None),"artifacts":(None,TypeRef("ArtifactList",False),error)},path=("run",))
        self.assertFalse(result.bubbled); self.assertIsNone(result.value["artifacts"]); self.assertEqual(len(result.errors),1)
    def test_non_null_failure_bubbles(self):
        result=complete_object({"analysisRuns":(None,TypeRef("Connection",True),GraphError("down",("project","analysisRuns"),"DOWNSTREAM_UNAVAILABLE"))},path=("project",))
        self.assertTrue(result.bubbled); self.assertIsNone(result.value)
