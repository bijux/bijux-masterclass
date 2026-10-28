#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re
import sys

try:
    import yaml
except ImportError as error:
    raise SystemExit(f"PyYAML is required for the program audit: {error}")

ROOT = Path(__file__).resolve().parents[1]
COURSES = [
    ("01-node-typescript-foundations", 1),
    ("02-javascript-object-model-runtime-protocols", 11),
    ("03-advanced-typescript-library-api-design", 21),
    ("04-async-node-event-driven-architecture", 31),
    ("05-node-streams-filesystems-data-pipelines", 41),
]
SKIP = {"node_modules", "dist", "site", "__pycache__", ".pytest_cache", ".mypy_cache"}
errors: list[str] = []


def visible(path: Path) -> bool:
    return not any(part in SKIP for part in path.parts)


def walk_nav(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, list):
        for item in value:
            found.extend(walk_nav(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(walk_nav(item))
    return found

# Program-level reader surfaces.
for name in (
    "README.md",
    "START_HERE.md",
    "REASONING_MODEL.md",
    "COURSE_MAP.md",
    "SKILL_MAP.md",
    "PROGRESS.md",
    "GLOSSARY.md",
    "SOURCE_NOTES.md",
    "Makefile",
    "mkdocs.yml",
):
    if not (ROOT / name).is_file():
        errors.append(f"missing program file: {name}")

all_modules: list[int] = []
all_labs: list[int] = []
all_cases = 0
package_names: list[str] = []
executable_packages = 0

for course_name, first_module in COURSES:
    course = ROOT / course_name
    if not course.is_dir():
        errors.append(f"missing course directory: {course_name}")
        continue

    modules = sorted((course / "course-book").glob("module-*"))
    if len(modules) != 10:
        errors.append(f"{course_name}: expected 10 modules, found {len(modules)}")
    for offset, module in enumerate(modules):
        number = first_module + offset
        if not module.name.startswith(f"module-{number:02d}-"):
            errors.append(f"{course_name}: unexpected module order: {module.name}")
        all_modules.append(number)
        for page in ("index.md", "workbook.md", "solutions.md"):
            if not (module / page).is_file():
                errors.append(f"{course_name}: missing {module.name}/{page}")

    labs = sorted((course / "labs").glob("module-*"))
    if len(labs) != 10:
        errors.append(f"{course_name}: expected 10 labs, found {len(labs)}")
    for offset, lab in enumerate(labs):
        number = first_module + offset
        if not lab.name.startswith(f"module-{number:02d}-"):
            errors.append(f"{course_name}: unexpected lab order: {lab.name}")
        all_labs.append(number)
        for kind in ("starter", "reference"):
            package = lab / kind / "package.json"
            source = lab / kind / "src" / "index.ts"
            tests = list((lab / kind / "tests").glob("*.test.ts"))
            if not package.is_file():
                errors.append(f"{course_name}: missing {package.relative_to(course)}")
            if not source.is_file():
                errors.append(f"{course_name}: missing {source.relative_to(course)}")
            if not tests:
                errors.append(f"{course_name}: no tests in {lab.name}/{kind}")
            executable_packages += 1

    capstone = course / "capstone"
    if not (capstone / "package.json").is_file():
        errors.append(f"{course_name}: capstone package missing")
    if not list((capstone / "src").glob("*.ts")):
        errors.append(f"{course_name}: capstone sources missing")
    if not list((capstone / "tests").glob("*.test.ts")):
        errors.append(f"{course_name}: capstone tests missing")
    executable_packages += 1

    manifest_path = course / "compiler-labs" / "manifest.json"
    if not manifest_path.is_file():
        errors.append(f"{course_name}: investigation manifest missing")
    else:
        try:
            cases = json.loads(manifest_path.read_text(encoding="utf-8")).get("cases", [])
        except Exception as error:
            errors.append(f"{course_name}: invalid investigation manifest: {error}")
            cases = []
        if len(cases) != 80:
            errors.append(f"{course_name}: expected 80 investigations, found {len(cases)}")
        all_cases += len(cases)

if all_modules != list(range(1, 51)):
    errors.append(f"global module sequence is not 1..50: {all_modules}")
if all_labs != list(range(1, 51)):
    errors.append(f"global lab sequence is not 1..50: {all_labs}")
if all_cases != 400:
    errors.append(f"expected 400 investigations, found {all_cases}")
if executable_packages != 105:
    errors.append(f"expected 105 executable packages, found {executable_packages}")

# JSON and package identity.
for path in ROOT.rglob("*.json"):
    if not visible(path):
        continue
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {error}")
        continue
    if path.name == "package.json" and isinstance(data, dict):
        name = data.get("name")
        if isinstance(name, str) and name:
            package_names.append(name)

for name, count in Counter(package_names).items():
    if count > 1:
        errors.append(f"duplicate package name ({count}): {name}")

# Program navigation must point at real reader pages.
try:
    mkdocs = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
except Exception as error:
    errors.append(f"invalid mkdocs.yml: {error}")
    mkdocs = {}
for target in walk_nav(mkdocs.get("nav", [])) if isinstance(mkdocs, dict) else []:
    if target.startswith(("http://", "https://")):
        continue
    if not (ROOT / target).is_file():
        errors.append(f"mkdocs target missing: {target}")

# Root progression must expose every module exactly once.
progress = (ROOT / "PROGRESS.md").read_text(encoding="utf-8") if (ROOT / "PROGRESS.md").is_file() else ""
progress_numbers = [int(value) for value in re.findall(r"^- \[ \] Module (\d+)\b", progress, flags=re.M)]
if progress_numbers != list(range(1, 51)):
    errors.append("PROGRESS.md does not contain one ordered checklist entry for Modules 1–50")

# Reader-facing hygiene and release cleanliness.
for page in ROOT.rglob("*.md"):
    if not visible(page):
        continue
    text = page.read_text(encoding="utf-8")
    if text.count("```") % 2:
        errors.append(f"unbalanced Markdown fence: {page.relative_to(ROOT)}")
    if re.search(r"\b(TODO|TBD|FIXME|coming soon|lorem ipsum)\b", text, flags=re.I):
        errors.append(f"unfinished marker: {page.relative_to(ROOT)}")

for path in ROOT.rglob("*"):
    if path.is_dir() and path.name in SKIP:
        errors.append(f"generated or temporary directory present: {path.relative_to(ROOT)}")
    if path.is_symlink():
        errors.append(f"symlink present: {path.relative_to(ROOT)}")
    if path.is_file() and path.stat().st_size == 0:
        errors.append(f"zero-byte file: {path.relative_to(ROOT)}")

if errors:
    print("Node Courses 1–5 program audit failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

markdown_pages = sum(1 for path in ROOT.rglob("*.md") if visible(path))
typescript_sources = sum(1 for path in ROOT.rglob("*.ts") if visible(path))
print("Node Courses 1–5 program audit passed:")
print(f"  modules: {len(all_modules)}")
print(f"  labs: {len(all_labs)}")
print(f"  investigations: {all_cases}")
print(f"  executable packages: {executable_packages}")
print(f"  Markdown pages: {markdown_pages}")
print(f"  TypeScript sources: {typescript_sources}")
