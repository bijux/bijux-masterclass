#!/usr/bin/env python3
"""Program-wide reader, handoff, syntax, data, and release proofs."""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
from typing import Any, Iterable
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
COURSES = [
    "01-openapi-contract-engineering",
    "02-contract-driven-api-service-engineering",
    "03-api-security-engineering",
    "04-api-reliability-and-observability-engineering",
    "05-api-performance-capacity-and-traffic-engineering",
    "06-event-driven-api-engineering",
    "07-grpc-and-protobuf-engineering",
    "08-distributed-api-architecture-and-microservices-engineering",
    "09-graphql-schema-and-runtime-engineering",
    "10-api-platform-governance-and-developer-experience-engineering",
]
PROGRAM_BOOK_FILES = {
    "index.md", "start-here.md", "ten-course-journey.md", "course-map.md",
    "analysis-runs-platform.md", "capstone-evolution.md",
    "version-and-handoff-ledger.md", "language-and-code-strategy.md",
    "evidence-model.md", "study-and-assessment.md", "standards-map.md",
    "final-program-defense.md", "glossary.md",
}
COURSE_GUIDES = {
    "index.md", "start-here.md", "study-plan.md", "capstone.md",
    "standards.md", "evidence-model.md", "language-strategy.md", "glossary.md",
}
MODULE_FILES = {"index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"}
ORIENTATION_FILES = {"index.md", "lab.md", "checkpoint.md"}
LAB_HEADINGS = {
    "## Objective", "## Why this lab matters", "## Setup conditions",
    "## Hypothesis", "## Controlled action and investigation",
    "## Operational oracle", "## Required evidence",
    "## Interpretation and defense", "## Cleanup and reset",
    "## Completion gate",
}
CHECKPOINT_HEADINGS = {
    "## Required result", "## Demonstrate", "## Commands",
    "## Evidence to retain", "## Defend the design", "## Continue only when",
}
CHAPTER_MARKERS = {
    "**Program stage:**", "**Central question:**", "## Where this module fits",
    "## Learning outcomes", "## Capstone increment", "## Module synthesis",
    "## Next in the story",
}
EXCLUDED_DIRS = {
    ".git", ".venv", "node_modules", "site", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".runtime", ".tmp", "dist-core", "work",
}
ROOT_MANIFESTS = {ROOT / "MANIFEST.json", ROOT / "MANIFEST.sha256"}
HANDOFF_PAIRS = [
    ("Course 1 → 2", ROOT/COURSES[0]/"capstone/handoff", ROOT/COURSES[1]/"predecessor"),
    ("Course 2 → 3", ROOT/COURSES[1]/"capstone/handoff", ROOT/COURSES[2]/"capstone/predecessor"),
    ("Course 3 → 4", ROOT/COURSES[2]/"capstone/handoff", ROOT/COURSES[3]/"capstone/predecessor/handoff"),
    ("Course 4 → 5", ROOT/COURSES[3]/"capstone/handoff", ROOT/COURSES[4]/"capstone/predecessor/handoff"),
    ("Course 5 → 6", ROOT/COURSES[4]/"capstone/handoff", ROOT/COURSES[5]/"capstone/predecessor/handoff"),
    ("Course 6 → 7", ROOT/COURSES[5]/"capstone/handoff", ROOT/COURSES[6]/"capstone/predecessor/handoff"),
    ("Course 7 → 8", ROOT/COURSES[6]/"capstone/handoff", ROOT/COURSES[7]/"capstone/predecessor/handoff"),
    ("Course 8 → 9", ROOT/COURSES[7]/"capstone/handoff", ROOT/COURSES[8]/"capstone/predecessor/handoff"),
    ("Course 9 → 10", ROOT/COURSES[8]/"capstone/handoff", ROOT/COURSES[9]/"capstone/predecessor/handoff"),
]


def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def course_dirs() -> list[Path]:
    return [ROOT / name for name in COURSES]


def learner_pages() -> list[Path]:
    pages = sorted((ROOT / "program-book").glob("*.md"))
    for course in course_dirs():
        pages.extend(sorted((course / "course-book").rglob("*.md")))
    return pages


def numbered_modules(course: Path) -> list[Path]:
    return sorted(
        path for path in (course / "course-book").glob("module-[0-9][0-9]-*")
        if path.is_dir() and not path.name.startswith("module-00-")
    )


def numbered_headings(path: Path) -> list[tuple[str, str]]:
    return re.findall(r"(?m)^##\s+(\d+)\.\s+(.+?)\s*$", read(path))


def eligible(path: Path, root: Path = ROOT) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
        return False
    if path in ROOT_MANIFESTS:
        return False
    if path.name.startswith("last-") and "reports" in rel.parts:
        return False
    return True


def payload_files() -> list[Path]:
    return [p for p in sorted(ROOT.rglob("*")) if eligible(p)]


def structure() -> None:
    failures: list[str] = []
    program_files = {p.name for p in (ROOT / "program-book").glob("*.md")}
    if program_files != PROGRAM_BOOK_FILES:
        failures.append(f"program-book mismatch missing={sorted(PROGRAM_BOOK_FILES-program_files)} extra={sorted(program_files-PROGRAM_BOOK_FILES)}")
    if len(COURSES) != 10:
        failures.append("program course registry must contain ten courses")
    module_total = 0
    page_total = 0
    for index, course in enumerate(course_dirs(), 1):
        if not course.is_dir():
            failures.append(f"missing {course.name}")
            continue
        for name in ("README.md", "Makefile", "mkdocs.yml", "course.json"):
            if not (course / name).is_file():
                failures.append(f"missing {course.name}/{name}")
        try:
            meta = json.loads(read(course / "course.json"))
            if meta.get("number") != index or meta.get("directory") != course.name:
                failures.append(f"metadata identity mismatch in {course.name}/course.json")
            if len(meta.get("modules", [])) != 10:
                failures.append(f"{course.name}/course.json must declare ten modules")
        except Exception as exc:
            failures.append(f"invalid {course.name}/course.json: {exc}")
        book = course / "course-book"
        roots = {p.name for p in book.glob("*.md")}
        if roots != COURSE_GUIDES:
            failures.append(f"{course.name} guide mismatch missing={sorted(COURSE_GUIDES-roots)} extra={sorted(roots-COURSE_GUIDES)}")
        pages = list(book.rglob("*.md")); page_total += len(pages)
        if len(pages) != 61:
            failures.append(f"{course.name} has {len(pages)} course-book pages, expected 61")
        dirs = sorted(p for p in book.glob("module-[0-9][0-9]-*") if p.is_dir())
        orientation = [p for p in dirs if p.name.startswith("module-00-")]
        numbered = [p for p in dirs if not p.name.startswith("module-00-")]
        module_total += len(numbered)
        if len(orientation) != 1 or len(numbered) != 10:
            failures.append(f"{course.name} must contain one orientation and ten numbered modules")
            continue
        if {p.name for p in orientation[0].glob("*.md")} != ORIENTATION_FILES:
            failures.append(f"orientation file shape mismatch in {course.name}")
        for module in numbered:
            files = {p.name for p in module.glob("*.md")}
            if files != MODULE_FILES:
                failures.append(f"module file shape mismatch {module.relative_to(ROOT)}")
    if module_total != 100 or page_total != 610:
        failures.append(f"program totals are {module_total} numbered modules and {page_total} course pages; expected 100 and 610")
    if failures:
        fail("program structure:\n" + "\n".join(failures[:150]))
    print("PASS structure — ten courses, 100 numbered modules, 610 course pages, 13 program pages")


def flatten_nav(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        if value.endswith(".md"):
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_nav(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_nav(item)


def nav_proof() -> None:
    import yaml
    expected = {p.relative_to(ROOT).as_posix() for p in learner_pages()}
    config = yaml.safe_load(read(ROOT / "mkdocs.yml"))
    listed = list(flatten_nav(config.get("nav", [])))
    if set(listed) != expected or len(listed) != len(expected):
        fail(f"root nav mismatch missing={sorted(expected-set(listed))[:12]} extra={sorted(set(listed)-expected)[:12]} duplicates={len(listed)-len(set(listed))}")
    for course in course_dirs():
        expected_course = {p.relative_to(course / "course-book").as_posix() for p in (course / "course-book").rglob("*.md")}
        local = yaml.safe_load(read(course / "mkdocs.yml"))
        listed_course = list(flatten_nav(local.get("nav", [])))
        if set(listed_course) != expected_course or len(listed_course) != len(expected_course):
            fail(f"{course.name} nav mismatch")
    print(f"PASS navigation — {len(expected)} learner pages listed exactly once")


def directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        fail(f"missing handoff directory {directory.relative_to(ROOT)}")
    return {p.relative_to(directory).as_posix(): sha256(p) for p in sorted(directory.rglob("*")) if p.is_file() and p.name != ".DS_Store"}


def handoff_proof() -> None:
    total = 0
    for label, source, target in HANDOFF_PAIRS:
        left = directory_hashes(source); right = directory_hashes(target)
        if left != right:
            fail(f"{label} handoff mismatch missing={sorted(set(left)-set(right))[:8]} extra={sorted(set(right)-set(left))[:8]} changed={sorted(k for k in set(left)&set(right) if left[k]!=right[k])[:8]}")
        total += len(left)
        print(f"PASS {label} handoff — {len(left)} exact files")
    print(f"PASS all adjacent handoffs — {total} file comparisons")


def markdown_targets(path: Path) -> Iterable[str]:
    text = read(path)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
        yield target.strip().split()[0].strip("<>")


def links() -> None:
    failures: list[str] = []; checked = 0
    for page in learner_pages():
        for target in markdown_targets(page):
            if not target or target.startswith(("http://", "https://", "mailto:", "#", "sandbox:")):
                continue
            rel = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not rel:
                continue
            checked += 1
            candidate = (page.parent / rel).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{page.relative_to(ROOT)} escapes program root: {target}")
                continue
            if not candidate.exists():
                failures.append(f"{page.relative_to(ROOT)} -> {target}")
    if failures:
        fail("broken learner links:\n" + "\n".join(failures[:120]))
    print(f"PASS learner links — {checked} local targets")


def quality() -> None:
    failures: list[str] = []
    exercise_total = answer_total = lab_total = checkpoint_total = 0
    for course in course_dirs():
        for module in numbered_modules(course):
            chapter = read(module / "index.md")
            missing = [marker for marker in CHAPTER_MARKERS if marker not in chapter]
            if missing:
                failures.append(f"{(module/'index.md').relative_to(ROOT)} missing {missing}")
            if words(chapter) < 1500:
                failures.append(f"{(module/'index.md').relative_to(ROOT)} has only {words(chapter)} words")
            questions = numbered_headings(module / "exercises.md")
            answers = numbered_headings(module / "exercise-answers.md")
            exercise_total += len(questions); answer_total += len(answers)
            if len(questions) != 12 or questions != answers:
                failures.append(f"exercise/answer mismatch in {module.relative_to(ROOT)}")
            lab = read(module / "lab.md"); lab_total += 1
            if words(lab) < 250:
                failures.append(f"lab too thin: {(module/'lab.md').relative_to(ROOT)}")
            lab_headers = {line.strip() for line in lab.splitlines() if line.startswith("## ")}
            if LAB_HEADINGS - lab_headers:
                failures.append(f"lab headings missing in {module.relative_to(ROOT)}: {sorted(LAB_HEADINGS-lab_headers)}")
            checkpoint = read(module / "checkpoint.md"); checkpoint_total += 1
            if words(checkpoint) < 130:
                failures.append(f"checkpoint too thin: {(module/'checkpoint.md').relative_to(ROOT)}")
            cp_headers = {line.strip() for line in checkpoint.splitlines() if line.startswith("## ")}
            if CHECKPOINT_HEADINGS - cp_headers:
                failures.append(f"checkpoint headings missing in {module.relative_to(ROOT)}: {sorted(CHECKPOINT_HEADINGS-cp_headers)}")
    if (exercise_total, answer_total, lab_total, checkpoint_total) != (1200, 1200, 100, 100):
        failures.append(f"totals are exercises={exercise_total}, answers={answer_total}, labs={lab_total}, checkpoints={checkpoint_total}")
    # Reader-facing unfinished/filler markers.
    forbidden = re.compile(r"(?i)\b(TBD|TO BE WRITTEN|COMING SOON|LOREM IPSUM)\b|A course term used in")
    for page in learner_pages():
        if forbidden.search(read(page)):
            failures.append(f"unfinished or placeholder prose in {page.relative_to(ROOT)}")
    # Exact long paragraphs should not be mechanically repeated through numbered modules.
    paragraphs: dict[str, list[str]] = defaultdict(list)
    for course in course_dirs():
        for module in numbered_modules(course):
            for page in module.glob("*.md"):
                for block in re.split(r"\n\s*\n", read(page)):
                    value = " ".join(line.strip() for line in block.strip().splitlines())
                    if len(value) < 220 or value.startswith(("#", "```", "|")):
                        continue
                    value = re.sub(r"\s+", " ", value)
                    paragraphs[value].append(str(page.relative_to(ROOT)))
    repeated = [(text, paths) for text, paths in paragraphs.items() if len(paths) >= 5]
    if repeated:
        text, paths = sorted(repeated, key=lambda item: len(item[1]), reverse=True)[0]
        failures.append(f"mechanically repeated module paragraph appears {len(paths)} times: {text[:180]}")
    if failures:
        fail("learner quality:\n" + "\n".join(failures[:160]))
    total_words = sum(words(read(p)) for p in learner_pages())
    print(f"PASS reader quality — 1,200 matched exercises, 100 labs, 100 checkpoints, {total_words:,} learner words")


def python_syntax() -> None:
    files = [p for p in ROOT.rglob("*.py") if eligible(p)]
    failures = []
    for path in files:
        try:
            compile(read(path), str(path), "exec")
        except SyntaxError as exc:
            failures.append(f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.msg}")
    if failures:
        fail("Python syntax:\n" + "\n".join(failures[:80]))
    print(f"PASS Python syntax — {len(files)} files")


def javascript_syntax() -> None:
    files = [p for p in ROOT.rglob("*") if eligible(p) and p.suffix in {".js", ".mjs", ".cjs"}]
    failures = []
    for path in files:
        result = subprocess.run(["node", "--check", str(path)], text=True, capture_output=True)
        if result.returncode:
            failures.append(f"{path.relative_to(ROOT)}: {result.stderr.strip()}")
    if failures:
        fail("JavaScript syntax:\n" + "\n".join(failures[:40]))
    print(f"PASS JavaScript syntax — {len(files)} files")


def curriculum_fences() -> None:
    python_count = 0; failures: list[str] = []
    for page in learner_pages():
        for index, match in enumerate(re.finditer(r"```([^\n`]*)\n(.*?)```", read(page), re.S), 1):
            language = match.group(1).strip().split()[0].lower() if match.group(1).strip() else ""
            if language in {"python", "py"}:
                python_count += 1
                try:
                    ast.parse(match.group(2), filename=f"{page}#fence-{index}")
                except SyntaxError as exc:
                    failures.append(f"{page.relative_to(ROOT)} fence {index}: {exc.msg}")
    if failures:
        fail("Python curriculum fences:\n" + "\n".join(failures[:50]))
    ts_lib = subprocess.run(["node", "-e", "console.log(require.resolve('typescript'))"], text=True, capture_output=True)
    ts_count = "not-executed"
    if ts_lib.returncode == 0:
        env = dict(**__import__('os').environ, TYPESCRIPT_LIB=ts_lib.stdout.strip())
        result = subprocess.run(["node", str(ROOT/"scripts/check_code_fences.mjs"), str(ROOT)], env=env, text=True, capture_output=True)
        if result.returncode:
            fail("TypeScript/JavaScript curriculum fences:\n" + result.stderr[:4000])
        try: ts_count = json.loads(result.stdout)["fences"]
        except Exception: ts_count = result.stdout.strip()
    print(f"PASS curriculum code fences — Python {python_count}, TypeScript/JavaScript {ts_count}")


class UniqueKeyLoader:
    pass


def data_proof() -> None:
    import yaml
    class Loader(yaml.SafeLoader):
        pass
    def construct_mapping(loader: Loader, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"duplicate key {key!r}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping
    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    counts = Counter(); failures: list[str] = []
    for path in payload_files():
        try:
            if path.suffix == ".json": json.loads(read(path)); counts["JSON"] += 1
            elif path.suffix in {".yaml", ".yml"}: list(yaml.load_all(read(path), Loader=Loader)); counts["YAML"] += 1
            elif path.suffix == ".toml": tomllib.loads(read(path)); counts["TOML"] += 1
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if failures:
        fail("structured data:\n" + "\n".join(failures[:100]))
    print(f"PASS structured data — JSON {counts['JSON']}, YAML {counts['YAML']}, TOML {counts['TOML']}")


def hygiene() -> None:
    bad: list[str] = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if path.is_symlink(): bad.append(f"symbolic link {rel}")
        if path.name == ".DS_Store" or "__MACOSX" in rel.parts: bad.append(str(rel))
        if path.name in {"__pycache__", ".pytest_cache", ".runtime", "node_modules", "site"}: bad.append(str(rel))
        if path.suffix in {".pyc", ".pyo"}: bad.append(str(rel))
    if bad:
        fail("repository hygiene:\n" + "\n".join(bad[:80]))
    print("PASS repository hygiene")


def run_course_proofs() -> None:
    make = shutil.which("gmake") or shutil.which("make") or "make"
    for course in course_dirs():
        print(f"\n=== {course.name}: core-proof ===")
        subprocess.run([make, "core-proof"], cwd=course, check=True)
    print("PASS all ten course-local core proofs")


def release_proof() -> None:
    structure(); nav_proof(); handoff_proof(); links(); quality(); python_syntax(); javascript_syntax(); curriculum_fences(); data_proof(); hygiene()
    print("PASS API Engineering ten-course release proof")


def core_proof() -> None:
    release_proof(); run_course_proofs(); print("PASS API Engineering ten-course core proof")


def manifest_create() -> None:
    rows = [{"path": p.relative_to(ROOT).as_posix(), "size": p.stat().st_size, "sha256": sha256(p)} for p in payload_files()]
    payload = {"format": "bijux-program-manifest-v2", "root": "programs/api-engineering", "file_count": len(rows), "files": rows}
    path = ROOT / "MANIFEST.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / "MANIFEST.sha256").write_text(f"{sha256(path)}  MANIFEST.json\n", encoding="utf-8")
    print(f"PASS manifest created — {len(rows)} payload files")


def manifest_proof() -> None:
    mp = ROOT / "MANIFEST.json"; dp = ROOT / "MANIFEST.sha256"
    if not mp.is_file() or not dp.is_file(): fail("missing program manifest")
    if sha256(mp) != dp.read_text().split()[0]: fail("program manifest digest mismatch")
    data = json.loads(read(mp)); declared = {row["path"]: row for row in data["files"]}
    actual = {p.relative_to(ROOT).as_posix(): p for p in payload_files()}
    if set(declared) != set(actual):
        fail(f"program manifest inventory mismatch missing={sorted(set(declared)-set(actual))[:10]} unlisted={sorted(set(actual)-set(declared))[:10]}")
    for rel, row in declared.items():
        path = actual[rel]
        if path.stat().st_size != row["size"] or sha256(path) != row["sha256"]:
            fail(f"program manifest mismatch: {rel}")
    if data.get("file_count") != len(declared): fail("program manifest file_count mismatch")
    print(f"PASS program manifest — {len(declared)} exact files")


def inventory() -> None:
    md = learner_pages(); modules = sum(len(numbered_modules(c)) for c in course_dirs())
    payload = payload_files()
    print(json.dumps({
        "courses": len(COURSES), "numbered_modules": modules,
        "program_book_pages": len(list((ROOT/'program-book').glob('*.md'))),
        "course_book_pages": len(md)-len(list((ROOT/'program-book').glob('*.md'))),
        "learner_words": sum(words(read(p)) for p in md),
        "payload_files": len(payload), "markdown_files": len([p for p in payload if p.suffix=='.md']),
        "python_files": len([p for p in payload if p.suffix=='.py']),
        "typescript_files": len([p for p in payload if p.suffix=='.ts']),
    }, indent=2, sort_keys=True))


COMMANDS = {
    "structure": structure, "nav-proof": nav_proof, "handoff-proof": handoff_proof,
    "links": links, "quality": quality, "python-syntax": python_syntax,
    "javascript-syntax": javascript_syntax, "curriculum-fences": curriculum_fences,
    "data-proof": data_proof, "hygiene": hygiene, "course-proofs": run_course_proofs,
    "release-proof": release_proof, "core-proof": core_proof,
    "manifest": manifest_create, "manifest-create": manifest_create,
    "manifest-proof": manifest_proof, "inventory": inventory,
}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args(); COMMANDS[args.command]()

if __name__ == "__main__":
    main()
