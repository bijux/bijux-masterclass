#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAPSTONE = ROOT / "capstone"
PY_TRACK = CAPSTONE / "tracks" / "python-fastapi"
TS_TRACK = CAPSTONE / "tracks" / "typescript-fastify"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL {message}")


def passed(message: str) -> None:
    print(f"PASS {message}")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> None:
    shown = " ".join(command)
    print(f"RUN  ({cwd}) {shown}")
    merged = os.environ.copy()
    if env:
        merged.update(env)
    result = subprocess.run(command, cwd=cwd, env=merged, text=True)
    if result.returncode != 0:
        fail(f"command failed ({result.returncode}): {shown}")


def clean_generated() -> None:
    for path in ROOT.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    for path in ROOT.rglob(".pytest_cache"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    shutil.rmtree(TS_TRACK / "dist-security", ignore_errors=True)


def doctor() -> None:
    print(f"course root: {ROOT}")
    for executable in ["python3", "node", "tsc", "mkdocs", "docker", "psql"]:
        path = shutil.which(executable)
        print(f"{executable:10} {path or 'not-available'}")
    passed("environment diagnostic complete; unavailable capabilities are not passes")


def verify_manifest(directory: Path, manifest_name: str = "MANIFEST.json") -> int:
    manifest = load_json(directory / manifest_name)
    listed = {entry["path"]: entry for entry in manifest["files"]}
    missing: list[str] = []
    changed: list[str] = []
    for relative, entry in listed.items():
        path = directory / relative
        if not path.is_file():
            missing.append(relative)
        elif path.stat().st_size != entry["size"] or sha256(path) != entry["sha256"]:
            changed.append(relative)
    if missing or changed:
        fail(f"manifest mismatch: missing={missing[:5]} changed={changed[:5]}")
    return len(listed)


def predecessor_proof() -> None:
    pred = CAPSTONE / "predecessor"
    count = verify_manifest(pred)
    contract = pred / "contract" / "openapi-api-1.2.bundle.yaml"
    if not contract.is_file():
        fail("predecessor API 1.2 bundle missing")
    migrations = sorted((pred / "migrations").glob("*.sql"))
    if [p.name[:3] for p in migrations] != ["001", "002", "003", "004", "005"]:
        fail("predecessor migrations 001-005 are incomplete")
    passed(f"predecessor integrity — {count} files, API 1.2, migrations 001-005")


def security_case_proof() -> None:
    case = CAPSTONE / "security-case"
    threats = load_yaml(case / "threats.yaml")["threats"]
    requirements = load_yaml(case / "requirements.yaml")["requirements"]
    proofs = load_yaml(case / "proof-map.yaml")["proofs"]
    assets = load_yaml(case / "assets.yaml")["assets"]
    actors = load_yaml(case / "actors.yaml")["actors"]
    boundaries = load_yaml(case / "boundaries.yaml")["boundaries"]

    def index(rows: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            identifier = row.get("id")
            if not isinstance(identifier, str) or not identifier:
                fail(f"{label} has missing identifier")
            if identifier in result:
                fail(f"duplicate {label} identifier {identifier}")
            result[identifier] = row
        return result

    asset_ids = index(assets, "asset")
    actor_ids = index(actors, "actor")
    boundary_ids = index(boundaries, "boundary")
    threat_ids = index(threats, "threat")
    requirement_ids = index(requirements, "requirement")
    proof_by_req: dict[str, list[dict[str, Any]]] = {}
    for proof in proofs:
        proof_by_req.setdefault(proof["requirement"], []).append(proof)

    for threat in threats:
        if threat["actor"] not in actor_ids:
            fail(f"{threat['id']} references unknown actor")
        for asset in threat["assets"]:
            if asset not in asset_ids:
                fail(f"{threat['id']} references unknown asset {asset}")
        for boundary in threat["boundaries"]:
            if boundary not in boundary_ids:
                fail(f"{threat['id']} references unknown boundary {boundary}")
        if threat.get("disposition") not in {"mitigate", "accept", "transfer", "avoid"}:
            fail(f"{threat['id']} has no valid disposition")
        for requirement in threat.get("requirements", []):
            if requirement not in requirement_ids:
                fail(f"{threat['id']} references unknown requirement {requirement}")
    for requirement in requirement_ids:
        if not proof_by_req.get(requirement):
            fail(f"requirement {requirement} has no proof mapping")

    operation_map = load_yaml(CAPSTONE / "predecessor" / "shared" / "operation-map.yaml")
    expected = set(operation_map["operations"]) | set(operation_map.get("releaseExtensions", {}))
    policies = load_yaml(case / "policy-matrix.yaml")["policies"]
    actual = [row["operationId"] for row in policies]
    if len(actual) != len(set(actual)):
        fail("duplicate operation policy row")
    if set(actual) != expected:
        fail(f"policy coverage mismatch missing={sorted(expected-set(actual))} extra={sorted(set(actual)-expected)}")

    jwks = load_json(CAPSTONE / "identity-provider" / "jwks.json")
    private_fields = {"d", "p", "q", "dp", "dq", "qi", "oth"}
    for key in jwks.get("keys", []):
        if private_fields.intersection(key):
            fail("public JWKS contains private key parameters")
    passed(f"security case — {len(threat_ids)} threats, {len(requirement_ids)} requirements, {len(expected)} operation policies")


def vector_proof() -> None:
    vector_dir = CAPSTONE / "shared" / "vectors"
    total = 0
    for path in sorted(vector_dir.glob("*.json")):
        data = load_json(path)
        for key in ("cases", "pathCases", "filenameCases", "archiveCases", "bucketCases", "permitCases"):
            rows = data.get(key, []) if isinstance(data, dict) else []
            ids: set[str] = set()
            for row in rows:
                identifier = row.get("id")
                if not isinstance(identifier, str) or identifier in ids:
                    fail(f"{path.name}:{key} has missing/duplicate case ID")
                ids.add(identifier)
                total += 1
    if total < 40:
        fail(f"hostile vector corpus unexpectedly small ({total})")
    passed(f"shared hostile vectors — {total} cases")


def migration_proof() -> None:
    own = sorted((CAPSTONE / "migrations").glob("*.sql"))
    if [p.name[:3] for p in own] != ["006", "007"]:
        fail("security migrations 006-007 missing or misordered")
    for track in [PY_TRACK, TS_TRACK]:
        predecessors = sorted((track / "migrations").glob("*.sql"))
        if [p.name[:3] for p in predecessors] != ["001", "002", "003", "004", "005"]:
            fail(f"{track.name} predecessor migration history changed")
    passed("migration boundary — predecessor 001-005 plus security 006-007")


def python_proof(module: str | None = None) -> None:
    mapping = {
        "02": ["test_strict_json.py", "test_edge.py", "test_fastapi_adapter.py"],
        "03": ["test_tokens.py", "test_api_keys.py"],
        "04": ["test_authorization.py"],
        "05": ["test_input_security.py"],
        "06": ["test_ssrf.py", "test_webhooks.py"],
        "07": ["test_secrets_audit.py"],
        "08": ["test_abuse.py"],
        "10": ["test_incident.py"],
    }
    tests = [str(PY_TRACK / "tests_security"), str(CAPSTONE / "tests")]
    if module in mapping:
        tests = [str(PY_TRACK / "tests_security" / name) for name in mapping[module]]
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    run([sys.executable, "-m", "pytest", "-q", *tests], cwd=PY_TRACK, env=env)
    clean_generated()
    passed("Python security proof" + (f" module {module}" if module else ""))


def typescript_proof() -> None:
    if shutil.which("tsc") is None or shutil.which("node") is None:
        fail("TypeScript core proof requires tsc and node")
    run(["tsc", "-p", "tsconfig.security-core.json"], cwd=TS_TRACK)
    run(["tsc", "-p", "tsconfig.audit.json"], cwd=TS_TRACK)
    tests = sorted(str(p.relative_to(TS_TRACK)) for p in (TS_TRACK / "test-security-core").glob("*.test.mjs"))
    run(["node", "--test", *tests], cwd=TS_TRACK)
    shutil.rmtree(TS_TRACK / "dist-security", ignore_errors=True)
    passed("TypeScript security core proof")


def incident_proof() -> None:
    env = {"PYTHONPATH": str(PY_TRACK / "src")}
    run([sys.executable, str(ROOT / "scripts" / "incident_drill.py")], cwd=ROOT, env=env)
    clean_generated()
    passed("incident exercise")


def release_proof() -> None:
    accepted = load_yaml(CAPSTONE / "releases" / "security-1.0" / "RELEASE.yaml")
    rejected = load_yaml(CAPSTONE / "releases" / "security-1.0-rejected-breaking" / "RELEASE.yaml")
    if accepted.get("publicApi") != "1.2.0" or accepted.get("compatibility") != "additive/internal-security-state":
        fail("accepted security release does not preserve API 1.2")
    if rejected.get("compatibility") != "breaking" or len(rejected.get("changes", [])) < 2:
        fail("rejected security release lacks explicit breaking changes")
    passed("static compatible security release and rejected breaking candidate")


def structure_proof() -> None:
    book = ROOT / "course-book"
    expected_common = {
        'index.md', 'exercises.md', 'exercise-answers.md', 'lab.md', 'checkpoint.md'
    }
    modules = sorted(p for p in book.glob("module-*") if p.is_dir())
    if len(modules) != 11:
        fail(f"expected 11 module directories, found {len(modules)}")
    for module in modules:
        names = {p.name for p in module.glob("*.md")}
        if module.name != "module-00-orientation" and not expected_common.issubset(names):
            fail(f"{module.name} missing {sorted(expected_common-names)}")
        if module.name == "module-00-orientation" and not {"index.md", "lab.md", "checkpoint.md"}.issubset(names):
            fail("orientation is incomplete")
    for required in ['README.md', 'Makefile', 'mkdocs.yml', 'course.json']:
        if not (ROOT / required).is_file():
            fail(f'missing top-level file {required}')
    passed(f"course structure — {len(modules)} modules and {len(list(book.rglob('*.md')))} course-book pages")


def markdown_links() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    checked = 0
    broken: list[str] = []
    for page in ROOT.rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        # Remove fenced code to avoid command examples that resemble links.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in pattern.findall(text):
            target = target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#", "sandbox:")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            checked += 1
            destination = (page.parent / relative).resolve()
            if not destination.exists():
                broken.append(f"{page.relative_to(ROOT)} -> {target}")
    if broken:
        fail("broken Markdown links: " + "; ".join(broken[:10]))
    passed(f"Markdown links — {checked} local targets")


def education_proof() -> None:
    prohibited = re.compile(r"\b(TODO|TBD|lorem ipsum|coming soon|fill this in)\b", re.I)
    hits: list[str] = []
    paragraphs: dict[str, int] = {}
    for page in ROOT.rglob("*.md"):
        if "planted-defects" in page.parts:
            continue
        text = page.read_text(encoding="utf-8")
        if prohibited.search(text):
            hits.append(str(page.relative_to(ROOT)))
        for paragraph in re.split(r"\n\s*\n", text):
            normalized = " ".join(paragraph.split())
            if len(normalized) >= 180 and not normalized.startswith(("```", "|")):
                paragraphs[normalized] = paragraphs.get(normalized, 0) + 1
    repeated = [p for p, count in paragraphs.items() if count >= 8]
    if hits:
        fail(f"unfinished markers in {hits[:8]}")
    if repeated:
        fail("educational paragraph repeated eight or more times")
    passed("educational quality guard")


def hygiene_proof() -> None:
    forbidden_dirs = {"__pycache__", ".pytest_cache", "node_modules", "dist-security", ".mypy_cache", ".ruff_cache"}
    found = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_dir() and p.name in forbidden_dirs]
    if found:
        fail(f"generated/cache directories present: {found[:10]}")
    private = CAPSTONE / "identity-provider" / "private" / "fixture-private.pem"
    handoff = CAPSTONE / "handoff"
    if handoff.exists():
        for path in handoff.rglob("*"):
            if path.is_file() and ("PRIVATE KEY" in path.read_text(encoding="utf-8", errors="ignore") or "fixture-pepper" in path.read_text(encoding="utf-8", errors="ignore")):
                fail(f"private fixture material in outgoing handoff: {path.relative_to(ROOT)}")
    passed("repository hygiene and handoff secret guard")


def iter_manifest_files() -> Iterable[Path]:
    excluded_names = {"MANIFEST.json", "MANIFEST.sha256"}
    excluded_dirs = {"__pycache__", ".pytest_cache", "node_modules", "dist-security", ".ruff_cache", ".mypy_cache"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name in excluded_names:
            continue
        if any(part in excluded_dirs for part in path.relative_to(ROOT).parts):
            continue
        yield path


def manifest_create() -> None:
    files = [
        {"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p), "size": p.stat().st_size}
        for p in iter_manifest_files()
    ]
    payload = {"algorithm": "sha256", "root": "programs/api-engineering/03-api-security-engineering", "files": files}
    manifest = ROOT / "MANIFEST.json"
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / "MANIFEST.sha256").write_text(f"{sha256(manifest)}  MANIFEST.json\n", encoding="utf-8")
    passed(f"course manifest created — {len(files)} payload files")


def manifest_proof() -> None:
    checksum_line = (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").split()[0]
    if checksum_line != sha256(ROOT / "MANIFEST.json"):
        fail("MANIFEST.json checksum mismatch")
    count = verify_manifest(ROOT)
    actual = {p.relative_to(ROOT).as_posix() for p in iter_manifest_files()}
    listed = {x["path"] for x in load_json(ROOT / "MANIFEST.json")["files"]}
    if actual != listed:
        fail(f"manifest coverage mismatch missing={sorted(actual-listed)[:5]} stale={sorted(listed-actual)[:5]}")
    passed(f"course manifest — {count} exact files")


def module_proof(module: str, track: str) -> None:
    if module == "01":
        security_case_proof()
    elif module == "09":
        vector_proof(); python_proof(); typescript_proof(); education_proof()
    elif module == "10":
        python_proof("10"); incident_proof(); release_proof()
    else:
        if track == "python":
            python_proof(module)
        elif track == "typescript":
            typescript_proof()
        else:
            fail("TRACK must be python or typescript")


def core_proof() -> None:
    predecessor_proof()
    security_case_proof()
    vector_proof()
    migration_proof()
    structure_proof()
    python_proof()
    typescript_proof()
    incident_proof()
    release_proof()
    markdown_links()
    education_proof()
    hygiene_proof()
    passed("API Security Engineering core proof")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    for name in ["predecessor-proof", "security-case-proof", "vector-proof", "migration-proof", "python-proof", "typescript-core-proof", "incident-proof", "release-proof", "structure-proof", "markdown-link-proof", "education-proof", "hygiene-proof", "core-proof", "manifest-create", "manifest-proof"]:
        sub.add_parser(name)
    module = sub.add_parser("module-proof")
    module.add_argument("--module", required=True)
    module.add_argument("--track", choices=["python", "typescript"], required=True)
    args = parser.parse_args()
    commands = {
        "doctor": doctor,
        "predecessor-proof": predecessor_proof,
        "security-case-proof": security_case_proof,
        "vector-proof": vector_proof,
        "migration-proof": migration_proof,
        "python-proof": python_proof,
        "typescript-core-proof": typescript_proof,
        "incident-proof": incident_proof,
        "release-proof": release_proof,
        "structure-proof": structure_proof,
        "markdown-link-proof": markdown_links,
        "education-proof": education_proof,
        "hygiene-proof": hygiene_proof,
        "core-proof": core_proof,
        "manifest-create": manifest_create,
        "manifest-proof": manifest_proof,
    }
    if args.command == "module-proof":
        module_proof(args.module.zfill(2), args.track)
    else:
        commands[args.command]()


if __name__ == "__main__":
    main()
