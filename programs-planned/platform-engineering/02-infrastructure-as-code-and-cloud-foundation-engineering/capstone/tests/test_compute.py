from __future__ import annotations

import json
from pathlib import Path

from cloud_model.compute import (
    replacement_capacity,
    validate_image_release,
    validate_launch_contract,
)

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_safe_image_and_launch() -> None:
    image = load("fixtures/compute/image-release-v1.json")
    launch = load("fixtures/compute/launch-template-v1.json")
    assert validate_image_release(image) == []
    assert validate_launch_contract(launch, image) == []


def test_secret_and_latest_bootstrap_rejected() -> None:
    image = load("fixtures/compute/image-release-v1.json")
    errors = validate_launch_contract(load("fixtures/compute/bad-bootstrap-secret.json"), image)
    assert any("secret-like" in error for error in errors)
    assert any("mutable latest" in error for error in errors)


def test_mutable_image_rejected() -> None:
    errors = validate_image_release(load("fixtures/compute/mutable-latest-image.json"))
    assert any("mutable alias" in error for error in errors)


def test_replacement_capacity_requires_overlap() -> None:
    insufficient = replacement_capacity(current_instances=1, desired_instances=1, create_before_destroy=True, quota=1)
    sufficient = replacement_capacity(current_instances=1, desired_instances=1, create_before_destroy=True, quota=2)
    assert insufficient["sufficient"] is False
    assert sufficient["sufficient"] is True
