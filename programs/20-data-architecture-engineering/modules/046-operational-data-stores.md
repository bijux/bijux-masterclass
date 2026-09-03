---
module_id: DARCH-046
program: Data Architecture Engineering
level: 1
module_number: 46
title: Operational Data Stores
status: complete
last_verified: 2026-09-03
---

# Operational Data Stores

## One-Page Review

### Governing question

When should an organization build an integrated current-state projection for operational reads and decisions, and how can it prevent that operational data store from becoming an ungoverned second system of record, a stale warehouse, or a hidden command path?

### Essential definitions

- An **operational data store (ODS)** is a governed, integrated, current-oriented projection designed to support bounded operational reads, coordination, reporting, or decisions across one or more authoritative sources.
- **operational authority** is the service or domain boundary entitled to accept a state transition and enforce its invariants.
- A **projection** is derived state built from authoritative facts, changes, snapshots, or queries for a declared consumer use.
- **applied position** is the greatest source position whose effects the ODS has durably and correctly incorporated for a declared partition and epoch.
- A **version fence** is the minimum source or product position a read must include before its result is usable for a decision.
- **staleness** is the difference between required or authoritative state and the state visible to a consumer under compatible version or time semantics.
- A **coherent cut** is a set of source positions whose combined state satisfies a declared cross-source observation contract.
- A **materialized read model** stores data shaped for reads while commands remain with authoritative services.
- A **tombstone** is durable deletion or invalidation evidence needed to prevent removed state from reappearing during replay or resynchronization.
- **degraded behavior** defines what consumers receive when freshness, completeness, consistency, or dependencies fall outside the contract.
- **reconciliation** compares the ODS with authoritative sources at compatible boundaries and drives governed repair.
- **operational projection authority** is accountability for publishing the ODS view; it does not transfer source command authority.

### Central model, mechanism, or theorem

Represent an ODS as:

`O = (decisions, sources, assertions, identity, acquisition, positions, integration, serving, freshness, consistency, failure, protection, ownership, evidence, lifecycle)`

Every ODS read identifies its source epochs and applied positions. A decision requiring minimum position vector `R` is ready only when the ODS applied vector dominates `R` for all required sources and product-level quality and protection gates pass. Low query latency cannot repair a stale or incoherent projection. Commands normally return to operational authorities; if the ODS accepts any write, its authority, synchronization, conflicts, recovery, and failure semantics must be designed explicitly.

### Critical invariants

- The ODS names authoritative sources and never becomes a command authority through consumer convenience alone.
- Every record has stable identity, grain, source lineage, source version or position, observation time, applied time, and correction behavior.
- Freshness is measured from authoritative change through consumer use, not from ODS query response time.
- Multi-source results declare whether they are independently latest, version-fenced, bounded-stale, causally related, or one coherent cut.
- Missing, duplicate, reordered, corrected, and deleted source effects are detectable and repairable.
- Consumers receive explicit stale, incomplete, unavailable, or partial states according to decision consequence.
- Read workload, ingestion, replay, reconciliation, backfill, and recovery cannot overload authoritative sources or one another without controls.
- Protection follows integrated fields, inferred relationships, histories, caches, APIs, replicas, exports, and operational users.
- Rebuild and failover preserve source epochs, positions, idempotency, tombstones, schema and rule versions, and consumer fences.
- Retirement removes feeds, tables, APIs, credentials, caches, jobs, alerts, catalog entries, and consumer dependencies while preserving required evidence.

### Common failures

Common failures are calling any replicated database an ODS; copying sources without operational decisions; writing corrections directly into the projection; using timestamps as total order; treating CDC rows as domain facts; bootstrapping without a log handoff; keeping only latest state when audit or replay needs history; discarding tombstones; joining independently fresh sources as one coherent present; measuring API latency instead of data age; returning stale eligibility as current; letting consumers poll unboundedly; replaying at full speed against production; reconciling only counts; granting broad access because the store is internal; exposing protected cross-domain relationships; building no degraded mode; allowing the ODS to become the only readable copy; dual-writing source and ODS; and never retiring the projection after its consumers move.

### Compact example

A support workflow reads Customer and Inventory through an ODS. Customer is applied through version 12; Inventory authority is at 29 but the ODS is at 27. The decision requires Customer 12 and Inventory 28. A five-millisecond query is not ready: the ODS reports Inventory stale, offers an authoritative fallback where permitted, and does not present the combined result as current. Telemetry records required and observed version vectors for diagnosis.

### Connections

[DARCH-004](004-systems-of-record-engagement-and-insight.md), [DARCH-005](005-operational-analytical-and-shared-data.md), [DARCH-036](036-change-data-capture-architecture.md), and [DARCH-040](040-choosing-an-integration-style-from-semantics-and-latency.md) establish authority, workload, capture, and integration foundations. API Engineering owns command and query interfaces; Data Engineering owns projection pipelines. This module defines the ODS boundary and prepares [DARCH-047](../ROADMAP.md) on streaming analytics architecture.

## Governing Question

Operational workflows often need a combined, low-latency view that no single source owns: a support agent needs customer, order, shipment, and entitlement state; a branch needs inventory and risk flags; a network operator needs topology and current alarms. Calling every source synchronously can be slow, fragile, expensive, or unable to reconstruct a coherent view.

An ODS materializes such a view. Its usefulness also creates danger: consumers begin treating it as authoritative, operators patch it directly, commands route around domain invariants, and stale integration errors become operational decisions. The governing question is which decisions justify the projection and which evidence makes each read safe enough.

## Why This Matters

PostgreSQL's [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html) documents extraction of changes from transaction logs, while its [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) documentation shows that visibility and concurrency claims depend on isolation semantics. Capture and storage mechanisms do not automatically define an ODS contract.

Microsoft's [CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) separates update and read models and describes synchronization consequences. The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) and [CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) describe request and event contracts that can feed or serve projections. Interface standards cannot assign business authority.

The W3C [PROV-O](https://www.w3.org/TR/prov-o/) recommendation supplies provenance concepts. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) explains retry and overload behavior across shared dependencies. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. An ODS must remain trustworthy during normal reads, lag, failure, correction, and retirement.

## Prerequisites and Retrieval

You should understand systems of record, domain boundaries, commands, queries, events, CDC, transactions, isolation, replication, caches, read models, consistency, freshness, identity, APIs, protection, recovery, and lifecycle.

Retrieve authority, projection, read model, source epoch, log position, applied position, watermark, version fence, coherent cut, staleness, idempotency, snapshot handoff, tombstone, replay, reconciliation, degraded mode, fallback, RPO, RTO, and retirement.

As a retrieval test, inspect “put a current customer view in the ODS.” Ask which workflow, customer identity, source assertions, minimum positions, time, useful age, joins, missing state, correction, protection, fallback, commands, consumers, service, and owner apply. “Current” is not a testable contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an ODS from a system of record, cache, replica, warehouse, event store, master-data hub, and analytical mart;
2. define operational decisions, source authority, identities, grain, time, versions, and projection contracts;
3. choose APIs, events, CDC, snapshots, or batch acquisition with safe bootstrap and replay;
4. specify applied positions, version fences, bounded staleness, coherent cuts, and consumer-visible readiness;
5. handle duplicates, ordering, gaps, deletes, late changes, source corrections, and resynchronization;
6. design read APIs, fallback, partial results, degraded modes, and workload isolation by decision consequence;
7. reconcile and repair integrated current state without bypassing source authority;
8. propagate purpose, minimization, authorization, derived sensitivity, retention, deletion, and audit;
9. assign source, ODS product, platform, consumer, operations, protection, and incident responsibilities;
10. plan incremental migration, failover, recovery, coexistence, review triggers, and verified retirement.

## Core Exposition

**Start with operational decisions.** Name the actor or system, decision, required assertions, maximum useful age, response deadline, error consequence, frequency, and fallback.

An ODS is justified when an integrated projection improves a current workflow enough to pay for synchronization and operational risk.

**Separate reads from commands.** The ODS normally answers queries. Commands return to the domain service that owns transitions and invariants.

A support screen may show an order and offer “cancel,” but cancellation calls the Order authority with current version and authorization rather than editing the projection.

**Define exceptions to read-only explicitly.** Some ODS designs accept annotations, workflow state, or reconciliation decisions.

Treat each write as a new authoritative domain or synchronized multi-writer problem. Define conflicts, transactions, propagation, audit, and failure instead of calling it harmless enrichment.

**Distinguish ODS from cache.** A cache accelerates access under an eviction and invalidation policy and may be rebuilt transparently. An ODS integrates governed state for named operational uses.

An ODS can use caches, but it needs product identity, semantic contracts, quality, consumers, and lifecycle beyond hit rate.

**Distinguish ODS from replica.** A replica reproduces one source's physical or logical state under replication semantics. An ODS often integrates several sources and reshapes them.

Replication can implement part of acquisition. It does not define cross-source identity, conformance, decision readiness, or correction.

**Distinguish ODS from warehouse.** An ODS emphasizes current or recent operational state, selective low-latency reads, and bounded workflow decisions. A warehouse emphasizes integrated analytical history and broad scans.

They can share products or platforms, but their freshness, consistency, history, workload, and failure contracts differ.

**Distinguish ODS from event store.** An event store preserves authoritative or recorded events and supports reconstruction. An ODS usually serves materialized current projections.

If the ODS retains only latest state, it cannot replace event evidence. If it stores history, define why and how it differs from analytical history.

**Distinguish ODS from master data.** A master-data capability governs shared identity, survivorship, and golden-record decisions. An ODS may consume mastered identities or expose current master projections.

Do not let a last-arriving ODS update become an implicit survivorship rule.

**Assign operational projection authority.** Name who owns the ODS assertion, source mapping, integration logic, freshness, service, correction, and consumer contract.

This authority permits publishing the projection, not accepting source-domain commands. Record the distinction in interfaces and incident procedures.

**Define source contracts.** For every input, record authority, schema or event version, key, grain, transaction boundaries, source epoch, positions, ordering scope, deletes, corrections, retention, service, and owner.

Private database layouts are weak contracts. Prefer stable APIs, events, or supported CDC products where feasible.

**Choose acquisition per assertion.** APIs fit bounded pulls and repair; domain events fit accepted occurrences; CDC fits physical state propagation; snapshots fit bootstrap; batches fit coherent low-frequency populations.

One ODS can combine methods, but shared identity, precedence, time, and release behavior must reconcile them.

**Design snapshot-to-change handoff.** Bind the initial population to a source log or event position, then apply later changes exactly according to the source contract.

Without a handoff, changes during snapshot can be lost or applied twice. Test source-specific visibility and retention.

**Track source epochs.** Positions compare only within compatible source histories. Failover, restore, reseed, or migration can create a new epoch.

Persist epoch with every checkpoint and row where needed. Reject apparent progress from an incomparable lineage.

**Track applied positions.** Separate received, durable, processed, applied, visible, and acknowledged boundaries.

One global offset can hide lagging partitions or sources. Expose vectors at the granularity relevant to consumer decisions.

**Use version fences.** A command response, event, or workflow step can supply the minimum version a subsequent ODS read must include.

The ODS may wait within a deadline, route to authority, return stale with evidence, or fail. It must not silently serve an older state as read-after-write.

**Define staleness precisely.** Express version or time distance from a named authoritative boundary for a population and percentile.

Wall-clock lag needs compatible clocks and event meanings. Position lag needs comparable epochs and partitions. Consumer useful age can differ from replication lag.

**Define multi-source consistency.** Independently latest source projections rarely form one global instant. State whether the decision accepts bounded skew, requires causal relationships, or needs a coordinated release.

For strict cross-source invariants, route the command or query to an authority capable of enforcing them instead of inferring them from asynchronous copies.

**Build coherent cuts where justified.** Use source snapshots, transaction positions, release vectors, event causal markers, or reconciliation barriers to establish compatible state.

Coherence costs latency and coordination. Require it only for decisions whose consequence justifies it.

**Resolve identity explicitly.** Integrate business keys, source IDs, mappings, merges, splits, reuse, confidence, valid intervals, and unresolved cases.

An ODS serving current workflows often cannot hide unknown identity in a generic member. Define safe partial or unavailable behavior.

**Define assertion precedence.** If two sources publish overlapping attributes, record authority by field, population, effective interval, and failure state.

Last arrival is not business authority. Preserve provenance so consumers and repair workflows can explain the chosen value.

**Model current and recent state.** Decide which historical changes, prior values, source positions, and correction evidence the ODS retains.

Current-only storage reduces volume but can make replay, audit, debugging, and consumer correction difficult. Retain the minimum justified evidence.

**Handle duplicates idempotently.** Use stable source event or transaction identity plus target effect semantics.

Payload equality is insufficient when two legitimate events share values. Retried deliveries must not double-apply counters or effects.

**Handle ordering by scope.** Define per-entity, partition, transaction, or global order requirements and the source evidence supporting them.

Buffer, reject, repair, or recompute out-of-order changes. Do not sort distributed facts solely by unsynchronized timestamps.

**Detect gaps.** Track expected sequences, source retention, partition activity, snapshot coverage, and reconciliation.

A quiet source and a broken feed can look identical. Heartbeats or control records need their own truth boundaries.

**Preserve deletes and tombstones.** A delete must remove or restrict current state and prevent older replay from resurrecting it.

Retain tombstones through the maximum replay and repair horizon, subject to protection and records policy. Propagate to caches and exports.

**Apply corrections.** Source correction can replace state, emit a corrective fact, or change authority. Identify affected ODS records and consumers.

Repair through governed source-aligned mechanisms. Direct target patches require provenance, approval, expiry, and convergence to source truth.

**Reconcile by keys and assertions.** Compare authoritative and ODS populations at compatible positions using missing, unexpected, duplicate, mismatched, stale, and unauthorized records.

Counts and totals can match while individual operational decisions remain wrong. Prioritize high-consequence keys and full periodic coverage.

**Design safe repair.** Quarantine corrupt changes, replay bounded positions, reload affected keys or partitions, or rebuild the projection.

Preserve source load budgets, idempotency, tombstones, rule versions, and consumer states. Validate before reopening decisions.

**Publish data readiness separately from service health.** An API can respond while inputs are stale or incomplete.

Expose source vectors, freshness, quality, incidents, and degraded mode in machine-readable responses or metadata appropriate to consumers.

**Define degraded behavior by decision.** Options include last-known state with age, partial fields, authoritative fallback, queued decision, manual review, conservative default, or unavailable.

Fail-open and fail-closed are consequence choices, not universal reliability rules. Avoid defaults that silently change business meaning.

**Design bounded authoritative fallback.** Direct source query can serve high-consequence stale cases but may overload the source during ODS failure.

Use quotas, circuit breakers, caching rules, admission control, prioritization, and source-owner agreements. Test correlated failure.

**Serve through stable interfaces.** Use APIs, query services, streams, or governed views with versioned schemas, authorization, consistency metadata, limits, errors, and deprecation.

Do not expose internal ODS tables as the only contract. Physical models should evolve without breaking workflows.

**Return version evidence.** Responses can include projection version, source positions, observed time, data age, quality or partial flags, and correlation IDs.

Do not expose sensitive infrastructure details. Provide enough evidence for callers to enforce fences and diagnose state.

**Control query shape.** Operational reads should have bounded keys, predicates, result sizes, concurrency, and deadlines.

Unbounded analytical scans belong on isolated products. Pagination over changing state needs snapshot or cursor semantics.

**Isolate workloads.** Separate ingestion, index updates, operational queries, reconciliation, replay, backfill, maintenance, and analytics through pools, queues, replicas, schedules, quotas, or stores.

Isolation protects freshness as well as latency. A repair that starves live application can deepen the incident.

**Protect sources from fan-out.** Multiple ODS consumers and fallbacks can amplify calls, retries, CDC slots, or event subscriptions.

Use shared projections where meanings align, connection and log-retention budgets, backoff, backpressure, and consumer registration.

**Protect the ODS from hot keys.** Skewed entities, tenants, or partitions can dominate locks, queues, indexes, and caches.

Measure distributions, shard or isolate where justified, bound per-key work, and preserve ordering and authority during mitigation.

**Define capacity for failure.** Include peak load, backlog catch-up, source outage, consumer retry, replay, resynchronization, regional failover, and reconciliation.

Average steady state is not an adequate operational model. Reserve or shed capacity by consequence.

**Apply purpose and minimization.** The ODS should contain only fields, histories, and populations required for named workflows.

Integrated current views can expose more about a person or organization than any source alone. Treat joins and inferred relationships as sensitive.

**Enforce row and field access.** Identity, tenant, role, purpose, field, and result policies must hold across APIs, views, caches, replicas, repair tools, and exports.

Do not rely solely on application filtering. Alternate paths and operational consoles require controls and audit.

**Control operational inference.** Existence, counts, status, timing, errors, and stale flags can reveal protected activity.

Design response shapes, denial behavior, rate limits, logs, and support tools with threat and purpose analysis.

**Propagate restriction and deletion.** Map subjects and source records to ODS projections, caches, replicas, exports, and backups while preserving required holds.

Deletion completion distinguishes current query exclusion, physical cleanup, backup expiry, and loss of recoverability.

**Observe end to end.** Correlate source changes, positions, ingestion, application, publication, queries, decisions, errors, corrections, and consumer outcomes.

Track lag distributions, gaps, duplicates, unresolved identities, mismatches, stale reads, fallbacks, source load, and repair duration.

**Avoid sensitive telemetry.** Keys, filters, payloads, and error messages can expose operational data.

Use opaque correlation IDs, scoped diagnostic access, redaction, retention, and audit while preserving enough evidence for repair.

**Set service objectives per product.** Define freshness, query latency, availability, completeness, correction, recovery, and authoritative fallback for declared workloads and failure states.

Measure at the consumer decision boundary. A broker, pipeline, database, and API can each be healthy while the decision is stale.

**Design recovery by responsibility.** Rebuild from authoritative snapshots plus retained changes or restore a protected ODS state and resume from compatible positions.

Restore schemas, mappings, rule versions, tombstones, checkpoints, policies, identities, indexes, caches, routes, and consumer fences.

**Test source loss and ODS loss separately.** Source recovery can invalidate epochs or replay history. ODS recovery can overload sources or expose partial state.

Exercise regional failure, corrupt projection, lost checkpoint, expired log, split traffic, and failed fallback. Reconcile before returning to normal.

**Assign incident authority.** Name who can pause ingestion, mark data unavailable, activate fallback, block consumers, repair state, approve resumption, and communicate.

Source, platform, ODS product, consumer, security, and privacy owners need clear handoffs. Shared urgency is not decision ownership.

**Track lifecycle cost.** Include source capture, storage, compute, network, indexes, APIs, operations, on-call, reconciliation, backfill, protection, incidents, migration, and retirement.

Compare with synchronous composition, source APIs, replicas, caches, events, and workflow redesign under the same outcomes.

**Migrate incrementally.** Inventory existing read paths, copies, reports, source calls, caches, consumers, decisions, versions, policies, and incidents.

Build one bounded projection, validate against authority, migrate consumer cohorts with version fences and rollback, then expand only with evidence.

**Bound dual reads.** Comparing source and ODS responses can validate migration but also doubles load and creates disagreement handling.

Define sampling, cutoffs, precedence, privacy, cost, decision behavior, exit criteria, and expiry. Do not let shadow traffic become permanent.

**Retire safely.** Stop feeds and queries, migrate consumers, revoke credentials and routes, remove tables, APIs, topics, slots, caches, jobs, alerts, catalogs, and infrastructure.

Preserve required provenance and incident evidence, propagate deletion, and verify no workflow depends on the old projection.

**Measure ODS value.** Track decision latency, stale-decision avoidance, source load reduction, workflow availability, correction time, reconciliation defects, protection incidents, change lead time, cost, and retired duplication.

Query count and low response time are insufficient. Value is safer operational decisions at justified lifecycle cost.

## Definitions and Notation

Represent ODS architecture as $O=(D,S,A,I,Q,P,V,C,F,Z,W,E,L)$, where $D$ is decisions, $S$ sources, $A$ assertions and authority, $I$ identity and integration, $Q$ acquisition, $P$ positions, $V$ serving, $C$ consistency and freshness, $F$ failure and recovery, $Z$ protection, $W$ ownership and workload, $E$ evidence, and $L$ lifecycle.

For required source-position vector $R=(r_1,...,r_n)$ and ODS applied vector $A=(a_1,...,a_n)$ within compatible epochs and scopes, readiness requires $A\succeq R$, meaning $a_i\ge r_i$ for every required source. This condition is necessary for the fence but does not prove semantic correctness, quality, protection, or cross-source coherence.

For source $i$, version lag can be $g_i=s_i-a_i$ only when positions are comparable and ordered. Time staleness needs compatible clocks and event boundaries; neither establishes consumer useful age alone.

Define `FitODS(O,d,t)` as a review predicate requiring justified operational decision $d$, explicit source and projection authority, compatible identities and positions, bounded freshness and consistency, correct integration, safe degraded behavior, effective protection, workload isolation, reconciliation and recovery evidence, supported ownership, alternatives, and lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every consequential ODS decision.

**1. Decision gate.** Name workflow, actor, effect, assertions, consequence, latency, useful age, consistency, fallback, owner, and alternatives.

**2. Authority gate.** Define source command boundaries, projection authority, overlapping assertions, precedence, writes, corrections, and escalation.

**3. Identity gate.** Define keys, grain, mappings, merges, splits, reuse, time, unresolved cases, provenance, and consumer behavior.

**4. Acquisition gate.** Define APIs, events, CDC, snapshots, batches, epochs, positions, handoff, duplicates, ordering, gaps, deletes, and replay.

**5. Readiness gate.** Define applied vectors, version fences, staleness, coherent cuts, quality, partial state, version evidence, and decision usability.

**6. Serving gate.** Define interfaces, schemas, queries, bounds, pagination, authorization, fallbacks, errors, caches, and deprecation.

**7. Protection gate.** Apply purpose, minimization, integrated and inferred sensitivity, row and field policy, regions, retention, deletion, egress, and audit.

**8. Operations gate.** Test workload isolation, fan-out, hot keys, capacity, backpressure, retry, observability, support, incidents, and cost.

**9. Recovery gate.** Exercise rebuild, restore, epochs, checkpoints, tombstones, policies, source loss, ODS loss, reconciliation, and resumption.

**10. Lifecycle gate.** Record evidence, migration, shadow reads, coexistence, rollback, review triggers, consumer closure, and verified retirement.

The executable example evaluates a version fence over two required sources.

<!-- bijux-verify: {"id":"ods-version-fence-readiness","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"customer_source_version=12\ncustomer_applied_version=12\ninventory_source_version=29\ninventory_applied_version=27\nrequired_inventory_version=28\nstale_sources=inventory\ndecision_ready=False\n","stderr":""}} -->
```python
source_versions = {"customer": 12, "inventory": 29}
applied_versions = {"customer": 12, "inventory": 27}
required_versions = {"customer": 12, "inventory": 28}

stale_sources = sorted(
    source
    for source, required in required_versions.items()
    if applied_versions.get(source, -1) < required
)
decision_ready = not stale_sources

print(f"customer_source_version={source_versions['customer']}")
print(f"customer_applied_version={applied_versions['customer']}")
print(f"inventory_source_version={source_versions['inventory']}")
print(f"inventory_applied_version={applied_versions['inventory']}")
print(f"required_inventory_version={required_versions['inventory']}")
print(f"stale_sources={','.join(stale_sources)}")
print(f"decision_ready={decision_ready}")
```

The result proves only that the declared applied vector fails one declared minimum-position fence. It does not prove source versions are comparable, applied effects are correct, the sources form a coherent cut, protection and quality pass, or the resulting decision is safe.

## Alternatives and Trade-Offs

**ODS versus synchronous API composition.** Materialization reduces request fan-out and isolates sources but introduces staleness and synchronization. Composition serves current source responses but couples latency and availability.

**ODS versus cache.** An ODS supports governed integrated semantics and repair. A cache can be simpler for one rebuildable source. Do not add product machinery without need.

**ODS versus replica.** A replica can serve one source efficiently. An ODS fits cross-source projections and consumer-specific structure at greater semantic responsibility.

**ODS versus warehouse.** An ODS optimizes bounded current operational reads. A warehouse supports historical analysis and broad scans. One platform can host separate products when isolation is proven.

**Events versus CDC acquisition.** Events expose deliberate domain facts but require producer design. CDC can capture source state changes with tighter physical coupling. Hybrid use needs precedence.

**Current-only versus retained recent history.** Current-only reduces volume and exposure. Recent history improves repair and diagnosis. Event or warehouse products may hold longer evidence.

**Independently fresh versus coherent multi-source state.** Independent progress lowers latency and coupling. Coherence protects cross-source decisions at coordination and delay cost.

**Stale response versus authoritative fallback.** Stale responses protect sources but may harm decisions. Fallback improves correctness while risking correlated overload. Choose by consequence.

**Shared enterprise ODS versus bounded domain projections.** Sharing reduces duplicate integration. Bounded projections preserve authority and blast-radius isolation. Standardize proven intersections.

**Build versus retire.** An ODS can be valuable during modernization and unnecessary afterward. Review triggers prevent transitional projections from becoming permanent by inertia.

## Failure Modes and Misconceptions

1. **Any replica is an ODS.** Integration, consumer semantics, service, and ownership distinguish the product.
2. **The ODS is the new system of record.** Projection authority does not grant command authority.
3. **Low response time means current data.** Data age and positions remain.
4. **One watermark proves every source is ready.** Partitions, epochs, and source vectors can differ.
5. **Latest from each source is one present.** Independent states may not form a coherent cut.
6. **CDC rows are stable domain facts.** Physical changes require accountable interpretation.
7. **A snapshot plus later changes cannot miss data.** Handoff position and isolation determine correctness.
8. **Timestamps provide total order.** Clocks and transaction scopes differ.
9. **Deleting current state prevents resurrection.** Replay needs durable tombstones and policy.
10. **Counts prove reconciliation.** Individual keys and assertions can disagree.
11. **Fallback always improves resilience.** It can overload already failing authorities.
12. **Read-only means low risk.** Operational decisions and integrated protected data can have high consequence.
13. **Internal users can read every field.** Purpose and least privilege still apply.
14. **A healthy API means a healthy ODS.** Inputs, quality, and freshness can fail independently.
15. **Replay should run as fast as possible.** Catch-up can starve live ingestion and sources.
16. **Dual reads are harmless validation.** They double load and require disagreement policy.
17. **Stopping ingestion retires the ODS.** Consumers, data, APIs, credentials, and obligations remain.

## Worked Examples

### Example 1

A support screen combines Customer, Order, Shipment, and Entitlement state but sends refund and cancellation commands to their authoritative services with version preconditions. **Conclusion:** integrated reads do not transfer command authority.

### Example 2

Customer is applied through version 12 while Inventory is at 27 and a reservation decision requires 28. The ODS marks the result stale despite a fast query. **Conclusion:** readiness is a vector, not response time.

### Example 3

A snapshot reads accounts while CDC continues. Binding the snapshot to a log position lets the projector discard covered changes and apply later ones without a gap. **Conclusion:** bootstrap needs an explicit handoff.

### Example 4

A restored source restarts sequence numbering under a new epoch. The ODS rejects numerical comparison with the old epoch and performs controlled resynchronization. **Conclusion:** positions need lineage.

### Example 5

Two sources disagree on customer risk. The contract assigns Fraud authority for risk and CRM authority for contact preference, rather than choosing the last arrival. **Conclusion:** precedence is semantic.

### Example 6

A deleted account reappears during a six-month replay because its tombstone expired after 30 days. Retention is extended beyond the replay horizon and old snapshots are protected. **Conclusion:** deletion and recovery must share time bounds.

### Example 7

During ODS lag, every client falls back to the primary Customer API and multiplies its load. Priority quotas, circuit breakers, and conservative degraded behavior preserve critical calls. **Conclusion:** fallback is a capacity design.

### Example 8

Counts match between Inventory authority and ODS, but keyed reconciliation finds one missing item and one unexpected stale item. The affected region is blocked and repaired. **Conclusion:** operational correctness is record-specific.

### Example 9

A low-privilege support user can infer a protected relationship from a combined household view unavailable in either source interface. The ODS minimizes fields and applies purpose-specific row policy. **Conclusion:** integration creates derived sensitivity.

### Example 10

After a service redesign removes the projection need, the team migrates consumers, stops feeds, revokes CDC slots and credentials, deletes eligible state and caches, removes APIs and alerts, and verifies no calls remain. **Conclusion:** an ODS can and should end.

## Cross-Program Connections

- **Data engineering:** snapshots, CDC, events, pipelines, idempotency, reconciliation, backfill, quality, and serving implement projections.
- **Database engineering:** transactions, isolation, logs, replicas, indexes, constraints, MVCC, queries, and recovery shape capability.
- **Distributed systems:** clocks, order, consistency, version vectors, retries, partitions, replication, convergence, and failure shape readiness.
- **API and service engineering:** commands, queries, schemas, versions, idempotency, authorization, quotas, errors, and deprecation govern interfaces.
- **Platform engineering:** paved paths, brokers, CDC, stores, identity, observability, workload isolation, capacity, and support enable operation.
- **Cybersecurity and privacy:** purpose, minimization, integrated sensitivity, row and field access, retention, deletion, egress, and audit constrain use.
- **Economics and operations research:** latency, capacity, queues, source load, opportunity cost, recovery, and retirement inform trade-offs.
- **Systems engineering:** requirements, interface control, failure analysis, verification, assurance cases, configuration, and closure structure trust.

## References

1. PostgreSQL Global Development Group, *Logical Decoding Concepts*. <https://www.postgresql.org/docs/current/logicaldecoding-explanation.html>
2. PostgreSQL Global Development Group, *Transaction Isolation*. <https://www.postgresql.org/docs/current/transaction-iso.html>
3. Microsoft, *CQRS Pattern*. <https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs>
4. OpenAPI Initiative, *OpenAPI Specification 3.1.1*. <https://spec.openapis.org/oas/v3.1.1.html>
5. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design an ODS for a customer-support workflow using Customer, Order, Shipment, Payment, and Entitlement sources. Define authority, identity, acquisition, positions, serving, degraded behavior, protection, and lifecycle.

### Exercise 2

Specify bootstrap, CDC application, gap detection, tombstone retention, replay, reconciliation, and rebuild for a source that can fail over to a new epoch.

### Exercise 3

Define version-fence and coherent-cut behavior for a workflow that reads Inventory, Price, Promotion, and Fraud state after an order command.

### Exercise 4

Design source protection, workload isolation, and fallback during an ODS incident with heavy consumer retries, replay backlog, and regional failover.

### Exercise 5

Plan migration from direct operational table reads to an ODS and later retirement after authoritative APIs can serve the workflow efficiently.

## Answers to the Exercises

### Answer 1

Name the support decisions: explain order state, estimate shipment, determine payment status, verify entitlement, and initiate bounded actions. Each source retains command authority. Define stable customer, order, shipment, payment, and entitlement identities; source precedence by assertion; current and recent history; business and observation times; source epochs and positions; useful-age and consistency requirements; unresolved identities; and correction.

Acquire domain events where stable facts exist, CDC for supported physical projections, APIs for repair, and positioned snapshots for bootstrap. Publish applied vectors, quality, and partial-state flags through a bounded authorized API. Commands call authoritative services with versions. Define last-known, queued, manual-review, authoritative-fallback, or unavailable behavior per consequence. Minimize cross-domain fields, restrict support roles and tenants, audit inference-sensitive access, propagate deletion, isolate queries and replay, assign source and ODS owners, test recovery, and define migration and retirement triggers.

### Answer 2

Obtain a source snapshot with declared transaction visibility and bind it to a log position in epoch E1. Load records idempotently with source keys, versions, schema, observation time, and provenance. Begin applying changes after the handoff position; track received, durable, applied, and visible positions per partition. Detect sequence gaps, inactive partitions, retained-log risk, schema changes, key changes, and duplicates. Preserve deletes as tombstones beyond the maximum replay and source-snapshot horizon, subject to holds and privacy policy.

On failover, detect epoch E2 and reject comparison with E1. Pause readiness claims, capture a compatible E2 snapshot and handoff, or use a verified mapping supplied by the source. Reconcile missing, unexpected, duplicate, mismatched, stale, and deleted keys at compatible boundaries. Throttle replay to protect live work, preserve rule versions, and validate before publication. A full rebuild restores mappings, policies, checkpoints, tombstones, indexes, and consumer fences, then receives accountable approval before normal service.

### Answer 3

The order command returns order version and causal references for inventory reservation, accepted price, promotion decision, and fraud decision where available. Define which assertions are immutable command outcomes and which remain independently changing current state. A confirmation view may require the exact accepted versions; a subsequent availability decision may require minimum current Inventory and Price positions with bounded Promotion and Fraud age.

Represent the requirement as a source-position and release vector with epochs. The ODS waits only within a deadline. If one fence fails, it returns explicit stale or partial evidence, routes a high-consequence check to an authorized source under quota, queues the workflow, or fails conservatively. It never merges independently latest values and calls them the command-time state. For decisions needing one coherent cross-source invariant, use the authoritative order workflow or a coordinated release, not inference from asynchronous projections. Log required and observed vectors and test partitions, lag, failure, and clock boundaries.

### Answer 4

Rank consumers and decisions by consequence. Apply admission control, per-consumer quotas, deadlines, bounded jittered retries, circuit breakers, backpressure, and load shedding. Reserve capacity for critical reads and live ingestion; isolate replay, reconciliation, backfill, analytics, and maintenance. Cap per-key work and identify hot tenants. Publish degraded state so clients do not retry ambiguous successes.

Fallback uses separate budgets agreed with source owners, request coalescing or bounded caching where safe, and priority routes; it stops before overloading recovering authorities. Replay resumes from durable checkpoints with idempotent effects, source log-retention monitoring, and rate limits based on source and target capacity. Regional failover fences old writers, preserves epochs and positions, restores policy and keys, and verifies routes. Observe end-to-end lag, retry amplification, fallback rate, source load, backlog age, gaps, quality, and consumer outcomes. Reconcile and obtain incident authority approval before returning traffic.

### Answer 5

Inventory every direct query, source table, field, join, consumer, workflow, credential, workload, snapshot behavior, decision consequence, policy, and owner. Define stable source contracts and the ODS projection contract. Build a bounded product with versioned identity, applied positions, readiness evidence, authorization, quality, reconciliation, service, recovery, and correction. Shadow selected direct reads under source budgets, compare equivalent positions and decisions, explain differences, and migrate cohorts with rollback.

Do not allow writes through the new read model. Revoke direct table access after acceptance and remove private-schema dependencies. Later, when authoritative APIs can compose the workflow within latency, availability, load, and policy bounds, compare them against the ODS under normal and failure scenarios. Move cohorts with explicit freshness behavior, stop ODS feeds, revoke CDC slots and credentials, remove tables, APIs, caches, jobs, alerts, catalogs, and infrastructure, preserve required evidence and holds, propagate deletion, and verify no observed or scheduled consumer remains.
