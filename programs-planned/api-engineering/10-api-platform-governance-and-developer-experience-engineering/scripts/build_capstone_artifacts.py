#!/usr/bin/env python3
"""Build deterministic learner-visible Analysis API Platform artifacts."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capstone"
PY_SRC = CAP / "tracks/python-platform/src"
sys.path.insert(0, str(PY_SRC))

from analysis_platform.analytics import product_metrics, search_success
from analysis_platform.catalog import Catalog
from analysis_platform.lifecycle import deprecation_impact
from analysis_platform.portal import build_search_index, write_portal
from analysis_platform.registry import ContractRegistry
from analysis_platform.runtime import route_drift
from analysis_platform.sandbox import create_session
from analysis_platform.scorecards import scorecard
from analysis_platform.supply_chain import verify_publication
from analysis_platform.support import response_seconds, route_ticket
from analysis_platform.templates import render_template
from analysis_platform.release import evaluate_platform_release


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict[str, object]:
    catalog = Catalog.from_records(read_json(CAP / "catalog/entities.json")["entities"])
    registry = ContractRegistry.from_records(read_json(CAP / "registry/releases.json")["releases"])
    verified_releases = []
    for (api_ref, version), release in sorted(registry.releases.items()):
        if not registry.verify_file(api_ref, version, CAP):
            raise SystemExit(f"registry digest mismatch: {api_ref}@{version}")
        verified_releases.append({"apiRef": api_ref, "version": version, "sha256": release.sha256})

    evidence = read_json(CAP / "governance/evidence-ledger.json")["evidence"]
    scorecards = [scorecard(api_ref, evidence) for api_ref, _ in catalog.api_inventory()]
    write_json(CAP / "reports/scorecards.json", {"version": "1.0", "scorecards": scorecards})

    consumers = read_json(CAP / "lifecycle/consumers.json")["consumers"]
    impact = deprecation_impact(consumers, "api:default/analysis-http", "1.1.0")
    write_json(CAP / "reports/deprecation-impact.json", impact)

    desired = read_json(CAP / "runtime/desired-routes.json")["routes"]
    current = read_json(CAP / "runtime/current-routes.json")["routes"]
    drift = route_drift(desired, current)
    write_json(CAP / "reports/runtime-drift.json", drift)

    usage = [json.loads(line) for line in (CAP / "analytics/usage-events.jsonl").read_text().splitlines() if line]
    analytics = product_metrics(usage, {("api:default/analysis-http", "1.1.0")})
    analytics["search"] = search_success(read_json(CAP / "analytics/search-events.json")["events"])
    write_json(CAP / "reports/product-metrics.json", analytics)

    docs_root = CAP / "docs/source"
    index = build_search_index(docs_root)
    portal_dir = CAP / "portal"
    shutil.rmtree(portal_dir, ignore_errors=True)
    write_portal(index, {"entities": len(catalog.entities), "apis": len(catalog.api_inventory())}, portal_dir)

    generated = CAP / "generated/golden-path/reporting-api"
    shutil.rmtree(generated, ignore_errors=True)
    template_spec = read_json(CAP / "templates/api-capability/template.json")
    generated_files = render_template(
        skeleton=CAP / "templates/api-capability/skeleton",
        destination=generated,
        params={
            "api_name": "reporting-api",
            "title": "Reporting API",
            "owner": "group:default/analysis-control-team",
            "protocol": "openapi",
            "system": "system:default/analysis-platform",
        },
        spec=template_spec,
    )

    sdk_ok, sdk_reason = verify_publication(
        read_json(CAP / "sdk/publication.json"),
        CAP / "sdk",
        read_json(CAP / "sdk/sbom.cyclonedx-1.7.json"),
        read_json(CAP / "sdk/provenance.slsa-v1.json"),
    )
    write_json(CAP / "reports/sdk-publication.json", {"verified": sdk_ok, "reason": sdk_reason})

    profile = read_json(CAP / "sandbox/profile.json")
    session = create_session(
        subject="course10-tour",
        nonce="analysis-platform-1",
        now=datetime(2026, 8, 8, 9, 0, tzinfo=timezone.utc),
        profile=profile,
    )
    write_json(CAP / "reports/sandbox-session.json", {
        "id": session.id,
        "tenant": session.tenant,
        "createdAt": session.created_at.isoformat(),
        "expiresAt": session.expires_at.isoformat(),
        "credentialExpiresAt": session.credential_expires_at.isoformat(),
        "dataClass": session.data_class,
    })

    routes = read_json(CAP / "support/routes.json")["routes"]
    tickets = read_json(CAP / "support/tickets.json")["tickets"]
    support = {
        "platformOwner": route_ticket("portal-registry-template", routes),
        "contractOwner": route_ticket("contract-semantics", routes, catalog_owner="group:default/analysis-control-team"),
        "responseSeconds": {t["id"]: response_seconds(t) for t in tickets},
    }
    write_json(CAP / "reports/support-summary.json", support)

    release_matrix = [
        {"id":"accepted-platform-1.0","expectedDecision":"accepted","evidence":{}},
        {"id":"review-doc-exception","expectedDecision":"review","evidence":{"policy_decision":"review"}},
        {"id":"rejected-unowned-api","expectedDecision":"rejected","evidence":{"catalog_valid":False}},
        {"id":"rejected-mutable-release","expectedDecision":"rejected","evidence":{"registry_valid":False}},
        {"id":"rejected-retirement-with-consumer","expectedDecision":"rejected","evidence":{"lifecycle_safe":False}},
        {"id":"rejected-secret-template","expectedDecision":"rejected","evidence":{"template_safe":False}},
        {"id":"rejected-sdk-without-provenance","expectedDecision":"rejected","evidence":{"sdk_traceable":False}},
        {"id":"rejected-gateway-domain-policy","expectedDecision":"rejected","evidence":{"runtime_safe":False}},
        {"id":"rejected-production-sandbox-data","expectedDecision":"rejected","evidence":{"sandbox_safe":False}},
        {"id":"rejected-score-average","expectedDecision":"rejected","evidence":{"policy_decision":"fail"}},
        {"id":"rejected-expiry-free-exception","expectedDecision":"rejected","evidence":{"policy_decision":"fail"}},
    ]
    base = dict(
        catalog_valid=True, registry_valid=True, policy_decision="pass",
        lifecycle_safe=True, template_safe=True, docs_complete=True,
        sdk_traceable=True, runtime_safe=True, sandbox_safe=True,
    )
    release_results = []
    for item in release_matrix:
        args = dict(base); args.update(item["evidence"])
        decision = evaluate_platform_release(**args)
        if decision.decision != item["expectedDecision"]:
            raise SystemExit(f"release fixture mismatch: {item['id']}")
        release_results.append({"id":item["id"],"decision":decision.decision,"reasons":list(decision.reasons)})
    write_json(CAP / "reports/release-decisions.json", {"version":"1.0","results":release_results})

    dossier = {
        "platformRelease":"1.0.0",
        "catalog":{"entities":len(catalog.entities),"apis":len(catalog.api_inventory())},
        "registry":{"verifiedReleases":verified_releases},
        "governance":{"scorecards":scorecards,"activeExceptions":len(read_json(CAP/'governance/exceptions.json')['exceptions'])},
        "lifecycle":impact,
        "goldenPath":{"generatedFiles":[str(p.relative_to(generated)) for p in generated_files]},
        "documentation":{"documents":len(index),"portalDigest":sha256(portal_dir/'portal.json')},
        "sdk":{"verified":sdk_ok,"reason":sdk_reason},
        "runtime":drift,
        "productMetrics":analytics,
        "support":support,
        "releaseDecisions":release_results,
        "evidenceBoundary":[
            "dependency-light semantic proof executed",
            "operated Backstage, package registry, identity platform, and cloud gateway not executed",
            "SLSA and CycloneDX files are course profiles, not third-party attestations",
        ],
    }
    write_json(CAP / "final-defense/platform-release-dossier.json", dossier)
    (CAP / "final-defense/README.md").write_text(
        "# Analysis API Platform 1.0 release dossier\n\n"
        "The machine-readable dossier assembles ownership, immutable releases, "
        "governance evidence, lifecycle impact, golden-path output, documentation, "
        "SDK traceability, runtime drift, product outcomes, support evidence, and "
        "release decisions. Defend the authority and limitations of every section; "
        "do not treat a green summary as proof by itself.\n",
        encoding="utf-8",
    )

    return {
        "catalogEntities": len(catalog.entities),
        "catalogApis": len(catalog.api_inventory()),
        "registryReleases": len(verified_releases),
        "scorecards": len(scorecards),
        "docs": len(index),
        "generatedFiles": len(generated_files),
        "releaseCandidates": len(release_results),
        "runtimeInSync": drift["inSync"],
        "sdkVerified": sdk_ok,
    }


if __name__ == "__main__":
    result = build()
    print(json.dumps(result, indent=2, sort_keys=True))
