# Checkpoint — Module 09: Event Reliability, Backpressure, Dead Letters, and Recovery

## Required result

Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks.

## Demonstrate

- Classify permanent, transient, capacity, and security failures.
- Explain how backpressure reaches producer admission.
- Interpret lag using count, age, partition, and rates.
- Describe dead-letter repair and why automatic republish is unsafe.

## Commands

```bash
make reliability-proof
make planted-defect-proof
make module-proof MODULE=09 TRACK=$TRACK
```

## Evidence to retain

- `work/module-09/incident-plan.md`
- time-series snapshots of outbox, lag, retries, and effects
- dead-letter and repair record
- replay canary report
- admission/load-shedding decisions
- reconciliation report
- output from `make reliability-proof`

## Defend the design

- Show retry budget enforcement.
- Demonstrate live-traffic protection during replay.
- Explain why zero lag is insufficient recovery evidence.
- Defend the dead-letter retention and access policy.

## Continue only when

- Any failure retries without a maximum or total age.
- Dead letters lack owner or repair path.
- Backlog can grow beyond storage/admission budget.
- Recovery has no durable reconciliation oracle.

The **Event Reliability, Backpressure, Dead Letters, and Recovery** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks.
