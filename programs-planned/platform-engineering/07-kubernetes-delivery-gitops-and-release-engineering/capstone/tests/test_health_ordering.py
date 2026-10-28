import unittest
from atlas_delivery.health import assess
from atlas_delivery.ordering import ordered

class HealthOrderingTests(unittest.TestCase):
    def test_deployment_healthy(self):
        r={'kind':'Deployment','metadata':{'generation':2},'spec':{'replicas':3},'status':{'observedGeneration':2,'availableReplicas':3}}
        self.assertEqual(assess(r).status,'Healthy')
    def test_stale_generation_progressing(self):
        r={'kind':'Deployment','metadata':{'generation':2},'spec':{'replicas':3},'status':{'observedGeneration':1,'availableReplicas':3}}
        self.assertEqual(assess(r).status,'Progressing')
    def test_progress_deadline_degraded(self):
        r={'kind':'Deployment','spec':{'replicas':3},'status':{'availableReplicas':1,'conditions':[{'type':'Progressing','status':'False','reason':'ProgressDeadlineExceeded'}]}}
        self.assertEqual(assess(r).status,'Degraded')
    def test_unknown_is_honest(self):
        self.assertEqual(assess({'kind':'Mystery'}).status,'Unknown')
    def obj(self,name,wave='0',deps=''):
        a={'argocd.argoproj.io/sync-wave':wave}
        if deps:a['delivery.atlas.dev/depends-on']=deps
        return {'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':name,'namespace':'n','annotations':a}}
    def test_ordering_respects_dependency_and_wave(self):
        a=self.obj('a','0'); b=self.obj('b','-1'); c=self.obj('c','-10','core/ConfigMap/n/a')
        names=[x['metadata']['name'] for x in ordered([c,a,b])]
        self.assertEqual(names,['b','a','c'])
    def test_missing_dependency_rejected(self):
        with self.assertRaises(ValueError): ordered([self.obj('a','0','core/ConfigMap/n/missing')])
    def test_cycle_rejected(self):
        a=self.obj('a','0','core/ConfigMap/n/b'); b=self.obj('b','0','core/ConfigMap/n/a')
        with self.assertRaises(ValueError): ordered([a,b])

if __name__=='__main__': unittest.main()
