from __future__ import annotations

import re
from collections import Counter
from datetime import date
from pathlib import Path

from .manifest import find_module
from .result import ValidationResult

FRONT_MATTER_FIELDS = (
    "module_id",
    "program",
    "level",
    "module_number",
    "title",
    "status",
    "last_verified",
)

REQUIRED_SECTIONS = (
    "One-Page Review",
    "Governing Question",
    "Why This Matters",
    "Prerequisites and Retrieval",
    "Learning Objectives",
    "Core Exposition",
    "Definitions and Notation",
    "Mechanisms, Invariants, or Proof Structure",
    "Alternatives and Trade-Offs",
    "Failure Modes and Misconceptions",
    "Worked Examples",
    "Cross-Program Connections",
    "References",
    "Exercises",
    "Answers to the Exercises",
)

REVIEW_SUBSECTIONS = (
    "Governing question",
    "Essential definitions",
    "Central model, mechanism, or theorem",
    "Critical invariants",
    "Common failures",
    "Compact example",
    "Connections",
)

FRONT_MATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
H1 = re.compile(r"^# (.+)$", re.MULTILINE)
H2 = re.compile(r"^## (.+)$", re.MULTILINE)
H3 = re.compile(r"^### (.+)$", re.MULTILINE)
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
REFERENCE_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
REFERENCE_DEFINITION = re.compile(r"^\[([^\]]+)\]:\s+(\S+)", re.MULTILINE)


def _front_matter(text: str, issues: list[str]) -> tuple[dict[str, str], int]:
    match = FRONT_MATTER.match(text)
    if not match:
        issues.append("chapter must begin with YAML front matter delimited by ---")
        return {}, 0
    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            issues.append(f"invalid front matter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in values:
            issues.append(f"duplicate front matter field: {key}")
        values[key] = value
    if tuple(values) != FRONT_MATTER_FIELDS:
        issues.append(f"front matter fields must be exactly {', '.join(FRONT_MATTER_FIELDS)} in order")
    return values, match.end()


def _section_bodies(text: str, issues: list[str]) -> dict[str, str]:
    matches = list(H2.finditer(text))
    names = tuple(match.group(1).strip() for match in matches)
    if names != REQUIRED_SECTIONS:
        issues.append("H2 sections do not match the required names and order")
    bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        bodies[match.group(1).strip()] = text[match.end():end].strip()
    for name in REQUIRED_SECTIONS:
        if not bodies.get(name):
            issues.append(f"section is empty or missing: {name}")
    return bodies


def _normalize_prose(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))


def _numbered_entries(section: str, kind: str, expected: int, issues: list[str]) -> None:
    matches = list(H3.finditer(section))
    names = [match.group(1).strip() for match in matches]
    required = [f"{kind} {number}" for number in range(1, expected + 1)]
    if names != required:
        issues.append(f"{kind.lower()} headings must be exactly numbered 1 through {expected}")
        return
    normalized: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        body = section[match.end():end].strip()
        prose = _normalize_prose(body)
        if not prose:
            issues.append(f"{kind} {index + 1} is empty")
        normalized.append(prose)
    duplicates = [body for body, count in Counter(normalized).items() if body and count > 1]
    if duplicates:
        issues.append(f"{kind.lower()} entries contain exact normalized duplicates")


def _destination(raw_target: str) -> str:
    stripped = raw_target.strip()
    if stripped.startswith("<") and ">" in stripped:
        return stripped[1:stripped.index(">")]
    return stripped.split(maxsplit=1)[0]


def _local_target(path: Path, raw_target: str, issues: list[str]) -> None:
    target = _destination(raw_target)
    if not target or target.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return
    target_path = target.split("#", 1)[0]
    if target_path:
        resolved = (path.parent / target_path).resolve()
        if not resolved.exists():
            issues.append(f"unresolved local link: {raw_target}")


def _links(path: Path, text: str, issues: list[str]) -> None:
    for raw_target in INLINE_LINK.findall(text):
        _local_target(path, raw_target, issues)

    definitions: dict[str, str] = {}
    for label, raw_target in REFERENCE_DEFINITION.findall(text):
        normalized = label.casefold().strip()
        if normalized in definitions:
            issues.append(f"duplicate Markdown reference definition: {label}")
        definitions[normalized] = raw_target
        _local_target(path, raw_target, issues)

    for label, reference in REFERENCE_LINK.findall(text):
        normalized = (reference or label).casefold().strip()
        if normalized not in definitions:
            issues.append(f"missing Markdown reference definition: {reference or label}")


def validate_chapter_text(
    text: str,
    manifest_row: dict[str, str],
    *,
    allow_draft: bool = False,
    path: Path | None = None,
) -> ValidationResult:
    issues: list[str] = []
    front, body_start = _front_matter(text, issues)
    body = text[body_start:]
    expected = {
        "module_id": manifest_row["module_id"],
        "program": manifest_row["program_name"],
        "level": manifest_row["level"],
        "module_number": str(int(manifest_row["module_number"])),
        "title": manifest_row["module_title"],
    }
    for key, value in expected.items():
        if front.get(key) != value:
            issues.append(f"front matter {key} differs from the manifest")

    status = front.get("status")
    manifest_status = manifest_row["status"]
    if allow_draft and manifest_status == "planned":
        if status != "draft":
            issues.append("a planned manifest row must use draft front matter during draft validation")
    elif status != "complete" or manifest_status != "complete":
        issues.append("completion validation requires complete status in both chapter and manifest")

    verified = front.get("last_verified", "")
    try:
        verified_date = date.fromisoformat(verified)
        if verified_date > date.today():
            issues.append("last_verified cannot be in the future")
    except ValueError:
        issues.append("last_verified must be an ISO date")

    h1_matches = H1.findall(body)
    if h1_matches != [manifest_row["module_title"]]:
        issues.append("chapter must contain exactly one H1 matching the canonical title")

    sections = _section_bodies(body, issues)
    review_names = [match.group(1).strip() for match in H3.finditer(sections.get("One-Page Review", ""))]
    if tuple(review_names) != REVIEW_SUBSECTIONS:
        issues.append("One-Page Review subsections do not match the contract")
    _numbered_entries(sections.get("Worked Examples", ""), "Example", 10, issues)
    _numbered_entries(sections.get("Exercises", ""), "Exercise", 5, issues)
    _numbered_entries(sections.get("Answers to the Exercises", ""), "Answer", 5, issues)

    references = [
        line
        for line in sections.get("References", "").splitlines()
        if re.match(r"^\s*(?:[-*+] |\d+\. )", line)
    ]
    if len(references) < 3:
        issues.append("References must contain at least three structured entries")
    if len({_normalize_prose(reference) for reference in references}) != len(references):
        issues.append("References contain exact normalized duplicates")
    if path is not None:
        _links(path, body, issues)
    return ValidationResult(tuple(issues))


def validate_chapter(root: Path, module_id: str, *, allow_draft: bool = False) -> ValidationResult:
    root = root.resolve()
    row = find_module(root, module_id)
    if row is None:
        return ValidationResult((f"module ID does not resolve exactly once: {module_id}",))
    path = root / row["future_path"]
    if not path.is_file():
        return ValidationResult((f"module file is missing: {row['future_path']}",))
    return validate_chapter_text(path.read_text(encoding="utf-8"), row, allow_draft=allow_draft, path=path)
