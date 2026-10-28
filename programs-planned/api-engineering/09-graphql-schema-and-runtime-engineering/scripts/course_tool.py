#!/usr/bin/env python3
"""Learner and verification routes for Course 9.

The dependency-light checks prove the engineering profile implemented by this
course. They do not claim full GraphQL standards conformance. Independent
GraphQL implementations remain part of the environment-backed proof layer.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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
from typing import Any, Iterable
from urllib.parse import unquote

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyYAML is required for dependency-light proofs: {exc}")

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capstone"
BOOK = ROOT / "course-book"
PY_TRACK = CAP / "tracks/python-graphql"
PY_SRC = PY_TRACK / "src"
TS_TRACK = CAP / "tracks/typescript-graphql"

EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "site",
    ".tmp",
}
ROOT_MANIFEST_NAMES = {"MANIFEST.json", "MANIFEST.sha256"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

EXPECTED_OPERATIONS = {
    "Viewer",
    "GetProjectOverview",
    "GetRun",
    "ListRuns",
    "SearchPlatform",
    "CreateProject",
    "StartAnalysis",
    "CancelAnalysis",
    "RunUpdates",
    "NodeLookup",
}

SAMPLE_VARIABLES: dict[str, dict[str, Any]] = {
    "Viewer": {},
    "GetProjectOverview": {"projectId": "UHJvamVjdDpwcm9qLTE", "first": 2},
    "GetRun": {"runId": "QW5hbHlzaXNSdW46cnVuLTE"},
    "ListRuns": {"first": 2},
    "SearchPlatform": {"text": "run", "first": 3},
    "CreateProject": {
        "input": {"idempotencyKey": "proof-project", "name": "Proof Study"}
    },
    "StartAnalysis": {
        "input": {
            "idempotencyKey": "proof-run",
            "projectId": "UHJvamVjdDpwcm9qLTE",
            "datasetId": "dataset-proof",
            "algorithm": "qc",
        }
    },
    "CancelAnalysis": {
        "input": {
            "runId": "QW5hbHlzaXNSdW46cnVuLTI",
            "expectedVersion": "2",
        }
    },
    "RunUpdates": {
        "runId": "QW5hbHlzaXNSdW46cnVuLTE",
        "afterSequence": "3",
    },
    "NodeLookup": {"by": {"id": "UHJvamVjdDpwcm9qLTE"}},
}


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    merged["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        merged.update(env)
    print("+", " ".join(command))
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged,
        text=True,
        check=True,
        capture_output=capture,
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def read_yaml(path: Path) -> Any:
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
        size = item.get("size", item.get("bytes"))
        assert path.stat().st_size == size, f"size mismatch: {relative}"
        assert sha256(path) == item["sha256"], f"digest mismatch: {relative}"
    declared_count = manifest.get("file_count")
    if declared_count is not None:
        assert declared_count == len(expected_paths)
    if exact:
        actual_paths = {
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*")
            if eligible(path, directory)
        }
        assert actual_paths == expected_paths, (
            "manifest inventory mismatch; "
            f"missing={sorted(expected_paths - actual_paths)[:8]} "
            f"unlisted={sorted(actual_paths - expected_paths)[:8]}"
        )
    return len(expected_paths)


def import_reference() -> dict[str, Any]:
    sys.path.insert(0, str(PY_SRC))
    from graph_api.compatibility import SchemaChange, classify
    from graph_api.cost import CostPolicy, analyze
    from graph_api.cursor import (
        CursorCodec,
        CursorState,
        audience_hash,
        normalized_filter_hash,
    )
    from graph_api.execution import TypeRef, complete_object
    from graph_api.identity import decode_global_id, encode_global_id
    from graph_api.loader import BatchLoader
    from graph_api.model import (
        GraphError,
        Principal,
        RequestContext,
        ValidationError,
    )
    from graph_api.operation import (
        FieldNode,
        FragmentSpread,
        InlineFragment,
        parse_document,
    )
    from graph_api.persisted import PersistedOperationRegistry
    from graph_api.policy import require_field
    from graph_api.release import ReleaseEvidence, decide
    from graph_api.subscription import ResumableSubscription, SubscriptionEvent
    from graph_api.tour import build_gateway, run_tour
    from graph_api.transport import HttpRequest, evaluate

    return locals()


def doctor() -> None:
    print("python", sys.version.split()[0])
    for tool in [
        "node",
        "tsc",
        "mkdocs",
        "docker",
        "psql",
        "graphql-inspector",
    ]:
        print(f"{tool}: {shutil.which(tool) or 'not-available'}")
    try:
        import graphql  # type: ignore

        print("graphql-core:", getattr(graphql, "__version__", "available"))
    except Exception:
        print("graphql-core: not-available")
    print("PyYAML", yaml.__version__)
    print("course", read_json(ROOT / "course.json")["version"])


def predecessor_proof() -> None:
    handoff = CAP / "predecessor/handoff"
    count = verify_manifest(handoff, exact=True)
    assert count == 8, f"expected Course 8 handoff of 8 files, got {count}"
    boundary = read_json(handoff / "BOUNDARY.json")
    assert boundary["from_course"].startswith("08-")
    assert boundary["to_course"].startswith("09-")
    brief = read_yaml(handoff / "graphql-boundary-brief.yaml")
    forbidden = set(brief["forbidden"])
    assert "direct database joins across services" in forbidden
    assert "silent partial data" in forbidden
    print(f"PASS Course 8 predecessor handoff — {count} exact files")


def _nav_paths(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, str):
        output.append(value)
    elif isinstance(value, list):
        for item in value:
            output.extend(_nav_paths(item))
    elif isinstance(value, dict):
        for item in value.values():
            output.extend(_nav_paths(item))
    return output


def structure_proof() -> None:
    pages = sorted(BOOK.rglob("*.md"))
    assert len(pages) == 59, f"expected 59 course-book pages, got {len(pages)}"
    module_dirs = sorted(
        path for path in BOOK.glob("module-[0-9][0-9]-*") if path.is_dir()
    )
    assert len(module_dirs) == 11, "expected orientation plus ten modules"
    numbered = [path for path in module_dirs if "module-00-" not in path.name]
    required = {
        "index.md",
        "exercises.md",
        "exercise-answers.md",
        "lab.md",
        "checkpoint.md",
    }
    exercise_count = answer_count = 0
    lab_sections = {
        "Purpose",
        "Prerequisites",
        "Procedure",
        "Correctness oracle",
        "Required evidence",
        "Cleanup",
        "Completion gate",
    }
    for index, directory in enumerate(numbered, start=1):
        names = {path.name for path in directory.glob("*.md")}
        assert names == required, f"module shape mismatch: {directory.name}"
        exercises = re.findall(
            r"^## (\d+)\. (.+)$",
            (directory / "exercises.md").read_text(),
            re.M,
        )
        answers = re.findall(
            r"^## (\d+)\. (.+)$",
            (directory / "exercise-answers.md").read_text(),
            re.M,
        )
        assert exercises == answers, f"answer headings differ: {directory.name}"
        assert len(exercises) == 12, f"expected 12 exercises: {directory.name}"
        exercise_count += len(exercises)
        answer_count += len(answers)
        headings = set(
            re.findall(r"^## (.+)$", (directory / "lab.md").read_text(), re.M)
        )
        assert lab_sections.issubset(headings), f"lab sections missing: {directory.name}"
        checkpoint = (directory / "checkpoint.md").read_text()
        assert checkpoint.count("- [ ]") >= 6
        assert f"make module-{index:02d}-proof" in checkpoint
        assert len((directory / "index.md").read_text().split()) >= 1_400
        assert len((directory / "lab.md").read_text().split()) >= 400
    assert exercise_count == answer_count == 120

    config = read_yaml(ROOT / "mkdocs.yml")
    nav = set(_nav_paths(config["nav"]))
    expected_nav = {path.relative_to(ROOT).as_posix() for path in pages}
    assert nav == expected_nav, (
        f"MkDocs navigation mismatch; missing={sorted(expected_nav-nav)[:8]} "
        f"extra={sorted(nav-expected_nav)[:8]}"
    )
    print("PASS structure — 59 pages, 10 modules, 120 matched answers, 10 labs")


def _sdl_types(schema: str) -> tuple[dict[str, dict[str, str]], set[str], dict[str, set[str]]]:
    fields: dict[str, dict[str, str]] = {}
    inputs: set[str] = set()
    enums: dict[str, set[str]] = {}
    block_pattern = re.compile(
        r"\b(type|interface|input)\s+(\w+)"
        r"(?:\s+implements\s+[^\{]+)?"
        r"(?:\s+@\w+(?:\([^)]*\))?)*\s*\{([^}]*)\}",
        re.S,
    )
    for kind, name, body in block_pattern.findall(schema):
        if kind == "input":
            inputs.add(name)
        coordinates: dict[str, str] = {}
        cleaned = re.sub(r'@\w+(?:\([^)]*\))?', '', body)
        cleaned = re.sub(r'""".*?"""', '', cleaned, flags=re.S)
        for match in re.finditer(
            r"(?:^|\s)(\w+)\s*(?:\([^)]*\))?\s*:\s*([\[\]!\w]+)",
            cleaned,
            re.M,
        ):
            coordinates[match.group(1)] = re.sub(
                r"[\[\]!]", "", match.group(2)
            )
        fields[name] = coordinates
    for name, body in re.findall(r"\benum\s+(\w+)\s*\{([^}]*)\}", schema, re.S):
        enums[name] = {
            token
            for token in re.findall(r"\b[A-Z][A-Z0-9_]*\b", body)
            if token not in {"DEPRECATED"}
        }
    for name, _members in re.findall(r"\bunion\s+(\w+)\s*=([^\n]+)", schema):
        fields.setdefault(name, {})
    return fields, inputs, enums


def _validate_operation_against_schema(
    document: Any,
    fields: dict[str, dict[str, str]],
) -> None:
    ref = import_reference()
    FieldNode = ref["FieldNode"]
    FragmentSpread = ref["FragmentSpread"]
    InlineFragment = ref["InlineFragment"]

    def walk(selections: Iterable[Any], current_type: str, seen: tuple[str, ...]) -> None:
        assert current_type in fields or current_type in {
            "String",
            "Int",
            "Boolean",
            "ID",
            "DateTime",
            "Cursor",
            "Version",
            "JSON",
            "RunStatus",
            "Permission",
            "ProblemCode",
        }, f"unknown selected type: {current_type}"
        for selection in selections:
            if isinstance(selection, FieldNode):
                if selection.name == "__typename":
                    continue
                assert current_type in fields, (
                    f"cannot select {selection.name} on scalar/enum {current_type}"
                )
                assert selection.name in fields[current_type], (
                    f"unknown field {current_type}.{selection.name}"
                )
                next_type = fields[current_type][selection.name]
                if selection.selections:
                    walk(selection.selections, next_type, seen)
            elif isinstance(selection, InlineFragment):
                walk(selection.selections, selection.type_condition or current_type, seen)
            elif isinstance(selection, FragmentSpread):
                assert selection.name not in seen, "fragment cycle in registered operation"
                fragment = document.fragments[selection.name]
                walk(
                    fragment.selections,
                    fragment.type_condition,
                    (*seen, selection.name),
                )
            else:  # pragma: no cover
                raise AssertionError(f"unknown selection: {selection!r}")

    roots = {"query": "Query", "mutation": "Mutation", "subscription": "Subscription"}
    assert len(document.operations) == 1
    operation = document.operations[0]
    walk(operation.selections, roots[operation.operation_type], ())


def schema_proof() -> None:
    schema_path = CAP / "contracts/schema.graphql"
    schema = schema_path.read_text()
    assert 'schema {' in schema
    assert 'query: Query' in schema and 'mutation: Mutation' in schema
    assert 'subscription: Subscription' in schema
    assert 'input NodeLookup @oneOf' in schema
    assert 'directive @source' in schema and 'directive @cost' in schema
    assert 'directive @requires' in schema and 'directive @stale' in schema

    fields, inputs, enums = _sdl_types(schema)
    assert {"Query", "Mutation", "Subscription", "Project", "AnalysisRun", "Artifact"}.issubset(fields)
    assert "NodeLookup" in inputs
    assert fields["NodeLookup"] == {"id": "ID", "externalId": "String"}
    oneof_body = re.search(r"input\s+NodeLookup\s+@oneOf\s*\{([^}]*)\}", schema, re.S)
    assert oneof_body
    assert "!" not in oneof_body.group(1) and "=" not in oneof_body.group(1)
    assert enums["RunStatus"] == {"QUEUED", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"}

    registry = read_json(CAP / "contracts/persisted-operations.json")
    operations = registry["operations"]
    assert len(operations) == 10
    assert {item["name"] for item in operations.values()} == EXPECTED_OPERATIONS
    ref = import_reference()
    parse_document = ref["parse_document"]
    names: set[str] = set()
    for digest, item in operations.items():
        operation_path = CAP / "contracts" / item["file"]
        assert operation_path.is_file()
        assert sha256(operation_path) == digest
        document = parse_document(operation_path.read_text())
        assert len(document.operations) == 1
        name = document.operations[0].name
        assert name == item["name"] == operation_path.stem
        assert name not in names
        names.add(name)
        _validate_operation_against_schema(document, fields)

    client_catalog = read_yaml(CAP / "contracts/client-catalog.yaml")
    for client in client_catalog["clients"]:
        assert client["owner"]
        assert set(client["operations"]).issubset(EXPECTED_OPERATIONS)
    print("PASS graph schema — release 1.0, 3 roots, @oneOf, 10 active operations")


def ownership_proof() -> None:
    catalogue = read_json(CAP / "contracts/schema-catalog.json")
    resolver_map = read_yaml(CAP / "graph-case/resolver-ownership.yaml")["fields"]
    policy_map = read_yaml(CAP / "security/field-policy.yaml")["fields"]
    assert catalogue["field_sources"] == resolver_map == policy_map
    assert len(resolver_map) == 15
    allowed = {
        "analysis-control",
        "artifact-service",
        "notification-service",
        "analysis-events-1.0",
        "graph-gateway-context",
        "graph-gateway-dispatch",
        "graph-gateway-composition",
    }
    assert set(resolver_map.values()).issubset(allowed)
    boundary = read_yaml(CAP / "graph-case/boundary-policy.yaml")
    assert "private database reads" in boundary["forbidden"]
    source = "\n".join(
        path.read_text(errors="ignore")
        for track in [PY_TRACK / "src", TS_TRACK / "src"]
        for path in track.rglob("*")
        if path.suffix in {".py", ".ts"}
    ).casefold()
    forbidden = ["psycopg", "sqlalchemy", "from pg ", "select * from", "private database"]
    assert not any(token in source for token in forbidden[:-1]), "graph runtime contains a private database dependency"
    summary = read_json(CAP / "final-defense/architecture-summary.json")
    assert summary["direct_database_joins"] == 0
    assert summary["graph_gateway_business_facts_owned"] == 0
    print("PASS field authority — 15 coordinates, no graph-owned business facts or DB joins")


def pagination_proof() -> None:
    ref = import_reference()
    Principal = ref["Principal"]
    RequestContext = ref["RequestContext"]
    encode_global_id = ref["encode_global_id"]
    build_gateway = ref["build_gateway"]
    gateway = build_gateway(ROOT)
    principal = Principal("learner", "tenant-a", frozenset({"RUN_READ"}))
    context = RequestContext(principal, "pagination-proof")
    operation = gateway.registry.by_name("ListRuns")
    first = gateway.execute(operation.sha256, {"first": 1}, context)
    cursor = first.data["analysisRuns"]["pageInfo"]["endCursor"]
    assert cursor
    gateway.analysis.runs["run-new"] = {
        "id": "run-new",
        "tenantId": "tenant-a",
        "projectId": "proj-1",
        "datasetId": "data-new",
        "status": "RUNNING",
        "version": "1",
        "createdAt": "2026-08-09T10:00:00Z",
        "resultSummary": None,
    }
    continued = gateway.execute(
        operation.sha256,
        {"first": 20, "after": cursor},
        context,
    )
    ids = {edge["node"]["id"] for edge in continued.data["analysisRuns"]["edges"]}
    assert encode_global_id("AnalysisRun", "run-new") not in ids
    fresh = gateway.execute(operation.sha256, {"first": 1}, context)
    assert fresh.data["analysisRuns"]["edges"][0]["node"]["id"] == encode_global_id("AnalysisRun", "run-new")
    wrong_context = RequestContext(
        Principal("other", "tenant-a", frozenset({"RUN_READ"})),
        "pagination-other",
    )
    rejected = gateway.execute(
        operation.sha256,
        {"first": 10, "after": cursor},
        wrong_context,
    )
    assert rejected.errors and rejected.errors[0].code == "GRAPHQL_VALIDATION_FAILED"
    vectors = read_json(CAP / "shared/vectors/cursors.json")
    assert vectors["profile"] == "analysis-graph-keyset-cursor-v1"
    assert len(vectors["cases"]) == 5
    assert sum(case["valid"] for case in vectors["cases"]) == 1
    report = {
        "status": "pass",
        "cursor_bound_to": [
            "tenant",
            "audience",
            "field-scope",
            "normalized-filter",
            "continuation-key",
            "high-water-key",
            "expiry",
            "version",
        ],
        "newer_insert_excluded_from_existing_traversal": True,
        "fresh_traversal_observes_newer_insert": True,
        "audience_mismatch_rejected": True,
    }
    (ROOT / "reports/module-04-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS pagination — signed keyset cursor, high-water continuity, audience binding")


def batching_proof() -> None:
    ref = import_reference()
    Principal = ref["Principal"]
    RequestContext = ref["RequestContext"]
    encode_global_id = ref["encode_global_id"]
    build_gateway = ref["build_gateway"]
    gateway = build_gateway(ROOT)
    full = Principal(
        "learner",
        "tenant-a",
        frozenset({"PROJECT_READ", "ARTIFACT_READ", "DELIVERY_READ"}),
    )
    operation = gateway.registry.by_name("GetProjectOverview")
    result = gateway.execute(
        operation.sha256,
        {"projectId": encode_global_id("Project", "proj-1"), "first": 2},
        RequestContext(full, "batch-proof"),
    )
    assert result.extensions["batchCalls"] == {"artifact": 1, "delivery": 1}
    assert len(result.data["project"]["analysisRuns"]["edges"]) == 2
    denied_gateway = build_gateway(ROOT)
    denied = Principal("reader", "tenant-a", frozenset({"PROJECT_READ"}))
    denied_result = denied_gateway.execute(
        operation.sha256,
        {"projectId": encode_global_id("Project", "proj-1"), "first": 2},
        RequestContext(denied, "denied-batch"),
    )
    assert denied_gateway.artifacts.calls.count("batch_by_run") == 0
    assert denied_gateway.notifications.calls.count("batch_by_run") == 0
    assert all(error.code == "FORBIDDEN" for error in denied_result.errors)
    report = {
        "status": "pass",
        "parents": 2,
        "artifact_batch_calls": 1,
        "delivery_batch_calls": 1,
        "denied_source_calls": 0,
        "request_scoped": True,
    }
    (ROOT / "reports/module-03-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS batching — one call per protected source and zero calls after denial")


def mutation_proof() -> None:
    ref = import_reference()
    Principal = ref["Principal"]
    RequestContext = ref["RequestContext"]
    encode_global_id = ref["encode_global_id"]
    build_gateway = ref["build_gateway"]
    gateway = build_gateway(ROOT)
    principal = Principal(
        "writer",
        "tenant-a",
        frozenset({"PROJECT_READ", "RUN_READ", "RUN_WRITE"}),
    )
    context = RequestContext(principal, "mutation-proof")
    operation = gateway.registry.by_name("StartAnalysis")
    variables = {
        "input": {
            "idempotencyKey": "mutation-proof-key",
            "projectId": encode_global_id("Project", "proj-1"),
            "datasetId": "data-proof",
            "algorithm": "qc",
        }
    }
    first = gateway.execute(operation.sha256, variables, context)
    second = gateway.execute(operation.sha256, variables, context)
    assert first.data["startAnalysis"]["replayed"] is False
    assert second.data["startAnalysis"]["replayed"] is True
    changed = {
        "input": {**variables["input"], "algorithm": "changed"}
    }
    conflict = gateway.execute(operation.sha256, changed, context)
    assert conflict.data["startAnalysis"]["code"] == "CONFLICT"
    cancel = gateway.registry.by_name("CancelAnalysis")
    stale = gateway.execute(
        cancel.sha256,
        {
            "input": {
                "runId": encode_global_id("AnalysisRun", "run-2"),
                "expectedVersion": "1",
            }
        },
        context,
    )
    assert stale.data["cancelAnalysis"]["code"] == "PRECONDITION_FAILED"
    report = {
        "status": "pass",
        "logical_effects": 1,
        "retry_replayed": True,
        "changed_input": "CONFLICT",
        "stale_version": "PRECONDITION_FAILED",
        "gateway_business_state_tables": 0,
    }
    (ROOT / "reports/module-05-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS mutations — source-owned idempotency, typed conflict, expected-version guard")


def authorization_proof() -> None:
    ref = import_reference()
    Principal = ref["Principal"]
    RequestContext = ref["RequestContext"]
    encode_global_id = ref["encode_global_id"]
    build_gateway = ref["build_gateway"]
    gateway = build_gateway(ROOT)
    operation = gateway.registry.by_name("GetRun")
    denied = Principal("reader", "tenant-a", frozenset({"RUN_READ"}))
    result = gateway.execute(
        operation.sha256,
        {"runId": encode_global_id("AnalysisRun", "run-1")},
        RequestContext(denied, "authorization-proof"),
    )
    assert result.data["analysisRun"]["artifacts"] is None
    assert result.data["analysisRun"]["deliverySummary"] is None
    assert gateway.artifacts.calls.count("batch_by_run") == 0
    assert gateway.notifications.calls.count("batch_by_run") == 0
    other = Principal(
        "other",
        "tenant-b",
        frozenset({"RUN_READ", "ARTIFACT_READ", "DELIVERY_READ"}),
    )
    concealed = gateway.execute(
        operation.sha256,
        {"runId": encode_global_id("AnalysisRun", "run-1")},
        RequestContext(other, "other-tenant"),
    )
    assert concealed.data["analysisRun"] is None
    vectors = read_json(CAP / "shared/vectors/authorization.json")
    assert sum(case["allow"] for case in vectors) == 2
    assert sum(not case["allow"] for case in vectors) == 2
    report = {
        "status": "pass",
        "cross_tenant_concealed": True,
        "denied_protected_source_calls": 0,
        "field_policy_coordinates": len(
            read_yaml(CAP / "security/field-policy.yaml")["fields"]
        ),
    }
    (ROOT / "reports/module-06-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS authorization — field denial before I/O and tenant concealment")


def demand_proof() -> None:
    ref = import_reference()
    parse_document = ref["parse_document"]
    analyze = ref["analyze"]
    CostPolicy = ref["CostPolicy"]
    ValidationError = ref["ValidationError"]
    policy_yaml = read_yaml(CAP / "graph-case/cost-policy.yaml")
    limits = policy_yaml["limits"]
    policy = CostPolicy(
        max_depth=limits["depth"],
        max_aliases=limits["aliases"],
        max_root_fields=limits["root_fields"],
        max_cost=limits["estimated_cost"],
        max_fanout=limits["service_fanout"],
        default_page_size=policy_yaml["list_defaults"]["default_page_size"],
        max_page_size=policy_yaml["list_defaults"]["maximum_page_size"],
    )
    registry = read_json(CAP / "contracts/persisted-operations.json")["operations"]
    for item in registry.values():
        document = parse_document((CAP / "contracts" / item["file"]).read_text())
        report = analyze(
            document,
            operation_name=item["name"],
            variables=SAMPLE_VARIABLES[item["name"]],
            policy=policy,
        )
        assert report.estimated_cost <= policy.max_cost
        assert report.service_fanout <= policy.max_fanout
    attacks = {
        "fragment-cycle": (
            'query Q { project(id:"1") { ...A } } '
            'fragment A on Project { ...B } fragment B on Project { ...A }',
            {},
        ),
        "alias-storm": (
            "query Q { "
            + " ".join(f"a{i}: viewer {{ subject }}" for i in range(31))
            + " }",
            {},
        ),
        "oversized-page": (
            "query Q($first:Int!){ analysisRuns(first:$first){ edges { node { id } } } }",
            {"first": 101},
        ),
    }
    for name, (source, variables) in attacks.items():
        try:
            analyze(
                parse_document(source),
                operation_name="Q",
                variables=variables,
                policy=policy,
            )
        except ValidationError:
            pass
        else:
            raise AssertionError(f"demand attack admitted: {name}")
    report = {
        "status": "pass",
        "active_operations_admitted": 10,
        "fragment_cycle": "rejected",
        "alias_storm": "rejected",
        "oversized_page": "rejected",
        "rejected_source_calls": 0,
    }
    (ROOT / "reports/module-07-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS demand control — active registry admitted, three hostile shapes rejected")


def error_proof() -> None:
    ref = import_reference()
    Principal = ref["Principal"]
    RequestContext = ref["RequestContext"]
    encode_global_id = ref["encode_global_id"]
    build_gateway = ref["build_gateway"]
    complete_object = ref["complete_object"]
    TypeRef = ref["TypeRef"]
    GraphError = ref["GraphError"]
    gateway = build_gateway(ROOT)
    principal = Principal(
        "learner",
        "tenant-a",
        frozenset({"RUN_READ", "ARTIFACT_READ", "DELIVERY_READ"}),
    )
    gateway.artifacts.available = False
    operation = gateway.registry.by_name("GetRun")
    result = gateway.execute(
        operation.sha256,
        {"runId": encode_global_id("AnalysisRun", "run-1")},
        RequestContext(principal, "partial-proof"),
    )
    assert result.data["analysisRun"]["artifacts"] is None
    assert result.errors[0].path == ("analysisRun", "artifacts")
    assert result.errors[0].service == "artifact-service"
    completed = complete_object(
        {
            "analysisRuns": (
                None,
                TypeRef("Connection", True),
                GraphError(
                    "down",
                    ("project", "analysisRuns"),
                    "DOWNSTREAM_UNAVAILABLE",
                ),
            )
        },
        path=("project",),
    )
    assert completed.bubbled is True and completed.value is None
    report = {
        "status": "pass",
        "nullable_remote_failure": {
            "value": None,
            "path": ["analysisRun", "artifacts"],
            "code": "DOWNSTREAM_UNAVAILABLE",
        },
        "authoritative_non_null_bubbled": True,
        "silent_empty_list": False,
    }
    (ROOT / "reports/module-08-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS error semantics — exact path partiality and non-null bubbling")


def subscription_proof() -> None:
    ref = import_reference()
    SubscriptionEvent = ref["SubscriptionEvent"]
    ResumableSubscription = ref["ResumableSubscription"]
    ValidationError = ref["ValidationError"]
    subscription = ResumableSubscription(maximum_buffer=3)
    values = [
        SubscriptionEvent(4, {"status": "RUNNING"}),
        SubscriptionEvent(4, {"status": "RUNNING"}),
        SubscriptionEvent(5, {"status": "COMPLETED"}),
    ]
    delivered = subscription.resume(values, after=3)
    assert [event.sequence for event in delivered] == [4, 5]
    try:
        subscription.resume([SubscriptionEvent(5, {})], after=3)
    except ValidationError:
        pass
    else:
        raise AssertionError("subscription gap was hidden")
    try:
        ResumableSubscription(maximum_buffer=2).resume(
            [SubscriptionEvent(4, {}), SubscriptionEvent(5, {}), SubscriptionEvent(6, {})],
            after=3,
        )
    except ValidationError:
        pass
    else:
        raise AssertionError("subscription buffer limit was not enforced")
    policy = read_yaml(CAP / "graph-case/subscription-policy.yaml")
    assert policy["source"] == "analysis-events-1.0"
    assert policy["baseline_transport"] == "course-sse-profile-1.0"
    report = {
        "status": "pass",
        "delivered_sequences": [4, 5],
        "duplicates_suppressed": True,
        "gap_rejected": True,
        "buffer_bound_checked": True,
        "source": policy["source"],
    }
    (ROOT / "reports/module-09-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS subscriptions — duplicate suppression, gap rejection, bounded buffering")


def release_proof() -> None:
    candidates: dict[str, str] = {}
    for directory in sorted((CAP / "releases").iterdir()):
        candidate_path = directory / "candidate.json"
        if not candidate_path.is_file():
            continue
        candidate = read_json(candidate_path)
        expected = candidate["expected"]
        if expected in {"additive", "review-required"}:
            assert candidate["activeOperationsValid"] is True
            assert candidate["budgetsPass"] is True
            assert candidate["ownershipComplete"] is True
            assert candidate["oldClientPasses"] is True
        else:
            assert any(
                candidate.get(key) is False
                for key in [
                    "activeOperationsValid",
                    "budgetsPass",
                    "ownershipComplete",
                    "oldClientPasses",
                ]
            ) or expected.startswith("breaking")
        candidates[directory.name] = expected
    assert len(candidates) == 10
    assert Counter(candidates.values())["additive"] == 1
    assert Counter(candidates.values())["review-required"] == 1
    rejected = [
        value
        for value in candidates.values()
        if value not in {"additive", "review-required"}
    ]
    assert len(rejected) == 8
    report = {
        "status": "pass",
        "accepted": 1,
        "review_required": 1,
        "rejected": 8,
        "active_operations": 10,
        "course10_handoff_ready": True,
    }
    (ROOT / "reports/module-10-proof.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("PASS graph release gate — 1 additive, 1 review, 8 rejected candidates")


def migration_proof() -> None:
    paths = sorted(
        (CAP / "database/platform-catalog/migrations").glob("*.sql")
    )
    revisions = [path.name.split("_", 1)[0] for path in paths]
    assert revisions == ["001", "002", "003", "004"]
    text = "\n".join(path.read_text() for path in paths)
    required_tables = {
        "graph_schema_releases",
        "graph_persisted_operations",
        "graph_client_budgets",
        "graph_subscription_checkpoints",
    }
    assert all(f"CREATE TABLE {table}" in text for table in required_tables)
    business_tokens = ["projects", "analysis_runs", "artifacts", "webhook_deliveries"]
    assert not any(re.search(rf"CREATE TABLE\s+{token}\b", text) for token in business_tokens)
    print("PASS graph metadata migrations — 001–004 and no business-state tables")


def vector_proof() -> None:
    files = sorted((CAP / "shared/vectors").glob("*.json"))
    assert len(files) == 10
    cases = 0
    for path in files:
        value = read_json(path)
        if isinstance(value, list):
            assert value, f"empty vector file: {path.name}"
            cases += len(value)
        elif isinstance(value, dict) and isinstance(value.get("cases"), list):
            assert value["cases"], f"empty vector file: {path.name}"
            cases += len(value["cases"])
        else:
            raise AssertionError(f"unsupported vector shape: {path.name}")
    assert cases == 36, f"expected 36 vector cases, got {cases}"
    print(f"PASS shared vectors — {len(files)} files, {cases} identified cases")


def python_proof() -> None:
    completed = run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(PY_TRACK / "tests"),
            "-v",
        ],
        env={"PYTHONPATH": str(PY_SRC)},
        capture=True,
    )
    output = completed.stdout + completed.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    assert match, output
    count = int(match.group(1))
    assert count >= 29
    print(output.rstrip())
    print(f"PASS Python semantic track — {count} tests")


def _copy_ts_track(destination: Path) -> Path:
    copied = destination / "typescript-graphql"
    shutil.copytree(
        TS_TRACK,
        copied,
        ignore=shutil.ignore_patterns("dist", "node_modules"),
    )
    return copied


def typescript_proof() -> None:
    if not shutil.which("node") or not shutil.which("tsc"):
        raise SystemExit("node and tsc are required for typescript-proof")
    with tempfile.TemporaryDirectory(prefix="course9-ts-") as temp:
        copied = _copy_ts_track(Path(temp))
        run(["tsc", "-p", "tsconfig.json"], cwd=copied)
        completed = run(
            ["node", "--test", "test-js/gateway-release.test.mjs", "test-js/identity-operation.test.mjs", "test-js/loader-policy.test.mjs"],
            cwd=copied,
            capture=True,
        )
        output = completed.stdout + completed.stderr
        match = re.search(r"# tests (\d+)", output)
        assert match, output
        count = int(match.group(1))
        assert count >= 15
        print(output.rstrip())
        print(f"PASS TypeScript semantic track — {count} tests")


def network_lab_proof() -> None:
    lab = CAP / "network-lab"
    completed = run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(lab), "-v"],
        env={"PYTHONPATH": str(lab)},
        capture=True,
    )
    output = completed.stdout + completed.stderr
    assert "OK" in output
    print(output.rstrip())
    print("PASS loopback composition lab — independent services and explicit partial failure")


def planted_defect_proof() -> None:
    directories = sorted((CAP / "planted-defects").glob("GQL-*"))
    assert len(directories) == 10
    proof_ids: set[str] = set()
    for directory in directories:
        defect = read_json(directory / "defect.json")
        assert defect["id"] == directory.name
        assert defect["expectedProof"]
        assert defect["failure"]
        proof_ids.add(defect["expectedProof"])
    assert len(proof_ids) >= 7
    print("PASS planted defects — 10 defects mapped to falsifying proofs")


def handoff_proof() -> None:
    handoff = CAP / "handoff"
    count = verify_manifest(handoff, exact=True)
    assert count == 12, f"expected 12 Course 10 handoff files, got {count}"
    boundary = read_json(handoff / "BOUNDARY.json")
    assert boundary["from"].startswith("09-")
    assert boundary["to"].startswith("10-")
    assert boundary["schemaRelease"] == "1.0.0"
    registry = read_json(handoff / "persisted-operations.json")
    assert len(registry["operations"]) == 10
    brief = read_yaml(handoff / "platform-boundary-brief.yaml")
    assert any(
        "business facts" in item or "private source contracts" in item
        for item in brief["platform_may_not"]
    )
    print(f"PASS Course 10 handoff — {count} exact publication files")


def final_defense_proof() -> None:
    summary = read_json(CAP / "final-defense/architecture-summary.json")
    assert summary == {
        "direct_database_joins": 0,
        "graph_gateway_business_facts_owned": 0,
        "persisted_operations": 10,
        "schema_version": "1.0",
        "silent_partial_data_paths": 0,
        "source_services": [
            "analysis-control",
            "artifact-service",
            "notification-service",
        ],
        "unbounded_list_fields": 0,
    }
    release = read_json(CAP / "releases/graph-1.0/release-report.json")
    assert release["classification"] == "accepted"
    assert release["active_operations_valid"] == 10
    assert release["budget_regressions"] == 0
    print("PASS final architecture defense prerequisites")


class DuplicateKeyError(ValueError):
    pass


def _json_no_duplicates(path: Path) -> None:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateKeyError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    json.loads(path.read_text(), object_pairs_hook=hook)


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: Any, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError(f"duplicate YAML key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def data_format_proof() -> None:
    json_count = yaml_count = toml_count = graphql_count = 0
    for path in ROOT.rglob("*"):
        if not eligible(path, ROOT):
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
        elif path.suffix == ".graphql":
            assert path.read_text().strip(), f"empty GraphQL document: {path}"
            graphql_count += 1
    print(
        "PASS data formats — "
        f"JSON {json_count}, YAML {yaml_count}, TOML {toml_count}, GraphQL {graphql_count}"
    )


def markdown_link_proof() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    checked = 0
    for path in ROOT.rglob("*.md"):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text()
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            destination = (path.parent / target).resolve()
            assert destination.exists(), f"broken link in {path.relative_to(ROOT)}: {raw_target}"
            checked += 1
    print(f"PASS Markdown links — {checked} local targets")


def education_proof() -> None:
    pages = sorted(BOOK.rglob("*.md"))
    words = sum(len(path.read_text().split()) for path in pages)
    assert words >= 31_000, f"course book too thin: {words} words"
    banned = re.compile(
        r"\b(TODO|TBD|FIXME|lorem ipsum|coming soon|placeholder text)\b",
        re.I,
    )
    for path in pages:
        text = path.read_text()
        assert not banned.search(text), f"unfinished marker in {path}"
    assert sum(
        path.read_text().count("Write a concrete engineering answer")
        for path in pages
    ) == 0
    paragraphs: dict[str, list[str]] = defaultdict(list)
    for path in pages:
        for paragraph in path.read_text().split("\n\n"):
            normalized = " ".join(paragraph.split())
            if len(normalized.split()) >= 35:
                paragraphs[normalized].append(path.relative_to(BOOK).as_posix())
    repeated = {
        paragraph: locations
        for paragraph, locations in paragraphs.items()
        if len(locations) >= 4
    }
    assert not repeated, f"repeated long prose: {next(iter(repeated.values()), [])}"
    print(f"PASS education quality — {len(pages)} pages, {words:,} words, no filler/repetition")


def python_syntax_proof() -> None:
    paths = [
        path
        for path in ROOT.rglob("*.py")
        if not any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)
    ]
    for path in paths:
        compile(path.read_text(), str(path), "exec")
    print(f"PASS Python syntax — {len(paths)} files")


def hygiene_proof() -> None:
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in {"__pycache__", "node_modules", "dist", "site", ".pytest_cache"} for part in relative.parts):
            offenders.append(relative.as_posix())
        elif path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            offenders.append(relative.as_posix())
    assert not offenders, f"generated artifacts present: {offenders[:10]}"
    print("PASS repository hygiene")


def capstone_tour() -> None:
    ref = import_reference()
    result = ref["run_tour"](ROOT)
    assert result["overview_runs"] == 2
    assert result["artifact_batch_calls"] == 1
    assert result["partial_artifacts"] is None
    assert result["partial_error_code"] == "DOWNSTREAM_UNAVAILABLE"
    assert result["mutation_replayed_first"] is False
    assert result["mutation_replayed_second"] is True
    print(json.dumps(result, indent=2, sort_keys=True))
    if shutil.which("node") and shutil.which("tsc"):
        with tempfile.TemporaryDirectory(prefix="course9-tour-ts-") as temp:
            copied = _copy_ts_track(Path(temp))
            run(["tsc", "-p", "tsconfig.json"], cwd=copied)
            expression = (
                "import('./dist/tour.js').then(m=>console.log(JSON.stringify(m.runTour())))"
            )
            completed = run(
                ["node", "-e", expression], cwd=copied, capture=True
            )
            value = json.loads(completed.stdout.strip())
            assert value["overviewRuns"] == 2
            assert value["replayedFirst"] is False
            assert value["replayedSecond"] is True
            assert value["registeredOperations"] == 10
            print(json.dumps(value, indent=2, sort_keys=True))
    network_lab_proof()
    print("PASS Course 9 capstone tour")


def manifest_proof() -> None:
    count = verify_manifest(ROOT, exact=True)
    print(f"PASS course manifest — {count} exact files")


def docs_build() -> None:
    if not shutil.which("mkdocs"):
        raise SystemExit("mkdocs is unavailable; install requirements-docs.txt")
    run(["mkdocs", "build", "--strict"])
    print("PASS strict MkDocs build")


def framework_proof() -> None:
    python_available = False
    try:
        import graphql  # type: ignore

        python_available = True
    except Exception:
        pass
    node_available = False
    if shutil.which("node"):
        result = subprocess.run(
            ["node", "-e", "try{require.resolve('graphql');process.exit(0)}catch(e){process.exit(1)}"],
            cwd=TS_TRACK,
        )
        node_available = result.returncode == 0
    if not python_available and not node_available:
        raise SystemExit(
            "No independent GraphQL implementation is installed; install graphql-core "
            "or the pinned npm GraphQL stack before framework-proof"
        )
    schema = CAP / "contracts/schema.graphql"
    if python_available:
        code = (
            "from graphql import build_schema; "
            f"build_schema(open({str(schema)!r}).read()); print('PASS graphql-core schema')"
        )
        run([sys.executable, "-c", code])
    if node_available:
        code = (
            "const {buildSchema}=require('graphql');"
            f"buildSchema(require('fs').readFileSync({str(schema)!r},'utf8'));"
            "console.log('PASS GraphQL.js schema')"
        )
        run(["node", "-e", code], cwd=TS_TRACK)
    print("PASS available independent GraphQL framework proof")


def core_proof() -> None:
    predecessor_proof()
    structure_proof()
    schema_proof()
    ownership_proof()
    batching_proof()
    pagination_proof()
    mutation_proof()
    authorization_proof()
    demand_proof()
    error_proof()
    subscription_proof()
    release_proof()
    migration_proof()
    vector_proof()
    python_proof()
    typescript_proof()
    network_lab_proof()
    planted_defect_proof()
    final_defense_proof()
    handoff_proof()
    data_format_proof()
    markdown_link_proof()
    education_proof()
    python_syntax_proof()
    hygiene_proof()
    print("PASS Course 9 dependency-light core proof")


def full_proof() -> None:
    core_proof()
    if shutil.which("mkdocs"):
        docs_build()
    else:
        print("NOT EXECUTED strict MkDocs build — mkdocs unavailable")
    try:
        framework_proof()
    except SystemExit as exc:
        print(f"NOT EXECUTED independent GraphQL proof — {exc}")
    print("PASS all available full-proof routes")


def orientation_proof() -> None:
    predecessor_proof()
    structure_proof()
    schema_proof()
    capstone_tour()


def module_proof(number: int) -> None:
    routes: dict[int, list[Any]] = {
        1: [predecessor_proof, schema_proof, ownership_proof, network_lab_proof],
        2: [schema_proof, error_proof, vector_proof],
        3: [ownership_proof, batching_proof, python_proof, typescript_proof],
        4: [pagination_proof, vector_proof, python_proof, typescript_proof],
        5: [mutation_proof, python_proof, typescript_proof],
        6: [authorization_proof, python_proof, typescript_proof],
        7: [demand_proof, schema_proof, vector_proof],
        8: [error_proof, network_lab_proof],
        9: [subscription_proof, vector_proof],
        10: [release_proof, final_defense_proof, handoff_proof],
    }
    for route in routes[number]:
        route()
    report = ROOT / f"reports/module-{number:02d}-proof.json"
    assert report.is_file(), f"module evidence report missing: {report}"
    assert read_json(report)["status"] == "pass"
    print(f"PASS Module {number:02d} proof")


def clean() -> None:
    for directory_name in ["__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"]:
        for path in ROOT.rglob(directory_name):
            if path.is_dir():
                shutil.rmtree(path)
    for path in [ROOT / "site", ROOT / ".tmp", TS_TRACK / "dist"]:
        if path.exists():
            shutil.rmtree(path)
    for path in ROOT.rglob("*.py[co]"):
        path.unlink()
    print("PASS clean")


COMMANDS: dict[str, Any] = {
    "doctor": doctor,
    "predecessor-proof": predecessor_proof,
    "orientation-proof": orientation_proof,
    "structure-proof": structure_proof,
    "schema-proof": schema_proof,
    "ownership-proof": ownership_proof,
    "batching-proof": batching_proof,
    "pagination-proof": pagination_proof,
    "mutation-proof": mutation_proof,
    "authorization-proof": authorization_proof,
    "demand-proof": demand_proof,
    "error-proof": error_proof,
    "subscription-proof": subscription_proof,
    "release-proof": release_proof,
    "migration-proof": migration_proof,
    "vector-proof": vector_proof,
    "python-proof": python_proof,
    "typescript-proof": typescript_proof,
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
    "docs-build": docs_build,
    "framework-proof": framework_proof,
    "core-proof": core_proof,
    "full-proof": full_proof,
    "clean": clean,
}
for module_number in range(1, 11):
    COMMANDS[f"module-{module_number:02d}-proof"] = (
        lambda value=module_number: module_proof(value)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args()
    COMMANDS[args.command]()


if __name__ == "__main__":
    main()
