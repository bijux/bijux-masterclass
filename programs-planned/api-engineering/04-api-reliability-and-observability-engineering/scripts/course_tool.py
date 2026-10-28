#!/usr/bin/env python3
"""Deterministic proof and packaging support for Course 4.

The dependency-light proof deliberately distinguishes local structural and
behavioral evidence from environment-backed PostgreSQL, telemetry-stack, and
full npm/MkDocs execution. Missing external tools are never converted into
passes.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAPSTONE = ROOT / "capstone"
PY_TRACK = CAPSTONE / "tracks" / "python-fastapi"
TS_TRACK = CAPSTONE / "tracks" / "typescript-fastify"
REPORTS = ROOT / "reports"
COURSE_ID = "api-reliability-and-observability-engineering"
COURSE_ARCHIVE_ROOT = "programs/api-engineering/04-api-reliability-and-observability-engineering"

IGNORED_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".coverage",
    "node_modules",
    "site",
    ".runtime",
    ".venv",
    "venv",
    "dist",
    "dist-core",
    "dist-security-core",
    "dist-reliability-core",
    "dist-security",
    "dist-reliability",
    "dist-audit",
}
EPHEMERAL_REPORTS = {
    "last-core-proof.json",
    "last-doctor.json",
    "last-live-proof.json",
}
HTTP_METHODS = {
    "get",
    "put",
    "post",
    "delete",
    "options",
    "head",
    "patch",
    "trace",
    "query",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL {message}")


def passed(message: str) -> None:
    print(f"PASS {message}")


def note(message: str) -> None:
    print(f"NOTE {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception as exc:  # pragma: no cover - message wrapping
        fail(f"cannot parse YAML {path.relative_to(ROOT)}: {exc}")


def _json_unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_json_unique_pairs,
        )
    except Exception as exc:  # pragma: no cover - message wrapping
        fail(f"cannot parse JSON {path.relative_to(ROOT)}: {exc}")


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> None:
    shown = " ".join(command)
    print(f"RUN  ({cwd}) {shown}")
    merged = os.environ.copy()
    if env:
        merged.update(env)
    result = subprocess.run(command, cwd=cwd, env=merged, text=True)
    if result.returncode != 0:
        fail(f"command failed ({result.returncode}): {shown}")


def run_capture(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged,
        text=True,
        capture_output=True,
    )


def clean_generated() -> None:
    for path in sorted(ROOT.rglob("*"), reverse=True):
        if path.is_dir() and path.name in IGNORED_DIRS:
            shutil.rmtree(path, ignore_errors=True)
    for path in REPORTS.glob("last-*.json"):
        path.unlink(missing_ok=True)


def doctor() -> None:
    tools: dict[str, str | None] = {}
    for executable in [
        "python3",
        "node",
        "tsc",
        "mkdocs",
        "docker",
        "psql",
        "promtool",
    ]:
        tools[executable] = shutil.which(executable)
        print(f"{executable:10} {tools[executable] or 'not-available'}")
    try:
        import fastapi  # type: ignore
        fastapi_version = getattr(fastapi, "__version__", "installed")
    except Exception:
        fastapi_version = "not-available"
    try:
        import psycopg  # type: ignore
        psycopg_version = getattr(psycopg, "__version__", "installed")
    except Exception:
        psycopg_version = "not-available"
    print(f"fastapi    {fastapi_version}")
    print(f"psycopg    {psycopg_version}")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "last-doctor.json").write_text(
        json.dumps(
            {
                "course": COURSE_ID,
                "tools": tools,
                "pythonPackages": {
                    "fastapi": fastapi_version,
                    "psycopg": psycopg_version,
                },
                "interpretation": (
                    "Unavailable external capabilities are not passes. "
                    "Use full-proof in a provisioned environment."
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    passed("environment diagnostic complete")


def verify_manifest(directory: Path, manifest_name: str = "MANIFEST.json") -> int:
    manifest_path = directory / manifest_name
    if not manifest_path.is_file():
        fail(f"manifest missing: {manifest_path.relative_to(ROOT)}")
    manifest = load_json(manifest_path)
    rows = manifest.get("files")
    if not isinstance(rows, list):
        fail(f"manifest has no files list: {manifest_path.relative_to(ROOT)}")
    listed: set[str] = set()
    missing: list[str] = []
    changed: list[str] = []
    unsafe: list[str] = []
    for entry in rows:
        relative = entry.get("path")
        if not isinstance(relative, str):
            fail("manifest entry has no path")
        pure = Path(relative)
        if pure.is_absolute() or ".." in pure.parts:
            unsafe.append(relative)
            continue
        if relative in listed:
            fail(f"duplicate manifest path {relative}")
        listed.add(relative)
        path = directory / relative
        if not path.is_file():
            missing.append(relative)
        elif path.stat().st_size != entry.get("size") or sha256(path) != entry.get("sha256"):
            changed.append(relative)
    if unsafe or missing or changed:
        fail(
            "manifest mismatch: "
            f"unsafe={unsafe[:5]} missing={missing[:5]} changed={changed[:5]}"
        )
    return len(listed)


def predecessor_proof() -> None:
    handoff = CAPSTONE / "predecessor" / "handoff"
    checksum_file = handoff / "MANIFEST.sha256"
    if not checksum_file.is_file():
        fail("Course 3 handoff checksum missing")
    expected = checksum_file.read_text(encoding="utf-8").split()[0]
    if expected != sha256(handoff / "MANIFEST.json"):
        fail("Course 3 handoff manifest checksum mismatch")
    count = verify_manifest(handoff)
    contract = handoff / "contract" / "openapi-api-1.2.bundle.yaml"
    api = load_yaml(contract)
    if api.get("info", {}).get("version") != "1.2.0":
        fail("predecessor public API is not 1.2.0")
    security = load_yaml(handoff / "security" / "security-profile.yaml")
    profile = str(security.get("profile", ""))
    if profile != "api-security-profile-1.0":
        fail("predecessor security profile is not api-security-profile-1.0")
    migration_names = sorted(p.name for p in (handoff / "migrations").glob("*.sql"))
    if [name[:3] for name in migration_names] != ["006", "007"]:
        fail("Course 3 handoff migrations 006-007 are incomplete")
    passed(
        f"Course 3 predecessor handoff — {count} exact files, API 1.2, "
        "security profile 1.0"
    )


def _index(rows: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier:
            fail(f"{label} has missing identifier")
        if identifier in result:
            fail(f"duplicate {label} identifier {identifier}")
        result[identifier] = row
    return result


def _operation_ids(contract: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for item in contract.get("paths", {}).values():
        if not isinstance(item, dict):
            continue
        for method, operation in item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            identifier = operation.get("operationId")
            if isinstance(identifier, str):
                if identifier in found:
                    fail(f"duplicate OpenAPI operationId {identifier}")
                found.add(identifier)
    return found


def reliability_case_proof() -> None:
    case = CAPSTONE / "reliability-case"
    journeys = load_yaml(case / "journeys.yaml")["journeys"]
    failures = load_yaml(case / "failure-modes.yaml")["failureModes"]
    requirements = load_yaml(case / "requirements.yaml")["requirements"]
    proofs = load_yaml(case / "proof-map.yaml")["proofs"]
    slo_catalog = load_yaml(case / "slo-catalog.yaml")
    alert_catalog = load_yaml(case / "alert-catalog.yaml")
    if str(slo_catalog.get("catalogVersion", "")) != "1.0":
        fail("SLO catalog must declare catalogVersion 1.0")
    if str(alert_catalog.get("catalogVersion", "")) != "1.0":
        fail("alert catalog must declare catalogVersion 1.0")
    slos = slo_catalog["slos"]
    alerts = alert_catalog["alerts"]
    dependencies = load_yaml(case / "dependency-policies.yaml")["dependencies"]
    risks = load_yaml(case / "residual-risks.yaml")["residualRisks"]
    trace_topology = load_yaml(
        CAPSTONE / "shared" / "contracts" / "trace-topology.yaml"
    )

    journey_by_id = _index(journeys, "journey")
    failure_by_id = _index(failures, "failure mode")
    requirement_by_id = _index(requirements, "requirement")
    slo_by_id = _index(slos, "SLO")
    alert_by_id = _index(alerts, "alert")
    dependency_by_id = _index(dependencies, "dependency")
    _index(risks, "residual risk")

    if len(journey_by_id) != 6 or len(failure_by_id) != 12 or len(requirement_by_id) != 30:
        fail(
            "reliability case inventory drifted: "
            f"journeys={len(journey_by_id)} failures={len(failure_by_id)} "
            f"requirements={len(requirement_by_id)}"
        )

    contract = load_yaml(
        CAPSTONE / "predecessor" / "handoff" / "contract" / "openapi-api-1.2.bundle.yaml"
    )
    operation_ids = _operation_ids(contract)
    for journey in journeys:
        if journey["entryOperation"] not in operation_ids:
            fail(
                f"{journey['id']} references missing OpenAPI operation "
                f"{journey['entryOperation']}"
            )
        dimensions = journey.get("reliabilityDimensions", [])
        if not dimensions or len(dimensions) != len(set(dimensions)):
            fail(f"{journey['id']} reliability dimensions are empty or duplicated")
        if not str(journey.get("success", "")).strip():
            fail(f"{journey['id']} has no observable success statement")

    source_ids = set(journey_by_id) | set(failure_by_id)
    for requirement in requirements:
        if requirement.get("source") not in source_ids:
            fail(f"{requirement['id']} references unknown source {requirement.get('source')}")
        if requirement.get("status") != "active":
            fail(f"{requirement['id']} is not active")
        if len(str(requirement.get("statement", ""))) < 25:
            fail(f"{requirement['id']} statement is not substantive")

    proof_by_requirement: dict[str, list[dict[str, Any]]] = {}
    for proof in proofs:
        requirement = proof.get("requirement")
        proof_by_requirement.setdefault(requirement, []).append(proof)
        if requirement not in requirement_by_id:
            fail(f"proof references unknown requirement {requirement}")
        evidence = ROOT / str(proof.get("evidence", ""))
        if not evidence.is_file():
            fail(f"proof evidence missing for {requirement}: {proof.get('evidence')}")
        command = str(proof.get("executable", ""))
        if not re.fullmatch(r"make module-proof MODULE=(0[1-9]|10)", command):
            fail(f"{requirement} has invalid executable proof command {command!r}")
    missing_proofs = sorted(set(requirement_by_id) - set(proof_by_requirement))
    duplicate_proofs = sorted(k for k, v in proof_by_requirement.items() if len(v) != 1)
    if missing_proofs or duplicate_proofs:
        fail(f"proof map mismatch missing={missing_proofs} duplicate={duplicate_proofs}")

    for slo in slos:
        objective = slo.get("objective")
        if not isinstance(objective, (float, int)) or not 0 < float(objective) <= 1:
            fail(f"{slo['id']} objective must be in (0,1]")
        unknown_journeys = set(slo.get("journeys", [])) - set(journey_by_id)
        if unknown_journeys:
            fail(f"{slo['id']} references unknown journeys {sorted(unknown_journeys)}")
        if not str(slo.get("indicator", "")).strip() or not str(slo.get("window", "")).strip():
            fail(f"{slo['id']} lacks indicator or window")

    runbooks = {
        load_yaml(path)["id"]
        for path in (CAPSTONE / "incident" / "runbooks").glob("*.yaml")
    }
    for alert in alerts:
        if "slo" in alert and alert["slo"] not in slo_by_id:
            fail(f"{alert['id']} references unknown SLO {alert['slo']}")
        if alert.get("runbook") not in runbooks:
            fail(f"{alert['id']} references unknown runbook {alert.get('runbook')}")
        if alert.get("severity") not in {"page", "ticket"}:
            fail(f"{alert['id']} has unsupported severity")

    for dependency in dependencies:
        if dependency.get("retryOwner") in {None, ""}:
            fail(f"{dependency['id']} has no retry owner")
        if dependency.get("readiness") and dependency.get("criticality") == "diagnostic":
            fail(f"diagnostic dependency {dependency['id']} cannot gate readiness")
        if dependency.get("circuitBreaker") is True and dependency.get("circuitScope") != "dependency":
            fail(f"{dependency['id']} circuit must be dependency-scoped")
    if dependency_by_id["otel-collector"].get("readiness") is not False:
        fail("telemetry collector incorrectly gates readiness")

    if str(trace_topology.get("topologyVersion", "")) != "1.0":
        fail("trace topology must declare topologyVersion 1.0")
    edge_ids: set[str] = set()
    for edge in trace_topology.get("edges", []):
        identifier = edge.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in edge_ids:
            fail(f"invalid or duplicate trace edge identifier {identifier!r}")
        edge_ids.add(identifier)
        kind = edge.get("kind")
        relation = edge.get("relation")
        if kind in {"durable-queue", "durable-outbox"} and relation != "link":
            fail(f"{identifier} must use a link across a durable boundary")
        if isinstance(kind, str) and kind.startswith("synchronous-") and relation != "parent-child":
            fail(f"{identifier} must use parent-child for a synchronous edge")
    if len(edge_ids) < 7:
        fail("trace topology is incomplete")

    passed(
        "reliability case — 6 journeys, 12 failure modes, 30 requirements, "
        f"{len(slo_by_id)} SLOs, {len(alert_by_id)} alerts"
    )


def _iter_case_rows(node: Any, path: str = "") -> Iterator[tuple[str, dict[str, Any]]]:
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else key
            if isinstance(value, list) and key.lower().endswith("cases"):
                for row in value:
                    if isinstance(row, dict):
                        yield child, row
            yield from _iter_case_rows(value, child)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _iter_case_rows(value, f"{path}[{index}]")


def data_proof() -> None:
    counts = Counter()
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        suffix = path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            load_yaml(path)
            counts["yaml"] += 1
        elif suffix == ".json":
            load_json(path)
            counts["json"] += 1
        elif suffix == ".toml":
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(f"cannot parse TOML {path.relative_to(ROOT)}: {exc}")
            counts["toml"] += 1
    passed(
        "duplicate-key-aware data parsing — "
        f"{counts['yaml']} YAML, {counts['json']} JSON, {counts['toml']} TOML"
    )


def vector_proof() -> None:
    vector_dir = CAPSTONE / "shared" / "vectors"
    total = 0
    identifiers: dict[str, str] = {}
    files = 0
    for path in sorted(vector_dir.glob("*.json")):
        files += 1
        data = load_json(path)
        local_count = 0
        for location, row in _iter_case_rows(data):
            identifier = row.get("id")
            if not isinstance(identifier, str) or not identifier:
                fail(f"{path.name}:{location} case has no identifier")
            compound = f"{path.name}:{identifier}"
            if compound in identifiers:
                fail(f"duplicate vector case {compound}")
            identifiers[compound] = location
            local_count += 1
        if local_count == 0:
            # Some vector documents use top-level scenario records rather than a
            # *Cases array. They remain parsed and are exercised by tests.
            if not isinstance(data, dict) or not data:
                fail(f"empty vector document {path.name}")
        total += local_count
    if files < 18 or total < 90:
        fail(f"shared vector corpus unexpectedly small: files={files} cases={total}")
    passed(f"shared cross-course vectors — {files} files, {total} identified cases")


def migration_proof() -> None:
    own = sorted((CAPSTONE / "migrations").glob("*.sql"))
    if [p.name[:3] for p in own] != ["008"]:
        fail("Course 4 must own exactly migration 008")
    expected_versions = [f"{value:03d}" for value in range(1, 9)]
    hashes_by_track: dict[str, list[str]] = {}
    for track in [PY_TRACK, TS_TRACK]:
        migrations = sorted((track / "migrations").glob("*.sql"))
        versions = [p.name[:3] for p in migrations]
        if versions != expected_versions:
            fail(f"{track.name} migration history is {versions}, expected {expected_versions}")
        hashes_by_track[track.name] = [sha256(path) for path in migrations]
    if hashes_by_track[PY_TRACK.name] != hashes_by_track[TS_TRACK.name]:
        fail("Python and TypeScript migration histories differ")
    if sha256(own[0]) != sha256(PY_TRACK / "migrations" / own[0].name):
        fail("Course 4 migration 008 differs from executable track")
    sql = own[0].read_text(encoding="utf-8")
    for required in [
        "operational_reconciliation_runs",
        "operational_repair_actions",
        "repair_key text PRIMARY KEY",
        "before_state jsonb",
        "after_state jsonb",
    ]:
        if required not in sql:
            fail(f"migration 008 missing {required}")
    passed("migration history — immutable, byte-identical revisions 001-008")


def _pytest_directory(directory: str) -> None:
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    run(
        [sys.executable, "-m", "pytest", "-q", directory],
        cwd=PY_TRACK,
        env=env,
    )


def python_proof(module: str | None = None) -> None:
    module_files = {
        "02": [
            "tests_reliability/test_context_deadline.py",
            "tests_reliability/test_retry_circuit.py",
            "tests_reliability/test_shared_vectors.py",
        ],
        "03": [
            "tests_reliability/test_retry_circuit.py",
            "tests_reliability/test_operational_primitives.py",
        ],
        "04": [
            "tests_reliability/test_metrics_health.py",
            "tests_reliability/test_fastapi_adapter.py",
        ],
        "05": [
            "tests_reliability/test_telemetry_reconcile.py",
            "tests_reliability/test_fastapi_adapter.py",
        ],
        "06": [
            "tests_reliability/test_metrics_health.py",
            "tests_reliability/test_slo_alerts.py",
        ],
        "07": [
            "tests_reliability/test_context_deadline.py",
            "tests_reliability/test_fastapi_adapter.py",
        ],
        "08": [
            "tests_reliability/test_slo_alerts.py",
        ],
        "09": [
            "tests_reliability/test_operational_primitives.py",
        ],
        "10": [
            "tests_reliability/test_telemetry_reconcile.py",
        ],
    }
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    if module in module_files:
        run(
            [sys.executable, "-m", "pytest", "-q", *module_files[module]],
            cwd=PY_TRACK,
            env=env,
        )
    else:
        # Separate invocations prevent inherited tests with the same basename
        # from shadowing each other while preserving all three course layers.
        for directory in ["tests", "tests_security", "tests_reliability"]:
            _pytest_directory(directory)
    clean_generated()
    passed("Python proof" + (f" for module {module}" if module else " across Courses 2-4"))


def typescript_proof(module: str | None = None) -> None:
    if shutil.which("node") is None or shutil.which("tsc") is None:
        fail("TypeScript dependency-light proof requires node and tsc")
    suites = [
        ("tsconfig.core.json", "test-core"),
        ("tsconfig.security-core.json", "test-security-core"),
        ("tsconfig.reliability-core.json", "test-reliability-core"),
    ]
    if module is not None and module not in {"01", "10"}:
        suites = [("tsconfig.reliability-core.json", "test-reliability-core")]
    for config, directory in suites:
        run(["tsc", "-p", config], cwd=TS_TRACK)
        tests = sorted(str(path.relative_to(TS_TRACK)) for path in (TS_TRACK / directory).glob("*.test.mjs"))
        if not tests:
            fail(f"no TypeScript tests in {directory}")
        run(["node", "--test", *tests], cwd=TS_TRACK)
    run(["tsc", "-p", "tsconfig.audit.json", "--noEmit"], cwd=TS_TRACK)
    for name in ["dist-core", "dist-security", "dist-reliability", "dist-security-core", "dist-reliability-core", "dist-audit"]:
        shutil.rmtree(TS_TRACK / name, ignore_errors=True)
    passed("TypeScript source and dependency-light proof")


def observability_config_proof() -> None:
    obs = CAPSTONE / "observability"
    compose = load_yaml(obs / "compose.yaml")
    services = compose.get("services", {})
    required_services = {
        "postgres",
        "otel-collector",
        "prometheus",
        "jaeger",
        "fault-injector",
        "python-api",
        "python-worker",
        "typescript-api",
        "typescript-worker",
    }
    missing = required_services - set(services)
    if missing:
        fail(f"observability topology missing services {sorted(missing)}")

    collector = load_yaml(obs / "otel-collector.yaml")
    processors = collector.get("processors", {})
    for processor in ["memory_limiter", "batch"]:
        if not any(key == processor or key.startswith(processor + "/") for key in processors):
            fail(f"collector missing {processor} processor")
    if not any(key.startswith("attributes/") for key in processors):
        fail("collector lacks privacy attributes processor")
    pipelines = collector.get("service", {}).get("pipelines", {})
    if not {"traces", "metrics"}.issubset(pipelines):
        fail("collector lacks traces/metrics pipelines")

    prometheus = load_yaml(obs / "prometheus.yaml")
    jobs = {
        config.get("job_name")
        for config in prometheus.get("scrape_configs", [])
        if isinstance(config, dict)
    }
    if not {
        "analysis-python-api",
        "analysis-typescript-api",
        "otel-collector-internal",
        "otel-collector-exporter",
    }.issubset(jobs):
        fail(f"Prometheus scrape jobs incomplete: {sorted(jobs)}")

    recording_text = (obs / "rules" / "recording-rules.yaml").read_text(encoding="utf-8")
    if 'outcome="late"' in recording_text or 'outcome="bad"' not in recording_text:
        fail("recording rules do not use the shared good/bad/excluded outcome profile")
    alerts = load_yaml(obs / "rules" / "alerts.yaml")
    if not alerts.get("groups"):
        fail("Prometheus alert rules are empty")

    dashboard = load_json(obs / "dashboards" / "reliability-overview.json")
    dashboard_text = json.dumps(dashboard, sort_keys=True)
    if "http_route" in dashboard_text or "run_id" in dashboard_text:
        fail("dashboard uses unbounded/raw-route labels")
    if "operation" not in dashboard_text:
        fail("dashboard does not use bounded operation identity")

    for source in [
        PY_TRACK / "src" / "api_reliability" / "fastapi_adapter.py",
        TS_TRACK / "src" / "reliability-fastify.ts",
    ]:
        text = source.read_text(encoding="utf-8")
        for route in ["/internal/health/live", "/internal/health/ready", "/internal/metrics"]:
            if route not in text:
                fail(f"{source.relative_to(ROOT)} does not own {route}")
        if "otel-collector" in text and "readiness" in text:
            fail(f"{source.relative_to(ROOT)} appears to gate readiness on telemetry")

    passed("static observability topology, telemetry pipeline, rules, and dashboards")


def runbook_proof() -> None:
    required = {
        "id",
        "title",
        "owner",
        "trigger",
        "customerImpact",
        "prerequisites",
        "immediateActions",
        "stopConditions",
        "diagnosis",
        "mitigation",
        "rollback",
        "recoveryValidation",
        "closureCriteria",
        "escalation",
    }
    ids: set[str] = set()
    for path in sorted((CAPSTONE / "incident" / "runbooks").glob("*.yaml")):
        runbook = load_yaml(path)
        missing = required - set(runbook)
        if missing:
            fail(f"{path.name} missing runbook fields {sorted(missing)}")
        if runbook["id"] in ids:
            fail(f"duplicate runbook ID {runbook['id']}")
        ids.add(runbook["id"])
        for key in required - {"id", "title", "owner", "trigger", "customerImpact"}:
            value = runbook[key]
            if not isinstance(value, list) or not value:
                fail(f"{path.name}:{key} must be a nonempty action list")
        markdown = path.with_suffix(".md")
        if not markdown.is_file():
            fail(f"runbook prose missing: {markdown.name}")
    alert_runbooks = {
        row["runbook"]
        for row in load_yaml(CAPSTONE / "reliability-case" / "alert-catalog.yaml")["alerts"]
    }
    if not alert_runbooks.issubset(ids):
        fail(f"alerts reference missing runbooks {sorted(alert_runbooks-ids)}")
    passed(f"runbook schema and alert linkage — {len(ids)} runbooks")


def incident_proof() -> None:
    scenario = load_yaml(CAPSTONE / "incident" / "scenarios" / "INC-REL-001.yaml")
    roles = scenario.get("roles", {})
    for role in ["incidentCommander", "operationsLead", "communicationsLead", "scribe"]:
        if not isinstance(roles.get(role), str) or not roles[role].strip():
            fail(f"incident scenario lacks required role {role}")
    timeline = scenario.get("timeline", [])
    kinds = {row.get("kind") for row in timeline}
    required_kinds = {"observation", "inference", "action", "confirmation"}
    if not required_kinds.issubset(kinds):
        fail(f"incident timeline lacks epistemic kinds {sorted(required_kinds-kinds)}")
    if len(scenario.get("severityTransitions", [])) < 2:
        fail("incident lacks severity transitions")
    if not scenario.get("closureCriteria") or not scenario.get("requiredActions"):
        fail("incident lacks closure or required actions")

    game_day = load_yaml(CAPSTONE / "shared" / "scenarios" / "game-day.yaml")
    stages = game_day.get("stages", [])
    if len(stages) < 2:
        fail("game day has no staged progression")
    if "precondition" in stages[0]:
        fail("first game-day stage cannot depend on a prior stage")
    for stage in stages[1:]:
        if not stage.get("precondition"):
            fail(f"{stage.get('id')} lacks a progression precondition")
    for key in ["roles", "steadyState", "abortConditions", "cleanup", "requiredEvidence"]:
        if not game_day.get(key):
            fail(f"game day lacks {key}")
    fault_source = (CAPSTONE / "fault-injector" / "server.py").read_text(encoding="utf-8")
    if "FAULT_CONTROL_ENABLED" not in fault_source:
        fail("fault injector lacks explicit environment authorization guard")
    passed("incident and staged game-day evidence model")


def release_proof() -> None:
    accepted = load_yaml(CAPSTONE / "releases" / "reliability-1.0" / "RELEASE.yaml")
    rejected = load_yaml(
        CAPSTONE / "releases" / "rejected-unobservable-release" / "RELEASE.yaml"
    )
    if accepted.get("publicApi") != "1.2.0":
        fail("accepted reliability release changes the public API version")
    if str(accepted.get("securityProfile")) != "1.0" or str(accepted.get("reliabilityProfile")) != "1.0":
        fail("accepted release does not preserve security 1.0 and add reliability 1.0")
    if accepted.get("compatibility") != "public-contract-preserving":
        fail("accepted release is not explicitly public-contract-preserving")
    if accepted.get("databaseMigrations") != [8] and accepted.get("databaseMigrations") != ["008"]:
        fail("accepted release does not own migration 008")
    defects = rejected.get("rejectedBecause", [])
    required_defects = {
        "removes run-start freshness metric",
        "adds run.id as a metric label",
        "marks collector availability as API liveness",
        "retries unsafe submissions without idempotency evidence",
    }
    if not required_defects.issubset(set(defects)):
        fail("rejected release does not encode all four observability/reliability failures")
    passed("accepted observable release and deliberately rejected unobservable release")


def structure_proof() -> None:
    book = ROOT / "course-book"
    numbered_required = {
        'index.md', 'exercises.md', 'exercise-answers.md', 'lab.md', 'checkpoint.md'
    }
    orientation_required = {'index.md', 'lab.md', 'checkpoint.md'}
    modules = sorted(path for path in book.glob("module-*") if path.is_dir())
    if len(modules) != 11:
        fail(f"expected orientation plus ten modules, found {len(modules)}")
    for module in modules:
        names = {path.name for path in module.glob("*.md")}
        required = orientation_required if module.name == "module-00-orientation" else numbered_required
        missing = required - names
        if missing:
            fail(f"{module.name} missing {sorted(missing)}")
        if module.name != "module-00-orientation":
            exercises = (module / "exercises.md").read_text(encoding="utf-8")
            answers = (module / "exercise-answers.md").read_text(encoding="utf-8")
            exercise_count = len(
                re.findall(r"^## (?:Exercise )?\d+\.", exercises, flags=re.M)
            )
            answer_count = len(
                re.findall(r"^## (?:Exercise )?\d+\.", answers, flags=re.M)
            )
            if exercise_count != 12 or answer_count != 12:
                fail(
                    f"{module.name} requires 12 exercises and answers; "
                    f"found {exercise_count}/{answer_count}"
                )
            lab = (module / "lab.md").read_text(encoding="utf-8")
            for heading in [
                "## Setup conditions",
                "## Failure action and investigation",
                "## Operational oracle",
                "## Required evidence",
                "## Cleanup and reset",
                "## Completion gate",
            ]:
                if heading not in lab:
                    fail(f"{module.name}/lab.md lacks {heading}")

    required_top = {'README.md', 'Makefile', 'mkdocs.yml', 'course.json'}
    missing_top = [name for name in sorted(required_top) if not (ROOT / name).is_file()]
    if missing_top:
        fail(f"missing top-level files {missing_top}")

    config = load_yaml(ROOT / "mkdocs.yml")
    nav_files: set[str] = set()

    def walk_nav(value: Any) -> None:
        if isinstance(value, str) and value.endswith(".md"):
            nav_files.add(value)
        elif isinstance(value, list):
            for item in value:
                walk_nav(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk_nav(item)

    walk_nav(config.get("nav", []))
    actual = {
        path.relative_to(book).as_posix()
        for path in book.rglob("*.md")
    }
    missing_nav = actual - nav_files
    stale_nav = {path for path in nav_files if not (book / path).is_file()}
    if missing_nav or stale_nav:
        fail(
            f"MkDocs nav mismatch missing={sorted(missing_nav)[:10]} "
            f"stale={sorted(stale_nav)[:10]}"
        )
    passed(f"course structure — 11 modules, {len(actual)} navigated course-book pages")


def markdown_links() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    checked = 0
    broken: list[str] = []
    for page in sorted(ROOT.rglob("*.md")):
        if any(part in IGNORED_DIRS for part in page.relative_to(ROOT).parts):
            continue
        text = page.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#", "sandbox:")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            checked += 1
            destination = (page.parent / relative).resolve()
            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                broken.append(f"{page.relative_to(ROOT)} -> escaping target {target}")
                continue
            if not destination.exists():
                broken.append(f"{page.relative_to(ROOT)} -> {target}")
    if broken:
        fail("broken Markdown links: " + "; ".join(broken[:15]))
    passed(f"Markdown links — {checked} local targets")


def _paragraphs(text: str) -> Iterator[str]:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for paragraph in re.split(r"\n\s*\n", text):
        normalized = " ".join(paragraph.split())
        if normalized and not normalized.startswith(("- ", "1. ", "|")):
            yield normalized


def education_proof() -> None:
    prohibited = re.compile(
        r"\b(TODO|TBD|FIXME|lorem ipsum|coming soon|fill this in|write here|placeholder text)\b",
        re.I,
    )
    hits: list[str] = []
    paragraphs: Counter[str] = Counter()
    empty: list[str] = []
    lab_actions: dict[str, str] = {}
    for page in sorted(ROOT.rglob("*.md")):
        relative = page.relative_to(ROOT)
        if "planted-defects" in relative.parts:
            continue
        text = page.read_text(encoding="utf-8")
        if not text.strip():
            empty.append(str(relative))
        if prohibited.search(text):
            hits.append(str(relative))
        for paragraph in _paragraphs(text):
            if len(paragraph) >= 220 and not paragraph.startswith("|"):
                paragraphs[paragraph] += 1
        if page.name == "lab.md" and page.parent.name.startswith("module-") and page.parent.name != "module-00-orientation":
            match = re.search(
                r"## Failure action and investigation\s+(.+?)(?=\n## )",
                text,
                flags=re.S,
            )
            if match:
                lab_actions[page.parent.name] = " ".join(match.group(1).split())
    if hits or empty:
        fail(f"unfinished/empty educational material hits={hits[:8]} empty={empty[:8]}")
    repeated = [(paragraph, count) for paragraph, count in paragraphs.items() if count >= 8]
    if repeated:
        sample, count = sorted(repeated, key=lambda item: item[1], reverse=True)[0]
        fail(f"long educational paragraph repeated {count} times: {sample[:160]}...")
    if len(lab_actions) != 10 or len(set(lab_actions.values())) != 10:
        fail("the ten module labs do not have ten distinct failure actions")

    # Validate fenced Python snippets syntactically where possible. Snippets
    # containing shell placeholders or ellipses are intentionally excluded.
    python_fences = 0
    js_fences = 0
    for page in ROOT.rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        for language, code in re.findall(r"```([A-Za-z0-9_+-]*)\n(.*?)```", text, flags=re.S):
            language = language.lower()
            if language in {"python", "py"}:
                python_fences += 1
                if "..." not in code and not re.search(r"<[^>]+>", code):
                    try:
                        ast.parse(code)
                    except SyntaxError as exc:
                        fail(f"invalid Python curriculum fence in {page.relative_to(ROOT)}: {exc}")
            elif language in {"typescript", "ts", "javascript", "js"}:
                js_fences += 1
    passed(
        "educational quality — distinct labs, no unfinished markers, "
        f"{python_fences} Python and {js_fences} JS/TS code fences inventoried"
    )


def hygiene_proof() -> None:
    forbidden: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.is_dir() and path.name in IGNORED_DIRS:
            forbidden.append(str(relative))
        if path.is_file() and path.name in {".DS_Store", "Thumbs.db"}:
            forbidden.append(str(relative))
        if path.is_symlink():
            try:
                path.resolve(strict=True).relative_to(ROOT.resolve())
            except (ValueError, FileNotFoundError):
                forbidden.append(f"escaping/broken symlink {relative}")
    if forbidden:
        fail(f"generated or unsafe paths present: {forbidden[:15]}")

    handoff = CAPSTONE / "handoff"
    secret_patterns = ["PRIVATE KEY", "fixture-pepper", "fixture-private"]
    leaks: list[str] = []
    for path in handoff.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern in text for pattern in secret_patterns):
            leaks.append(str(path.relative_to(ROOT)))
    if leaks:
        fail(f"private fixture material in Course 4 handoff: {leaks[:10]}")
    passed("repository hygiene, symlink confinement, and outgoing-handoff secret guard")


def _manifest_excluded(relative: Path) -> bool:
    if relative.name in {"MANIFEST.json", "MANIFEST.sha256"}:
        return True
    if any(part in IGNORED_DIRS for part in relative.parts):
        return True
    if relative.parts and relative.parts[0] == "reports" and relative.name in EPHEMERAL_REPORTS:
        return True
    return False


def iter_manifest_files(base: Path = ROOT) -> Iterable[Path]:
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(base)
        if _manifest_excluded(relative):
            continue
        yield path


def _file_mode(path: Path) -> str:
    mode = stat.S_IMODE(path.stat().st_mode)
    return format(mode, "04o")


def create_manifest(base: Path, root_label: str) -> int:
    rows = [
        {
            "path": path.relative_to(base).as_posix(),
            "sha256": sha256(path),
            "size": path.stat().st_size,
            "mode": _file_mode(path),
        }
        for path in iter_manifest_files(base)
    ]
    payload = {
        "algorithm": "sha256",
        "root": root_label,
        "files": rows,
    }
    manifest = base / "MANIFEST.json"
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (base / "MANIFEST.sha256").write_text(
        f"{sha256(manifest)}  MANIFEST.json\n",
        encoding="utf-8",
    )
    return len(rows)


def manifest_create() -> None:
    handoff = CAPSTONE / "handoff"
    handoff_count = create_manifest(
        handoff,
        f"{COURSE_ARCHIVE_ROOT}/capstone/handoff",
    )
    course_count = create_manifest(ROOT, COURSE_ARCHIVE_ROOT)
    passed(f"manifests created — handoff {handoff_count}, course {course_count} files")


def manifest_proof() -> None:
    for base in [CAPSTONE / "handoff", ROOT]:
        checksum_file = base / "MANIFEST.sha256"
        if not checksum_file.is_file():
            fail(f"manifest checksum missing under {base.relative_to(ROOT)}")
        expected = checksum_file.read_text(encoding="utf-8").split()[0]
        if expected != sha256(base / "MANIFEST.json"):
            fail(f"MANIFEST.json checksum mismatch under {base.relative_to(ROOT)}")
        count = verify_manifest(base)
        actual = {path.relative_to(base).as_posix() for path in iter_manifest_files(base)}
        listed = {row["path"] for row in load_json(base / "MANIFEST.json")["files"]}
        if actual != listed:
            fail(
                f"manifest coverage mismatch under {base.relative_to(ROOT)}: "
                f"missing={sorted(actual-listed)[:5]} stale={sorted(listed-actual)[:5]}"
            )
        passed(f"manifest verified — {base.relative_to(ROOT) or Path('.')} {count} files")


def planted_defect_proof() -> None:
    defects_doc = load_json(CAPSTONE / "planted-defects" / "DEFECTS.json")
    defects = defects_doc.get("defects", [])
    modules = {row.get("module") for row in defects if isinstance(row, dict)}
    if len(defects) != 10 or modules != set(range(1, 11)):
        fail("planted defects must cover modules 1-10 exactly once")
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    run(
        [sys.executable, str(ROOT / "scripts" / "planted_defect_sensitivity.py")],
        cwd=ROOT,
        env=env,
    )
    passed("planted-defect sensitivity — ten named mutants rejected")


def source_reference_proof() -> None:
    python_files = 0
    javascript_files = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(
            part in IGNORED_DIRS for part in path.relative_to(ROOT).parts
        ):
            continue
        if path.suffix == ".py":
            python_files += 1
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                fail(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")
        elif path.suffix in {".js", ".mjs", ".cjs"}:
            javascript_files += 1
            if shutil.which("node") is None:
                fail("JavaScript syntax proof requires node")
            result = run_capture(["node", "--check", str(path)], cwd=ROOT)
            if result.returncode != 0:
                fail(
                    f"JavaScript syntax error in {path.relative_to(ROOT)}: "
                    f"{result.stderr.strip()}"
                )

    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    targets = {
        match.group(1)
        for match in re.finditer(r"^([A-Za-z0-9_.-]+):(?:\s|$)", makefile, flags=re.M)
    }
    path_prefixes = ("capstone/", "course-book/", "scripts/", "assessment/", "instructor/")
    missing_paths: list[str] = []
    missing_targets: list[str] = []
    referenced_paths: set[str] = set()
    referenced_targets: set[str] = set()
    code_span = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
    fenced = re.compile(r"```[^\n]*\n(.*?)```", re.S)
    shell_fenced = re.compile(
        r"```(?:bash|sh|shell|console)\s*\n(.*?)```", re.S | re.I
    )
    for page in sorted(ROOT.rglob("*.md")):
        if any(part in IGNORED_DIRS for part in page.relative_to(ROOT).parts):
            continue
        text = page.read_text(encoding="utf-8")
        fenced_snippets = fenced.findall(text)
        shell_snippets = shell_fenced.findall(text)
        inline_text = fenced.sub("", text)
        inline_snippets = code_span.findall(inline_text)
        snippets = [*inline_snippets, *fenced_snippets]
        for snippet in snippets:
            for candidate in re.findall(
                r"(?:capstone|course-book|scripts|assessment|instructor)/[A-Za-z0-9_./-]+",
                snippet,
            ):
                candidate = candidate.rstrip(".,:;)")
                if any(char in candidate for char in "*{}$<>"):
                    continue
                referenced_paths.add(candidate)
                if not (ROOT / candidate).exists():
                    missing_paths.append(
                        f"{page.relative_to(ROOT)} -> {candidate}"
                    )
        for snippet in [*inline_snippets, *shell_snippets]:
            for target in re.findall(
                r"(?:^|[;&|\n]\s*|\s)make\s+([A-Za-z0-9_.-]+)", snippet
            ):
                referenced_targets.add(target)
                if target not in targets:
                    missing_targets.append(
                        f"{page.relative_to(ROOT)} -> make {target}"
                    )
    if missing_paths or missing_targets:
        fail(
            "documentation reference mismatch: "
            f"paths={missing_paths[:12]} targets={missing_targets[:12]}"
        )
    passed(
        "source and documentation references — "
        f"{python_files} Python, {javascript_files} JavaScript files; "
        f"{len(referenced_paths)} paths and {len(referenced_targets)} Make targets"
    )


def module_proof(module: str, track: str) -> None:
    module = module.zfill(2)
    if module == "01":
        reliability_case_proof()
    elif module == "08":
        reliability_case_proof()
        runbook_proof()
        if track == "python":
            python_proof("08")
        else:
            typescript_proof("08")
    elif module == "09":
        incident_proof()
        planted_defect_proof()
        if track == "python":
            python_proof("09")
        else:
            typescript_proof("09")
    elif module == "10":
        incident_proof()
        runbook_proof()
        release_proof()
        if track == "python":
            python_proof("10")
        else:
            typescript_proof("10")
    elif module in {"02", "03", "04", "05", "06", "07"}:
        if track == "python":
            python_proof(module)
        elif track == "typescript":
            typescript_proof(module)
        else:
            fail("TRACK must be python or typescript")
    else:
        fail("MODULE must be 01 through 10")
    passed(f"module {module} proof ({track})")


def capstone_tour() -> None:
    script = CAPSTONE / "scripts" / "capstone_tour.py"
    if not script.is_file():
        fail("capstone tour script missing")
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    run([sys.executable, str(script)], cwd=ROOT, env=env)
    clean_generated()
    passed("capstone tour")


def orientation_proof() -> None:
    predecessor_proof()
    structure_proof()
    data_proof()
    doctor()
    passed("orientation proof")


def core_proof() -> None:
    clean_generated()
    predecessor_proof()
    reliability_case_proof()
    data_proof()
    vector_proof()
    migration_proof()
    python_proof()
    typescript_proof()
    observability_config_proof()
    runbook_proof()
    incident_proof()
    planted_defect_proof()
    release_proof()
    structure_proof()
    markdown_links()
    source_reference_proof()
    education_proof()
    clean_generated()
    hygiene_proof()
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "last-core-proof.json").write_text(
        json.dumps(
            {
                "course": COURSE_ID,
                "status": "passed",
                "scope": "dependency-light",
                "executed": [
                    "predecessor integrity",
                    "reliability case traceability",
                    "duplicate-key-aware data parsing",
                    "shared vector inventory",
                    "migration parity 001-008",
                    "Python inherited and reliability tests",
                    "TypeScript inherited and reliability tests",
                    "whole TypeScript source audit",
                    "observability configuration policy",
                    "runbooks, incident, game day, planted-defect sensitivity, releases",
                    "source syntax, documentation references, course structure, links, educational quality, hygiene",
                ],
                "notExecutedByCoreProof": [
                    "live PostgreSQL concurrency and recovery proof",
                    "Docker observability topology",
                    "full dependency-backed Fastify/Vitest suite",
                    "strict MkDocs build",
                    "promtool validation when unavailable",
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    passed("API Reliability and Observability Engineering core proof")


def external_status() -> dict[str, bool]:
    return {
        "mkdocs": shutil.which("mkdocs") is not None,
        "docker": shutil.which("docker") is not None,
        "psql": shutil.which("psql") is not None,
        "promtool": shutil.which("promtool") is not None,
        "npmDependencies": (TS_TRACK / "node_modules").is_dir(),
        "testDatabaseUrl": bool(os.environ.get("TEST_DATABASE_URL")),
    }


def full_proof() -> None:
    core_proof()
    manifest_proof()
    status = external_status()
    if not status["mkdocs"]:
        fail("full-proof requires mkdocs; dependency-light core-proof already passed")
    run(["mkdocs", "build", "--strict"], cwd=ROOT)
    if status["promtool"]:
        run(
            [
                "promtool",
                "check",
                "rules",
                "capstone/observability/rules/recording-rules.yaml",
                "capstone/observability/rules/alerts.yaml",
            ],
            cwd=ROOT,
        )
    else:
        fail("full-proof requires promtool")
    if status["npmDependencies"]:
        run(["npm", "run", "typecheck"], cwd=TS_TRACK)
        run(["npm", "test"], cwd=TS_TRACK)
    else:
        fail("full-proof requires the pinned npm dependency graph")
    if status["testDatabaseUrl"]:
        run(
            [sys.executable, str(CAPSTONE / "tests" / "failure" / "postgres_proof.py")],
            cwd=ROOT,
            env={"PYTHONPATH": str(PY_TRACK / "src")},
        )
    else:
        fail("full-proof requires TEST_DATABASE_URL")
    passed("complete environment-backed proof")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    for name in [
        "orientation-proof",
        "predecessor-proof",
        "reliability-case-proof",
        "data-proof",
        "vector-proof",
        "migration-proof",
        "python-proof",
        "typescript-core-proof",
        "observability-config-proof",
        "runbook-proof",
        "incident-proof",
        "planted-defect-proof",
        "release-proof",
        "structure-proof",
        "markdown-link-proof",
        "source-reference-proof",
        "education-proof",
        "hygiene-proof",
        "capstone-tour",
        "core-proof",
        "manifest-create",
        "manifest-proof",
        "full-proof",
    ]:
        sub.add_parser(name)
    module = sub.add_parser("module-proof")
    module.add_argument("--module", required=True)
    module.add_argument("--track", choices=["python", "typescript"], required=True)
    args = parser.parse_args()
    commands = {
        "doctor": doctor,
        "orientation-proof": orientation_proof,
        "predecessor-proof": predecessor_proof,
        "reliability-case-proof": reliability_case_proof,
        "data-proof": data_proof,
        "vector-proof": vector_proof,
        "migration-proof": migration_proof,
        "python-proof": python_proof,
        "typescript-core-proof": typescript_proof,
        "observability-config-proof": observability_config_proof,
        "runbook-proof": runbook_proof,
        "incident-proof": incident_proof,
        "planted-defect-proof": planted_defect_proof,
        "release-proof": release_proof,
        "structure-proof": structure_proof,
        "markdown-link-proof": markdown_links,
        "source-reference-proof": source_reference_proof,
        "education-proof": education_proof,
        "hygiene-proof": hygiene_proof,
        "capstone-tour": capstone_tour,
        "core-proof": core_proof,
        "manifest-create": manifest_create,
        "manifest-proof": manifest_proof,
        "full-proof": full_proof,
    }
    if args.command == "module-proof":
        module_proof(args.module, args.track)
    else:
        commands[args.command]()


if __name__ == "__main__":
    main()
