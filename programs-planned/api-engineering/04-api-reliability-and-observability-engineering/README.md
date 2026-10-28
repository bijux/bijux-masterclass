# API Reliability and Observability Engineering

**Course 4 of 6 — Operate and recover the promise**

Detect, diagnose, contain, reconcile, and recover when processes, dependencies, networks, or operators fail.

> How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

## Begin with the course book

1. Read [Course introduction](course-book/index.md).
2. Complete [Start here](course-book/start-here.md) and [orientation](course-book/module-00-orientation/index.md).
3. Follow the ten modules in order.
4. Use the capstone and implementation tracks only through the reading routes named in each chapter.
5. Preserve checkpoint evidence before progressing.

## Modules

01. [Reliability Model and Critical Journeys](course-book/module-01-reliability-model-and-critical-journeys/index.md)
02. [Deadlines, Cancellation, and Retry Budgets](course-book/module-02-deadlines-timeouts-cancellation-and-retry-budgets/index.md)
03. [Dependency Resilience and Graceful Degradation](course-book/module-03-dependency-resilience-and-graceful-degradation/index.md)
04. [Lifecycle, Health, Shutdown, and Recovery](course-book/module-04-lifecycle-health-graceful-shutdown-and-recovery/index.md)
05. [Telemetry Architecture and Structured Events](course-book/module-05-telemetry-architecture-and-structured-operational-events/index.md)
06. [Metrics and Service-Level Indicators](course-book/module-06-metrics-and-service-level-indicators/index.md)
07. [Distributed Tracing Across Asynchronous Work](course-book/module-07-distributed-tracing-across-http-workers-storage-and-webhooks/index.md)
08. [SLOs, Error Budgets, Dashboards, and Alerts](course-book/module-08-slos-error-budgets-dashboards-and-alerts/index.md)
09. [Fault Injection, Troubleshooting, and Game Days](course-book/module-09-fault-injection-troubleshooting-and-game-days/index.md)
10. [Incident Command, Reconciliation, and Readiness](course-book/module-10-incident-command-state-reconciliation-and-operational-readiness/index.md)

## Program boundary

**Incoming:** The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

**Outgoing:** Reliability Profile 1.0, migration 008, critical journeys, deadlines, resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.

## Implementation strategy

Choose one primary implementation track. Compare failure semantics, telemetry meaning, and recovery invariants across both languages.

## Verification

```bash
make doctor
make core-proof
make manifest-proof
```

Environment-dependent routes are reported separately. Missing infrastructure is never represented as a passing live proof.
