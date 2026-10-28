import pytest
from atlas_kube.api_store import ApiStore, ApplyConflict, VersionConflict, NotFound
from atlas_kube.models import KubeObject, ObjectMeta


def obj():
    return KubeObject("apps/v1", "Deployment", ObjectMeta("api", "atlas"),
                      spec={"replicas": 3, "template": {"image": "digest"}})


def test_create_get_clone():
    store = ApiStore(); created = store.create(obj(), "author")
    copy = store.get(*created.key); copy.spec["replicas"] = 9
    assert store.get(*created.key).spec["replicas"] == 3


def test_duplicate_create_fails():
    store = ApiStore(); store.create(obj())
    with pytest.raises(Exception): store.create(obj())


def test_resource_version_conflict():
    store=ApiStore(); created=store.create(obj())
    changed=created.clone(); changed.spec["replicas"]=4
    store.replace(changed, created.metadata.resource_version)
    with pytest.raises(VersionConflict): store.replace(changed, created.metadata.resource_version)


def test_spec_change_increments_generation():
    store=ApiStore(); created=store.create(obj())
    changed=created.clone(); changed.spec["replicas"]=4
    updated=store.replace(changed, created.metadata.resource_version)
    assert updated.metadata.generation == created.metadata.generation + 1


def test_status_change_does_not_increment_generation():
    store=ApiStore(); created=store.create(obj())
    updated=store.update_status(created, {"ready": 1})
    assert updated.metadata.generation == created.metadata.generation


def test_apply_conflict_and_force_transfer():
    store=ApiStore(); created=store.create(obj())
    created.metadata.managed_fields={"author":{"spec.replicas"}}
    created=store.replace(created, created.metadata.resource_version)
    with pytest.raises(ApplyConflict):
        store.apply(*created.key, {"spec":{"replicas":2}}, "controller")
    updated=store.apply(*created.key, {"spec":{"replicas":2}}, "controller", force=True)
    assert updated.spec["replicas"] == 2
    assert "spec.replicas" not in updated.metadata.managed_fields["author"]


def test_finalizer_delays_deletion():
    store=ApiStore(); created=store.create(obj())
    created=store.add_finalizer(created, "cleanup", "controller")
    pending=store.delete(created)
    assert pending is not None and pending.metadata.deletion_timestamp
    assert store.remove_finalizer(pending, "cleanup", "controller") is None
    with pytest.raises(NotFound): store.get(*created.key)


def test_watch_since_revision():
    store=ApiStore(); created=store.create(obj())
    rv=created.metadata.resource_version
    changed=created.clone(); changed.spec["replicas"]=4
    store.replace(changed, rv)
    assert len(store.watch_since(rv)) == 1
