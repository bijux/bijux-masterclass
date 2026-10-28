# Checkpoint — Event Reliability, Backpressure, Dead Letters, and Recovery

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Classify permanent, transient, capacity, and security failures.
- Explain how backpressure reaches producer admission.
- Interpret lag using count, age, partition, and rates.
- Describe dead-letter repair and why automatic republish is unsafe.

## Required result

- `work/module-09/incident-plan.md`
- `work/module-09/lag-and-backlog.json`
- `work/module-09/dead-letter-repair.json`
- `work/module-09/reconciliation.json`
- `work/module-09/residual-risk.md`

## Commands

```bash
make reliability-proof
make planted-defect-proof
make module-proof MODULE=09 TRACK=$TRACK
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks.
