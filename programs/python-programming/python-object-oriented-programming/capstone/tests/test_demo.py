from __future__ import annotations

from service_monitoring.demo import main


def test_demo_route_prints_the_scenario_snapshot(capsys) -> None:
    main()

    output = capsys.readouterr().out
    assert "Monitoring walkthrough" in output
    assert "Stage 1: create policy" in output
    assert "Stage 2: register rules" in output
    assert "Stage 3: activate rules" in output
    assert "Stage 4: observe samples" in output
    assert "Stage 5: inspect derived state" in output
    assert "alerts_published=2" in output
