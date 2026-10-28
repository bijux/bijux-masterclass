#!/usr/bin/env python3
"""Verification and learner routes for Course 10.

Dependency-light checks prove the bounded Analysis API Platform profile in this
course. They do not claim that an operated Backstage deployment, package
registry, cloud gateway, identity platform, or external standards toolchain was
executed when those systems are absent.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import py_compile
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
import tomllib
from typing import Any
from urllib.parse import urlparse, unquote

try:
    import yaml
except Exception as exc:
    raise SystemExit(f"PyYAML is required: {exc}")

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capstone"
BOOK = ROOT / "course-book"
PY_TRACK = CAP / "tracks/python-platform"
PY_SRC = PY_TRACK / "src"
TS_TRACK = CAP / "tracks/typescript-platform"

EXCLUDED_DIRS = {".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "__pycache__", "node_modules", "dist", "site", ".tmp"}
ROOT_MANIFEST_NAMES = {"MANIFEST.json", "MANIFEST.sha256"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def run(command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None, capture: bool = False):
    merged = os.environ.copy(); merged["PYTHONDONTWRITEBYTECODE"] = "1"
    if env: merged.update(env)
    print("+", " ".join(command))
    return subprocess.run(command, cwd=cwd, env=merged, text=True, check=True, capture_output=capture)


def read_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def read_yaml(path: Path): return yaml.safe_load(path.read_text(encoding="utf-8"))
def sha256(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def eligible(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in rel.parts): return False
    if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES: return False
    if len(rel.parts) == 1 and path.name in ROOT_MANIFEST_NAMES: return False
    return path.is_file()


def verify_manifest(directory: Path, exact: bool = True) -> int:
    mp = directory / "MANIFEST.json"; dp = directory / "MANIFEST.sha256"
    assert mp.is_file() and dp.is_file(), f"missing manifest in {directory}"
    assert sha256(mp) == dp.read_text().split()[0], "manifest digest mismatch"
    manifest = read_json(mp); declared = {x["path"]:x for x in manifest["files"]}
    for rel, item in declared.items():
        p = directory / rel
        assert p.is_file(), f"missing manifest file: {rel}"
        assert p.stat().st_size == item.get("size", item.get("bytes")), f"size mismatch: {rel}"
        assert sha256(p) == item["sha256"], f"digest mismatch: {rel}"
    if exact:
        actual = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if eligible(p,directory)}
        assert actual == set(declared), f"manifest inventory mismatch missing={sorted(set(declared)-actual)[:5]} unlisted={sorted(actual-set(declared))[:5]}"
    assert manifest.get("file_count", len(declared)) == len(declared)
    return len(declared)


def import_core():
    sys.path.insert(0, str(PY_SRC))
    from analysis_platform.analytics import product_metrics, search_success
    from analysis_platform.catalog import Catalog, CatalogError
    from analysis_platform.identifiers import entity_ref
    from analysis_platform.lifecycle import deprecation_impact, evaluate_transition
    from analysis_platform.models import Finding
    from analysis_platform.policy import evaluate_findings, validate_exception
    from analysis_platform.registry import ContractRegistry, RegistryError
    from analysis_platform.runtime import route_drift, validate_route, RuntimePolicyError
    from analysis_platform.sandbox import create_session, validate_import, SandboxError
    from analysis_platform.scorecards import scorecard
    from analysis_platform.supply_chain import verify_publication
    from analysis_platform.templates import render_template, TemplateError
    from analysis_platform.support import route_ticket, response_seconds
    from analysis_platform.release import evaluate_platform_release
    return locals()


def doctor():
    print("python", sys.version.split()[0]); print("PyYAML", yaml.__version__)
    for tool in ["node","tsc","pytest","mkdocs","docker","psql","backstage-cli","openapi-generator","asyncapi","buf"]:
        print(f"{tool}: {shutil.which(tool) or 'not-available'}")
    print("course", read_json(ROOT/"course.json")["versionState"])


def predecessor_proof():
    handoff = CAP / "predecessor/handoff"
    count = verify_manifest(handoff, exact=True)
    boundary = read_json(handoff/"BOUNDARY.json")
    assert boundary.get("from", boundary.get("from_course", "")).startswith("09-") and boundary.get("to", boundary.get("to_course", "")).startswith("10-")
    assert count == 12, f"expected 12 Course 9 handoff files, got {count}"
    brief = read_yaml(handoff/"platform-boundary-brief.yaml")
    text = json.dumps(brief).lower()
    assert "business" in text and "catalog" in text
    print(f"PASS Course 9 predecessor handoff — {count} exact files")


def _nav_paths(value: Any) -> list[str]:
    out=[]
    if isinstance(value,str): out.append(value)
    elif isinstance(value,list):
        for x in value: out.extend(_nav_paths(x))
    elif isinstance(value,dict):
        for x in value.values(): out.extend(_nav_paths(x))
    return out


def structure_proof():
    assert (ROOT/"README.md").is_file() and (ROOT/"Makefile").is_file()
    modules = sorted(p for p in BOOK.iterdir() if p.is_dir() and p.name.startswith("module-"))
    assert len(modules) == 11
    orientation = [p for p in modules if p.name.startswith("module-00")]
    numbered = [p for p in modules if not p.name.startswith("module-00")]
    assert len(orientation) == 1 and len(numbered) == 10
    assert {p.name for p in orientation[0].glob("*.md")} == {"index.md", "lab.md", "checkpoint.md"}
    required = {"index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"}
    for module in numbered:
        assert {p.name for p in module.glob("*.md")} == required, f"module shape mismatch {module.name}"
        ex = re.findall(r"^## (\d+)\. (.+)$", (module/"exercises.md").read_text(), re.M)
        ans = re.findall(r"^## (\d+)\. (.+)$", (module/"exercise-answers.md").read_text(), re.M)
        assert ex == ans and len(ex) == 12
        lab = (module/"lab.md").read_text()
        for heading in ["## Objective", "## Why this lab matters", "## Setup conditions",
                        "## Hypothesis", "## Controlled action and investigation",
                        "## Operational oracle", "## Required evidence",
                        "## Interpretation and defense", "## Cleanup and reset",
                        "## Completion gate"]:
            assert heading in lab, f"missing {heading} in {module.name}/lab.md"
        checkpoint = (module/"checkpoint.md").read_text()
        for heading in ["## Required result", "## Demonstrate", "## Commands",
                        "## Evidence to retain", "## Defend the design", "## Continue only when"]:
            assert heading in checkpoint, f"missing {heading} in {module.name}/checkpoint.md"
    pages = list(BOOK.rglob("*.md")); assert len(pages) == 61, len(pages)
    cfg = read_yaml(ROOT/"mkdocs.yml")
    nav = {str((BOOK/p).resolve()) for p in _nav_paths(cfg["nav"]) if p.endswith(".md")}
    expected = {str(p.resolve()) for p in pages}
    assert nav == expected, f"mkdocs nav mismatch missing={len(expected-nav)} extra={len(nav-expected)}"
    print(f"PASS structure — {len(pages)} navigated pages, 10 numbered modules")


def orientation_proof():
    predecessor_proof(); structure_proof()
    version = read_json(ROOT/"course.json")
    assert version["number"] == 10
    assert version["id"] == "api-platform-governance-and-developer-experience-engineering"
    print("PASS orientation")


def contract_proof():
    index = read_yaml(CAP/"contracts/contract-index.yaml")["contracts"]
    registry = read_json(CAP/"registry/releases.json")["releases"]
    by_ref = {(x["apiRef"],x["version"]):x for x in registry}
    assert len(index) == 7 and len(registry) == 7
    protocols = Counter()
    for item in index:
        path = CAP/item["path"]
        assert path.is_file() and sha256(path)==item["sha256"]
        record=by_ref[(item["apiRef"],str(item["version"]))]
        assert record["sha256"]==item["sha256"] and record["source"]==item["path"]
        protocols[item["protocol"]]+=1
        if item["protocol"] in {"openapi","asyncapi"}:
            parsed=read_yaml(path); assert isinstance(parsed,dict)
            key=item["protocol"]; assert str(parsed[key]).startswith("3.")
        elif item["protocol"]=="protobuf":
            text=path.read_text(); assert 'syntax = "proto3"' in text and "service " in text
        elif item["protocol"]=="graphql":
            text=path.read_text(); assert "type Query" in text and "type Mutation" in text and "type Subscription" in text
    assert protocols["openapi"]==4 and protocols["asyncapi"]==1 and protocols["protobuf"]==1 and protocols["graphql"]==1
    print(f"PASS contracts — {len(index)} immutable releases across four protocols")


def catalog_proof():
    c=import_core(); records=read_json(CAP/"catalog/entities.json")["entities"]
    catalog=c["Catalog"].from_records(records)
    assert len(catalog.entities)==23 and len(catalog.api_inventory())==7
    registered={r["apiRef"] for r in read_json(CAP/"registry/releases.json")["releases"]}
    for ref,entity in catalog.api_inventory():
        assert entity.owner and entity.attributes.get("definition") and ref in registered
        assert catalog.consumers_of(ref) or any(ref in x.provides_apis for x in catalog.entities.values())
    docs=list(yaml.safe_load_all((CAP/"catalog/catalog-info.yaml").read_text()))
    assert len(docs)==23
    doc_refs={f"{d['kind'].lower()}:{d['metadata'].get('namespace','default')}/{d['metadata']['name']}" for d in docs}
    assert doc_refs==set(catalog.entities)
    bad=[dict(x) for x in records]; bad.append({"kind":"API","namespace":"default","name":"orphan","title":"Orphan","owner":"group:default/api-platform-team","lifecycle":"active","system":"system:default/analysis-platform","providesApis":[],"consumesApis":[],"dependsOn":[],"definition":"x","protocol":"openapi"})
    try: c["Catalog"].from_records(bad); raise AssertionError("orphan accepted")
    except c["CatalogError"]: pass
    print("PASS catalog — 23 entities, 7 owned and implemented API products")


def registry_proof():
    c=import_core(); records=read_json(CAP/"registry/releases.json")["releases"]
    reg=c["ContractRegistry"].from_records(records)
    for (api,ver),_ in reg.releases.items(): assert reg.verify_file(api,ver,CAP)
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"evidence.json"; path.write_text("{}")
        kwargs=dict(api_ref="api:default/test",protocol="openapi",version="1.0.0",source="x",lifecycle="active",owner="group:default/api-platform-team",compatibility_evidence=str(path),published_at=datetime.now(timezone.utc))
        assert reg.publish(data=b"a",**kwargs)=="published"
        assert reg.publish(data=b"a",**kwargs)=="idempotent"
        try: reg.publish(data=b"b",**kwargs); raise AssertionError("mutable version accepted")
        except c["RegistryError"]: pass
    print(f"PASS registry — {len(records)} digests and immutability")


def governance_proof():
    c=import_core(); policy=read_json(CAP/"governance/policy-pack.json")
    ids=[x["id"] for x in policy["rules"]]; assert len(ids)==len(set(ids))==18
    evidence=read_json(CAP/"governance/evidence-ledger.json")["evidence"]
    now=datetime(2026,8,8,tzinfo=timezone.utc)
    for item in evidence:
        assert (CAP/"governance"/item["source"]).is_file()
        if item.get("expiresAt"): assert datetime.fromisoformat(item["expiresAt"].replace("Z","+00:00"))>now
    apis=[x["apiRef"] for x in read_json(CAP/"registry/releases.json")["releases"]]
    for api in apis:
        card=c["scorecard"](api,evidence); assert card["status"]=="ready" and not card["blockers"]
    exception=read_json(CAP/"governance/exceptions.json")["exceptions"][0]
    assert c["validate_exception"](exception,now)==(True,"valid")
    bad=dict(exception); bad.pop("expiresAt")
    assert c["validate_exception"](bad,now)[0] is False
    findings=[c["Finding"]("SEC","blocker","fail","api:default/x","broken"),c["Finding"]("DOC","major","pass","api:default/x","ok")]
    assert c["evaluate_findings"](findings)=="fail"
    print(f"PASS governance — {len(policy['rules'])} rules, {len(evidence)} evidence records")


def lifecycle_proof():
    c=import_core(); policy=read_json(CAP/"lifecycle/policy.json")
    consumers=read_json(CAP/"lifecycle/consumers.json")["consumers"]
    impact=c["deprecation_impact"](consumers,"api:default/analysis-http","1.1.0")
    assert impact["retirementDecision"]=="blocked" and impact["blockingConsumers"]==["consumer-legacy-cli"]
    evidence=["zeroBlockingConsumers","retirementApproval","runtimeRemovalPlan","archivePlan"]
    assert not c["evaluate_transition"](current="deprecated",target="retired",evidence=evidence,policy=policy,blocking_consumers=1).allowed
    assert c["evaluate_transition"](current="deprecated",target="retired",evidence=evidence,policy=policy,blocking_consumers=0).allowed
    print("PASS lifecycle — consumer-safe retirement gate")


def template_proof():
    c=import_core(); spec=read_json(CAP/"templates/api-capability/template.json")
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"generated"
        files=c["render_template"](skeleton=CAP/"templates/api-capability/skeleton",destination=out,params={"api_name":"reporting-api","title":"Reporting API","owner":"group:default/analysis-control-team","protocol":"openapi","system":"system:default/analysis-platform"},spec=spec)
        assert len(files)==6 and {str(p.relative_to(out)) for p in files}==set(spec["outputs"])
        secret=Path(td)/"secret"; secret.mkdir(); (secret/"x.tmpl").write_text("token=abcdefghijk")
        broken=dict(spec); broken["outputs"]=["x"]
        try: c["render_template"](skeleton=secret,destination=Path(td)/"bad",params={"api_name":"reporting-api","title":"Reporting API","owner":"group:default/analysis-control-team","protocol":"openapi","system":"system:default/analysis-platform"},spec=broken); raise AssertionError("secret accepted")
        except c["TemplateError"]: pass
    checked=CAP/"generated/golden-path/reporting-api"
    assert checked.is_dir() and {str(p.relative_to(checked)) for p in checked.rglob("*") if p.is_file()}==set(spec["outputs"])
    print("PASS golden path — deterministic six-file output and secret rejection")


def documentation_proof():
    policy=read_json(CAP/"docs/coverage-policy.json"); coverage=read_json(CAP/"docs/coverage.json")["apis"]
    active={r["apiRef"] for r in read_json(CAP/"registry/releases.json")["releases"]}
    assert {x["apiRef"] for x in coverage}==active
    for item in coverage:
        for field in policy["requiredForActive"]:
            assert field in item and item[field]
            assert (CAP/"docs"/item[field]).resolve().is_file(), f"missing docs {item['apiRef']} {field}"
    portal=read_json(CAP/"portal/portal.json"); assert len(portal["documents"])>=15
    metrics=read_json(CAP/"reports/product-metrics.json")
    assert metrics["search"]["zeroResultRate"] <= policy["searchZeroResultBudget"]
    print(f"PASS documentation — {len(coverage)} API products and {len(portal['documents'])} indexed pages")


def sandbox_proof():
    c=import_core(); profile=read_json(CAP/"sandbox/profile.json")
    s=c["create_session"](subject="proof",nonce="1",now=datetime(2026,8,8,tzinfo=timezone.utc),profile=profile)
    assert s.data_class=="synthetic-only" and s.tenant.startswith("sandbox-")
    try: c["validate_import"](s,"production"); raise AssertionError("production data accepted")
    except c["SandboxError"]: pass
    assert read_json(CAP/"sandbox/synthetic-data.json")["dataClass"]=="synthetic-only"
    print("PASS sandbox — isolated, expiring, synthetic-only")


def sdk_proof():
    c=import_core(); ok,reason=c["verify_publication"](read_json(CAP/"sdk/publication.json"),CAP/"sdk",read_json(CAP/"sdk/sbom.cyclonedx-1.7.json"),read_json(CAP/"sdk/provenance.slsa-v1.json"))
    assert ok and reason=="verified"
    assert read_json(CAP/"sdk/sbom.cyclonedx-1.7.json")["specVersion"]=="1.7"
    assert read_json(CAP/"sdk/provenance.slsa-v1.json")["predicateType"]=="https://slsa.dev/provenance/v1"
    print("PASS SDK publication — digests, CycloneDX profile, SLSA provenance profile")


def runtime_proof():
    c=import_core(); desired=read_json(CAP/"runtime/desired-routes.json")["routes"]; current=read_json(CAP/"runtime/current-routes.json")["routes"]
    drift=c["route_drift"](desired,current); assert drift["inSync"] and len(desired)==3
    for route in desired: c["validate_route"](route)
    bad=dict(desired[0]); bad["domainAuthz"]="gateway-project-owner"
    try: c["validate_route"](bad); raise AssertionError("domain policy at edge accepted")
    except c["RuntimePolicyError"]: pass
    print("PASS runtime — approved routes in sync; business authorization remains with owners")


def analytics_proof():
    c=import_core(); events=[json.loads(x) for x in (CAP/"analytics/usage-events.jsonl").read_text().splitlines() if x]
    result=c["product_metrics"](events,{("api:default/analysis-http","1.1.0")})
    assert result=={"activeConsumers":5,"medianTimeToFirstSuccessSeconds":240.0,"deprecatedVersionUses":1}
    search=c["search_success"](read_json(CAP/"analytics/search-events.json")["events"])
    baseline=c["search_success"](read_json(CAP/"analytics/search-events-baseline.json")["events"])
    assert search["zeroResultRate"]==0.0 and baseline["zeroResultRate"]==0.25
    print("PASS analytics — outcomes, deprecated use, and search improvement")


def support_proof():
    routes=read_json(CAP/"support/routes.json")["routes"]; tickets=read_json(CAP/"support/tickets.json")["tickets"]
    categories={x["category"] for x in routes}; assert len(categories)==4
    from statistics import median
    c=import_core(); responses=[c["response_seconds"](x) for x in tickets]
    assert all(x>=0 for x in responses) and median(responses)>=0
    assert c["route_ticket"]("portal-registry-template",routes)=="group:default/api-platform-team"
    print(f"PASS support — {len(routes)} routes, {len(tickets)} evidence tickets")


def release_proof():
    c=import_core(); results=read_json(CAP/"reports/release-decisions.json")["results"]
    counts=Counter(x["decision"] for x in results)
    assert counts==Counter({"rejected":9,"accepted":1,"review":1})
    dossier=read_json(CAP/"final-defense/platform-release-dossier.json")
    assert dossier["platformRelease"]=="1.0.0" and dossier["runtime"]["inSync"]
    accepted=c["evaluate_platform_release"](catalog_valid=True,registry_valid=True,policy_decision="pass",lifecycle_safe=True,template_safe=True,docs_complete=True,sdk_traceable=True,runtime_safe=True,sandbox_safe=True)
    assert accepted.decision=="accepted"
    print("PASS release — accepted, review, and nine rejection paths")


def migration_proof():
    files=sorted((CAP/"database/platform-catalog/migrations").glob("*.sql"))
    assert [p.name[:3] for p in files]==["001","002","003","004"]
    text="\n".join(p.read_text() for p in files)
    for table in ["platform_entities","api_contract_releases","api_consumers","platform_evidence","policy_exceptions","platform_product_events","platform_support_cases"]:
        assert f"CREATE TABLE {table}" in text
    assert "UPDATE api_contract_releases" not in text
    print("PASS migrations — four platform-catalog revisions")


def vector_proof():
    files=sorted((CAP/"shared/vectors").glob("*.json")); assert len(files)==10
    cases=0
    for p in files:
        data=read_json(p); assert data.get("cases"); cases+=len(data["cases"])
    print(f"PASS shared vectors — {len(files)} files, {cases} cases")


def python_proof():
    run([sys.executable,"-m","pytest","-q","-p","no:cacheprovider"],cwd=PY_TRACK,env={"PYTHONPATH":str(PY_SRC)})
    print("PASS Python semantic track")


def typescript_proof():
    run(["tsc","-p","tsconfig.json"],cwd=TS_TRACK)
    run(["node","--test","test/platform.test.mjs"],cwd=TS_TRACK)
    shutil.rmtree(TS_TRACK / "dist", ignore_errors=True)
    print("PASS TypeScript semantic track")


def network_lab_proof():
    run([sys.executable,"-m","pytest","-q","-p","no:cacheprovider","test_network_lab.py"],cwd=CAP/"network-lab")
    print("PASS loopback platform network laboratory")


def planted_defect_proof():
    dirs=sorted((CAP/"planted-defects").iterdir()); assert len(dirs)==10
    allowed={"catalog-proof","registry-proof","policy-proof","lifecycle-proof","template-proof","docs-proof","sdk-proof","runtime-proof","analytics-proof"}
    ids=set()
    for d in dirs:
        x=read_json(d/"defect.json"); ids.add(x["id"]); assert x["expectedRejectingProof"] in allowed
    assert len(ids)==10
    print("PASS planted defects — 10 defects mapped to rejecting proofs")


def final_defense_proof():
    dossier=read_json(CAP/"final-defense/platform-release-dossier.json")
    required={"catalog","registry","governance","lifecycle","goldenPath","documentation","sdk","runtime","productMetrics","support","releaseDecisions","evidenceBoundary"}
    assert required <= set(dossier)
    rubric=(ROOT/"assessment/final-rubric.md").read_text(); defense=(ROOT/"assessment/final-defense.md").read_text()
    assert "100" in rubric and "85" in rubric
    for word in ["consumer","owner","reviewer","operator","platform"]: assert word in defense.lower()
    graduation = CAP / "graduation"
    assert verify_manifest(graduation, exact=True) == 8
    assert read_yaml(graduation / "version-ledger.yaml")["completedCourses"] == 10
    print("PASS final defense dossier, graduation bundle, and assessment")


def capstone_tour():
    run([sys.executable,"scripts/build_capstone_artifacts.py"])
    summary=read_json(CAP/"final-defense/platform-release-dossier.json")
    print(json.dumps({"release":summary["platformRelease"],"apis":summary["catalog"]["apis"],"runtimeInSync":summary["runtime"]["inSync"],"deprecatedBlockingConsumers":summary["lifecycle"]["blockingConsumers"],"sdkVerified":summary["sdk"]["verified"]},indent=2))
    print("PASS capstone tour")


def data_format_proof():
    json_files=[p for p in ROOT.rglob("*.json") if not any(x in EXCLUDED_DIRS for x in p.parts)]
    yaml_files=[p for p in ROOT.rglob("*.yaml") if not any(x in EXCLUDED_DIRS for x in p.parts)]+[p for p in ROOT.rglob("*.yml") if not any(x in EXCLUDED_DIRS for x in p.parts)]
    toml_files=[p for p in ROOT.rglob("*.toml") if not any(x in EXCLUDED_DIRS for x in p.parts)]
    for p in json_files: json.loads(p.read_text())
    for p in yaml_files: list(yaml.safe_load_all(p.read_text()))
    for p in toml_files: tomllib.loads(p.read_text())
    print(f"PASS data formats — JSON {len(json_files)}, YAML {len(yaml_files)}, TOML {len(toml_files)}")


def _local_links(text: str):
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)",text):
        target=target.strip().split()[0].strip("<>")
        if target.startswith(("http://","https://","mailto:","#","data:")): continue
        yield unquote(target.split("#",1)[0])


def markdown_link_proof():
    checked=0
    for p in ROOT.rglob("*.md"):
        if any(x in EXCLUDED_DIRS for x in p.parts): continue
        for target in _local_links(p.read_text(errors="ignore")):
            if not target: continue
            checked+=1; resolved=(p.parent/target).resolve()
            assert resolved.exists(), f"broken Markdown link {p.relative_to(ROOT)} -> {target}"
    print(f"PASS Markdown links — {checked} local targets")


def education_proof():
    pages=list(BOOK.rglob("*.md")); words=sum(len(p.read_text().split()) for p in pages)
    assert len(pages)==61 and words>=26000
    modules=sorted(p for p in BOOK.iterdir() if p.is_dir() and p.name.startswith("module-") and not p.name.startswith("module-00"))
    exercise_count=answer_count=0
    paragraphs=[]
    for module in modules:
        ex=re.findall(r"^## (\d+)\.", (module/"exercises.md").read_text(), re.M)
        ans=re.findall(r"^## (\d+)\.", (module/"exercise-answers.md").read_text(), re.M)
        assert ex==ans==[str(i) for i in range(1,13)]
        exercise_count+=len(ex); answer_count+=len(ans)
        lab=(module/"lab.md").read_text(); checkpoint=(module/"checkpoint.md").read_text()
        for heading in ["## Objective", "## Why this lab matters", "## Setup conditions",
                        "## Hypothesis", "## Controlled action and investigation",
                        "## Operational oracle", "## Required evidence",
                        "## Interpretation and defense", "## Cleanup and reset",
                        "## Completion gate"]: assert heading in lab
        assert len(re.findall(r"^- ",checkpoint,re.M))>=5
        chapter=(module/"index.md").read_text(); assert len(chapter.split())>=1350
        for block in re.split(r"\n\s*\n",chapter):
            norm=" ".join(block.split())
            if len(norm.split())>=45: paragraphs.append(norm)
    assert exercise_count==answer_count==120
    common=[(p,n) for p,n in Counter(paragraphs).items() if n>=3]
    assert not common, f"repeated long teaching paragraphs: {common[:2]}"
    forbidden=["TODO","TBD","lorem ipsum","as an ai","evidence direction","common incomplete answer"]
    lower="\n".join(p.read_text(errors="ignore") for p in pages).lower()
    for term in forbidden: assert term.lower() not in lower, f"unfinished or generated filler: {term}"
    print(f"PASS education — {words} words, 120 exercises/answers, 10 labs/checkpoints")


def snippet_proof():
    python_blocks=[]; ts_blocks=[]
    pattern=re.compile(r"^```(python|typescript)\n(.*?)^```",re.M|re.S)
    for page in BOOK.rglob("*.md"):
        for language,code in pattern.findall(page.read_text()):
            (python_blocks if language=="python" else ts_blocks).append((page,code))
    assert len(python_blocks)==10 and len(ts_blocks)==10
    for page,code in python_blocks:
        compile(code,str(page),"exec")
    if not shutil.which("tsc"):
        raise SystemExit("tsc unavailable for TypeScript curriculum snippets")
    with tempfile.TemporaryDirectory() as td:
        for index,(page,code) in enumerate(ts_blocks,1):
            path=Path(td)/f"snippet-{index:02d}.ts"; path.write_text(code)
            run(["tsc","--strict","--target","ES2022","--module","ESNext","--noEmit","--skipLibCheck",str(path)],cwd=ROOT)
    print(f"PASS curriculum snippets — Python {len(python_blocks)}, TypeScript {len(ts_blocks)}")

def python_syntax_proof():
    files=[p for p in ROOT.rglob("*.py") if not any(x in EXCLUDED_DIRS for x in p.parts)]
    with tempfile.TemporaryDirectory() as td:
        for i,p in enumerate(files): py_compile.compile(str(p),cfile=str(Path(td)/f"{i}.pyc"),doraise=True)
    print(f"PASS Python syntax — {len(files)} files")


def hygiene_proof():
    bad=[]
    for p in ROOT.rglob("*"):
        rel=p.relative_to(ROOT)
        if any(part in {"__MACOSX","node_modules",".pytest_cache","__pycache__","dist","site"} for part in rel.parts): bad.append(str(rel))
        if p.name==".DS_Store" or p.suffix in {".pyc",".pyo"}: bad.append(str(rel))
    assert not bad, f"repository hygiene failures: {bad[:8]}"
    print("PASS repository hygiene")


def manifest_proof():
    count=verify_manifest(ROOT,exact=True); print(f"PASS course manifest — {count} exact payload files")


def docs_build():
    if not shutil.which("mkdocs"): raise SystemExit("mkdocs not available; install requirements-docs.txt")
    run(["mkdocs","build","--strict"]); print("PASS strict documentation build")


def clean():
    for name in [".pytest_cache","__pycache__","dist","site"]:
        for p in ROOT.rglob(name):
            if p.is_dir(): shutil.rmtree(p,ignore_errors=True)
    for p in ROOT.rglob("*.pyc"): p.unlink(missing_ok=True)
    print("PASS clean")


def module_proof(number: int):
    mapping={1:[catalog_proof],2:[catalog_proof],3:[contract_proof,registry_proof],4:[governance_proof],5:[lifecycle_proof],6:[template_proof],7:[documentation_proof,sandbox_proof],8:[sdk_proof],9:[runtime_proof,analytics_proof,support_proof],10:[release_proof,final_defense_proof]}
    for fn in mapping[number]: fn()
    report={"module":number,"status":"pass","proofs":[fn.__name__ for fn in mapping[number]]}
    (ROOT/"reports").mkdir(exist_ok=True); (ROOT/"reports"/f"module-{number:02d}-proof.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(f"PASS module {number:02d}")


def core_proof():
    funcs=[predecessor_proof,structure_proof,contract_proof,catalog_proof,registry_proof,governance_proof,lifecycle_proof,template_proof,documentation_proof,sandbox_proof,sdk_proof,runtime_proof,analytics_proof,support_proof,release_proof,migration_proof,vector_proof,python_proof,typescript_proof,network_lab_proof,planted_defect_proof,final_defense_proof,data_format_proof,markdown_link_proof,education_proof,snippet_proof,python_syntax_proof,hygiene_proof]
    for fn in funcs: fn()
    print("PASS Course 10 dependency-light core proof")


def full_proof():
    core_proof(); docs_build()


COMMANDS={
"doctor":doctor,"predecessor-proof":predecessor_proof,"orientation-proof":orientation_proof,"structure-proof":structure_proof,
"contract-proof":contract_proof,"catalog-proof":catalog_proof,"registry-proof":registry_proof,"governance-proof":governance_proof,"policy-proof":governance_proof,
"lifecycle-proof":lifecycle_proof,"template-proof":template_proof,"documentation-proof":documentation_proof,"docs-proof":documentation_proof,"sandbox-proof":sandbox_proof,
"sdk-proof":sdk_proof,"runtime-proof":runtime_proof,"analytics-proof":analytics_proof,"support-proof":support_proof,"release-proof":release_proof,
"migration-proof":migration_proof,"vector-proof":vector_proof,"python-proof":python_proof,"typescript-proof":typescript_proof,"network-lab-proof":network_lab_proof,
"planted-defect-proof":planted_defect_proof,"final-defense-proof":final_defense_proof,"capstone-tour":capstone_tour,"data-format-proof":data_format_proof,
"markdown-link-proof":markdown_link_proof,"education-proof":education_proof,"snippet-proof":snippet_proof,"python-syntax-proof":python_syntax_proof,"hygiene-proof":hygiene_proof,
"manifest-proof":manifest_proof,"docs-build":docs_build,"clean":clean,"core-proof":core_proof,"full-proof":full_proof,
}
for i in range(1,11): COMMANDS[f"module-{i:02d}-proof"]=(lambda n=i: module_proof(n))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=sorted(COMMANDS)); args=parser.parse_args(); COMMANDS[args.command]()

if __name__=="__main__": main()
