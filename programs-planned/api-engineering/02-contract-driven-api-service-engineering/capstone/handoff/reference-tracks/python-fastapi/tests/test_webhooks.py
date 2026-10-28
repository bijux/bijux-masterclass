from __future__ import annotations

import pytest

from analysis_service.failures import ServiceError
from analysis_service.webhooks import parse_destination


@pytest.mark.parametrize(
    "value",
    [
        "https://hooks.example.test/analysis-complete",
        "https://hooks.example.test:443/path?tenant=learner",
    ],
)
def test_approved_webhook_destinations(value: str) -> None:
    assert parse_destination(value).hostname == "hooks.example.test"


@pytest.mark.parametrize(
    "value",
    [
        "http://hooks.example.test/path",
        "https://user@hooks.example.test/path",
        "https://hooks.example.test:444/path",
        "https://hooks.example.test:invalid/path",
        "https://hooks.example.test/path#fragment",
        "https://evil.example.test/path",
    ],
)
def test_rejected_webhook_destinations_are_validation_errors(value: str) -> None:
    with pytest.raises(ServiceError) as captured:
        parse_destination(value)
    assert captured.value.status == 422
    assert captured.value.code == "validation"
