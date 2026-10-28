import pytest
from atlas_kube.api_store import ApiStore, NotFound
from atlas_kube.models import KubeObject, ObjectMeta
from atlas_kube.controllers import DeploymentController
from atlas_kube.controller import AtlasController, ReleaseReservationStore, FINALIZER

API="platform/atlas-api@sha256:"+"a"*64
WORKER="platform/atlas-worker@sha256:"+"b"*64


def deployment():
    labels={"app":"api"}
    return KubeObject("apps/v1","Deployment",ObjectMeta("api","atlas",labels=labels),
        spec={"replicas":2,"selector":{"matchLabels":labels},"template":{"metadata":{"labels":labels},"spec":{"containers":[]}}})


def atlas():
    return KubeObject("platform.bijux.dev/v1alpha1","AtlasWorkload",ObjectMeta("atlas","atlas-system"),
        spec={"apiImage":API,"workerImage":WORKER,"apiReplicas":3,"workerReplicas":1,"configurationRef":"atlas-config"})


def mark_pods_ready(store):
    for pod in store.list(api_version="v1",kind="Pod"):
        pod.status={"phase":"Running","conditions":[{"type":"Ready","status":"True"}]}
        store.replace(pod,pod.metadata.resource_version,"kubelet",status_only=True)


def test_deployment_reconcile_idempotent():
    store=ApiStore(); dep=store.create(deployment())
    ctrl=DeploymentController(store); ctrl.reconcile(dep)
    writes=len(store.writes); ctrl.reconcile(store.get(*dep.key))
    assert len(store.list(kind="Pod"))==2
    assert len(store.writes)==writes


def test_deployment_scale():
    store=ApiStore(); dep=store.create(deployment()); ctrl=DeploymentController(store); ctrl.reconcile(dep)
    dep=store.get(*dep.key); dep.spec["replicas"]=3; dep=store.replace(dep,dep.metadata.resource_version)
    ctrl.reconcile(dep); assert len(store.list(kind="Pod"))==3


def test_atlas_controller_creates_two_deployments():
    store=ApiStore(); cr=store.create(atlas(),"author")
    ctrl=AtlasController(store); ctrl.reconcile(cr)
    assert {d.metadata.name for d in store.list(kind="Deployment")}=={"atlas-api","atlas-worker"}
    assert FINALIZER in store.get(*cr.key).metadata.finalizers


def test_atlas_controller_steady_state_no_writes():
    store=ApiStore(); cr=store.create(atlas(),"author"); ctrl=AtlasController(store)
    ctrl.reconcile(cr); writes=len(store.writes)
    ctrl.reconcile(store.get(*cr.key))
    assert len(store.writes)==writes


def test_atlas_status_becomes_ready_after_pods_ready():
    store=ApiStore(); cr=store.create(atlas(),"author"); ctrl=AtlasController(store)
    ctrl.reconcile(cr); mark_pods_ready(store)
    for dep in store.list(kind="Deployment"): ctrl.deployment_controller.reconcile(dep)
    ctrl.reconcile(store.get(*cr.key))
    condition=store.get(*cr.key).status["conditions"][0]
    assert condition["status"]=="True"


def test_status_churn_defect_detectable():
    store=ApiStore(); cr=store.create(atlas(),"author"); ctrl=AtlasController(store)
    ctrl.reconcile(cr); before=len(store.writes)
    for _ in range(3): ctrl.reconcile(store.get(*cr.key),churn_status=True)
    assert len(store.writes)-before==3


def test_finalizer_cleanup_denied_then_succeeds():
    store=ApiStore(); cr=store.create(atlas(),"author")
    reservations=ReleaseReservationStore(set()); ctrl=AtlasController(store,reservations)
    ctrl.reconcile(cr); cr=store.get(*cr.key); store.delete(cr); cr=store.get(*cr.key)
    reservations.deny_cleanup=True; ctrl.reconcile(cr)
    assert store.get(*cr.key).metadata.deletion_timestamp
    reservations.deny_cleanup=False; ctrl.reconcile(store.get(*cr.key))
    with pytest.raises(NotFound): store.get(*cr.key)
    assert not reservations.reservations
