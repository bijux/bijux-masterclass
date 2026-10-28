from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.review import (
    MATHEMATICS_CATEGORIES,
    chapter_digest,
    validate_review_record,
)
from test_chapter import valid_draft


def completed_review(chapter: str) -> dict:
    return {
        "schema_version": 1,
        "module_id": "PLS-001",
        "chapter_digest": chapter_digest(chapter),
        "review_date": "2026-08-28",
        "source_review": {
            "status": "passed",
            "checked_references": 3,
            "current_claims": "not_applicable",
            "retrieval_date": None,
            "notes": "All three cited editions and publication identities were checked.",
        },
        "mathematics": {
            category: {
                "status": "not_applicable",
                "method": "not_applicable",
                "evidence": [],
                "notes": f"{category} is not required by this synthetic structural fixture.",
            }
            for category in MATHEMATICS_CATEGORIES
        },
        "conceptual_review": {
            "status": "passed",
            "notes": "Definitions, assumptions, mechanisms, and conclusions are internally coherent.",
        },
        "practitioner_review": {
            "status": "passed",
            "notes": "Implementation consequences and failure behavior were reviewed.",
        },
        "pedagogical_review": {
            "status": "passed",
            "notes": "Examples are distinct and exercises progress from retrieval through transfer.",
        },
        "external_review_claimed": False,
        "limitations": "Internal review only; no external academic or practitioner review is claimed.",
    }


class ReviewValidationTests(unittest.TestCase):
    def test_completed_review_passes(self) -> None:
        chapter = valid_draft()
        record = completed_review(chapter)
        result = validate_review_record(json.dumps(record), chapter, "PLS-001")
        self.assertEqual((), result.issues)

    def test_unreviewed_category_fails(self) -> None:
        chapter = valid_draft()
        record = completed_review(chapter)
        record["conceptual_review"]["status"] = "unreviewed"
        result = validate_review_record(json.dumps(record), chapter, "PLS-001")
        self.assertTrue(any("conceptual_review" in issue for issue in result.issues))

    def test_chapter_change_invalidates_review(self) -> None:
        chapter = valid_draft()
        record = completed_review(chapter)
        changed = chapter.replace("explicit conclusion", "different conclusion", 1)
        result = validate_review_record(json.dumps(record), changed, "PLS-001")
        self.assertTrue(any("chapter_digest" in issue for issue in result.issues))

    def test_status_transition_preserves_review_digest(self) -> None:
        chapter = valid_draft()
        complete = chapter.replace("status: draft", "status: complete", 1)
        self.assertEqual(chapter_digest(chapter), chapter_digest(complete))

    def test_current_claims_require_retrieval_date(self) -> None:
        chapter = valid_draft()
        record = completed_review(chapter)
        record["source_review"]["current_claims"] = "passed"
        result = validate_review_record(json.dumps(record), chapter, "PLS-001")
        self.assertTrue(any("retrieval_date" in issue for issue in result.issues))

    def test_limitations_must_disclaim_external_review(self) -> None:
        chapter = valid_draft()
        record = completed_review(chapter)
        record["limitations"] = "All review was comprehensive."
        result = validate_review_record(json.dumps(record), chapter, "PLS-001")
        self.assertTrue(any("disclaim external review" in issue for issue in result.issues))

    def test_passed_mathematics_requires_explicit_evidence(self) -> None:
        chapter = valid_draft()
        record = completed_review(chapter)
        record["mathematics"]["invariant_checking"] = {
            "status": "passed",
            "method": "invariant_analysis",
            "evidence": [],
            "notes": "The invariant was checked against the worked examples.",
        }
        result = validate_review_record(json.dumps(record), chapter, "PLS-001")
        self.assertTrue(any("explicit evidence entries" in issue for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
