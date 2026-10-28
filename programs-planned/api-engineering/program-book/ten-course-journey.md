# The Ten-Course Journey

## Course 1 — OpenAPI Contract Engineering

**Responsibility:** Specify the public promise.

**Governing question:** What exactly does the API promise, and how can providers and consumers verify that promise?

**Incoming boundary:** Basic programming ability, command-line familiarity, and no assumed OpenAPI experience.

**What changes:** a canonical multi-document OpenAPI description; precise JSON Schema models and examples; Python and TypeScript provider parity; generated and authored consumer evidence; compatibility, security, Overlay, and Arazzo artifacts.

**What remains deliberately out of scope:** durable persistence; production identity infrastructure; operated deployment; performance or reliability claims.

**Outgoing boundary:** A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflow description, compatibility policy, and provider-neutral behavioral scenarios. The outgoing handoff becomes the immutable starting point for Course 2.

## Course 2 — Contract-Driven API Service Engineering

**Responsibility:** Implement the promise durably.

**Governing question:** Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure?

**Incoming boundary:** The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

**What changes:** application use cases and domain invariants; PostgreSQL persistence and migration ownership; transactions, idempotency, ETags, and stable cursors; durable workers, leases, and recovery; bounded artifact transfer and transactional outbox delivery.

**What remains deliberately out of scope:** full security engineering; SRE and observability operations; performance tuning as a goal; service decomposition.

**Outgoing boundary:** A durable API 1.2 service with migrations 001–005, persistent idempotency, atomic conditional updates, stable pagination, worker recovery, artifact integrity, transactional webhook delivery, and compatible-release evidence. The outgoing handoff becomes the immutable starting point for Course 3.

## Course 3 — API Security Engineering

**Responsibility:** Defend the promise.

**Governing question:** How does the API remain trustworthy when callers, credentials, inputs, destinations, dependencies, and networks cannot be trusted by default?

**Incoming boundary:** The Course 2 API 1.2 durable-service handoff and migrations 001–005.

**What changes:** threat modeling and security requirements; strict request and credential validation; tenant-, scope-, role-, and ownership-aware authorization; hostile input, file, outbound request, and webhook controls; secrets, audit, abuse, supply-chain, and incident-response evidence.

**What remains deliberately out of scope:** building a production authorization server; generic penetration-testing instruction; compliance certification; operated key-management infrastructure.

**Outgoing boundary:** Security Profile 1.0, migrations 006–007, a threat-to-requirement security case, identity and authorization policy, hostile-input vectors, SSRF and webhook protections, abuse controls, and incident evidence. The outgoing handoff becomes the immutable starting point for Course 4.

## Course 4 — API Reliability and Observability Engineering

**Responsibility:** Observe, diagnose, contain, and recover the promise.

**Governing question:** How do operators know whether the user promise is still true, and how do they recover it without making the incident worse?

**Incoming boundary:** The Course 3 API 1.2 service protected by Security Profile 1.0 and migrations 001–007.

**What changes:** critical-journey reliability models; deadlines, cancellation, retries, circuits, and bulkheads; health, draining, shutdown, startup recovery, and reconciliation; structured events, metrics, traces, SLOs, alerts, and runbooks; fault injection, game days, incident command, and repair evidence.

**What remains deliberately out of scope:** claiming telemetry is authoritative business state; full capacity engineering; vendor-specific observability operations; multi-region disaster recovery.

**Outgoing boundary:** Reliability Profile 1.0, migration 008, critical journeys, deadline and resilience policies, lifecycle controls, telemetry contracts, SLOs, alerts, runbooks, game-day evidence, and reconciliation plans. The outgoing handoff becomes the immutable starting point for Course 5.

## Course 5 — API Performance, Capacity, and Traffic Engineering

**Responsibility:** Sustain the promise under pressure.

**Governing question:** Where do time and capacity go, what is the first limiting resource, and which measured change improves the system without weakening correctness?

**Incoming boundary:** The Course 4 observable and recoverable API 1.2 service with Security and Reliability Profiles 1.0 and migrations 001–008.

**What changes:** measurement contracts and representative workload models; valid benchmark design and statistical interpretation; HTTP, database, and runtime profiling; queueing, backpressure, caching, quotas, and load shedding; capacity, cost, and regression release decisions.

**What remains deliberately out of scope:** language benchmark contests; automatic Redis or Kubernetes prescriptions; production capacity claims from laptop evidence; optimization that weakens correctness or security.

**Outgoing boundary:** Performance Profile 1.0, migration 009, workload identities, benchmark evidence, HTTP and query optimizations, concurrency and cache policy, traffic controls, capacity models, and performance release gates. The outgoing handoff becomes the immutable starting point for Course 6.

## Course 6 — Event-Driven API Engineering

**Responsibility:** Extend the promise across asynchronous time.

**Governing question:** How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

**Incoming boundary:** The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

**What changes:** event taxonomy and ownership; AsyncAPI and CloudEvents contract architecture; delivery, ordering, partition, acknowledgement, outbox, and inbox semantics; schema evolution, replay, workflows, and event-time processing; event security, reliability, dead-letter custody, and governance.

**What remains deliberately out of scope:** teaching a broker before message semantics; claiming exactly-once delivery; event sourcing every domain; microservice decomposition.

**Outgoing boundary:** Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations. The outgoing handoff becomes the immutable starting point for Course 7.

## Course 7 — gRPC and Protobuf Engineering

**Responsibility:** Engineer typed internal invocation and streaming.

**Governing question:** How should typed internal capabilities be modeled and operated when remote calls can fail ambiguously, stream for long periods, and evolve across language boundaries?

**Incoming boundary:** The Course 6 HTTP API 1.2 and Analysis Events API 1.0 handoff with profiles and migrations through 012.

**What changes:** interaction-choice and ownership discipline; Protobuf semantic modeling and wire compatibility; unary metadata, status, deadlines, cancellation, and retries; bounded unary and streaming protocols; workload identity, authorization, health, discovery, generation, and governance.

**What remains deliberately out of scope:** replacing public HTTP or durable events; treating generated code as architecture; assuming RPC methods justify microservices; claiming a local TLS fixture is an operated trust system.

**Outgoing boundary:** Analysis RPC API 1.0, gRPC Profile 1.0, proto3 executable baseline, Edition 2024 frontier, migrations 013–015, streaming protocols, method policy, and compatibility evidence. The outgoing handoff becomes the immutable starting point for Course 8.

## Course 8 — Distributed API Architecture and Microservices Engineering

**Responsibility:** Distribute ownership deliberately.

**Governing question:** When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces?

**Incoming boundary:** The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015.

**What changes:** distribution economics and boundary fitness functions; service, contract, and data ownership; cross-service queries, projections, dependency budgets, and sagas; workload identity, routing, version skew, and release choreography; fault verification, strangler extraction, rollback, decommission, and merge-back.

**What remains deliberately out of scope:** service-per-table decomposition; shared-database microservices; gateway-owned business workflows; distribution as a maturity badge.

**Outgoing boundary:** Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief. The outgoing handoff becomes the immutable starting point for Course 9.

## Course 9 — GraphQL Schema and Runtime Engineering

**Responsibility:** Compose governed client-shaped capabilities.

**Governing question:** How can clients select graph-shaped data and operations without moving business ownership, authorization, cost, or consistency into an uncontrolled gateway?

**Incoming boundary:** The Course 8 distributed architecture handoff with explicit service, data, contract, and trust boundaries.

**What changes:** graph interface placement and operation lifecycle; type-system, nullability, resolver, source-ownership, and batching discipline; stable identifiers, connections, mutations, idempotency, and policy enforcement; persisted operations, demand control, caching, partial data, and observability; subscriptions, schema evolution, federation boundaries, and release governance.

**What remains deliberately out of scope:** direct database joins by the graph gateway; unbounded arbitrary query execution; using GraphQL to replace every existing interface; federation without ownership evidence.

**Outgoing boundary:** Analysis Graph API 1.0, GraphQL September 2025 schema, persisted operation registry, resolver ownership, demand policy, resumable subscriptions, compatibility gates, and platform-publication metadata. The outgoing handoff becomes the immutable starting point for Course 10.

## Course 10 — API Platform, Governance, and Developer Experience Engineering

**Responsibility:** Operate APIs as an organizational platform.

**Governing question:** How can an organization make trustworthy API work easier to discover, create, publish, consume, evolve, support, and retire without centralizing domain ownership?

**Incoming boundary:** The Course 9 handoff containing HTTP, event, RPC, distributed-service, and GraphQL contracts with explicit ownership and release evidence.

**What changes:** platform product and operating boundaries; catalog, ownership graph, immutable contract registry, and governance as code; consumer-aware lifecycle, exceptions, templates, and self-service; documentation, discovery, sandbox, SDK, SBOM, and provenance workflows; runtime reconciliation, product analytics, federated decision rights, and program final defense.

**What remains deliberately out of scope:** a portal as a substitute for authoritative metadata; gateway ownership of domain authorization; governance by average score or manual theater; claiming local fixtures are an operated enterprise platform.

**Outgoing boundary:** Analysis API Platform 1.0, a governed catalog and registry, lifecycle and policy engine, golden path, documentation and sandbox, SDK and provenance publication, runtime reconciliation, support model, and a ten-course graduation dossier. The outgoing graduation dossier closes the ten-course program.

## Why the order matters

The sequence prevents attractive shortcuts. Security comes before distribution because every remote edge creates another identity and authorization boundary. Reliability and performance come before service extraction because otherwise teams use microservices to hide unknown bottlenecks. Events and RPC precede microservices so a learner can choose an interaction model rather than default to synchronous HTTP. GraphQL follows ownership because a graph edge must not become permission for a gateway to join private databases. Platform engineering comes last because governance without trustworthy artifacts is theater.
