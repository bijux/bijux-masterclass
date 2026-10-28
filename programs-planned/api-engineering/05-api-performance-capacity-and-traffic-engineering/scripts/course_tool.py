#!/usr/bin/env python3
"""Deterministic proof, evidence, and manifest support for Course 5."""

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
COURSE_ID = "api-performance-capacity-and-traffic-engineering"
ARCHIVE_ROOT = f"programs/api-engineering/05-{COURSE_ID}"
IGNORED_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".coverage",
    "node_modules", "site", ".runtime", ".venv", "venv", "dist", "dist-core",
}
EPHEMERAL = {"last-core-proof.json", "last-doctor.json", "capstone-tour.json", "live-run-list-plan.json"}


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader: UniqueLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


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


def load_json(path: Path) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)
    except Exception as exc:
        fail(f"cannot parse JSON {path.relative_to(ROOT)}: {exc}")


def load_yaml(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    except Exception as exc:
        fail(f"cannot parse YAML {path.relative_to(ROOT)}: {exc}")


def run(command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> None:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    shown = " ".join(command)
    print(f"RUN  ({cwd}) {shown}")
    result = subprocess.run(command, cwd=cwd, env=merged, text=True)
    if result.returncode:
        fail(f"command failed ({result.returncode}): {shown}")


def clean_generated() -> None:
    for path in sorted(ROOT.rglob("*"), reverse=True):
        if path.is_dir() and path.name in IGNORED_DIRS:
            shutil.rmtree(path, ignore_errors=True)
    for path in REPORTS.glob("*.json"):
        if path.name in EPHEMERAL:
            path.unlink(missing_ok=True)


def doctor() -> None:
    tools = {}
    for executable in ["python3", "node", "tsc", "mkdocs", "docker", "psql", "k6", "locust"]:
        tools[executable] = shutil.which(executable)
        print(f"{executable:10} {tools[executable] or 'not-available'}")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "last-doctor.json").write_text(json.dumps({"tools": tools}, indent=2) + "\n")
    passed("doctor completed; missing optional tools are reported, not passed")


def verify_manifest(base: Path, manifest_name: str = "MANIFEST.json") -> int:
    manifest = load_json(base / manifest_name)
    rows = manifest.get("files")
    if not isinstance(rows, list):
        fail(f"{manifest_name} has no files list")
    expected = set()
    for row in rows:
        if not isinstance(row, dict):
            fail("manifest row is not an object")
        relative = Path(str(row["path"]))
        expected.add(relative.as_posix())
        path = base / relative
        if not path.is_file():
            fail(f"manifest file missing: {relative}")
        if path.stat().st_size != int(row["size"]):
            fail(f"manifest size mismatch: {relative}")
        if sha256(path) != row["sha256"]:
            fail(f"manifest digest mismatch: {relative}")
        mode = oct(stat.S_IMODE(path.stat().st_mode))[2:].zfill(4)
        if mode != str(row["mode"]):
            fail(f"manifest mode mismatch: {relative}")
    actual = {p.relative_to(base).as_posix() for p in iter_manifest_files(base)}
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        fail(f"manifest set mismatch missing={missing[:5]} extra={extra[:5]}")
    return len(rows)


def predecessor_proof() -> None:
    handoff = CAPSTONE / "predecessor" / "handoff"
    count = verify_manifest(handoff)
    profile = load_yaml(handoff / "reliability/reliability-profile.yaml")
    if not isinstance(profile, dict):
        fail("predecessor reliability profile is invalid")
    if not (handoff / "contract/openapi-api-1.2.bundle.yaml").is_file():
        fail("API 1.2 predecessor contract missing")
    passed(f"Course 4 predecessor handoff — {count} files")


def structure_proof() -> None:
    required_root = [
        "README.md", "course.json", "tool-versions.json", "Makefile", "mkdocs.yml",
    ]
    for relative in required_root:
        if not (ROOT / relative).is_file():
            fail(f"missing root file {relative}")
    course_book = ROOT / "course-book"
    pages = sorted(course_book.rglob("*.md"))
    if len(pages) != 59:
        fail(f"expected 59 course-book pages, found {len(pages)}")
    modules = sorted(course_book.glob("module-*"))
    if len(modules) != 11:
        fail(f"expected orientation plus 10 modules, found {len(modules)}")
    numbered = [p for p in modules if not p.name.startswith("module-00")]
    for module in numbered:
        for name in ["index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"]:
            if not (module / name).is_file():
                fail(f"missing {name} in {module.name}")
        exercises = re.findall(r"^## (\d+)\.", (module / "exercises.md").read_text(), re.M)
        answers = re.findall(r"^## (\d+)\.", (module / "exercise-answers.md").read_text(), re.M)
        if exercises != [str(i) for i in range(1, 13)] or answers != exercises:
            fail(f"exercise/answer numbering mismatch in {module.name}")
        lab = (module / "lab.md").read_text()
        for heading in ["Objective", "Setup conditions", "Failure action and investigation", "Operational oracle", "Required evidence", "Cleanup and reset", "Completion gate"]:
            if f"## {heading}" not in lab:
                fail(f"lab missing {heading}: {module.name}")
    mkdocs = load_yaml(ROOT / "mkdocs.yml")
    nav_paths: set[str] = set()
    def walk(value: Any) -> None:
        if isinstance(value, str) and value.endswith(".md"):
            nav_paths.add(value)
        elif isinstance(value, list):
            for item in value: walk(item)
        elif isinstance(value, dict):
            for item in value.values(): walk(item)
    walk(mkdocs.get("nav"))
    actual = {p.relative_to(course_book).as_posix() for p in pages}
    if nav_paths != actual:
        fail(f"MkDocs coverage mismatch missing={sorted(actual-nav_paths)[:5]} extra={sorted(nav_paths-actual)[:5]}")
    passed("course structure — 59 navigated pages, 10 complete modules")


def data_proof() -> None:
    counts = Counter()
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.suffix == ".json":
            load_json(path); counts["json"] += 1
        elif path.suffix in {".yaml", ".yml"}:
            load_yaml(path); counts["yaml"] += 1
        elif path.suffix == ".toml":
            try:
                tomllib.loads(path.read_text())
            except Exception as exc:
                fail(f"cannot parse TOML {path.relative_to(ROOT)}: {exc}")
            counts["toml"] += 1
    passed(f"data parsing — JSON {counts['json']}, YAML {counts['yaml']}, TOML {counts['toml']}")


def performance_case_proof() -> None:
    case = CAPSTONE / "performance-case"
    profile = load_yaml(case / "performance-profile.yaml")
    workloads = load_yaml(case / "workload-catalog.yaml")
    required = ["profile", "workloads"]
    if not isinstance(profile, dict) or not isinstance(workloads, dict):
        fail("performance case files must be mappings")
    rows = workloads.get("workloads")
    if not isinstance(rows, list) or len(rows) != 6:
        fail("expected six critical workloads")
    ids = [str(row.get("id")) for row in rows if isinstance(row, dict)]
    if len(set(ids)) != 6 or any(not item.startswith("WL-") for item in ids):
        fail("workload ids must be unique and stable")
    for name in ["environment-schema.json", "concurrency-budget.yaml", "cache-catalog.yaml", "traffic-policy.yaml", "capacity-scenarios.yaml"]:
        if not (case / name).is_file(): fail(f"missing performance case file {name}")
    passed("performance case — six workloads and profile 1.0 evidence model")


def vector_proof() -> None:
    vector_dir = CAPSTONE / "shared" / "vectors"
    files = sorted(vector_dir.glob("*.json"))
    if len(files) < 10:
        fail(f"expected at least 10 vector files, found {len(files)}")
    cases = 0
    ids: set[str] = set()
    def walk(value: Any) -> Iterator[dict[str, Any]]:
        if isinstance(value, dict):
            if isinstance(value.get("id"), str): yield value
            for child in value.values(): yield from walk(child)
        elif isinstance(value, list):
            for child in value: yield from walk(child)
    for path in files:
        for row in walk(load_json(path)):
            case_id = str(row["id"])
            if case_id in ids: fail(f"duplicate vector id {case_id}")
            ids.add(case_id); cases += 1
    if cases < 35:
        fail(f"expected at least 35 identified vector cases, found {cases}")
    passed(f"shared vectors — {len(files)} files, {cases} identified cases")


def migration_proof() -> None:
    tracks = [PY_TRACK / "migrations", TS_TRACK / "migrations", CAPSTONE / "database" / "migrations"]
    expected = [f"{number:03d}" for number in range(1, 10)]
    digests: list[dict[str, str]] = []
    for directory in tracks:
        files = sorted(directory.glob("*.sql"))
        prefixes = [path.name[:3] for path in files]
        if prefixes != expected:
            fail(f"migration sequence mismatch in {directory.relative_to(ROOT)}: {prefixes}")
        digests.append({path.name: sha256(path) for path in files})
    if digests[0] != digests[1]:
        fail("Python and TypeScript migrations differ")
    if sha256(tracks[0] / "009_performance_indexes.sql") != sha256(tracks[2] / "009_performance_indexes.sql"):
        fail("canonical migration 009 differs from track copy")
    sql = (tracks[0] / "009_performance_indexes.sql").read_text().lower()
    for token in ["idx_analysis_runs_owner_status_created_id", "idx_run_jobs_available_claim", "idx_webhook_deliveries_available_claim"]:
        if token not in sql: fail(f"migration 009 missing {token}")
    passed("database migrations — 001–009 with cross-track parity")


def python_proof() -> None:
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests_performance", "-q"], cwd=PY_TRACK, env=env)
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in IGNORED_DIRS for part in path.parts): continue
        try: ast.parse(path.read_text())
        except SyntaxError as exc: fail(f"Python syntax error {path.relative_to(ROOT)}: {exc}")
    passed("Python performance track and course tooling")


def typescript_proof() -> None:
    tsc = shutil.which("tsc")
    node = shutil.which("node")
    if not tsc or not node: fail("dependency-light TypeScript proof requires tsc and node")
    run([tsc, "-p", "tsconfig.json"], cwd=TS_TRACK)
    run([node, "--test", *[str(p.relative_to(TS_TRACK)) for p in sorted((TS_TRACK / "test-performance-core").glob("*.test.mjs"))]], cwd=TS_TRACK)
    passed("TypeScript performance track — compile and core tests")


def plan_proof() -> None:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from api_performance.query_plans import compare_plans, summarize_plan
    vectors = load_json(CAPSTONE / "shared/vectors/query-plans.json")
    for case in vectors["cases"]:
        before = summarize_plan(load_json(CAPSTONE / case["before"]))
        after = summarize_plan(load_json(CAPSTONE / case["after"]))
        comparison = compare_plans(before, after)
        expected = case["expected"]
        if sorted(comparison.removed_sequential_scans) != sorted(expected["removedSequentialScans"]): fail(f"{case['id']} removed scan mismatch")
        if sorted(comparison.added_indexes) != sorted(expected["addedIndexes"]): fail(f"{case['id']} index mismatch")
        if comparison.read_block_delta > expected["readBlockDeltaMaximum"]: fail(f"{case['id']} read-block improvement too small")
        if comparison.actual_row_delta != expected["actualRowDelta"]: fail(f"{case['id']} changed result rows")
    passed("PostgreSQL plan fixtures and before/after decision oracles")


def release_proof() -> None:
    sys.path.insert(0, str(PY_TRACK / "src"))
    from api_performance.release import evaluate_release
    releases = CAPSTONE / "releases"
    baseline = load_json(releases / "baseline/envelope.json")
    policy = load_json(releases / "performance-policy.json")
    expected = {
        "accepted-candidate": "accepted",
        "rejected-faster-but-wrong": "rejected",
        "inconclusive-environment-mismatch": "inconclusive",
        "rejected-regression": "rejected",
    }
    for name, status in expected.items():
        decision = evaluate_release(baseline, load_json(releases / name / "envelope.json"), policy)
        if decision.status != status: fail(f"release {name}: expected {status}, got {decision.status}")
    passed("performance release states — accepted, rejected, and inconclusive")


def planted_defect_proof() -> None:
    rows = []
    for path in sorted((CAPSTONE / "planted-defects").glob("PERF-*/defect.json")):
        row = load_json(path)
        if row.get("mustBeRejected") is not True or not row.get("expectedOracle"):
            fail(f"invalid planted defect {path.relative_to(ROOT)}")
        rows.append(row)
    if [row["id"] for row in rows] != [f"PERF-{i:02d}" for i in range(1, 11)]:
        fail("planted defects must be PERF-01 through PERF-10")
    # Mechanically exercise representative proof sensitivity.
    release_proof()
    cache_cases = load_json(CAPSTONE / "shared/vectors/cache.json")["cases"]
    if any(case.get("sameKeyExpected") is not False for case in cache_cases):
        fail("cache vectors do not reject identity collapse")
    mismatch = load_json(CAPSTONE / "releases/inconclusive-environment-mismatch/envelope.json")
    base = load_json(CAPSTONE / "releases/baseline/envelope.json")
    if mismatch["environmentHash"] == base["environmentHash"]:
        fail("environment mismatch defect not planted")
    passed("ten planted performance defects have named rejection oracles")


def capstone_tour() -> None:
    run([sys.executable, "run_tour.py"], cwd=CAPSTONE / "benchmarks" / "harness")
    report = load_json(CAPSTONE / "reports/capstone-tour.json")
    if report.get("passed") is not True: fail("capstone tour did not pass")
    passed("local HTTP performance tour")


def markdown_links() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in IGNORED_DIRS for part in path.parts): continue
        text = path.read_text()
        for target in pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")): continue
            if target.startswith("<") and target.endswith(">"): target = target[1:-1]
            destination = (path.parent / target).resolve()
            try: destination.relative_to(ROOT.resolve())
            except ValueError: fail(f"Markdown link escapes course: {path.relative_to(ROOT)} -> {target}")
            if not destination.exists(): fail(f"broken Markdown link: {path.relative_to(ROOT)} -> {target}")
            count += 1
    passed(f"local Markdown links — {count}")


def source_reference_proof() -> None:
    mapping = (CAPSTONE / "SOURCE-MAP.md").read_text()
    required = [
        "models.py", "statistics.py", "http_efficiency.py", "query_plans.py",
        "runtime.py", "admission.py", "cache.py", "traffic.py", "capacity.py", "release.py",
        "models.ts", "statistics.ts", "http-efficiency.ts", "query-plans.ts",
        "runtime.ts", "admission.ts", "cache.ts", "traffic.ts", "capacity.ts", "release.ts",
    ]
    for name in required:
        if name not in mapping: fail(f"source map missing {name}")
    passed("course-book mechanisms map to executable Python and TypeScript sources")


def education_proof() -> None:
    pages = sorted((ROOT / "course-book").rglob("*.md"))
    text = "\n".join(path.read_text() for path in pages)
    forbidden = ["TODO", "TBD", "lorem ipsum", "write this later", "as an AI", "placeholder"]
    for marker in forbidden:
        if marker.lower() in text.lower(): fail(f"unfinished marker in course book: {marker}")
    for path in pages:
        words = len(re.findall(r"\b\w+[\w'-]*\b", path.read_text()))
        if path.name == "checkpoint.md" and words < 90: fail(f"thin checkpoint {path.relative_to(ROOT)}: {words} words")
        if path.name == "lab.md" and words < 180: fail(f"thin lab {path.relative_to(ROOT)}: {words} words")
        if path.name == "index.md" and "module-" in path.parent.name and path.parent.name != "module-00-orientation" and words < 1700:
            fail(f"thin module chapter {path.relative_to(ROOT)}: {words} words")
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        normalized = re.sub(r"\s+", " ", paragraph.strip())
        if len(normalized.split()) >= 35 and not normalized.startswith("```"):
            paragraphs.append(normalized)
    repeated = [item for item, count in Counter(paragraphs).items() if count >= 4]
    if repeated: fail(f"repeated long course-book paragraph found: {repeated[0][:100]}")
    passed("learner-first education guard — depth, completeness, and repetition")


def hygiene_proof() -> None:
    forbidden_names = {".DS_Store", "Thumbs.db"}
    forbidden_suffixes = {".pyc", ".pyo", ".swp", "~"}
    for path in ROOT.rglob("*"):
        if path.name in forbidden_names: fail(f"forbidden file {path.relative_to(ROOT)}")
        if path.is_file() and (path.suffix in forbidden_suffixes or path.name.endswith("~")): fail(f"generated file {path.relative_to(ROOT)}")
        if path.is_dir() and path.name in IGNORED_DIRS: fail(f"generated directory {path.relative_to(ROOT)}")
    passed("repository hygiene")


def _manifest_excluded(relative: Path) -> bool:
    if relative.as_posix() in {"MANIFEST.json", "MANIFEST.sha256"}: return True
    if any(part in IGNORED_DIRS for part in relative.parts): return True
    if relative.parts and relative.parts[0] == "reports" and relative.name in EPHEMERAL: return True
    if relative.parts[:2] == ("capstone", "reports") and relative.name in EPHEMERAL: return True
    return False


def iter_manifest_files(base: Path = ROOT) -> Iterable[Path]:
    for path in sorted(base.rglob("*")):
        if not path.is_file(): continue
        relative = path.relative_to(base)
        if not _manifest_excluded(relative): yield path


def create_manifest() -> int:
    rows = []
    for path in iter_manifest_files():
        rows.append({
            "path": path.relative_to(ROOT).as_posix(),
            "size": path.stat().st_size,
            "sha256": sha256(path),
            "mode": oct(stat.S_IMODE(path.stat().st_mode))[2:].zfill(4),
        })
    manifest = {"schema": "bijux-course-manifest-1", "course": COURSE_ID, "archiveRoot": ARCHIVE_ROOT, "files": rows}
    rendered = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (ROOT / "MANIFEST.json").write_text(rendered)
    (ROOT / "MANIFEST.sha256").write_text(f"{hashlib.sha256(rendered.encode()).hexdigest()}  MANIFEST.json\n")
    return len(rows)


def manifest_proof() -> None:
    expected = (ROOT / "MANIFEST.sha256").read_text().split()[0]
    if sha256(ROOT / "MANIFEST.json") != expected: fail("MANIFEST.sha256 mismatch")
    count = verify_manifest(ROOT)
    passed(f"course manifest — {count} files")


def orientation_proof() -> None:
    predecessor_proof(); structure_proof(); performance_case_proof()
    passed("orientation readiness")


def module_proof(module: str, track: str) -> None:
    value = int(module)
    if not 1 <= value <= 10: fail("module must be 01–10")
    if track not in {"python", "typescript"}: fail("track must be python or typescript")
    mapping = {
        1: [performance_case_proof, vector_proof],
        2: [vector_proof, capstone_tour],
        3: [python_proof if track == "python" else typescript_proof, capstone_tour],
        4: [migration_proof, plan_proof],
        5: [python_proof if track == "python" else typescript_proof],
        6: [python_proof if track == "python" else typescript_proof],
        7: [python_proof if track == "python" else typescript_proof, vector_proof],
        8: [python_proof if track == "python" else typescript_proof, vector_proof],
        9: [python_proof if track == "python" else typescript_proof, performance_case_proof],
        10: [release_proof, planted_defect_proof],
    }
    for proof in mapping[value]: proof()
    passed(f"module {value:02d} checkpoint for {track}")


def core_proof() -> None:
    clean_generated()
    results = []
    proofs = [
        predecessor_proof, structure_proof, data_proof, performance_case_proof,
        vector_proof, migration_proof, python_proof, typescript_proof, plan_proof,
        release_proof, planted_defect_proof, capstone_tour, markdown_links,
        source_reference_proof, education_proof,
    ]
    for proof in proofs:
        proof(); results.append(proof.__name__)
    clean_generated()
    hygiene_proof(); results.append("hygiene_proof")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "last-core-proof.json").write_text(json.dumps({"course": COURSE_ID, "status": "passed", "proofs": results}, indent=2) + "\n")
    passed("Course 5 dependency-light core proof")


def external_status() -> dict[str, bool]:
    return {
        "postgresql": bool(os.environ.get("TEST_DATABASE_URL")) and bool(shutil.which("psql")),
        "k6": bool(shutil.which("k6")),
        "locust": bool(shutil.which("locust")),
        "mkdocs": bool(shutil.which("mkdocs")),
        "docker": bool(shutil.which("docker")),
    }


def full_proof() -> None:
    core_proof()
    status = external_status()
    print(json.dumps(status, indent=2, sort_keys=True))
    missing = [name for name, available in status.items() if not available]
    if missing: fail("full proof requires external environment: " + ", ".join(missing))
    run([sys.executable, "capstone/tests/postgres_plan_proof.py"])
    run(["mkdocs", "build", "--strict"])
    passed("full environment-backed proof")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--module", default="01")
    parser.add_argument("--track", default="python")
    args = parser.parse_args()
    commands = {
        "doctor": doctor,
        "orientation-proof": orientation_proof,
        "predecessor-proof": predecessor_proof,
        "structure-proof": structure_proof,
        "data-proof": data_proof,
        "performance-case-proof": performance_case_proof,
        "vector-proof": vector_proof,
        "migration-proof": migration_proof,
        "python-proof": python_proof,
        "typescript-proof": typescript_proof,
        "plan-proof": plan_proof,
        "release-proof": release_proof,
        "planted-defect-proof": planted_defect_proof,
        "capstone-tour": capstone_tour,
        "markdown-link-proof": markdown_links,
        "source-reference-proof": source_reference_proof,
        "education-proof": education_proof,
        "hygiene-proof": hygiene_proof,
        "manifest-create": lambda: passed(f"course manifest created — {create_manifest()} files"),
        "manifest-proof": manifest_proof,
        "core-proof": core_proof,
        "full-proof": full_proof,
    }
    if args.command == "module-proof": module_proof(args.module, args.track); return
    try: command = commands[args.command]
    except KeyError: fail(f"unknown command {args.command}")
    command()


if __name__ == "__main__":
    main()
