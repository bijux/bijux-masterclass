from __future__ import annotations

import inspect

import pytest

from incident_plugins import PluginBase, PluginMeta, StringField, action


def test_generated_constructor_signature_matches_declared_fields() -> None:
    class SignatureExample(PluginBase):
        plugin_name = "signature-example"
        group = "signatures"

        endpoint = StringField(description="Endpoint", min_length=8)
        channel = StringField(default="critical", description="Channel")

    signature = inspect.signature(SignatureExample)

    assert str(signature) == "(*, endpoint, channel='critical')"


def test_registry_is_deterministic_and_duplicate_names_are_rejected() -> None:
    class AlphaPlugin(PluginBase):
        plugin_name = "alpha"
        group = "registry-check"

    class BetaPlugin(PluginBase):
        plugin_name = "beta"
        group = "registry-check"

    assert PluginMeta.registry("registry-check") == ("alpha", "beta")

    with pytest.raises(ValueError):

        class AlphaDuplicate(PluginBase):
            plugin_name = "alpha"
            group = "registry-check"


def test_action_decorator_preserves_signature_and_wrapped_metadata() -> None:
    class ActionExample(PluginBase):
        plugin_name = "action-example"
        group = "actions"

        @action("Echo the configured value.")
        def echo(self, *, value: str) -> str:
            return value

    signature = inspect.signature(ActionExample.echo)
    result = ActionExample().echo(value="hello")

    assert tuple(signature.parameters) == ("self", "value")
    assert signature.parameters["value"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.return_annotation == "str"
    assert result == "hello"
    assert ActionExample.echo.__wrapped__.__name__ == "echo"
