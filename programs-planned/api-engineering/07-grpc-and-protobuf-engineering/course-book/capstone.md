# Capstone — gRPC and Protobuf Engineering

## Cumulative system

Course 7 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to engineer typed internal invocation and streaming while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012.

The inherited boundary is read-only: The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- interaction-choice and ownership discipline;
- Protobuf semantic modeling and wire compatibility;
- unary metadata, status, deadlines, cancellation, and retries;
- bounded unary and streaming protocols;
- workload identity, authorization, health, discovery, generation, and governance;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | RPC Boundaries, Service Ownership, and Interaction Choice | Publish an interaction decision record, service-ownership map, and minimal Analysis RPC surface without splitting the platform prematurely. |
| 2 | Protobuf Modeling, Presence, and Semantic Types | Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior. |
| 3 | Wire Format, Unknown Fields, and Compatibility Discipline | Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes. |
| 4 | Unary RPCs, Metadata, Status, and Rich Errors | Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior. |
| 5 | Deadlines, Cancellation, Retries, and Idempotent Calls | Implement deadline-aware CreateRun and GetRun clients, persistent retry semantics, deterministic retry vectors, and fault-injection evidence for failures before invocation, before commit, after commit, and during response delivery. |
| 6 | Streaming RPCs, Flow Control, and Backpressure | Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing. |
| 7 | Identity, Authorization, mTLS, and Tenant Isolation | Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization. |
| 8 | Channels, Health, Discovery, Load Balancing, and Lifecycle | Implement channel and server lifecycle state machines, standard health semantics, bounded reconnect behavior, two-instance routing evidence, graceful drain, and an operational service configuration. |
| 9 | Generation, Testing, Reflection, and Schema Governance | Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate. |
| 10 | HTTP, Events, and gRPC in One Architecture: Release and Final Defense | Release Analysis RPC API 1.0 behind the unchanged public HTTP API and Event API, execute the final defense, and publish a sanitized service-boundary dossier rather than prematurely splitting the system. |

## Implementation route

Build the complete Course 7 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **engineer typed internal invocation and streaming** survives an idiomatic implementation in another runtime.

## Final state

Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence.

## Handoff discipline

The successor receives only the settled result: Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
