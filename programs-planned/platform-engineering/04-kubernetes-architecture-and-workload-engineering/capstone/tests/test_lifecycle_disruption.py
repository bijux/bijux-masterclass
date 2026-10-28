import pytest
from atlas_kube.lifecycle import ProbeState, ShutdownPlan, restart_backoff_seconds
from atlas_kube.disruption import disruptions_allowed


def test_probe_thresholds():
    p=ProbeState(failure_threshold=3)
    assert [p.observe(False) for _ in range(3)] == ["pending","pending","failed"]
    assert p.observe(True)=="succeeded"


def test_shutdown_budget():
    assert ShutdownPlan(30,5,20).feasible
    assert ShutdownPlan(30,10,25).feasible is False


def test_restart_backoff_capped():
    assert restart_backoff_seconds(0)==10
    assert restart_backoff_seconds(10)==300

@pytest.mark.parametrize("healthy,expected",[(3,1),(2,0),(1,0)])
def test_pdb_min_available(healthy,expected):
    assert disruptions_allowed(desired=3,healthy=healthy,min_available=2)==expected


def test_pdb_percentage():
    assert disruptions_allowed(desired=5,healthy=5,max_unavailable="20%")==1


def test_pdb_requires_one_policy():
    with pytest.raises(ValueError): disruptions_allowed(desired=3,healthy=3)
