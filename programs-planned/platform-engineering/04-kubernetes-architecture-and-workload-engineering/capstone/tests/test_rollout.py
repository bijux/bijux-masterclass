import pytest
from atlas_kube.rollout import rollout_bounds, rollout_complete, resolve_int_or_percent


def test_percent_rounding():
    bounds=rollout_bounds(3,"25%","25%")
    assert (bounds.max_surge,bounds.max_unavailable,bounds.max_total,bounds.min_available)==(1,0,4,3)

@pytest.mark.parametrize("replicas,surge,unavailable,expected",[
    (1,"25%","25%",(1,0,2,1)),
    (4,"25%","25%",(1,1,5,3)),
    (5,"40%","20%",(2,1,7,4)),
])
def test_bounds(replicas,surge,unavailable,expected):
    b=rollout_bounds(replicas,surge,unavailable)
    assert (b.max_surge,b.max_unavailable,b.max_total,b.min_available)==expected


def test_zero_zero_rejected():
    with pytest.raises(ValueError): rollout_bounds(3,0,0)


def test_completion_requires_all_populations():
    assert rollout_complete(desired=3,updated=3,ready=3,available=3,unavailable=0)
    assert not rollout_complete(desired=3,updated=3,ready=3,available=2,unavailable=0)
