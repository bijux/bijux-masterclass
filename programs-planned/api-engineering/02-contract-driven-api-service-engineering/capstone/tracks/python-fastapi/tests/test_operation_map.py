from __future__ import annotations

import re
from pathlib import Path

import yaml


def test_python_provider_owns_every_frozen_operation() -> None:
    capstone = Path(__file__).parents[3]
    operation_map = yaml.safe_load(
        (capstone / "shared" / "operation-map.yaml").read_text(
            encoding="utf-8"
        )
    )["operations"]
    application_source = (
        Path(__file__).parents[1] / "src" / "analysis_service" / "app.py"
    ).read_text(encoding="utf-8")
    owned = set(
        re.findall(
            r"operation_id=['\"]([A-Za-z0-9]+)",
            application_source,
        )
    )

    missing = sorted(set(operation_map) - owned)
    assert not missing, f"Python provider is missing operation owners: {missing}"
