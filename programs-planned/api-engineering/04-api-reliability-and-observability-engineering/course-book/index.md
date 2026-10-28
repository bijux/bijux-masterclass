# API Reliability and Observability Engineering

**Course 4 of 6 — Operate and recover the promise**

> **Central question:** How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

## Course responsibility

Detect, diagnose, contain, reconcile, and recover when processes, dependencies, networks, or operators fail. The course inherits earlier guarantees rather than restating them as new work. Its purpose is to add one mature engineering responsibility to the same Analysis Runs Platform.

## Incoming and outgoing boundaries

**Incoming boundary:** The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

**Outgoing boundary:** Reliability Profile 1.0, migration 008, critical journeys, deadlines, resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.

## What you will be able to do

After completing the course, you can:

- create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims.
- implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation.
- add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses.
- implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation.
- create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy.
- implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics.
- implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes.
- publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy.
- design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects.
- run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates.

## Ten-module learning path

| Day | Module | Governing question | Capstone result |
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


## How the book is organized

Each numbered module has five learner-facing files:

1. `index.md` — the complete explanation, worked designs, implementation reading, failure analysis, and transition;
2. `exercises.md` — twelve transfer questions;
3. `exercise-answers.md` — matching reasoned reference answers;
4. `lab.md` — one controlled failure, pressure, or release experiment;
5. `checkpoint.md` — the evidence required before progression.

The course book is authoritative. Capstone source, fixtures, reports, and proof scripts make the material executable; they do not replace the explanation.

## Completion standard

You complete the course only when every module checkpoint, the capstone proof, and the final defense pass. A strong result states not only what worked but which claim was established, which evidence class supports it, and what remains unexecuted.

Continue with [Start here](start-here.md).
