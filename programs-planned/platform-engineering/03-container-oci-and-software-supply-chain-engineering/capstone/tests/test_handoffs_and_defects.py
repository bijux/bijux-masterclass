from __future__ import annotations

import hashlib
import json
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]


def _verify_manifest(directory: Path) -> None:
    manifest = json.loads((directory / "MANIFEST.json").read_text())
    for item in manifest["files"]:
        path = directory / item["path"]
        assert path.is_file()
        assert path.stat().st_size == item["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]


def test_predecessor_and_successor_handoffs_are_exact() -> None:
    _verify_manifest(CAPSTONE / "predecessor")
    _verify_manifest(CAPSTONE / "handoff")


def test_all_ten_planted_defects_name_a_decisive_proof() -> None:
    defects = sorted((CAPSTONE / "planted-defects").glob("*.json"))
    assert len(defects) == 10
    ids = set()
    for path in defects:
        value = json.loads(path.read_text())
        assert value["id"].startswith("C3-DEFECT-")
        assert value["id"] not in ids
        ids.add(value["id"])
        assert value["defect"].strip()
        assert value["expectedProof"].endswith("-proof")
