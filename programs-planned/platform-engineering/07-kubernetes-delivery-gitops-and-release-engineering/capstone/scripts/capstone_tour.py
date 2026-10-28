#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from atlas_delivery.canonical import identity_string, render_digest
from atlas_delivery.fleet import ClusterProfile, ReleaseRequirements, compatible, generate_targets
from atlas_delivery.health import assess
from atlas_delivery.inventory import Inventory
from atlas_delivery.kustomize_model import build
from atlas_delivery.models import ArtifactSet, DesiredRevision, EvidenceGate, MetricObservation, SegmentObservation
from atlas_delivery.progressive import evaluate_analysis
from atlas_delivery.promotion import evaluate_promotion
from atlas_delivery.reconcile import ClusterState, Reconciler

ROOT=Path(__file__).resolve().parents[1]
report={'checks':[]}
def check(name,condition,details):
    if not condition: raise SystemExit(f"FAIL {name}: {details}")
    report['checks'].append({'name':name,'status':'pass','details':details})

prod=build(ROOT/'repository/apps/atlas/overlays/prod')
digest=render_digest(prod)
check('deterministic-render',digest==render_digest(build(ROOT/'repository/apps/atlas/overlays/prod')),digest)
check('immutable-workloads',all('@sha256:' in c['image'] for r in prod for c in r.get('spec',{}).get('template',{}).get('spec',{}).get('containers',[])),'all rendered workload images use digests')

cluster=ClusterState(); inv=Inventory('atlas-prod')
inv,initial=Reconciler().reconcile(cluster,prod,inv,'3'*40)
check('initial-convergence',initial.writes==len(prod),f"created {initial.writes} resources")
inv,steady=Reconciler().reconcile(cluster,prod,inv,'3'*40)
check('no-op-steady-state',steady.writes==0,'second reconciliation performed no writes')

api_id=next(identity_string(r) for r in prod if r.get('kind')=='Deployment' and r['metadata']['name']=='atlas-api-prod')
cluster.objects[api_id].resource['spec']['replicas']=9
cluster.objects[api_id].resource['spec']['template']['spec']['containers'][0]['image']='registry.invalid/manual@sha256:'+'9'*64
cluster.objects[api_id].external_paths={'/spec/replicas'}
inv,drift=Reconciler().reconcile(cluster,prod,inv,'3'*40)
api=cluster.get(api_id)
check('field-ownership',api['spec']['replicas']==9 and api['spec']['template']['spec']['containers'][0]['image'].endswith('a'*64),'external replicas preserved; owned image repaired')

pvc={'apiVersion':'v1','kind':'PersistentVolumeClaim','metadata':{'name':'atlas-artifacts','namespace':'atlas-prod','annotations':{'delivery.atlas.dev/prune-protected':'true'}},'spec':{}}
cluster.put(pvc); inv.identities.add(identity_string(pvc))
inv,prune=Reconciler().reconcile(cluster,prod,inv,'4'*40)
check('protected-prune',identity_string(pvc) in prune.blocked_prune,'ordinary reconciliation blocked data deletion')

before=len(cluster.objects)
_,source_failure=Reconciler().reconcile(cluster,[],inv,'5'*40,source_available=False)
check('source-outage',len(cluster.objects)==before and source_failure.writes==0,'unavailable source did not become empty desired state')

metrics=[MetricObservation('error-rate',1000,1000,.004,.003,.01,.003)]
segments=[SegmentObservation('large-artifacts',250,0,.01)]
analysis=evaluate_analysis(metrics,segments,100)
check('progressive-analysis',analysis.decision=='pass',analysis.reasons)
inconclusive=evaluate_analysis([MetricObservation('error-rate',2,2,0,0,.01,.003)],[],100)
check('sample-guard',inconclusive.decision=='inconclusive',inconclusive.reasons)

artifacts=ArtifactSet(('sha256:'+'a'*64,'sha256:'+'b'*64),'sha256:'+'e'*64,'sha256:'+'f'*64)
stage=DesiredRevision('stage','staging','2'*40,'kustomize','5.8.1',digest,artifacts,'dev')
prodrev=DesiredRevision('prod','prod','3'*40,'kustomize','5.8.1',digest,artifacts,'stage')
promotion=evaluate_promotion(stage,prodrev,[EvidenceGate('restore','pass','atlas','verified')])
check('artifact-promotion',promotion.accepted,promotion.reason)

profile=ClusterProfile('atlas-prod-eu1','platform-prod','prod','eu-north-1','multi-zone','1.36.2','argocd-3.5.0',frozenset({'gateway-api-v1','external-secrets-v1','argo-rollouts-v1alpha1'}))
ok,reasons=compatible(profile,ReleaseRequirements(36,frozenset({'gateway-api-v1','argo-rollouts-v1alpha1'}),'argocd-'))
check('fleet-compatibility',ok,reasons)
check('catalogue-outage',generate_targets([profile],'prod',source_available=False) is None,'unknown target set preserved as unknown')

healthy={'kind':'Deployment','metadata':{'generation':3},'spec':{'replicas':3},'status':{'observedGeneration':3,'availableReplicas':3}}
check('resource-health',assess(healthy).status=='Healthy','current generation and availability observed')

out=ROOT/'reports/runtime';out.mkdir(parents=True,exist_ok=True)
(out/'capstone-tour.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(f"PASS Atlas Delivery Plane tour — {len(report['checks'])} checks")
