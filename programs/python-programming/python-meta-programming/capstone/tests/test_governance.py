from __future__ import annotations

from incident_plugins import inspect_runtime_governance


def test_governance_report_is_observational() -> None:
    report = inspect_runtime_governance()

    assert report["constructed"] is False
    assert report["executed"] is False
    assert report["scope"] == "incident-plugin runtime"


def test_governance_report_covers_each_shipped_dynamic_owner() -> None:
    report = inspect_runtime_governance()
    mechanisms = [decision["mechanism"] for decision in report["decisions"]]

    assert mechanisms == [
        "action decorators",
        "field descriptors",
        "PluginMeta",
        "process-global plugin registry",
        "runtime introspection CLI",
    ]
    assert [decision["outcome"] for decision in report["decisions"]] == [
        "approve",
        "approve",
        "approve",
        "constrain",
        "approve",
    ]


def test_every_accepted_or_constrained_power_has_rollback_and_proof() -> None:
    report = inspect_runtime_governance()

    for decision in report["decisions"]:
        assert decision["observability"]
        assert decision["rollback"]
        assert decision["proof"]


def test_governance_report_rejects_unowned_runtime_powers() -> None:
    report = inspect_runtime_governance()
    rejected = [item["power"] for item in report["rejected_powers"]]

    assert rejected == [
        "eval or exec for plugin configuration",
        "application monkey patching",
        "application import hooks or AST rewriting",
        "package discovery during class creation",
        "automatic metaclass conflict repair",
    ]
    assert all(item["alternative"] for item in report["rejected_powers"])


def test_governance_report_names_small_and_durable_evidence_routes() -> None:
    report = inspect_runtime_governance()

    assert report["evidence_commands"][:6] == [
        "manifest",
        "field-system",
        "action-wrapper",
        "class-creation",
        "registry",
        "governance",
    ]
    assert len(report["review_gate"]) == 5
