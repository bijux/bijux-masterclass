---
module_id: DARCH-055
program: Data Architecture Engineering
level: 2
module_number: 55
title: Registry, Consolidation, and Coexistence Styles
status: complete
last_verified: 2026-09-03
---

# Registry, Consolidation, and Coexistence Styles

## One-Page Review

### Governing question

How should an enterprise choose and combine registry, consolidation, and coexistence styles so that master-data authority, storage, reads, writes, synchronization, failures, and lifecycle obligations remain explicit for every domain and attribute?

### Essential definitions

- An **implementation style** is a durable allocation of authoring authority, persistence, integration, resolution, publication, correction, and operational responsibility.
- A **registry style** keeps master values authored and primarily stored in source systems while a central capability maintains identifiers, cross-references, linkage, and enough indexed data to resolve or assemble views.
- A **virtual view** is composed from registry and source data at request or near-request time rather than treated as one centrally authored record.
- A **consolidation style** ingests source assertions into a hub, resolves and persists master views for downstream use, while source systems remain authoritative for declared attributes.
- A **coexistence style** persists master views and divides authoring across hub and sources, synchronizing governed changes in both directions according to attribute and workflow policy.
- A **centralized transactional style** makes the master service authoritative for declared creation and mutation; it is a useful contrast but not the title focus.
- An **authority matrix** assigns originate, validate, correct, override, expire, and delete rights by domain, attribute, source, hub, and workflow.
- A **system of record** is authoritative for specified decisions and mutations; it is not simply the system holding a copy.
- A **system of reference** publishes governed representations for consumers without necessarily owning source mutation.
- **writeback** propagates an approved hub or mastered change into a participating source.
- **origin metadata** records where and why a change began so synchronization can avoid loops and false recency.
- A **style boundary** states which entities, attributes, relationships, consumers, times, and operations use a style.

### Central model, mechanism, or theorem

Represent style architecture as:

`S = (outcomes, domains, attributes, sources, authority, persistence, resolution, reads, writes, propagation, consistency, protection, service, ownership, evidence, lifecycle)`

Registry, consolidation, and coexistence are not maturity levels and need not apply to an entire enterprise. The choice follows authority and operational need. Registry centralizes identity and discovery while leaving value service distributed. Consolidation centralizes copies and mastered publication while leaving authoring distributed. Coexistence distributes authoring according to explicit attribute and workflow rules and therefore adds bidirectional synchronization. A legitimate hybrid can use registry for sensitive source detail, consolidation for analytical views, and coexistence for centrally approved status—provided every boundary has one clear mutation authority at a time.

### Critical invariants

- Every style decision names outcomes, domain, entity, attributes, relationships, source systems, consumers, consequences, owner, and exit.
- Storage location never substitutes for authoring authority; copied data does not become authoritative by proximity.
- Each attribute and operation has one unambiguous mutation authority at an effective time, even when several systems participate.
- Registry indexes retain source identity, linkage provenance, source availability, and visible partial-result semantics.
- Consolidated views retain source assertions, positions, effective and observation time, survivorship policy, freshness, and correction route.
- Coexistence changes carry origin, operation, version, authority, effective time, idempotency, propagation intent, and loop-prevention evidence.
- Initial snapshots and ongoing changes meet at a recorded boundary and are reconciled.
- APIs, events, files, virtual reads, caches, and embedded copies expose resolved version, freshness, completeness, failure, and compatibility.
- Protection follows source data, linkage indexes, central copies, derived views, synchronization payloads, logs, histories, exports, and backups.
- Recovery includes identities, sources, assertions, rules, mappings, offsets, pending work, permissions, and consumer state—not only current master rows.
- Style migration transfers authority and consumer contracts deliberately; it is not inferred from moving data.
- Retirement closes source access, central copies, writes, feeds, credentials, histories, consumers, and retained obligations.

### Common failures

Common failures are choosing a style from a vendor edition; calling registry low risk because it stores less data; hiding runtime source dependency behind a virtual view; treating consolidation as central authority; allowing corrections directly in a read-only hub; claiming coexistence while two systems can write the same field; using timestamps to settle write conflicts without clock and authority semantics; reingesting hub writeback as new source evidence; omitting origin metadata; mixing snapshots and changes without a boundary; replicating rows without policies and positions; synchronizing every attribute everywhere; exposing partial registry results as complete; measuring only hub uptime; replaying under current rules into live state; migrating storage before mutation authority; and retiring a hub while aliases, writeback, consumers, or histories remain.

### Compact example

A customer identifier stays registry-style: three source systems retain their records and the hub stores cross-references. A customer profile is consolidation-style: assertions are copied and a purpose-limited view is published, but corrections route to sources. Risk status is coexistence-style: a qualified central workflow authors the approved status and propagates it to sources with origin and version metadata. The styles coexist safely because the authority matrix has zero ambiguous attributes.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-051](051-master-data-and-golden-records.md), [DARCH-053](053-identity-resolution.md), and [DARCH-054](054-match-merge-and-survivorship.md) establish time, ownership, product, master, resolution, and action policy. This module allocates implementation responsibility; [DARCH-058](../ROADMAP.md) later deepens master-data change propagation.

## Governing Question

An MDM platform can store indexes, copies, golden views, workflows, and authoritative values at the same time. Those capabilities do not determine who is allowed to change legal name, product description, supplier status, address, relationship, or identifier. Architecture fails when product topology is mistaken for business authority.

The governing question is which combination of registry, consolidation, and coexistence improves named decisions while keeping mutation rights, runtime dependencies, lag, conflict, protection, recovery, cost, and exit observable. The answer can differ by domain, attribute, relationship, consumer, region, and lifecycle interval.

## Why This Matters

IBM's [InfoSphere MDM Technologies](https://www.ibm.com/docs/en/imdm/12.0.0?topic=overview-infosphere-mdm-technologies) distinguishes virtual, physical, and hybrid capabilities from the implementation styles those capabilities can support. IBM's [Technical Overview of Hybrid MDM](https://www.ibm.com/docs/en/imdm/11.6.0?topic=overview-technical-hybrid-mdm) contrasts distributed source maintenance with central persistence and combined designs. Product vocabulary is useful evidence, not a substitute for local authority decisions.

IBM's [Supported Hybrid MDM Scenarios](https://www.ibm.com/docs/en/imdm/12.0.0?topic=mdm-supported-hybrid-scenarios) shows that a solution can persist only selected views or attributes. [Before You Implement Hybrid MDM](https://www.ibm.com/docs/en/imdm/12.0.0?topic=mdm-before-you-implement-hybrid) emphasizes attribute ownership, while [Strategies for Loading Physical MDM Party Data](https://www.ibm.com/docs/en/imdm/12.0?topic=database-strategies-loading-physical-mdm-party-data) describes initial load and continuing synchronization. Microsoft [Master Data Management in Microsoft Purview](https://learn.microsoft.com/en-us/purview/data-governance-master-data-management) describes governed master products and golden records. These are implementation mechanisms, not proof that one style fits every domain.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides a vocabulary for provenance. The [OpenLineage Object Model](https://openlineage.io/docs/next/spec/object-model/) represents datasets, jobs, runs, and events. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) covers overload and retry amplification, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. Style selection changes dependency topology, failure propagation, and evidence needs.

## Prerequisites and Retrieval

You should understand master data, identity resolution, match and survivorship, source authority, identifiers, assertions, temporal modeling, APIs, events, bulk transfer, consistency, concurrency, caches, privacy, security, reliability, recovery, and governance.

Retrieve implementation style, registry, virtual MDM, index, cross-reference, virtual view, consolidation, physical copy, system of reference, coexistence, hybrid, centralized transactional, system of record, source authority, hub authority, attribute authority, writeback, origin, synchronization, snapshot, change stream, position, loop, conflict, reconciliation, migration, and retirement.

As a retrieval test, inspect “put customer MDM in coexistence mode.” Ask which customer entity, attributes and relationships, sources, current and future authoring authority, central persistence, read paths, write commands, propagation directions, consistency, conflicts, loops, failures, consumers, protection, recovery, migration boundary, and closure evidence apply. A mode label cannot answer those questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish implementation style from product capability, deployment topology, storage engine, and organizational maturity;
2. characterize registry, consolidation, coexistence, centralized transactional, and hybrid boundaries by authority and data flow;
3. create domain-, attribute-, relationship-, and operation-level authority matrices;
4. design registry indexes and virtual views with explicit source dependencies, partial states, latency, and protection;
5. design consolidated master products with snapshots, changes, survivorship, freshness, correction, and replay;
6. design coexistence synchronization with divided authorship, origin, versions, idempotency, conflicts, loops, and acknowledgement;
7. choose APIs, events, files, caches, and persistence according to consumer decision and consequence;
8. evaluate consistency, availability, capacity, recovery, protection, economics, and organizational readiness by style;
9. migrate between styles without ambiguous dual writes, silent consumer changes, or lost provenance; and
10. measure outcomes and verify succession or retirement across every dependency and obligation.

## Core Exposition

**Start with outcomes, not style names.** Name the entity-dependent decisions, consumers, deadlines, consequences, and fallback that justify shared mastering.

A virtual lookup may fit occasional support inquiry. A centrally approved sanctions status may require governed authoring and rapid propagation. One domain can contain both needs.

**Define the style boundary.** State entity types, attributes, relationships, operations, source systems, consumers, regions, purposes, and effective interval.

“Party uses registry” is too broad if identity links are registry-based, contact views are consolidated, and compliance status is centrally authored.

**Separate capability from style.** A platform may offer virtual matching, physical storage, workflow, APIs, events, and collaboration.

Those are technical capabilities. The implementation style is the allocation of authority and responsibility that uses them.

**Build an authority matrix.** For each attribute and relationship, assign rights to originate, validate, correct, override, expire, delete, approve, and publish.

Include workflow states and effective dates. An authority transition must not leave a period with two uncoordinated writers or no accountable writer.

**Separate storage from authority.** A hub can store a complete copy while a source remains authoritative. A source can cache a centrally authored value without gaining write rights.

Use explicit roles such as authoring system, evidence source, system of reference, replica, cache, analytical copy, and archive.

**Separate read and write paths.** Consumers may read one mastered representation while corrections and commands route elsewhere.

Document inquiry, search, bulk, command, correction, review, and exception paths. A convenient read endpoint should not accept unauthorized writes.

**Understand registry style.** Sources author and retain master values. The registry holds enterprise identifiers, source cross-references, match or link evidence, and enough indexed attributes to resolve entities.

Views can be composed from cached assertions or live source calls. Registry does not mean stateless; its identity graph can be critical and sensitive.

**Use registry when authority must remain distributed.** Regulatory, organizational, ownership, latency, migration, or source-specialization constraints may prevent central authoring or copying.

Registry can accelerate identity translation without moving every attribute. It is useful only if source contracts and runtime behavior meet consumer needs.

**Model source reachability.** A virtual view depends on source availability, latency, authorization, schema, identifier resolution, and semantic compatibility.

Define timeout, parallelism, circuit breaking, caching, partial results, required sources, and degraded behavior. Do not label a partial view complete.

**Control fan-out.** One registry lookup can trigger calls to many sources. Retries, slow tails, and large entities can amplify load.

Bound concurrency and deadlines, isolate sources, cache intentionally, apply backpressure, and prevent one failing dependency from exhausting the registry.

**Expose registry freshness.** Report registry index position and the source or cache time for returned attributes.

A current identity link does not make a source value current. Per-source and per-attribute evidence is more useful than one response timestamp.

**Protect the registry.** Cross-references reveal that records across contexts concern the same entity, which can be more sensitive than individual source fields.

Apply purpose limits, attribute and role controls, encryption, query limits, enumeration resistance, audit, retention, deletion, and incident handling to linkage indexes and access patterns.

**Correct at the authority.** If a source owns an attribute, a registry correction request routes to that source or its steward.

The registry may correct a link, cross-reference, or local metadata under its own authority. Do not patch a virtual value and present it as a source correction.

**Recover registry semantics.** Restore enterprise IDs, cross-references, match decisions, aliases, source positions, index configuration, source contracts, permissions, caches, and audit.

Rebuilding only from current sources may change historical links and lose retired identifiers. Preserve the evidence needed for stable resolution.

**Understand consolidation style.** Source systems remain authoritative for declared values, while a hub ingests assertions, standardizes, matches, applies survivorship, and persists mastered products.

Consumers read the hub instead of fanning out to sources. Availability and query performance improve while ingestion lag and central copies become explicit concerns.

**Use consolidation for governed downstream views.** Analytics, reporting, search, service, modeling, and cross-domain products often benefit from coherent persisted generations.

The hub becomes a system of reference, not automatically the system of record. Correction ownership remains with declared source authorities.

**Preserve assertions, not only selected rows.** Store source namespace and ID, original and transformed values, effective and observation time, ingestion position, status, quality, and provenance.

Without retained assertions, the hub cannot explain a golden value, rerun new policies, or distinguish source correction from selection change.

**Design initial load and change handoff.** Record snapshot time, source epoch, start and end positions, extraction filters, counts, and checksums.

Buffer or replay changes across the snapshot boundary so nothing is lost or applied twice. Reconcile sources, assertions, and mastered output after handoff.

**Define consolidation cadence.** Batch, microbatch, and streaming can all support consolidation. Choose by decision freshness, source capability, cost, recoverability, and coherent release needs.

Do not promise real time merely because events exist. Measure source-to-master and master-to-consumer lag by attribute and consequence.

**Publish immutable generations where useful.** A generation binds source positions, assertion set, reference versions, match policy, survivorship policy, overrides, schema, and output.

Consumers can reproduce or compare decisions. Incremental serving can still expose the resolved generation or entity version.

**Route corrections explicitly.** Consumers report bad source assertions, identity links, mappings, or survivorship outcomes to the owner of that decision.

The hub can carry a temporary governed override when authorized, but it must not become an unexplained shadow source.

**Avoid analytical writeback by accident.** A consolidated risk or segmentation view can inform decisions without being authorized to overwrite operational records.

Define whether derived attributes are advisory, centrally authored, or inputs to a source-owned workflow. Storage and usefulness do not establish mutation rights.

**Recover the whole consolidated product.** Restore raw and normalized assertions, positions, transformations, reference data, models and rules, golden generations, overrides, schemas, permissions, events, and audit.

An up-to-date master table alone cannot support explanation, replay, or safe correction.

**Understand coexistence style.** The hub persists master representations and owns some authoring decisions while sources own others. Approved changes propagate according to attribute and workflow rules.

Coexistence adds bidirectional or multidirectional synchronization. Its defining problem is not data movement but unambiguous authority during concurrent change and failure.

**Use coexistence when central decisions must return operationally.** Product approval, supplier status, global classification, or mastered contact correction may need to reach source applications.

Do not synchronize fields merely because the tooling can. Each writeback increases coupling, conflict, protection, testing, and retirement cost.

**Give one authority per mutation.** For attribute `risk_status`, a central qualified workflow may be the only writer while sources consume replicas. For `local_contact_note`, a regional source may remain writer.

Several systems can propose values; one governed process accepts the mutation. Proposal is not equivalent to authoritative write.

**Model commands and assertions separately.** A source can submit a proposed change with evidence. The hub approves or rejects it and publishes an authoritative result.

Conversely, a source-authored value can be ingested as an assertion without granting the hub permission to edit the source.

**Propagate origin metadata.** Carry origin system, source event, operation ID, authority, entity and attribute version, effective time, policy, and propagation purpose.

When the source re-emits an applied writeback, the hub recognizes the echo and records acknowledgement rather than treating it as independent new evidence.

**Prevent loops.** Without origin and version checks, hub-to-source updates return as newer source changes, trigger new survivorship, and oscillate.

Use stable event and operation IDs, expected versions, source positions, idempotency, echo suppression, and bounded retry. Monitor repeated values and direction changes.

**Define conflict semantics.** Concurrent proposals, stale writes, offline sources, and delayed events need rules based on authority, expected version, effective time, and workflow—not simple last-write-wins.

Return conflict or pending state, preserve both assertions, and route ambiguity. A later timestamp from a nonauthority cannot override an approved decision.

**Track propagation state.** Requested, accepted, applied, rejected, timed out, unknown, compensated, and reconciled are distinct.

Hub success does not prove source activation. Store acknowledgement by target and expose incomplete propagation to decision makers.

**Handle partial writeback.** One of ten sources may accept a new status while others fail or remain offline.

Choose whether the workflow pauses, compensates, continues provisionally, or completes with declared exceptions. Reconcile and retry without duplicating semantic changes.

**Avoid global transactions as fiction.** A local hub transaction can atomically update master state and an outbox. It cannot atomically commit arbitrary external sources.

Use durable workflow, idempotent consumers, acknowledgement, compensation where semantically valid, and reconciliation. State which completion level an API reports.

**Control coexistence queues.** Writeback bursts, slow sources, poison messages, retries, and large entity changes can exhaust capacity.

Partition fairly, cap attempts, use dead-letter or exception workflows, apply backpressure, and protect unrelated domains. Queue age is part of master freshness.

**Protect synchronization.** Authenticate sources and commands, authorize attributes and operations, validate schemas and values, encrypt transport, protect secrets, and audit changes.

A compromised source must not gain authority over hub-owned fields. A compromised hub can spread errors widely, so blast-radius and approval controls matter.

**Contrast centralized transactional style.** A central master service owns declared creation and mutation and publishes results to consumers.

This can simplify authority but creates a critical operational dependency and requires migration of business workflow, validation, latency, authorization, recovery, and support—not only central storage.

**Build hybrids by attribute and workflow.** Registry, consolidation, coexistence, and centralized operation can coexist within one domain when boundaries are explicit.

Avoid the word “hybrid” as a substitute for design. Publish the authority matrix, flow, service objective, failure behavior, protection, and exit for each slice.

**Treat relationships separately.** Entity attributes, source links, parent-child hierarchy, ownership, household membership, and account participation can use different styles.

A hub may consolidate profile attributes but leave legal ownership relationships at a registry source. Do not infer relationship authority from entity persistence.

**Choose consumer contracts by style.** Registry inquiry exposes source participation and partial states. Consolidation exposes generation and lag. Coexistence exposes authoritative version and propagation state.

Use typed errors, stable IDs, freshness, effective time, evidence appropriate to the consumer, and correction routes across all styles.

**Manage caches as replicas.** Record scheme, entity generation, source position, freshness, and invalidation policy.

Registry caches trade source dependence for staleness; consolidated and coexistence caches can obscure new master or propagation state. Define stale-if-error by consequence.

**Observe the whole flow.** Monitor source extraction, positions, candidate and match work, survivorship, registry calls, master persistence, events, writeback, acknowledgements, consumer activation, and correction.

Break down by domain, attribute authority, source, region, style, version, and error state. Hub uptime alone is weak evidence.

**Define service objectives by decision.** Include identity-resolution latency, source fan-out, master freshness, publication, writeback completion, correction, reconciliation, and recovery.

Registry may prioritize query latency; consolidation may prioritize bounded data lag; coexistence may prioritize authoritative propagation. All still need integrity and safe degradation.

**Design degraded behavior.** Registry can return partial results, cached results, or unresolved; consolidation can serve a marked stale generation; coexistence can queue commands or restrict writes.

Decide by consequence and maximum age. Never present degraded state as complete or broaden write authority to preserve availability.

**Plan source onboarding.** Define entity and identifier mapping, attribute semantics, authority, snapshots, changes, deletes, corrections, ordering, protection, service, and replay.

Profile and test before production. A successfully transferred file does not prove compatible meaning or complete population.

**Plan source offboarding.** Stop new authority at a recorded boundary, capture final changes, resolve pending work, migrate relationships, and preserve required history.

Remove source credentials, calls, writeback, caches, mappings, queues, alerts, and contracts only after consumers and retention owners agree.

**Migrate registry to consolidation deliberately.** Persist assertions and views, compare virtual and stored results, define freshness, preserve source correction paths, and migrate consumers.

Central copying does not transfer authorship. Keep sources authoritative until an explicit later authority transition.

**Migrate consolidation to coexistence deliberately.** Choose centrally authored attributes, establish commands and approval, stop source writes for those fields, and enable writeback with origin and version control.

Use shadow propagation, canaries, reconciliation, and rollback. The dangerous interval is ambiguous dual authority.

**Migrate away from coexistence deliberately.** Freeze or transfer central writes, drain and reconcile queues, identify last acknowledged versions, and move consumers and corrections.

Do not turn off writeback while sources still expect hub-owned state. Record the new authority effective time.

**Evaluate organizational readiness.** Registry needs reliable source ownership and service. Consolidation needs ingestion, stewardship, product, and consumer discipline. Coexistence also needs shared workflows and operational coordination.

Technology cannot repair unresolved decision rights. Escalation, funding, on-call, source change governance, and consumer obligations must exist.

**Evaluate economics.** Include source integration, copies, egress, match and survivorship compute, fan-out, workflow, writeback, review, incidents, compliance, recovery, migration, and exit.

A registry can cost more in runtime integration; consolidation can cost more in storage and lag management; coexistence can cost more in coordination and failure handling.

**Measure outcomes and harms.** Track decision improvement, false links, stale attributes, partial views, correction time, consumer adoption, write conflicts, loop suppression, propagation completion, incidents, and cost.

Counts of central records or integrated sources show activity, not fitness. Tie style evidence to consumer outcomes.

**Plan succession and retirement from launch.** Define export of identifiers, cross-references, assertions, mappings, rules, positions, histories, pending work, permissions, and consumer bindings.

Retire only after authority transfers, consumers migrate, queues close, access is revoked, retained evidence has custody, prohibited copies are removed, and restore cannot resurrect unsupported behavior.

## Definitions and Notation

For domain attribute $a$, define authority assignment:

$$
A(a,t)=(originator,validator,corrector,overrider,expirer,deleter,publisher)_t.
$$

At each effective time, a mutation type has one accountable authority even when proposals and replicas exist elsewhere.

Represent a style slice as $s=(D,E,K,R,W,P,C,F)$ for domain $D$, entity type $E$, governed attributes or relationships $K$, read path $R$, write path $W$, persistence $P$, consistency contract $C$, and failure behavior $F$.

Registry commonly has central identity persistence and distributed value reads; consolidation adds central assertion and view persistence without transferring source writes; coexistence adds governed central writes and propagation for selected $K$.

For propagated change $e=(op,origin,authority,id,k,v,p,t_e,t_o)$, stable operation, origin, authority, entity, attribute, value, prior version, effective time, and observation time support idempotency, conflict detection, and loop suppression.

Define `FitStyle(S,u,t)` as a review predicate requiring justified outcomes, explicit boundaries and authority, preserved provenance, appropriate persistence and contracts, controlled propagation, protected and recoverable service, measurable value, and lifecycle closure for use $u$ at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name entity decisions, consumers, deadlines, harms, fallback, value, and assurance depth.

**2. Boundary gate.** Define domain, entity, attributes, relationships, sources, regions, purposes, operations, consumers, time, and excluded uses.

**3. Authority gate.** Assign originate, validate, correct, override, expire, delete, approve, and publish rights without ambiguous dual writers.

**4. Registry gate.** Define index content, source contracts, virtual assembly, fan-out, partial results, caches, source correction, link protection, and recovery.

**5. Consolidation gate.** Define assertion persistence, snapshot-change boundary, survivorship, generations, freshness, source authority, correction, replay, and recovery.

**6. Coexistence gate.** Define central attributes, proposals, commands, origin, versions, idempotency, conflicts, loops, writeback states, acknowledgement, and compensation.

**7. Contract gate.** Publish APIs, events, files, reads, writes, effective time, consistency, degraded states, corrections, reconciliation, and consumer obligations.

**8. Protection and service gate.** Bound linkability, access, integrity, licenses, latency, freshness, capacity, queues, incidents, recovery, retention, and deletion.

**9. Migration gate.** Transfer storage, authority, write paths, consumer contracts, positions, pending work, histories, and rollback through explicit effective boundaries.

**10. Lifecycle gate.** Assign ownership, measure outcomes and cost, onboard and offboard sources, transfer custody, migrate consumers, and verify retirement.

Passing these gates supports one style slice. It does not prove an entire domain shares that style, central storage creates authority, a registry is low risk, or coexistence has globally atomic writes.

### Executable evidence

The executable example classifies three attribute slices and checks that their declared authoring authority is unambiguous.

<!-- bijux-verify: {"id":"attribute-scoped-mdm-styles","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"customer-identifier=registry\ncustomer-profile=consolidation\nrisk-status=coexistence\nambiguous_authority=0\nsource_systems=3\narchitecture=attribute-scoped\n","stderr":""}} -->
```python
slices = {
    "customer-identifier": {
        "hub_persists_values": False,
        "hub_authors": False,
        "writers": {"sources"},
    },
    "customer-profile": {
        "hub_persists_values": True,
        "hub_authors": False,
        "writers": {"sources"},
    },
    "risk-status": {
        "hub_persists_values": True,
        "hub_authors": True,
        "writers": {"approved-hub-workflow"},
    },
}


def style(spec):
    if spec["hub_authors"]:
        return "coexistence"
    if spec["hub_persists_values"]:
        return "consolidation"
    return "registry"


for name, spec in slices.items():
    print(f"{name}={style(spec)}")

ambiguous = sum(len(spec["writers"]) != 1 for spec in slices.values())
print(f"ambiguous_authority={ambiguous}")
print("source_systems=3")
print("architecture=attribute-scoped")
```

The result proves only the declared Boolean classification and writer-cardinality check for three in-memory slices. It does not prove that the style labels fit a real domain, that writers are truly authoritative, or that source contracts, persistence, synchronization, consistency, protection, recovery, economics, and consumer outcomes are adequate.

## Alternatives and Trade-Offs

**Registry.** Minimizes central value persistence and preserves distributed source authority; runtime source dependency, fan-out, partial views, linkability, and source service quality remain.

**Consolidation.** Provides coherent persisted views and decoupled reads; copies, ingestion lag, replay, correction routing, and false impressions of central authority grow.

**Coexistence.** Supports centrally approved operational values alongside source-owned attributes; conflicts, loops, queues, writeback failures, and organizational coordination are substantial.

**Centralized transactional.** Clarifies declared master writes and can simplify convergence; it creates a critical service and demands migration of operational workflow and availability responsibility.

**One style per domain.** Documentation is simpler, but attribute authority and consumer needs can be misrepresented.

**Attribute-scoped hybrid.** Fits real authority and consequence more closely, at the cost of more contracts, mappings, observability, and governance.

**Live virtual views.** Offer current source data when sources respond; tail latency, outages, schema drift, access, and inconsistent read times complicate use.

**Cached virtual views.** Improve resilience and speed while adding staleness, invalidation, and replica semantics.

**Streaming consolidation.** Reduces lag but raises ordering, duplicate, replay, capacity, and source-event contract demands.

**Versioned batch consolidation.** Produces coherent reproducible generations while accepting bounded delay and batch recovery costs.

**Synchronous writeback.** Gives callers immediate target feedback but couples command latency and availability to sources.

**Asynchronous writeback.** Decouples services and absorbs bursts while requiring pending states, acknowledgement, reconciliation, and consumer tolerance.

Choose by authority, decision latency, source capability, consumer contract, consistency, failure consequence, protection, organizational readiness, cost, migration, and exit.

## Failure Modes and Misconceptions

1. **Implementation style is a product setting.** It is an authority and responsibility design implemented with capabilities.
2. **One domain needs one style.** Attributes, relationships, operations, and consumers can justify different slices.
3. **Storage location determines the system of record.** Mutation authority is declared, not inferred from copies.
4. **Registry stores no sensitive data.** Cross-references and link evidence can be highly sensitive.
5. **Virtual means always current.** Sources, caches, indexes, and request times can differ.
6. **A complete registry response means all sources answered.** Completeness must be explicit.
7. **Consolidation transfers authority.** It centralizes assertions and views unless writes also move.
8. **Hub correction fixes source data.** Source-owned errors require an authoritative correction path.
9. **Coexistence means both systems may write.** Each mutation still needs one authority.
10. **Last write wins resolves authority.** Clock order cannot replace business decision rights.
11. **Writeback success at the hub means source activation.** Target acknowledgement and reconciliation are required.
12. **Idempotency prevents loops.** Origin, version, direction, and echo semantics are also needed.
13. **Events guarantee real time.** Backlogs, outages, retries, and consumer activation create lag.
14. **Replication provides recovery.** Rules, positions, identities, histories, permissions, and pending work also matter.
15. **Hybrid means flexible.** Unspecified hybrid boundaries are ambiguity, not architecture.
16. **Changing style is a data migration.** It also transfers authority, workflows, contracts, failures, and ownership.
17. **Hub uptime proves master availability.** Registry sources or coexistence queues may be unhealthy.
18. **Turning off the hub completes retirement.** Source calls, writeback, IDs, copies, consumers, histories, and obligations remain.

## Worked Examples

### Example 1

A hospital registry links patient identifiers while clinics retain and serve clinical demographics because mutation and protection remain local. The response marks an unavailable clinic as partial. **Conclusion:** registry preserves source authority and runtime dependency.

### Example 2

A support view fans out to twelve systems. Per-source deadlines, bounded concurrency, caches, and partial-result metadata stop one outage from exhausting the registry. **Conclusion:** virtual assembly is a distributed service.

### Example 3

Supplier records are consolidated nightly for reporting while procurement systems remain authoritative. A steward routes a bad tax identifier to procurement instead of editing the reporting copy. **Conclusion:** system of reference is not system of record.

### Example 4

A snapshot at source position 500 is loaded while changes 501 onward are buffered and replayed before reconciliation. **Conclusion:** initial load and ongoing change need an explicit handoff.

### Example 5

Risk status is approved centrally and sent to regional systems with operation, origin, entity version, and effective time. Returning echoes become acknowledgements rather than new assertions. **Conclusion:** coexistence requires loop-aware provenance.

### Example 6

Two sources concurrently propose different product names, but only the global product workflow may accept that attribute. Both proposals remain evidence while one approved version publishes. **Conclusion:** distributed proposals do not imply distributed authority.

### Example 7

Nine sources accept a writeback and one is offline. The master reports `partially_propagated`, blocks a dependent high-risk workflow, and reconciles the final source later. **Conclusion:** distributed completion must be typed.

### Example 8

A domain uses registry for protected source details, consolidation for analytics, and coexistence for approved classification. The authority matrix names one writer per attribute. **Conclusion:** a precise hybrid can be safer than a false single label.

### Example 9

Migration from consolidation to coexistence shadows writeback before disabling source edits for hub-owned fields at a recorded time. **Conclusion:** authority transfer, not copying, marks the style change.

### Example 10

An old hub has no consumers but still owns alias resolution, two pending writebacks, historical generations, and recovery credentials. **Conclusion:** retirement requires state, dependency, and custody closure.

## Cross-Program Connections

- **Data engineering:** source contracts, snapshots, change capture, temporal assertions, consolidation, events, offsets, reconciliation, replay, and deletion implement style flows.
- **Platform engineering:** service discovery, identity, workflow, APIs, eventing, caches, storage, policy, observability, recovery, isolation, and paved migration support operation.
- **API and service engineering:** inquiry, commands, operation resources, typed partial states, expected versions, idempotency, events, correction, and deprecation shape contracts.
- **Security and privacy:** linkage, purpose, source and command trust, field authority, access, enumeration resistance, audit, retention, deletion, and incident scope change by style.
- **Reliability engineering:** fan-out, tail latency, retries, queues, backpressure, partial writes, stale reads, failover, recovery, and reconciliation define behavior.
- **Organizational design:** source, domain, hub, workflow, steward, consumer, platform, incident, and retirement decision rights determine actual authority.
- **Analytics and machine learning:** persisted generations aid reproducibility while identity and attribute versions, feedback, feature freshness, and correction still require contracts.
- **Economics and decision science:** integration, runtime calls, copies, egress, coordination, incident loss, review, migration, and exit cost distinguish styles.
- **Enterprise architecture:** systems of record, reference, engagement, analysis, and archive need explicit responsibilities rather than labels inferred from topology.
- **Systems engineering:** stakeholder outcomes, interfaces, configuration control, hazards, evidence, lifecycle, and verification frame style assurance.

## References

1. IBM, *InfoSphere MDM Technologies*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=overview-infosphere-mdm-technologies>
2. IBM, *Technical Overview of Hybrid MDM*. <https://www.ibm.com/docs/en/imdm/11.6.0?topic=overview-technical-hybrid-mdm>
3. IBM, *Supported Hybrid MDM Scenarios*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=mdm-supported-hybrid-scenarios>
4. IBM, *Before You Implement Hybrid MDM*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=mdm-before-you-implement-hybrid>
5. IBM, *Strategies for Loading Physical MDM Party Data*. <https://www.ibm.com/docs/en/imdm/12.0?topic=database-strategies-loading-physical-mdm-party-data>
6. Microsoft, *Master Data Management in Microsoft Purview*. <https://learn.microsoft.com/en-us/purview/data-governance-master-data-management>
7. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
8. OpenLineage, *Object Model*. <https://openlineage.io/docs/next/spec/object-model/>
9. Google, *Site Reliability Engineering: Addressing Cascading Failures*. <https://sre.google/sre-book/addressing-cascading-failures/>
10. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design implementation styles for a customer, supplier, product, or asset domain. Define at least three attribute or relationship slices and justify registry, consolidation, coexistence, or centralized authority for each.

### Exercise 2

A registry-style customer view must query eight sources, two of which are slow and one intermittently unavailable. Design latency, partial-result, cache, protection, and recovery behavior.

### Exercise 3

A consolidated supplier product is updated nightly, but consumers need urgent compliance corrections within fifteen minutes. Design authority, ingestion, overrides, publication, and reconciliation without silently creating coexistence.

### Exercise 4

An organization will move product classification from source-owned consolidation to centrally authored coexistence. Design the authority-transfer and writeback migration.

### Exercise 5

An MDM hub uses all three styles and is being replaced. Define evidence that identities, values, authority, propagation, consumers, and obligations have transferred or ended.

## Answers to the Exercises

### Answer 1

Begin with decisions, entity scope, sources, consumers, deadlines, and consequences. Build an authority matrix per attribute and relationship. Customer source identifiers can be registry-style when source systems retain identity records and the hub needs cross-reference only. A contact profile can be consolidation-style when sources author values but support and analytics need a persisted purpose-limited view. Compliance status can be coexistence-style when a central qualified workflow accepts the authoritative value and operational sources must receive it. A product creation command can be centralized if the master service truly owns the workflow and availability.

For every slice define persistence, source and hub writes, reads, effective and observation time, origin, propagation, consistency, failure, correction, protection, recovery, consumer contract, owner, cost, and exit. Preserve assertions and provenance across all styles. Ensure exactly one authority per mutation at a time; multiple proposers or replicas do not violate that rule. Document cross-slice relationships so a change in one style cannot silently overwrite another. Test snapshots, changes, partial state, loops, stale writes, replay, recovery, and migration before accepting the design.

### Answer 2

Classify sources as required or optional for each consumer decision. Give the entire request a deadline and each source a smaller budget; issue calls with bounded concurrency, per-source isolation, circuit breakers, retry budgets, and backpressure. Avoid multiplying retries across client, registry, and source. Cache only declared attributes with source identity, observed time, expiry, and invalidation rules. A stale-if-error response includes source, age, and degraded status and is allowed only for decisions whose consequence accepts it.

Return typed completeness: complete, partial with missing sources, cached, unresolved, or unavailable. Do not fill missing fields with ordinary nulls. Expose registry index generation separately from source-value freshness. Protect cross-references, query purpose, source credentials, cache, logs, and enumeration surfaces. Monitor fan-out, latency, error, cache age, source availability, and decision outcomes. Recovery restores IDs, link history, source contracts, indexes, permissions, and safe caches; test that the view resolves stable IDs after restore even when sources remain unavailable.

### Answer 3

Keep supplier systems authoritative. Establish a streaming or frequent change route for the compliance source, separate from the nightly general snapshot, with source positions, effective time, validation, idempotency, and a fifteen-minute source-to-master objective. Publish an incremental master version or urgent coherent release and notify consumers. The hub remains a system of reference because it does not originate the compliance status.

If a source correction cannot arrive within the required window, define a temporary governed override owned by the appropriate compliance authority. Record source assertion, override value, reason, evidence, approver, scope, effective interval, expiry, and precedence. This does not grant general hub authorship or write back to sources. Reconcile when the authoritative source correction arrives, retire the override, compare views, and confirm consumers activated the corrected version. Monitor staleness and fail closed or queue high-consequence decisions if both source and authorized override are unavailable.

### Answer 4

Define precisely which classification attributes and operations move, the central decision owner, regional proposal rights, effective transfer time, consumers, and fallback. Build versioned commands, approval workflow, reference mappings, outbox events, source adapters, operation identity, origin, expected versions, effective time, idempotency, acknowledgement, conflict, retry, and reconciliation. Establish source permissions that accept hub-approved changes but reject unauthorized central edits to source-owned fields.

Shadow central decisions and writeback without activating source changes; compare values, latency, conflicts, queue load, and consumer outcomes. Canary selected products and regions. At the authority boundary, stop direct source writes for the moved fields, capture final source positions, activate central commands, and publish the new owner. Track requested, applied, unknown, failed, and reconciled states per source. Suppress echoed updates, preserve rollback, and do not declare completion until source and consumer versions reconcile. Rollback may transfer authority back at a new effective time; it must not re-enable ambiguous concurrent writing.

### Answer 5

Inventory every domain, entity, attribute and relationship style slice, source, identifier, cross-reference, assertion, match and survivorship rule, virtual call, persisted generation, central command, writeback, event, file, API, cache, mapping, source position, pending operation, conflict, consumer, credential, history, backup, retention rule, deletion path, and incident duty. For each authority and capability, name the receiving system and owner or prove it is no longer required.

Run old and new paths in bounded comparison. Verify registry resolution and partial states, consolidated assertions and golden views, coexistence commands and acknowledgements, aliases, freshness, correction, protection, and recovery. Migrate consumers by cohort and include batch, offline, seasonal, manual, and disaster-recovery dependencies. Freeze and transfer writes at explicit times, drain and reconcile queues, revoke source and hub access, remove prohibited copies, and place required history under named custody. Test operation without the old hub and ensure backups, delayed messages, old jobs, or source echoes cannot resurrect retired identities, values, or authority before accountable closure.
