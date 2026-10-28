from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "capstone" / "handoff"


def test_handoff_contains_no_private_key_or_fixture_pepper():
    for path in HANDOFF.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert "PRIVATE KEY" not in text
        assert "fixture-pepper" not in text
