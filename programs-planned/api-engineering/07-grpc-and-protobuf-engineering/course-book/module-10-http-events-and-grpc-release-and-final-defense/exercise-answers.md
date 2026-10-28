# Worked answers — HTTP, Events, and gRPC in One Architecture: Release and Final Defense

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Assign one responsibility each to public HTTP, durable events, local calls, and gRPC.

HTTP owns public resource interaction; events own durable committed facts for independent consumers; local calls own behavior inside one transaction/ownership boundary; gRPC owns controlled internal synchronous or streaming capabilities.

**Decisive evidence:** interaction responsibility matrix

## 2. Why should gRPC be introduced before extracting a separate deployable service?

It lets the team prove contract, semantics, security, and operational behavior without simultaneously adding independent deployment, discovery, network, and team ownership complexity.

**Decisive evidence:** in-process/remote staged architecture

## 3. Design a safe shadow step for GetRun and explain why CreateRun is harder.

Mirror or sample GetRun through both paths and compare authorized snapshots because it is read-only. CreateRun can create duplicate effects unless the shadow is side-effect-free or uses one durable idempotency identity.

**Decisive evidence:** shadow comparison report

## 4. Why is automatic local fallback after an ambiguous CreateRun RPC failure unsafe?

The RPC may have committed. A second local execution can create another effect. Reuse the same request identity or reconcile authoritative state.

**Decisive evidence:** post-commit fallback test

## 5. What public evidence must remain unchanged during cutover?

Status and Problem Details, headers, ETags, idempotency, pagination, validation, security concealment, streaming behavior, and documented response bodies.

**Decisive evidence:** public HTTP conformance

## 6. Who publishes AnalysisRunCompleted after a worker result arrives over gRPC?

Analysis Control after validating workload identity, assignment, lease generation, and state, in the same transaction as durable state/outbox. The worker or gateway does not publish it.

**Decisive evidence:** worker-to-outbox transaction trace

## 7. How should Course 4 and Course 5 gates participate in the RPC release?

Reliability gates check deadlines, cancellation, health, telemetry, drain, and recovery. Performance gates check budgets, resources, admission, and regression after correctness/security pass.

**Decisive evidence:** cross-course release report

## 8. Name three signs that a proposed gRPC service would create a distributed monolith.

Table-shaped services, shared private database ownership, chatty synchronous chains, cross-service transactions, and mandatory coordinated releases are warning signs.

**Decisive evidence:** distributed-monolith rejection case

## 9. Why are RPC API version and service release version separate?

The contract may remain Analysis RPC 1.0 while service releases add implementation, canary routing, fixes, or observability. Conflating them forces unnecessary client version changes.

**Decisive evidence:** version ledger

## 10. Describe a rollback-compatible migration sequence for migrations 013–015.

Expand schema first, deploy code that can use or ignore new columns/tables, canary new writers/readers, preserve old-path compatibility for rollback, then enforce only after old writers retire.

**Decisive evidence:** migration coexistence proof

## 11. What must the final defense prove after response loss?

That one durable effect exists, the idempotency outcome is replayable, the public client can reconcile, the event history is correct, and no unsafe fallback duplicated work.

**Decisive evidence:** response-loss final trace

## 12. What evidence belongs in the Course 8 service-boundary dossier?

Ownership, authoritative data, transaction boundaries, methods/events, dependencies, scaling evidence, security, SLO/failure behavior, consumers, operational burden, migration/rollback, and an explicit keep-or-split recommendation with uncertainty.

**Decisive evidence:** service-boundary dossier
