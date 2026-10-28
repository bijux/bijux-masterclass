# Lab — Run a controlled event-system failure and recovery

## Objective

Demonstrate bounded retry, poison handling, backpressure, backlog drain, replay protection, and reconciliation under a staged broker/consumer incident.

## Setup conditions


1. Prepare valid, transient-failure, permanent-failure, and high-volume event fixtures.
2. Set retry, dead-letter, lag, outbox, and replay budgets from the event profile.
3. Start deterministic producers, relay, notification, and analytics consumers.
4. Create `work/module-09/incident-plan.md` with abort and cleanup criteria.
5. Preserve a pre-fault source/outbox/inbox/projection snapshot.


## Failure action and investigation


Stage four faults: broker unavailable, analytics database transient failure, one schema-invalid poison event,
and a replay burst competing with live events. Observe outbox growth, lag age/count, retries, dead-letter
creation, and admission response.

Recover the broker, pace backlog drain, repair the poison condition, execute a bounded canary replay, and
reconcile all durable identities. Plant a retry-all defect and show dependency calls exceed the budget.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks. A passing command without this causal explanation is insufficient.

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


## Cleanup and reset


Stop fault injection and replay, acknowledge or terminate all test deliveries, clear transient fixture data,
restore admission policy, and verify lag/outbox/effect state returns to baseline. Preserve sanitized evidence.


## Completion gate


The lab passes only when recovery is proven by durable reconciliation, not by a green broker status or zero
lag alone. Every fault must have a bounded response and named owner.
