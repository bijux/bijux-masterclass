#!/usr/bin/env python3
"""Program-wide proofs for the six-course API Engineering curriculum."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tomllib
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
COURSES = [
    "01-openapi-contract-engineering",
    "02-contract-driven-api-service-engineering",
    "03-api-security-engineering",
    "04-api-reliability-and-observability-engineering",
    "05-api-performance-capacity-and-traffic-engineering",
    "06-event-driven-api-engineering",
]
PROGRAM_BOOK_FILES = {
    "index.md",
    "start-here.md",
    "six-course-journey.md",
    "analysis-runs-platform.md",
    "version-and-handoff-ledger.md",
    "language-and-code-strategy.md",
    "evidence-model.md",
    "study-and-assessment.md",
    "final-program-defense.md",
    "glossary.md",
}
COURSE_BOOK_ROOT_FILES = {
    "index.md",
    "start-here.md",
    "study-plan.md",
    "capstone.md",
    "standards.md",
    "glossary.md",
}
MODULE_FILES = {
    "index.md",
    "exercises.md",
    "exercise-answers.md",
    "lab.md",
    "checkpoint.md",
}
ORIENTATION_FILES = {"index.md", "lab.md", "checkpoint.md"}
LAB_HEADINGS = {
    "## Objective",
    "## Setup conditions",
    "## Failure action and investigation",
    "## Operational oracle",
    "## Required evidence",
    "## Cleanup and reset",
    "## Completion gate",
}
CHECKPOINT_HEADINGS = {
    "## Required result",
    "## Demonstrate",
    "## Commands",
    "## Defend the design",
    "## Continue only when",
}
MODULE_FRONT_MARKERS = {
    "**Program stage:**",
    "**Central question:**",
    "## Where this module fits",
    "## Learning outcomes",
    "## Capstone result",
    "## Module synthesis",
    "## Next in the story",
}
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "node_modules",
    "site",
    "__pycache__",
    ".pytest_cache",
    ".runtime",
    "dist-core",
}
ROOT_MANIFEST_FILES = {ROOT / "MANIFEST.json", ROOT / "MANIFEST.sha256"}
HANDOFF_PAIRS = [
    (
        "Course 1 → Course 2",
        ROOT / COURSES[0] / "capstone" / "handoff",
        ROOT / COURSES[1] / "predecessor",
    ),
    (
        "Course 2 → Course 3",
        ROOT / COURSES[1] / "capstone" / "handoff",
        ROOT / COURSES[2] / "capstone" / "predecessor",
    ),
    (
        "Course 3 → Course 4",
        ROOT / COURSES[2] / "capstone" / "handoff",
        ROOT / COURSES[3] / "capstone" / "predecessor" / "handoff",
    ),
    (
        "Course 4 → Course 5",
        ROOT / COURSES[3] / "capstone" / "handoff",
        ROOT / COURSES[4] / "capstone" / "predecessor" / "handoff",
    ),
    (
        "Course 5 → Course 6",
        ROOT / COURSES[4] / "capstone" / "handoff",
        ROOT / COURSES[5] / "capstone" / "predecessor" / "handoff",
    ),
]


def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def numbered_headings(path: Path) -> list[str]:
    return [
        match.group(2).strip()
        for match in re.finditer(r"(?m)^##\s+(\d+)\.\s+(.+?)\s*$", read(path))
    ]


def learner_pages() -> Iterable[Path]:
    yield from sorted((ROOT / "program-book").glob("*.md"))
    for course in COURSES:
        yield from sorted((ROOT / course / "course-book").rglob("*.md"))


def payload_files() -> list[Path]:
    rows: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            fail(f"symbolic link is not allowed in the release payload: {path.relative_to(ROOT)}")
        if not path.is_file() or path in ROOT_MANIFEST_FILES:
            continue
        if any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            continue
        rows.append(path)
    return rows


def _module_dirs(book: Path) -> tuple[Path, list[Path]]:
    modules = sorted(book.glob("module-[0-9][0-9]-*"))
    orientation = [p for p in modules if p.name.startswith("module-00-")]
    numbered = [p for p in modules if not p.name.startswith("module-00-")]
    if len(orientation) != 1:
        fail(f"{book.relative_to(ROOT)} must contain exactly one orientation module")
    return orientation[0], numbered


def structure() -> None:
    failures: list[str] = []
    program_book = ROOT / "program-book"
    if not program_book.is_dir():
        failures.append("missing program-book directory")
    else:
        actual = {p.name for p in program_book.glob("*.md")}
        if actual != PROGRAM_BOOK_FILES:
            failures.append(
                "program-book files differ: "
                f"missing={sorted(PROGRAM_BOOK_FILES - actual)} "
                f"extra={sorted(actual - PROGRAM_BOOK_FILES)}"
            )

    for course_name in COURSES:
        course = ROOT / course_name
        if not course.is_dir():
            failures.append(f"missing course {course_name}")
            continue
        for required in ("README.md", "Makefile", "mkdocs.yml", "course.json"):
            if not (course / required).is_file():
                failures.append(f"missing {course_name}/{required}")

        book = course / "course-book"
        if not book.is_dir():
            failures.append(f"missing {course_name}/course-book")
            continue
        root_files = {p.name for p in book.glob("*.md")}
        if root_files != COURSE_BOOK_ROOT_FILES:
            failures.append(
                f"{course_name} course-book root differs: "
                f"missing={sorted(COURSE_BOOK_ROOT_FILES - root_files)} "
                f"extra={sorted(root_files - COURSE_BOOK_ROOT_FILES)}"
            )
        pages = list(book.rglob("*.md"))
        if len(pages) != 59:
            failures.append(f"{course_name} has {len(pages)} course-book pages; expected 59")

        modules = sorted(book.glob("module-[0-9][0-9]-*"))
        if len(modules) != 11:
            failures.append(f"{course_name} has {len(modules)} module directories; expected 11")
            continue
        orientation = [m for m in modules if m.name.startswith("module-00-")]
        numbered = [m for m in modules if not m.name.startswith("module-00-")]
        if len(orientation) != 1:
            failures.append(f"{course_name} must have one orientation module")
        else:
            files = {p.name for p in orientation[0].glob("*.md")}
            if files != ORIENTATION_FILES:
                failures.append(
                    f"{orientation[0].relative_to(ROOT)} files differ: "
                    f"missing={sorted(ORIENTATION_FILES-files)} "
                    f"extra={sorted(files-ORIENTATION_FILES)}"
                )
        if len(numbered) != 10:
            failures.append(f"{course_name} has {len(numbered)} numbered modules; expected 10")

        for module in numbered:
            files = {p.name for p in module.glob("*.md")}
            if files != MODULE_FILES:
                failures.append(
                    f"{module.relative_to(ROOT)} files differ: "
                    f"missing={sorted(MODULE_FILES-files)} extra={sorted(files-MODULE_FILES)}"
                )
                continue
            questions = numbered_headings(module / "exercises.md")
            answers = numbered_headings(module / "exercise-answers.md")
            if len(questions) != 12 or len(answers) != 12:
                failures.append(
                    f"{module.relative_to(ROOT)} exercises/answers are "
                    f"{len(questions)}/{len(answers)}; expected 12/12"
                )
            elif questions != answers:
                failures.append(f"{module.relative_to(ROOT)} answer headings do not match exercises")

            lab_headings = {
                line.strip() for line in read(module / "lab.md").splitlines()
                if line.startswith("## ")
            }
            if LAB_HEADINGS - lab_headings:
                failures.append(
                    f"{(module/'lab.md').relative_to(ROOT)} missing "
                    f"{sorted(LAB_HEADINGS-lab_headings)}"
                )
            checkpoint_headings = {
                line.strip() for line in read(module / "checkpoint.md").splitlines()
                if line.startswith("## ")
            }
            if CHECKPOINT_HEADINGS - checkpoint_headings:
                failures.append(
                    f"{(module/'checkpoint.md').relative_to(ROOT)} missing "
                    f"{sorted(CHECKPOINT_HEADINGS-checkpoint_headings)}"
                )
            chapter = read(module / "index.md")
            missing_markers = [m for m in MODULE_FRONT_MARKERS if m not in chapter]
            if missing_markers:
                failures.append(
                    f"{(module/'index.md').relative_to(ROOT)} missing learner markers "
                    f"{missing_markers}"
                )

    if failures:
        fail("program structure:\n" + "\n".join(failures[:160]))
    print(
        "PASS program structure — six courses, sixty numbered modules, "
        "354 course-book pages, 10 program-book pages"
    )


def _flatten_nav(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        if value.endswith(".md"):
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from _flatten_nav(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _flatten_nav(item)


def nav_proof() -> None:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:
        fail(f"PyYAML is required for nav-proof: {exc}")
    config = yaml.safe_load(read(ROOT / "mkdocs.yml"))
    listed = list(_flatten_nav(config.get("nav", [])))
    expected = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in learner_pages()
    }
    listed_set = set(listed)
    duplicates = sorted({item for item in listed if listed.count(item) > 1})
    missing = sorted(expected - listed_set)
    extra = sorted(listed_set - expected)
    absent = sorted(item for item in listed_set if not (ROOT / item).is_file())
    if duplicates or missing or extra or absent:
        fail(
            "MkDocs navigation coverage:\n"
            f"duplicates={duplicates[:20]}\n"
            f"missing={missing[:40]}\n"
            f"extra={extra[:40]}\n"
            f"absent={absent[:40]}"
        )
    if len(listed) != 364:
        fail(f"MkDocs nav contains {len(listed)} pages; expected 364")
    print("PASS combined MkDocs navigation — 364 learner-facing pages, no duplicates")


def _directory_snapshot(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        fail(f"handoff directory is missing: {directory.relative_to(ROOT)}")
    result: dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            fail(f"handoff contains a symlink: {path.relative_to(ROOT)}")
        if path.is_file():
            relative = path.relative_to(directory).as_posix()
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def handoff_proof() -> None:
    counts: list[str] = []
    for label, source, destination in HANDOFF_PAIRS:
        left = _directory_snapshot(source)
        right = _directory_snapshot(destination)
        if left != right:
            missing = sorted(set(left) - set(right))
            extra = sorted(set(right) - set(left))
            changed = sorted(k for k in set(left) & set(right) if left[k] != right[k])
            fail(
                f"{label} handoff differs:\n"
                f"missing={missing[:20]}\nextra={extra[:20]}\nchanged={changed[:20]}"
            )
        counts.append(f"{label}: {len(left)} files")
    print("PASS adjacent-course handoffs — " + "; ".join(counts))


def links() -> None:
    pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
    broken: list[str] = []
    escaping: list[str] = []
    checked = 0
    for path in learner_pages():
        for target in pattern.findall(read(path)):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            checked += 1
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                escaping.append(f"{path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    if broken or escaping:
        fail(
            "learner-facing Markdown links:\n"
            + ("broken:\n" + "\n".join(broken[:80]) + "\n" if broken else "")
            + ("escaping:\n" + "\n".join(escaping[:80]) if escaping else "")
        )
    print(f"PASS learner-facing Markdown links — {checked} local targets")


def _check_answer_sections(path: Path, failures: list[str]) -> None:
    text = read(path)
    matches = list(re.finditer(r"(?m)^##\s+(\d+)\.\s+(.+?)\s*$", text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if words(text[start:end]) < 8:
            failures.append(
                f"{path.relative_to(ROOT)} answer {match.group(1)} lacks a reasoned explanation"
            )


def quality() -> None:
    failures: list[str] = []
    stale_patterns = [
        r"\bof 4\b",
        r"\bfour-course\b",
        r"\bfour courses\b",
        r"\bforty modules\b",
        r"API Engineering is a two-course program",
        r"standards-and-evidence\.md",
        r"(?im)^\s*(?:TODO|TBD|FIXME)\b",
        r"(?i)\[(?:PLACEHOLDER|TODO|TBD)\]",
    ]
    forbidden_phrases = {
        "This chapter is the authoritative explanation",
        "State the decision, show one counterexample",
        "A complete answer names the exact source file",
        "The repair must make this oracle pass again",
        "Before reading the repair",
    }
    orphan_pattern = re.compile(
        r"(?m)^(?:Identify|Interrogate the excerpt|Decide|Reason|Explain|Compare|Trace|"
        r"Predict|Observe|Repair|Verify):\s*$"
    )
    paragraphs: defaultdict[str, list[Path]] = defaultdict(list)

    for path in learner_pages():
        text = read(path)
        if not re.search(r"(?m)^#\s+\S", text):
            failures.append(f"{path.relative_to(ROOT)} has no level-one title")
        for pattern in stale_patterns:
            if re.search(pattern, text, re.I):
                failures.append(f"{path.relative_to(ROOT)} contains stale marker {pattern!r}")
        for phrase in forbidden_phrases:
            if phrase in text:
                failures.append(f"{path.relative_to(ROOT)} contains template prose {phrase!r}")
        if orphan_pattern.search(text):
            failures.append(f"{path.relative_to(ROOT)} contains an orphan prompt")
        submission = re.search(
            r"(?ms)^## Submission format\s*$\n(.*?)(?=^##\s|\Z)", text
        )
        if submission is not None and words(submission.group(1)) < 8:
            failures.append(f"{path.relative_to(ROOT)} has an empty submission format")

        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for paragraph in re.split(r"\n\s*\n", prose):
            normalized = " ".join(paragraph.split())
            if words(normalized) >= 70:
                paragraphs[normalized].append(path)

    for course_name in COURSES:
        book = ROOT / course_name / "course-book"
        orientation, numbered = _module_dirs(book)
        if words(read(orientation / "index.md")) < 450:
            failures.append(f"{(orientation/'index.md').relative_to(ROOT)} is too thin")
        for module in numbered:
            chapter_words = words(read(module / "index.md"))
            if chapter_words < 1800:
                failures.append(
                    f"{(module/'index.md').relative_to(ROOT)} has {chapter_words} words; minimum 1800"
                )
            lab_words = words(read(module / "lab.md"))
            if lab_words < 300:
                failures.append(
                    f"{(module/'lab.md').relative_to(ROOT)} has {lab_words} words; minimum 300"
                )
            checkpoint_words = words(read(module / "checkpoint.md"))
            if checkpoint_words < 150:
                failures.append(
                    f"{(module/'checkpoint.md').relative_to(ROOT)} has {checkpoint_words} words; minimum 150"
                )
            _check_answer_sections(module / "exercise-answers.md", failures)

    for paragraph, paths in paragraphs.items():
        unique = sorted(set(paths))
        if len(unique) >= 3:
            failures.append(
                f"long learner paragraph repeated in {len(unique)} files: {paragraph[:180]!r}"
            )

    if failures:
        fail("learner-first quality guard:\n" + "\n".join(failures[:180]))
    print(
        "PASS learner-first quality guard — sixty substantive chapters, "
        "480 matched exercises and answers, 60 labs, 60 checkpoints"
    )


def python_syntax() -> None:
    files = [
        path for path in ROOT.rglob("*.py")
        if not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    ]
    failures: list[str] = []
    for path in files:
        try:
            compile(path.read_bytes(), str(path), "exec")
        except SyntaxError as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if failures:
        fail("Python syntax:\n" + "\n".join(failures[:60]))
    print(f"PASS Python syntax — {len(files)} files")


def javascript_syntax() -> None:
    files = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in {".js", ".mjs", ".cjs"}
        and not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    ]
    failures: list[str] = []
    node = shutil.which("node")
    if not node:
        fail("Node.js is required for JavaScript syntax proof")
    for path in files:
        result = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
        if result.returncode:
            failures.append(f"{path.relative_to(ROOT)}:\n{result.stderr}")
    if failures:
        fail("JavaScript syntax:\n" + "\n".join(failures[:30]))
    print(f"PASS JavaScript syntax — {len(files)} files")


class DuplicateKeyError(ValueError):
    pass


def _json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def data_proof() -> None:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:
        fail(f"PyYAML is required for data-proof: {exc}")

    class UniqueLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: Any, node: Any, deep: bool = False) -> Any:
        loader.flatten_mapping(node)
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise DuplicateKeyError(f"duplicate YAML key {key!r}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    counts = {"json": 0, "yaml": 0, "toml": 0}
    failures: list[str] = []
    for path in payload_files():
        try:
            if path.suffix == ".json":
                json.loads(read(path), object_pairs_hook=_json_pairs)
                counts["json"] += 1
            elif path.suffix in {".yaml", ".yml"}:
                list(yaml.load_all(read(path), Loader=UniqueLoader))
                counts["yaml"] += 1
            elif path.suffix == ".toml":
                tomllib.loads(read(path))
                counts["toml"] += 1
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if failures:
        fail("structured data:\n" + "\n".join(failures[:120]))
    print(
        f"PASS structured data — {counts['json']} JSON, "
        f"{counts['yaml']} YAML, {counts['toml']} TOML files"
    )


def course_proofs() -> None:
    make = shutil.which("gmake") or shutil.which("make") or "make"
    for directory in COURSES:
        print(f"RUN {directory}", flush=True)
        result = subprocess.run([make, "-C", str(ROOT / directory), "core-proof"])
        if result.returncode:
            fail(f"course proof failed: {directory}")
    print("PASS all six course-local proofs")


def manifest() -> None:
    rows = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
        for path in payload_files()
    ]
    payload = {
        "format": 2,
        "program": "api-engineering",
        "courses": COURSES,
        "files": rows,
    }
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (ROOT / "MANIFEST.json").write_bytes(data)
    (ROOT / "MANIFEST.sha256").write_text(
        hashlib.sha256(data).hexdigest() + "  MANIFEST.json\n", encoding="utf-8"
    )
    print(f"PASS program manifest created — {len(rows)} payload files")


def manifest_proof() -> None:
    manifest_path = ROOT / "MANIFEST.json"
    checksum_path = ROOT / "MANIFEST.sha256"
    if not manifest_path.is_file() or not checksum_path.is_file():
        fail("program manifest pair is missing")
    expected_digest = checksum_path.read_text(encoding="utf-8").split()[0]
    actual_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if actual_digest != expected_digest:
        fail("MANIFEST.json digest does not match MANIFEST.sha256")
    payload = json.loads(read(manifest_path), object_pairs_hook=_json_pairs)
    expected = {row["path"]: row for row in payload["files"]}
    actual = {path.relative_to(ROOT).as_posix(): path for path in payload_files()}
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed: list[str] = []
    for relative, row in expected.items():
        path = actual.get(relative)
        if path is None:
            continue
        if path.stat().st_size != row["bytes"]:
            changed.append(relative + " (size)")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            changed.append(relative + " (sha256)")
    if missing or extra or changed:
        fail(
            "program manifest verification:\n"
            f"missing={missing[:50]}\nextra={extra[:50]}\nchanged={changed[:50]}"
        )
    print(f"PASS program manifest verification — {len(expected)} exact payload files")


def inventory() -> None:
    markdown = list(learner_pages())
    payload = payload_files()
    data = {
        "courses": len(COURSES),
        "numberedModules": 60,
        "programBookPages": len(list((ROOT / "program-book").glob("*.md"))),
        "courseBookPages": sum(len(list((ROOT / c / "course-book").rglob("*.md"))) for c in COURSES),
        "learnerFacingWords": sum(words(read(p)) for p in markdown),
        "payloadFiles": len(payload),
        "pythonFiles": sum(p.suffix == ".py" for p in payload),
        "typescriptFiles": sum(p.suffix == ".ts" for p in payload),
        "javascriptFiles": sum(p.suffix in {".js", ".mjs", ".cjs"} for p in payload),
    }
    print(json.dumps(data, indent=2, sort_keys=True))


def release_proof() -> None:
    structure()
    nav_proof()
    handoff_proof()
    links()
    quality()
    python_syntax()
    javascript_syntax()
    data_proof()
    print("PASS API Engineering six-course release proof")


def core() -> None:
    release_proof()
    course_proofs()
    print("PASS API Engineering six-course core proof")


COMMANDS = {
    "core-proof": core,
    "release-proof": release_proof,
    "structure": structure,
    "nav-proof": nav_proof,
    "handoff-proof": handoff_proof,
    "links": links,
    "quality": quality,
    "python-syntax": python_syntax,
    "javascript-syntax": javascript_syntax,
    "data-proof": data_proof,
    "course-proofs": course_proofs,
    "manifest": manifest,
    "manifest-proof": manifest_proof,
    "inventory": inventory,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=sorted(COMMANDS))
    args = parser.parse_args()
    COMMANDS[args.command]()


if __name__ == "__main__":
    main()
