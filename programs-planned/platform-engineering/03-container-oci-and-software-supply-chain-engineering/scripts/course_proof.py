#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

import yaml

COURSE = Path(__file__).resolve().parents[1]
BOOK = COURSE / "course-book"
WORKLOAD = COURSE / "capstone" / "workload"
EXPECTED_MODULES = [
    "module-01-containers-as-linux-process-isolation",
    "module-02-oci-runtime-bundles-lifecycle-and-rootless-execution",
    "module-03-oci-images-layers-content-addressability-and-whiteouts",
    "module-04-build-graphs-cache-reproducibility-and-secret-hygiene",
    "module-05-multi-platform-images-abi-and-architecture-truth",
    "module-06-registries-distribution-digests-tags-and-referrers",
    "module-07-runtime-hardening-resource-control-and-operational-contracts",
    "module-08-sboms-vulnerabilities-licenses-and-vex",
    "module-09-provenance-signatures-attestations-and-verification-policy",
    "module-10-release-promotion-revocation-and-kubernetes-handoff",
]


def clean_generated() -> None:
    for cache in [*COURSE.rglob("__pycache__"), *COURSE.rglob(".pytest_cache")]:
        if cache.is_dir():
            shutil.rmtree(cache)
    for generated in (COURSE / "site", COURSE / "capstone" / "registry" / "local-store"):
        if generated.is_dir():
            shutil.rmtree(generated)


def run(
    label: str,
    *command: str,
    cwd: Path = COURSE,
    env: dict[str, str] | None = None,
) -> None:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, check=False)
    if result.returncode:
        raise SystemExit(f"FAIL {label}: {' '.join(command)}")
    print(f"PASS {label}")


def section_bodies(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, line[3:].strip())
        for index, line in enumerate(lines)
        if line.startswith("## ")
    ]
    sections: dict[str, str] = {}
    for position, (start, title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        sections[title] = "\n".join(lines[start + 1 : end]).strip()
    return sections


def flatten_nav(value: object) -> list[str]:
    paths: list[str] = []
    if isinstance(value, str) and value.endswith(".md"):
        paths.append(value)
    elif isinstance(value, list):
        for item in value:
            paths.extend(flatten_nav(item))
    elif isinstance(value, dict):
        for item in value.values():
            paths.extend(flatten_nav(item))
    return paths


def unique_json(path: Path) -> object:
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs_hook)


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def unique_yaml_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    result: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    unique_yaml_mapping,
)


clean_generated()

metadata = unique_json(COURSE / "course.json")
if not isinstance(metadata, dict):
    raise SystemExit("course.json must contain an object")
if metadata.get("courseNumber") != 3:
    raise SystemExit("course number must be 3")
if metadata.get("primaryProduct") != "course-book":
    raise SystemExit("course book must be the declared primary product")
if metadata.get("capstone") != "Atlas Workload Release 1.0":
    raise SystemExit("unexpected capstone identity")
print("PASS course metadata and capstone identity")

orientation = BOOK / "module-00-orientation"
for filename in ("index.md", "lab.md", "checkpoint.md"):
    if not (orientation / filename).is_file():
        raise SystemExit(f"orientation missing {filename}")

numbered = sorted(
    path.name
    for path in BOOK.glob("module-[0-9][0-9]-*")
    if path.name != "module-00-orientation"
)
if numbered != sorted(EXPECTED_MODULES):
    raise SystemExit(f"unexpected numbered module set: {numbered}")

question_total = 0
answer_total = 0
for module_name in EXPECTED_MODULES:
    module = BOOK / module_name
    for filename in (
        "index.md",
        "exercises.md",
        "exercise-answers.md",
        "lab.md",
        "checkpoint.md",
    ):
        if not (module / filename).is_file():
            raise SystemExit(f"missing {module_name}/{filename}")

    chapter_words = len((module / "index.md").read_text(encoding="utf-8").split())
    if chapter_words < 2_000:
        raise SystemExit(f"chapter too thin ({chapter_words} words): {module_name}")

    questions = section_bodies(module / "exercises.md")
    answers = section_bodies(module / "exercise-answers.md")
    question_titles = [title for title in questions if re.match(r"^\d+\. ", title)]
    answer_titles = [title for title in answers if re.match(r"^\d+\. ", title)]
    expected_titles = [
        title
        for index in range(1, 13)
        for title in question_titles
        if title.startswith(f"{index}. ")
    ]
    if question_titles != expected_titles or len(question_titles) != 12:
        raise SystemExit(f"exercise numbering mismatch: {module_name}")
    if answer_titles != question_titles:
        raise SystemExit(f"exercise/answer heading mismatch: {module_name}")
    for title in answer_titles:
        words = len(answers[title].split())
        if words < 30:
            raise SystemExit(
                f"worked answer too shallow ({words} words): {module_name} / {title}"
            )

    question_total += len(question_titles)
    answer_total += len(answer_titles)

    lab = (module / "lab.md").read_text(encoding="utf-8")
    for heading in (
        "## Goal",
        "## Safety boundary",
        "## Baseline",
        "## Hypothesis",
        "## Controlled action",
        "## Oracle",
        "## Evidence",
        "## Interpretation",
        "## Cleanup",
        "## Completion gate",
    ):
        if heading not in lab:
            raise SystemExit(f"{module_name} laboratory missing {heading}")

    checkpoint = (module / "checkpoint.md").read_text(encoding="utf-8")
    for heading in (
        "## Required evidence",
        "## Decision defense",
        "## Progression gate",
    ):
        if heading not in checkpoint:
            raise SystemExit(f"{module_name} checkpoint missing {heading}")

print(
    "PASS ten reader-first modules — "
    f"{question_total} exercises / {answer_total} worked answers"
)

mkdocs = yaml.load(
    (COURSE / "mkdocs.yml").read_text(encoding="utf-8"),
    Loader=UniqueKeyLoader,
)
if not isinstance(mkdocs, dict):
    raise SystemExit("mkdocs.yml must contain an object")
nav_paths = flatten_nav(mkdocs.get("nav"))
book_pages = sorted(path.relative_to(BOOK).as_posix() for path in BOOK.rglob("*.md"))
if len(nav_paths) != len(set(nav_paths)):
    raise SystemExit("MkDocs navigation contains duplicate page paths")
if sorted(nav_paths) != book_pages:
    missing = sorted(set(book_pages) - set(nav_paths))
    extra = sorted(set(nav_paths) - set(book_pages))
    raise SystemExit(
        f"MkDocs navigation mismatch: missing={missing[:10]} extra={extra[:10]}"
    )
print(f"PASS exact course-book navigation — {len(book_pages)} pages")

json_count = yaml_count = toml_count = python_count = 0
for path in COURSE.rglob("*.json"):
    if any(part in {"__pycache__", ".pytest_cache", "local-store"} for part in path.parts):
        continue
    unique_json(path)
    json_count += 1
for path in [*COURSE.rglob("*.yaml"), *COURSE.rglob("*.yml")]:
    if any(part in {"__pycache__", ".pytest_cache", "local-store"} for part in path.parts):
        continue
    yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    yaml_count += 1
for path in COURSE.rglob("*.toml"):
    tomllib.loads(path.read_text(encoding="utf-8"))
    toml_count += 1
for path in COURSE.rglob("*.py"):
    if "__pycache__" in path.parts:
        continue
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    python_count += 1
print(
    "PASS structured data and Python syntax — "
    f"JSON {json_count}, YAML {yaml_count}, TOML {toml_count}, Python {python_count}"
)

for shell in sorted(COURSE.rglob("*.sh")):
    run(f"shell syntax {shell.relative_to(COURSE)}", "sh", "-n", str(shell))

gofmt = subprocess.run(
    ["gofmt", "-d", "."],
    cwd=WORKLOAD,
    text=True,
    capture_output=True,
    check=False,
)
if gofmt.returncode or gofmt.stdout.strip():
    raise SystemExit("Go source is not gofmt-clean:\n" + gofmt.stdout[:2_000])
run(
    "Go workload compilation",
    "go",
    "test",
    "./...",
    cwd=WORKLOAD,
    env={**os.environ, "GOTOOLCHAIN": "local", "GOWORK": "off"},
)

forbidden_markers = (
    "TODO",
    "TBD",
    "lorem ipsum",
    "as an AI",
    "insert content here",
    "write content here",
)
for page in BOOK.rglob("*.md"):
    text = page.read_text(encoding="utf-8")
    lowered = text.lower()
    for marker in forbidden_markers:
        if marker.lower() in lowered:
            raise SystemExit(f"unfinished marker {marker!r}: {page}")

paragraph_locations: dict[str, set[str]] = defaultdict(set)
for page in BOOK.rglob("*.md"):
    if page.name in {"exercises.md", "exercise-answers.md"}:
        continue
    for paragraph in re.split(r"\n\s*\n", page.read_text(encoding="utf-8")):
        normalized = " ".join(paragraph.split()).lower()
        if len(normalized.split()) >= 35 and not normalized.startswith("```"):
            paragraph_locations[normalized].add(page.relative_to(BOOK).as_posix())
repeated = {
    text: locations
    for text, locations in paragraph_locations.items()
    if len(locations) > 1
}
if repeated:
    text, locations = next(iter(repeated.items()))
    raise SystemExit(
        f"repeated long explanatory paragraph in {sorted(locations)}: {text[:180]}"
    )
print("PASS reader-first completion, depth, and non-repetition guards")

run("handoff integrity", sys.executable, "scripts/verify_handoff.py")
run("reader links", sys.executable, "scripts/check_links.py")
run("planted-defect declarations", sys.executable, "scripts/verify_defects.py")
run("release decision corpus", sys.executable, "scripts/verify_releases.py")

proof_env = {
    **os.environ,
    "PYTHONPATH": "capstone",
    "PYTHONDONTWRITEBYTECODE": "1",
}
run(
    "course and capstone tests",
    sys.executable,
    "-m",
    "pytest",
    "-q",
    "-p",
    "no:cacheprovider",
    "capstone/tests",
    "tests",
    env=proof_env,
)
run(
    "checked capstone release",
    sys.executable,
    "capstone/scripts/generate_checked_release.py",
    env=proof_env,
)
run(
    "handoff integrity after release generation",
    sys.executable,
    "scripts/verify_handoff.py",
)
run(
    "release corpus after generation",
    sys.executable,
    "scripts/verify_releases.py",
)

clean_generated()
for forbidden_dir in ("__pycache__", ".pytest_cache", "site", "local-store"):
    if any(path.is_dir() for path in COURSE.rglob(forbidden_dir)):
        raise SystemExit(f"generated directory remains: {forbidden_dir}")
fixture_key = COURSE / "capstone" / "security" / "atlas-course-signing-private.pem"
if fixture_key.exists() and fixture_key.stat().st_mode & 0o077:
    raise SystemExit("fixture private-key mode must be 0600")
print("PASS repository hygiene and fixture-key mode")
print("PASS Course 3 complete core proof")
