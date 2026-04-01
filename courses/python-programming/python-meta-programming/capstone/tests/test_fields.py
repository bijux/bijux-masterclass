from __future__ import annotations

import pytest

from incident_plugins import ChoiceField, IntegerField, PluginBase, StringField


class ExamplePlugin(PluginBase):
    plugin_name = "example"
    group = "examples"

    endpoint = StringField(description="Endpoint", min_length=8)
    stream = ChoiceField("stdout", "stderr", default="stdout", description="Output stream")
    retries = IntegerField(default=3, description="Retry budget", minimum=0, maximum=10)


def test_descriptor_fields_validate_and_coerce_per_instance() -> None:
    first = ExamplePlugin(endpoint="https://api.example.com")
    second = ExamplePlugin(endpoint="https://other.example.com", retries="4")

    assert first.endpoint == "https://api.example.com"
    assert first.stream == "stdout"
    assert first.retries == 3
    assert second.retries == 4


def test_descriptor_fields_reject_invalid_values() -> None:
    with pytest.raises(ValueError):
        ExamplePlugin(endpoint="short")

    with pytest.raises(ValueError):
        ExamplePlugin(endpoint="https://api.example.com", stream="console")

    with pytest.raises(ValueError):
        ExamplePlugin(endpoint="https://api.example.com", retries=99)
