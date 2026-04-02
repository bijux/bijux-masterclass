from __future__ import annotations

from incident_plugins import (
    ActionSpec,
    ChoiceField,
    ConsoleNotifier,
    Field,
    PagerNotifier,
    PluginBase,
    PluginMeta,
    WebhookNotifier,
    action,
    build_manifest,
    create_plugin,
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
    assert action is not None


def test_public_api_exports_concrete_plugins_for_review_routes() -> None:
    assert ConsoleNotifier.plugin_name == "console"
    assert WebhookNotifier.plugin_name == "webhook"
    assert PagerNotifier.plugin_name == "pager"
