from incident_escalation_capstone.common import stable_bucket
from incident_escalation_capstone.prepare import build_profile, normalize_row


def test_stable_bucket_is_repeatable() -> None:
    first = stable_bucket("INC-1005", seed=17, modulus=5)
    second = stable_bucket("INC-1005", seed=17, modulus=5)
    assert first == second


def test_normalize_row_enforces_expected_ranges() -> None:
    row = normalize_row(
        {
            "incident_id": "INC-1005",
            "team": "data-platform",
            "backlog_days": "11",
            "reopened_count": "2",
            "integration_touchpoints": "5",
            "customer_tier": "3",
            "weekend_handoff": "1",
            "severity_score": "0.76",
            "escalated": "1",
        }
    )

    assert row["incident_id"] == "INC-1005"
    assert row["severity_score"] == 0.76
    assert row["escalated"] == 1


def test_build_profile_counts_rows_and_teams() -> None:
    rows = [
        {"team": "billing", "escalated": 0},
        {"team": "billing", "escalated": 1},
        {"team": "checkout", "escalated": 1},
    ]

    profile = build_profile(rows, train_rows=rows[:2], eval_rows=rows[2:])
    assert profile["raw_rows"] == 3
    assert profile["escalated_rows"] == 2
    assert profile["teams"] == {"billing": 2, "checkout": 1}
