# Module 08 — Deployment Independence, Version Skew, and Release Choreography

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** How can services release independently while old and new clients, events, schemas, and database migrations coexist safely?

## Where this module fits

Module 07 produced **Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision**. This module extends that result by asking: **How can services release independently while old and new clients, events, schemas, and database migrations coexist safely?**

The new capstone increment is **Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence**. It becomes the prerequisite for **Distributed Verification, Fault Injection, and Operability**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish independent deployment from independent change and ownership.
- Model provider and consumer compatibility across HTTP, events, and gRPC.
- Design expand, migrate, observe, and contract release sequences.
- Support bounded version skew without permanent multi-version complexity.
- Use shadow and canary evidence before route cutover.
- Define rollback boundaries when data or messages have already changed.

## Capstone increment

Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence.

## Independent deployment is a tested property

A service is not independently deployable merely because it has its own pipeline. Independence exists when a new version can be released, observed, and rolled back without requiring simultaneous changes to callers, databases, or other services.

The course tests a bounded skew window:

```text
consumer 1.0 -> provider 1.0  compatible
consumer 1.0 -> provider 1.1  compatible
consumer 1.1 -> provider 1.0  compatible with feature disabled
consumer 2.0 -> provider 1.x  rejected
```

This is a policy, not a universal semantic-versioning law. Each interface type also has its own compatibility rules.

## Three release dimensions

### Interface evolution

HTTP, event, and gRPC contracts evolve under their established compatibility policies. A provider may add an optional field, but strict consumers and behavior changes still require evidence.

### Service implementation evolution

Internal code, dependencies, and deployment configuration may change without interface changes. The release gate still checks security, reliability, and performance profiles.

### Data schema evolution

Each service owns its migrations. Expand schema first, deploy compatible code, migrate data, remove old writers, then contract. One service must not require another service’s private migration to deploy.

## Mixed versions are normal

Rolling deployment creates a period when two provider versions are live. Callers may also lag. Tests must cover the matrix, not only the final version.

A new Artifact Service may support a new retention attribute. Old Control callers ignore it. New Control callers must continue operating when routed to an old Artifact instance, perhaps with the feature disabled. If the new caller assumes the field always exists, the rollout is not safe.

## Event versioning

Events can remain in retention long after producers upgrade. Consumers must process historical versions or use governed upcasters. Rewriting history silently invalidates audit and replay evidence.

During Notification extraction, the new consumer proves it can replay the retained Analysis Events API 1.0 history before cutover.

## Database release ownership

The old monolith had one migration sequence through 015. The distributed architecture starts service-owned histories. That does not erase history; it stops future services from sharing one migration train.

Artifact Service’s database can add a storage class without Analysis Control deploying. Notification Service can change delivery indexes independently. A platform catalogue records heads for visibility but does not execute every migration centrally.

## Shadow, compare, canary, cutover

A safe release sequence is:

1. deploy candidate with traffic disabled;
2. prove health and contract compatibility;
3. replay or backfill required state;
4. shadow representative traffic;
5. compare semantics, authorization, performance, and side-effect suppression;
6. canary a deterministic fraction;
7. observe SLO and reconciliation evidence;
8. cut over with rollback target retained;
9. remove old writers;
10. contract schema and decommission after the window.

Skipping shadow because unit tests pass ignores topology and real data shape.

## Rollback is not always code rollback

If the new service emitted a durable event, stored an artifact, or changed schema, reverting the binary may not restore the previous state. The rollback plan must state:

- which routes change back;
- which versions remain compatible;
- how new data is read by old code;
- whether a compensating migration is required;
- which external effects cannot be undone;
- how reconciliation determines completion.

## Release choreography versus central train

Independent services coordinate through contracts and supported skew, not a mandatory all-service release train. However, some cross-service changes still require choreography. Independence means the choreography is explicit and bounded—not that coordination disappears.

## Python and TypeScript implications

The shared `VersionPolicy` classifies the supported matrix. It deliberately rejects major-version mismatch and permits one minor-version feature gap. Real contract checks remain interface-specific; version numbers alone cannot prove compatibility.

## Evidence required before Module 9

Produce the old/new matrix, expand-and-contract sequence, shadow report, rollback route, and evidence that each service’s database can migrate without another service writing it.

## Build a compatibility matrix, not a version slogan

Semantic version labels are useful communication, but release safety depends on concrete producer-consumer combinations.

For every interface, test at least:

```text
old consumer → old provider
old consumer → new provider
new consumer → old provider
new consumer → new provider
```

For retained events, add:

```text
new consumer → historical old event
old consumer → additive new event during rollout
```

For database evolution, add old and new application versions against the expanded schema. A matrix row is supported only when executable or independently reviewable evidence exists.

## Worked additive change

Artifact Service 1.1 adds an optional `storageClass` field.

Safe sequence:

1. Add nullable storage column under Artifact ownership.
2. Deploy provider 1.1 that writes and returns the optional field.
3. Verify old consumers ignore it.
4. Deploy new consumers that tolerate absence.
5. Backfill when useful.
6. Observe mixed-version operation.
7. Require the field only in a later contract version after old writers retire, if ever.

Unsafe sequence:

1. Make `storageClass` required in the response and database.
2. Deploy new consumer first.
3. Assume all provider instances are upgraded.

Rolling deployment guarantees a period of skew. The unsafe sequence converts normal skew into failure.

## Contract dimensions differ

### HTTP/OpenAPI

Consider request acceptance, response tolerance, status codes, media types, security requirements, and behavior. An optional response field may still break strict consumers.

### Events/AsyncAPI

Consider retained history, producer and consumer upgrade order, partition keys, meaning, and replay. Removing or changing a fact’s meaning is more dangerous than adding metadata.

### gRPC/Protobuf

Consider wire compatibility, source compatibility, JSON mapping, generated code, unknown fields, and behavioral semantics. Reusing a field number is forbidden even if the field name looks internal.

A service release can touch multiple interface types. Each policy applies independently.

## Database expand-and-contract under service ownership

Each service owns its schema history. The platform catalogue records migration heads but does not run a global transaction across them.

A typical owner-local migration:

```text
expand schema
→ deploy code that reads old and new shape
→ deploy writers for new shape
→ backfill under stable identity
→ verify counts and semantics
→ remove old writers
→ contract obsolete shape
```

A cross-service release may depend on data migration completion, but one service must not reach into another database to “help.” The owner exposes a migration/import interface or executes the process itself.

## Version skew is bounded technical debt

Supporting old and new versions temporarily enables independent rollout. Supporting every historical version forever creates permanent complexity.

A version policy should define:

- supported current and previous versions;
- minimum consumer and provider versions;
- maximum coexistence window;
- deprecation evidence;
- telemetry showing active consumers;
- retirement owner;
- emergency extension process.

The capstone supports 1.0 and 1.1 during rollout and rejects a 2.x caller against 1.x providers. The exact numbers are illustrative; the discipline is the important part.

## Shadow comparison as release evidence

A useful shadow report includes:

```text
input population identity
current and candidate versions
semantic outcome comparison
authorization comparison
error classification comparison
side-effect suppression proof
latency and resource comparison
missing or uncomparable cases
sampled evidence links
```

A candidate with better p95 latency but one cross-tenant authorization mismatch is rejected. Correctness and security gates precede performance promotion.

## Canary and rollback

Canary routing limits exposure but does not make a release safe by itself. Define:

- deterministic population selection;
- maximum exposure;
- observation duration;
- SLO and error-budget guard;
- reconciliation checks;
- abort conditions;
- route rollback command;
- data and event compatibility after rollback.

Rollback may mean route reversal plus roll-forward repair. If a new service wrote data or emitted events, simply deploying the old binary can be unsafe.

## Event consumers and replay before cutover

Notification extraction requires more than consuming live events. The candidate must:

1. validate its contract against the retained event catalogue;
2. replay the required historical window;
3. build its projection deterministically;
4. compare with legacy delivery state;
5. prove duplicate and gap behavior;
6. process live tail without losing the handoff point;
7. cut over one writer;
8. retain a replay-based rollback route.

This is why Course 6 precedes distributed extraction. Event contracts and replay are migration mechanisms, not decorations.

## Independent deployment does not mean zero coordination

Some changes cross boundaries by nature. A new artifact capability profile may require issuer and verifier changes. Independence means:

- contracts define the overlap;
- rollout order is explicit;
- old/new coexistence is tested;
- one service can roll back within the overlap;
- coordination is bounded to the change, not every release.

A system that denies all coordination is unrealistic. A system that coordinates every release is a distributed monolith.

## Release ownership and evidence retention

Each service release should identify:

- service and contract versions;
- migration head;
- dependency versions exercised;
- compatibility matrix result;
- security, reliability, and performance profile result;
- shadow/canary evidence;
- rollback target;
- decommissioned paths;
- residual risk owner.

The platform release report aggregates these facts without becoming the authority for each service’s internals.

## Module synthesis

You are ready to leave this module when you can **distinguish independent deployment from independent change and ownership, model provider and consumer compatibility across HTTP, events, and gRPC, and design expand, migrate, observe, and contract release sequences** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove the old writer and contract only after the coexistence window passes** and requiring the following oracle: **Every supported pair preserves existing outcomes; unsupported major skew is rejected; rollback reads all committed data; no other service writes Artifact schema.**

The cumulative platform now includes **Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Distributed Verification, Fault Injection, and Operability](../module-09-distributed-verification-fault-injection-and-operability/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
