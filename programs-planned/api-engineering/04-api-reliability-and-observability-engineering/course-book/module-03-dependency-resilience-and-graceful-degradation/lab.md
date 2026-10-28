# Lab — Module 03: Dependency Resilience and Graceful Degradation

> **Module 03:** Dependency Resilience and Graceful Degradation

## Objective

Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified.

## Why this lab matters

This lab turns the module’s governing question—**How should circuits, bulkheads, and degradation be scoped so they contain rather than hide dependency failure?**—into a falsifiable experiment. Apply Dependency contract, Circuit breaker, Bulkhead to this module’s capstone increment: Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Add dependency-local state machines, bounded probes, concurrency isolation, and truthful degraded responses**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *When a dependency slows or fails, which work should stop, continue, queue, or degrade—and what must the API say?*

## Hypothesis

The clean implementation should satisfy this claim: **API reads remain available during webhook saturation; Collector outage causes drop evidence, not response failure; No completed run lacks artifact evidence; Half-open concurrency stays bounded; Transitions are diagnosable without identifier labels.** When the lab introduces this fault—**Inject artifact failure and plant false-success fallback**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Open webhook circuit after classified failures.
2. Exhaust webhook bulkhead while reading API resources.
3. Disable collector and prove requests continue.
4. Inject artifact failure and plant false-success fallback.
5. Repair terminal behavior.
6. Test bounded half-open recovery.

### Required planted defect

Remove or bypass the central control for **Dependency Resilience and Graceful Degradation** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject artifact failure and plant false-success fallback**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- API reads remain available during webhook saturation.
- Collector outage causes drop evidence, not response failure.
- No completed run lacks artifact evidence.
- Half-open concurrency stays bounded.
- Transitions are diagnosable without identifier labels.

## Required evidence

- baseline transcript proving the previous checkpoint before **Dependency Resilience and Graceful Degradation** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Dependency Resilience and Graceful Degradation**
- focused result for: Classify dependency failures and ownership.
- public, durable, security, or operational observation showing: PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **dependency-local resilience**
- a limitation statement naming every live dependency required to support the strongest **Dependency Resilience and Graceful Degradation** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Dependency Resilience and Graceful Degradation**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject artifact failure and plant false-success fallback** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Remove faults.
2. Reset/wait for circuits according to policy.
3. Drain or document durable backlogs.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=03` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Dependency Resilience and Graceful Degradation**. A green command without the negative case and causal explanation does not satisfy this gate.
