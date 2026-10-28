# Course contents

## Reader-facing course book

- 8 program/course guide pages
- 1 orientation page
- 10 numbered modules
- 5 pages per numbered module
- 120 exercises
- 120 matching worked answers
- 10 labs
- 10 checkpoints
- 59 total navigated pages

## Modules

1. **RPC Boundaries, Service Ownership, and Interaction Choice** — Which interactions deserve a typed RPC boundary, and which should remain HTTP requests, durable events, or local function calls?
2. **Protobuf Modeling, Presence, and Semantic Types** — How do we encode domain meaning in Protobuf without allowing language defaults, JSON conventions, or storage models to erase important distinctions?
3. **Wire Format, Unknown Fields, and Compatibility Discipline** — How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?
4. **Unary RPCs, Metadata, Status, and Rich Errors** — How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals?
5. **Deadlines, Cancellation, Retries, and Idempotent Calls** — How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects?
6. **Streaming RPCs, Flow Control, and Backpressure** — How do we design long-lived and bulk-transfer RPCs so that slow peers, reconnects, oversized messages, and stale attempts cannot exhaust memory or corrupt state?
7. **Identity, Authorization, mTLS, and Tenant Isolation** — How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust?
8. **Channels, Health, Discovery, Load Balancing, and Lifecycle** — How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?
9. **Generation, Testing, Reflection, and Schema Governance** — How do we make proto source, generated code, runtime services, tests, descriptors, reflection, and release policy agree without treating code generation as proof?
10. **HTTP, Events, and gRPC in One Architecture: Release and Final Defense** — How do we introduce an internal RPC control plane without breaking the public HTTP contract, durable event history, database authority, security profile, or rollback path?

## Executable capstone

The capstone includes:

- canonical proto3 source and Editions 2024 frontier
- Python generated-equivalent messages and live `grpcio` server/client
- TypeScript dependency-light semantic implementation and optional grpc-js adapter
- unary, server-streaming, client-streaming, and bidirectional protocols
- shared cross-language vectors
- compatibility candidates and golden wire fixtures
- health, lifecycle, security, retry, and stream policies
- migrations 001–015
- release and rollback evidence
- ten planted defects
- outgoing Course 8 service-boundary dossier

## Proof classes

1. static contract and descriptor proof
2. dependency-light semantic proof
3. live Python network gRPC proof
4. optional external `protoc`, Buf, grpcurl, TLS, PostgreSQL, and TypeScript network proof
5. course-structure, education, link, hygiene, and manifest proof
