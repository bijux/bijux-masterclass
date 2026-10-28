from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from analysis_service.models import (
    AnalysisRunCreate,
    AnalysisRunV12,
    ProjectCreate,
    ProjectPatch,
    RemoteObjectSource,
)


def test_optional_nonnullable_fields_reject_explicit_null() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate.model_validate({"name": "A", "description": None})
    with pytest.raises(ValidationError):
        ProjectPatch.model_validate({"name": None})
    with pytest.raises(ValidationError):
        RemoteObjectSource.model_validate(
            {
                "kind": "remote-object",
                "uri": "https://objects.example.test/a.csv",
                "checksumSha256": None,
            }
        )
    with pytest.raises(ValidationError):
        AnalysisRunCreate.model_validate(
            {
                "projectId": "prj_0001",
                "datasetId": "dts_0001",
                "parameters": {"algorithm": "checksum"},
                "callbackUrl": None,
            }
        )


def test_nullable_patch_description_accepts_null() -> None:
    assert ProjectPatch.model_validate({"description": None}).description is None


def test_api_1_2_model_tolerates_old_row_during_coexistence() -> None:
    now = datetime.now(timezone.utc)
    run = AnalysisRunV12.model_validate(
        {
            "id": "run_0001",
            "projectId": "prj_0001",
            "datasetId": "dts_0001",
            "ownerId": "learner",
            "status": "queued",
            "parameters": {"algorithm": "checksum"},
            "progress": 0,
            "createdAt": now,
            "updatedAt": now,
            "completedAt": None,
            "artifactIds": [],
        }
    )
    assert run.result_summary is None
    assert run.model_dump(by_alias=True)["resultSummary"] is None
