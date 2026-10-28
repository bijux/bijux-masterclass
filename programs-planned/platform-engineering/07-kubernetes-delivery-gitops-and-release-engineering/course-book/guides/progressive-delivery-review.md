# Guide — Progressive delivery review

A progressive-release proposal is acceptable only when it defines candidate identity, stable identity, actual traffic population, analysis signals, minimum samples, observation delay, segment coverage, missing-data outcome, data compatibility, and abort behavior.

Review configured traffic weights and the router's observed distribution separately. Ensure the analysis query measures useful outcomes rather than only infrastructure health. Require absolute thresholds in addition to candidate-versus-stable comparison.

Document the rollback frontier. If the candidate writes data the stable revision cannot read, traffic rollback is not a safe recovery. Test abort before production and prove how Git desired state becomes consistent with the emergency routing action.

## Extended reader notes

Begin with a failure hypothesis and affected population. Define stable and candidate subjects, actual exposure measurement, minimum samples, analysis delay, absolute and relative thresholds, segment coverage, missing-data outcome, and abort procedure. Check the data compatibility phase before exposing traffic.

During execution, compare configured and observed traffic. Preserve raw metric queries and results. Force one failing segment while aggregate success remains high; the gate must fail. Force telemetry absence; the gate must become unavailable or inconclusive, never a silent pass.

Abort both the router and desired-state selection, then verify candidate side effects and data remain compatible. Record whether the incident used revert or forward fix.
