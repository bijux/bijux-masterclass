---
module_id: DARCH-062
program: Data Architecture Engineering
level: 2
module_number: 62
title: Metadata Harvesting and Synchronization
status: complete
last_verified: 2026-09-03
---

# Metadata Harvesting and Synchronization

## One-Page Review

### Governing question

How should an enterprise collect and synchronize metadata from heterogeneous authorities so that derived registries, graphs, indexes, and catalogs converge without losing identity, provenance, deletions, conflicts, or recoverability?

### Essential definitions

- **Harvesting** is the controlled retrieval of metadata records or observations from a source for use in another system.
- **Synchronization** is the continuing process of bringing a destination into a declared relationship with an evolving source, including creation, change, deletion, correction, and recovery.
- A **source of authority** is the governed system or role entitled to issue a class of metadata assertions; it is not necessarily the system from which a collector reads them.
- A **collector** obtains records, events, logs, or observations and preserves source identity, position, provenance, and collection evidence.
- A **connector** is a configured adapter between a source contract and a destination ingestion contract.
- A **snapshot** is a bounded representation of source state associated with a scope, version or high-water mark, creation time, and completeness claim.
- A **change event** describes an occurrence such as create, update, correct, deprecate, or delete with stable event and subject identities.
- A **cursor** or **checkpoint** records a resumable source position under a defined ordering and retention contract.
- A **high-water mark** is a source position through which a snapshot or consumer state claims complete processing for a declared scope.
- A **tombstone** is a durable indication that a subject or assertion is deleted, withdrawn, or no longer active; its semantics and retention must be explicit.
- **Idempotent application** produces the same materialized effect when the same identified change is applied more than once.
- **Reconciliation** compares authoritative and derived states or evidence to detect omissions, duplicates, divergence, and invalid assumptions.
- **Resynchronization** rebuilds or repairs a destination from a trustworthy boundary after a gap, incompatible change, corruption, or lost checkpoint.
- **Convergence** means that, after all relevant changes are available and successfully processed under the contract, a projection reaches the intended source-relative state.

### Central model, mechanism, or theorem

Represent a synchronization relationship as:

`Y = (S, D, I, A, M, X, O, C, V, P, R, E, L)`

where `S` is source scope, `D` destination projection, `I` identity, `A` authority, `M` collection mechanism, `X` exchange contract, `O` ordering and offsets, `C` compatibility and conflict, `V` validation, `P` protection, `R` reconciliation and repair, `E` operating evidence, and `L` lifecycle closure. Synchronization is fit only when every applied assertion remains attributable to a source and authority; snapshots and changes share a recoverable boundary; duplicates, gaps, late arrivals, deletions, and incompatible versions have defined behavior; derived projections can be reconciled and rebuilt; and collection itself is authorized, observable, bounded, and closable.

### Critical invariants

- Harvesting creates a derived copy or observation; it does not transfer semantic authority to the harvester.
- Source subject identity, assertion identity, event identity, connector identity, and destination record identity remain distinguishable.
- Every snapshot declares scope, source version or high-water mark, creation time, completeness boundary, schema or profile, and integrity evidence.
- Every change declares source, stable identity, operation, subject, version or sequence, occurrence time when known, schema, provenance, and deletion semantics.
- At-least-once delivery requires idempotent consumers; transport acknowledgment is not application or convergence evidence.
- Timestamps alone are not safe cursors unless precision, monotonicity, tie-breaking, timezone, late-write, and clock assumptions are governed.
- A checkpoint advances only after the intended materialized effects and required evidence are durable.
- Deletion and withdrawal are synchronized explicitly; absence from an incremental response does not mean deletion.
- Schema evolution, semantic evolution, connector configuration, mapping, and policy versions are independently identifiable.
- Reconciliation is scheduled independently of ordinary delivery and uses authoritative counts, identifiers, versions, digests, or sampled assertions.
- Sensitive metadata is minimized and protected in discovery, collection, staging, quarantine, dead-letter, logs, replay, backups, and metrics.
- Retirement closes source access, credentials, connectors, subscriptions, checkpoints, buffers, projections, evidence, retention, and recovery paths.

### Common failures

Common failures include crawling without an authority contract; using file paths as stable identity; treating `updated_at` as a lossless cursor; beginning change capture after an inconsistent snapshot; advancing offsets before durable application; making retries non-idempotent; dropping duplicates before validating identity scope; interpreting missing records as deletion; losing tombstones to retention; flattening events and discarding source positions; overwriting conflicting assertions; letting a connector invent semantic mappings; ignoring backpressure; retrying poison records forever; trusting transport lag as freshness; never reconciling; running a big-bang reharvest without isolation; leaking sensitive metadata through errors; and deleting the old connector before its dependencies and recovery obligations close.

### Compact example

A destination begins from a two-asset snapshot at source sequence 2. It receives an update at sequence 3, its duplicate, a deletion at sequence 5 before a create at sequence 4, buffers the gap, and drains contiguous changes when sequence 4 arrives. A small executable check reports four received events, three applied changes, one duplicate, one gap observation, last sequence 5, two active assets, one tombstone, and a reconciled final state. It proves only the invented state machine, not source completeness, authentic positions, semantic correctness, or production recovery.

### Connections

[DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-058](058-master-data-change-propagation.md), and [DARCH-061](061-metadata-architecture.md) establish contract, propagation, and metadata-subject boundaries. [DARCH-063](../ROADMAP.md) next governs business glossaries and terms, whose assertions must also be synchronized safely.

## Governing Question

An enterprise metadata plane is assembled from schema registries, databases, orchestration engines, source repositories, deployment systems, access services, quality engines, business glossaries, policy systems, incident tools, and human decisions. No single collection mechanism can obtain all of those assertions with identical guarantees.

The governing question is how to combine crawling, pull APIs, snapshots, change inventories, events, logs, and manual publication while preserving authority and making omissions, duplicates, order, deletion, conflict, lag, and recovery observable instead of silently producing a plausible but false catalog.

## Why This Matters

The [Open Archives Initiative Protocol for Metadata Harvesting 2.0](https://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm) distinguishes resources, items, metadata records, repositories, and harvesters; supports identifiers, datestamps, sets, metadata formats, deletion status, and resumable lists; and illustrates a stable pull protocol for metadata exchange. Its domain and XML design are specific, but its boundaries remain instructive.

The ANSI/NISO [ResourceSync Framework Specification](https://www.openarchives.org/rs/1.1/resourcesync) separates resource lists, change lists, dumps, change dumps, capability discovery, and related-resource links so destinations can remain aligned with evolving web resources. It explicitly addresses create, update, delete, discovery, packaging, and modular synchronization capability.

IETF [HTTP Semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines validators such as entity tags, conditional requests, preconditions, and `304 Not Modified`, enabling efficient retrieval and lost-update protection when used under a correct representation contract. IETF [JSON Patch, RFC 6902](https://www.rfc-editor.org/rfc/rfc6902.html) defines ordered operations for partial modification of a JSON document. A patch still needs a known base version and safe failure behavior.

The CNCF [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md) standardizes event context attributes including source, identifier, specification version, type, subject, time, data content type, and schema reference. It does not define application-specific ordering, delivery, payload, retention, or reconciliation semantics.

[OpenLineage's run cycle](https://openlineage.io/docs/spec/run-cycle/) represents lifecycle state changes for jobs and runs with input and output datasets, showing how operational metadata can arrive incrementally as an activity progresses. W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) distinguishes catalog records from described resources and adds versioning, series, and checksums useful for exchanged catalog representations.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) supplies entities, activities, agents, derivation, generation, use, and attribution for provenance exchange. Debezium's [PostgreSQL connector documentation](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) illustrates snapshot and log-based change events carrying operation, source, transaction, log position, and timestamps. Product-specific behavior must be validated for each connector and version.

W3C [SHACL](https://www.w3.org/TR/shacl/) defines validation of RDF data graphs against shapes graphs and structured validation reports. Boundary validation can reject or quarantine malformed metadata, but conformance cannot establish source authority, semantic truth, or destination convergence.

## Prerequisites and Retrieval

You should understand metadata architecture, stable identifiers, assertions, provenance, APIs, HTTP, event systems, logs, database transactions, change data capture, schemas, graphs, indexes, distributed systems, ordering, idempotency, consistency, checkpoints, backpressure, security, privacy, reliability, observability, recovery, and lifecycle governance.

Retrieve harvester, publisher, repository, collector, connector, source authority, snapshot, inventory, dump, change list, event, operation, cursor, checkpoint, offset, sequence, high-water mark, watermark, resumption token, validator, entity tag, conditional request, delta, patch, tombstone, duplicate, gap, late arrival, replay, quarantine, dead-letter, reconciliation, repair, resynchronization, convergence, freshness, lag, retention, and closure.

As a retrieval test, inspect “the catalog syncs every five minutes.” Ask which subjects and assertions, from which authority, by what mechanism, using which cursor and ordering scope, with what deletion and schema behavior, when the checkpoint advances, how gaps are detected, how derived state is reconciled, what five minutes measures, which failures degrade service, and how a full rebuild works. A schedule is not a synchronization guarantee.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish harvesting, observation, replication, synchronization, reconciliation, and resynchronization;
2. identify sources of authority separately from technical collection endpoints;
3. choose crawl, pull, snapshot, inventory, event, change-log, or hybrid mechanisms by consequence and source capability;
4. design stable identities, ordering scopes, cursors, high-water marks, and snapshot-to-change boundaries;
5. specify idempotency, duplicate, late, gap, deletion, correction, replay, and poison-record behavior;
6. evolve schemas, profiles, mappings, connectors, and policies without losing interpretability;
7. validate, reconcile, observe, protect, and recover metadata flows end to end;
8. manage backpressure, retention, capacity, service objectives, and degraded modes;
9. migrate or rebuild projections with consumer-visible evidence and bounded risk; and
10. retire collection relationships only after dependencies and obligations close.

## Core Exposition

**Begin with the synchronization outcome.** Name which decisions depend on which metadata being sufficiently current, complete, authoritative, and available.

Schema compatibility for a deployment, owner lookup during an incident, access classification at query time, discovery ranking, and monthly audit evidence demand different latency and assurance. Do not assign one interval to all metadata.

**Define the source boundary.** Identify source system, endpoint, repository, database, collection, topic, branch, tenant, namespace, and predicate scope.

Document inclusions, exclusions, filters, partitions, jurisdictions, and historical depth. “Harvest the warehouse” is ambiguous when temporary schemas, system objects, external tables, and restricted tenants differ.

**Name the authority for each assertion.** A database is authoritative for observed columns; a schema registry can be authoritative for supported contract schemas; a domain owner is authoritative for business meaning.

The collector preserves each role. Technical proximity does not let a crawler override a governed definition.

**Separate collection from interpretation.** A connector should extract and normalize under a versioned mapping while retaining raw or reconstructable source evidence where justified.

Semantic enrichment is a separate activity with its own authority, version, provenance, and correction. Hidden interpretation inside connectors makes disagreement and migration untraceable.

**Select mechanisms per source.** Use crawling for discoverable resources where occasional omission and delay are acceptable; pull APIs for governed queries; resource inventories for complete scopes; snapshots for consistent baselines; events for low-latency changes; and transaction logs for ordered source mutations.

Hybrid designs are normal. A change stream gives speed while periodic inventory or snapshot reconciliation supplies completeness.

**Understand crawl limitations.** Crawlers depend on reachability, permissions, link discovery, robots or policy, pagination, rate limits, timeouts, representation stability, and naming conventions.

They may observe resources but miss deletions, unlinked objects, transient states, or semantic declarations. Record observation time and collection scope; do not claim completeness without evidence.

**Design pull APIs explicitly.** Define subject filters, assertion types, version selection, time bounds, page size, stable sort, cursor semantics, authorization, rate limits, errors, and retention.

Offset-number pagination over a changing collection can skip or duplicate records. Prefer opaque cursors tied to a stable ordering or snapshot boundary.

**Use conditional retrieval.** Entity tags or equivalent validators can avoid retransmitting unchanged representations.

Specify whether validators are strong or weak, which representation dimensions they cover, and whether authorization or content negotiation changes the tag. A `304` response proves the selected representation matched the validator, not that upstream metadata remained semantically correct.

**Treat modification times cautiously.** A `last_modified` filter is safe only if all relevant writes update it, precision exceeds write density, timezones are normalized, clocks and retroactive updates are handled, and tie-breaking is stable.

Use overlap windows and deduplication when these guarantees are incomplete. A composite cursor such as `(timestamp, stable_id)` can reduce ambiguity but does not solve late commits with old timestamps.

**Design snapshots as contracts.** A snapshot declares subject scope, predicate scope, source identity, snapshot identifier, source position, creation start and completion times, consistency model, schema or profile, row or record count, digest, partitions, omissions, and retention.

Do not label an ordinary scan consistent if source mutations can interleave without a controlled boundary. Consumers must know what the snapshot includes.

**Bridge snapshot and change capture.** Establish a source position that makes snapshot contents and later changes contiguous.

Possible patterns start logging before the snapshot, take a transactionally consistent snapshot at a log position, or buffer changes during the scan. The invariant is no unobservable gap and a defined rule for overlapping changes.

**Represent change operations.** Distinguish create, replace, partial update, correct, deprecate, withdraw, delete, restore, merge, split, and relationship change where consumer behavior differs.

An “upsert” hides whether absence should create, whether deletion occurred, and whether history must be repaired. Operation semantics belong in the contract.

**Use stable event identity.** Event identity supports duplicate detection and traceability; subject identity identifies what changed; source and sequence identify ordering scope.

Do not derive event identity solely from mutable payload content if equivalent serializations differ. Define uniqueness retention and behavior when a producer accidentally reuses an identifier.

**Define ordering scope.** Global order is expensive and often unnecessary. Per-source, partition, subject, assertion, or relationship order may suffice.

Consumers need to know which changes commute. A deletion and later restore for one subject require order; independent quality measurements may not.

**Choose source positions over wall clocks where possible.** Transaction log sequence numbers, monotonically assigned revisions, or opaque cursors can express source order more reliably than event time.

Positions are meaningful only within a declared source generation and retention window. Failover, restore, sharding, or reconfiguration can reset or fork sequences.

**Separate occurrence, commit, publish, ingest, and apply time.** Occurrence time says when the described change happened; commit establishes source durability; publish records emission; ingest records receipt; apply records destination effect.

Lag metrics must name both endpoints. Conflating clocks can produce negative or misleading latency and hide queueing.

**Assume at-least-once effects unless stronger evidence exists.** Networks, brokers, clients, and checkpoint recovery commonly redeliver.

Make application idempotent using stable event identity, source version, conditional mutation, or naturally idempotent replacement. Exactly-once transport marketing does not eliminate external side effects or reconciliation.

**Define deduplication scope and retention.** A key is commonly `(source, event_id)` or `(source_generation, sequence)`.

Retain it at least as long as replay can reintroduce duplicates, or make the materialization independently version-aware. Premature expiry can reapply an old correction or resurrect a deletion.

**Advance checkpoints after durable effect.** A consumer records a checkpoint only after state mutation, necessary indexes or outbox evidence, and required audit records are durable under the recovery model.

Checkpoint-before-apply loses changes on failure. Apply-before-checkpoint redelivers but is safe only when application is idempotent.

**Define gap detection.** Sequence discontinuity, expired cursor, missing page, checksum difference, source-generation change, event-retention breach, or failed partition can indicate a gap.

Do not advance silently. Pause affected scope, buffer safely, request missing changes, reconcile, or resynchronize from a trustworthy snapshot.

**Handle out-of-order arrival.** Buffer within a bounded window, apply version preconditions, or materialize commutative assertions independently.

Define window size, memory and disk bounds, late-event disposition, watermark, escalation, and repair. Indefinite buffering converts disorder into capacity failure.

**Treat watermarks as claims.** A watermark says no event earlier than a time or position is expected under a declared lateness model.

It is not proof that none will arrive. Preserve a correction route for violated assumptions and distinguish event-time watermarks from processed source offsets.

**Synchronize deletion explicitly.** Use tombstones, deleted-record status, change inventories, or authoritative membership comparison.

Specify whether deletion means resource removed, metadata record withdrawn, access revoked, subject merged, or representation unavailable. Consumers may need to retain identity and provenance while removing active discovery.

**Retain tombstones long enough.** A consumer offline longer than tombstone retention can miss deletion and retain a ghost resource.

Bound maximum outage, require periodic full reconciliation, or provide durable deletion history. State the privacy and storage trade-off; tombstones themselves can reveal sensitive existence.

**Do not infer deletion from absence casually.** Absence in one page, filtered query, authorization view, incomplete crawl, failed partition, or new profile is not deletion.

Only an explicit operation or a verified complete-inventory comparison under stable identity can authorize removal from the corresponding projection.

**Support partial updates carefully.** A patch reduces bandwidth but depends on an exact base version, operation order, path semantics, authorization, and atomic failure behavior.

Use preconditions and reject an incompatible base rather than applying a patch approximately. Retain the resulting full assertion or reconstructable history where recovery requires it.

**Prefer replacement for small metadata records.** Full versioned replacement is easy to make idempotent and can avoid field-level merge ambiguity.

It costs more bandwidth and may overwrite independently owned predicates. Split records by authority or use assertion-level updates when ownership differs.

**Preserve provenance through transformation.** Record connector, configuration, code, mapping, source record, source position, collection time, validation result, transformation, and destination version.

Flattened metadata can serve queries, but raw or canonical evidence must support explanation and repair within retention and privacy constraints.

**Version connector configuration.** Filters, credentials scope, mappings, batch size, timeouts, parsing, normalization, and deletion modes change what metadata is observed.

Treat configuration as governed code with review, tests, deployment, rollback, provenance, and effective time. A connector upgrade can be a semantic migration.

**Evolve schemas and profiles independently.** Source schema, event envelope, payload profile, mapping, destination model, and consumer API each have versions.

Classify additive, compatible, conditionally compatible, and breaking changes at every boundary. Preserve unknown fields where appropriate and prevent silent narrowing.

**Validate before authoritative projection.** Check envelope, identity, source, operation, schema, required provenance, temporal consistency, relationship endpoints, authority, and policy.

Separate invalid metadata from infrastructure failure. Quarantine bounded records with reason, evidence, owner, retry or repair path, retention, and sensitive access controls.

**Avoid infinite poison retries.** A malformed or semantically rejected record can block a partition if retried without change.

Set retry classes and budgets. Move permanent failures to controlled quarantine, alert accountable owners, keep checkpoint semantics explicit, and preserve the ability to replay a correction.

**Design backpressure.** Limit concurrent requests, batch size, queues, memory, disk, retries, and downstream writes.

Use source rate limits and destination capacity signals. Shed or delay low-criticality enrichment before losing identity, deletion, or authority changes; document degraded priority.

**Isolate tenants and sources.** One high-volume or failing source must not exhaust queues, workers, checkpoints, storage, or retry budgets for others.

Partition resources and service objectives. Isolation boundaries should align with security, failure, ownership, and recovery requirements.

**Protect collection credentials.** Use least-privileged, short-lived identities scoped to required metadata and operations.

Rotate credentials, audit use, restrict network paths, and prevent connectors from reading sample data or secrets merely because the platform account can. Source metadata access can still be highly sensitive.

**Minimize sensitive payloads.** Do not place raw sample values, access tokens, SQL literals, personal search behavior, secret-bearing configuration, or unrestricted lineage into general events and logs.

Use safe references, redaction, field controls, encryption, isolated quarantine, retention limits, and purpose-specific projections.

**Authenticate source and integrity evidence.** Confirm producer identity, transport protection, authorization, and, where consequence warrants, signatures or digest chains.

Integrity checks detect alteration of a representation; they do not prove the source assertion was true or authorized.

**Distinguish transport acknowledgment.** Broker or HTTP acknowledgment proves receipt under that protocol boundary.

It does not prove validation, materialization, graph update, search indexing, consumer visibility, control activation, or reconciliation. Model these stages separately.

**Expose end-to-end positions.** Track produced, retained, fetched, validated, applied, indexed, published, and reconciled positions by source scope.

Dashboards should show the oldest unresolved gap and stalled subject or partition, not only average event throughput.

**Measure freshness by assertion need.** Define source-to-apply and source-to-visible objectives per metadata class and criticality.

Owner deactivation for access may require seconds; descriptive text may tolerate a day. Report percentiles, breach duration, stale population, and consequence.

**Schedule reconciliation independently.** Compare complete authoritative inventory or trustworthy summaries against the destination even when events report no error.

Use identifiers, counts by partition, versions, checksums, digests, relationship endpoints, tombstones, and sampled values. Independent reconciliation detects shared blind spots in normal processing.

**Make reconciliation actionable.** Classify missing, extra, stale, conflicting, malformed, unauthorized, and untraceable records.

Assign owner, severity, repair mechanism, consumer impact, escalation, and closure evidence. A mismatch dashboard without a repair loop is merely observability.

**Design targeted repair.** Replay a range, refetch a subject, rebuild one partition, recompute a projection, apply a correction, or reissue a tombstone.

Avoid full rebuilds when a bounded repair is safer. Verify that repair is idempotent and does not overwrite newer authoritative state.

**Design full resynchronization.** Capture a new consistent snapshot and change boundary, build an isolated destination generation, validate and reconcile it, then atomically or controllably promote readers.

Keep the old generation until acceptance and rollback limits are clear. In-place reharvest can mix old and new models and expose partial state.

**Treat indexes and graphs as projections.** Registry state, graph relationships, search documents, and catalog pages can update at different times.

Expose projection version and staleness, reconcile each, and never allow a derived index to become the correction authority.

**Handle source restore and failover.** A restored database or replaced service can reuse offsets, move clocks backward, or lose history.

Use a source-generation identifier, detect position regression or fork, stop automatic application, and resynchronize or arbitrate rather than assuming continuity.

**Plan retention across the chain.** Coordinate source log retention, broker retention, cursor lifetime, dedupe keys, tombstones, snapshots, quarantine, provenance, destination history, and backups.

The shortest critical retention sets the maximum recoverable outage. Privacy and records obligations can require different retention by artifact.

**Test failure combinations.** Exercise timeout after source success, duplicate response pages, stale cursor, partial batch, process crash before and after checkpoint, out-of-order changes, poison record, expired tombstone, incompatible schema, partition loss, and source restore.

Verify materialized state, evidence, alerts, repair, and consumer visibility—not only connector restart.

**Define service ownership.** Source owners maintain publication correctness and retention; connector owners maintain collection and mapping; metadata product owners maintain semantics and projections; platform owners maintain shared transport and storage; consumer owners maintain use and adoption.

Incident and risk ownership follow consequence. One team can hold several roles, but the decisions remain explicit.

**Fund ongoing synchronization.** Budget source integration, connector maintenance, version upgrades, capacity, observability, on-call, reconciliation, repair, security, consumer migration, and retirement.

Connector count is a cost driver but source diversity, change rate, criticality, and failure behavior matter more than raw count.

**Migrate with parallel evidence.** Run old and new collectors against bounded scopes, normalize identity, compare outputs, investigate discrepancies, and migrate projections or consumers by cohort.

Do not double-apply effects because two pipelines observe the same source. Establish one promotion authority and a reversible cutover boundary.

**Retire collection relationships fully.** Stop source publication or revoke subscription, disable schedules, close credentials, drain or discard buffers under policy, freeze checkpoints, reconcile final state, notify consumers, and archive or delete evidence.

Remove recovery automation and secrets so the old connector cannot resume. Preserve required identifiers, provenance, tombstones, and historical versions under named custody.

## Definitions and Notation

Let:

- `S` be the set of authoritative source scopes;
- `D` be the set of destination projections;
- `E` be the set of identified change events;
- `N_s` be the ordered position domain for source scope `s`;
- `K` be the set of durable checkpoints;
- `T` be the set of snapshots and tombstones;
- `V` be the set of schema, profile, mapping, connector, and policy versions;
- `Q` be the set of quarantined or disputed records;
- `R` be the set of reconciliation observations and repairs; and
- `C` be the set of consumers and lifecycle obligations.

Define event identity within a source:

`EventKey(e) = (source_generation(e), source(e), event_id(e))`

The same subject can have many events. A replay of one occurrence preserves its event key; a correction is a new identified occurrence linked to what it corrects.

For a consumer materialization `m`, define idempotent application:

`Apply(Apply(m, e), e) = Apply(m, e)`

This equality concerns materialized effect under the declared event identity. Logging, attempt counts, and receipt timestamps may still change.

Define contiguous progress for ordered scope `s`:

`Contiguous(s, k) = forall n in (start(s), k] : applied_or_intentionally_skipped(s, n) with evidence`

An intentionally skipped position requires governed evidence; advancing because a message was inconvenient violates the invariant.

Define a valid snapshot/change bridge:

`Bridged(snapshot, stream) = complete_through(snapshot, h) and stream_includes_all_after(stream, h) and overlap_is_idempotent`

The exact mechanism differs by source. The invariant forbids an unobservable interval between baseline and incremental change.

Define convergence for destination `d` and scope `s` at position `k`:

`Converged(d, s, k) = Contiguous(s, k) and projection(d, s, k) = intended_projection(authoritative_state(s, k))`

Equality is defined by the destination profile, not byte identity. Its proof requires reconciliation evidence and bounded assumptions about authority and source completeness.

The assurance predicate is:

`FitSync = Scoped and Authorized and Identified and Bridged and Versioned and Idempotent and GapAware and DeletionAware and Validated and Protected and Observable and Reconciled and Repairable and Recoverable and Closable`

This is a review structure. It does not claim exactly-once delivery, universal ordering, complete source truth, or zero lag.

## Mechanisms, Invariants, or Proof Structure

**Outcome gate.** Bind freshness, completeness, authority, and recovery requirements to named metadata decisions and consumers.

**Source gate.** Define endpoint, scope, exclusions, authority, publication contract, positions, retention, availability, protection, and owner.

**Identity gate.** Distinguish source generation, subject, assertion, event, connector, snapshot, checkpoint, and destination identities.

**Mechanism gate.** Justify crawl, pull, inventory, snapshot, event, change-log, manual publication, or hybrid collection against source guarantees and consequence.

**Bridge gate.** Prove the baseline and incremental stream overlap safely or meet contiguously at a recoverable high-water mark.

**Ordering gate.** State sequence domain, partition, tie-breaker, event-time assumptions, late window, watermark, gap response, and position reset behavior.

**Application gate.** Verify idempotent effects, atomic durability, checkpoint timing, conflict policy, partial update base, and downstream projection behavior.

**Deletion gate.** Define delete, withdraw, deprecate, merge, split, tombstone identity, retention, authorization, consumer action, and offline recovery.

**Compatibility gate.** Version envelope, payload, source schema, profile, mapping, connector, destination model, and consumer interface independently.

**Validation gate.** Validate identity, source, authority, operation, schema, provenance, time, relationship, policy, and sensitive content before projection.

**Protection gate.** Apply least privilege, minimization, encryption, isolation, retention, deletion, audit, and incident response across staging and replay paths.

**Operations gate.** Bound request rate, batch, concurrency, queues, retry, quarantine, backpressure, tenant isolation, and degraded priorities.

**Evidence gate.** Expose production, collection, validation, application, indexing, publication, and reconciliation positions plus oldest unresolved gaps.

**Repair gate.** Test refetch, replay, partition rebuild, correction, tombstone recovery, full resynchronization, promotion, rollback, and source-generation change.

**Lifecycle gate.** Close access, credentials, publication, subscriptions, schedules, checkpoints, buffers, projections, evidence, secrets, and recovery automation.

### Executable evidence: buffered metadata change convergence

This Python example starts from a snapshot through sequence 2, receives one duplicate and one out-of-order deletion, buffers the gap, and applies changes only when the sequence becomes contiguous.

<!-- bijux-verify: {"id":"buffered-metadata-change-convergence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"received_events=4\napplied_changes=3\nduplicates=1\ngap_observations=1\nlast_sequence=5\nactive_assets=2\ntombstones=1\nreconciled=true\n","stderr":""}} -->
```python
state = {
    "alpha": {"version": 1, "title": "Alpha"},
    "beta": {"version": 1, "title": "Beta"},
}
events = [
    {"id": "catalog-3", "sequence": 3, "op": "update", "subject": "alpha", "version": 2},
    {"id": "catalog-3", "sequence": 3, "op": "update", "subject": "alpha", "version": 2},
    {"id": "catalog-5", "sequence": 5, "op": "delete", "subject": "beta", "version": 2},
    {"id": "catalog-4", "sequence": 4, "op": "create", "subject": "gamma", "version": 1},
]

last_sequence = 2
seen = set()
pending = {}
tombstones = set()
duplicates = 0
gap_observations = 0
applied_changes = 0

for event in events:
    event_key = ("catalog-generation-1", event["id"])
    if event_key in seen:
        duplicates += 1
        continue
    seen.add(event_key)
    pending[event["sequence"]] = event
    if event["sequence"] > last_sequence + 1:
        gap_observations += 1

    while last_sequence + 1 in pending:
        change = pending.pop(last_sequence + 1)
        if change["op"] == "delete":
            state.pop(change["subject"], None)
            tombstones.add(change["subject"])
        else:
            state[change["subject"]] = {"version": change["version"]}
        last_sequence += 1
        applied_changes += 1

expected = {"alpha": {"version": 2}, "gamma": {"version": 1}}
reconciled = state == expected and not pending and tombstones == {"beta"}

print(f"received_events={len(events)}")
print(f"applied_changes={applied_changes}")
print(f"duplicates={duplicates}")
print(f"gap_observations={gap_observations}")
print(f"last_sequence={last_sequence}")
print(f"active_assets={len(state)}")
print(f"tombstones={len(tombstones)}")
print(f"reconciled={str(reconciled).lower()}")
```

The expected output reports `received_events=4`, `applied_changes=3`, `duplicates=1`, `gap_observations=1`, `last_sequence=5`, `active_assets=2`, `tombstones=1`, and `reconciled=true` on separate lines.

The example proves only deterministic behavior of a tiny in-memory buffer with trusted integer positions and payloads. It does not persist checkpoints or dedupe state, bound the buffer, authenticate a producer, detect identifier reuse, bridge a real snapshot and log, validate versions, handle source generations, enforce authorization, survive crashes, or prove authoritative completeness. The final equality is an invented oracle. Production evidence requires source-specific guarantees, crash testing, retention analysis, reconciliation against independent authoritative state, security and privacy review, failure exercises, and accountable acceptance.

## Alternatives and Trade-Offs

**Scheduled full harvest.** A full pull is simple and can detect membership deletion, but it creates source load, transfer cost, long stale intervals, and partial-scan problems. Use versioned isolated builds rather than exposing half a refresh.

**Incremental timestamp pull.** This is widely available and easy to inspect. It risks precision ties, late commits, unchanged timestamps, clock errors, and retroactive writes; overlap and dedupe mitigate but do not prove completeness.

**Opaque cursor pull.** A source-defined cursor can preserve stable paging and ordering without exposing internals. It creates source coupling and requires expiry, invalidation, replay, and recovery semantics.

**Change inventory.** A resource or identifier list with create, update, and delete information enables efficient alignment and audit. It requires authoritative membership, durable history, pagination, and integrity.

**Push events.** Events reduce latency and source polling. They introduce broker dependency, delivery duplication, ordering scope, retention, subscription, backpressure, and gap recovery concerns.

**Transaction-log capture.** Logs can preserve source commit order and detect every represented database mutation. They expose physical implementation, high volume, sensitive values, retention constraints, and changes that may not represent authoritative business semantics.

**Full replacement.** Replacing a bounded metadata record is idempotent and easy to reconstruct. It transmits more and can overwrite predicates owned independently unless records are partitioned by authority.

**Patch exchange.** Patches reduce bandwidth and precisely express edits. They require a known base, ordered atomic operations, path stability, version preconditions, and safe recovery after missed changes.

**Single central collector.** Central operation standardizes controls and reduces connector duplication. It concentrates credentials, capacity, outage, change, and organizational risk and can become an accidental semantic owner.

**Domain-owned collectors.** Domains retain context and move quickly. Shared interoperability, security, observability, and repair can fragment unless a platform supplies governed capabilities.

**Immediate application.** Low latency benefits access and incident decisions. It exposes consumers quickly to bad changes and requires stronger validation, rollback, and isolation.

**Staged promotion.** Quarantine, validation, and approval improve assurance but add lag and operational queues. Apply higher ceremony to consequential assertion classes rather than every description.

## Failure Modes and Misconceptions

1. **“Polling guarantees a complete copy.”** Filters, paging, writes, permissions, and failures can omit records.
2. **“The latest timestamp is a cursor.”** Precision, clocks, ties, late commits, and retroactive updates can lose changes.
3. **“Events remove the need for snapshots.”** Baselines and resynchronization still need bounded state.
4. **“Snapshots remove the need for events.”** Repeated full copies can be too stale or expensive for critical change.
5. **“At-least-once means duplicate rows are acceptable.”** It requires idempotent materialized effects and evidence.
6. **“Exactly-once transport proves convergence.”** External side effects, source gaps, and semantic conflicts remain.
7. **“Event time defines order.”** Clocks and publication delay differ from source commit sequence.
8. **“A received acknowledgment means synced.”** Validation, application, indexing, activation, and reconciliation are later boundaries.
9. **“Missing means deleted.”** Absence can result from filters, permission, incomplete scan, or failure.
10. **“Tombstones can expire quickly.”** Offline consumers may retain ghost state beyond the deletion history.
11. **“Upsert is enough.”** It hides creation preconditions, deletion, conflict, and historical correction.
12. **“A connector is only plumbing.”** Mapping, filtering, normalization, and deletion modes change meaning.
13. **“Retries always heal.”** Permanent poison records can block progress and exhaust capacity.
14. **“Lag is one number.”** Production, ingest, apply, index, publish, and reconcile delays answer different questions.
15. **“No errors means synchronized.”** Shared blind spots require independent reconciliation.
16. **“A full rebuild is harmless.”** In-place rebuilds can expose partial generations and overwrite newer state.
17. **“Metadata needs no strict protection.”** Schemas, lineage, behavior, and configuration can be sensitive.
18. **“Disabling the schedule retires sync.”** Credentials, subscriptions, queues, state, copies, and recovery can remain active.

## Worked Examples

### Example 1

A university repository exposes metadata records through OAI-PMH with stable item identifiers, datestamps, metadata formats, sets, deleted-record status, and resumption tokens. The harvester stores the repository response date, request, token, record provenance, and checkpoint. It overlaps date ranges at the source's declared granularity and deduplicates by record identity and datestamp rather than assuming wall-clock exclusivity.

### Example 2

A public-data publisher supplies a ResourceSync resource dump for baseline, a change list with create, update, and delete operations, and digests for distributions. A consumer builds a new isolated generation, applies changes after the dump boundary, verifies checksums, compares membership, and promotes only after reconciliation. Capability discovery lets it avoid inventing unsupported patch behavior.

### Example 3

A schema registry offers an API with strong entity tags. The collector uses conditional GET for each profile, records `304` as unchanged representation evidence, and uses `If-Match` for controlled corrections. It does not treat unchanged bytes as proof that ownership, policy, or business meaning remains valid.

### Example 4

A warehouse crawler queries tables ordered by `(last_altered, stable_object_id)` with a ten-minute overlap because timestamp precision and commit timing are imperfect. It deduplicates observations, reconciles a daily complete inventory, and emits explicit deletions only after an authoritative membership comparison. Restricted schemas use separate credentials and projections.

### Example 5

An orchestration engine emits OpenLineage-style run events. `START` records planned inputs and code version; `COMPLETE` records actual outputs; `FAIL` records a failed activity without making proposed outputs current. A gap in run events triggers API retrieval and reconciliation rather than inference from the last visible state.

### Example 6

A database connector takes a consistent snapshot tied to a transaction-log position and then streams changes. Source generation, transaction, log sequence, table, operation, and before-and-after evidence are retained. Only approved structural assertions enter the catalog; raw payloads remain in a restricted, short-lived repair store.

### Example 7

A metadata event at sequence 42 arrives twice, sequence 44 arrives before 43, and 43 is delayed. The consumer deduplicates 42, buffers 44 within a bounded window, applies 43 then 44, and checkpoints only after graph and registry state are durable. If 43 remains unavailable beyond the service threshold, it stops the partition and requests replay.

### Example 8

A domain withdraws a sensitive dataset. The event says withdrawal rather than physical deletion, includes authority and effective time, and produces a restricted tombstone. Search removes active discovery, access blocks new use, consumers receive notification, provenance remains under records policy, and reconciliation detects any stale public index.

### Example 9

A connector configuration update changes a mapping from physical tables to logical products. Teams version and test the mapping, run old and new projections in parallel, inspect splits and merges, preserve crosswalks, and cut over one domain. They do not label the change a routine connector upgrade because subject identity and consumer navigation change.

### Example 10

A source restore moves its log position backward. The consumer detects a new source generation and refuses to compare offsets across generations. It captures a new snapshot and boundary, builds an isolated projection, reconciles current identifiers and tombstones, records history discontinuity, and promotes after owner approval rather than replaying ambiguous old events.

## Cross-Program Connections

- **Data engineering:** source extraction, CDC, snapshots, event processing, checkpoints, backfills, reconciliation, quarantine, and replay implement metadata flows.
- **API and service engineering:** conditional requests, cursors, pagination, idempotency, patch preconditions, errors, rate limits, webhooks, compatibility, and deprecation shape exchange.
- **Platform engineering:** connector frameworks, credential vending, queues, schedulers, schema registries, policy, observability, tenancy, recovery, and self-service reduce repeated effort.
- **Database engineering:** isolation, logs, transaction positions, snapshots, temporal state, indexes, replication, restore, and failover determine source guarantees.
- **Distributed systems engineering:** delivery semantics, ordering, clocks, partitions, consensus boundaries, idempotency, convergence, and failure detectors explain synchronization limits.
- **Security and privacy engineering:** least privilege, minimization, secret handling, transport protection, integrity, isolation, audit, retention, and incident response cover the full replay path.
- **Reliability engineering:** objectives, backpressure, retries, poison records, dead letters, capacity, degraded modes, continuity, reconciliation, and recovery establish operational trust.
- **Software architecture:** adapters, anti-corruption layers, versioned contracts, dependency direction, isolation, and evolutionary change keep connector semantics bounded.
- **Systems engineering:** boundary assumptions, interface control, configuration, hazards, verification, validation, lifecycle, and assurance frame synchronization evidence.
- **Organizational design:** source, connector, metadata-product, platform, consumer, incident, and risk owners make technical recovery actionable.

## References

1. Open Archives Initiative, [“The Open Archives Initiative Protocol for Metadata Harvesting, Version 2.0”](https://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm), 2002–2004. Retrieved 2026-09-03.
2. NISO and Open Archives Initiative, [“ResourceSync Framework Specification, ANSI/NISO Z39.99-2017”](https://www.openarchives.org/rs/1.1/resourcesync), 2017. Retrieved 2026-09-03.
3. IETF, [“HTTP Semantics,” RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), 2022. Retrieved 2026-09-03.
4. IETF, [“JavaScript Object Notation (JSON) Patch,” RFC 6902](https://www.rfc-editor.org/rfc/rfc6902.html), 2013. Retrieved 2026-09-03.
5. Cloud Native Computing Foundation, [“CloudEvents Specification, Version 1.0.2”](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md), 2022. Retrieved 2026-09-03.
6. OpenLineage, [“The Run Cycle”](https://openlineage.io/docs/spec/run-cycle/). Retrieved 2026-09-03.
7. W3C, [“Data Catalog Vocabulary (DCAT) — Version 3”](https://www.w3.org/TR/vocab-dcat-3/), 2024. Retrieved 2026-09-03.
8. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/2013/REC-prov-o-20130430/), 2013. Retrieved 2026-09-03.
9. Debezium, [“Debezium Connector for PostgreSQL”](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Retrieved 2026-09-03.
10. W3C, [“Shapes Constraint Language (SHACL)”](https://www.w3.org/TR/shacl/), 2017. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design a harvesting contract for a catalog API that offers `updated_at`, offset pagination, no deletion feed, and a nightly export. Identify unsafe assumptions and propose a complete, efficient synchronization mechanism.

### Exercise 2

A connector takes six hours to snapshot a changing schema registry, then starts consuming events from the time the scan finished. Design a snapshot-to-stream bridge, ordering, deduplication, checkpoint, validation, and recovery protocol.

### Exercise 3

A consumer misses deletion tombstones after being offline for 45 days while broker retention is 14 days. Design retention, reconciliation, resynchronization, identity, and consumer obligations that prevent ghost metadata.

### Exercise 4

Create an observability and assurance scorecard for 200 metadata connectors with different criticality, cadence, source guarantees, and sensitive scopes. Include end-to-end lag, gaps, validation, reconciliation, repair, security, recovery, and cost.

### Exercise 5

Plan replacement of a central crawler with domain-published snapshots and events plus shared connector and reconciliation services. Include parallel evidence, promotion, rollback, consumer activation, and old-path retirement.

## Answers to the Exercises

### Answer 1

Document source scope, stable subject identifiers, assertion authority, schema and profile, update semantics, export consistency, authorization, rate limits, retention, and ownership. Offset pagination over a changing set can skip or repeat; `updated_at` can collide, fail to change, or receive late commits; absence from an incremental page does not establish deletion. Treat the nightly export as a candidate inventory only after the source declares its scope, consistency boundary, identifier uniqueness, completion, generation, digest, and deletion implications.

Add an opaque cursor or stable composite order such as source revision plus subject identity. If the source cannot provide it, use an overlapping timestamp window and durable dedupe while acknowledging residual risk. Build each nightly export into an isolated generation, compare authoritative membership to detect deletion, and reconcile versions and counts. Use conditional retrieval for unchanged records. Advance checkpoints after durable registry and projection effects. Record gaps, rejected assertions, source and destination positions, oldest stale record, and repair. Retain tombstones or complete inventories long enough for offline consumers, and provide versioned snapshots for resynchronization. Never let the harvester become the semantic authority merely because the source API is weak.

### Answer 2

Starting events only after the scan creates an unobservable six-hour gap. Prefer a source-consistent snapshot at position `h` and consume all changes after `h`. If the registry cannot snapshot transactionally, begin event retention before the scan, record start position `a`, scan stable identifiers and versions, then replay from `a` with version-aware idempotency; or buffer events while scanning and reconcile overlap. The source must retain the stream long enough for the snapshot and failures. Identify source generation so restore or failover cannot reuse positions silently.

Partition ordering by subject or source if global order is unnecessary. Use `(source_generation, event_id)` for dedupe and source revision for stale-write rejection. Validate envelope, identity, authority, operation, profile, time, and mappings before authoritative projection. Apply effect and checkpoint atomically where possible; otherwise apply before checkpoint and rely on idempotency. Detect gaps, expired cursors, and incompatible schemas; stop only the affected scope and use bounded quarantine. Test crashes around snapshot completion, replay overlap, application, indexing, and checkpoint. Recovery builds an isolated projection from a fresh bridge, reconciles it with source inventory, and promotes after consumer-visible validation.

### Answer 3

The shortest deletion history is shorter than the supported outage, so the current contract cannot prevent ghosts. Either extend broker or source tombstone retention beyond the maximum offline interval plus repair margin, require consumers to reconnect within 14 days, or require a complete membership reconciliation before an expired consumer can resume. Prefer an authoritative versioned inventory and durable deletion or withdrawal history so identity and provenance survive even when active descriptions do not.

On reconnect, compare the consumer's checkpoint and source generation to the earliest retained position. If the checkpoint expired, reject incremental continuation, obtain a current consistent snapshot and change boundary, rebuild an isolated local generation, compare identifiers, remove absent records only under the snapshot's verified completeness scope, apply retained tombstones, and promote. Keep stable identifiers non-reusable so an old identity cannot bind to a new subject. Record resynchronization evidence and consumer activation. Protect tombstones because they can reveal sensitive existence, and set distinct retention for active discovery, identity redirects, provenance, audit, and personal metadata. Monitor consumers approaching expiry and make the contract explicit.

### Answer 4

Group connectors by source guarantee, criticality, sensitivity, change rate, and consumer consequence rather than average all 200. For every stage expose source produced or observed position, fetched position, validated position, applied position, graph and index position, published position, and reconciled position. Measure source-to-apply and source-to-visible lag percentiles, breach duration, stale subject count, oldest unresolved gap, expired cursor, buffer depth, backpressure, throughput, retry, duplicate, out-of-order, poison, quarantine age, and checkpoint durability.

Measure validation failure by rule, profile, source, and consequence; distinguish malformed, unauthorized, incompatible, and disputed. Reconcile authoritative identifiers, versions, counts, digests, tombstones, and sampled assertions independently; measure mismatches, detection time, repair time, recurrence, and affected consumers. Track credential scope and age, denied access, sensitive payload leakage, integrity failures, isolation, retention, and incidents. Run snapshot bridge, crash, replay, source restore, partition rebuild, tombstone expiry, and full-resynchronization exercises; record recovery objectives and correctness. Add connector ownership, version currency, consumer activation, support burden, compute, network, storage, and human repair cost. Report denominators and confidence, and assign corrective owners.

### Answer 5

Inventory crawler scopes, credentials, schedules, observations, mappings, identifiers, current and historical records, deletion assumptions, graph and search projections, consumers, dashboards, incidents, retention, backups, and recovery automation. Establish domain publication contracts with stable subject and assertion identities, authority, snapshot completeness, event source and identifiers, ordering, schema, operations, tombstones, retention, and service objectives. Shared services supply connector runtime, credential vending, envelope validation, queues, checkpoints, quarantine, observation, reconciliation, resynchronization, and support without taking semantic ownership.

Select one bounded domain and consumer journey. Run crawler output and domain publication in parallel, normalize identity, compare assertions and membership, investigate discrepancies, test deletion and replay, validate sensitive projections, and exercise source restore. Build the new destination in an isolated generation and promote after domain, platform, consumer, security, privacy, and operational owners accept evidence. Migrate consumers by registered cohort with versioned contracts and rollback or compensating repair. Prevent old and new paths from double-applying assertions. Freeze new crawler integrations early. After the last consumer activates, reconcile final state, disable schedules, revoke credentials, drain queues, close checkpoints, remove mappings and recovery automation, delete unneeded staging and behavioral records, preserve required provenance and tombstones, update ownership, and prove the old path cannot republish.
