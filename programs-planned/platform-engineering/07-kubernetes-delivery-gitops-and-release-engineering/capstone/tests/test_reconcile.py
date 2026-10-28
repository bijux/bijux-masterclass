import unittest
from atlas_delivery.canonical import identity_string
from atlas_delivery.inventory import Inventory, is_protected
from atlas_delivery.reconcile import ClusterState, Reconciler

class ReconcileTests(unittest.TestCase):
    def cm(self,name='a',value='1'):
        return {'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':name,'namespace':'n'},'data':{'x':value}}
    def deployment(self,replicas=2,image='r@sha256:'+'a'*64):
        return {'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':'api','namespace':'n'},'spec':{'replicas':replicas,'template':{'spec':{'containers':[{'name':'api','image':image}]}}}}
    def test_create_and_noop(self):
        cluster=ClusterState(); inv=Inventory('a')
        inv,r=Reconciler().reconcile(cluster,[self.cm()],inv,'c1')
        self.assertEqual(r.writes,1)
        inv,r=Reconciler().reconcile(cluster,[self.cm()],inv,'c1')
        self.assertEqual(r.writes,0)
    def test_repair_owned_drift(self):
        cluster=ClusterState(); inv=Inventory('a')
        inv,_=Reconciler().reconcile(cluster,[self.cm(value='1')],inv,'c1')
        cluster.objects[identity_string(self.cm())].resource['data']['x']='manual'
        inv,r=Reconciler().reconcile(cluster,[self.cm(value='1')],inv,'c1')
        self.assertEqual(r.updated,['core/ConfigMap/n/a'])
        self.assertEqual(cluster.get('core/ConfigMap/n/a')['data']['x'],'1')
    def test_preserve_external_field_but_repair_owned_field(self):
        desired=self.deployment(replicas=2,image='r@sha256:'+'b'*64)
        live=self.deployment(replicas=7,image='r@sha256:'+'a'*64)
        cluster=ClusterState(); cluster.put(live,external_paths={'/spec/replicas'})
        inv=Inventory.from_resources('a',[live])
        inv,r=Reconciler().reconcile(cluster,[desired],inv,'c2')
        result=cluster.get('apps/Deployment/n/api')
        self.assertEqual(result['spec']['replicas'],7)
        self.assertTrue(result['spec']['template']['spec']['containers'][0]['image'].endswith('b'*64))
        self.assertIn('apps/Deployment/n/api',r.preserved_external)
    def test_source_unavailable_is_not_empty_desired_set(self):
        cluster=ClusterState(); inv=Inventory('a')
        inv,_=Reconciler().reconcile(cluster,[self.cm()],inv,'c1')
        next_inv,r=Reconciler().reconcile(cluster,[],inv,'c2',source_available=False)
        self.assertEqual(next_inv.identities,inv.identities)
        self.assertEqual(len(cluster.objects),1)
        self.assertEqual(r.writes,0)
    def test_suspension_preserves_live_state(self):
        cluster=ClusterState(); inv=Inventory('a')
        inv,_=Reconciler().reconcile(cluster,[self.cm()],inv,'c1')
        _,r=Reconciler().reconcile(cluster,[],inv,'c2',suspended=True)
        self.assertEqual(r.writes,0)
    def test_unprotected_prune(self):
        cluster=ClusterState(); cm=self.cm(); cluster.put(cm); inv=Inventory.from_resources('a',[cm])
        next_inv,r=Reconciler().reconcile(cluster,[],inv,'c2')
        self.assertEqual(r.deleted,['core/ConfigMap/n/a']); self.assertFalse(next_inv.identities)
    def test_protected_prune_blocked(self):
        pvc={'apiVersion':'v1','kind':'PersistentVolumeClaim','metadata':{'name':'data','namespace':'n'}}
        cluster=ClusterState(); cluster.put(pvc); inv=Inventory.from_resources('a',[pvc])
        next_inv,r=Reconciler().reconcile(cluster,[],inv,'c2')
        self.assertEqual(r.blocked_prune,['core/PersistentVolumeClaim/n/data'])
        self.assertIn('core/PersistentVolumeClaim/n/data',next_inv.identities)
    def test_annotation_protects_arbitrary_kind(self):
        cm=self.cm(); cm['metadata']['annotations']={'delivery.atlas.dev/prune-protected':'true'}
        self.assertTrue(is_protected(cm))

if __name__=='__main__': unittest.main()
