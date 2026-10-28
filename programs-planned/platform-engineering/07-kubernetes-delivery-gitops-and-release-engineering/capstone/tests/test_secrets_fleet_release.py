import json
import tempfile
import unittest
from pathlib import Path
from atlas_delivery.fleet import ClusterProfile, ReleaseRequirements, compatible, generate_targets, promotion_waves
from atlas_delivery.models import ArtifactSet, DesiredRevision, EvidenceGate, ReleaseCandidate
from atlas_delivery.release import classify_release
from atlas_delivery.secrets import scan_repository, secret_version_event

class SecurityFleetReleaseTests(unittest.TestCase):
    def test_plaintext_secret_detected(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'bad.yaml').write_text('apiVersion: v1\nkind: Secret\nmetadata: {name: bad}\nstringData:\n  password: hunter2\n')
            self.assertTrue(scan_repository(d))
    def test_encrypted_sops_fixture_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'safe.enc.yaml').write_text('apiVersion: v1\nkind: Secret\nmetadata: {name: safe}\nstringData:\n  password: ENC[AES256_GCM,data:x]\n')
            self.assertFalse(scan_repository(d))
    def test_course_capstone_has_no_plaintext_secret_findings(self):
        root=Path(__file__).resolve().parents[1]
        self.assertEqual(scan_repository(root),[])
    def test_secret_adoption_event(self):
        self.assertEqual(secret_version_event('db','v2',True,False)['version'],'v2')
    def cluster(self,version='1.36.2',caps=frozenset({'gateway'}),controller='argocd-3.5.0',lifecycle='active'):
        return ClusterProfile('c','o','prod','r','multi-zone',version,controller,caps,lifecycle)
    def test_compatible_cluster(self):
        ok,reasons=compatible(self.cluster(),ReleaseRequirements(36,frozenset({'gateway'}),'argocd-'))
        self.assertTrue(ok); self.assertFalse(reasons)
    def test_incompatible_cluster(self):
        ok,reasons=compatible(self.cluster(version='1.35.7',caps=frozenset()),ReleaseRequirements(36,frozenset({'gateway'}),'argocd-'))
        self.assertFalse(ok); self.assertGreaterEqual(len(reasons),2)
    def test_unavailable_catalogue_not_empty_targets(self):
        self.assertIsNone(generate_targets([self.cluster()],'prod',source_available=False))
    def test_lifecycle_filter(self):
        self.assertEqual(generate_targets([self.cluster(lifecycle='retired')],'prod'),[])
    def test_promotion_waves_diverse_first(self):
        a=self.cluster(); b=ClusterProfile('d','o','prod','r2','single-zone','1.36.2','argocd-3.5.0',frozenset({'gateway'}))
        waves=promotion_waves([a,b]); self.assertEqual(len(waves),2)
    def candidate(self,gates,protected=(),approvals=()):
        rev=DesiredRevision('r','prod','c'*40,'kustomize','5.8.1','sha256:'+'d'*64,ArtifactSet(('sha256:'+'a'*64,),None),'p')
        return ReleaseCandidate(rev,list(gates),list(approvals),list(protected))
    def test_release_accepted(self):
        self.assertEqual(classify_release(self.candidate([EvidenceGate('g','pass','s','ok')]))[0],'accepted')
    def test_release_rejected(self):
        self.assertEqual(classify_release(self.candidate([EvidenceGate('g','fail','s','bad')]))[0],'rejected')
    def test_release_review_required(self):
        self.assertEqual(classify_release(self.candidate([EvidenceGate('g','review','s','human')]))[0],'review-required')
    def test_release_review_approved(self):
        self.assertEqual(classify_release(self.candidate([EvidenceGate('g','review','s','human')],approvals=['owner']))[0],'accepted')
    def test_release_not_executed(self):
        self.assertEqual(classify_release(self.candidate([EvidenceGate('g','not-executed','s','absent')]))[0],'not-executed')
    def test_protected_deletion_rejected(self):
        self.assertEqual(classify_release(self.candidate([],protected=['pvc']))[0],'rejected')

if __name__=='__main__': unittest.main()
