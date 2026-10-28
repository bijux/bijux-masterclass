from __future__ import annotations

import json
from pathlib import Path

from cloud_model.module_api import compare_module_versions, validate_module_interface
from cloud_model.organization import validate_organization

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_good_module_interface() -> None:
    assert validate_module_interface(load("fixtures/modules/network-v1.json")) == []


def test_bad_module_owns_provider_and_remote_state() -> None:
    errors = validate_module_interface(load("fixtures/modules/network-bad.json"))
    assert any("provider" in error for error in errors)
    assert any("remote state" in error for error in errors)
    assert any("material default" in error for error in errors)


def test_additive_module_version() -> None:
    result = compare_module_versions(
        load("fixtures/modules/network-v1.json"),
        load("fixtures/modules/network-v2.json"),
    )
    assert not result["breaking"]
    assert "new optional input: enable_s3_endpoint" in result["additive"]


def test_organization_model_is_sound() -> None:
    assert validate_organization(load("fixtures/organization/organization-small.json")) == []


def test_management_workload_rejected() -> None:
    errors = validate_organization(load("fixtures/organization/bad-management-workload.json"))
    assert any("management account" in error for error in errors)
