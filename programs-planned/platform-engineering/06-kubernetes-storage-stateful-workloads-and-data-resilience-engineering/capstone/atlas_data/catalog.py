from __future__ import annotations

from dataclasses import asdict
from .models import DataClass, FailureDomain


def atlas_catalog() -> dict[str, DataClass]:
    items = [
        DataClass("run-state", True, FailureDomain.REGION, 60, 900, 1),
        DataClass("artifacts", True, FailureDomain.REGION, 300, 1800, 1),
        DataClass("worker-scratch", False, FailureDomain.POD, 0, 60, 0),
        DataClass("read-cache", False, FailureDomain.POD, 0, 60, 0),
        DataClass("recovery-evidence", True, FailureDomain.ACCOUNT, 3600, 3600, 1),
    ]
    for item in items:
        item.validate()
    return {item.name: item for item in items}


def catalogue_document() -> dict[str, object]:
    return {
        "schemaVersion": "1.0",
        "dataClasses": [
            {**asdict(item), "maximum_loss": item.maximum_loss.value}
            for item in atlas_catalog().values()
        ],
    }
