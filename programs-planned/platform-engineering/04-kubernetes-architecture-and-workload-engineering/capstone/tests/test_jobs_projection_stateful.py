import pytest
from atlas_kube.jobs import EffectStore, JobState, AttemptResult, CronConcurrency, cron_decision
from atlas_kube.projection import configuration_digest, Projection, ApplicationConfig, secret_annotation_guard
from atlas_kube.stateful import identities, controller_fit


def test_exactly_once_effect_identity():
    store=EffectStore(); assert store.commit("run/0","abc")
    assert store.commit("run/0","abc") is False
    with pytest.raises(ValueError): store.commit("run/0","different")


def test_indexed_job_completion():
    job=JobState(completions=3,backoff_limit=1)
    job.record(0,AttemptResult.SUCCEEDED); job.record(1,AttemptResult.SUCCEEDED)
    assert not job.complete
    job.record(2,AttemptResult.SUCCEEDED); assert job.complete


def test_job_failure_limit():
    job=JobState(completions=1,backoff_limit=1)
    job.record(0,AttemptResult.FAILED); assert not job.failed
    job.record(0,AttemptResult.FAILED); assert job.failed


def test_cron_policy():
    assert cron_decision(CronConcurrency.FORBID,1)=="skip"
    assert cron_decision(CronConcurrency.REPLACE,1)=="replace"
    assert cron_decision(CronConcurrency.ALLOW,2)=="start"


def test_configuration_digest_order_independent():
    assert configuration_digest({"a":"1","b":"2"})==configuration_digest({"b":"2","a":"1"})


def test_projection_reload():
    app=ApplicationConfig({"fixed":"x"})
    p=Projection("1",{"dynamic":"a"})
    assert app.reload_projection(p); assert not app.reload_projection(p)


def test_secret_annotation_guard():
    assert secret_annotation_guard({"note":"ok","api_token":"secret-value"})==["api_token"]


def test_stateful_identities():
    ids=identities("db","db","atlas","data",2)
    assert ids[1].pod_name=="db-1" and ids[1].claim_name=="data-db-1"

@pytest.mark.parametrize("kwargs,expected",[
    ({"finite":True,"per_node":False,"stable_identity":False,"continuously_running":False},"Job"),
    ({"finite":False,"per_node":True,"stable_identity":False,"continuously_running":False},"DaemonSet"),
    ({"finite":False,"per_node":False,"stable_identity":True,"continuously_running":False},"StatefulSet"),
    ({"finite":False,"per_node":False,"stable_identity":False,"continuously_running":True},"Deployment"),
])
def test_controller_fit(kwargs,expected): assert controller_fit(**kwargs)==expected
