from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from .chapter import FRONT_MATTER, H2
from .manifest import find_module
from .result import ValidationResult

MATHEMATICS_CATEGORIES = (
    "notation_and_syntax",
    "numerical_recomputation",
    "symbolic_recomputation",
    "boundary_and_adversarial_cases",
    "invariant_checking",
    "proof_review",
    "proof_sketch_labeling",
    "empirical_evidence_labeling",
)

REVIEW_SECTIONS = (
    "conceptual_review",
    "practitioner_review",
    "pedagogical_review",
)

TOP_LEVEL_FIELDS = (
    "schema_version",
    "module_id",
    "chapter_digest",
    "review_date",
    "source_review",
    "mathematics",
    "conceptual_review",
    "practitioner_review",
    "pedagogical_review",
    "external_review_claimed",
    "limitations",
)

SOURCE_FIELDS = (
    "status",
    "checked_references",
    "current_claims",
    "retrieval_date",
    "notes",
)

REVIEW_FIELDS = (
    "status",
    "notes",
)

MATHEMATICS_FIELDS = (
    "status",
    "method",
    "evidence",
    "notes",
)

MATHEMATICS_METHODS = {
    "boundary_analysis",
    "empirical_reproduction",
    "invariant_analysis",
    "label_audit",
    "manual_review",
    "numerical_recomputation",
    "proof_review",
    "symbolic_recomputation",
}


def review_path(root: Path, module_id: str) -> Path:
    return root / "artifacts" / "reviews" / module_id / "review.json"


def chapter_digest(text: str) -> str:
    front = FRONT_MATTER.match(text)
    if front is None:
        normalized = text
    else:
        normalized_front = re.sub(
            r"^status: (?:draft|complete)$",
            "status: <reviewed>",
            front.group(0),
            count=1,
            flags=re.MULTILINE,
        )
        normalized = normalized_front + text[front.end():]
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def reference_count(text: str) -> int:
    matches = list(H2.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() != "References":
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end():end]
        return sum(
            bool(re.match(r"^\s*(?:[-*+] |\d+\. )", line))
            for line in section.splitlines()
        )
    return 0


def _front_value(text: str, field: str) -> str | None:
    front = FRONT_MATTER.match(text)
    if front is None:
        return None
    match = re.search(rf"^{re.escape(field)}:\s*(.+)$", front.group("body"), re.MULTILINE)
    return match.group(1).strip() if match else None


def create_review_template(root: Path, module_id: str) -> Path:
    root = root.resolve()
    row = find_module(root, module_id)
    if row is None:
        raise ValueError(f"module ID does not resolve exactly once: {module_id}")
    chapter = root / row["future_path"]
    if not chapter.is_file():
        raise ValueError(f"module file is missing: {row['future_path']}")
    text = chapter.read_text(encoding="utf-8")
    verified = _front_value(text, "last_verified") or ""
    record: dict[str, Any] = {
        "schema_version": 1,
        "module_id": module_id,
        "chapter_digest": chapter_digest(text),
        "review_date": verified,
        "source_review": {
            "status": "unreviewed",
            "checked_references": reference_count(text),
            "current_claims": "unreviewed",
            "retrieval_date": None,
            "notes": "",
        },
        "mathematics": {
            category: {
                "status": "unreviewed",
                "method": "unreviewed",
                "evidence": [],
                "notes": "",
            }
            for category in MATHEMATICS_CATEGORIES
        },
        "conceptual_review": {"status": "unreviewed", "notes": ""},
        "practitioner_review": {"status": "unreviewed", "notes": ""},
        "pedagogical_review": {"status": "unreviewed", "notes": ""},
        "external_review_claimed": False,
        "limitations": (
            "Internal evidence record only; no external academic or practitioner review is claimed."
        ),
    }
    path = review_path(root, module_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"review record already exists: {path.relative_to(root)}")
    candidate = path.parent / ".review.json.bijux-candidate"
    candidate.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    candidate.replace(path)
    return path


def _validate_review_entry(
    value: Any,
    name: str,
    issues: list[str],
) -> None:
    if not isinstance(value, dict) or tuple(value) != REVIEW_FIELDS:
        issues.append(f"{name} fields must be exactly status and notes in order")
        return
    if value["status"] != "passed":
        issues.append(f"{name} has non-completing status {value['status']!r}")
    if not isinstance(value["notes"], str) or not value["notes"].strip():
        issues.append(f"{name} must record substantive review notes")


def _validate_mathematics_entry(value: Any, name: str, issues: list[str]) -> None:
    if not isinstance(value, dict) or tuple(value) != MATHEMATICS_FIELDS:
        issues.append(
            f"{name} fields must be exactly status, method, evidence, and notes in order"
        )
        return
    status = value["status"]
    method = value["method"]
    evidence = value["evidence"]
    if status not in {"passed", "not_applicable"}:
        issues.append(f"{name} has non-completing status {status!r}")
    if not isinstance(value["notes"], str) or not value["notes"].strip():
        issues.append(f"{name} must record substantive review notes")
    if status == "not_applicable":
        if method != "not_applicable" or evidence != []:
            issues.append(f"{name} not_applicable outcomes require no evidence")
        return
    if method not in MATHEMATICS_METHODS:
        issues.append(f"{name} must identify a supported verification method")
    if not isinstance(evidence, list) or not evidence or not all(
        isinstance(item, str) and item.strip() for item in evidence
    ):
        issues.append(f"{name} passed outcomes require explicit evidence entries")


def validate_review_record(
    text: str,
    chapter_text: str,
    module_id: str,
) -> ValidationResult:
    issues: list[str] = []
    try:
        record = json.loads(text)
    except json.JSONDecodeError as error:
        return ValidationResult((f"invalid review JSON: {error.msg}",))
    if not isinstance(record, dict):
        return ValidationResult(("review record must be a JSON object",))
    if tuple(record) != TOP_LEVEL_FIELDS:
        issues.append("review record fields differ from the canonical schema or order")
        return ValidationResult(tuple(issues))

    if record["schema_version"] != 1:
        issues.append("review record schema_version must be 1")
    if record["module_id"] != module_id:
        issues.append("review record module_id differs from the selected module")
    if record["chapter_digest"] != chapter_digest(chapter_text):
        issues.append("review record chapter_digest does not match the chapter")
    try:
        reviewed = date.fromisoformat(record["review_date"])
        if reviewed > date.today():
            issues.append("review_date cannot be in the future")
    except (TypeError, ValueError):
        issues.append("review_date must be an ISO date")
    if record["review_date"] != _front_value(chapter_text, "last_verified"):
        issues.append("review_date must match the chapter last_verified date")

    source = record["source_review"]
    if not isinstance(source, dict) or tuple(source) != SOURCE_FIELDS:
        issues.append("source_review fields differ from the canonical schema or order")
    else:
        if source["status"] != "passed":
            issues.append(f"source_review has non-completing status {source['status']!r}")
        expected_references = reference_count(chapter_text)
        if source["checked_references"] != expected_references or expected_references < 3:
            issues.append("source_review must cover every structured chapter reference")
        if source["current_claims"] not in {"passed", "not_applicable"}:
            issues.append("source_review current_claims must be passed or not_applicable")
        retrieval_date = source["retrieval_date"]
        if source["current_claims"] == "passed":
            try:
                retrieved = date.fromisoformat(retrieval_date)
                if retrieved > date.today():
                    issues.append("source_review retrieval_date cannot be in the future")
            except (TypeError, ValueError):
                issues.append("source_review retrieval_date must be an ISO date for current claims")
        elif retrieval_date is not None:
            issues.append("source_review retrieval_date must be null when current claims do not apply")
        if not isinstance(source["notes"], str) or not source["notes"].strip():
            issues.append("source_review must record substantive notes")

    mathematics = record["mathematics"]
    if not isinstance(mathematics, dict) or tuple(mathematics) != MATHEMATICS_CATEGORIES:
        issues.append("mathematics categories differ from the canonical schema or order")
    else:
        for category in MATHEMATICS_CATEGORIES:
            _validate_mathematics_entry(
                mathematics[category],
                f"mathematics.{category}",
                issues,
            )

    for section in REVIEW_SECTIONS:
        _validate_review_entry(record[section], section, issues)
    if record["external_review_claimed"] is not False:
        issues.append("internal evidence must not claim external review")
    limitations = record["limitations"]
    if not isinstance(limitations, str) or not limitations.strip():
        issues.append("review limitations must be stated")
    elif "external" not in limitations.casefold() or not re.search(
        r"\b(?:no|not)\b", limitations.casefold()
    ):
        issues.append("review limitations must explicitly disclaim external review")
    return ValidationResult(tuple(issues))


def validate_module_review(root: Path, module_id: str) -> ValidationResult:
    root = root.resolve()
    row = find_module(root, module_id)
    if row is None:
        return ValidationResult((f"module ID does not resolve exactly once: {module_id}",))
    chapter = root / row["future_path"]
    if not chapter.is_file():
        return ValidationResult((f"module file is missing: {row['future_path']}",))
    path = review_path(root, module_id)
    if not path.is_file():
        return ValidationResult((f"module review evidence is missing: {path.relative_to(root)}",))
    try:
        chapter_text = chapter.read_text(encoding="utf-8")
        record_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return ValidationResult((f"cannot read review inputs: {error}",))
    return validate_review_record(record_text, chapter_text, module_id)
