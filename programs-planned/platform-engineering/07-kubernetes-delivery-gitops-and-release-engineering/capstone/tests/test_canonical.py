import tempfile
import unittest
from pathlib import Path
from atlas_delivery.canonical import (
    DuplicateKeyError, canonical_resource, identity_string,
    load_yaml_documents, render_digest, resource_identity,
)

class CanonicalTests(unittest.TestCase):
    def resource(self, name='x'):
        return {'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':name,'namespace':'n'},'data':{'x':'1'}}
    def test_identity(self):
        self.assertEqual(resource_identity(self.resource()), ('','ConfigMap','n','x'))
        self.assertEqual(identity_string(self.resource()), 'core/ConfigMap/n/x')
    def test_status_and_server_metadata_do_not_change_digest(self):
        a=self.resource(); b=self.resource(); b['status']={'x':'server'}; b['metadata']['uid']='u'; b['metadata']['resourceVersion']='3'
        self.assertEqual(render_digest([a]), render_digest([b]))
    def test_order_does_not_change_set_digest(self):
        a=self.resource('a'); b=self.resource('b')
        self.assertEqual(render_digest([a,b]), render_digest([b,a]))
    def test_duplicate_identity_rejected(self):
        with self.assertRaises(ValueError): render_digest([self.resource(),self.resource()])
    def test_scalar_type_changes_digest(self):
        a=self.resource(); b=self.resource(); a['data']['x']='1'; b['data']['x']=1
        self.assertNotEqual(render_digest([a]),render_digest([b]))
    def test_duplicate_yaml_key_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.yaml'; p.write_text('apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: a\n  name: b\n')
            with self.assertRaises(DuplicateKeyError): load_yaml_documents(p)
    def test_non_mapping_document_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.yaml'; p.write_text('- one\n- two\n')
            with self.assertRaises(ValueError): load_yaml_documents(p)
    def test_canonical_bytes_stable(self):
        self.assertEqual(canonical_resource(self.resource()), canonical_resource(self.resource()))

if __name__=='__main__': unittest.main()
