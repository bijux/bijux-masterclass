# Module 10 — Incremental Extraction, Strangler Migration, and Final Architecture Defense

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** How do we extract services incrementally, preserve every existing contract, and retain a safe path to stop, roll back, or merge a service back into the platform?

## Where this module fits

Module 09 produced **Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects**. This final module consolidates the course by asking: **How do we extract services incrementally, preserve every existing contract, and retain a safe path to stop, roll back, or merge a service back into the platform?**

The capstone must now deliver **Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff** while preserving every earlier module result. Successful completion establishes the outgoing boundary for the next course or final program defense: **Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief.**

## Learning outcomes

- Sequence extraction from low-coupling evidence rather than organizational pressure.
- Use strangler routing, shadow comparison, and read/write cutover safely.
- Migrate data without uncontrolled dual writes.
- Define decommission, rollback, and merge-back criteria.
- Defend the final architecture against shared-database and distributed-monolith critiques.
- Publish a sanitized service and query boundary for GraphQL without bypassing service ownership.

## Capstone increment

Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff.

## Extraction is a migration, not a rewrite

The final module changes production ownership while preserving every contract built in Courses 1–7. The safe method is incremental: create a candidate behind the existing boundary, compare it, move one authority at a time, and keep a path to stop.

The course extracts Notification Delivery first and Artifact Delivery second. Analysis Control remains cohesive.

## Phase 0 — modular baseline

Before extraction, the modular implementation passes public HTTP conformance, event and RPC compatibility, security, reliability, performance, and reconciliation. Without a stable baseline, divergence cannot be attributed to the candidate.

## Notification extraction

### Shadow consumer

Replay retained completion and failure events into Notification Service with external deliveries disabled. Compare subscription selection, delivery identity, destination policy, retry classification, and final state with the legacy dispatcher.

### Cutover

Enable Notification Service as the only writer of delivery attempts. The legacy dispatcher remains deployable for the rollback window but consumes no new events.

### Rollback

Stop the new consumer, restore the legacy dispatcher at the recorded event position, and replay idempotently. Because run completion never called Notification synchronously, core state does not roll back.

### Decommission

Remove legacy delivery writes only after replay, retention, and incident evidence are complete.

## Artifact extraction

Artifact is harder because it owns bytes and participates in run completion.

### Backfill

Copy historical objects and metadata into Artifact Service using stable artifact ids and checksums. Backfill does not change Control authority.

### Shadow reads

For selected requests, read both legacy and candidate artifacts. Compare exact bytes, checksum, metadata, tenant authorization, range behavior, and latency. Return the legacy result until the comparison is clean.

### Move write authority

Workers receive upload capabilities and write only to Artifact Service. Avoid independent writes to legacy and candidate stores. Control stores references after Artifact Service publishes the owned fact.

### Cutover reads

Route a stable canary fraction to Artifact Service, observe correctness and resource limits, then cut over. Keep legacy read fallback only for the bounded rollback window.

### Orphan reconciliation

An artifact stored before a stale completion is not hidden. Reconciliation marks it orphaned and applies retention policy.

## Strangler routing

The reference `StranglerRouter` models legacy, shadow, canary, cutover, and decommissioned phases. Shadow always returns the legacy result while recording comparison. Canary selection is deterministic by key. Cutover requires a rollback target.

```python
router = StranglerRouter(legacy_read, artifact_service_read)
router.transition(ExtractionPhase.SHADOW)
result = router.call("artifact-42", "artifact-42")
assert router.shadow_clean()
router.transition(ExtractionPhase.CUTOVER)
```

A real router additionally records service version, route decision, latency, authorization outcome, and comparison reason.

## Decommission is a deliverable

A service extraction is incomplete while the old path still writes, hidden consumers read the old database, or operators maintain two runbooks indefinitely. Decommission includes:

- consumer inventory;
- old writer removal;
- data retention decision;
- credential revocation;
- route and DNS removal;
- dashboard and alert retirement;
- backup and restore ownership;
- incident ownership update;
- documentation and catalogue update.

## Merge-back is legitimate

Course 8 includes merge-back criteria. If Notification and Control always release together, one team owns both, event lag creates no value, and on-call cost exceeds isolation benefit, merging Notification back into the modular service may be the correct architecture. The event contract can remain useful even if deployment changes.

## Final architecture defense

The defense must answer:

- Why not Project Service?
- Why not a shared database?
- Why is Worker Plane not a state owner?
- What happens when Artifact Service commits but Control times out?
- How does a user get an artifact without trusting gateway headers?
- Which queries are authoritative and which are stale?
- Which old/new versions coexist?
- How is cutover reversed?
- How are orphans and missing notifications found?
- What evidence would justify the next extraction?

## Preparing Course 9

GraphQL will add client-shaped graph access. Course 8 exports a boundary brief so that graph resolvers do not read service databases directly or create unbounded fan-out. Safe roots name an authority, staleness policy, batch strategy, and field authorization. Partial data must be explicit.

## Course completion

You complete Course 8 only when:

- the predecessor handoff remains intact;
- service and data ownership are unambiguous;
- the synchronous graph is acyclic and bounded;
- the saga survives duplicate and ambiguous schedules;
- service capabilities reject authority confusion;
- supported version skew passes;
- shadow comparison is clean;
- rollback and merge-back exist;
- reconciliation is empty after the final workflow;
- the outgoing Course 9 handoff verifies exactly.

## The strangler pattern is controlled ownership transfer

A strangler migration is often drawn as a router gradually directing traffic to a new system. Routing is only the visible part. A complete extraction transfers:

- contract responsibility;
- write authority;
- historical data;
- operational ownership;
- security policy;
- release responsibility;
- failure recovery;
- decommission obligation.

Course 8’s extraction plan makes these transfers explicit.

## Phase-by-phase notification extraction

### Phase 0 — prove the modular baseline

Before moving anything, prove current behavior, event publication, replay, delivery semantics, security, telemetry, and capacity. Otherwise migration differences cannot be attributed.

### Phase 1 — shadow consumer

Notification Service consumes completion events and builds its own state, but legacy delivery remains authoritative. External effects are suppressed. Compare subscription selection, payload identity, retry classification, and receiver policy over a representative replay window.

### Phase 2 — establish one writer

Pause legacy creation of new delivery records. Record the event offset and ownership transition. Notification becomes the only writer. Legacy remains a bounded read/rollback path.

### Phase 3 — canary delivery

Route a deterministic tenant population to Notification delivery. Compare outcomes and observe lag, retries, security, and cost. Abort on semantic or cross-tenant mismatch.

### Phase 4 — full cutover

Route all delivery to Notification. Keep replay and reconciliation active. Rollback changes routing and consumption ownership without creating two writers.

### Phase 5 — decommission

Remove legacy write code, credentials, tables after retention, alerts, dashboards, and operational procedures. Update the service catalogue and threat model.

The extraction is incomplete until Phase 5.

## Artifact extraction has a harder data path

Artifact Service owns bytes and metadata, so migration includes content integrity and authorization.

A safe sequence:

1. create the new store and capability verifier;
2. import existing objects idempotently;
3. verify SHA-256, size, tenant, run mapping, and retention state;
4. shadow metadata and byte reads;
5. route new writes to Artifact only;
6. keep a bounded legacy read fallback if representation-compatible;
7. reconcile Control references and Artifact objects;
8. canary reads and downloads;
9. cut over all reads;
10. remove legacy storage authority after retention and rollback gates.

Uncontrolled dual write is forbidden. A controlled importer has one source population, stable import identity, checkpointing, and comparison evidence.

## Strangler routing state machine

The capstone’s routing model uses explicit phases rather than ad hoc percentages:

```text
legacy
shadow
canary
new-primary
decommissioned
```

Each transition has preconditions and a rollback target. `decommissioned` is intentionally not a quick reversible state; it requires evidence that old dependencies, data, and credentials are gone.

A route flag without ownership state is unsafe. If both old and new implementations can still write, switching reads does not complete migration.

## Cutover oracles

A cutover needs more than “error rate looks normal.” Compare:

- semantic result;
- authorization result;
- durable effect count;
- event identity and ordering;
- data checksum and version;
- partial/fallback behavior;
- latency and resource bounds;
- trace topology;
- reconciliation findings;
- support and incident signals.

For notification, external side effects complicate comparison. Use a controlled receiver or effect sink before live canary.

For artifacts, compare exact bytes and metadata under authorized and unauthorized cases.

## Decommission checklist

A legacy path is not gone when traffic reaches zero. Remove:

- route configuration;
- write code;
- database credentials;
- scheduled jobs;
- event consumers;
- backup and restore obligations;
- alerts and dashboards;
- secrets and certificates;
- data after retention and legal gates;
- documentation and runbooks;
- obsolete compatibility code.

Record which evidence permits each removal. Decommission reduces complexity only when obligations disappear.

## Merge-back criteria

The course keeps explicit reversal criteria:

- no stable owner emerges;
- releases remain coordinated;
- synchronous coupling grows;
- independent scale is unused;
- on-call cost exceeds isolation value;
- the service becomes a shared-library shell;
- incidents repeatedly cross the boundary without clear ownership.

Merging services can preserve separate modules and data ownership inside one deployable unit. It is not failure; it is an architecture correction.

## Final architecture defense

The learner must defend both extracted and retained boundaries.

For each service or component, answer:

```text
What business or platform responsibility does it own?
Which facts may it write?
Which contracts does it provide and consume?
Which synchronous dependencies are required?
Which asynchronous dependencies exist?
What is its failure-isolation value?
How is identity and tenant context validated?
How does it release with old and new neighbors?
How is its state reconciled?
Who operates it?
What would make us merge it back?
```

The defense must also explain why Project Service, Dataset Table Service, and Idempotency Service were rejected. An architecture is not mature if it can justify only additions.

## Final proof narrative

A strong final demonstration follows one run across all course layers:

```text
public HTTP request satisfies OpenAPI contract
→ Control commits run and outbox atomically
→ event contract carries the durable fact
→ worker invokes typed RPC under deadline and workload identity
→ Control mints a bounded artifact capability
→ Artifact stores exactly one checksum-bound effect
→ process manager completes only the current run attempt
→ Notification consumes completion independently
→ gateway returns an authoritative or explicitly partial view
→ traces and metrics preserve causal evidence
→ reconciliation reports no unexplained findings
→ old/new versions coexist through cutover
```

The learner then injects one failure after Artifact commit but before response, demonstrates idempotent recovery, and explains which service owns every decision.

## Preparing the GraphQL course

Course 9 will add a graph-oriented client interface. It must not dissolve the service boundaries established here. The outgoing handoff therefore includes:

- service catalogue;
- data ownership map;
- dependency graph;
- consistency and staleness policy;
- version ledger;
- GraphQL boundary brief.

GraphQL resolvers will call owner interfaces or read governed projections. They will not join private databases or become a new business authority.

## What mastery looks like

Completing Course 8 does not mean preferring microservices. It means you can:

- retain a modular monolith when distribution lacks evidence;
- extract a service incrementally when evidence is strong;
- preserve one writer per fact;
- design cross-service queries and workflows honestly;
- bound synchronous dependency cost;
- propagate identity without trusting headers;
- release across version skew;
- prove behavior under ambiguity and failure;
- decommission or merge a failed boundary.

That is the professional skill this course is designed to establish.

## Python and TypeScript implications

Both reference tracks implement the same extraction phases, stable route selection, shadow comparison, rollback guard, and reconciliation outcomes. Python makes phase transitions and comparison records explicit through enums and dataclasses. TypeScript uses discriminated string states and strict return types. The final defense compares the architecture and externally visible behavior, not identical internal class layouts.

In the primary track, add one failed transition and one rollback case. In the comparative track, review whether static types alone could prevent an unsafe dual writer or side-effecting shadow. They cannot; runtime ownership and proof remain necessary.

## Module synthesis

You are ready to leave this module when you can **sequence extraction from low-coupling evidence rather than organizational pressure, use strangler routing, shadow comparison, and read/write cutover safely, and migrate data without uncontrolled dual writes** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject candidate divergence and execute rollback before final cutover** and requiring the following oracle: **Public HTTP, event, and RPC contracts remain valid; extracted services own their data; Analysis Control remains cohesive; rollback works; final reconciliation is empty.**

The cumulative platform now includes **Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Complete the course final defense and outgoing handoff described in [Capstone](../capstone.md). Course 9 may treat only the manifested handoff as settled.
