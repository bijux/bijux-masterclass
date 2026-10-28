import unittest
from graph_api.compatibility import SchemaChange, classify
from graph_api.model import AuthorizationError, Principal, ValidationError
from graph_api.policy import require_field
from graph_api.release import ReleaseEvidence, decide
from graph_api.subscription import ResumableSubscription, SubscriptionEvent
from graph_api.transport import HttpRequest, evaluate

class PolicySubscriptionReleaseTests(unittest.TestCase):
    def test_field_permission_and_tenant(self):
        p=Principal("u","tenant-a",frozenset({"ARTIFACT_READ"})); require_field(p,"AnalysisRun.artifacts",resource_tenant="tenant-a")
        with self.assertRaises(AuthorizationError): require_field(p,"AnalysisRun.artifacts",resource_tenant="tenant-b")
    def test_subscription_duplicate_suppression(self):
        values=[SubscriptionEvent(4,{}),SubscriptionEvent(4,{}),SubscriptionEvent(5,{})]; out=ResumableSubscription().resume(values,after=3); self.assertEqual([e.sequence for e in out],[4,5])
    def test_subscription_gap_rejected(self):
        with self.assertRaises(ValidationError): ResumableSubscription().resume([SubscriptionEvent(5,{})],after=3)
    def test_compatibility_classification(self):
        self.assertEqual(classify(SchemaChange("remove-field","AnalysisRun.status",True)).classification,"breaking"); self.assertEqual(classify(SchemaChange("add-enum-value","RunStatus.PAUSED")).classification,"review-required")
    def test_release_rejects_breaking_change(self):
        evidence=ReleaseEvidence((classify(SchemaChange("remove-field","x")),),True,True,True,True); self.assertFalse(decide(evidence).accepted)
    def test_http_profile(self):
        self.assertTrue(evaluate(HttpRequest("POST","application/graphql-response+json","application/json","query")).accepted); self.assertEqual(evaluate(HttpRequest("GET","application/graphql-response+json",None,"mutation")).status,405)
