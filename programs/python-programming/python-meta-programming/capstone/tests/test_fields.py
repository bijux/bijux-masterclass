from __future__ import annotations

import pytest

from incident_plugins import (
    ChoiceField,
    IntegerField,
    PluginBase,
    StringField,
    inspect_field_ownership,
)


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


def test_field_ownership_exposes_descriptor_and_storage_boundaries() -> None:
    report = inspect_field_ownership("examples", "example", "endpoint")

    assert report == {
        "group": "examples",
        "plugin_name": "example",
        "field_name": "endpoint",
        "declaring_class": "ExamplePlugin",
        "descriptor_type": "StringField",
        "descriptor_kind": "data",
        "hooks": ["__get__", "__set__", "__set_name__"],
        "public_name": "endpoint",
        "storage_name": "_endpoint",
        "storage_owner": "plugin-instance.__dict__",
        "class_access_returns_descriptor": True,
        "collected_by_metaclass": True,
        "field": {
            "name": "endpoint",
            "kind": "string",
            "description": "Endpoint",
            "required": True,
            "default": None,
            "choices": None,
            "minimum": 8,
            "maximum": None,
        },
        "constructed": False,
        "executed": False,
    }
