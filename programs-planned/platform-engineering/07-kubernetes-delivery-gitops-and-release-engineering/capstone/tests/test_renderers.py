import json
import unittest
from pathlib import Path
from atlas_delivery.canonical import identity_string, render_digest
from atlas_delivery.helm_model import ValuesError, render_atlas, validate_values
from atlas_delivery.kustomize_model import build

ROOT=Path(__file__).resolve().parents[1]

class RendererTests(unittest.TestCase):
    def test_kustomize_prod(self):
        resources=build(ROOT/'repository/apps/atlas/overlays/prod')
        identities={identity_string(x) for x in resources}
        self.assertIn('apps/Deployment/atlas-prod/atlas-api-prod',identities)
        api=next(x for x in resources if x.get('kind')=='Deployment' and x['metadata']['name']=='atlas-api-prod')
        self.assertEqual(api['spec']['replicas'],3)
        self.assertTrue(api['spec']['template']['spec']['containers'][0]['image'].endswith('@sha256:'+'a'*64))
        self.assertEqual(api['spec']['template']['spec']['serviceAccountName'],'atlas-api-prod')
        config=next(x for x in resources if x.get('kind')=='ConfigMap')
        self.assertEqual(config['data']['DATA_RELEASE_PHASE'],'writer-cutover')
    def test_kustomize_environment_digests_differ(self):
        dev=render_digest(build(ROOT/'repository/apps/atlas/overlays/dev'))
        prod=render_digest(build(ROOT/'repository/apps/atlas/overlays/prod'))
        self.assertNotEqual(dev,prod)
    def test_kustomize_deterministic(self):
        path=ROOT/'repository/apps/atlas/overlays/staging'
        self.assertEqual(render_digest(build(path)),render_digest(build(path)))
    def test_helm_schema(self):
        schema=json.loads((ROOT/'repository/charts/atlas/values.schema.json').read_text())
        values={'namespace':'atlas','replicas':2,'image':{'repository':'r','digest':'sha256:'+'a'*64},'resources':{},'service':{},'security':{}}
        validate_values(schema,values)
    def test_helm_schema_rejects_mutable_tag(self):
        schema=json.loads((ROOT/'repository/charts/atlas/values.schema.json').read_text())
        values={'namespace':'atlas','replicas':2,'image':{'repository':'r','digest':'latest'},'resources':{},'service':{},'security':{}}
        with self.assertRaises(ValuesError): validate_values(schema,values)
    def test_helm_schema_rejects_unknown(self):
        schema=json.loads((ROOT/'repository/charts/atlas/values.schema.json').read_text())
        values={'namespace':'atlas','replicas':2,'image':{'repository':'r','digest':'sha256:'+'a'*64},'resources':{},'service':{},'security':{},'mystery':1}
        with self.assertRaises(ValuesError): validate_values(schema,values)
    def test_helm_semantic_render(self):
        values={'namespace':'atlas','replicas':2,'image':{'repository':'r','digest':'sha256:'+'a'*64},'resources':{'requests':{}},'service':{},'security':{}}
        resources=render_atlas(values)
        self.assertEqual({r['kind'] for r in resources},{'Deployment','Service'})
        self.assertIn('@sha256:',resources[0]['spec']['template']['spec']['containers'][0]['image'])

if __name__=='__main__': unittest.main()
