from __future__ import annotations

import pytest

from incident_plugins import (
    PluginBase,
    PluginMeta,
    action,
    bind_action_arguments,
    build_manifest,
    inspect_action_wrapper,
    invoke,
)
from incident_plugins.plugins import ConsoleNotifier, PagerNotifier, WebhookNotifier
from incident_plugins.scenarios import DEFAULT_DEMO_SCENARIO, DEFAULT_TRACE_SCENARIO


def test_manifest_exposes_schema_and_actions_without_execution() -> None:
    manifest = build_manifest("delivery")

    assert [item["plugin_name"] for item in manifest["delivery"]] == [
        "console",
        "pager",
        "webhook",
    ]
    console = manifest["delivery"][0]
    assert console["fields"][0]["name"] == "prefix"
    assert console["actions"][0]["name"] == "deliver"


def test_manifest_does_not_construct_or_invoke_registered_plugin() -> None:
    runtime_events: list[str] = []

    class ObservationProofPlugin(PluginBase):
        group = "observation-proof"
        plugin_name = "event-recorder"

        def __init__(self) -> None:
            runtime_events.append("constructed")
            self._action_history = []

        @action("Record one deliberately executed event.")
        def deliver(self) -> str:
            runtime_events.append("invoked")
            return "delivered"

    manifest = build_manifest("observation-proof")

    assert manifest["observation-proof"][0]["plugin_name"] == "event-recorder"
    assert manifest["observation-proof"][0]["actions"][0]["name"] == "deliver"
    assert runtime_events == []


def test_action_binding_validates_and_applies_defaults_without_execution() -> None:
    runtime_events: list[str] = []

    class BindingProofPlugin(PluginBase):
        group = "binding-proof"
        plugin_name = "event-recorder"

        def __init__(self) -> None:
            runtime_events.append("constructed")
            self._action_history = []

        @action("Record one deliberately executed event.")
        def deliver(self, title: str, *, severity: str = "warning") -> str:
            runtime_events.append("invoked")
            return f"{severity}:{title}"

    arguments = bind_action_arguments(
        "binding-proof",
        "event-recorder",
        "deliver",
        "CPU high",
    )

    assert arguments == {"title": "CPU high", "severity": "warning"}
    assert runtime_events == []


def test_action_binding_rejects_invalid_calls_before_execution() -> None:
    with pytest.raises(TypeError, match="missing a required argument: 'summary'"):
        bind_action_arguments(
            "delivery",
            "console",
            "deliver",
            title="CPU high",
            severity="warning",
        )


def test_action_wrapper_audit_preserves_execution_boundaries() -> None:
    runtime_events: list[str] = []

    class WrapperAuditPlugin(PluginBase):
        group = "wrapper-audit"
        plugin_name = "event-recorder"

        def __init__(self) -> None:
            runtime_events.append("constructed")
            self._action_history = []

        @action("Record one deliberately executed event.")
        def deliver(self, incident_id: str, *, severity: str = "warning") -> str:
            """Deliver one incident."""

            runtime_events.append("invoked")
            return f"{incident_id}:{severity}"

    audit = inspect_action_wrapper(
        "wrapper-audit",
        "event-recorder",
        "deliver",
    )

    assert audit["constructed"] is False
    assert audit["executed"] is False
    assert audit["wrapper"]["wrapper_depth"] == 1
    assert audit["wrapper"]["visible_signature"] == (
        "(self, incident_id: 'str', *, severity: 'str' = 'warning') -> 'str'"
    )
    assert audit["wrapper"]["chain"][0]["owns_action_spec"] is True
    assert audit["wrapper"]["chain"][0]["owns_explicit_signature"] is True
    assert audit["wrapper"]["chain"][1]["owns_action_spec"] is False
    assert audit["wrapper"]["chain"][1]["owns_explicit_signature"] is False
    assert all(audit["wrapper"]["metadata_preserved"].values())
    assert audit["wrapper"]["action_spec_signature_matches_original"] is True
    assert runtime_events == []


def test_runtime_invocation_returns_structured_payloads() -> None:
    console = invoke(
        "delivery",
        "console",
        "deliver",
        config={"prefix": "[ops]", "uppercase_severity": True},
        title="CPU high",
        severity="warning",
        summary="node-1 crossed 90%",
    )
    webhook = invoke(
        "delivery",
        "webhook",
        "deliver",
        config={"endpoint": "https://hooks.example.com/incidents", "redact_summary": True},
        title="Disk full",
        severity="critical",
        summary="db-3 at 99%",
    )

    assert console == "[ops] WARNING CPU high: node-1 crossed 90%"
    assert webhook["payload"]["summary"] == "[redacted]"


def test_actions_record_invocation_history() -> None:
    pager = PagerNotifier(service="core", routing_key="sev1")
    preview = pager.preview(title="Queue lag", severity="critical", summary="worker backlog growing")

    assert "\"routing_key\": \"sev1\"" in preview
    assert pager.action_history()[-1]["action"] == "preview"


def test_shipped_scenarios_stay_stable() -> None:
    assert DEFAULT_DEMO_SCENARIO.plugin_name == "console"
    assert DEFAULT_DEMO_SCENARIO.action_name == "deliver"
    assert DEFAULT_DEMO_SCENARIO.arguments["severity"] == "warning"

    assert DEFAULT_TRACE_SCENARIO.plugin_name == "pager"
    assert DEFAULT_TRACE_SCENARIO.action_name == "preview"
    assert DEFAULT_TRACE_SCENARIO.config["routing_key"] == "sev1"
