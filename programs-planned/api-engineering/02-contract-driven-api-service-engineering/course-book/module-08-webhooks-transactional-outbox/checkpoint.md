# Checkpoint — Module 08: Transactional Outbox and Webhook Delivery

## Required result

Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.

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

## Defend the design

1. Answer the central question: **How can a committed domain outcome produce an external notification without losing intent or duplicating effects unpredictably?**
2. Demonstrate this capstone result: Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.—all focused checks pass, the **Transactional Outbox and Webhook Delivery** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
