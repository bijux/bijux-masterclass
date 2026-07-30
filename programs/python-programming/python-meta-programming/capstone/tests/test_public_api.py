from __future__ import annotations

from incident_plugins import (
    ActionSpec,
    ClassCreationSpec,
    ChoiceField,
    ConsoleNotifier,
    Field,
    PagerNotifier,
    PluginBase,
    PluginMeta,
    WebhookNotifier,
    action,
    bind_action_arguments,
    build_manifest,
    check_action_arguments,
    create_plugin,
    inspect_action_wrapper,
    inspect_field_ownership,
    inspect_field_system,
    inspect_plugin_class_creation,
    invoke,
)


def test_public_api_exports_the_supported_framework_surface() -> None:
    assert PluginBase is not None
    assert PluginMeta is not None
    assert build_manifest is not None
    assert create_plugin is not None
    assert invoke is not None
    assert Field is not None
    assert ChoiceField is not None
    assert ActionSpec is not None
    assert ClassCreationSpec is not None
    assert action is not None
    assert bind_action_arguments is not None
    assert check_action_arguments is not None
    assert inspect_action_wrapper is not None
    assert inspect_field_ownership is not None
    assert inspect_field_system is not None
    assert inspect_plugin_class_creation is not None


def test_public_api_exports_concrete_plugins_for_review_routes() -> None:
    assert ConsoleNotifier.plugin_name == "console"
    assert WebhookNotifier.plugin_name == "webhook"
    assert PagerNotifier.plugin_name == "pager"
