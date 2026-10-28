# Worked Answers — Module 10: HTTP, Events, and gRPC in One Architecture: Release and Final Defense

Use these solutions to audit your reasoning for **HTTP, Events, and gRPC in One Architecture: Release and Final Defense**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Assign one responsibility each to public HTTP, durable events, local calls, and gRPC.

HTTP owns public resource interaction; events own durable committed facts for independent consumers; local calls own behavior inside one transaction/ownership boundary; gRPC owns controlled internal synchronous or streaming capabilities.

**Decisive evidence:** interaction responsibility matrix

The chapter’s decisive distinction is this: The Analysis Runs Platform now has four interaction forms. Public HTTP exposes resource-oriented operations to external clients. Durable events publish committed facts to independent consumers. Local application calls preserve transaction and ownership boundaries inside one process. gRPC provides controlled typed synchronous and streaming capabilities between internal components. The same domain nouns may appear in each surface, but the semantics differ.

## 2. Why should gRPC be introduced before extracting a separate deployable service?

It lets the team prove contract, semantics, security, and operational behavior without simultaneously adding independent deployment, discovery, network, and team ownership complexity.

**Decisive evidence:** in-process/remote staged architecture

In the cumulative capstone, the rule becomes concrete: Before Course 7, the public HTTP handler invokes an application port in the same process. The first RPC release introduces an adapter around the same use case and database transaction. This is intentionally less dramatic than extracting a microservice. It lets the team prove method semantics, generated clients, deadlines, status, security, and streams while keeping rollback cheap.

## 3. Design a safe shadow step for GetRun and explain why CreateRun is harder.

Mirror or sample GetRun through both paths and compare authorized snapshots because it is read-only. CreateRun can create duplicate effects unless the shadow is side-effect-free or uses one durable idempotency identity.

**Decisive evidence:** shadow comparison report

A useful way to reason about the boundary is: The migration begins with a baseline. The team captures public HTTP responses, Problem Details, ETags, idempotency outcomes, database state, outbox events, traces, and latency/resource budgets. Read-only GetRun traffic can then be shadowed through the RPC adapter. The shadow result is authorized and normalized before comparison. It cannot influence the public response.

## 4. Why is automatic local fallback after an ambiguous CreateRun RPC failure unsafe?

The RPC may have committed. A second local execution can create another effect. Reuse the same request identity or reconcile authoritative state.

**Decisive evidence:** post-commit fallback test

The implementation consequence is: Mutations require stronger care. CreateRun can be canaried only when both paths use the same durable request identity and one path is authoritative. Running both as independent side effects would create duplicate runs. During canary, the gateway routes a bounded population to RPC and never performs an automatic local fallback after an ambiguous status. It retries through the same idempotency binding or reconciles the request outcome.

## 5. What public evidence must remain unchanged during cutover?

Status and Problem Details, headers, ETags, idempotency, pagination, validation, security concealment, streaming behavior, and documented response bodies.

**Decisive evidence:** public HTTP conformance

The important nuance is: External clients must not detect an unintended transport change. Run the Course 1 HTTP conformance suite against the local-path baseline and RPC-backed candidate. Compare status, Problem Details, headers, ETags, idempotency replay, pagination, streaming, and security behavior. gRPC status codes are internal implementation detail.

**Evidence.** Combine proto/descriptor validation, generated surface checks, shared vectors, and a live client/server RPC scenario.

## 6. Who publishes AnalysisRunCompleted after a worker result arrives over gRPC?

Analysis Control after validating workload identity, assignment, lease generation, and state, in the same transaction as durable state/outbox. The worker or gateway does not publish it.

**Decisive evidence:** worker-to-outbox transaction trace

Under concurrency or failure, the distinction becomes: Introducing RPC must not move correctness into the network. Analysis Control owns run state, idempotency, revisions, worker leases, artifacts, and event outbox through the application/database boundary inherited from Courses 2 and 6. An RPC handler cannot report success before that boundary commits. A worker stream cannot override a stale lease. A gateway retry cannot create a second run.

## 7. How should Course 4 and Course 5 gates participate in the RPC release?

Reliability gates check deadlines, cancellation, health, telemetry, drain, and recovery. Performance gates check budgets, resources, admission, and regression after correctness/security pass.

**Decisive evidence:** cross-course release report

The design remains honest only if: The candidate must pass Course 3 identity and authorization vectors for both the gateway/workload and delegated principal. It must pass Course 4 deadline, cancellation, health, telemetry, and incident evidence. It must pass Course 5 latency, resource, admission, and regression gates. gRPC-specific tests supplement these profiles; they do not replace them.

## 8. Name three signs that a proposed gRPC service would create a distributed monolith.

Table-shaped services, shared private database ownership, chatty synchronous chains, cross-service transactions, and mandatory coordinated releases are warning signs.

**Decisive evidence:** distributed-monolith rejection case

The consumer-facing consequence is: A distributed monolith emerges when components are separately deployed but cannot change, operate, or fail independently. gRPC can make such coupling fast and type-safe without making it healthy. Warning signs include table-shaped services, synchronous chains for one user operation, shared private database tables, chatty fine-grained calls, cross-service transactions, and coordinated releases for ordinary changes.

## 9. Why are RPC API version and service release version separate?

The contract may remain Analysis RPC 1.0 while service releases add implementation, canary routing, fixes, or observability. Conflating them forces unnecessary client version changes.

**Decisive evidence:** version ledger

The operational consequence is: Analysis RPC API 1.0 uses package bijux.analysis.v1. Service release 1.0 may expose the methods while the HTTP gateway still uses the local path. A later service release enables canary routing without changing the RPC contract. Schema version, service release, public API version, event API version, and database migration revision remain distinct.

## 10. Describe a rollback-compatible migration sequence for migrations 013–015.

Expand schema first, deploy code that can use or ignore new columns/tables, canary new writers/readers, preserve old-path compatibility for rollback, then enforce only after old writers retire.

**Decisive evidence:** migration coexistence proof

The strongest engineering interpretation is: Migrations 013–015 add RPC idempotency/resume evidence, worker-session/attempt records, and contract catalogue state without invalidating Courses 1–6. Expand changes precede new writers. Rollback leaves expanded schema compatible. Enforcement occurs only after old paths no longer violate new invariants.

## 11. What must the final defense prove after response loss?

That one durable effect exists, the idempotency outcome is replayable, the public client can reconcile, the event history is correct, and no unsafe fallback duplicated work.

**Decisive evidence:** response-loss final trace

The defect-oriented view is: The learner demonstrates one complete journey: a public HTTP request authenticates at the edge, maps to an internal CreateRun RPC with one deadline and request identity, commits durable run/idempotency/outbox state, returns through the HTTP adapter, publishes the integration event, assigns work over the worker stream, rejects a stale completion, commits a valid result, serves WatchRun and artifact download, and supports retry/reconciliation after response loss.

## 12. What evidence belongs in the Course 8 service-boundary dossier?

Ownership, authoritative data, transaction boundaries, methods/events, dependencies, scaling evidence, security, SLO/failure behavior, consumers, operational burden, migration/rollback, and an explicit keep-or-split recommendation with uncertainty.

**Decisive evidence:** service-boundary dossier

Across the Python and TypeScript tracks, the invariant is: Course 8 receives the public HTTP and Event API contracts, Analysis RPC source/descriptors, version ledger, method catalogue, ownership map, data and transaction map, critical journeys, SLOs, security policy, failure evidence, performance profiles, consumer declarations, and a service-boundary dossier.
