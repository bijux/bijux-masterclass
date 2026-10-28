from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

COURSE = Path(__file__).resolve().parents[2]
CAP = COURSE / "capstone"
BOOK = COURSE / "course-book"


def run(cmd: list[str], *, cwd: Path = COURSE) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def check_structure() -> None:
    required = ["index.md", "start-here.md", "study-plan.md", "capstone.md", "standards.md", "evidence-model.md", "language-strategy.md", "glossary.md"]
    for name in required:
        path = BOOK / name
        if not path.is_file():
            raise SystemExit(f"missing course-book/{name}")
        if len(path.read_text().split()) < 500:
            raise SystemExit(f"reader guide too shallow: course-book/{name}")

    modules = sorted(BOOK.glob("module-[0-9][0-9]-*"))
    if len(modules) != 11:
        raise SystemExit(f"expected orientation plus ten modules, found {len(modules)}")
    orientation = [p for p in modules if "module-00-" in p.name][0]
    for name in ["index.md", "lab.md", "checkpoint.md"]:
        if not (orientation / name).is_file():
            raise SystemExit(f"missing {orientation.name}/{name}")

    numbered = [p for p in modules if "module-00-" not in p.name]
    for path in numbered:
        for name in ["index.md", "exercises.md", "exercise-answers.md", "lab.md", "checkpoint.md"]:
            if not (path / name).is_file():
                raise SystemExit(f"missing {path.name}/{name}")
        questions = re.findall(r"^## Exercise (\d+) — (.+)$", (path / "exercises.md").read_text(), re.M)
        answers = re.findall(r"^## Exercise (\d+) — (.+)$", (path / "exercise-answers.md").read_text(), re.M)
        if len(questions) != 12 or questions != answers:
            raise SystemExit(f"exercise/answer mismatch in {path.name}")
        chapter_words = len((path / "index.md").read_text().split())
        if chapter_words < 2000:
            raise SystemExit(f"chapter too shallow: {path.name} ({chapter_words} words)")
        if len((path / "exercise-answers.md").read_text().split()) < 500:
            raise SystemExit(f"worked answers too shallow: {path.name}")
        lab = (path / "lab.md").read_text()
        for heading in ["## Goal", "## Safety boundary", "## Baseline", "## Hypothesis", "## Controlled action", "## Oracle", "## Evidence", "## Interpretation", "## Cleanup", "## Completion gate"]:
            if heading not in lab:
                raise SystemExit(f"lab missing {heading}: {path.name}")
        checkpoint = (path / "checkpoint.md").read_text()
        if "## Evidence to retain" not in checkpoint or "## Progression decision" not in checkpoint:
            raise SystemExit(f"checkpoint lacks evidence/progression decision: {path.name}")
    print(f"PASS learner structure — {len(numbered)} numbered modules")



def flatten_nav(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, str):
        if value.endswith(".md"):
            paths.append(value)
    elif isinstance(value, list):
        for item in value:
            paths.extend(flatten_nav(item))
    elif isinstance(value, dict):
        for item in value.values():
            paths.extend(flatten_nav(item))
    return paths


def check_navigation() -> None:
    config = yaml.load((COURSE / "mkdocs.yml").read_text(), Loader=UniqueKeyLoader)
    nav_paths = flatten_nav(config.get("nav", []))
    if len(nav_paths) != len(set(nav_paths)):
        raise SystemExit("MkDocs navigation contains duplicate pages")
    actual = sorted(path.relative_to(BOOK).as_posix() for path in BOOK.rglob("*.md"))
    if sorted(nav_paths) != actual:
        missing = sorted(set(actual) - set(nav_paths))
        extra = sorted(set(nav_paths) - set(actual))
        raise SystemExit(f"MkDocs coverage mismatch missing={missing[:10]} extra={extra[:10]}")
    print(f"PASS MkDocs navigation coverage — {len(actual)} pages")

def check_markdown_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    checked = 0
    for source in BOOK.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            if raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (source.parent / target).resolve()
            if not resolved.exists():
                raise SystemExit(f"broken link in {source.relative_to(COURSE)}: {raw}")
            checked += 1
    print(f"PASS Markdown links — {checked}")


def check_data() -> None:
    json_count = yaml_count = toml_count = 0
    for path in COURSE.rglob("*.json"):
        if "reports" in path.parts or path.name == "MANIFEST.json":
            continue
        json.loads(path.read_text())
        json_count += 1
    for pattern in ("*.yaml", "*.yml"):
        for path in COURSE.rglob(pattern):
            yaml.load(path.read_text(), Loader=UniqueKeyLoader)
            yaml_count += 1
    for path in COURSE.rglob("*.toml"):
        tomllib.loads(path.read_text())
        toml_count += 1
    print(f"PASS data parsing — JSON {json_count}, YAML {yaml_count}, TOML {toml_count}")


def check_python() -> None:
    count = 0
    for path in COURSE.rglob("*.py"):
        if any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        ast.parse(path.read_text(), filename=str(path))
        count += 1
    print(f"PASS Python syntax — {count} files")


def check_shell() -> None:
    count = 0
    for path in COURSE.rglob("*"):
        if not path.is_file():
            continue
        try:
            first = path.open("rb").readline().decode("utf-8")
        except UnicodeDecodeError:
            continue
        if first.startswith("#!") and ("sh" in first or "bash" in first):
            run(["bash", "-n", str(path)])
            count += 1
    print(f"PASS shell syntax — {count} files")


def check_reader_quality() -> None:
    forbidden = [r"\bTODO\b", r"\bTBD\b", r"lorem ipsum", r"insert (?:content|example) here"]
    for path in BOOK.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            if re.search(pattern, text, re.I):
                raise SystemExit(f"unfinished reader content in {path.relative_to(COURSE)}: {pattern}")
    blocks: dict[str, list[str]] = {}
    for path in BOOK.rglob("*.md"):
        for paragraph in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
            normalized = re.sub(r"\s+", " ", paragraph.strip())
            if len(normalized.split()) >= 45:
                blocks.setdefault(normalized, []).append(path.relative_to(BOOK).as_posix())
    duplicates = [(block, paths) for block, paths in blocks.items() if len(set(paths)) >= 4]
    if duplicates:
        raise SystemExit(f"repeated long learner prose across {len(set(duplicates[0][1]))} pages: {duplicates[0][1]}")
    print("PASS reader-first quality guard")


def check_handoff() -> None:
    run([sys.executable, str(CAP / "scripts" / "export_handoff.py")])
    run([sys.executable, str(CAP / "scripts" / "validate_handoff.py")])
    manifest = json.loads((CAP / "handoff" / "MANIFEST.json").read_text())
    if len(manifest["files"]) < 9:
        raise SystemExit("handoff is incomplete")
    print(f"PASS Course 2 handoff — {len(manifest['files'])} files")


def core_proof() -> int:
    check_structure()
    check_markdown_links()
    check_navigation()
    check_data()
    check_python()
    check_shell()
    check_reader_quality()
    check_handoff()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(CAP)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"], cwd=CAP)
    run([sys.executable, str(CAP / "scripts" / "verify_pki.py")])
    print("PASS core proof")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["core-proof", "structure", "links", "data", "python", "handoff"])
    args = parser.parse_args()
    return {
        "core-proof": core_proof,
        "structure": lambda: (check_structure() or 0),
        "links": lambda: (check_markdown_links() or 0),
        "data": lambda: (check_data() or 0),
        "python": lambda: (check_python() or 0),
        "handoff": lambda: (check_handoff() or 0),
    }[args.action]()


if __name__ == "__main__":
    raise SystemExit(main())
