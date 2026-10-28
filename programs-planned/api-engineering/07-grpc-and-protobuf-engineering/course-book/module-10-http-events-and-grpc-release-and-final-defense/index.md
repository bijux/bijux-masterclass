# HTTP, Events, and gRPC in One Architecture: Release and Final Defense

**Module 10 of 10**

> **Governing question:** How do we introduce an internal RPC control plane without breaking the public HTTP contract, durable event history, database authority, security profile, or rollback path?

## Place in the program

The previous modules made individual RPC mechanisms correct. The final module makes the architecture correct. Course 7 is not successful because a server and client exchange Protobuf messages. It succeeds only when HTTP, events, local application logic, and gRPC have explicit non-overlapping responsibilities; migration is observable and reversible; and the outgoing boundary gives Course 8 evidence for deciding whether any component should become an independent service.

## Learning outcomes

- assign distinct public, asynchronous, local, and RPC responsibilities in one architecture
- migrate an internal call path with shadow, compare, bounded cutover, and rollback
- preserve database authority, transactional event publication, and public HTTP conformance
- design an RPC release gate spanning schema, generated code, runtime, security, reliability, and performance
- reject distributed-monolith boundaries even when the RPC implementation is efficient
- produce a service-boundary dossier for Course 8 based on measured ownership and failure evidence

## Capstone result

Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system.

## One capability can have several interfaces

The Analysis Runs Platform now has four interaction forms. Public HTTP exposes resource-oriented operations to external clients. Durable events publish committed facts to independent consumers. Local application calls preserve transaction and ownership boundaries inside one process. gRPC provides controlled typed synchronous and streaming capabilities between internal components. The same domain nouns may appear in each surface, but the semantics differ.

`POST /analysis-runs` remains the public command. An internal gateway may invoke `AnalysisControlService/CreateRun`. The committed state and outbox remain authoritative, and `AnalysisRunRequested` is published transactionally. `WatchRun` is a bounded operational observation stream; it does not replace the durable Event API. Worker `Work` coordinates attempts; accepted state changes still produce governed integration events.

Document this matrix explicitly. If two interfaces claim to be authoritative for the same mutation without one transaction owner, the architecture is inconsistent.

## The database and application transaction remain authoritative

Introducing RPC must not move correctness into the network. Analysis Control owns run state, idempotency, revisions, worker leases, artifacts, and event outbox through the application/database boundary inherited from Courses 2 and 6. An RPC handler cannot report success before that boundary commits. A worker stream cannot override a stale lease. A gateway retry cannot create a second run.

The first release can keep Analysis Control in the same deployable process while exercising the gRPC boundary in-process or over localhost. This separates protocol design from service extraction. Course 8 may later move the component only if ownership, scaling, security, and failure evidence justify it.

A protocol boundary without independent deployment can still be useful for generated worker clients or future isolation, but it must not add avoidable remote hops to every path merely to appear distributed.

## Strangler migration for an internal call path

Use a staged migration. **Baseline** invokes the local application port and records established behavior. **Shadow** sends a non-authoritative or safely duplicated query to the RPC path and compares results. For mutations, shadow only when idempotency and side-effect suppression make it safe; otherwise compare at a lower semantic layer. **Canary** routes a bounded eligible population to RPC with public conformance and durability oracles. **Cutover** increases traffic under gates. **Rollback** restores the local path without schema or data repair.

The routing decision is explicit and observable. It records path chosen, request identity, method, deadline, result classification, and comparison outcome without sensitive data. Fail-open or fail-closed behavior is operation-specific. A public mutation should not automatically fall back to a local second attempt after an ambiguous RPC failure because that can duplicate effects; it reconciles or reuses the same idempotency identity.

Rollback is rehearsed before cutover. Generated client and server versions coexist across the migration window.

## Public HTTP conformance is the first release gate

External clients must not detect an unintended transport change. Run the Course 1 HTTP conformance suite against the local-path baseline and RPC-backed candidate. Compare status, Problem Details, headers, ETags, idempotency replay, pagination, streaming, and security behavior. gRPC status codes are internal implementation detail.

Latency can change, but Course 5 budgets and Course 4 SLOs govern it. A faster candidate that weakens validation, authorization, or durability is rejected before performance is considered. A slower candidate may be rejected or reviewed according to the declared budget; transport novelty is not an exception.

The release report links every public operation affected by the internal migration to RPC method and comparison evidence.

## Durable events must remain truthful

An RPC command that commits state must create the same outbox event as the previous local path, in the same transaction. Event identity, schema, ordering policy, tenant, causation, and replay behavior remain governed by Course 6. The gateway or client does not publish the integration event merely because it received RPC success.

Compare event histories between baseline and candidate for successful, rejected, idempotent replay, post-commit response loss, cancellation, and worker completion. An internal stream frame is not an integration event until the authority validates and commits it. If RPC cutover changes event timing or duplication, the Event API release requires its own review.

This prevents transport migration from silently changing asynchronous consumers.

## Security, reliability, and performance gates remain active

The candidate must pass Course 3 identity and authorization vectors for both the gateway/workload and delegated principal. It must pass Course 4 deadline, cancellation, health, telemetry, and incident evidence. It must pass Course 5 latency, resource, admission, and regression gates. gRPC-specific tests supplement these profiles; they do not replace them.

The release gate records unexecuted environment capabilities. Live mTLS, load balancing, PostgreSQL concurrency, or external Buf checks cannot be claimed from dependency-light simulation. A candidate may be suitable for learning release while still carrying production evidence requirements.

Every new metric and trace attribute follows cardinality and privacy policy. Method names are bounded labels; resource and user identifiers are not.

## Avoiding the distributed monolith

A distributed monolith emerges when components are separately deployed but cannot change, operate, or fail independently. gRPC can make such coupling fast and type-safe without making it healthy. Warning signs include table-shaped services, synchronous chains for one user operation, shared private database tables, chatty fine-grained calls, cross-service transactions, and coordinated releases for ordinary changes.

The final architecture intentionally keeps Project, Dataset, Run, lease, and outbox state under one control authority. Dataset transfer and worker sessions are protocol capabilities, not automatic microservices. The Course 8 dossier evaluates candidate boundaries using ownership, data, transaction, scaling, security, failure, and team evidence.

At least one proposed extraction must be rejected. A mature architect can decide not to distribute.

## Release versions and coexistence

Analysis RPC API 1.0 uses package `bijux.analysis.v1`. Service release 1.0 may expose the methods while the HTTP gateway still uses the local path. A later service release enables canary routing without changing the RPC contract. Schema version, service release, public API version, event API version, and database migration revision remain distinct.

Migrations 013–015 add RPC idempotency/resume evidence, worker-session/attempt records, and contract catalogue state without invalidating Courses 1–6. Expand changes precede new writers. Rollback leaves expanded schema compatible. Enforcement occurs only after old paths no longer violate new invariants.

The version ledger names which component implements which contract and which migrations it requires.

## Final defense

The learner demonstrates one complete journey: a public HTTP request authenticates at the edge, maps to an internal `CreateRun` RPC with one deadline and request identity, commits durable run/idempotency/outbox state, returns through the HTTP adapter, publishes the integration event, assigns work over the worker stream, rejects a stale completion, commits a valid result, serves WatchRun and artifact download, and supports retry/reconciliation after response loss.

Then the learner explains why each interface exists and what it does not promise. They inject one compatibility break, one authorization failure, one deadline ambiguity, one slow stream, one server drain, and one rollback. Evidence must identify the authoritative state after each case.

The defense is an engineering argument supported by artifacts, not a tour of generated files.

## Outgoing boundary to Course 8

Course 8 receives the public HTTP and Event API contracts, Analysis RPC source/descriptors, version ledger, method catalogue, ownership map, data and transaction map, critical journeys, SLOs, security policy, failure evidence, performance profiles, consumer declarations, and a service-boundary dossier.

The dossier evaluates Analysis Control, Dataset Transfer, Worker Plane, Artifact Delivery, and Notification capabilities. It records reasons to keep together, reasons to split, state ownership, synchronous and asynchronous dependencies, independent scaling evidence, operational burden, and reversibility. It does not prescribe microservices.

Course 8 begins by challenging these candidate boundaries. Course 7's final skill is therefore protocol judgment: the learner can use gRPC deeply without assuming gRPC implies decomposition.

## Worked migration review: local port to RPC adapter

Before Course 7, the public HTTP handler invokes an application port in the same process. The first RPC release introduces an adapter around the same use case and database transaction. This is intentionally less dramatic than extracting a microservice. It lets the team prove method semantics, generated clients, deadlines, status, security, and streams while keeping rollback cheap.

The migration begins with a baseline. The team captures public HTTP responses, Problem Details, ETags, idempotency outcomes, database state, outbox events, traces, and latency/resource budgets. Read-only `GetRun` traffic can then be shadowed through the RPC adapter. The shadow result is authorized and normalized before comparison. It cannot influence the public response.

Mutations require stronger care. `CreateRun` can be canaried only when both paths use the same durable request identity and one path is authoritative. Running both as independent side effects would create duplicate runs. During canary, the gateway routes a bounded population to RPC and never performs an automatic local fallback after an ambiguous status. It retries through the same idempotency binding or reconciles the request outcome.

Suppose Analysis Control commits the run and outbox but the RPC response is lost. The HTTP gateway receives failure. It queries or retries with the same identity, obtains the stored result, and returns the existing public response. The event relay publishes one `AnalysisRunRequested` fact from the transaction. No client or gateway publishes the event based on observed transport success.

Now inject a stale worker result. The worker stream is authenticated, but its lease generation is old. Analysis Control rejects the frame; no terminal state or event is committed. A valid current result commits state, artifact metadata, and outbox. WatchRun emits a bounded operational snapshot; the Event API carries the durable integration fact. The interfaces agree because they share one authority, not because messages happen to look similar.

Operational cutover also runs health, drain, telemetry, SLO, and performance gates inherited from Courses 4 and 5. A faster RPC candidate that weakens authorization fails before latency review. A correct but materially slower candidate may be rejected or held. External tool and infrastructure evidence remains separate.

Rollback switches routing back to the local adapter while expanded migrations remain compatible. Because the database and application semantics never moved, rollback does not require data repair. Only after stable operation would Course 8 consider extracting a deployable service. The outgoing dossier records evidence for and against each boundary, including a deliberate recommendation to keep Analysis Control cohesive.

The final defense is successful when the learner can explain the authoritative state and recovery action for every fault—response loss, deadline expiry, slow stream, server drain, stale lease, schema evolution, and rollback—while preserving the public HTTP promise and durable event truth.

## Implementation reading

Read `capstone/final-defense/`, `capstone/releases/rpc-1.0/`, `capstone/rpc-case/version-ledger.yaml`, and `capstone/handoff/service-boundary-dossier.yaml`. Run the final tour through Python live gRPC and both dependency-light semantic tracks, then compare public HTTP and event evidence.

## Failure checklist

- Has internal gRPC changed any undocumented public HTTP behavior?
- Can RPC success occur before authoritative state and outbox commit?
- Can ambiguous RPC failure trigger an unsafe local fallback?
- Do worker frames bypass durable lease and event authority?
- Can rollback restore the previous path without data repair?
- Does any proposed service boundary create chatty calls, shared private state, or coordinated releases?

## Transition

After preserving the checkpoint evidence, continue to **Course 8 — Distributed API Architecture and Microservices Engineering**. Do not progress while the non-compensable gate remains unresolved.
