# Exercises — Module 04 — Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

Reason in transactions and durable identities. “Retry it” is not a complete answer.

## 1. Place the outbox transaction

Identify the exact Course 2 transaction that should create `AnalysisRunCompleted` and its outbox row.

## 2. Enumerate producer crash windows

Describe outcomes for crash before domain commit, after commit before relay, after broker acceptance before mark, and after mark.

## 3. Design an outbox row

List fields needed for identity, canonical content, claim ownership, retry, publication evidence, and reconciliation.

## 4. Choose an inbox key

Compare event ID alone, delivery token, broker offset, and `(consumer, effectVersion, eventId)`. Select and justify.

## 5. Prove one effect

Define counters that can distinguish one broker record, two deliveries, two handler attempts, and one committed projection update.

## 6. Handle concurrent duplicates

Two instances receive duplicate records simultaneously. Explain how a unique constraint and transaction decide the winner.

## 7. Protect an email side effect

Design the inbox/projection/outbound-command transaction for a completion email.

## 8. Version an effect

Analytics v2 changes its aggregation. Explain how it can replay without deleting v1 evidence or resending notifications.

## 9. Freeze event bytes

Explain why the relay must not re-read the run row and rebuild the payload after a schema deployment.

## 10. Reconcile a missing inbox

The broker shows an acknowledged event but no inbox or projection row. Identify likely defects and a safe investigation order.

## 11. Reject distributed-transaction magic

A proposal wraps PostgreSQL, NATS, and an email API in one application `try/except`. Explain why this is not atomic.

## 12. State an honest exactly-once claim

Write a bounded claim for the analytics projection and identify what it excludes.

## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
