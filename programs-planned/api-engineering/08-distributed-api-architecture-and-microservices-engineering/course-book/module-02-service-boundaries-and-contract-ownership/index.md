# Module 02 — Service Boundaries, Bounded Contexts, and Contract Ownership

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** How do we draw service boundaries around cohesive decisions and language without turning tables, classes, or teams into accidental services?

## Where this module fits

Module 01 produced **Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services**. This module extends that result by asking: **How do we draw service boundaries around cohesive decisions and language without turning tables, classes, or teams into accidental services?**

The new capstone increment is **Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control**. It becomes the prerequisite for **Data Ownership, Replication, and Cross-Service Query Design**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Identify capabilities, invariants, and ubiquitous language that belong together.
- Separate business-service ownership from gateway, worker, and platform components.
- Assign one accountable owner to every public HTTP operation, event, RPC, and data set.
- Reject shared libraries that secretly preserve cross-service domain coupling.
- Design anti-corruption mappings between service-specific models.
- Recognize distributed-monolith boundaries before implementation begins.

## Capstone increment

Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control.

## A service owns decisions, not nouns

Nouns are easy to extract: Project, Dataset, Run, Artifact. Cohesive decisions are harder. `CreateRun` depends on project ownership, dataset readiness, algorithm policy, idempotency, capacity admission, and run-state initialization. Those rules form one capability even though they touch several nouns. A Run Service separated from Project and Dataset table services would call across the network to reconstruct a decision that was previously local.

A service boundary should contain a language and a set of invariants that can be understood together. In Analysis Control, “attempt,” “lease generation,” “run completion,” and “idempotency record” have precise meanings. Artifact Service has a different language: “staged object,” “published content,” “checksum,” “retention,” and “orphan.” Notification Service speaks about “subscription,” “delivery attempt,” “destination,” “retry schedule,” and “receipt.”

## Bounded contexts without ceremony

You do not need a large domain-driven-design vocabulary to use bounded contexts well. Ask three questions:

1. Does the same word mean different things here?
2. Which rules must be consistent in one transaction?
3. Which group can change this model without coordinating every release?

An artifact reference in Analysis Control is not the Artifact Service’s full object. It is a stable identifier and perhaps a checksum or state needed for the run representation. The Artifact Service’s internal object key, retention class, and storage backend are private. Mapping between those models is an anti-corruption layer, not duplication to be “cleaned up” through a shared package.

## Five kinds of component

The final topology distinguishes:

- **business service** — owns business decisions and canonical data;
- **edge component** — normalizes public protocols, identity, budgets, and routing;
- **compute plane** — performs scalable work under another service’s authority;
- **platform component** — provides technical capabilities such as discovery or telemetry;
- **data product or analytical consumer** — derives views without becoming transaction authority.

Calling all five “microservices” erases important responsibilities. The gateway and Worker Plane are separately deployed, but neither owns core business facts.

## Contract ownership

Every interface must have one contract owner and one implementation owner. The owners may differ from the caller.

| Interface | Contract owner | State authority |
|---|---|---|
| Public HTTP API 1.2 | API product owner | Analysis Control / Artifact Service by resource |
| Analysis Events API 1.0 | Analysis Control | committed source service |
| Analysis RPC API 1.0 | Analysis Control | method-specific owner |
| Artifact RPC/HTTP 1.0 | Artifact Platform | Artifact Service |
| Notification administration | Notification Platform | Notification Service |

Contract ownership includes compatibility, deprecation, examples, generated clients, and incident communication. It is not “the team that last edited the YAML.”

## Data ownership follows service ownership

The service catalogue assigns canonical facts:

```text
Analysis Control
  project
  dataset metadata
  run
  idempotency record
  job lease

Artifact Service
  artifact metadata
  content object
  retention state

Notification Service
  webhook subscription
  delivery attempt
  receipt history
```

A replicated run view inside Notification Service is not a second owner. It can be stale, rebuilt, or deleted and regenerated. The owner remains Analysis Control.

## Shared libraries: three categories

### Safe technical libraries

Logging, trace propagation, basic error envelopes, serialization helpers, and generated contract code can be shared if they contain no business policy.

### Risky semantic libraries

A package that contains `canCompleteRun`, `calculateArtifactRetention`, or `authorizeProject` can silently make multiple services co-own decisions. If two services need the same fact, expose a contract or replicate a view; do not distribute mutable policy as a package without an explicit governance model.

### Generated contracts

Generated OpenAPI, AsyncAPI, or Protobuf types are shared contract artifacts. They do not replace runtime validation or authorize access. Generated messages should not become persistence entities.

## Anti-corruption mappings

Suppose Artifact Service publishes:

```json
{
  "artifactId": "artifact-42",
  "runId": "run-9",
  "sha256": "...",
  "sizeBytes": 2048,
  "storageClass": "warm",
  "retentionUntil": "2026-10-01T00:00:00Z"
}
```

Analysis Control may only need:

```json
{
  "artifactId": "artifact-42",
  "sha256": "...",
  "state": "available"
}
```

The mapping protects both services. Control does not become coupled to storage classes. Artifact Service does not learn run-state transitions.

## The distributed-monolith test

A proposed service is probably part of a distributed monolith when:

- it cannot release without another service’s private change;
- it reads or writes another service’s database;
- it needs several synchronous calls for one local decision;
- shared domain libraries determine its behavior;
- a user-visible request fails if all services are not simultaneously available;
- ownership and on-call remain collective and ambiguous.

A network boundary with these properties adds failure without autonomy.

## Python and TypeScript implications

Both tracks implement `ServiceCatalog` and require one writer per fact. The TypeScript track uses `ReadonlySet` to make ownership declarations non-accidental. The Python track returns the exact owner or fails. This is intentionally stricter than a runtime that “usually” routes to the right service.

## Evidence required before Module 3

The catalogue must classify every component, assign one accountable owner, declare canonical data, and reject table-shaped services. You must be able to explain why Worker Plane is a deployment boundary but not a business-state boundary.

## A context map for the Analysis Runs Platform

A bounded context is a boundary within which terms, rules, and models have one coherent meaning. It is not automatically a process boundary. Course 8 uses contexts to clarify ownership before deciding deployment.

The platform has three business contexts and two supporting components:

```text
Analysis Control
    project policy, dataset metadata, run lifecycle,
    idempotency, leases, authoritative events

Artifact Management
    artifact identity, bytes, checksum, retention,
    publication, retrieval

Notification Delivery
    subscriptions, attempts, receiver state,
    retry policy, delivery evidence

Worker Plane
    execution capacity and attempt reporting;
    no authority over run truth

Edge Gateway
    protocol edge, routing, budget propagation,
    response composition; no business state
```

The same word may mean different things across contexts. In Analysis Control, an artifact reference means “the artifact attached to this completed run.” In Artifact Management, an artifact is a stored object with checksum, retention state, publication version, and access policy. The contexts exchange a stable artifact identifier rather than sharing one object model.

This translation is an **anti-corruption mapping**. It prevents Artifact Service storage concerns from entering the Control domain and prevents Control’s run model from becoming Artifact Service’s database schema.

## Contract ownership has two directions

A service owns the meaning and evolution of the interface it provides. Consumers own how they tolerate and use that interface. Neither side owns the other’s implementation.

For a synchronous interface:

```text
provider owns
    operation semantics
    request acceptance
    response and error contract
    compatibility policy
    availability objective

consumer owns
    deadline
    retry decision
    fallback behavior
    response tolerance
    feature negotiation
```

For an event interface, ownership is more nuanced. The event producer owns the fact and schema meaning. Each consumer owns its projection, acknowledgement, and side effects. A consumer must not reinterpret `AnalysisRunCompleted` as “a notification was delivered.” The event means only that Analysis Control committed completion.

For gRPC worker communication, Analysis Control owns lease authority and the method contract. A worker owns execution behavior but cannot turn an attempt report into authoritative completion by itself.

## Provider models are not shared domain models

Generated clients and schema packages are useful at the wire boundary. Problems begin when teams import provider domain classes or persistence entities into their own application model.

Bad shared package:

```text
shared-analysis-model
    RunEntity
    ArtifactEntity
    DeliveryEntity
    ProjectRepository
    RunStateMachine
```

This package creates coordinated changes and hides ownership. A consumer may start mutating a provider-owned type locally and expect the same invariant.

Acceptable shared artifacts are narrower:

1. generated contract types;
2. cross-cutting protocol utilities with no business decisions;
3. test fixtures and compatibility vectors.

Even generated types should stop at the adapter. Map them to consumer-owned concepts before applying business behavior.

```python
# Wire type received from Artifact Service.
wire = ArtifactResponse(...)

# Notification-owned projection.
summary = DeliveryArtifactSummary(
    artifact_id=wire.artifact_id,
    run_id=wire.run_id,
    available=wire.state == "published",
)
```

The mapping looks repetitive, but it is deliberate isolation. It allows each context to evolve without a hidden shared model.

## Five kinds of boundary in the capstone

The course distinguishes components that are often all called “services”:

### Business service

Owns business decisions and authoritative data. Analysis Control, Artifact Service, and Notification Service fit this definition.

### Edge component

Owns protocol concerns such as routing, normalization, and composition. The gateway is deployable but cannot decide whether a run may complete.

### Compute plane

Owns execution capacity and ephemeral attempt state. The worker plane scales independently but does not own the durable lease or final run state.

### Platform component

Provides infrastructure capability such as discovery, telemetry transport, or certificate issuance. It must not become a hidden business authority.

### Internal module

Maintains cohesion inside a service. Project policy and dataset metadata remain modules inside Analysis Control because their rules and transactions are strongly connected.

Calling each of these a microservice erases the distinctions that make architecture review possible.

## Contract surface area is an architectural cost

A boundary is not only the number of endpoints. Count:

- operations and event types;
- error categories;
- security claims;
- version combinations;
- timeout and retry policies;
- projection rules;
- migrations and backfills;
- runbooks and alerts;
- test fixtures;
- deprecation obligations.

A proposed split that turns three local method calls into twelve remote operations has expanded the permanent compatibility surface. The new surface must create enough independent value to justify that cost.

The capstone keeps the Artifact interface narrow:

```text
Store artifact under a bounded capability
Retrieve artifact under an authorized capability
Report publication fact
Manage retention under Artifact ownership
```

It does not expose the Artifact database as CRUD endpoints.

## The distributed-monolith diagnostic

A distributed monolith has process boundaries without decision independence. Common symptoms are:

- one release train for all services;
- a shared database or cross-database joins;
- synchronous call chains for every user action;
- shared domain libraries;
- gateway-owned business rules;
- one team approving every change;
- inability to test or run a service with contract substitutes;
- failures requiring coordinated restarts;
- “independent” services that cannot be rolled back independently.

Run this diagnostic before celebrating a repository split. The outcome may be to retain a modular monolith. That is a valid, often superior architecture.

## Worked contract decision: artifact upload

A worker needs to publish bytes produced for a specific run attempt. Three designs are possible.

### Design A — Worker sends user credentials

Artifact Service reuses the original end-user token. This extends a credential beyond its intended interaction, may outlive user context, and gives the worker unnecessary authority.

### Design B — Artifact Service calls Control for every upload

Artifact Service asks Control whether the upload is permitted. This creates a synchronous reverse edge and makes Artifact availability depend on Control at upload time.

### Design C — Control mints a narrow capability

The capability binds tenant, run, attempt, checksum, size, audience, and expiry. Artifact Service verifies it locally. This preserves owner authorization without a reverse synchronous call.

Course 8 selects Design C. The contract is owned by Artifact Service as verifier and Analysis Control as issuer under an agreed profile. A capability does not transfer run authority; it authorizes one bounded artifact effect.

## A boundary is complete only when deletion is understood

Creation paths are easy to design. Deletion exposes ownership ambiguity:

- Who decides an artifact is no longer referenced?
- Who applies retention holds?
- What if Control deletes a run before Artifact sees the event?
- Can Notification retain a delivery record after project deletion?
- Which service proves erasure?

The course requires each authoritative fact to have lifecycle ownership, not only creation ownership. Reconciliation and retention policies later depend on this decision.

## Module synthesis

You are ready to leave this module when you can **identify capabilities, invariants, and ubiquitous language that belong together, separate business-service ownership from gateway, worker, and platform components, and assign one accountable owner to every public HTTP operation, event, RPC, and data set** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Find and remove shared domain policies that would couple services** and requiring the following oracle: **Every business fact has one canonical writer, every interface has one owner, and no table-shaped service or shared domain policy survives.**

The cumulative platform now includes **Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Data Ownership, Replication, and Cross-Service Query Design](../module-03-data-ownership-replication-and-cross-service-queries/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
