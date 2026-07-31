from __future__ import annotations

import pytest

from incident_plugins import (
    ChoiceField,
    IntegerField,
    PluginBase,
    StringField,
    inspect_field_ownership,
    inspect_field_system,
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


def test_field_system_exposes_accepted_and_rejected_powers() -> None:
    report = inspect_field_system("examples", "example")

    assert report["class_name"] == "ExamplePlugin"
    assert report["fields"] == [
        {
            "name": "endpoint",
            "descriptor_type": "StringField",
            "coercion_owner": "StringField",
            "storage_name": "_endpoint",
            "source_of_truth": "plugin-instance.__dict__",
        },
        {
            "name": "stream",
            "descriptor_type": "ChoiceField",
            "coercion_owner": "ChoiceField",
            "storage_name": "_stream",
            "source_of_truth": "plugin-instance.__dict__",
        },
        {
            "name": "retries",
            "descriptor_type": "IntegerField",
            "coercion_owner": "IntegerField",
            "storage_name": "_retries",
            "source_of_truth": "plugin-instance.__dict__",
        },
    ]
    assert [item["power"] for item in report["accepted_powers"]] == [
        "assignment coercion and validation",
        "per-instance configuration storage",
        "field collection and constructor generation",
        "public field schema",
    ]
    assert [item["power"] for item in report["rejected_powers"]] == [
        "derived-value caching",
        "external storage during attribute access",
        "field wrapper composition",
        "annotation-inferred field policy",
        "cross-field transactions",
    ]
    assert report["constructed"] is False
    assert report["executed"] is False
