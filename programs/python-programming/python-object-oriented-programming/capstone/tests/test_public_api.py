from __future__ import annotations

from service_monitoring import (
    CollectingIncidentSink,
    DomainError,
    MonitoringApplication,
    MonitoringRuntime,
    RateOfChangePolicy,
    RuleEvaluator,
    RuleRegistration,
    ThresholdRule,
    __all__,
)


def test_public_api_exports_the_supported_entry_surface() -> None:
    expected_names = {
        "CollectingIncidentSink",
        "DomainError",
        "MonitoringApplication",
        "MonitoringRuntime",
        "RateOfChangePolicy",
        "RuleEvaluator",
        "RuleRegistration",
        "ThresholdRule",
    }

    assert expected_names.issubset(set(__all__))


def test_public_api_supports_top_level_imports_for_common_review_paths() -> None:
    assert MonitoringApplication is not None
    assert MonitoringRuntime is not None
    assert RuleRegistration is not None
    assert ThresholdRule is not None
    assert RuleEvaluator is not None
    assert RateOfChangePolicy is not None
    assert CollectingIncidentSink is not None
    assert DomainError is not None
