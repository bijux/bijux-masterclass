import unittest
from atlas_delivery.models import ArtifactSet, DesiredRevision, EvidenceGate, MetricObservation, SegmentObservation
from atlas_delivery.progressive import Canary, evaluate_analysis
from atlas_delivery.promotion import evaluate_promotion

class ProgressivePromotionTests(unittest.TestCase):
    def metric(self, candidate=0.01, stable=0.01, samples=1000):
        return MetricObservation('error',samples,samples,candidate,stable,0.02,0.005)
    def test_pass(self):
        result=evaluate_analysis([self.metric()], [SegmentObservation('tenant-a',100,0,0.01)], 50)
        self.assertEqual(result.decision,'pass')
    def test_absolute_failure_dominates_incomplete_other_metric(self):
        result=evaluate_analysis([self.metric(candidate=.2), MetricObservation('late',0,0,None,None,.1,.1)], [], 50)
        self.assertEqual(result.decision,'fail')
    def test_missing_required_metric_unavailable(self):
        m=MetricObservation('missing',0,0,None,None,.1,.1)
        self.assertEqual(evaluate_analysis([m],[],50).decision,'unavailable')
    def test_insufficient_samples_inconclusive(self):
        self.assertEqual(evaluate_analysis([self.metric(samples=3)],[],50).decision,'inconclusive')
    def test_segment_failure(self):
        r=evaluate_analysis([self.metric()],[SegmentObservation('tenant-a',100,10,.01)],50)
        self.assertEqual(r.decision,'fail')
    def test_canary_state(self):
        c=Canary('stable','candidate'); c.expose(5,100); c.complete(evaluate_analysis([self.metric()],[],50))
        self.assertEqual((c.state,c.configured_weight),('Promoted',100))
    def revision(self,name,artifacts):
        return DesiredRevision(name,'prod','c'*40,'kustomize','5.8.1','sha256:'+'d'*64,artifacts,'previous')
    def test_promotion_same_artifacts(self):
        a=ArtifactSet(('sha256:'+'a'*64,), 'sha256:'+'b'*64)
        gate=EvidenceGate('proof','pass','s','ok')
        self.assertTrue(evaluate_promotion(self.revision('stage',a),self.revision('prod',a),[gate]).accepted)
    def test_promotion_rebuild_rejected(self):
        a=ArtifactSet(('sha256:'+'a'*64,),None); b=ArtifactSet(('sha256:'+'b'*64,),None)
        self.assertFalse(evaluate_promotion(self.revision('stage',a),self.revision('prod',b),[]).accepted)
    def test_blocker_gate_rejected(self):
        a=ArtifactSet(('sha256:'+'a'*64,),None)
        gate=EvidenceGate('restore','not-executed','s','no cluster')
        self.assertFalse(evaluate_promotion(self.revision('stage',a),self.revision('prod',a),[gate]).accepted)

if __name__=='__main__': unittest.main()
