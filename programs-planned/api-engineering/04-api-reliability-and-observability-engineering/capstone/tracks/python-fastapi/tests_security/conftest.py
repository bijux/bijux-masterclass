from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[4]
VECTORS = COURSE_ROOT / "capstone" / "shared" / "vectors"
IDENTITY = COURSE_ROOT / "capstone" / "identity-provider"
POLICIES = COURSE_ROOT / "capstone" / "security-case" / "policy-matrix.yaml"


def load_vector(name: str):
    return json.loads((VECTORS / name).read_text(encoding="utf-8"))


def load_issuer():
    spec = importlib.util.spec_from_file_location("course_fixture_issuer", IDENTITY / "issuer.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def vector_loader():
    return load_vector
