from __future__ import annotations

from service_monitoring.cli import main


def test_summary_command_reports_policy_and_incident_state(capsys) -> None:
    assert main(["summary"]) == 0

    output = capsys.readouterr().out
    assert "policy_id: service-monitoring" in output
    assert "alerts_published: 2" in output
    assert "open_incidents: cpu-hot, cpu-sustained" in output


def test_rules_command_reports_rule_lifecycle_state(capsys) -> None:
    assert main(["rules"]) == 0

    output = capsys.readouterr().out
    assert "draft_rules: (none)" in output
    assert "active_rules: cpu-hot, cpu-sustained" in output
    assert "retired_rules: (none)" in output
    assert "rule_details:" in output
    assert "cpu-hot state=active metric=cpu mode=threshold threshold=0.9 window=1 severity=critical" in output
    assert (
        "cpu-sustained state=active metric=cpu mode=consecutive threshold=0.8 window=3 severity=warning"
        in output
    )


def test_history_command_reports_metric_history(capsys) -> None:
    assert main(["history"]) == 0

    output = capsys.readouterr().out
    assert "metric: cpu" in output
    assert "cpu-hot -> critical observed=0.95 threshold=0.9" in output
    assert "cpu-sustained -> warning observed=0.95 threshold=0.8" in output


def test_timeline_command_reports_the_ordered_scenario_flow(capsys) -> None:
    assert main(["timeline"]) == 0

    output = capsys.readouterr().out
    assert "step: register rules" in output
    assert "step: activate rules" in output
    assert "step: observe samples" in output
    assert "step: published alerts" in output
    assert "cpu-hot mode=threshold threshold=0.9 window=1" in output
    assert "cpu  cpu-hot" not in output
    assert "cpu cpu-hot -> critical observed=0.95 threshold=0.9" in output


def test_retirement_command_reports_before_and_after_state(capsys) -> None:
    assert main(["retirement"]) == 0

    output = capsys.readouterr().out
    assert "before_retirement:" in output
    assert "after_retirement:" in output
    assert "open_incidents=['disk-hot']" in output
    assert "retired_rules=disk-hot" in output
    assert "open_incidents=[]" in output
    assert "retirement_reason=replaced by storage saturation policy" in output


def test_rate_of_change_command_reports_the_alternate_mode(capsys) -> None:
    assert main(["rate-of-change"]) == 0

    output = capsys.readouterr().out
    assert "policy_id: service-monitoring-rate-of-change" in output
    assert "rule_mode: rate_of_change" in output
    assert "alerts_published: 1" in output
    assert "open_incidents: ['latency-spike']" in output
    assert "observed_value=0.26" in output
