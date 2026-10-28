from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile

import pytest

from analysis_platform.analytics import product_metrics, search_success
from analysis_platform.catalog import Catalog, CatalogError
from analysis_platform.identifiers import entity_ref, IdentifierError
from analysis_platform.lifecycle import deprecation_impact, evaluate_transition
from analysis_platform.models import Finding
from analysis_platform.policy import evaluate_findings, validate_exception
from analysis_platform.registry import ContractRegistry, RegistryError
from analysis_platform.runtime import route_drift, validate_route, RuntimePolicyError
from analysis_platform.sandbox import create_session, validate_import, SandboxError
from analysis_platform.scorecards import scorecard
from analysis_platform.supply_chain import publication_decision
from analysis_platform.templates import render_template, TemplateError
from analysis_platform.release import evaluate_platform_release

CAP=Path(__file__).resolve().parents[3]


def load(rel):
    return json.loads((CAP/rel).read_text())


def test_entity_ref_is_canonical():
    assert entity_ref('API','default','analysis-http')=='api:default/analysis-http'
    with pytest.raises(IdentifierError): entity_ref('API','default','AnalysisHTTP')


def test_catalog_validates_real_inventory():
    catalog=Catalog.from_records(load('catalog/entities.json')['entities'])
    assert catalog.owner_of('api:default/analysis-http')=='group:default/analysis-control-team'
    assert 'component:default/analysis-api-platform' in catalog.consumers_of('api:default/analysis-http')


def test_catalog_rejects_orphan_api():
    records=load('catalog/entities.json')['entities']
    bad=[dict(x) for x in records]
    bad.append({'kind':'API','namespace':'default','name':'orphan','title':'Orphan','owner':'group:default/api-platform-team','lifecycle':'active','system':'system:default/analysis-platform','providesApis':[],'consumesApis':[],'dependsOn':[]})
    with pytest.raises(CatalogError,match='orphan-api'): Catalog.from_records(bad)


def test_registry_verifies_real_contracts():
    registry=ContractRegistry.from_records(load('registry/releases.json')['releases'])
    for release in registry.releases.values():
        assert registry.verify_file(release.api_ref,release.version,CAP)


def test_registry_is_immutable():
    reg=ContractRegistry(); now=datetime.now(timezone.utc)
    kwargs=dict(api_ref='api:default/x',protocol='openapi',version='1.0.0',source='x',owner='group:default/x',compatibility_evidence='e.json',published_at=now)
    assert reg.publish(data=b'a',**kwargs)=='published'
    assert reg.publish(data=b'a',**kwargs)=='idempotent'
    with pytest.raises(RegistryError,match='immutable-release'): reg.publish(data=b'b',**kwargs)


def test_policy_never_averages_away_blocker():
    findings=[Finding('SEC-001','blocker','fail','api:default/x','missing'),Finding('DOC-001','major','pass','api:default/x','ok')]
    assert evaluate_findings(findings)=='fail'


def test_exception_requires_expiry_and_control():
    record=load('governance/exceptions.json')['exceptions'][0]
    ok,reason=validate_exception(record,datetime(2026,8,8,tzinfo=timezone.utc))
    assert (ok,reason)==(True,'valid')
    bad=dict(record); bad.pop('expiresAt')
    assert validate_exception(bad,datetime(2026,8,8,tzinfo=timezone.utc))[0] is False


def test_lifecycle_blocks_retirement_with_consumer():
    policy=load('lifecycle/policy.json')
    decision=evaluate_transition(current='deprecated',target='retired',evidence=['zeroBlockingConsumers','retirementApproval','runtimeRemovalPlan','archivePlan'],policy=policy,blocking_consumers=1)
    assert not decision.allowed and decision.reason=='blocking-consumers'


def test_deprecation_impact_uses_real_consumers():
    result=deprecation_impact(load('lifecycle/consumers.json')['consumers'],'api:default/analysis-http','1.1.0')
    assert result['retirementDecision']=='blocked'
    assert result['blockingConsumers']==['consumer-legacy-cli']


def test_template_renders_exact_outputs():
    spec=load('templates/api-capability/template.json')
    params={'api_name':'reporting-api','title':'Reporting API','owner':'group:default/analysis-control-team','protocol':'openapi','system':'system:default/analysis-platform'}
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'generated'
        files=render_template(skeleton=CAP/'templates/api-capability/skeleton',destination=out,params=params,spec=spec)
        assert len(files)==6
        assert 'Reporting API' in (out/'README.md').read_text()


def test_template_rejects_bad_parameter():
    spec=load('templates/api-capability/template.json')
    params={'api_name':'Reporting API','title':'Reporting API','owner':'group:default/analysis-control-team','protocol':'openapi','system':'system:default/analysis-platform'}
    with tempfile.TemporaryDirectory() as td:
        with pytest.raises(TemplateError,match='invalid-parameter'): render_template(skeleton=CAP/'templates/api-capability/skeleton',destination=Path(td)/'x',params=params,spec=spec)


def test_sandbox_is_synthetic_and_expiring():
    now=datetime(2026,8,8,tzinfo=timezone.utc)
    session=create_session(subject='learner',nonce='1',now=now,profile=load('sandbox/profile.json'))
    assert session.tenant.startswith('sandbox-') and session.active(now)
    with pytest.raises(SandboxError): validate_import(session,'production')


def test_runtime_drift_and_domain_boundary():
    desired=load('runtime/desired-routes.json')['routes']; current=load('runtime/current-routes.json')['routes']
    assert route_drift(desired,current)['inSync']
    for route in desired: validate_route(route)
    bad=dict(desired[0]); bad['domainAuthz']='gateway-project-owner'
    with pytest.raises(RuntimePolicyError): validate_route(bad)


def test_product_metrics_measure_outcome_not_page_views():
    events=[json.loads(line) for line in (CAP/'analytics/usage-events.jsonl').read_text().splitlines()]
    result=product_metrics(events,{('api:default/analysis-http','1.1.0')})
    assert result=={'activeConsumers':5,'medianTimeToFirstSuccessSeconds':240.0,'deprecatedVersionUses':1}
    search_result=search_success(load('analytics/search-events.json')['events'])
    assert search_result['zeroResultRate']==0.0


def test_scorecard_has_blockers_not_average():
    evidence=load('governance/evidence-ledger.json')['evidence']
    assert scorecard('api:default/analysis-http',evidence)['status']=='ready'
    broken=evidence+[{'entityRef':'api:default/analysis-http','kind':'security','status':'fail'}]
    assert scorecard('api:default/analysis-http',broken)['status']=='blocked'


def test_publication_decision_requires_all_evidence():
    assert publication_decision(has_digest=True,has_sbom=True,has_provenance=True)=='publish'
    assert publication_decision(has_digest=True,has_sbom=True,has_provenance=False)=='incomplete-publication'


def test_release_gate_orders_correctness_before_convenience():
    accepted=evaluate_platform_release(catalog_valid=True,registry_valid=True,policy_decision='pass',lifecycle_safe=True,template_safe=True,docs_complete=True,sdk_traceable=True,runtime_safe=True,sandbox_safe=True)
    assert accepted.decision=='accepted'
    rejected=evaluate_platform_release(catalog_valid=True,registry_valid=True,policy_decision='pass',lifecycle_safe=True,template_safe=True,docs_complete=True,sdk_traceable=True,runtime_safe=False,sandbox_safe=True)
    assert rejected.decision=='rejected' and rejected.reasons==('runtime',)
