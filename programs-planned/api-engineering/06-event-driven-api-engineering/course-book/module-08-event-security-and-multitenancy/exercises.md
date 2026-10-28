# Exercises — Module 08 — Event Security, Multi-Tenancy, Privacy, and Trust

Use least privilege and durable trust evidence. Do not answer “TLS” as a complete event-security design.

## 1. Bind a producer

Define a grant for the analysis control plane that may publish completed/failed events for two tenants but not artifact events.

## 2. Authorize a consumer

Define notification-v1 access without granting raw dataset or progress-event subscriptions.

## 3. Find a tenant leak

An inbox key includes consumer and event ID but the projection table is not tenant-scoped. Explain the remaining risk.

## 4. Minimize a failure event

Choose safe fields for `AnalysisRunFailed` and reject sensitive candidates.

## 5. Compare TLS and signatures

Explain what each protects and what neither proves about business truth.

## 6. Compute signature input

State the exact inputs signed by the course profile and why ordinary object serialization is insufficient.

## 7. Distinguish two replays

Compare hostile live injection of an old signed message with an authorized historical projection replay.

## 8. Rotate a key

Design the order for publishing verification key, switching producers, observing overlap, and retiring old material.

## 9. Respond to compromise

A producer key may be stolen. List evidence needed to scope false events and reconcile source truth.

## 10. Secure dead letters

Define fields, access, retention, and redaction for a dead-letter record.

## 11. Protect a shared channel

Explain how a shared multi-tenant channel can remain safe and when subject-per-tenant may be justified.

## 12. Audit rejection

Design a safe event-security rejection record without logging the raw payload.

## Submission format

Submit Module 08 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
