# Lab — Module 03: Dependency Resilience and Graceful Degradation

## Objective

Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified.


## Setup conditions

The previous baseline is: **Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *When a dependency slows or fails, which work should stop, continue, queue, or degrade—and what must the API say?*

## Failure action and investigation

1. Open webhook circuit after classified failures.
2. Exhaust webhook bulkhead while reading API resources.
3. Disable collector and prove requests continue.
4. Inject artifact failure and plant false-success fallback.
5. Repair terminal behavior.
6. Test bounded half-open recovery.

### Required planted defect

Remove or bypass the central control for **Dependency Resilience and Graceful Degradation** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- API reads remain available during webhook saturation.
- Collector outage causes drop evidence, not response failure.
- No completed run lacks artifact evidence.
- Half-open concurrency stays bounded.
- Transitions are diagnosable without identifier labels.

## Required evidence

- baseline transcript proving the previous checkpoint before **Dependency Resilience and Graceful Degradation** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Classify dependency failures and ownership.
- public, durable, security, or operational observation showing: PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **dependency-local resilience**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Remove faults.
2. Reset/wait for circuits according to policy.
3. Drain or document durable backlogs.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=03` succeeds on the primary track.
