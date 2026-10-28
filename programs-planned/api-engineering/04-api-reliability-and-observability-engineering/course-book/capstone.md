# Capstone — API Reliability and Observability Engineering

## Cumulative system

Course 4 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to observe, diagnose, contain, and recover the promise while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

The inherited boundary is read-only: The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- critical-journey reliability models;
- deadlines, cancellation, retries, circuits, and bulkheads;
- health, draining, shutdown, startup recovery, and reconciliation;
- structured events, metrics, traces, SLOs, alerts, and runbooks;
- fault injection, game days, incident command, and repair evidence;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Reliability Model and Critical Journeys | Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims. |
| 2 | Deadlines, Cancellation, and Retry Budgets | Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation. |
| 3 | Dependency Resilience and Graceful Degradation | Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses. |
| 4 | Lifecycle, Health, Shutdown, and Recovery | Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation. |
| 5 | Telemetry Architecture and Structured Events | Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy. |
| 6 | Metrics and Service-Level Indicators | Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics. |
| 7 | Distributed Tracing Across Asynchronous Work | Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes. |
| 8 | SLOs, Error Budgets, Dashboards, and Alerts | Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy. |
| 9 | Fault Injection, Troubleshooting, and Game Days | Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects. |
| 10 | Incident Command, Reconciliation, and Readiness | Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates. |

## Implementation route

Build the complete Course 4 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **observe, diagnose, contain, and recover the promise** survives an idiomatic implementation in another runtime.

## Final state

Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.

## Handoff discipline

The successor receives only the settled result: Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
