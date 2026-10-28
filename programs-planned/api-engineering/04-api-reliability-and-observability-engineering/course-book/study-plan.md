# Ten-Day Study Plan — API Reliability and Observability Engineering

This is a dense two-week course with one numbered module per weekday. Orientation is required before Day 1 and is not counted as a teaching module. The middle weekend contains no hidden new curriculum.

| Day | Module | Main intellectual move | Required result |
|---:|---|---|---|
| 1 | [Reliability Model and Critical Journeys](module-01-reliability-model-and-critical-journeys/index.md) | Which user journeys matter, what makes them good or bad, and which durable facts establish the outcome? | Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims. |
| 2 | [Deadlines, Cancellation, and Retry Budgets](module-02-deadlines-timeouts-cancellation-and-retry-budgets/index.md) | How is one absolute time budget propagated through retries, dependencies, and cancellation without multiplying work? | Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation. |
| 3 | [Dependency Resilience and Graceful Degradation](module-03-dependency-resilience-and-graceful-degradation/index.md) | How should circuits, bulkheads, and degradation be scoped so they contain rather than hide dependency failure? | Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses. |
| 4 | [Lifecycle, Health, Shutdown, and Recovery](module-04-lifecycle-health-graceful-shutdown-and-recovery/index.md) | How do APIs, workers, and dispatchers start, become ready, drain, stop, and recover without losing accepted work? | Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation. |
| 5 | [Telemetry Architecture and Structured Events](module-05-telemetry-architecture-and-structured-operational-events/index.md) | Which operational events are useful, bounded, redacted, versioned, and clearly separated from business truth? | Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy. |
| 6 | [Metrics and Service-Level Indicators](module-06-metrics-and-service-level-indicators/index.md) | How are counters, gauges, histograms, and SLI populations defined so the math means what operators think it means? | Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics. |
| 7 | [Distributed Tracing Across Asynchronous Work](module-07-distributed-tracing-across-http-workers-storage-and-webhooks/index.md) | How does trace context cross HTTP, queues, workers, storage, retries, and webhooks without inventing false parentage? | Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes. |
| 8 | [SLOs, Error Budgets, Dashboards, and Alerts](module-08-slos-error-budgets-dashboards-and-alerts/index.md) | How do versioned SLOs, exact error budgets, burn rates, dashboards, alerts, and runbooks drive decisions? | Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy. |
| 9 | [Fault Injection, Troubleshooting, and Game Days](module-09-fault-injection-troubleshooting-and-game-days/index.md) | How can fault injection and game days produce falsifiable evidence without creating uncontrolled damage? | Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects. |
| 10 | [Incident Command, Reconciliation, and Readiness](module-10-incident-command-state-reconciliation-and-operational-readiness/index.md) | How do responders command an incident, reconcile durable state, repair safely, and decide whether a release is operationally ready? | Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates. |


## Daily rhythm

A productive day uses four blocks:

- **Model:** read the chapter and reconstruct the governing diagram or state machine;
- **Transfer:** answer the exercises and compare with the reasoned answers;
- **Experiment:** perform the lab, including the failure or pressure condition;
- **Defense:** complete the checkpoint and preserve evidence.

Do not treat “morning to night” as uninterrupted screen time. Use deliberate breaks. Stop blind copying when fatigue removes your ability to predict outcomes.

## Middle weekend

Use Saturday for at most one focused repair cycle per failed checkpoint and for a cross-module synthesis note. Sunday contains no required implementation. Rerun predecessor and accumulated course proofs before Week 2.

## Recovery rule

When behind, reduce breadth before reducing evidence. Complete one language track deeply, keep the comparison focused, and do not skip the failure experiment. A copied second implementation is less valuable than one defended invariant.
