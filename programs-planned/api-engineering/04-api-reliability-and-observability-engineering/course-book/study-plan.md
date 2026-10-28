# Two-Week Study Plan — API Reliability and Observability Engineering

## Rhythm

Course 4 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the observe, diagnose, contain, and recover the promise model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Reliability Model and Critical Journeys](module-01-reliability-model-and-critical-journeys/index.md) | Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims. |
| 2 | [Deadlines, Cancellation, and Retry Budgets](module-02-deadlines-timeouts-cancellation-and-retry-budgets/index.md) | Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation. |
| 3 | [Dependency Resilience and Graceful Degradation](module-03-dependency-resilience-and-graceful-degradation/index.md) | Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses. |
| 4 | [Lifecycle, Health, Shutdown, and Recovery](module-04-lifecycle-health-graceful-shutdown-and-recovery/index.md) | Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation. |
| 5 | [Telemetry Architecture and Structured Events](module-05-telemetry-architecture-and-structured-operational-events/index.md) | Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy. |
| 6 | [Metrics and Service-Level Indicators](module-06-metrics-and-service-level-indicators/index.md) | Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics. |
| 7 | [Distributed Tracing Across Asynchronous Work](module-07-distributed-tracing-across-http-workers-storage-and-webhooks/index.md) | Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes. |
| 8 | [SLOs, Error Budgets, Dashboards, and Alerts](module-08-slos-error-budgets-dashboards-and-alerts/index.md) | Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy. |
| 9 | [Fault Injection, Troubleshooting, and Game Days](module-09-fault-injection-troubleshooting-and-game-days/index.md) | Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects. |
| 10 | [Incident Command, Reconciliation, and Readiness](module-10-incident-command-state-reconciliation-and-operational-readiness/index.md) | Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates. |

## Suggested day

```text
08:30  retrieval practice and checkpoint repair
09:00  chapter reading and diagram reconstruction
11:00  worked examples and standards review
13:00  primary-track implementation reading
15:00  exercises before answers
17:00  controlled lab
19:30  evidence package and checkpoint defense
```

The two-week schedule is subordinate to evidence. If the observe, diagnose, contain, and recover the promise argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007. Rerun those checkpoints and postpone every feature that does not serve the Course 4 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
