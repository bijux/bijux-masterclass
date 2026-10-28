# Capstone — API Reliability and Observability Engineering

## One continuing platform

The capstone is the Analysis Runs Platform. Principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive or consume completion facts. Course 4 does not replace the platform; it adds the responsibility **operate and recover the promise**.

## Starting state

The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

## Course increments

| Module | Platform increment |
|---:|---|
| 1 | Create the reliability case, critical-journey populations, failure modes, ownership, residual risk, and negative claims. |
| 2 | Implement monotonic deadlines, child budgets, safe retry classification, backoff, Retry-After handling, and cancellation. |
| 3 | Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses. |
| 4 | Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation. |
| 5 | Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy. |
| 6 | Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics. |
| 7 | Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes. |
| 8 | Publish five journey SLOs, multiwindow alerts, owner-linked runbooks, and release policy. |
| 9 | Design bounded faults, control populations, abort conditions, cleanup contracts, and proof-sensitive planted defects. |
| 10 | Run incident roles, read-only reconciliation, stable repair plans, verification, retrospective, and observable release gates. |


## Language tracks

Choose one primary implementation track. Compare failure semantics, telemetry meaning, and recovery invariants across both languages.

Shared fixtures, vectors, operation maps, releases, and black-box scenarios define parity. Identical class names or directory shape do not.

## Capstone reading order

1. read the module chapter and identify the owning mechanism;
2. inspect the narrow source path named by the chapter;
3. inspect the corresponding test or vector;
4. run the focused proof;
5. perform the lab modification in a working branch;
6. return to the chapter and explain how the implementation realizes the model.

## Handoff discipline

The predecessor material is read-only evidence. The current course may add a compatible public interface, migration, or profile only when its release rules permit it. It must not rewrite earlier history to simplify the present implementation.

**Outgoing handoff:** Reliability Profile 1.0, migration 008, critical journeys, deadlines, resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans.

## Final capstone question

Can you trace one accepted case and one rejected, failed, overloaded, or duplicated case from the public boundary to the authoritative outcome, then name the proof and limitation at every layer this course owns?
