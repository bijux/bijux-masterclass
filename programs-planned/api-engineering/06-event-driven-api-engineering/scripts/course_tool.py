#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import stat
sys.dont_write_bytecode = True
import tempfile
import textwrap
from typing import Any, Callable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment diagnostic
    raise SystemExit(f"PyYAML is required for course proofs: {exc}")

ROOT = Path(__file__).resolve().parents[1]
CAPSTONE = ROOT / "capstone"
PY_TRACK = CAPSTONE / "tracks/python-fastapi"
TS_TRACK = CAPSTONE / "tracks/typescript-fastify"
COURSE_BOOK = ROOT / "course-book"


class ProofError(RuntimeError):
    pass


def pass_line(message: str) -> None:
    print(f"PASS {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProofError(message)


def file_mode(path: Path) -> str:
    return f"{stat.S_IMODE(path.stat().st_mode):04o}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], cwd: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    result = subprocess.run(command, cwd=cwd, env=merged, text=True, capture_output=True)
    if result.returncode:
        if result.stdout:
            print(result.stdout, end="", file=sys.stderr)
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        raise ProofError(f"command failed ({result.returncode}): {' '.join(command)}")
    if result.stdout.strip():
        print(result.stdout.rstrip())
    return result


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ProofError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_yaml(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ProofError(f"invalid YAML {path.relative_to(ROOT)}: {exc}") from exc


def _json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProofError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_json_pairs)
    except (json.JSONDecodeError, ProofError) as exc:
        raise ProofError(f"invalid JSON {path.relative_to(ROOT)}: {exc}") from exc


def words(path: Path) -> int:
    return len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))


def doctor() -> None:
    tools = {
        "python": shutil.which("python3"),
        "node": shutil.which("node"),
        "tsc": shutil.which("tsc"),
        "mkdocs": shutil.which("mkdocs"),
        "docker": shutil.which("docker"),
        "nats": shutil.which("nats"),
        "psql": shutil.which("psql"),
        "asyncapi": shutil.which("asyncapi"),
    }
    print(json.dumps(tools, indent=2, sort_keys=True))
    require(tools["python"] is not None, "python3 is required")
    pass_line("doctor — dependency-light Python route available")


def predecessor_proof() -> None:
    base = CAPSTONE / "predecessor/handoff"
    manifest_path = base / "MANIFEST.json"
    checksum_path = base / "MANIFEST.sha256"
    require(manifest_path.is_file() and checksum_path.is_file(), "predecessor manifest pair missing")
    expected_manifest_hash = checksum_path.read_text(encoding="utf-8").split()[0]
    require(sha256(manifest_path) == expected_manifest_hash, "predecessor MANIFEST.json digest mismatch")
    manifest = load_json(manifest_path)
    require(manifest.get("handoff") == "course-5-to-course-6", "wrong predecessor handoff identity")
    listed = set()
    for row in manifest.get("files", []):
        relative = row["path"]
        path = base / relative
        require(path.is_file(), f"predecessor file missing: {relative}")
        require(path.stat().st_size == row["size"], f"predecessor size mismatch: {relative}")
        require(sha256(path) == row["sha256"], f"predecessor digest mismatch: {relative}")
        require(file_mode(path) == row["mode"], f"predecessor mode mismatch: {relative}")
        listed.add(relative)
    actual = {
        path.relative_to(base).as_posix()
        for path in base.rglob("*")
        if path.is_file() and path.name not in {"MANIFEST.json", "MANIFEST.sha256"}
    }
    require(actual == listed, f"predecessor file-set mismatch: extra={sorted(actual-listed)}, missing={sorted(listed-actual)}")
    pass_line(f"Course 5 predecessor integrity — {len(listed)} files")



def orientation_proof() -> None:
    predecessor_proof()
    orientation = COURSE_BOOK / "module-00-orientation"
    require(words(orientation / "index.md") >= 500, "orientation chapter is too thin")
    lab = (orientation / "lab.md").read_text(encoding="utf-8")
    checkpoint = (orientation / "checkpoint.md").read_text(encoding="utf-8")
    require("make predecessor-proof" in checkpoint and "make capstone-tour" in checkpoint, "orientation does not establish the proof route")
    require((CAPSTONE / "event-case/event-profile.json").is_file(), "event profile missing")
    pass_line("orientation — predecessor locked, tracks and evidence classes established")

def structure_proof() -> None:
    require((ROOT / "README.md").is_file(), "README.md missing")
    pages = sorted(COURSE_BOOK.rglob("*.md"))
    require(len(pages) == 59, f"expected 59 course-book pages, found {len(pages)}")
    module_dirs = sorted(path for path in COURSE_BOOK.iterdir() if path.is_dir() and path.name.startswith("module-"))
    require(len(module_dirs) == 11, f"expected orientation plus ten modules, found {len(module_dirs)}")
    orientation = COURSE_BOOK / "module-00-orientation"
    require({p.name for p in orientation.glob("*.md")} == {"index.md", "lab.md", "checkpoint.md"}, "orientation file set is incomplete")
    for number in range(1, 11):
        matches = list(COURSE_BOOK.glob(f"module-{number:02d}-*"))
        require(len(matches) == 1, f"module {number:02d} directory missing or duplicated")
        module = matches[0]
        expected = {"index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"}
        require({p.name for p in module.glob("*.md")} == expected, f"module {number:02d} file set differs from authoritative five-page structure")
        ex = module / "exercises.md"
        ans = module / "exercise-answers.md"
        ex_numbers = re.findall(r"^##\s+(\d+)\.", ex.read_text(encoding="utf-8"), flags=re.M)
        an_numbers = re.findall(r"^##\s+(\d+)\.", ans.read_text(encoding="utf-8"), flags=re.M)
        require(ex_numbers == [str(i) for i in range(1, 13)], f"module {number:02d} does not have exercises 1–12")
        require(an_numbers == ex_numbers, f"module {number:02d} answer numbering does not match exercises")
        lab = (module / "lab.md").read_text(encoding="utf-8")
        for heading in ["Objective", "Setup conditions", "Failure action and investigation", "Operational oracle", "Required evidence", "Cleanup and reset", "Completion gate"]:
            require(f"## {heading}" in lab, f"module {number:02d} lab lacks {heading}")
    mkdocs = load_yaml(ROOT / "mkdocs.yml")
    nav_paths: set[str] = set()
    def collect_nav(value: Any) -> None:
        if isinstance(value, str):
            nav_paths.add(value)
        elif isinstance(value, list):
            for item in value:
                collect_nav(item)
        elif isinstance(value, dict):
            for item in value.values():
                collect_nav(item)
    collect_nav(mkdocs.get("nav", []))
    expected_nav = {path.relative_to(ROOT).as_posix() for path in pages}
    require(nav_paths == expected_nav, f"MkDocs navigation differs from course-book pages: extra={sorted(nav_paths-expected_nav)}, missing={sorted(expected_nav-nav_paths)}")
    pass_line("course structure — 59 navigated pages, ten modules, 120 exercises and answers")


def data_proof() -> None:
    json_count = yaml_count = 0
    for path in ROOT.rglob("*.json"):
        if any(part in {"node_modules", "dist", ".venv"} for part in path.parts):
            continue
        load_json(path); json_count += 1
    for suffix in ("*.yaml", "*.yml"):
        for path in ROOT.rglob(suffix):
            if any(part in {"node_modules", "dist", ".venv"} for part in path.parts):
                continue
            load_yaml(path); yaml_count += 1
    pass_line(f"duplicate-key-aware data parse — {json_count} JSON, {yaml_count} YAML")


def event_case_proof() -> None:
    profile = load_json(CAPSTONE / "event-case/event-profile.json")
    require(profile["asyncapi"] == "3.1.0" and profile["cloudEvents"] == "1.0", "event profile versions are inconsistent")
    taxonomy = load_yaml(CAPSTONE / "event-case/message-taxonomy.yaml")
    require(len(taxonomy.get("messages", [])) == 7, "message taxonomy must contain seven governed messages")
    names = [row["name"] for row in taxonomy["messages"]]
    require(len(names) == len(set(names)), "duplicate message taxonomy name")
    channel_policy = load_yaml(CAPSTONE / "event-case/channel-policy.yaml")
    require(len(channel_policy.get("channels", {})) == 3, "channel policy must define three primary channels")
    consumers = load_yaml(CAPSTONE / "event-case/consumer-catalog.yaml")
    require(len(consumers.get("consumers", [])) == 5, "consumer catalogue must define five owned consumers")
    compat = load_yaml(CAPSTONE / "event-case/compatibility-policy.yaml")
    require(compat["historicalPolicy"]["immutableBytes"] is True, "historical events must remain immutable")
    pass_line("event case — taxonomy, channels, consumers, compatibility, and historical policy")


def contract_proof() -> None:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from event_engineering.asyncapi_profile import validate_course_profile
    from event_engineering.contracts import load_schema, validate_payload
    from event_engineering.envelope import EventEnvelope
    import jsonschema

    contract_path = CAPSTONE / "contracts/asyncapi.yaml"
    document = load_yaml(contract_path)
    report = validate_course_profile(document)
    require((report.operation_count, report.channel_count, report.message_count) == (3, 3, 7), "unexpected AsyncAPI profile counts")
    base_schema = load_schema(CAPSTONE / "contracts/components/schemas/event-envelope.v1.schema.json")
    jsonschema.Draft202012Validator.check_schema(base_schema)
    envelope_validator = jsonschema.Draft202012Validator(
        base_schema, format_checker=jsonschema.FormatChecker()
    )
    seen_types: set[str] = set()
    examples = 0
    for channel in document["channels"].values():
        for ref_row in channel["messages"].values():
            ref = ref_row["$ref"]
            message_path = (contract_path.parent / ref).resolve()
            require(message_path.is_file() and message_path.is_relative_to(CAPSTONE), f"invalid message reference: {ref}")
            message = load_yaml(message_path)
            event_type = message.get("x-event-type")
            require(isinstance(event_type, str) and event_type not in seen_types, f"missing or duplicate x-event-type: {event_type}")
            seen_types.add(event_type)
            data_schema_path = (message_path.parent / message["x-data-schema"]).resolve()
            example_path = (message_path.parent / message["x-example"]).resolve()
            require(data_schema_path.is_file(), f"data schema missing for {event_type}")
            require(example_path.is_file(), f"example missing for {event_type}")
            schema = load_schema(data_schema_path)
            event = EventEnvelope(**load_json(example_path))
            envelope_validator.validate(event.to_dict())
            require(event.type == event_type, f"example type mismatch for {event_type}")
            require(event.dataschema == schema["$id"], f"example dataschema mismatch for {event_type}")
            validate_payload(event, schema)
            examples += 1
    catalog = load_yaml(CAPSTONE / "contracts/event-catalog.yaml")
    catalog_types = {row["eventType"] for row in catalog["entries"]}
    require(catalog_types == seen_types, "event catalogue and AsyncAPI message set differ")
    pass_line(f"AsyncAPI 3.1 course profile — {report.operation_count} operations, {report.channel_count} channels, {examples} valid examples")


def vector_proof() -> None:
    files = sorted((CAPSTONE / "shared/vectors").glob("*.json"))
    require(len(files) == 10, f"expected ten vector files, found {len(files)}")
    ids: set[str] = set(); count = 0
    for path in files:
        value = load_json(path)
        cases = value.get("cases", [])
        require(len(cases) >= 6, f"vector file {path.name} is too thin")
        for case in cases:
            identity = case.get("id")
            require(identity and identity not in ids, f"missing or duplicate vector id {identity}")
            require(case.get("description") and case.get("expected"), f"incomplete vector case {identity}")
            ids.add(identity); count += 1
    pass_line(f"shared adversarial vectors — {len(files)} files, {count} cases")


def migration_proof() -> None:
    canonical = CAPSTONE / "database/migrations"
    tracks = [PY_TRACK / "migrations", TS_TRACK / "migrations"]
    names = [f"{number:03d}_" for number in range(1, 13)]
    canonical_files = sorted(canonical.glob("*.sql"))
    require(len(canonical_files) == 12, f"expected migrations 001–012, found {len(canonical_files)}")
    for prefix in names:
        require(sum(path.name.startswith(prefix) for path in canonical_files) == 1, f"migration {prefix[:3]} missing or duplicated")
    for track in tracks:
        track_files = sorted(track.glob("*.sql"))
        require([p.name for p in track_files] == [p.name for p in canonical_files], f"migration file set differs in {track.relative_to(ROOT)}")
        for source, target in zip(canonical_files, track_files):
            require(source.read_bytes() == target.read_bytes(), f"migration differs: {target.relative_to(ROOT)}")
    inherited = CAPSTONE / "predecessor/handoff/migrations/009_performance_indexes.sql"
    require(inherited.read_bytes() == (canonical / "009_performance_indexes.sql").read_bytes(), "migration 009 differs from predecessor handoff")
    text = "\n".join(path.read_text(encoding="utf-8") for path in canonical_files[-3:])
    for table in ["event_outbox", "event_inbox", "event_replay_runs", "event_dead_letters", "event_contract_releases", "event_consumer_contracts"]:
        require(table in text, f"event migration omits {table}")
    pass_line("migration parity — revisions 001–012 across canonical, Python, and TypeScript trees")


def python_proof() -> None:
    env = {"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"}
    result = run([sys.executable, "-m", "unittest", "discover", "-s", "tests_event", "-q"], cwd=PY_TRACK, env=env)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests_postgres", "-q"], cwd=PY_TRACK, env=env)
    for path in list((PY_TRACK / "src").rglob("*.py")) + list((PY_TRACK / "tests_event").rglob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    match = re.search(r"Ran (\d+) tests", result.stderr + result.stdout)
    pass_line(f"Python event implementation — {match.group(1) if match else 'all'} dependency-light tests")


def typescript_proof() -> None:
    require(shutil.which("tsc") is not None and shutil.which("node") is not None, "node and tsc are required")
    shutil.rmtree(TS_TRACK / "dist", ignore_errors=True)
    run(["tsc", "-p", "tsconfig.json"], cwd=TS_TRACK)
    result = run(["node", "--test", "test-event-core/*.test.mjs"], cwd=TS_TRACK)
    match = re.search(r"# pass (\d+)", result.stdout)
    require(match and int(match.group(1)) >= 20, "TypeScript test count is unexpectedly low")
    shutil.rmtree(TS_TRACK / "dist", ignore_errors=True)
    pass_line(f"TypeScript event implementation — {match.group(1)} dependency-light tests")


def _import_event_modules() -> dict[str, Any]:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from event_engineering.broker import DeterministicBroker
    from event_engineering.demo import run_demo
    from event_engineering.evolution import compare_object_schemas
    from event_engineering.replay import ReplayPlan, execute_replay
    from event_engineering.release import evaluate_event_release
    from event_engineering.stream import EventTimeWindows
    return locals()


def delivery_proof() -> None:
    modules = _import_event_modules()
    report = modules["run_demo"]()
    require(report["brokerRecords"] == 2 and report["effects"] == 1, "delivery demo did not demonstrate duplicate publication plus one effect")
    pass_line("delivery and acknowledgement — duplicate publication, one committed effect")


def outbox_inbox_proof() -> None:
    run([sys.executable, "-m", "unittest", "tests_event.test_outbox_inbox", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"})
    text = (CAPSTONE / "database/migrations/010_event_outbox_inbox.sql").read_text(encoding="utf-8")
    require("PRIMARY KEY (tenant_id, consumer_name, effect_version, event_id)" in text, "inbox identity is incomplete")
    pass_line("transactional publication and idempotent effects")


def evolution_proof() -> None:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from event_engineering.evolution import compare_object_schemas
    base = load_json(CAPSTONE / "releases/baseline/analysis-run-completed.v1.schema.json")
    additive = load_json(CAPSTONE / "releases/accepted-additive/analysis-run-completed.v1.schema.json")
    breaking = load_json(CAPSTONE / "releases/rejected-required-field/analysis-run-completed.v1.schema.json")
    require(compare_object_schemas(base, additive).status == "accepted", "additive candidate not accepted")
    require(compare_object_schemas(base, breaking).status == "rejected", "breaking candidate not rejected")
    pass_line("event schema evolution — additive and breaking fixtures classified")


def replay_proof() -> None:
    policy = load_yaml(CAPSTONE / "replay/replay-policy.yaml")
    plan = load_yaml(CAPSTONE / "replay/example-plan.yaml")
    require(policy["requirements"]["externalSideEffects"] == "disabled", "replay policy permits external side effects")
    require(plan["sideEffects"] == "disabled" and plan["maximumEvents"] > 0, "example replay plan is unbounded or unsafe")
    run([sys.executable, "-m", "unittest", "tests_event.test_evolution_replay", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"})
    pass_line("bounded replay — dry-run, tenant scope, event bound, and side-effect prohibition")


def workflow_proof() -> None:
    run([sys.executable, "-m", "unittest", "tests_event.test_workflows", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"})
    pass_line("consumer workflow state — stable command identity and monotonic terminal state")


def stream_proof() -> None:
    policy = load_yaml(CAPSTONE / "stream-processing/window-policy.yaml")
    require(policy["eventTimeField"] == "data.occurredAt", "stream policy does not use event time")
    require(policy["lateBeyondPolicy"] == "quarantine", "late-data policy is not explicit")
    run([sys.executable, "-m", "unittest", "tests_event.test_stream_security.StreamSecurityTests.test_event_time_window_and_duplicate", "tests_event.test_stream_security.StreamSecurityTests.test_late_event_recorded", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"})
    pass_line("event-time processing — deduplication, watermark, lateness, and correction policy")


def security_proof() -> None:
    grants = load_yaml(CAPSTONE / "security/producer-grants.yaml")
    require(len(grants.get("grants", [])) == 3, "producer grants are incomplete")
    run([sys.executable, "-m", "unittest", "tests_event.test_stream_security.StreamSecurityTests.test_authorization", "tests_event.test_stream_security.StreamSecurityTests.test_sensitive_payload_rejected", "tests_event.test_stream_security.StreamSecurityTests.test_cross_language_signature_profile", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"})
    pass_line("event security — source/channel/type/tenant authorization and exact-byte signatures")


def reliability_proof() -> None:
    for name in ["dead-letter-runbook.md", "lag-runbook.md", "replay-runbook.md"]:
        path = CAPSTONE / "operations" / name
        require(path.is_file() and words(path) >= 120, f"runbook is incomplete: {name}")
    run([sys.executable, "-m", "unittest", "tests_event.test_reliability_catalog_release", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1"})
    pass_line("event reliability — bounded retry, dead-letter custody, lag, catalogue, and release tests")


def release_proof() -> None:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from event_engineering.release import evaluate_event_release
    baseline_default = load_json(CAPSTONE / "releases/baseline/analysis-run-completed.v1.schema.json")
    decisions: dict[str, str] = {}
    for directory in sorted(path for path in (CAPSTONE / "releases").iterdir() if path.is_dir()):
        metadata = load_json(directory / "release.json")
        old = load_json(directory / metadata["comparisonBaseline"]) if metadata.get("comparisonBaseline") else baseline_default
        new = load_json(directory / "analysis-run-completed.v1.schema.json")
        gates = metadata["gates"]
        decision = evaluate_event_release(old, new, replay_safe=gates["replaySafe"], catalog_complete=gates["catalogComplete"], contract_valid=gates["contractValid"], security_valid=gates["securityValid"], reliability_ready=gates["reliabilityReady"])
        require(decision.status == metadata["expectedDecision"], f"release decision mismatch for {directory.name}: {decision.status}")
        decisions[directory.name] = decision.status
    require(set(decisions.values()) == {"accepted", "review-required", "rejected"}, "release fixtures do not cover all decision states")
    pass_line(f"event release gates — {len(decisions)} candidates across accepted, review-required, and rejected states")


def planted_defect_proof() -> None:
    directories = sorted(path for path in (CAPSTONE / "planted-defects").iterdir() if path.is_dir())
    require(len(directories) == 10, f"expected ten planted defects, found {len(directories)}")
    ids: set[str] = set(); families: set[str] = set()
    for path in directories:
        defect = load_json(path / "defect.json")
        identity = defect.get("id")
        require(re.fullmatch(r"EVT-(?:0[1-9]|10)", identity or ""), f"invalid defect id {identity}")
        require(identity not in ids and defect.get("mustBeRejected") is True, f"duplicate or non-rejecting defect {identity}")
        require(defect.get("expectedOracle") and defect.get("proofFamily"), f"defect {identity} lacks oracle")
        ids.add(identity); families.add(defect["proofFamily"])
    require(len(families) >= 8, "planted defects do not span enough mechanisms")
    pass_line("planted defects — ten failures with named rejecting oracles")


def handoff_proof() -> None:
    base = CAPSTONE / "handoff"
    manifest_path = base / "MANIFEST.json"
    checksum_path = base / "MANIFEST.sha256"
    require(manifest_path.is_file() and checksum_path.is_file(), "outgoing handoff manifest missing")
    require(sha256(manifest_path) == checksum_path.read_text(encoding="utf-8").split()[0], "handoff manifest digest mismatch")
    manifest = load_json(manifest_path)
    require(manifest.get("handoff") == "course-6-to-course-7", "wrong outgoing handoff identity")
    listed = set()
    for row in manifest.get("files", []):
        path = base / row["path"]
        require(
            path.is_file()
            and sha256(path) == row["sha256"]
            and path.stat().st_size == row["size"]
            and file_mode(path) == row["mode"],
            f"outgoing handoff mismatch: {row['path']}",
        )
        listed.add(row["path"])
    actual = {path.relative_to(base).as_posix() for path in base.rglob("*") if path.is_file() and path.name not in {"MANIFEST.json", "MANIFEST.sha256"}}
    require(actual == listed, "outgoing handoff file set differs from manifest")
    pass_line(f"Course 6 outgoing handoff — {len(listed)} files")


def markdown_link_proof() -> None:
    checked = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if any(part in {"node_modules", "dist", ".venv"} for part in path.parts):
            continue
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            target = target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            resolved = (path.parent / relative).resolve()
            require(resolved.exists() and resolved.is_relative_to(ROOT.resolve()), f"broken local Markdown link in {path.relative_to(ROOT)}: {target}")
            checked += 1
    pass_line(f"local Markdown links — {checked} targets")


def source_reference_proof() -> None:
    references: set[str] = set()
    pattern = re.compile(r"capstone/[A-Za-z0-9_./*?-]+")
    for path in COURSE_BOOK.rglob("*.md"):
        for match in pattern.findall(path.read_text(encoding="utf-8")):
            references.add(match.rstrip(".,;:)`"))
    for ref in sorted(references):
        pattern_path = ref[len("capstone/"):]
        if "*" in pattern_path or "?" in pattern_path:
            require(list(CAPSTONE.glob(pattern_path)), f"documented wildcard path has no match: {ref}")
        else:
            require((ROOT / ref).exists(), f"documented source path does not exist: {ref}")
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8") if (ROOT / "Makefile").exists() else ""
    declared_targets: set[str] = set()
    for line in makefile.splitlines():
        if not line or line[0].isspace() or line.startswith("#") or ":" not in line:
            continue
        head = line.split(":", 1)[0]
        declared_targets.update(token for token in head.split() if re.fullmatch(r"[a-z0-9-]+", token))
    targets = set()
    for path in COURSE_BOOK.rglob("*.md"):
        targets.update(re.findall(r"`make\s+([a-z0-9-]+)", path.read_text(encoding="utf-8")))
    for target in targets:
        require(target in declared_targets, f"documented Make target does not exist: {target}")
    pass_line(f"course-book source references — {len(references)} paths, {len(targets)} Make targets")


def education_proof() -> None:
    main_counts = []
    for number in range(1, 11):
        module = next(COURSE_BOOK.glob(f"module-{number:02d}-*"))
        count = words(module / "index.md")
        require(count >= 1800, f"module {number:02d} main chapter is too thin: {count} words")
        require(words(module / "exercise-answers.md") >= 540, f"module {number:02d} answers are too thin")
        require(words(module / "lab.md") >= 250, f"module {number:02d} lab is too thin")
        require(words(module / "checkpoint.md") >= 120, f"module {number:02d} checkpoint is too thin")
        main_counts.append(count)
    forbidden = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|coming soon|answer direction)\b", re.I)
    paragraphs: dict[str, set[str]] = {}
    for path in COURSE_BOOK.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        require(not forbidden.search(text), f"unfinished or generated filler in {path.relative_to(ROOT)}")
        for paragraph in re.split(r"\n\s*\n", text):
            normalized = re.sub(r"\s+", " ", paragraph.strip())
            if len(normalized.split()) >= 80:
                paragraphs.setdefault(normalized, set()).add(path.as_posix())
    offenders = [(text, paths) for text, paths in paragraphs.items() if len(paths) >= 5]
    require(not offenders, f"long instructional paragraph repeated across {len(offenders)} blocks")
    python_fences: list[tuple[Path, str]] = []
    typescript_fences: list[tuple[Path, str]] = []
    fence_pattern = re.compile(r"```([^\n]*)\n(.*?)```", re.S)
    for path in COURSE_BOOK.rglob("*.md"):
        for language, body in fence_pattern.findall(path.read_text(encoding="utf-8")):
            if language.strip() == "python":
                python_fences.append((path, textwrap.dedent(body)))
            elif language.strip() in {"typescript", "ts"}:
                typescript_fences.append((path, textwrap.dedent(body)))
    for path, body in python_fences:
        try:
            compile(body, f"{path}:python-fence", "exec")
        except SyntaxError as exc:
            raise ProofError(f"invalid Python curriculum fence in {path.relative_to(ROOT)}: {exc}") from exc
    if typescript_fences:
        require(shutil.which("tsc") is not None, "tsc is required to check TypeScript curriculum fences")
        with tempfile.TemporaryDirectory(prefix="course6-fences-") as directory:
            temp = Path(directory)
            for index, (_, body) in enumerate(typescript_fences, 1):
                (temp / f"fence-{index}.ts").write_text("declare function buildEvent(value: any): any;\n" + body, encoding="utf-8")
            run(["tsc", "--noEmit", "--target", "ES2022", "--module", "NodeNext", "--moduleResolution", "NodeNext", *[str(path) for path in sorted(temp.glob("*.ts"))]], cwd=ROOT)
    pass_line(f"educational depth — module chapters {min(main_counts)}–{max(main_counts)} words; {len(python_fences)} Python and {len(typescript_fences)} TypeScript fences parse")


def hygiene_proof() -> None:
    forbidden_names = {".DS_Store", "Thumbs.db", ".pytest_cache", "__pycache__", "node_modules", "dist", ".venv", "venv", "work"}
    bad = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if any(part in forbidden_names for part in path.relative_to(ROOT).parts)]
    require(not bad, f"repository hygiene violation: {bad[:10]}")
    symlinks = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_symlink()]
    require(not symlinks, f"symlinks are not allowed in the release: {symlinks}")
    pass_line("repository hygiene")


def manifest_proof() -> None:
    manifest_path = ROOT / "MANIFEST.json"
    checksum_path = ROOT / "MANIFEST.sha256"
    require(manifest_path.is_file() and checksum_path.is_file(), "course manifest pair missing")
    require(sha256(manifest_path) == checksum_path.read_text(encoding="utf-8").split()[0], "MANIFEST.json checksum mismatch")
    manifest = load_json(manifest_path)
    listed = set()
    for row in manifest.get("files", []):
        path = ROOT / row["path"]
        require(path.is_file(), f"manifest file missing: {row['path']}")
        require(
            path.stat().st_size == row["size"]
            and sha256(path) == row["sha256"]
            and file_mode(path) == row["mode"],
            f"manifest mismatch: {row['path']}",
        )
        listed.add(row["path"])
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in {"MANIFEST.json", "MANIFEST.sha256"}
        and not any(part in {"__pycache__", ".pytest_cache", "node_modules", "dist", ".venv", "work"} for part in path.relative_to(ROOT).parts)
    }
    require(actual == listed, f"course manifest file-set mismatch: extra={sorted(actual-listed)[:10]}, missing={sorted(listed-actual)[:10]}")
    pass_line(f"course manifest — {len(listed)} files")


def capstone_tour() -> None:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from event_engineering.demo import run_demo
    report = run_demo()
    print(json.dumps(report, indent=2, sort_keys=True))
    require(report["brokerRecords"] == 2 and report["effects"] == 1, "Python capstone tour failed")
    shutil.rmtree(TS_TRACK / "dist", ignore_errors=True)
    run(["tsc", "-p", "tsconfig.json"], cwd=TS_TRACK)
    result = run(["node", "--input-type=module", "-e", "import('./dist/event-engineering/demo.js').then(m=>console.log(JSON.stringify(m.runDemo())))"], cwd=TS_TRACK)
    ts_report = json.loads(result.stdout.strip().splitlines()[-1])
    require(ts_report["brokerRecords"] == 2 and ts_report["effects"] == 1, "TypeScript capstone tour failed")
    shutil.rmtree(TS_TRACK / "dist", ignore_errors=True)
    pass_line("capstone tour — duplicate transport publication, one committed effect in both tracks")


def asyncapi_cli_proof() -> None:
    require(shutil.which("asyncapi") is not None, "AsyncAPI CLI is not installed")
    run(["asyncapi", "validate", "capstone/contracts/asyncapi.yaml"], cwd=ROOT)
    pass_line("external AsyncAPI CLI validation")


def postgres_proof() -> None:
    url = os.environ.get("TEST_DATABASE_URL")
    require(url, "TEST_DATABASE_URL is required")
    require(shutil.which("psql") is not None, "psql is not installed")
    for path in sorted((CAPSTONE / "database/migrations").glob("*.sql")):
        run(["psql", url, "-v", "ON_ERROR_STOP=1", "-f", str(path)], cwd=ROOT)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests_postgres", "-q"], cwd=PY_TRACK, env={"PYTHONPATH": os.pathsep.join([str(PY_TRACK / "src"), str(PY_TRACK / "tests_event")]), "PYTHONDONTWRITEBYTECODE": "1", "TEST_DATABASE_URL": url})
    pass_line("live PostgreSQL event migrations and constraints")


def docs_build() -> None:
    require(shutil.which("mkdocs") is not None, "mkdocs is not installed")
    run(["mkdocs", "build", "--strict"], cwd=ROOT)
    shutil.rmtree(ROOT / "site", ignore_errors=True)
    pass_line("strict MkDocs build")


def nats_proof() -> None:
    try:
        __import__("nats")
    except ImportError as exc:
        raise ProofError(f"nats-py is not installed: {exc}") from exc
    run([sys.executable, "scripts/nats_live_proof.py"], cwd=ROOT, env={"PYTHONDONTWRITEBYTECODE": "1"})
    pass_line("live NATS JetStream publish, broker-window deduplication, pull delivery, and acknowledgement")


def core_proof(include_manifest: bool = True) -> None:
    proofs: list[Callable[[], None]] = [
        predecessor_proof, structure_proof, data_proof, event_case_proof,
        contract_proof, vector_proof, migration_proof, python_proof,
        typescript_proof, delivery_proof, outbox_inbox_proof, evolution_proof,
        replay_proof, workflow_proof, stream_proof, security_proof,
        reliability_proof, release_proof, planted_defect_proof, handoff_proof,
        markdown_link_proof, source_reference_proof, education_proof, hygiene_proof,
    ]
    if include_manifest:
        proofs.append(manifest_proof)
    for proof in proofs:
        proof()
    pass_line("Event-Driven API Engineering core proof")


def module_proof(module: int, track: str) -> None:
    require(1 <= module <= 10, "MODULE must be 01–10")
    require(track in {"python", "typescript", "python-fastapi", "typescript-fastify"}, "TRACK must identify Python or TypeScript")
    mapping: dict[int, list[Callable[[], None]]] = {
        1: [event_case_proof, vector_proof],
        2: [contract_proof],
        3: [delivery_proof],
        4: [outbox_inbox_proof],
        5: [evolution_proof, replay_proof],
        6: [workflow_proof],
        7: [stream_proof],
        8: [security_proof],
        9: [reliability_proof],
        10: [release_proof, handoff_proof],
    }
    for proof in mapping[module]: proof()
    (python_proof if track.startswith("python") else typescript_proof)()
    pass_line(f"module {module:02d} proof for {track}")


COMMANDS: dict[str, Callable[[], None]] = {
    "doctor": doctor,
    "predecessor-proof": predecessor_proof,
    "orientation-proof": orientation_proof,
    "structure-proof": structure_proof,
    "data-proof": data_proof,
    "event-case-proof": event_case_proof,
    "contract-proof": contract_proof,
    "vector-proof": vector_proof,
    "migration-proof": migration_proof,
    "python-proof": python_proof,
    "typescript-proof": typescript_proof,
    "delivery-proof": delivery_proof,
    "outbox-inbox-proof": outbox_inbox_proof,
    "evolution-proof": evolution_proof,
    "replay-proof": replay_proof,
    "workflow-proof": workflow_proof,
    "stream-proof": stream_proof,
    "security-proof": security_proof,
    "reliability-proof": reliability_proof,
    "release-proof": release_proof,
    "planted-defect-proof": planted_defect_proof,
    "handoff-proof": handoff_proof,
    "markdown-link-proof": markdown_link_proof,
    "source-reference-proof": source_reference_proof,
    "education-proof": education_proof,
    "hygiene-proof": hygiene_proof,
    "manifest-proof": manifest_proof,
    "capstone-tour": capstone_tour,
    "asyncapi-cli-proof": asyncapi_cli_proof,
    "postgres-proof": postgres_proof,
    "docs-build": docs_build,
    "nats-proof": nats_proof,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Course 6 proof and learner tooling")
    parser.add_argument("command", choices=sorted([*COMMANDS, "core-proof", "core-proof-no-manifest", "full-proof", "module-proof"]))
    parser.add_argument("--module", type=int)
    parser.add_argument("--track", default="python")
    args = parser.parse_args()
    try:
        if args.command == "core-proof": core_proof(True)
        elif args.command == "core-proof-no-manifest": core_proof(False)
        elif args.command == "full-proof":
            core_proof(True); asyncapi_cli_proof(); postgres_proof(); docs_build()
        elif args.command == "module-proof":
            require(args.module is not None, "--module is required")
            module_proof(args.module, args.track)
        else:
            COMMANDS[args.command]()
    except ProofError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
