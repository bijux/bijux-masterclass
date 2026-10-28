#!/usr/bin/env python3
"""Proof and learner utility routes for Course 8."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
import tomllib
from urllib.parse import unquote

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyYAML is required for dependency-light proofs: {exc}")

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capstone"
PY_TRACK = CAP / "tracks/python-distributed"
PY_SRC = PY_TRACK / "src"
TS_TRACK = CAP / "tracks/typescript-distributed"
BOOK = ROOT / "course-book"

EXCLUDED_DIRS = {
    ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "__pycache__",
    "node_modules", "dist", "site", ".tmp",
}
ROOT_MANIFEST_NAMES = {"MANIFEST.json", "MANIFEST.sha256"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def run(
    cmd: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    merged["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        merged.update(env)
    print("+", " ".join(cmd))
    return subprocess.run(
        cmd, cwd=cwd, env=merged, check=True, text=True,
        capture_output=capture,
    )


def read_json(path: Path):
    return json.loads(path.read_text())


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def eligible(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
        return False
    if len(relative.parts) == 1 and path.name in ROOT_MANIFEST_NAMES:
        return False
    return path.is_file()


def verify_manifest(directory: Path, *, exact: bool = True) -> int:
    manifest_path = directory / "MANIFEST.json"
    digest_path = directory / "MANIFEST.sha256"
    assert manifest_path.is_file(), f"missing manifest: {manifest_path}"
    assert digest_path.is_file(), f"missing manifest digest: {digest_path}"
    expected_digest = digest_path.read_text().split()[0]
    assert sha256(manifest_path) == expected_digest, "manifest digest mismatch"
    manifest = read_json(manifest_path)
    expected_paths: set[str] = set()
    for item in manifest["files"]:
        relative = item["path"]
        expected_paths.add(relative)
        path = directory / relative
        assert path.is_file(), f"missing manifest file: {relative}"
        assert path.stat().st_size == item["size"], f"size mismatch: {relative}"
        assert sha256(path) == item["sha256"], f"digest mismatch: {relative}"
    if "file_count" in manifest:
        assert manifest["file_count"] == len(expected_paths)
    if exact:
        actual_paths = {
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*") if eligible(path, directory)
        }
        assert actual_paths == expected_paths, (
            f"manifest inventory mismatch; missing={sorted(expected_paths-actual_paths)[:8]} "
            f"unlisted={sorted(actual_paths-expected_paths)[:8]}"
        )
    return len(expected_paths)


def import_reference():
    sys.path.insert(0, str(PY_SRC))
    from distributed_api.boundary import BoundaryCandidate, decision
    from distributed_api.capability import CapabilityAuthority, CapabilityClaims
    from distributed_api.catalog import ServiceCatalog, ServiceDefinition
    from distributed_api.consistency import VersionedProjection
    from distributed_api.extraction import ExtractionPhase, StranglerRouter
    from distributed_api.model import RequestContext, Unauthorized, ValidationError
    from distributed_api.reconciliation import reconcile
    from distributed_api.release import VersionPolicy
    from distributed_api.routing import Instance, ServiceRegistry
    from distributed_api.saga import ArtifactCompletionSaga, SagaState
    from distributed_api.services import AnalysisControlService, ArtifactService, NotificationService
    from distributed_api.topology import DependencyGraph, SyncEdge
    from distributed_api.tour import run_tour
    return locals()


def doctor() -> None:
    print("python", sys.version.split()[0])
    for tool in ["node", "tsc", "mkdocs", "docker", "kubectl", "psql"]:
        print(f"{tool}: {shutil.which(tool) or 'not-available'}")
    print("PyYAML", yaml.__version__)
    print("course", read_json(ROOT / "course.json")["versionState"])


def predecessor_proof() -> None:
    count = verify_manifest(CAP / "predecessor/handoff", exact=True)
    assert count == 46, f"expected Course 7 handoff of 46 files, got {count}"
    boundary = read_json(CAP / "predecessor/handoff/BOUNDARY.json")
    assert boundary["from_course"].startswith("07-")
    assert boundary["to_course"].startswith("08-")
    print(f"PASS predecessor handoff — {count} exact files")


def structure_proof() -> None:
    pages = sorted(BOOK.rglob("*.md"))
    assert len(pages) == 61, f"expected 61 course-book pages, got {len(pages)}"
    module_dirs = sorted(p for p in BOOK.glob("module-[0-9][0-9]-*") if p.is_dir())
    assert len(module_dirs) == 11, f"expected orientation plus 10 modules, got {len(module_dirs)}"
    numbered = [p for p in module_dirs if not p.name.startswith("module-00-")]
    required = {"index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"}
    exercises = answers = 0
    for directory in numbered:
        assert {p.name for p in directory.glob("*.md")} == required, f"module shape mismatch: {directory.name}"
        ex_text = (directory / "exercises.md").read_text()
        ans_text = (directory / "exercise-answers.md").read_text()
        ex_heads = re.findall(r"^## (\d+)\. (.+)$", ex_text, re.M)
        ans_heads = re.findall(r"^## (\d+)\. (.+)$", ans_text, re.M)
        assert ex_heads == ans_heads, f"exercise/answer mismatch: {directory.name}"
        assert len(ex_heads) == 12, f"expected 12 exercises: {directory.name}"
        exercises += len(ex_heads)
        answers += len(ans_heads)
        lab = (directory / "lab.md").read_text()
        for heading in [
            "## Objective", "## Why this lab matters", "## Setup conditions",
            "## Hypothesis", "## Controlled action and investigation",
            "## Operational oracle", "## Required evidence",
            "## Interpretation and defense", "## Cleanup and reset",
            "## Completion gate",
        ]:
            assert heading in lab, f"missing {heading}: {directory.name}/lab.md"
        checkpoint = (directory / "checkpoint.md").read_text()
        for heading in ["## Required result", "## Demonstrate", "## Commands",
                           "## Evidence to retain", "## Defend the design", "## Continue only when"]:
            assert heading in checkpoint, f"missing {heading}: {directory.name}/checkpoint.md"
    assert exercises == answers == 120
    print("PASS course structure — 61 pages, 120 exercises, 120 worked answers, 10 labs")


def boundary_proof() -> None:
    data = read_yaml(CAP / "architecture/boundary-scorecard.yaml")
    candidates = {x["capability"]: x for x in data["candidates"]}
    assert candidates["Notification Delivery"]["decision"] == "extract-first"
    assert candidates["Artifact Delivery"]["decision"] == "extract-second"
    assert candidates["Analysis Control"]["decision"] == "keep-cohesive"
    assert candidates["Worker Plane"]["decision"] == "separate-deployment-not-data-owner"
    assert candidates["Project CRUD"]["decision"] == "reject"
    assert candidates["Idempotency Service"]["decision"] == "reject"
    ref = import_reference()
    notification = ref["BoundaryCandidate"]("notification", 2, 2, 2, 1, 2, 1, 1, 0)
    table = ref["BoundaryCandidate"]("project-table", 1, 0, 0, 0, 0, 0, 1, 2)
    assert ref["decision"](notification) == "extract"
    assert ref["decision"](table) == "reject"
    report = read_json(ROOT / "reports/module-01-boundary-proof.json")
    assert report["status"] == "pass" and "idempotency-service" in report["rejected"]
    print("PASS boundary proof — evidence approves 2 extractions and rejects table-shaped services")


def ownership_proof() -> None:
    catalog = read_yaml(CAP / "architecture/service-catalog.yaml")
    services = catalog["services"]
    names = [s["name"] for s in services]
    assert len(names) == len(set(names)) == 5
    assert all(s["owner"] for s in services)
    gateway = next(s for s in services if s["name"] == "edge-gateway")
    worker = next(s for s in services if s["name"] == "worker-plane")
    assert gateway["data_owner"] is False and worker["data_owner"] is False
    assert "project-service" in catalog["rejected_services"]
    ownership = read_yaml(CAP / "architecture/data-ownership.yaml")
    facts = [x["fact"] for x in ownership["facts"]]
    assert len(facts) == len(set(facts)) == 8
    assert all(x["writer"] in names for x in ownership["facts"])
    ref = import_reference()
    service_catalog = ref["ServiceCatalog"]()
    for service in services:
        owned = frozenset(x["fact"] for x in ownership["facts"] if x["writer"] == service["name"])
        service_catalog.add(ref["ServiceDefinition"](
            service["name"], service["owner"], service["kind"], owned,
            frozenset(service.get("interfaces", [])),
        ))
    service_catalog.validate_single_writers()
    service_catalog.validate_no_table_services()
    assert service_catalog.owner_of("analysis-run") == "analysis-control"
    assert service_catalog.owner_of("artifact") == "artifact-service"
    report = read_json(ROOT / "reports/module-02-ownership-proof.json")
    assert report["duplicate_writers"] == [] and report["ownerless_services"] == []
    print("PASS ownership proof — 5 components, 8 facts, exactly one writer per fact")


def data_proof() -> None:
    ownership = read_yaml(CAP / "architecture/data-ownership.yaml")
    assert "no service reads another service private database" in ownership["rules"]
    consistency = read_yaml(CAP / "architecture/consistency-policy.yaml")
    views = {x["name"]: x for x in consistency["views"]}
    assert views["notification-run-view"]["gap_policy"] == "pause-and-replay"
    assert views["control-artifact-reference"]["guarantee"] == "monotonic-versioned"
    ref = import_reference()
    projection = ref["VersionedProjection"]()
    assert projection.apply("run-1", 1, {"state": "queued"}, now_ms=0) == "apply"
    assert projection.apply("run-1", 1, {"state": "queued"}, now_ms=1) == "duplicate"
    assert projection.apply("run-1", 3, {"state": "done"}, now_ms=2) == "gap"
    try:
        projection.get("run-1", now_ms=3, max_staleness_ms=100)
    except ref["ValidationError"]:
        pass
    else:
        raise AssertionError("projection with a gap must not be served")
    report = read_json(ROOT / "reports/module-03-data-proof.json")
    assert report["cross_service_database_reads"] == 0
    assert report["uncontrolled_dual_writes"] == 0
    print("PASS data proof — owner-local writes, versioned views, gap detection, staleness policies")


def dependency_proof() -> None:
    data = read_yaml(CAP / "architecture/dependency-graph.yaml")
    ref = import_reference()
    graph = ref["DependencyGraph"]([
        ref["SyncEdge"](edge["from"], edge["to"], edge["purpose"], edge["max_budget_ms"])
        for edge in data["synchronous_edges"]
    ])
    forbidden = {(edge["from"], edge["to"]) for edge in data["forbidden_edges"]}
    graph.validate(max_public_depth=data["max_public_sync_depth"], forbidden=forbidden)
    assert graph.cycle() is None
    assert graph.longest_depth("edge-gateway") == 1  # declared public edges are direct
    assert all(edge["max_budget_ms"] > 0 for edge in data["synchronous_edges"])
    report = read_json(ROOT / "reports/module-04-dependency-proof.json")
    assert report["cycles"] == [] and report["public_sync_depth"] <= report["maximum_public_sync_depth"]
    partial = read_json(ROOT / "reports/module-04-partial-response.json")
    assert partial["partial"] is True and partial["silent_empty_list"] is False
    print("PASS dependency proof — acyclic graph, bounded depth, positive edge budgets, truthful partiality")


def saga_proof() -> None:
    data = read_yaml(CAP / "architecture/saga-catalog.yaml")
    saga_def = data["sagas"][0]
    assert saga_def["owner"] == "analysis-control-process-manager"
    assert len(saga_def["steps"]) == 5
    assert "compensated" in saga_def["terminal_states"]
    ref = import_reference()
    saga = ref["ArtifactCompletionSaga"]("saga-1", "run-1", "attempt-1")
    assert saga.record_artifact(event_id="event-1", artifact_id="artifact-1", attempt_id="attempt-1") == "stored"
    assert saga.record_artifact(event_id="event-1", artifact_id="artifact-1", attempt_id="attempt-1") == "duplicate"
    assert saga.complete(command_id="complete-1", current_attempt_id="attempt-1") == "completed"
    stale = ref["ArtifactCompletionSaga"]("saga-2", "run-2", "attempt-2")
    assert stale.record_artifact(event_id="event-2", artifact_id="artifact-2", attempt_id="attempt-old") == "compensate"
    assert stale.compensate(action_id="orphan-2") == "compensated"
    report = read_json(ROOT / "reports/module-05-saga-proof.json")
    assert report["response_loss_schedule_passed"] is True
    print("PASS saga proof — durable identities, duplicate tolerance, stale-attempt compensation")


def reconciliation_proof() -> None:
    ref = import_reference()
    assert ref["reconcile"](
        control_artifact_refs={"artifact-1"}, artifact_ids={"artifact-1"},
        completed_runs={"run-1"}, notification_run_ids={"run-1"},
    ) == []
    findings = ref["reconcile"](
        control_artifact_refs=set(), artifact_ids={"artifact-orphan"},
        completed_runs={"run-missing"}, notification_run_ids=set(),
    )
    assert findings == ["orphan-artifact:artifact-orphan", "missing-notification:run-missing"]
    report = read_json(ROOT / "reports/module-05-reconciliation.json")
    assert report["unexplained_findings"] == 0 and report["read_only_comparison"] is True
    print("PASS reconciliation proof — clean path and deterministic missing/orphan findings")


def security_proof() -> None:
    policy = read_yaml(CAP / "architecture/security-policy.yaml")
    assert "zero implicit network trust" in policy["principles"]
    assert "x-user-id as authority" in policy["forbidden"]
    upload = next(x for x in policy["capabilities"] if x["name"] == "artifact-upload")
    assert upload["audience"] == "artifact-service"
    assert {"tenant", "run", "attempt", "sha256", "max_bytes", "expires_at"}.issubset(upload["claims"])
    ref = import_reference()
    authority = ref["CapabilityAuthority"](issuer="analysis-control", key=b"0123456789abcdef0123456789abcdef")
    claims = ref["CapabilityClaims"](
        jti="upload:run-1:attempt-1:abc", issuer="analysis-control",
        audience="artifact-service", subject="learner", tenant="tenant-a",
        resource="run-1", action="artifact:upload", issued_at=10, expires_at=20,
        sha256="abc", max_bytes=1024,
    )
    token = authority.mint(claims)
    vector = read_json(CAP / "shared/vectors/capability.json")
    assert token == vector["interoperability"]["expected_token"]
    profile = read_yaml(CAP / "security/capability-profile.yaml")
    assert profile["profile"] == "artifact-capability-1.0"
    assert profile["status"] == "course-specific"
    assert authority.verify(token, audience="artifact-service", tenant="tenant-a", action="artifact:upload", now=11).resource == "run-1"
    for bad in [
        {"audience": "analysis-control", "tenant": "tenant-a", "action": "artifact:upload", "now": 11},
        {"audience": "artifact-service", "tenant": "tenant-b", "action": "artifact:upload", "now": 11},
        {"audience": "artifact-service", "tenant": "tenant-a", "action": "artifact:upload", "now": 21},
    ]:
        try:
            authority.verify(token, **bad)
        except ref["Unauthorized"]:
            pass
        else:
            raise AssertionError(f"capability should be rejected: {bad}")
    report = read_json(ROOT / "reports/module-06-security-proof.json")
    assert report["trusted_identity_headers"] is False and report["cross_tenant_cases_rejected"] is True
    print("PASS security proof — workload trust separated from narrow tenant/effect capability")


def routing_proof() -> None:
    ref = import_reference()
    registry = ref["ServiceRegistry"]()
    registry.register(ref["Instance"]("artifact-a", "artifact-service", "1.0"))
    registry.register(ref["Instance"]("artifact-b", "artifact-service", "1.0"))
    assert [registry.choose("artifact-service").instance_id for _ in range(3)] == ["artifact-a", "artifact-b", "artifact-a"]
    registry.set_health("artifact-service", "artifact-a", False)
    assert registry.choose("artifact-service").instance_id == "artifact-b"
    compose = read_yaml(CAP / "topology/compose.yaml")
    assert "services" in compose and len(compose["services"]) >= 5
    network_documents = list(yaml.safe_load_all((CAP / "topology/kubernetes/network-policy.yaml").read_text()))
    assert all(document["kind"] == "NetworkPolicy" for document in network_documents)
    report = read_json(ROOT / "reports/module-07-routing-proof.json")
    assert report["gateway_business_state"] is False and report["shadow_side_effects_suppressed"] is True
    print("PASS routing proof — healthy selection, topology declarations, edge without business authority")


def release_proof() -> None:
    policy = read_yaml(CAP / "architecture/release-policy.yaml")
    assert len(policy["supported_skew"]) == 5
    ref = import_reference()
    versions = ref["VersionPolicy"]()
    expected = {
        ("1.0", "1.0"): "compatible",
        ("1.0", "1.1"): "compatible",
        ("1.1", "1.0"): "compatible-with-feature-disabled",
        ("2.0", "1.1"): "reject",
    }
    for pair, classification in expected.items():
        assert versions.classify(*pair) == classification
    accepted = read_json(CAP / "releases/distributed-1.0/release-report.json")
    assert accepted["decision"] == "accepted"
    assert all(value == "pass" for value in accepted["gates"].values())
    rejected = sorted((CAP / "releases").glob("rejected-*/candidate.json"))
    assert len(rejected) == 10
    assert all(read_json(path)["expected"] == "reject" for path in rejected)
    report = read_json(ROOT / "reports/module-08-release-proof.json")
    assert report["rollback_target_present"] is True and report["owner_local_migrations"] is True
    print("PASS release proof — supported skew, accepted profile, 10 rejected candidates")


def extraction_proof() -> None:
    plan = read_yaml(CAP / "architecture/extraction-plan.yaml")
    phases = [x["n"] for x in plan["phases"]]
    assert phases == list(range(7))
    assert plan["retained"] == "analysis-control remains cohesive"
    assert len(plan["merge_back_trigger"]) >= 3
    ref = import_reference()
    clean = ref["StranglerRouter"](lambda value: value * 2, lambda value: value * 2)
    clean.transition(ref["ExtractionPhase"].SHADOW)
    assert clean.call("tenant-a", 3) == 6 and clean.shadow_clean()
    clean.transition(ref["ExtractionPhase"].CANARY, canary_fraction=0.5)
    assert clean.call("tenant-a", 4) == 8
    clean.transition(ref["ExtractionPhase"].CUTOVER)
    assert clean.call("tenant-a", 5) == 10
    divergent = ref["StranglerRouter"](lambda value: value, lambda value: value + 1)
    divergent.transition(ref["ExtractionPhase"].SHADOW)
    divergent.call("tenant-a", 1)
    assert not divergent.shadow_clean()
    print("PASS extraction proof — ordered phases, clean shadow, bounded canary, rollback-aware cutover")


def migration_proof() -> None:
    legacy = sorted((CAP / "database/legacy").glob("*.sql"))
    legacy_numbers = [path.name.split("_", 1)[0] for path in legacy]
    assert legacy_numbers == [f"{n:03d}" for n in range(1, 16)]
    expected = {
        "analysis-control": ["001"],
        "artifact-service": ["001", "002"],
        "notification-service": ["001", "002"],
        "platform-catalog": ["001"],
    }
    for service, numbers in expected.items():
        found = [path.name.split("_", 1)[0] for path in sorted((CAP / f"database/{service}/migrations").glob("*.sql"))]
        assert found == numbers, f"migration head mismatch for {service}: {found}"
    ledger = read_yaml(CAP / "architecture/version-ledger.yaml")
    assert ledger["legacy_migration_head"] == "015"
    assert ledger["service_migration_heads"] == {k: v[-1] for k, v in expected.items()}
    print("PASS migration proof — legacy 001–015 and four owner-local histories")


def vector_proof() -> None:
    files = sorted((CAP / "shared/vectors").glob("*.json"))
    assert len(files) == 10
    total = 0
    for path in files:
        data = read_json(path)
        cases = data["cases"]
        ids = [case["id"] for case in cases]
        assert ids and len(ids) == len(set(ids)), f"empty or duplicate vector IDs: {path.name}"
        total += len(ids)
    shared_capability = CAP / "shared/vectors/capability.json"
    typescript_fixture = (
        CAP / "tracks/typescript-distributed/test-js/fixtures/capability.json"
    )
    assert shared_capability.read_bytes() == typescript_fixture.read_bytes(), (
        "TypeScript capability fixture diverges from the shared vector"
    )
    print(f"PASS shared vectors — {len(files)} files, {total} cases")


def python_proof() -> None:
    env = {"PYTHONPATH": str(PY_SRC), "PYTHONDONTWRITEBYTECODE": "1"}
    result = run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=PY_TRACK, env=env, capture=True,
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    assert "OK" in result.stderr or "OK" in result.stdout
    print("PASS Python reference suite")


def _copy_ts_track(destination: Path) -> Path:
    target = destination / "typescript-distributed"
    shutil.copytree(TS_TRACK, target, ignore=shutil.ignore_patterns("dist", "node_modules"))
    return target


def typescript_proof() -> None:
    assert shutil.which("node"), "node is required"
    assert shutil.which("tsc"), "tsc is required"
    with tempfile.TemporaryDirectory(prefix="course8-ts-") as tmp:
        track = _copy_ts_track(Path(tmp))
        run(["tsc", "-p", "tsconfig.json"], cwd=track)
        result = run(["node", "--test", "test-js/*.test.mjs"], cwd=track, capture=True)
        # Shell expansion is not applied in subprocess; rerun with explicit paths when needed.
        if result.returncode != 0:  # pragma: no cover; check=True normally raises
            raise AssertionError(result.stderr)
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
    print("PASS TypeScript reference compilation and tests")


def _typescript_proof_explicit() -> None:
    assert shutil.which("node"), "node is required"
    assert shutil.which("tsc"), "tsc is required"
    with tempfile.TemporaryDirectory(prefix="course8-ts-") as tmp:
        track = _copy_ts_track(Path(tmp))
        run(["tsc", "-p", "tsconfig.json"], cwd=track)
        tests = [str(path.relative_to(track)) for path in sorted((track / "test-js").glob("*.test.mjs"))]
        result = run(["node", "--test", *tests], cwd=track, capture=True)
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
    print("PASS TypeScript reference compilation and tests")

# Use explicit test paths; kept as a separate function to avoid shell-glob assumptions.
typescript_proof = _typescript_proof_explicit


def distributed_proof() -> None:
    ref = import_reference()
    result = ref["run_tour"]()
    assert result["state"] == "completed"
    assert result["delivery_count"] == 1
    assert result["reconciliation"] == []
    accepted = read_json(CAP / "final-defense/architecture-summary.json")
    assert accepted["sync_cycles"] == 0 and accepted["shared_databases"] == 0
    print("PASS distributed outcome proof — completed run, one artifact, one delivery, clean reconciliation")


def planted_defect_proof() -> None:
    defects = sorted((CAP / "planted-defects").glob("*/defect.json"))
    assert len(defects) == 10
    release_gates = {
        read_json(path)["candidate"]: read_json(path)["rejecting_gate"]
        for path in (CAP / "releases").glob("rejected-*/candidate.json")
    }
    for path in defects:
        defect = read_json(path)
        assert defect["expected"] == "reject"
        assert defect["rejecting_gate"] in {
            "boundary-evidence", "single-writer-ownership", "acyclic-sync-graph",
            "dependency-budget", "saga-recovery", "service-auth", "version-skew",
            "operability",
        }
        assert release_gates[defect["candidate"]] == defect["rejecting_gate"]
    report = read_json(ROOT / "reports/module-09-distributed-proof.json")
    assert report["planted_defects_rejected"] == 10
    print("PASS planted-defect proof — 10 defects mapped to rejecting gates")


def final_defense_proof() -> None:
    summary = read_json(CAP / "final-defense/architecture-summary.json")
    assert summary == {
        "business_services": 3,
        "compute_planes": 1,
        "edge_components": 1,
        "extracted": ["notification-service", "artifact-service"],
        "max_public_sync_depth": 2,
        "outcome": "accepted",
        "retained": ["analysis-control"],
        "services": 5,
        "shared_databases": 0,
        "sync_cycles": 0,
    }
    report = read_json(ROOT / "reports/module-10-final-defense.json")
    assert report["status"] == "pass" and report["decommission_plan"] == "present"
    assert (CAP / "architecture/adr/0001-keep-analysis-control-cohesive.md").is_file()
    assert (CAP / "architecture/adr/0002-extract-notification-first.md").is_file()
    assert (CAP / "architecture/adr/0003-extract-artifact-second.md").is_file()
    print("PASS final architecture defense — extracted 2, retained 1, rejected weak boundaries")


def handoff_proof() -> None:
    count = verify_manifest(CAP / "handoff", exact=True)
    boundary = read_json(CAP / "handoff/BOUNDARY.json")
    assert boundary["from_course"].startswith("08-")
    assert boundary["to_course"].startswith("09-")
    brief = read_yaml(CAP / "handoff/graphql-boundary-brief.yaml")
    assert "direct database joins across services" in brief["forbidden"]
    assert "traceable service fan-out" in brief["required_controls"]
    print(f"PASS Course 9 handoff — {count} exact files and graph boundary brief")


class DuplicateKeyError(ValueError):
    pass


def _json_no_duplicates(path: Path) -> None:
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateKeyError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result
    json.loads(path.read_text(), object_pairs_hook=hook)


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError(f"duplicate YAML key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping,
)


def data_format_proof() -> None:
    json_count = yaml_count = toml_count = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix == ".json":
            _json_no_duplicates(path)
            json_count += 1
        elif path.suffix in {".yaml", ".yml"}:
            list(yaml.load_all(path.read_text(), Loader=UniqueKeyLoader))
            yaml_count += 1
        elif path.suffix == ".toml":
            tomllib.loads(path.read_text())
            toml_count += 1
    print(f"PASS data formats — JSON {json_count}, YAML {yaml_count}, TOML {toml_count}")


def markdown_link_proof() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    checked = 0
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text()
        for raw in pattern.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#", "sandbox:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            assert resolved.exists(), f"broken Markdown link in {path.relative_to(ROOT)}: {raw}"
            checked += 1
    print(f"PASS local Markdown links — {checked} targets")


def education_proof() -> None:
    pages = sorted(BOOK.rglob("*.md"))
    total_words = sum(len(path.read_text().split()) for path in pages)
    assert total_words >= 35_000, f"course book too thin: {total_words} words"
    main_chapters = sorted(BOOK.glob("module-[0-9][1-9]-*/index.md")) + sorted(BOOK.glob("module-10-*/index.md"))
    assert len(main_chapters) == 10
    for path in main_chapters:
        words = len(path.read_text().split())
        assert words >= 1_600, f"main chapter too thin ({words} words): {path.parent.name}"
        text = path.read_text()
        assert "## Learning outcomes" in text
        assert "## Capstone increment" in text
        assert "## Python and TypeScript implications" in text
    forbidden = ["lorem ipsum", "write something here", "coming soon", "to be completed", "placeholder text"]
    combined = "\n".join(path.read_text().lower() for path in pages)
    for phrase in forbidden:
        assert phrase not in combined, f"unfinished learner content: {phrase}"
    # Reject long copied prose blocks across several pages.
    blocks: Counter[str] = Counter()
    for path in pages:
        paragraphs = re.split(r"\n\s*\n", path.read_text())
        for paragraph in paragraphs:
            normalized = re.sub(r"\s+", " ", paragraph.strip())
            if len(normalized.split()) >= 45:
                blocks[normalized] += 1
    repeated = [(count, block[:90]) for block, count in blocks.items() if count >= 4]
    assert not repeated, f"repeated long learner prose: {repeated[:3]}"
    print(f"PASS educational quality — {len(pages)} pages, {total_words} words, 10 deep chapters")


def python_syntax_proof() -> None:
    files = sorted(ROOT.rglob("*.py"))
    for path in files:
        compile(path.read_text(), str(path), "exec")
    print(f"PASS Python syntax — {len(files)} files")


def hygiene_proof() -> None:
    forbidden_names = {".DS_Store", "Thumbs.db"}
    forbidden_dirs = {"__MACOSX", "node_modules", "dist", "site", "__pycache__", ".pytest_cache"}
    bad = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.name in forbidden_names or any(part in forbidden_dirs for part in relative.parts):
            bad.append(relative.as_posix())
        if path.is_file() and path.suffix in {".pyc", ".pyo"}:
            bad.append(relative.as_posix())
    assert not bad, f"repository hygiene violations: {bad[:12]}"
    print("PASS repository hygiene")


def capstone_tour() -> None:
    ref = import_reference()
    result = ref["run_tour"]()
    print(json.dumps(result, indent=2, sort_keys=True))
    assert result["state"] == "completed" and result["reconciliation"] == []
    if shutil.which("node") and shutil.which("tsc"):
        with tempfile.TemporaryDirectory(prefix="course8-tour-") as tmp:
            track = _copy_ts_track(Path(tmp))
            run(["tsc", "-p", "tsconfig.json"], cwd=track)
            ts_result = run(["node", "dist/src/tour.js"], cwd=track, capture=True)
            print(ts_result.stdout.strip())
    print("PASS capstone tour")



def network_lab_proof() -> None:
    lab = CAP / "network-lab"
    env = {
        "PYTHONPATH": os.pathsep.join([str(PY_SRC), str(lab)]),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    result = run(
        [sys.executable, "-m", "network_lab.tour"],
        cwd=lab,
        env=env,
        capture=True,
    )
    data = json.loads(result.stdout)
    assert data["services_started"] == 5
    assert data["remote_calls_exercised"] is True
    assert data["event_relay_simulated"] is True
    assert data["unauthenticated_artifact_rejected"] is True
    assert data["cross_tenant_read_rejected"] is True
    assert data["state"] == "completed"
    assert data["notification_deliveries"] == 1
    assert data["full_view_partial"] is False
    assert data["degraded_view_partial"] is True
    assert data["degraded_warnings"] == ["artifactsUnavailable"]
    print(json.dumps(data, indent=2, sort_keys=True))
    print("PASS multi-process network laboratory — five components and explicit degradation")

def manifest_proof() -> None:
    count = verify_manifest(ROOT, exact=True)
    print(f"PASS course manifest — {count} exact files")


def postgres_proof() -> None:
    if not shutil.which("psql") or not os.environ.get("TEST_DATABASE_URL"):
        raise SystemExit(
            "psql and TEST_DATABASE_URL are required for postgres-proof"
        )
    run([sys.executable, str(ROOT / "scripts/postgres_proof.py")])
    print("PASS owner-local PostgreSQL migration proof")


def docs_build() -> None:
    if not shutil.which("mkdocs"):
        raise SystemExit("mkdocs is not available; install requirements-docs.txt")
    run(["mkdocs", "build", "--strict"])
    print("PASS strict MkDocs build")


def compose_proof() -> None:
    compose = read_yaml(CAP / "topology/compose.yaml")
    assert set(compose["services"]) == {
        "analysis-control",
        "artifact-service",
        "notification-service",
        "worker-plane",
        "edge-gateway",
    }
    assert all("build" in service for service in compose["services"].values())
    if shutil.which("docker"):
        run(["docker", "compose", "-f", str(CAP / "topology/compose.yaml"), "config", "--quiet"])
        print("PASS Docker Compose native validation")
    else:
        print("NOT EXECUTED native Docker Compose validation — docker unavailable")


def kubernetes_proof() -> None:
    documents = []
    for path in sorted((CAP / "topology/kubernetes").glob("*.yaml")):
        documents.extend(yaml.safe_load_all(path.read_text()))
    assert {doc["kind"] for doc in documents} >= {"Namespace", "Deployment", "Service", "NetworkPolicy"}
    if shutil.which("kubectl"):
        for path in sorted((CAP / "topology/kubernetes").glob("*.yaml")):
            run(["kubectl", "apply", "--dry-run=client", "-f", str(path)])
        print("PASS kubectl client-side validation")
    else:
        print("NOT EXECUTED kubectl validation — kubectl unavailable")


def core_proof() -> None:
    predecessor_proof()
    structure_proof()
    boundary_proof()
    ownership_proof()
    data_proof()
    dependency_proof()
    saga_proof()
    reconciliation_proof()
    security_proof()
    routing_proof()
    release_proof()
    extraction_proof()
    migration_proof()
    vector_proof()
    python_proof()
    typescript_proof()
    distributed_proof()
    network_lab_proof()
    planted_defect_proof()
    final_defense_proof()
    handoff_proof()
    data_format_proof()
    markdown_link_proof()
    education_proof()
    python_syntax_proof()
    hygiene_proof()
    print("PASS Course 8 dependency-light core proof")


def full_proof() -> None:
    core_proof()
    compose_proof()
    kubernetes_proof()
    if shutil.which("mkdocs"):
        docs_build()
    else:
        print("NOT EXECUTED strict MkDocs build — mkdocs unavailable")
    if shutil.which("psql") and os.environ.get("TEST_DATABASE_URL"):
        postgres_proof()
    else:
        print("NOT EXECUTED live PostgreSQL proof — psql or TEST_DATABASE_URL unavailable")
    print("PASS available full-proof routes; see FINAL-VERIFICATION.md for evidence boundary")


COMMANDS = {
    "doctor": doctor,
    "predecessor-proof": predecessor_proof,
    "orientation-proof": lambda: (predecessor_proof(), boundary_proof(), python_proof(), typescript_proof()),
    "structure-proof": structure_proof,
    "boundary-proof": boundary_proof,
    "ownership-proof": ownership_proof,
    "data-proof": data_proof,
    "dependency-proof": dependency_proof,
    "saga-proof": saga_proof,
    "reconciliation-proof": reconciliation_proof,
    "security-proof": security_proof,
    "routing-proof": routing_proof,
    "release-proof": release_proof,
    "extraction-proof": extraction_proof,
    "migration-proof": migration_proof,
    "vector-proof": vector_proof,
    "python-proof": python_proof,
    "typescript-proof": typescript_proof,
    "distributed-proof": distributed_proof,
    "network-lab-proof": network_lab_proof,
    "planted-defect-proof": planted_defect_proof,
    "final-defense-proof": final_defense_proof,
    "handoff-proof": handoff_proof,
    "data-format-proof": data_format_proof,
    "markdown-link-proof": markdown_link_proof,
    "education-proof": education_proof,
    "python-syntax-proof": python_syntax_proof,
    "hygiene-proof": hygiene_proof,
    "capstone-tour": capstone_tour,
    "manifest-proof": manifest_proof,
    "postgres-proof": postgres_proof,
    "docs-build": docs_build,
    "compose-proof": compose_proof,
    "kubernetes-proof": kubernetes_proof,
    "core-proof": core_proof,
    "full-proof": full_proof,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args()
    COMMANDS[args.command]()


if __name__ == "__main__":
    main()
