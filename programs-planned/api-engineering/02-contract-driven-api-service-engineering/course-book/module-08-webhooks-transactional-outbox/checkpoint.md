# Checkpoint — Module 08: Transactional Outbox and Webhook Delivery

## Required result

Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints.

## Demonstrate

- Explain the dual-write failure.
- Insert outbox intent in the domain transaction.
- Separate dispatcher attempts from logical events.
- Retry only classified failures with bounded delay.
- Require receiver deduplication for at-least-once delivery.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=08 TRACK=python
make module-proof MODULE=08 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Transactional Outbox and Webhook Delivery** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Transactional Outbox and Webhook Delivery**
- focused result for: Explain the dual-write failure.
- public, durable, security, or operational observation showing: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **transactional outbox delivery**
- a limitation statement naming every live dependency required to support the strongest **Transactional Outbox and Webhook Delivery** claim but not exercised

## Defend the design

1. Answer the central question: **How can a committed domain outcome produce an external notification without losing intent or duplicating effects unpredictably?**
2. Demonstrate this capstone result: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.
3. Show the **Transactional Outbox and Webhook Delivery** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated.
5. State which environment-backed **Transactional Outbox and Webhook Delivery** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.—all focused checks pass, the **Transactional Outbox and Webhook Delivery** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
