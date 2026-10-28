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
import tempfile
import zipfile

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyYAML is required for dependency-light proofs: {exc}")

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capstone"
PY_SRC = CAP / "tracks/python-grpc/src"
PY_TESTS = CAP / "tracks/python-grpc/tests"
TS = CAP / "tracks/typescript-grpc"

def run(cmd: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> None:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, env=merged, check=True)

def read_json(path: Path):
    return json.loads(path.read_text())

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_manifest(directory: Path) -> int:
    manifest_path = directory / "MANIFEST.json"
    digest_path = directory / "MANIFEST.sha256"
    if not manifest_path.exists() or not digest_path.exists():
        raise AssertionError(f"missing manifest in {directory}")
    expected_digest = digest_path.read_text().split()[0]
    assert sha(manifest_path) == expected_digest, "manifest digest mismatch"
    manifest = read_json(manifest_path)
    for item in manifest["files"]:
        path = directory / item["path"]
        assert path.is_file(), f"missing {item['path']}"
        assert path.stat().st_size == item["size"], f"size mismatch {item['path']}"
        assert sha(path) == item["sha256"], f"digest mismatch {item['path']}"
    return len(manifest["files"])

def doctor() -> None:
    print("python", sys.version.split()[0])
    for tool in ["node", "tsc", "protoc", "buf", "grpcurl", "mkdocs", "psql"]:
        print(f"{tool}: {shutil.which(tool) or 'not-available'}")
    try:
        import grpc
        import google.protobuf
        print("grpcio", grpc.__version__)
        print("protobuf", google.protobuf.__version__)
    except Exception as exc:
        print("python grpc runtime unavailable:", exc)

def predecessor_proof() -> None:
    count = verify_manifest(CAP / "predecessor/handoff")
    assert count == 48 or count == 50, f"unexpected handoff file count {count}"
    print(f"PASS predecessor handoff — {count} files")

def orientation_proof() -> None:
    predecessor_proof()
    contract_proof()
    boundary_proof()
    print("PASS orientation readiness proof")

def structure_proof() -> None:
    book = ROOT / "course-book"
    pages = sorted(book.rglob("*.md"))
    assert len(pages) == 59, f"expected 59 course-book pages, found {len(pages)}"
    module_dirs = sorted(p for p in book.glob("module-[0-9][0-9]-*") if p.is_dir())
    assert len(module_dirs) == 11, f"expected orientation plus 10 modules, found {len(module_dirs)}"
    required = {"index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"}
    numbered = [p for p in module_dirs if not p.name.startswith("module-00-")]
    assert len(numbered) == 10
    exercise_total = 0
    answer_total = 0
    for d in numbered:
        assert {p.name for p in d.glob("*.md")} == required, f"module shape mismatch {d.name}"
        ex = (d / "exercises.md").read_text()
        ans = (d / "exercise-answers.md").read_text()
        ex_head = re.findall(r"^## (\d+)\. (.+)$", ex, re.M)
        ans_head = re.findall(r"^## (\d+)\. (.+)$", ans, re.M)
        assert ex_head == ans_head, f"exercise/answer heading mismatch {d.name}"
        assert len(ex_head) == 12, f"expected 12 exercises in {d.name}"
        exercise_total += len(ex_head)
        answer_total += len(ans_head)
        lab = (d / "lab.md").read_text()
        for h in ["## Setup", "## Controlled actions", "## Correctness oracle",
                  "## Required evidence", "## Cleanup", "## Completion gate"]:
            assert h in lab, f"missing {h} in {d.name}/lab.md"
        checkpoint = (d / "checkpoint.md").read_text()
        assert "## Non-compensable gate" in checkpoint
    assert exercise_total == answer_total == 120
    print("PASS course structure — 59 pages, 120 exercises and answers")

def contract_proof() -> None:
    descriptor = read_json(CAP / "contracts/descriptors/analysis-v1.json")
    assert descriptor["package"] == "bijux.analysis.v1"
    assert descriptor["syntax"] == "proto3"
    enum = descriptor["enums"]["RunState"]
    assert enum[0] == {"name":"RUN_STATE_UNSPECIFIED","number":0}
    methods = [
        method for methods in descriptor["services"].values() for method in methods
    ]
    assert len(methods) == 7
    expected_shapes = {
        "CreateRun":(False,False), "GetRun":(False,False),
        "CancelRun":(False,False), "WatchRun":(False,True),
        "UploadDataset":(True,False), "DownloadArtifact":(False,True),
        "Work":(True,True),
    }
    for method in methods:
        assert (method["client_streaming"], method["server_streaming"]) == expected_shapes[method["name"]]
    for message, shape in descriptor["messages"].items():
        tags = [field["number"] for field in shape["fields"]]
        assert len(tags) == len(set(tags)), f"duplicate tags in {message}"
    run_fields = {f["name"]:f for f in descriptor["messages"]["AnalysisRun"]["fields"]}
    assert run_fields["result_summary"]["proto3_optional"]
    assert run_fields["failure_code"]["proto3_optional"]
    source = (CAP / "contracts/proto/bijux/analysis/v1/analysis.proto").read_text()
    assert "RUN_STATE_UNSPECIFIED = 0;" in source
    assert 'edition = "2024";' in (CAP / "contracts/proto/frontier/analysis_edition_2024.proto").read_text()
    print("PASS contract profile — 3 services, 7 methods, proto3 baseline, Editions frontier")

def descriptor_proof() -> None:
    env = {"PYTHONPATH": str(PY_SRC)}
    code = r"""
from analysis_rpc import analysis_pb2
from google.protobuf import descriptor_pb2
from pathlib import Path

source = descriptor_pb2.FileDescriptorProto()
source.ParseFromString(Path("capstone/contracts/descriptors/analysis-v1.pb").read_bytes())
runtime = analysis_pb2.DESCRIPTOR

assert source.name == runtime.name
assert source.package == runtime.package
assert source.syntax == "proto3"
assert {m.name for m in source.message_type} == set(runtime.message_types_by_name)
assert {e.name for e in source.enum_type} == set(runtime.enum_types_by_name)
assert {svc.name for svc in source.service} == set(runtime.services_by_name)

for message in source.message_type:
    actual = runtime.message_types_by_name[message.name]
    expected_fields = {
        field.name: (field.number, field.type, field.type_name)
        for field in message.field
    }
    actual_fields = {
        field.name: (
            field.number,
            field.type,
            field.message_type.full_name if field.message_type else
            field.enum_type.full_name if field.enum_type else "",
        )
        for field in actual.fields
    }
    for name, (number, field_type, type_name) in expected_fields.items():
        actual_number, actual_type, actual_type_name = actual_fields[name]
        assert actual_number == number
        assert actual_type == field_type
        normalized = type_name.lstrip(".")
        assert actual_type_name == normalized or not normalized

for service in source.service:
    actual = runtime.services_by_name[service.name]
    expected = {
        method.name: (
            method.client_streaming,
            method.server_streaming,
            method.input_type.lstrip("."),
            method.output_type.lstrip("."),
        )
        for method in service.method
    }
    observed = {
        method.name: (
            method.client_streaming,
            method.server_streaming,
            method.input_type.full_name,
            method.output_type.full_name,
        )
        for method in actual.methods
    }
    assert expected == observed

print("PASS descriptor semantic parity", len(source.message_type), "messages")
"""
    run([sys.executable, "-c", code], env=env)

def boundary_proof() -> None:
    policy = yaml.safe_load((CAP / "rpc-case/interaction-decisions.yaml").read_text())
    forms = {x["capability"]:x["form"] for x in policy["interactions"]}
    assert forms["public run creation"] == "HTTP"
    assert forms["committed run facts"] == "durable-event"
    assert forms["domain validation and transactional mutation"] == "local-call"
    assert forms["internal run control"] == "gRPC"
    assert len(policy["rejected"]) >= 2
    print("PASS interaction boundary proof")

def model_proof() -> None:
    vectors = read_json(CAP / "shared/vectors/int64.json")["cases"]
    assert any(x["decimal"] == "9007199254740992" and x["valid"] for x in vectors)
    assert any(x["decimal"] == "9223372036854775808" and not x["valid"] for x in vectors)
    golden = read_json(CAP / "shared/golden/analysis-run-v1.json")
    assert sha(CAP / "shared/golden/analysis-run-v1.bin") == golden["sha256"]
    print("PASS model and golden-wire proof")

def compatibility_proof() -> None:
    accepted = read_json(CAP / "releases/rpc-1.1/compatibility-report.json")
    assert accepted["classification"]["wire"] == "compatible"
    rejected = sorted((CAP / "releases").glob("rejected-*/candidate.json"))
    assert len(rejected) == 7
    for path in rejected:
        data = read_json(path)
        assert data["expected"] == "reject"
    policy = yaml.safe_load((CAP / "contracts/compatibility-policy.yaml").read_text())
    assert policy["rules"]["field_numbers"]["reuse"] == "forbidden"
    print("PASS compatibility proof — 1 accepted candidate, 7 rejected candidates")

def vector_proof(name: str) -> None:
    data = read_json(CAP / f"shared/vectors/{name}.json")
    assert data["cases"], f"empty vector file {name}"
    ids = [case["id"] for case in data["cases"]]
    assert len(ids) == len(set(ids)), f"duplicate vector ids in {name}"
    print(f"PASS {name} vectors — {len(ids)} cases")

def migration_proof() -> None:
    canonical = sorted((CAP / "database/migrations").glob("*.sql"))
    assert [p.name[:3] for p in canonical] == [f"{i:03d}" for i in range(1,16)]
    for track in ["python-grpc", "typescript-grpc"]:
        other = CAP / f"tracks/{track}/migrations"
        for source in canonical:
            target = other / source.name
            assert target.is_file() and source.read_bytes() == target.read_bytes(), f"migration drift {track}/{source.name}"
    print("PASS migrations 001–015 and track parity")

def _remove_generated() -> None:
    for path in ROOT.rglob("__pycache__"):
        shutil.rmtree(path, ignore_errors=True)
    for path in ROOT.rglob("*.pyc"):
        path.unlink(missing_ok=True)
    shutil.rmtree(TS / "dist", ignore_errors=True)

def python_proof(network: bool = True) -> None:
    env = {"PYTHONPATH": str(PY_SRC)}
    pattern = "test_*.py" if network else "test_core.py"
    try:
        run([sys.executable, "-m", "unittest", "discover", "-s", str(PY_TESTS), "-p", pattern, "-v"], env=env)
    finally:
        _remove_generated()

def typescript_proof() -> None:
    try:
        run(["tsc", "-p", "tsconfig.json"], cwd=TS)
        tests = [str(p.relative_to(TS)) for p in sorted((TS / "test-js").glob("*.test.mjs"))]
        run(["node", "--test", *tests], cwd=TS)
    finally:
        _remove_generated()

def release_proof() -> None:
    release = read_json(CAP / "releases/rpc-1.0/release-report.json")
    assert release["decision"] == "accepted"
    assert all(value == "pass" for value in release["gates"].values())
    assert release["unexecuted"], "evidence boundary must be explicit"
    dossier = yaml.safe_load((CAP / "handoff/service-boundary-dossier.yaml").read_text())
    assert any(x["recommendation"] == "keep-cohesive" for x in dossier["candidates"])
    print("PASS release and boundary-dossier proof")

def planted_defect_proof() -> None:
    defects = sorted((CAP / "planted-defects").glob("RPC-*/defect.json"))
    assert len(defects) == 10
    proofs = set()
    for path in defects:
        data = read_json(path)
        assert data["expected_rejection"]
        proofs.add(data["expected_rejection"])
    assert len(proofs) >= 8
    print("PASS planted defects — 10 assigned rejection proofs")

def handoff_proof() -> None:
    count = verify_manifest(CAP / "handoff")
    assert count >= 20
    print(f"PASS Course 8 handoff — {count} files")

def markdown_link_proof() -> None:
    checked = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text()
        for target in pattern.findall(text):
            if target.startswith(("http://","https://","#","mailto:")):
                continue
            target = target.split("#",1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            assert str(resolved).startswith(str(ROOT.resolve())), f"link escapes course: {path} -> {target}"
            assert resolved.exists(), f"broken link: {path.relative_to(ROOT)} -> {target}"
            checked += 1
    print(f"PASS Markdown links — {checked} local targets")

def education_proof() -> None:
    book = ROOT / "course-book"
    total = 0
    chapter_words = []
    for path in book.rglob("*.md"):
        words = len(re.findall(r"\b[\w][\w'-]*\b", path.read_text()))
        total += words
        if re.match(r"module-(0[1-9]|10)-", path.parent.name) and path.name == "index.md":
            chapter_words.append((path.parent.name, words))
    assert total >= 35000, f"course book too thin: {total}"
    assert len(chapter_words) == 10
    for name, words in chapter_words:
        assert words >= 1500, f"main chapter too thin {name}: {words}"
    banned = ["lorem ipsum", "TODO", "TBD", "coming soon", "fill this in later"]
    combined = "\n".join(p.read_text() for p in book.rglob("*.md"))
    for phrase in banned:
        assert phrase.lower() not in combined.lower(), f"unfinished marker: {phrase}"
    print(f"PASS educational depth — {total} course-book words")

def hygiene_proof() -> None:
    forbidden_dirs = {"__pycache__", ".pytest_cache", "node_modules", "dist", "site", ".DS_Store", "__MACOSX"}
    bad = [p for p in ROOT.rglob("*") if p.name in forbidden_dirs]
    assert not bad, "generated or forbidden paths present: " + ", ".join(str(p.relative_to(ROOT)) for p in bad)
    for path in ROOT.rglob("*"):
        if path.is_file():
            assert not path.name.endswith((".pyc",".log")), f"generated file {path}"
    print("PASS repository hygiene")

def capstone_tour() -> None:
    env = {"PYTHONPATH": str(PY_SRC)}
    try:
        run([sys.executable, "-m", "analysis_rpc.tour"], env=env)
    finally:
        _remove_generated()

def docs_build() -> None:
    if not shutil.which("mkdocs"):
        raise SystemExit("NOT EXECUTED: mkdocs is not installed")
    run(["mkdocs", "build", "--strict"])

def protoc_proof() -> None:
    if not shutil.which("protoc"):
        raise SystemExit("NOT EXECUTED: protoc is not installed")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "descriptor.pb"
        run([
            "protoc",
            f"--proto_path={CAP / 'contracts/proto'}",
            f"--descriptor_set_out={out}",
            "--include_imports",
            str(CAP / "contracts/proto/bijux/analysis/v1/analysis.proto"),
        ])
        assert out.stat().st_size > 0
        print("PASS protoc descriptor generation")

def buf_proof() -> None:
    if not shutil.which("buf"):
        raise SystemExit("NOT EXECUTED: buf is not installed")
    run(["buf", "lint"])
    print("PASS Buf lint")

def grpcurl_proof() -> None:
    if not shutil.which("grpcurl"):
        raise SystemExit("NOT EXECUTED: grpcurl is not installed")
    raise SystemExit("NOT EXECUTED: run the documented live reflection lab with an explicitly enabled reflection server")

def manifest_proof() -> None:
    count = verify_manifest(ROOT)
    print(f"PASS course manifest — {count} files")

def core_proof() -> None:
    predecessor_proof()
    structure_proof()
    contract_proof()
    descriptor_proof()
    boundary_proof()
    model_proof()
    compatibility_proof()
    for name in ["presence","int64","status","deadlines","retries","streaming","flow-control","security","lifecycle"]:
        vector_proof(name)
    migration_proof()
    python_proof(network=True)
    typescript_proof()
    release_proof()
    planted_defect_proof()
    handoff_proof()
    markdown_link_proof()
    education_proof()
    hygiene_proof()
    print("PASS Course 7 dependency-light core proof")

def full_proof() -> None:
    core_proof()
    docs_build()
    protoc_proof()
    buf_proof()

COMMANDS = {
    "doctor": doctor,
    "predecessor-proof": predecessor_proof,
    "orientation-proof": orientation_proof,
    "structure-proof": structure_proof,
    "contract-proof": contract_proof,
    "descriptor-proof": descriptor_proof,
    "boundary-proof": boundary_proof,
    "model-proof": model_proof,
    "compatibility-proof": compatibility_proof,
    "unary-proof": lambda: vector_proof("status"),
    "deadline-proof": lambda: (vector_proof("deadlines"), vector_proof("retries")),
    "streaming-proof": lambda: (vector_proof("streaming"), vector_proof("flow-control")),
    "security-proof": lambda: vector_proof("security"),
    "lifecycle-proof": lambda: vector_proof("lifecycle"),
    "governance-proof": lambda: (contract_proof(), descriptor_proof(), release_proof()),
    "migration-proof": migration_proof,
    "python-proof": lambda: python_proof(network=False),
    "python-network-proof": lambda: python_proof(network=True),
    "typescript-proof": typescript_proof,
    "release-proof": release_proof,
    "planted-defect-proof": planted_defect_proof,
    "handoff-proof": handoff_proof,
    "markdown-link-proof": markdown_link_proof,
    "education-proof": education_proof,
    "hygiene-proof": hygiene_proof,
    "capstone-tour": capstone_tour,
    "core-proof": core_proof,
    "full-proof": full_proof,
    "manifest-proof": manifest_proof,
    "docs-build": docs_build,
    "protoc-proof": protoc_proof,
    "buf-proof": buf_proof,
    "grpcurl-proof": grpcurl_proof,
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args()
    COMMANDS[args.command]()

if __name__ == "__main__":
    main()
