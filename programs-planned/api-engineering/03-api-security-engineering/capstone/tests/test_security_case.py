from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "capstone" / "security-case"


def test_every_requirement_has_a_proof():
    requirements = {x["id"] for x in yaml.safe_load((CASE / "requirements.yaml").read_text())["requirements"]}
    proofs = {x["requirement"] for x in yaml.safe_load((CASE / "proof-map.yaml").read_text())["proofs"]}
    assert requirements == proofs


def test_every_operation_has_one_policy():
    policies = yaml.safe_load((CASE / "policy-matrix.yaml").read_text())["policies"]
    operation_ids = [x["operationId"] for x in policies]
    assert len(operation_ids) == len(set(operation_ids)) == 20
