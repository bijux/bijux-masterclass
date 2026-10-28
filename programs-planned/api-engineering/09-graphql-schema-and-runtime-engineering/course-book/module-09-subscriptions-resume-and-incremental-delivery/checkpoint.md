# Checkpoint — Module 09: Subscriptions, Resume, and Incremental Delivery

## Required result

Deliver resumable run updates with gap and duplicate handling.

## Demonstrate

- [ ] Map durable events to subscription responses.
- [ ] Resume by sequence.
- [ ] Re-evaluate long-lived authorization.
- [ ] Bound subscriber buffers.
- [ ] Classify incremental-delivery features honestly.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-09-subscriptions.json` containing source sequences, delivered sequences, duplicate count, gap category, retention floor, maximum queue occupancy, close reason, authorization revision, cancellation state, and last safe resume coordinate.

## Defend the design

1. Answer the central question in one paragraph: How can real-time graph results remain authorized, bounded, and recoverable across disconnects?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Subscriptions, Resume, and Incremental Delivery** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
