from incident_escalation_capstone.fit import fit_model, sigmoid


def test_sigmoid_stays_in_probability_range() -> None:
    assert 0.0 < sigmoid(-10.0) < 1.0
    assert 0.0 < sigmoid(10.0) < 1.0


def test_fit_model_learns_positive_weight_for_separable_signal() -> None:
    rows = [
        {"escalated": 0, "features": {"backlog_days": -1.0, "reopened_count": -1.0, "integration_touchpoints": -1.0, "customer_tier": -1.0, "weekend_handoff": -1.0, "severity_score": -1.0}},
        {"escalated": 0, "features": {"backlog_days": -0.8, "reopened_count": -0.9, "integration_touchpoints": -0.8, "customer_tier": -0.8, "weekend_handoff": -0.9, "severity_score": -0.7}},
        {"escalated": 1, "features": {"backlog_days": 0.8, "reopened_count": 0.9, "integration_touchpoints": 0.8, "customer_tier": 0.9, "weekend_handoff": 0.7, "severity_score": 0.9}},
        {"escalated": 1, "features": {"backlog_days": 1.0, "reopened_count": 1.0, "integration_touchpoints": 1.0, "customer_tier": 1.0, "weekend_handoff": 0.9, "severity_score": 1.0}},
    ]

    _, weights, loss = fit_model(rows, learning_rate=0.2, iterations=400, l2=0.01)
    assert weights["severity_score"] > 0
    assert loss < 0.5
