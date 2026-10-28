# Version and Handoff Ledger

## Keep the version axes separate

The program uses several independent axes:

- interface specification version, such as OpenAPI 3.2.0;
- public API product version, such as Analysis HTTP API 1.2;
- executable service release;
- database migration revision;
- engineering profile version, such as Security Profile 1.0;
- generated artifact or SDK version.

Changing one does not automatically change another.

| Course | Course | Version state | Outgoing handoff |
|---:|---|---|---|
| 1 | OpenAPI Contract Engineering | Public API 1.1; OpenAPI 3.1.2 executable baseline; OpenAPI 3.2.0 standards frontier; no durable database yet. | A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflow description, compatibility policy, and provider-neutral behavioral scenarios. |
| 2 | Contract-Driven API Service Engineering | API 1.1 preserved; additive API 1.2 introduced; OpenAPI 3.1.2 preserved; migrations 001–005. | A durable API 1.2 service with migrations 001–005, persistent idempotency, atomic conditional updates, stable pagination, worker recovery, artifact integrity, transactional webhook delivery, and compatible-release evidence. |
| 3 | API Security Engineering | API 1.2 preserved; Security Profile 1.0 introduced; migrations 001–007. | Security Profile 1.0, migrations 006–007, a threat-to-requirement security case, identity and authorization policy, hostile-input vectors, SSRF and webhook protections, abuse controls, and incident evidence. |
| 4 | API Reliability and Observability Engineering | API 1.2 and Security Profile 1.0 preserved; Reliability Profile 1.0 introduced; migrations 001–008. | Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans. |
| 5 | API Performance, Capacity, and Traffic Engineering | API 1.2, Security Profile 1.0, and Reliability Profile 1.0 preserved; Performance Profile 1.0 introduced; migrations 001–009. | Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates. |
| 6 | Event-Driven API Engineering | HTTP API 1.2 preserved; Analysis Events API 1.0 introduced; AsyncAPI 3.1.0; CloudEvents 1.0-compatible profile; migrations 001–012. | Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations. |
| 7 | gRPC and Protobuf Engineering | HTTP API 1.2 and Events API 1.0 preserved; RPC API 1.0 introduced; proto3 baseline; Edition 2024 frontier; migrations 001–015. | Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence. |
| 8 | Distributed API Architecture and Microservices Engineering | HTTP API 1.2, Events API 1.0, and RPC API 1.0 preserved; distributed architecture profile 1.0 introduced; owner-local migration histories begin. | Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief. |
| 9 | GraphQL Schema and Runtime Engineering | HTTP, Event, and RPC APIs preserved; Analysis Graph API 1.0 introduced; GraphQL September 2025; graph metadata migrations 001–004. | Analysis Graph API 1.0, GraphQL September 2025 schema, persisted operation registry, resolver ownership, demand policy, resumable subscriptions, compatibility gates, and platform-publication metadata. |
| 10 | API Platform, Governance, and Developer Experience Engineering | All earlier interface and engineering profiles preserved; Analysis API Platform 1.0 and platform-catalog metadata migrations 001–004 introduced. | Analysis API Platform 1.0, a governed catalog and registry, lifecycle and policy engine, golden path, documentation and sandbox, SDK and provenance publication, runtime reconciliation, support model, and a ten-course graduation dossier. |

## Handoff rule

A handoff is read-only historical evidence. The successor may add a compatible interface, profile, migration, or capability under its release policy. It may not rewrite the predecessor to make the new implementation easier. The program-level `handoff-proof` verifies all nine adjacent boundaries byte-for-byte.
