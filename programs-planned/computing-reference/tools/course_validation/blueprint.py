from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from .manifest import normalized_row, read_csv, read_jsonl
from .result import ValidationResult

BANNED_TITLE_PHRASES = (
    "overview",
    "advanced topics",
    "miscellaneous",
    "future directions",
    "final synthesis",
    "capstone",
    "comprehensive project",
)

PROGRAM_FIELDS = (
    "program_number",
    "program_code",
    "program_name",
    "slug",
    "minimum_levels",
    "modules_per_level",
    "total_modules",
    "purpose",
    "role_readiness",
)

MODULE_FIELDS = (
    "program_number",
    "program_code",
    "program_name",
    "program_slug",
    "level",
    "level_name",
    "level_module_number",
    "block_number",
    "block_in_level",
    "block_title",
    "module_number",
    "module_id",
    "module_title",
    "future_path",
    "status",
)

PROGRAM_INTEGER_FIELDS = (
    "program_number",
    "minimum_levels",
    "modules_per_level",
    "total_modules",
)

MODULE_INTEGER_FIELDS = (
    "program_number",
    "level",
    "level_module_number",
    "block_number",
    "block_in_level",
    "module_number",
)

ROADMAP_ROW = re.compile(
    r"^\|\s*(\d{3})\s*\|\s*\*\*(.+?)\*\*\s*\|\s*`([^`]+)`\s*\|$",
    re.MULTILINE,
)
INDEX_ROW = re.compile(
    r"^\|\s*(\d{3})\s*\|\s*`([A-Z0-9]+-\d{3})`\s*\|\s*(.+?)\s*\|\s*`([^`]+)`\s*\|$",
    re.MULTILINE,
)


def _read_manifests(root: Path, issues: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    programs_path = root / "manifests" / "programs.csv"
    modules_path = root / "manifests" / "modules.csv"
    jsonl_path = root / "manifests" / "modules.jsonl"
    for path in (programs_path, modules_path, jsonl_path):
        if not path.is_file():
            issues.append(f"missing manifest: {path.relative_to(root)}")
    if issues:
        return [], []

    try:
        programs = read_csv(programs_path)
        modules = read_csv(modules_path)
        jsonl = read_jsonl(jsonl_path)
    except (csv.Error, json.JSONDecodeError, OSError, UnicodeError) as error:
        issues.append(f"cannot parse manifests: {error}")
        return [], []

    schema_is_valid = True
    if not programs or tuple(programs[0]) != PROGRAM_FIELDS:
        issues.append("program manifest fields differ from the canonical schema")
        schema_is_valid = False
    if not modules or tuple(modules[0]) != MODULE_FIELDS:
        issues.append("module CSV fields differ from the canonical schema")
        schema_is_valid = False
    if not jsonl or any(tuple(row) != MODULE_FIELDS for row in jsonl):
        issues.append("module JSONL fields differ from the canonical schema")
        schema_is_valid = False
    if not schema_is_valid:
        return [], []

    normalized_jsonl = [normalized_row(row) for row in jsonl]
    if modules != normalized_jsonl:
        issues.append("module CSV and JSONL rows or values differ")
    return programs, modules


def _check_unique(rows: list[dict[str, str]], field: str, issues: list[str], *, casefold: bool = False) -> None:
    values = [row[field].strip() for row in rows]
    compared = [value.casefold() for value in values] if casefold else values
    duplicate_keys = {value for value, count in Counter(compared).items() if count > 1}
    if duplicate_keys:
        examples = [value for value in values if (value.casefold() if casefold else value) in duplicate_keys]
        issues.append(f"duplicate {field}: {examples[:10]}")


def _check_integers(
    rows: list[dict[str, str]],
    fields: tuple[str, ...],
    row_identity: str,
    issues: list[str],
) -> bool:
    valid = True
    for row_number, row in enumerate(rows, start=2):
        for field in fields:
            try:
                int(row[field])
            except ValueError:
                identity = row.get(row_identity) or f"row {row_number}"
                issues.append(f"{identity}: {field} must be an integer")
                valid = False
    return valid


def _check_program(
    root: Path,
    program: dict[str, str],
    rows: list[dict[str, str]],
    issues: list[str],
) -> None:
    code = program["program_code"]
    if len(rows) != 100:
        issues.append(f"{code}: expected 100 modules, found {len(rows)}")
        return
    rows.sort(key=lambda row: int(row["module_number"]))
    numbers = [int(row["module_number"]) for row in rows]
    if numbers != list(range(1, 101)):
        issues.append(f"{code}: numbering is not continuous from 001 through 100")

    levels = Counter(int(row["level"]) for row in rows)
    if levels != Counter({1: 50, 2: 50}):
        issues.append(f"{code}: expected 50 modules in each level, found {dict(levels)}")
    blocks = Counter(int(row["block_number"]) for row in rows)
    if set(blocks) != set(range(1, 11)) or any(count != 10 for count in blocks.values()):
        issues.append(f"{code}: expected ten blocks of ten modules")
    block_titles: defaultdict[int, set[str]] = defaultdict(set)
    for row in rows:
        block_titles[int(row["block_number"])].add(row["block_title"].strip())
    if any(len(titles) != 1 or "" in titles for titles in block_titles.values()):
        issues.append(f"{code}: block titles are empty or inconsistent within a block")

    roadmap = root / "programs" / program["slug"] / "ROADMAP.md"
    if not roadmap.is_file():
        issues.append(f"{code}: roadmap is missing")
        return
    text = roadmap.read_text(encoding="utf-8")
    code_match = re.search(r"^\*\*Program code:\*\* `([^`]+)`", text, re.MULTILINE)
    if not code_match or code_match.group(1) != code:
        issues.append(f"{code}: roadmap program code differs from the manifest")
    for label in (
        "Purpose",
        "Level-II professional outcome",
        "Prerequisites",
        "Primary ownership",
        "Explicit exclusions",
    ):
        if not re.search(rf"^\*\*{re.escape(label)}:\*\*\s+\S", text, re.MULTILINE):
            issues.append(f"{code}: roadmap omits {label}")

    roadmap_rows = [
        (int(match.group(1)), match.group(2), match.group(3))
        for match in ROADMAP_ROW.finditer(text)
    ]
    expected_rows = [
        (int(row["module_number"]), row["module_title"], Path(row["future_path"]).name)
        for row in rows
    ]
    if roadmap_rows != expected_rows:
        issues.append(f"{code}: roadmap rows differ from the module manifests")

    for row in rows:
        module_id = row["module_id"]
        number = int(row["module_number"])
        level = int(row["level"])
        if (
            row["program_number"] != program["program_number"]
            or row["program_code"] != code
            or row["program_slug"] != program["slug"]
            or row["program_name"] != program["program_name"]
        ):
            issues.append(f"{module_id}: program identity differs between manifests")
        if level != (1 if number <= 50 else 2):
            issues.append(f"{module_id}: level does not match module number")
        expected_level_name = (
            "Level I — Undergraduate Core"
            if level == 1
            else "Level II — Graduate and Professional Depth"
        )
        if row["level_name"] != expected_level_name:
            issues.append(f"{module_id}: level name is incorrect")
        expected_level_number = number if level == 1 else number - 50
        if int(row["level_module_number"]) != expected_level_number:
            issues.append(f"{module_id}: level-relative module number is incorrect")
        if int(row["block_number"]) != (number - 1) // 10 + 1:
            issues.append(f"{module_id}: block number is incorrect")
        if int(row["block_in_level"]) != (number - 1) // 10 % 5 + 1:
            issues.append(f"{module_id}: level-relative block number is incorrect")
        if not row["block_title"].strip():
            issues.append(f"{module_id}: block title is empty")
        if not re.fullmatch(rf"{re.escape(code)}-\d{{3}}", module_id):
            issues.append(f"{module_id}: invalid module identifier")
        title = row["module_title"].strip()
        for phrase in BANNED_TITLE_PHRASES:
            if phrase in title.casefold():
                issues.append(f'{module_id}: banned filler phrase "{phrase}"')
        expected_path = re.compile(
            rf"programs/{re.escape(program['slug'])}/modules/"
            rf"{number:03}-[a-z0-9]+(?:-[a-z0-9]+)*\.md"
        )
        if not expected_path.fullmatch(row["future_path"]):
            issues.append(f"{module_id}: future path does not match its program and number")
        status = row["status"]
        if status not in {"planned", "complete"}:
            issues.append(f"{module_id}: unsupported status {status!r}")
        chapter = root / row["future_path"]
        if chapter.exists() and chapter.stat().st_size == 0:
            issues.append(f"{module_id}: empty placeholder chapter exists")
        if status == "complete" and not chapter.is_file():
            issues.append(f"{module_id}: complete status has no chapter file")


def validate_blueprint(root: Path) -> tuple[ValidationResult, dict[str, int]]:
    root = root.resolve()
    issues: list[str] = []
    programs, modules = _read_manifests(root, issues)
    if not programs or not modules:
        return ValidationResult(tuple(issues)), {}

    if len(programs) != 30:
        issues.append(f"expected 30 programs, found {len(programs)}")
    if len(modules) != 3000:
        issues.append(f"expected 3,000 modules, found {len(modules)}")
    integers_are_valid = _check_integers(
        programs,
        PROGRAM_INTEGER_FIELDS,
        "program_code",
        issues,
    )
    integers_are_valid = (
        _check_integers(modules, MODULE_INTEGER_FIELDS, "module_id", issues)
        and integers_are_valid
    )
    if not integers_are_valid:
        return ValidationResult(tuple(issues)), {}
    _check_unique(programs, "program_code", issues)
    _check_unique(programs, "slug", issues)
    _check_unique(modules, "module_id", issues)
    _check_unique(modules, "module_title", issues, casefold=True)
    _check_unique(modules, "future_path", issues)

    program_numbers = [int(program["program_number"]) for program in programs]
    if program_numbers != list(range(1, 31)):
        issues.append("program numbers are not ordered continuously from 1 through 30")
    for program in programs:
        code = program["program_code"]
        number = int(program["program_number"])
        if not re.fullmatch(r"[A-Z0-9]+", code):
            issues.append(f"{code}: invalid program code")
        if not re.fullmatch(rf"{number:02}-[a-z0-9]+(?:-[a-z0-9]+)*", program["slug"]):
            issues.append(f"{code}: invalid canonical program slug")
        if (
            program["minimum_levels"] != "2"
            or program["modules_per_level"] != "50"
            or program["total_modules"] != "100"
        ):
            issues.append(f"{code}: program size metadata differs from the canonical model")
        if not program["purpose"].strip() or not program["role_readiness"].strip():
            issues.append(f"{code}: purpose or role-readiness statement is empty")

    by_program: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in modules:
        by_program[row["program_code"]].append(row)
    manifest_codes = {program["program_code"] for program in programs}
    if set(by_program) != manifest_codes:
        issues.append("program codes differ between program and module manifests")
    for program in programs:
        _check_program(root, program, by_program[program["program_code"]], issues)

    combined_path = root / "ALL_3000_MODULES.md"
    if not combined_path.is_file():
        issues.append("combined module index is missing")
    else:
        combined = combined_path.read_text(encoding="utf-8")
        index_rows = [
            (match.group(2), match.group(3), match.group(4))
            for match in INDEX_ROW.finditer(combined)
        ]
        expected_index = [
            (row["module_id"], row["module_title"], row["future_path"])
            for row in modules
        ]
        if index_rows != expected_index:
            issues.append("combined module index differs from the manifests")

    summary = {
        "programs": len(programs),
        "modules": len(modules),
        "complete_modules": sum(row["status"] == "complete" for row in modules),
        "planned_modules": sum(row["status"] == "planned" for row in modules),
    }
    return ValidationResult(tuple(issues)), summary
