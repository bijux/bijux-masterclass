# Public API Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  root["service_monitoring package"] --> exports["__init__.py exports"]
  exports --> consumers["Learner or consumer imports"]
  consumers --> proof["Public API proof surface"]
```

```mermaid
flowchart LR
  question["What should another module import?"] --> root["Start at the package root"]
  root --> boundary["Check whether the name is intentionally exported"]
  boundary --> review["Use tests and guides to keep the public surface narrow"]
```
<!-- page-maps:end -->

Use this guide when the capstone starts to feel like a reusable package rather than only
an internal teaching example. The goal is to keep the supported import surface explicit.

## Supported import surface

The local public package surface is `service_monitoring.__init__`. That file intentionally
re-exports the names a learner or downstream consumer should start with before reaching for
deep module imports.

## Best supported imports

| Import need | Start here |
| --- | --- |
| learner-facing application route | `MonitoringApplication`, `RuleRegistration`, `ObservationResult` |
| domain review | `MonitoringPolicy`, `ThresholdRule`, `MetricSample`, `MetricName`, `Severity`, `DomainError` |
| evaluation seam review | `RuleEvaluator`, `ThresholdPolicy`, `ConsecutiveThresholdPolicy`, `RateOfChangePolicy` |
| runtime and repository review | `MonitoringRuntime`, `CollectingIncidentSink`, `StaticMetricSource`, `InMemoryPolicyRepository`, `InMemoryUnitOfWork` |
| shipped fixed scenarios | `build_default_observation`, `build_default_application`, `DEFAULT_POLICY_ID` |

## What should stay internal by default

- deep imports that are only convenient because of current file layout
- local guide assumptions about package internals that are not backed by tests or exported names
- ad hoc imports of helper functions before the package root has been checked

## Best proof surfaces

- `tests/test_public_api.py` for the supported exported names
- `__init__.py` for the intentionally published surface
- [PACKAGE_GUIDE.md](PACKAGE_GUIDE.md) and [SOURCE_GUIDE.md](SOURCE_GUIDE.md) for the internal reading route behind the exports
