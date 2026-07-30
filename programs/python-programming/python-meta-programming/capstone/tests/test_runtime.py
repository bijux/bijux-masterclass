from __future__ import annotations

import pytest

from incident_plugins import (
    PluginBase,
    PluginMeta,
    StringField,
    action,
    bind_action_arguments,
    build_manifest,
    check_action_arguments,
    inspect_action_wrapper,
    inspect_plugin_class_creation,
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


def test_action_contract_checks_supported_hints_without_execution() -> None:
    runtime_events: list[str] = []

    class ContractProofPlugin(PluginBase):
        group = "contract-proof"
        plugin_name = "event-recorder"

        def __init__(self) -> None:
            runtime_events.append("constructed")
            self._action_history = []

        @action("Record one deliberately executed event.")
        def deliver(self, incident_id: str, *, attempts: int = 1) -> str:
            runtime_events.append("invoked")
            return f"{incident_id}:{attempts}"

    report = check_action_arguments(
        "contract-proof",
        "event-recorder",
        "deliver",
        "INC-42",
    )

    assert report["bound_arguments"] == {"incident_id": "INC-42", "attempts": 1}
    assert report["checked"] == [
        {
            "name": "incident_id",
            "annotation": "str",
            "actual_type": "str",
            "matches": True,
        },
        {
            "name": "attempts",
            "annotation": "int",
            "actual_type": "int",
            "matches": True,
        },
    ]
    assert report["accepted"] is True
    assert report["contract_complete"] is True
    assert report["constructed"] is False
    assert report["executed"] is False
    assert runtime_events == []


def test_action_contract_reports_mismatch_and_unsupported_hints() -> None:
    class PartialContractPlugin(PluginBase):
        group = "partial-contract"
        plugin_name = "partial"

        @action("Expose partial contract behavior.")
        def deliver(
            self,
            incident_id: str,
            tags: list[str],
            context,
        ) -> str:
            return incident_id

    report = check_action_arguments(
        "partial-contract",
        "partial",
        "deliver",
        42,
        ["urgent"],
        "manual",
    )

    assert report["checked"] == [
        {
            "name": "incident_id",
            "annotation": "str",
            "actual_type": "int",
            "matches": False,
        }
    ]
    assert report["refused"] == [
        {
            "name": "tags",
            "annotation": "list[str]",
            "reason": "annotation is outside the supported runtime subset",
        }
    ]
    assert report["unchecked"] == [{"name": "context", "reason": "no annotation"}]
    assert report["contract_complete"] is False
    assert report["accepted"] is False


def test_action_contract_defers_and_reports_unresolved_forward_references() -> None:
    class ForwardReferencePlugin(PluginBase):
        group = "forward-reference"
        plugin_name = "unresolved"

        @action("Keep ordinary registration independent of optional hint checks.")
        def deliver(self, incident: MissingIncidentType) -> str:  # type: ignore[name-defined]
            return str(incident)

    assert bind_action_arguments(
        "forward-reference",
        "unresolved",
        "deliver",
        "INC-42",
    ) == {"incident": "INC-42"}

    report = check_action_arguments(
        "forward-reference",
        "unresolved",
        "deliver",
        "INC-42",
    )

    assert report["checked"] == []
    assert report["refused"] == []
    assert report["unchecked"] == [
        {"name": "incident", "reason": "annotation resolution failed"}
    ]
    assert report["resolution_error"].startswith("NameError:")
    assert "MissingIncidentType" in report["resolution_error"]
    assert report["contract_complete"] is False
    assert report["accepted"] is False


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


def test_action_wrapper_preserves_failures_and_records_only_success() -> None:
    failure = RuntimeError("delivery failed")

    class OutcomePolicyPlugin(PluginBase):
        group = "wrapper-outcome"
        plugin_name = "outcome-policy"

        @action("Deliver or expose the original failure.")
        def deliver(self, *, should_fail: bool) -> str:
            if should_fail:
                raise failure
            return "delivered"

    plugin = OutcomePolicyPlugin()

    with pytest.raises(RuntimeError) as caught:
        plugin.deliver(should_fail=True)

    assert caught.value is failure
    assert plugin.action_history() == []

    result = plugin.deliver(should_fail=False)

    assert result == "delivered"
    assert plugin.action_history() == [
        {
            "action": "deliver",
            "arguments": {"should_fail": False},
            "result_type": "str",
        }
    ]


def test_class_creation_audit_separates_inherited_declared_and_generated_surfaces() -> None:
    class AuditedDeliveryBase(PluginBase):
        __abstract__ = True
        group = "class-creation-proof"

        base_endpoint = StringField(description="Inherited endpoint")

        @action("Inherited action.")
        def inspect(self) -> str:
            return self.base_endpoint

    class AuditedDelivery(AuditedDeliveryBase):
        plugin_name = "audited"

        channel = StringField(default="critical", description="Declared channel")

        @action("Declared action.")
        def deliver(self) -> str:
            return self.channel

    report = inspect_plugin_class_creation("class-creation-proof", "audited")

    assert report["class_creation"] == {
        "namespace_type": "DefinitionNamespace",
        "metaclass": "PluginMeta",
        "base_classes": ("AuditedDeliveryBase",),
        "namespace_names": ("plugin_name", "channel", "deliver"),
        "declared_fields": ("channel",),
        "declared_actions": ("deliver",),
        "inherited_fields": ("base_endpoint",),
        "inherited_actions": ("inspect",),
        "generated_init": True,
        "abstract": False,
        "hook_trace": (
            "prepare:DefinitionNamespace",
            "body:complete",
            "new:shape",
            "init:register",
        ),
    }
    assert report["metaclass_selection"] == "inherited from base class"
    assert report["hook_ownership"]["new"].startswith("collect fields")
    assert report["hook_ownership"]["init"] == "register the finished concrete class"
    assert report["accepted_powers"] == [
        "declaration-time duplicate tracking",
        "field and action collection",
        "constructor signature and initializer generation",
        "automatic in-process concrete subclass registration",
    ]
    assert [item["power"] for item in report["rejected_powers"]] == [
        "package discovery",
        "external I/O during class creation",
        "automatic metaclass conflict resolution",
        "reload reconciliation",
    ]
    assert report["visible_signature"] == "(*, base_endpoint, channel='critical')"
    assert report["collected_fields"] == ["base_endpoint", "channel"]
    assert report["collected_actions"] == ["inspect", "deliver"]
    assert report["registered"] is True
    assert report["constructed"] is False
    assert report["executed"] is False


def test_class_creation_audit_records_an_explicit_initializer() -> None:
    runtime_events: list[str] = []

    class ExplicitInitializerPlugin(PluginBase):
        group = "class-creation-proof"
        plugin_name = "explicit-initializer"

        def __init__(self) -> None:
            runtime_events.append("constructed")
            self._action_history = []

    report = inspect_plugin_class_creation(
        "class-creation-proof",
        "explicit-initializer",
    )

    assert report["class_creation"]["generated_init"] is False
    assert report["class_creation"]["hook_trace"][-1] == "init:register"
    assert report["constructed"] is False
    assert runtime_events == []


def test_definition_namespace_rejects_duplicate_tracked_declarations() -> None:
    with pytest.raises(
        TypeError,
        match="duplicate tracked definition for 'endpoint'",
    ):

        class DuplicateFieldPlugin(PluginBase):
            group = "class-creation-proof"
            plugin_name = "duplicate-field"

            endpoint = StringField(description="First endpoint")
            endpoint = StringField(description="Second endpoint")

    assert "duplicate-field" not in PluginMeta.registry("class-creation-proof")


def test_definition_namespace_allows_ordinary_helper_replacement() -> None:
    class ReplacedHelperPlugin(PluginBase):
        group = "class-creation-proof"
        plugin_name = "replaced-helper"

        helper = "first"
        helper = "second"

    report = inspect_plugin_class_creation(
        "class-creation-proof",
        "replaced-helper",
    )

    assert ReplacedHelperPlugin.helper == "second"
    assert report["class_creation"]["namespace_names"] == (
        "group",
        "plugin_name",
        "helper",
    )


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
