#!/usr/bin/env python3
"""Deterministic proof and maintenance routes for Course 2.

Every proof states its boundary. Dependency-light checks run without Docker or
PostgreSQL; live transaction and process-failure claims belong to the separate
runtime proof runner and are never converted into false passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # pragma: no cover - doctor reports the missing module
    yaml = None

from compatibility import compare_contracts

ROOT = Path(__file__).resolve().parents[2]
CAPSTONE = ROOT / "capstone"
PREDECESSOR = ROOT / "predecessor"
REPORTS = CAPSTONE / "reports"
RELEASES = CAPSTONE / "releases"
PYTHON_TRACK = CAPSTONE / "tracks" / "python-fastapi"
TYPESCRIPT_TRACK = CAPSTONE / "tracks" / "typescript-fastify"
HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


class ProofFailure(RuntimeError):
    """A machine-checkable course guarantee did not hold."""


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> None:
    print("+", " ".join(command))
    completed = subprocess.run(command, cwd=cwd, env=env, text=True)
    if completed.returncode:
        raise ProofFailure(
            f"command failed with exit code {completed.returncode}: "
            + " ".join(command)
        )


def write_report(name: str, payload: dict) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise ProofFailure("PyYAML is required for this proof")
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProofFailure(f"expected a YAML mapping: {path}")
    return value


def predecessor_proof() -> dict:
    manifest_path = PREDECESSOR / "MANIFEST.json"
    checksum_path = PREDECESSOR / "MANIFEST.sha256"
    if not manifest_path.is_file() or not checksum_path.is_file():
        raise ProofFailure("predecessor manifest is incomplete")
    expected_checksum = checksum_path.read_text().split()[0]
    if expected_checksum != digest(manifest_path):
        raise ProofFailure("predecessor MANIFEST.sha256 does not match MANIFEST.json")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    for item in manifest["files"]:
        path = PREDECESSOR / item["path"]
        if not path.is_file():
            failures.append(f"missing: {item['path']}")
            continue
        if path.stat().st_size != item["size"]:
            failures.append(f"size changed: {item['path']}")
        if digest(path) != item["sha256"]:
            failures.append(f"digest changed: {item['path']}")

    listed = {item["path"] for item in manifest["files"]}
    actual = {
        path.relative_to(PREDECESSOR).as_posix()
        for path in PREDECESSOR.rglob("*")
        if path.is_file() and path.name not in {"MANIFEST.json", "MANIFEST.sha256"}
    }
    if actual - listed:
        failures.append(
            "unmanifested predecessor files: " + ", ".join(sorted(actual - listed))
        )
    if listed - actual:
        failures.append(
            "manifest entries missing on disk: " + ", ".join(sorted(listed - actual))
        )
    if failures:
        raise ProofFailure("predecessor handoff changed:\n" + "\n".join(failures))

    baseline = load_yaml(PREDECESSOR / "spec" / "dist" / "openapi.bundle.yaml")
    if baseline.get("info", {}).get("version") != "1.1.0":
        raise ProofFailure("Course 2 predecessor must be public API 1.1.0")
    payload = {
        "status": "passed",
        "files": len(listed),
        "manifestSha256": digest(manifest_path),
        "publicApiVersion": "1.1.0",
    }
    write_report("predecessor-proof.json", payload)
    return payload


def operation_ids(document: dict) -> set[str]:
    result: set[str] = set()
    for item in (document.get("paths") or {}).values():
        if not isinstance(item, dict):
            continue
        for method, operation in item.items():
            if (
                str(method).lower() in HTTP_METHODS
                and isinstance(operation, dict)
                and isinstance(operation.get("operationId"), str)
            ):
                result.add(operation["operationId"])
        for operation in (item.get("additionalOperations") or {}).values():
            if isinstance(operation, dict) and isinstance(operation.get("operationId"), str):
                result.add(operation["operationId"])
    return result


def operation_proof() -> dict:
    mapping_document = load_yaml(CAPSTONE / "shared" / "operation-map.yaml")
    baseline_mapping = mapping_document.get("operations") or {}
    extension_mapping = mapping_document.get("releaseExtensions") or {}
    if not isinstance(baseline_mapping, dict) or not isinstance(extension_mapping, dict):
        raise ProofFailure("operation map sections must be mappings")

    predecessor = load_yaml(PREDECESSOR / "spec" / "dist" / "openapi.bundle.yaml")
    api_1_2 = load_yaml(RELEASES / "api-1.2" / "openapi.bundle.yaml")
    baseline = operation_ids(predecessor)
    accepted = operation_ids(api_1_2)
    extensions = accepted - baseline

    if baseline != set(baseline_mapping):
        raise ProofFailure(
            "baseline operation map mismatch: "
            f"missing={sorted(baseline-set(baseline_mapping))} "
            f"extra={sorted(set(baseline_mapping)-baseline)}"
        )
    if extensions != set(extension_mapping):
        raise ProofFailure(
            "release-extension operation map mismatch: "
            f"missing={sorted(extensions-set(extension_mapping))} "
            f"extra={sorted(set(extension_mapping)-extensions)}"
        )

    sources = {
        "python": (PYTHON_TRACK / "src" / "analysis_service" / "app.py").read_text(),
        "typescript": (TYPESCRIPT_TRACK / "src" / "app.ts").read_text(),
    }
    patterns = {
        "python": r"operation_id\s*=\s*['\"]{operation_id}['\"]",
        "typescript": r"operationId\s*:\s*['\"]{operation_id}['\"]",
    }
    for language, source in sources.items():
        for operation_id in baseline | extensions:
            expression = patterns[language].format(
                operation_id=re.escape(operation_id)
            )
            count = len(re.findall(expression, source))
            if count != 1:
                raise ProofFailure(
                    f"{language} owns {operation_id} {count} times; expected exactly once"
                )

    payload = {
        "status": "passed",
        "baselineOperations": len(baseline),
        "releaseExtensions": sorted(extensions),
        "languages": sorted(sources),
    }
    write_report("operation-proof.json", payload)
    return payload


def migration_proof() -> dict:
    shared = CAPSTONE / "shared" / "sql"
    track_dirs = {
        "python": PYTHON_TRACK / "migrations",
        "typescript": TYPESCRIPT_TRACK / "migrations",
    }
    filenames = {
        language: sorted(path.name for path in directory.glob("[0-9][0-9][0-9]_*.sql"))
        for language, directory in track_dirs.items()
    }
    if filenames["python"] != filenames["typescript"]:
        raise ProofFailure("reference migration histories have different filenames")
    expected = filenames["python"]
    required_sequence = [
        "001_base.sql",
        "002_indexes.sql",
        "003_expand_result_summary.sql",
        "004_backfill_result_summary.sql",
        "005_enforce_result_summary.sql",
    ]
    if expected != required_sequence:
        raise ProofFailure(f"unexpected migration sequence: {expected}")

    parity: dict[str, dict[str, str]] = {}
    for name in expected:
        values = {
            language: digest(directory / name)
            for language, directory in track_dirs.items()
        }
        parity[name] = values
        if len(set(values.values())) != 1:
            raise ProofFailure(f"migration {name} differs between reference tracks")

    for name in required_sequence[:2]:
        if digest(shared / name) != parity[name]["python"]:
            raise ProofFailure(f"shared SQL differs from track migration: {name}")
    release_migrations = RELEASES / "api-1.2" / "migrations"
    for name in required_sequence[2:]:
        if digest(release_migrations / name) != parity[name]["python"]:
            raise ProofFailure(f"release migration differs from track history: {name}")

    base = (shared / "001_base.sql").read_text(encoding="utf-8")
    required_fragments = [
        "PRIMARY KEY(owner_id,operation_id,idempotency_key)",
        "lease_generation bigint",
        "CREATE TABLE outbox_events",
        "FOREIGN KEY(dataset_id,project_id,owner_id)",
        "CREATE TABLE pagination_cursors",
        "snapshot_position bigint",
    ]
    absent = [fragment for fragment in required_fragments if fragment not in base]
    if absent:
        raise ProofFailure(
            "baseline SQL omits required guarantees: " + ", ".join(absent)
        )

    payload = {
        "status": "passed",
        "migrations": expected,
        "sha256": parity,
        "axes": {
            "service": ["1.0", "1.1"],
            "publicApi": ["1.1.0", "1.2.0"],
            "database": ["001", "002", "003", "004", "005"],
        },
    }
    write_report("migration-proof.json", payload)
    return payload


def vector_proof() -> dict:
    parsed: dict[str, int] = {}
    for path in sorted((CAPSTONE / "shared").glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        parsed[path.name] = len(value) if hasattr(value, "__len__") else 1
    for path in [
        CAPSTONE / "shared" / "operation-map.yaml",
        PREDECESSOR / "behavioral-scenarios.yaml",
        PREDECESSOR / "scope-matrix.yaml",
    ]:
        load_yaml(path)
    payload = {"status": "passed", "jsonVectors": parsed, "yamlAssets": 3}
    write_report("vector-proof.json", payload)
    return payload


def python_proof() -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(PYTHON_TRACK / "src"), str(CAPSTONE / "webhook-receiver")]
    )
    tests = sorted(str(path) for path in (PYTHON_TRACK / "tests").glob("test_*.py"))
    tests.append(str(CAPSTONE / "webhook-receiver" / "test_receiver.py"))
    test_command = [sys.executable, "-m", "pytest", "-q", *tests]
    print("+", " ".join(test_command))
    completed = subprocess.run(
        test_command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode:
        raise ProofFailure("Python core tests failed")
    passed_match = re.search(r"(\d+) passed", completed.stdout)
    skipped_match = re.search(r"(\d+) skipped", completed.stdout)
    if not passed_match:
        raise ProofFailure("could not read executed Python test count from pytest")
    run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            str(PYTHON_TRACK / "src"),
            str(CAPSTONE / "webhook-receiver"),
        ]
    )
    payload = {
        "status": "passed",
        "testFiles": [
            Path(name).relative_to(ROOT).as_posix() for name in tests
        ],
        "testCasesPassed": int(passed_match.group(1)),
        "testCasesSkipped": int(skipped_match.group(1)) if skipped_match else 0,
        "python": platform.python_version(),
        "databaseIntegration": (
            "executed" if os.getenv("TEST_DATABASE_URL") else "skipped-no-TEST_DATABASE_URL"
        ),
    }
    write_report("python-core-proof.json", payload)
    return payload


def typescript_core_proof() -> dict:
    tsc = shutil.which("tsc")
    node = shutil.which("node")
    if not tsc or not node:
        raise ProofFailure("node and tsc are required for the dependency-light proof")
    run([tsc, "-p", "tsconfig.core.json"], cwd=TYPESCRIPT_TRACK)
    tests = sorted((TYPESCRIPT_TRACK / "test-core").glob("*.test.mjs"))
    command = [node, "--test", *[str(path) for path in tests]]
    print("+", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=TYPESCRIPT_TRACK,
        text=True,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode:
        raise ProofFailure("TypeScript core tests failed")
    match = re.search(r"(?m)^# tests (\d+)\s*$", completed.stdout)
    if not match:
        raise ProofFailure("could not read executed TypeScript test count from TAP")
    payload = {
        "status": "passed",
        "testFiles": len(tests),
        "testCasesExecuted": int(match.group(1)),
        "node": subprocess.check_output([node, "--version"], text=True).strip(),
    }
    write_report("typescript-core-proof.json", payload)
    return payload


def typescript_syntax_proof() -> dict:
    node = shutil.which("node")
    tsc = shutil.which("tsc")
    if not node or not tsc:
        raise ProofFailure("node and tsc are required for TypeScript syntax proof")
    compiler = Path(tsc).resolve().parents[1] / "lib" / "typescript.js"
    if not compiler.is_file():
        raise ProofFailure(f"cannot locate TypeScript compiler library: {compiler}")
    env = os.environ.copy()
    env["TYPESCRIPT_LIB"] = str(compiler)
    script = CAPSTONE / "scripts" / "ts_syntax_check.mjs"
    completed = subprocess.run(
        [node, str(script), str(TYPESCRIPT_TRACK)],
        text=True,
        capture_output=True,
        env=env,
    )
    if completed.returncode:
        raise ProofFailure("TypeScript syntax proof failed:\n" + completed.stderr)
    result = json.loads(completed.stdout.strip())
    # Compile all TypeScript sources and tests against deliberately narrow
    # dependency shims. This catches duplicate declarations, broken internal
    # imports, unsafe narrowing, and cross-file type errors without claiming
    # that third-party package declarations were checked. The authoritative
    # dependency-backed proof remains `npm run typecheck`.
    run(
        [tsc, "-p", "tsconfig.audit.json", "--pretty", "false"],
        cwd=TYPESCRIPT_TRACK,
    )
    payload = {
        "status": "passed",
        "files": result["files"],
        "semanticAudit": "passed-with-course-owned-dependency-shims",
        "authoritativeDependencyTypecheck": "separate-npm-gate",
    }
    write_report("typescript-syntax-proof.json", payload)
    return payload


def compatibility_self_test() -> dict:
    def contract(request: dict, response: dict) -> dict:
        return {
            "openapi": "3.1.2",
            "info": {"title": "fixture", "version": "1.0.0"},
            "paths": {
                "/items": {
                    "post": {
                        "operationId": "createItem",
                        "security": [],
                        "requestBody": {
                            "required": True,
                            "content": {"application/json": {"schema": request}},
                        },
                        "responses": {
                            "200": {
                                "description": "ok",
                                "content": {"application/json": {"schema": response}},
                            }
                        },
                    }
                }
            },
        }

    old_request = {
        "type": "object",
        "additionalProperties": False,
        "required": ["mode"],
        "properties": {"mode": {"type": "string", "enum": ["a", "b"]}},
    }
    old_response = {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "ownerId"],
        "properties": {
            "id": {"type": "string"},
            "ownerId": {"type": "string"},
        },
    }
    new_request = json.loads(json.dumps(old_request))
    new_request["required"].append("callbackUrl")
    new_request["properties"]["callbackUrl"] = {"type": "string"}
    new_request["properties"]["mode"]["enum"] = ["a"]
    new_response = json.loads(json.dumps(old_response))
    new_response["properties"].pop("ownerId")
    new_response["required"].remove("ownerId")
    result = compare_contracts(
        contract(old_request, old_response),
        contract(new_request, new_response),
    )
    reasons = {item["reason"] for item in result["breaking"]}
    required = {
        "request property became required",
        "request enum narrowed",
        "required response property removed or made optional",
        "response property removed",
    }
    if not required.issubset(reasons):
        raise ProofFailure(
            "compatibility engine self-test missed planted breaks: "
            + ", ".join(sorted(required - reasons))
        )

    additive_response = json.loads(json.dumps(old_response))
    additive_response["properties"]["summary"] = {
        "type": ["object", "null"],
        "additionalProperties": False,
    }
    review = compare_contracts(
        contract(old_request, old_response),
        contract(old_request, additive_response),
    )
    if review["breaking"] or not review["risky"]:
        raise ProofFailure("response-addition self-test was not classified as review-required")
    return {"status": "passed", "plantedBreaks": len(required)}


def release_proof() -> dict:
    self_test = compatibility_self_test()
    baseline = load_yaml(RELEASES / "api-1.1" / "openapi.bundle.yaml")
    accepted = load_yaml(RELEASES / "api-1.2" / "openapi.bundle.yaml")
    rejected = load_yaml(
        RELEASES
        / "rejected-api-1.2-breaking-candidate"
        / "openapi.bundle.yaml"
    )
    if baseline.get("info", {}).get("version") != "1.1.0":
        raise ProofFailure("baseline release is not public API 1.1.0")
    if accepted.get("info", {}).get("version") != "1.2.0":
        raise ProofFailure("accepted release is not public API 1.2.0")

    accepted_result = compare_contracts(baseline, accepted)
    if accepted_result["breaking"]:
        raise ProofFailure(
            "accepted API 1.2.0 contains breaking changes:\n"
            + json.dumps(accepted_result["breaking"], indent=2)
        )
    if not any(
        item["location"] == "GET /artifacts/{artifactId}/content"
        and item["reason"] == "operation added"
        for item in accepted_result["additive"]
    ):
        raise ProofFailure("accepted release did not expose the additive content operation")
    if not any("resultSummary" in item["location"] for item in accepted_result["risky"]):
        raise ProofFailure("resultSummary response addition was not surfaced for review")

    rejected_result = compare_contracts(baseline, rejected)
    reasons = [item["reason"] for item in rejected_result["breaking"]]
    locations = [item["location"] for item in rejected_result["breaking"]]
    expectations = {
        "callbackUrl required": any(
            "callbackUrl" in location and reason == "request property became required"
            for location, reason in zip(locations, reasons)
        ),
        "request enum narrowed": "request enum narrowed" in reasons,
        "ownerId removed": any(
            "ownerId" in location and reason in {
                "response property removed",
                "required response property removed or made optional",
            }
            for location, reason in zip(locations, reasons)
        ),
    }
    missing = [name for name, present in expectations.items() if not present]
    if missing:
        raise ProofFailure(
            "rejected release did not expose planted breaks: " + ", ".join(missing)
        )

    payload = {
        "status": "passed",
        "selfTest": self_test,
        "accepted": accepted_result,
        "rejected": rejected_result,
        "versionAxes": {
            "openapiSpecification": "3.1.2",
            "publicApi": ["1.1.0", "1.2.0"],
            "service": ["1.0", "1.1"],
            "database": ["002", "003", "004", "005"],
        },
    }
    write_report("release-proof.json", payload)
    return payload


def markdown_link_proof() -> dict:
    failures: list[str] = []
    pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    checked = 0
    markdown_files = list(ROOT.rglob("*.md"))
    for source in markdown_files:
        text = source.read_text(errors="replace")
        for raw in pattern.findall(text):
            target = raw.strip().split(" ", 1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            checked += 1
            path = (source.parent / target).resolve()
            if not path.exists():
                failures.append(f"{source.relative_to(ROOT)} -> {raw}")
    if failures:
        raise ProofFailure("broken local Markdown links:\n" + "\n".join(failures[:100]))
    payload = {
        "status": "passed",
        "links": checked,
        "markdownFiles": len(markdown_files),
    }
    write_report("markdown-link-proof.json", payload)
    return payload


def course_structure_proof() -> dict:
    book = ROOT / "course-book"
    required_guides = [
        book / 'index.md', book / 'start-here.md', book / 'study-plan.md',
        book / 'capstone.md', book / 'standards.md', book / 'glossary.md',
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_guides if not path.is_file()]
    modules = sorted(path for path in book.glob("module-[0-9][0-9]-*") if path.is_dir())
    if len(modules) != 11:
        missing.append(f"expected module 00 plus ten modules; found {len(modules)}")
    required_module_files = [
        "index.md",
        "exercises.md",
        "exercise-answers.md",
        "lab.md",
        "checkpoint.md",
    ]
    for module in modules:
        if module.name.startswith("module-00-"):
            if not (module / "index.md").is_file():
                missing.append(f"{module.name}/index.md")
            continue
        for name in required_module_files:
            if not (module / name).is_file():
                missing.append(f"{module.name}/{name}")
    if missing:
        raise ProofFailure("course structure incomplete:\n" + "\n".join(missing))

    exercise_questions = 0
    for module in modules[1:]:
        text = (module / "exercises.md").read_text(encoding="utf-8")
        count = len(re.findall(r"(?m)^##\s+\d+\.", text))
        if count < 8:
            raise ProofFailure(f"{module.name} has only {count} numbered exercises")
        exercise_questions += count
    payload = {
        "status": "passed",
        "modules": len(modules) - 1,
        "orientation": True,
        "numberedExercises": exercise_questions,
        "markdownFiles": len(list(book.rglob("*.md"))),
    }
    write_report("course-structure-proof.json", payload)
    return payload


def hygiene_proof() -> dict:
    forbidden_names = {
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        ".mypy_cache",
        ".ruff_cache",
        ".git",
    }
    forbidden_suffixes = {".pyc", ".pyo"}
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in forbidden_names for part in relative.parts):
            failures.append(str(relative))
        if path.is_file() and path.suffix in forbidden_suffixes:
            failures.append(str(relative))
    marker = re.compile(r"(?im)^\s*(TODO|FIXME|TBD)\s*[:\-]")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {
            ".md", ".py", ".ts", ".sql", ".yaml", ".yml"
        }:
            if marker.search(path.read_text(errors="replace")):
                failures.append(f"unresolved marker: {path.relative_to(ROOT)}")
    if failures:
        raise ProofFailure(
            "repository hygiene failures:\n" + "\n".join(sorted(set(failures))[:100])
        )
    payload = {
        "status": "passed",
        "files": sum(1 for path in ROOT.rglob("*") if path.is_file()),
    }
    write_report("hygiene-proof.json", payload)
    return payload


def doctor() -> dict:
    tools = {}
    for name in ["python3", "node", "npm", "tsc", "docker", "psql", "git"]:
        path = shutil.which(name)
        tools[name] = {"available": bool(path), "path": path}
    modules = {}
    for name in ["yaml", "pytest", "fastapi", "pydantic", "psycopg", "httpx"]:
        try:
            module = __import__(name)
            modules[name] = {
                "available": True,
                "version": getattr(module, "__version__", "unknown"),
            }
        except Exception as exc:  # pragma: no cover - environment dependent
            modules[name] = {"available": False, "reason": type(exc).__name__}
    payload = {
        "status": "informational",
        "platform": platform.platform(),
        "tools": tools,
        "pythonModules": modules,
    }
    write_report("doctor.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def clean_generated() -> None:
    for name in ["__pycache__", ".pytest_cache", "dist-core"]:
        for path in ROOT.rglob(name):
            if path.is_dir():
                shutil.rmtree(path)
    for path in ROOT.rglob("*.py[co]"):
        path.unlink(missing_ok=True)


def core_proof() -> dict:
    results = {
        "predecessor": predecessor_proof(),
        "operations": operation_proof(),
        "migrations": migration_proof(),
        "vectors": vector_proof(),
        "release": release_proof(),
        "python": python_proof(),
        "typescriptCore": typescript_core_proof(),
        "typescriptSyntax": typescript_syntax_proof(),
        "structure": course_structure_proof(),
        "links": markdown_link_proof(),
    }
    clean_generated()
    results["hygiene"] = hygiene_proof()
    payload = {
        "status": "passed",
        "proofs": {key: value["status"] for key, value in results.items()},
    }
    write_report("core-proof.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def _manifest_payload_files() -> list[Path]:
    excluded_parts = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        ".venv",
        ".runtime",
        "dist-core",
        "site",
    }
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if relative.as_posix() in {"MANIFEST.json", "MANIFEST.sha256"}:
            continue
        if any(part in excluded_parts for part in relative.parts):
            continue
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def _file_mode(path: Path) -> str:
    return format(path.stat().st_mode & 0o7777, "04o")


def make_manifest() -> dict:
    files = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "mode": _file_mode(path),
            "sha256": digest(path),
        }
        for path in _manifest_payload_files()
    ]
    manifest = {
        "format": 1,
        "root": ROOT.name,
        "scope": (
            "All distributable payload files except this manifest pair and "
            "generated dependency/cache/site directories."
        ),
        "files": files,
    }
    target = ROOT / "MANIFEST.json"
    target.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (ROOT / "MANIFEST.sha256").write_text(
        f"{digest(target)}  MANIFEST.json\n",
        encoding="utf-8",
    )
    return {"files": len(files), "manifestSha256": digest(target)}


def verify_manifest() -> dict:
    path = ROOT / "MANIFEST.json"
    checksum = ROOT / "MANIFEST.sha256"
    if not path.is_file() or not checksum.is_file():
        raise ProofFailure("course manifest does not exist; run manifest-create")
    if checksum.read_text(encoding="utf-8").split()[0] != digest(path):
        raise ProofFailure("MANIFEST.sha256 does not match MANIFEST.json")

    manifest = json.loads(path.read_text(encoding="utf-8"))
    expected = {item["path"]: item for item in manifest["files"]}
    current = {
        path.relative_to(ROOT).as_posix(): {
            "bytes": path.stat().st_size,
            "mode": _file_mode(path),
            "sha256": digest(path),
        }
        for path in _manifest_payload_files()
    }
    if expected.keys() != current.keys():
        raise ProofFailure(
            "manifest file set differs: "
            f"missing={sorted(expected.keys() - current.keys())[:10]}, "
            f"unexpected={sorted(current.keys() - expected.keys())[:10]}"
        )
    for name, item in expected.items():
        wanted = {
            "bytes": item["bytes"],
            "mode": item["mode"],
            "sha256": item["sha256"],
        }
        if current[name] != wanted:
            raise ProofFailure(f"manifest mismatch: {name}")
    return {
        "status": "passed",
        "files": len(expected),
        "manifestSha256": digest(path),
    }


def main() -> None:
    commands = {
        "doctor": doctor,
        "predecessor-proof": predecessor_proof,
        "operation-proof": operation_proof,
        "migration-proof": migration_proof,
        "vector-proof": vector_proof,
        "release-proof": release_proof,
        "python-proof": python_proof,
        "typescript-core-proof": typescript_core_proof,
        "typescript-syntax-proof": typescript_syntax_proof,
        "course-structure-proof": course_structure_proof,
        "markdown-link-proof": markdown_link_proof,
        "hygiene-proof": hygiene_proof,
        "core-proof": core_proof,
        "manifest-create": make_manifest,
        "manifest-proof": verify_manifest,
    }
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=sorted(commands))
    command = parser.parse_args().command
    try:
        result = commands[command]()
        if command not in {"doctor", "core-proof"}:
            print(json.dumps(result, indent=2, sort_keys=True))
    except ProofFailure as exc:
        print(f"PROOF FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
