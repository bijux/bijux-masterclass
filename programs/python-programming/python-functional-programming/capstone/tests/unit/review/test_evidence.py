from __future__ import annotations

from funcpipe_rag.review.evidence import EvidenceClaim, assess_evidence


def test_assess_evidence_reports_missing_paths_in_declared_order() -> None:
    claim = EvidenceClaim(
        name="ranking-law",
        statement="Ranking remains stable.",
        required_paths=("src/ranking.py", "tests/test_ranking.py"),
        command="pytest -q tests/test_ranking.py",
    )

    assessment = assess_evidence(claim, frozenset({"src/ranking.py"}))

    assert assessment.complete is False
    assert assessment.missing_paths == ("tests/test_ranking.py",)


def test_assess_evidence_accepts_an_exact_observation() -> None:
    claim = EvidenceClaim(
        name="ranking-law",
        statement="Ranking remains stable.",
        required_paths=("src/ranking.py", "tests/test_ranking.py"),
        command="pytest -q tests/test_ranking.py",
    )

    assessment = assess_evidence(
        claim,
        frozenset({"src/ranking.py", "tests/test_ranking.py"}),
    )

    assert assessment.complete is True
    assert assessment.missing_paths == ()
