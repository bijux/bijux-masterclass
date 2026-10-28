# gRPC and Protobuf Engineering

**Course 7 of 10 — Engineer typed internal invocation and streaming**

## Course promise

Design and verify Protobuf schemas and gRPC interactions without pretending that generated stubs turn remote calls into local functions.

> **Governing question:** How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries?

## Place in the program

**Incoming boundary:** The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012.

**Outgoing boundary:** Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence.

Course 7 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the engineer typed internal invocation and streaming mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- interaction-choice and ownership discipline;
- Protobuf semantic modeling and wire compatibility;
- unary metadata, status, deadlines, cancellation, and retries;
- bounded unary and streaming protocols;
- workload identity, authorization, health, discovery, generation, and governance;

## Course-level learning outcomes

- Distinguish local calls, public HTTP operations, durable events, and internal RPCs by ownership, coupling, latency, and failure semantics.
- Design request and response messages around application decisions rather than persistence records.
- Explain how field numbers and wire types determine binary compatibility.
- Implement thin unary server adapters around application use cases.
- Derive child RPC budgets from one absolute edge deadline.
- Choose unary, server-streaming, client-streaming, or bidirectional RPC from interaction semantics.
- Distinguish server TLS, mutual TLS workload identity, bearer identity, and delegated end-user context.
- Treat channels as long-lived managed resources rather than create-per-call sockets.
- Define authoritative proto source and reproducible generation inputs.
- Assign distinct public, asynchronous, local, and RPC responsibilities in one architecture.

## Module map

| Day | Chapter | Governing question | Capstone increment |
|---:|---|---|---|
| 1 | [RPC Boundaries, Service Ownership, and Interaction Choice](module-01-rpc-boundaries-and-service-ownership/index.md) | Which interactions deserve a typed RPC boundary, and which should remain HTTP requests, durable events, or local function calls? | Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely. |
| 2 | [Protobuf Modeling, Presence, and Semantic Types](module-02-protobuf-modeling-presence-and-semantic-types/index.md) | How do we encode domain meaning in Protobuf without allowing language defaults, JSON conventions, or storage models to erase important distinctions? | Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior. |
| 3 | [Wire Format, Unknown Fields, and Compatibility Discipline](module-03-wire-format-unknown-fields-and-compatibility/index.md) | How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe? | Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes. |
| 4 | [Unary RPCs, Metadata, Status, and Rich Errors](module-04-unary-rpcs-metadata-status-and-rich-errors/index.md) | How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals? | Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior. |
| 5 | [Deadlines, Cancellation, Retries, and Idempotent Calls](module-05-deadlines-cancellation-retries-and-idempotent-calls/index.md) | How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects? | Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery. |
| 6 | [Streaming RPCs, Flow Control, and Backpressure](module-06-streaming-rpcs-flow-control-and-backpressure/index.md) | How do we design long-lived and bulk-transfer RPCs so that slow peers, reconnects, oversized messages, and stale attempts cannot exhaust memory or corrupt state? | Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing. |
| 7 | [Identity, Authorization, mTLS, and Tenant Isolation](module-07-identity-authorization-mtls-and-tenant-isolation/index.md) | How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust? | Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization. |
| 8 | [Channels, Health, Discovery, Load Balancing, and Lifecycle](module-08-channels-health-discovery-load-balancing-and-lifecycle/index.md) | How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work? | Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration. |
| 9 | [Generation, Testing, Reflection, and Schema Governance](module-09-generation-testing-reflection-and-schema-governance/index.md) | How do we make proto source, generated code, runtime services, tests, descriptors, reflection, and release policy agree without treating code generation as proof? | Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate. |
| 10 | [HTTP, Events, and gRPC in One Architecture: Release and Final Defense](module-10-http-events-and-grpc-release-and-final-defense/index.md) | How do we introduce an internal RPC control plane without breaking the public HTTP contract, durable event history, database authority, security profile, or rollback path? | Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system. |

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- replacing public HTTP or durable events;
- treating generated code as architecture;
- assuming RPC methods justify microservices;
- claiming a local TLS fixture is an operated trust system;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 7, read each chapter around the question **How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
