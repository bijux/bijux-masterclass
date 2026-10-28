#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, sys
from common import CAPSTONE, passed
sys.path.insert(0,str(CAPSTONE))
from atlas_kube.api_store import ApiStore, NotFound
from atlas_kube.models import KubeObject, ObjectMeta
from atlas_kube.controller import AtlasController, ReleaseReservationStore
from atlas_kube.rollout import rollout_bounds
from atlas_kube.scheduler import Node, PodRequest, Taint, schedule
from atlas_kube.handoff import verify_manifest

API="platform/atlas-api@sha256:6e3b38e88f6ef4252b635b6d199095db46233d7b6f85f3be4384d746386317a7"
WORKER="platform/atlas-worker@sha256:bbd52b30969ebb6fb3568d2ce5c1ebfb420c7bd7a80001f2a1014feaa4d7a036"
store=ApiStore(); reservations=ReleaseReservationStore(set()); controller=AtlasController(store,reservations)
cr=KubeObject("platform.bijux.dev/v1alpha1","AtlasWorkload",ObjectMeta("atlas","atlas-system"),spec={"apiImage":API,"workerImage":WORKER,"apiReplicas":3,"workerReplicas":1,"configurationRef":"atlas-config"})
cr=store.create(cr,"atlas-author")
first_writes=controller.reconcile(cr)
children=store.list(kind="Deployment")
assert len(children)==2
# Controller stops: desired state and children remain; no hidden process advances state.
stopped_revision=store.revision
assert store.get(*cr.key).spec["apiReplicas"]==3 and store.revision==stopped_revision
# Restart/reconcile is idempotent.
second_writes=controller.reconcile(store.get(*cr.key))
assert second_writes==0 and len(store.list(kind="Pod"))==4
# Kubelet observations make Pods ready; native controllers and Atlas controller converge.
for pod in store.list(kind="Pod"):
    pod.status={"phase":"Running","conditions":[{"type":"Ready","status":"True"}]}
    store.replace(pod,pod.metadata.resource_version,"kubelet",status_only=True)
for dep in store.list(kind="Deployment"):
    controller.deployment_controller.reconcile(dep)
controller.reconcile(store.get(*cr.key))
ready=store.get(*cr.key).status["conditions"][0]["status"]
assert ready=="True"
# Rollout and scheduling evidence.
bounds=rollout_bounds(3,1,0)
nodes=[Node("n1",2000,2048,{"pool":"general"}),Node("n2",2000,2048,{"pool":"general"}),Node("n3",4000,4096,{"pool":"batch"},[Taint("dedicated","batch")])]
selected,decisions=schedule(nodes,PodRequest("atlas-api-new",1500,64,{"pool":"general"},prohibited_hostnames={"n1","n2"}))
assert selected is None
# Finalizer remains during denied cleanup, then completes exactly once.
store.delete(store.get(*cr.key)); reservations.deny_cleanup=True
controller.reconcile(store.get(*cr.key)); assert store.get(*cr.key).metadata.deletion_timestamp
reservations.deny_cleanup=False; controller.reconcile(store.get(*cr.key))
try: store.get(*cr.key)
except NotFound: pass
else: raise AssertionError("custom resource deletion did not complete")
assert not reservations.reservations
assert verify_manifest(CAPSTONE/"handoff")==[]
report={
  "initialReconcileWrites":first_writes,
  "steadyStateWrites":second_writes,
  "childDeployments":[d.metadata.name for d in children],
  "childPodCount":4,
  "readyCondition":ready,
  "rollout":{"maxTotal":bounds.max_total,"minAvailable":bounds.min_available},
  "scheduling":{"selected":selected,"reasons":{d.node:list(d.reasons) for d in decisions}},
  "cleanup":"completed-after-denied-attempt",
  "handoff":"verified",
}
(CAPSTONE/"reports").mkdir(exist_ok=True)
(CAPSTONE/"reports"/"capstone-tour.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
passed("Atlas Kubernetes Runtime capstone tour — 9 checks")
print(json.dumps(report,indent=2,sort_keys=True))
