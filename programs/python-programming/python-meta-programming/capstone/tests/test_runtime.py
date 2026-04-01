from __future__ import annotations

from incident_plugins import PluginMeta, build_manifest, invoke
from incident_plugins.plugins import ConsoleNotifier, PagerNotifier, WebhookNotifier


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
