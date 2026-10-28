# API Reliability and Observability Engineering

**Course 4 of 10 — Observe, diagnose, contain, and recover the promise**

## Course promise

Make failures observable and recoverable through explicit budgets, lifecycle states, telemetry meaning, service-level objectives, fault experiments, and reconciliation.

> **Governing question:** How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

## Place in the program

**Incoming boundary:** The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

**Outgoing boundary:** Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.

Course 4 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the observe, diagnose, contain, and recover the promise mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- critical-journey reliability models;
- deadlines, cancellation, retries, circuits, and bulkheads;
- health, draining, shutdown, startup recovery, and reconciliation;
- structured events, metrics, traces, SLOs, alerts, and runbooks;
- fault injection, game days, incident command, and repair evidence;

## Course-level learning outcomes

- Define critical journeys and eligible event populations.
- Distinguish absolute deadlines from per-call timeouts.
- Classify dependency failures and ownership.
- Separate startup, liveness, and readiness.
- Separate logs, metrics, traces, and audit records by purpose.
- Choose metric instruments from the measured quantity.
- Parse and validate W3C trace context.
- Choose objectives from critical journeys.
- Predict the failure and first oracle before injection.
- Assign incident command, operations, communication, and recording roles.

## Module map

| Day | Chapter | Governing question | Capstone increment |
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

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- claiming telemetry is authoritative business state;
- full capacity engineering;
- vendor-specific observability operations;
- multi-region disaster recovery;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 4, read each chapter around the question **How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
