from __future__ import annotations

from service_monitoring.demo import main


def test_demo_route_prints_the_scenario_snapshot(capsys) -> None:
    main()

    output = capsys.readouterr().out
    assert "Cycle report:" in output
    assert "Policy summary:" in output
    assert "Active rule index:" in output
    assert "Open incidents:" in output
