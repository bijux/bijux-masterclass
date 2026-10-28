from __future__ import annotations

import os

import pytest

from scripts.run_live_conformance import run


@pytest.mark.live
def test_running_provider_matches_shared_behavioral_contract() -> None:
    base_url = os.environ.get("OACE_BASE_URL")
    if not base_url:
        pytest.skip("set OACE_BASE_URL to a clean running provider")
    payload = run(base_url, os.environ.get("OACE_PROVIDER", "unknown"))
    assert payload["passed"] is True
