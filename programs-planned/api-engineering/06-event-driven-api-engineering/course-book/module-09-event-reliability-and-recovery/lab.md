# Lab — Run a controlled event-system failure and recovery

> **Module 09:** Event Reliability, Backpressure, Dead Letters, and Recovery

## Objective

Demonstrate bounded retry, poison handling, backpressure, backlog drain, replay protection, and reconciliation under a staged broker/consumer incident.

## Why this lab matters

This lab turns the module’s governing question—**How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery?**—into a falsifiable experiment. Review each channel/consumer pair with a failure worksheet: objective, arrival rate, service rate, backlog budget, retention, retry classes, maximum attempts/age, dead-letter owner, replay capacity, and reconciliation oracle. Then run fault injection at receive, effect commit, acknowledgement, broker disconnect, and recovery.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

1. Prepare valid, transient-failure, permanent-failure, and high-volume event fixtures.
2. Set retry, dead-letter, lag, outbox, and replay budgets from the event profile.
3. Start deterministic producers, relay, notification, and analytics consumers.
4. Create `work/module-09/incident-plan.md` with abort and cleanup criteria.
5. Preserve a pre-fault source/outbox/inbox/projection snapshot.

## Hypothesis

The clean implementation should satisfy this claim: **The system does not exceed declared outbox, retry, or replay budgets; permanent failure does not retry forever; critical live events retain priority; backlog drain is measurable; dead letter has an owner and repair record; reconciliation proves one effect per event/effect identity. The retry-all mutant fails.** When the lab introduces this fault—**Plant a retry-all defect and show dependency calls exceed the budget**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Stage four faults: broker unavailable, analytics database transient failure, one schema-invalid poison event,
and a replay burst competing with live events. Observe outbox growth, lag age/count, retries, dead-letter
creation, and admission response.

Recover the broker, pace backlog drain, repair the poison condition, execute a bounded canary replay, and
reconcile all durable identities. Plant a retry-all defect and show dependency calls exceed the budget.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a retry-all defect and show dependency calls exceed the budget**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Demonstrate bounded retry, poison handling, backpressure, backlog drain, replay protection, and reconciliation under a staged broker/consumer incident**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The system does not exceed declared outbox, retry, or replay budgets; permanent failure does not retry
forever; critical live events retain priority; backlog drain is measurable; dead letter has an owner and
repair record; reconciliation proves one effect per event/effect identity. The retry-all mutant fails.

## Required evidence

- `work/module-09/incident-plan.md`
- time-series snapshots of outbox, lag, retries, and effects
- dead-letter and repair record
- replay canary report
- admission/load-shedding decisions
- reconciliation report
- output from `make reliability-proof`

## Interpretation and defense

1. Which state or effect is authoritative for **Event Reliability, Backpressure, Dead Letters, and Recovery**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a retry-all defect and show dependency calls exceed the budget** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Stop fault injection and replay, acknowledge or terminate all test deliveries, clear transient fixture data,
restore admission policy, and verify lag/outbox/effect state returns to baseline. Preserve sanitized evidence.

## Completion gate

The lab passes only when recovery is proven by durable reconciliation, not by a green broker status or zero
lag alone. Every fault must have a bounded response and named owner.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Event Reliability, Backpressure, Dead Letters, and Recovery**. A green command without the negative case and causal explanation does not satisfy this gate.
