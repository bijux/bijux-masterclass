# gRPC and Protobuf Engineering

**Course 7 — Engineer typed RPC boundaries without erasing HTTP, events, or local ownership**

> **Central question:** How do we design, evolve, secure, operate, and verify strongly typed remote procedure calls while preserving the public HTTP API, durable event contracts, and authoritative service semantics built in Courses 1–6?

## Course responsibility

Course 7 adds an internal RPC capability to the same Analysis Runs Platform. It does not replace the public OpenAPI API, the AsyncAPI event API, or local application calls. It teaches the judgment required to decide where gRPC belongs, how Protocol Buffers evolve, and which guarantees generated stubs do not provide.

## Incoming boundary

- public HTTP API 1.2 and OpenAPI 3.1.2 baseline;
- Analysis Events API 1.0 and AsyncAPI 3.1.0;
- Security, Reliability, Performance, and Event Profiles 1.0;
- migrations 001–012;
- durable idempotency, worker leases, artifact integrity, transactional outbox, event replay, and operational evidence.

## Outgoing boundary

- Analysis RPC API 1.0 in package `bijux.analysis.v1`;
- proto3 executable baseline and Editions 2024 frontier capability example;
- gRPC Service Profile 1.0;
- migrations 013–015;
- method catalogue, status policy, deadline and retry profile, streaming protocol, identity policy, health and lifecycle profile;
- Course 8 service-boundary dossier for distributed architecture decisions.

## What you will be able to do

After completing the course, you can:

- choose among local calls, public HTTP, durable events, unary RPC, and streaming RPC using explicit criteria;
- model Protobuf messages with correct presence, numeric, enum, oneof, resource identity, and compatibility semantics;
- reason from field numbers and wire bytes rather than generated source alone;
- implement unary and streaming gRPC services with deadlines, cancellation, idempotency, status policy, and bounded resources;
- authenticate channel peers, propagate caller identity, and enforce tenant and resource policy;
- operate channels, health, discovery, balancing, reflection, drain, and reconnect behavior;
- govern deterministic generation, descriptor sets, linting, breaking changes, conformance, and releases;
- integrate HTTP, events, and gRPC around one authoritative application model without creating a distributed monolith.

## The ten modules

1. RPC Boundaries, Service Ownership, and Interaction Choice  
2. Protobuf Modeling, Presence, and Semantic Types  
3. Wire Format, Unknown Fields, and Compatibility Discipline  
4. Unary RPCs, Metadata, Status, and Rich Errors  
5. Deadlines, Cancellation, Retries, and Idempotent Calls  
6. Streaming RPCs, Flow Control, and Backpressure  
7. Identity, Authorization, mTLS, and Tenant Isolation  
8. Channels, Health, Discovery, Load Balancing, and Lifecycle  
9. Generation, Testing, Reflection, and Schema Governance  
10. HTTP, Events, and gRPC in One Architecture: Release and Final Defense  

## How the course book works

Every numbered module has five reader-facing files:

1. `index.md` — the complete chapter and implementation reading;
2. `exercises.md` — twelve transfer questions;
3. `exercise-answers.md` — twelve matching reasoned answers;
4. `lab.md` — one controlled experiment with a real failure oracle;
5. `checkpoint.md` — evidence required before progression.

The course book is the product. Capstone code, fixtures, generated surfaces, and proof scripts make claims executable; they do not replace explanation.

Continue with [Start here](start-here.md).
