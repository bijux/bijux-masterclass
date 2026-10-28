---
module_id: DARCH-058
program: Data Architecture Engineering
level: 2
module_number: 58
title: Master-Data Change Propagation
status: complete
last_verified: 2026-09-03
---

# Master-Data Change Propagation

## One-Page Review

### Governing question

How should an enterprise propagate master-data changes from authoritative decisions to every bound consumer with explicit semantics, ordering, compatibility, freshness, protection, recovery, and proof of convergence?

### Essential definitions

- An **authoritative change** is an approved mutation to a governed master-data entity, relationship, hierarchy, identity, or lifecycle state at its owning boundary.
- A **propagation record** is a durable, identified description of a committed change and the context consumers need to interpret it.
- An **entity revision** is a monotonically governed version of one master entity or aggregate; it is not necessarily a global sequence.
- A **source position** is a durable location in an ordered change source, such as a log offset or database-log coordinate.
- **Publication** makes a committed change durably available through an event, log, API, file, or another declared channel.
- **Delivery** places a propagation record within a consumer's processing boundary; delivery alone does not prove application.
- **Application** validates and incorporates a change into a consumer projection according to its contract.
- **Activation** makes the applied change effective for the consumer's business decisions, which can occur after storage.
- **Reconciliation** compares authoritative and consumer evidence to detect omissions, duplicates, divergence, or unauthorized interpretation.
- A **tombstone** is a durable deletion or retirement signal that prevents absent data from being mistaken for an active entity.
- A **snapshot** is an identified, versioned materialization of authoritative state at a declared boundary or source position.
- A **watermark** is evidence that a producer or consumer has durably processed all in-scope changes through a declared position or time.

### Central model, mechanism, or theorem

Represent propagation architecture as:

`P = (decisions, commits, revisions, events, channels, consumers, projections, activation, reconciliation, protection, service, ownership, evidence, lifecycle)`

For consumer `c` and entity `x`, trustworthy convergence is not `message_sent = true`. It requires an unbroken evidence chain from an authorized committed revision through durable publication, interpretable delivery, idempotent application, policy-correct activation, and reconciliation against the authoritative boundary. Delivery can be at least once while effects remain once per identified revision. Ordering may be scoped per entity or aggregate rather than globally, but gaps must be observable and repairable.

### Critical invariants

- A master-data decision and its propagation record are committed atomically or connected by a durable repairable source such as an outbox or database log.
- Every record exposes event identity, entity identity, entity revision, operation, source, schema, relevant times, provenance, and payload semantics.
- Event identity, entity identity, business identity, correlation identity, schema version, source position, and entity revision remain distinct.
- Consumers apply a revision idempotently, reject or quarantine incompatible content, detect gaps, and never let an older revision overwrite a newer one.
- Ordering guarantees are stated by scope—entity, aggregate, partition, stream, batch, or none—and partition keys preserve the intended scope.
- Create, correct, update, merge, split, reparent, replace, deactivate, delete, and restore operations retain their distinct semantics.
- Effective time, source-commit time, publication time, receipt time, application time, and activation time are not collapsed.
- Snapshots and change streams share a reproducible cut boundary so bootstrap and replay neither omit nor double-apply changes.
- Consumer contracts define full-state, changed-field, patch, notification, tombstone, unknown-field, and missing-field behavior.
- Retries, dead letters, replay, backfill, and disaster recovery preserve identity, ordering evidence, protection, and audit history.
- Freshness is measured at consequential consumers, not inferred from broker availability or publisher throughput.
- Retirement closes publishers, subscriptions, caches, files, replay stores, mappings, credentials, histories, and recovery paths.

### Common failures

Common failures are updating a record and publishing separately; equating CDC rows with domain decisions; claiming global order from partition order; relying on timestamps for causality; treating at-least-once delivery as duplicate-free; deduplicating forever with an expiring event-ID cache; interpreting missing fields inconsistently; letting a patch target unknown state; deleting without a tombstone; losing merge aliases; activating future-effective changes immediately; using the latest mapping during replay; retrying poison records without bounds; replaying side effects; trusting a green broker while one consumer is stale; bootstrapping from a snapshot without its stream position; exposing protected attributes in routing metadata; and retiring the source before every consumer and recovery copy is closed.

### Compact example

A customer publisher emits entity revisions `1`, `3`, `2`, a duplicate `3`, and retirement revision `4`. The consumer applies `1`, buffers `3` because `2` is missing, applies `2`, drains `3`, ignores the duplicate, and applies the tombstone at `4`. Its evidence shows ordered applied revisions, two duplicate or stale deliveries, one detected gap, no pending records, and final retired state. That proves the small state-machine behavior, not end-to-end production convergence.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-035](035-event-driven-data-integration.md), [DARCH-036](036-change-data-capture-architecture.md), [DARCH-039](039-replication-and-synchronization.md), [DARCH-051](051-master-data-and-golden-records.md), [DARCH-054](054-match-merge-and-survivorship.md), and [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md) establish time, contracts, movement, authority, identity, and shared semantics. [DARCH-059](../ROADMAP.md) next governs shared data across these boundaries.

## Governing Question

Master data changes slowly relative to transactions, but its changes can alter thousands of decisions. A legal-name correction can affect sanctions screening, a product reclassification can change tax and routing, a supplier merge can redirect obligations, and a hierarchy move can restate reporting. “The event was sent” is therefore an inadequate completion claim.

The governing question is which semantic and operational architecture lets an owner commit a change once, distribute it through heterogeneous channels, tolerate partial failure and asynchronous consumers, preserve historical interpretation, and prove that each consequential consumer reached the appropriate state.

## Why This Matters

The CNCF [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md) defines interoperable event context including `id`, `source`, `type`, `subject`, `time`, and `dataschema`; it explicitly scopes duplicate recognition to `source` plus `id`. A standard envelope improves interchange but does not supply master-data revision, ordering, activation, or reconciliation policy.

[RFC 6902](https://www.rfc-editor.org/rfc/rfc6902) defines JSON Patch as an ordered sequence of operations, while [RFC 7386](https://www.rfc-editor.org/rfc/rfc7386) defines JSON Merge Patch with object-shaped replacement semantics and special treatment for null. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) defines HTTP method idempotence, validators, and conditional requests. These are useful mechanisms, but a propagation contract must still define the base revision, domain meaning, authorization, and conflict response.

Apache Kafka's [design documentation](https://kafka.apache.org/40/design/design/) distinguishes at-most-once, at-least-once, and exactly-once delivery concerns and explains partition-scoped ordering. Debezium's [change-event structure](https://debezium.io/documentation/reference/stable/transformations/event-flattening.html) preserves operation, source metadata, time, and before/after row state. Microsoft's [transactional outbox guidance](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos) illustrates committing state and an event atomically before asynchronous relay. No one mechanism proves that an external consumer applied the correct master-data meaning.

The GS1 [EPCIS 2.0.1 standard](https://ref.gs1.org/standards/epcis/2.0.1/) distinguishes event data and master data and defines identified document exchange. W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides provenance concepts for entities, activities, and agents. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthiness across the system lifecycle. Together they support treating propagation as a governed information product rather than an incidental message path.

## Prerequisites and Retrieval

You should understand master and reference data, golden records, identity resolution, survivorship, hierarchies, controlled vocabularies, transactions, database logs, events, APIs, files, queues, stream partitions, temporal modeling, schemas, caches, retries, reconciliation, security, reliability, recovery, and governance.

Retrieve authoritative change, command, decision, commit, domain event, change event, notification, snapshot, delta, patch, tombstone, outbox, change data capture, entity revision, event ID, correlation ID, causation ID, source position, sequence, watermark, checkpoint, idempotency, deduplication, gap, replay, backfill, projection, activation, reconciliation, drift, quarantine, dead-letter record, and dependency closure.

As a retrieval test, inspect “publish customer updates in real time.” Ask which customer authority, entity boundary, revision rule, change types, effective dates, transaction-to-publication bridge, payload contract, ordering scope, consumer inventory, latency class, protection policy, replay boundary, gap response, activation evidence, reconciliation procedure, recovery objective, and retirement owner apply. A topic name and latency target do not answer those questions.

## Learning Objectives

After completing this module, you should be able to:

1. separate authoritative decision, commit, publication, delivery, application, activation, and reconciliation;
2. choose among domain events, outbox relay, change data capture, APIs, snapshots, and files from semantic and operational needs;
3. design propagation envelopes with stable identities, revisions, source positions, schemas, temporal axes, provenance, and protection metadata;
4. define full-state, delta, patch, notification, merge, split, hierarchy, and tombstone semantics;
5. scope ordering and implement idempotent consumers that detect duplicates, stale revisions, gaps, and incompatible events;
6. bootstrap and replay consumers from snapshots and change streams without omission or double application;
7. govern schema and meaning evolution across independently deployed producers, intermediaries, and consumers;
8. design retries, quarantine, dead letters, backpressure, reconciliation, correction, and disaster recovery;
9. measure end-to-end freshness, completeness, divergence, activation, and business consequences; and
10. migrate or retire propagation paths only after consumer and evidence closure.

## Core Exposition

**Start with the decision consequence.** Inventory the decisions that depend on each master-data element and relationship.

Latency and consistency should follow consequence. A sanctions classification used before payment can require synchronous current validation, while a marketing display name can accept bounded asynchronous delay.

**Name the authoritative boundary.** State which domain, role, workflow, and system may approve each change type.

A hub can publish consolidated master data without owning legal identity, supplier qualification, product composition, or customer consent. Propagation must retain source authority.

**Separate request from accepted fact.** A command asks to change data. Validation, approval, matching, survivorship, and conflict handling determine whether an authoritative revision is committed.

Do not publish `CustomerChanged` merely because a request entered a queue. Publish the accepted outcome or a clearly typed workflow event.

**Separate commit from publication.** A successful database transaction does not prove an event exists, and a successful broker call does not prove the database transaction committed.

The dual-write gap can create lost changes or phantom events. Resolve it through one atomic boundary or a durable derivation and repair mechanism.

**Use a transactional outbox when the application knows the domain event.** Commit authoritative state and an outbox record in the same local transaction.

A relay can retry publication independently. Consumers must still tolerate duplicates because acknowledgement and relay-state updates can fail separately.

**Use change data capture when the database log is the durable source.** CDC can capture committed inserts, updates, and deletes without modifying every writer.

It observes storage mutations, not necessarily business intent. Row changes may split one domain decision, include maintenance writes, omit approval context, or expose physical schema.

**Enrich CDC deliberately.** Map physical changes to stable entity identities and event semantics at an owned boundary.

Preserve source coordinates and raw evidence for repair. Do not claim a semantic domain event if the transformation lacks enough context to establish it.

**Use application events for meaning, not optimism.** Domain-aware code can express `SupplierMerged` or `CustomerLegalNameCorrected` more clearly than `row_updated`.

The application still needs durable coupling to commit. Rich names do not repair an unreliable dual write.

**Do not require event sourcing by default.** An event-sourced master can preserve decision history as its authority, but it increases event-design, evolution, replay, and operational obligations.

Snapshot plus changes, temporal tables, or audited current state can be sufficient when requirements do not justify a permanent domain-event store.

**Define the propagation unit.** Choose the entity or aggregate boundary whose invariants and changes must travel together.

Publishing individual fields can expose impossible intermediate states. Publishing an entire enterprise customer graph can make every change huge and highly coupled.

**Give every propagation record identity.** Use a stable event ID scoped by producer source, separate from entity ID and entity revision.

Retries preserve the same event identity. A semantically new correction receives a new event ID and revision even if it reverses an earlier value.

**Expose entity identity explicitly.** The routing key, envelope subject, and payload identifier must follow a declared canonicalization rule.

When merges preserve aliases, consumers need both surviving identity and affected source identities. A broker key alone is not a durable business identifier contract.

**Version per entity or aggregate.** A monotonic entity revision provides a cheap stale-update and gap check within its scope.

Do not infer enterprise-wide order from it. Independent entities can progress concurrently without a global sequencer.

**Preserve source position.** A database coordinate, outbox sequence, or log offset supports exact bootstrap cuts, replay, diagnostics, and reconciliation.

Source position describes publication order in a source, not necessarily business-effective order across sources.

**Distinguish ordering scopes.** State whether order is guaranteed per entity, aggregate, partition, producer session, file, batch, or stream.

Partition by the identity whose changes require order. Changing keys during a merge or repartition needs an explicit handoff protocol.

**Do not use wall-clock time as a sequence.** Clocks skew, concurrent commits can share a timestamp, and intermediaries can publish late.

Use sequence or revision for ordering. Preserve timestamps for their actual semantic axes.

**Model temporal axes.** Keep business effective time, authoritative commit time, publication time, broker append time, receipt time, application time, and activation time.

A future-effective address can be committed and distributed today but should activate next month. A correction learned today can change the interpretation of an earlier interval.

**Choose full-state payloads when replacement is safe.** An event can carry the complete consumer-facing representation at revision `r`.

This simplifies recovery from missed intermediate revisions but increases payload size and exposure. Consumers must know whether absence means empty, withheld, inapplicable, or not included.

**Choose changed-field payloads when deltas are valuable.** Carry changed paths plus old and new values when consumers need impact detail.

Define the required base revision. Applying a delta to an unknown or different base can silently corrupt state.

**Use JSON Patch with its ordered semantics.** JSON Patch operations act against paths and can include tests before mutation.

Path stability, array indexing, authorization, base version, and atomic failure behavior require an explicit contract. A syntactically valid patch can be semantically invalid.

**Use JSON Merge Patch with explicit null policy.** Merge Patch is compact for object updates but uses null to remove members.

It cannot distinguish setting a field to JSON null from removing it without another domain convention. Arrays are replaced rather than edited element by element.

**Use notification events when the API remains the authority.** A small event can say entity `x` reached revision `r`; the consumer then retrieves an authorized representation.

This reduces event exposure and stale embedded payloads but adds API load, race handling, and dependence on representation retention.

**Support compare-and-set writes.** Conditional mutation using a revision or strong validator prevents a stale writer from overwriting concurrent work.

An HTTP `If-Match` contract can expose this mechanism. Idempotent HTTP method semantics do not by themselves deduplicate domain side effects in downstream systems.

**Make operation semantics explicit.** Distinguish create, update, correct, replace, deactivate, reactivate, merge, split, reparent, delete, purge, and restore.

Generic `upsert` loses the reason and lifecycle consequence. Consumers cannot infer whether history, aliases, relationships, or side effects need special treatment.

**Model deletion as a governed state transition.** A missing record can mean not loaded, filtered, unauthorized, compacted, failed, or deleted.

Publish a tombstone or typed retirement with identity, revision, reason class, effective time, retention, and replacement where allowed.

**Separate deactivate from delete.** Deactivation can preserve the entity for history and prohibit new use. Deletion can remove a representation but still require retained audit or non-resurrection markers.

Privacy erasure, legal hold, operational retirement, and business inactivity have different obligations.

**Propagate merges as identity operations.** Include survivor, absorbed identities, mapping relation, effective time, revision boundary, provenance, and affected relationships.

Consumers must redirect future use without rewriting facts that require historical source identity. Alias retention prevents a retired identifier from reappearing as new.

**Propagate splits without guessing.** A source entity divided into several successors usually needs evidence to classify existing facts.

Publish the successor set and decision requirements. Preserve unresolved migration when no deterministic mapping exists.

**Treat hierarchy changes as graph operations.** A subtree move, edge correction, or new placement affects descendants, rollups, permissions, and search.

Version the hierarchy release and relation type. A node update alone cannot communicate all derived impact.

**Bundle dependent changes when partial activation is unsafe.** A product, its classification, and an allowed code-set revision can require one release unit.

Use a release ID, manifest, dependency graph, and atomic consumer activation or a safe intermediate-state contract. Broker transactions do not automatically span external consumer databases.

**Publish schema identity.** The envelope identifies the event type and payload schema or compatible schema family.

Schema version is not entity revision. Changing a schema does not mean the master entity changed, and changing the entity does not necessarily change schema.

**Evolve additively where semantics permit.** New optional fields and event types can support rolling upgrades if consumers ignore unknown fields safely.

An optional field whose presence changes interpretation can still break consumers. Compatibility is semantic, not only syntactic.

**Version meaning as well as shape.** If the definition, units, authority, or state machine changes, publish that semantic change even when JSON shape stays constant.

Bind controlled vocabularies and mappings to versions. Replay must use the interpretation valid for the historical event or a declared restatement policy.

**Define missing-field behavior.** Full snapshots, sparse deltas, redacted views, and merge patches give absence different meanings.

Require an explicit payload mode and projection. Never let a consumer guess whether absence means clear, preserve, unknown, or forbidden.

**Make consumers declare bindings.** Record consumer, owner, purpose, entity scope, fields, event types, schema versions, latency class, activation rule, protection level, replay position, and retirement path.

Observed subscriptions can reveal undeclared dependencies, but they do not replace accountable registration.

**Design consumer idempotency around durable effects.** Record the applied entity revision or event identity in the same local transaction as the projection and downstream intent where possible.

An in-memory cache of message IDs disappears during restart. A short deduplication window cannot protect a long replay.

**Reject stale revisions safely.** If revision `r <= applied(x)`, verify whether it is an exact duplicate or an inconsistent reuse of revision identity.

Ignoring every lower revision can hide divergent histories. Retain digest or event evidence proportional to consequence.

**Detect gaps.** If revision `r > applied(x) + 1`, buffer, quarantine, or retrieve missing state according to contract.

Applying the later change may be safe for a complete replacement but unsafe for a patch. Record the gap even when replacement permits forward progress.

**Do not confuse commutativity with ordering.** Some set additions or maximum operations commute, while replacement, merge, split, and lifecycle transitions usually do not.

Document algebraic properties only for the exact operation and domain. Transport reordering remains an operational fact to observe.

**Set bounded retry policy.** Classify transient transport failures, throttling, unavailable dependencies, invalid schema, unauthorized content, and semantic conflicts.

Retry transient failures with backoff and jitter. Quarantine deterministic poison records instead of blocking a partition forever or retrying without limit.

**Operate dead-letter records as obligations.** Preserve original bytes, envelope, position, error class, attempts, protection, owner, and next action.

A dead-letter queue is not successful propagation. Measure age and consequence, provide safe redrive, and reconcile after repair.

**Control backpressure.** Slow consumers need bounded buffers, lag budgets, admission control, scaling, or degraded modes.

Dropping master-data changes is rarely an acceptable overload strategy. Coalescing is safe only when intermediate revisions have no required meaning and the final state is complete.

**Use snapshots for bootstrap.** Publish immutable, identified snapshots with schema, scope, record count, digest, generation time, source cut, and protection metadata.

The consumer loads snapshot `S` through source position `p`, then consumes changes strictly after `p`. An uncoordinated export and live stream create omission or duplication races.

**Make replay a designed operation.** Declare start and end positions, target consumer generation, event versions, transformation versions, side-effect suppression, rate limits, and completion evidence.

Replaying a projection update can be safe; replaying emails, payments, access grants, or external submissions can be catastrophic.

**Use backfill for newly required attributes or consumers.** Backfill can publish current state, historical changes, or purpose-built migration records.

Do not disguise a backfill as live history. Mark origin, generation, temporal semantics, and coverage.

**Reconcile independently of delivery.** Compare authoritative and consumer counts, identities, revisions, digests, lifecycle states, and selected semantic fields.

Transport acknowledgements prove only a transport boundary. Reconciliation detects software bugs, unauthorized transformations, expired dedupe state, manual edits, and missed subscriptions.

**Use layered reconciliation.** Compare stream watermarks and gap metrics continuously, partition counts and digests periodically, and high-consequence records semantically.

Aggregate equality can hide offsetting errors. Sampling alone cannot prove completeness.

**Repair from authority with history.** A repair can reissue an identified event, replace current state, or rebuild from a snapshot plus log.

Record which path was used and which prior consumer state was displaced. Silent manual editing destroys repeatability.

**Measure end-to-end freshness.** For change `e` and consumer `c`, measure publication lag, transport lag, application lag, activation lag, and total decision-visible lag.

Broker lag can be zero while a cache, search index, batch export, or application release still serves old master data.

**Measure completeness and divergence.** Track missing revisions, stale entities, duplicate deliveries, quarantined changes, dead-letter age, checksum mismatch, repair duration, and consumer acknowledgement.

Weight measures by entity criticality and decision consequence. A small count of stale sanctioned parties matters more than many stale descriptions.

**Trace causation and correlation carefully.** A correlation ID groups related work; a causation ID identifies the preceding event or command; neither is the unique event ID.

Preserve them across relays and transformations without exposing protected business identifiers in generic headers.

**Minimize propagation payloads.** Publish only fields required by declared consumers and purpose.

Wide golden-record events increase confidentiality risk, license exposure, bandwidth, retention burden, and accidental dependency. Use authorized projections or claim-check retrieval for sensitive detail.

**Protect metadata too.** Subjects, types, tenant IDs, classification codes, error strings, offsets, and routing keys can reveal identities or sensitive state.

Apply encryption, access control, tenant isolation, retention, audit, and log-redaction to envelopes, payloads, snapshots, dead letters, replay stores, and observability systems.

**Prevent cross-tenant propagation.** Partitioning and filters are not sufficient authorization boundaries by themselves.

Verify tenant identity at publication and consumption, scope credentials, test confused-deputy cases, and reconcile per tenant without leaking counts.

**Retain provenance through transformation.** Record source entity and revision, authoritative agent, transformation version, mapping version, publisher, and consumer application result.

Derived consumer identifiers and values should remain traceable without pretending the propagation platform made the business decision.

**Design correction propagation.** A correction creates a new revision and explicit relationship to affected prior assertions.

Identify which consumers, derived data, reports, decisions, files, indexes, models, and external recipients require repair or notification. Fixing current state alone can leave historical consequences wrong.

**Exercise disaster recovery.** Restore the authority, outbox or source log, broker or channel state, snapshots, schema artifacts, keys, consumer checkpoints, and reconciliation evidence.

Test duplicates, gaps, retention boundaries, restored old producers, credential rotation, and downstream side-effect suppression. A recovered broker with unrecoverable source positions is not full recovery.

**Plan migrations as dual evidence.** During a channel or publisher migration, correlate old and new propagation for the same authoritative revisions.

Compare content, order, latency, protection, error behavior, consumer activation, replay, and recovery. Do not declare equivalence from equal message counts.

**Use compatibility windows with owners.** Some consumers can upgrade gradually while producer emits multiple schema versions or maintains a retrieval API.

Bound the window, measure usage, prevent new legacy bindings, and name removal criteria. Permanent dual publication doubles semantic and operational risk.

**Retire by dependency closure.** Inventory publishers, relays, connectors, topics, APIs, files, subscriptions, caches, snapshots, dead letters, replay stores, credentials, transforms, mappings, consumers, dashboards, backups, and runbooks.

Prove every obligation moved or ended. Delete or revoke only under retention, legal, privacy, and recovery policy, and prevent an old restored component from republishing stale authority.

## Definitions and Notation

Let `X` be the set of master entities, `C` the set of bound consumers, and `E` the set of propagation records.

For `e ∈ E`, write `id(e)` for event identity, `x(e)` for entity identity, `rev(e)` for entity revision, `op(e)` for operation, `schema(e)` for payload schema, `pos(e)` for source position, and `digest(e)` for canonical content digest.

Let `commit(e)` mean the authoritative change represented by `e` committed. Let `published(e)`, `delivered(e,c)`, `applied(e,c)`, and `active(e,c)` describe successive evidence boundaries. None implies the next without a declared mechanism and evidence.

Let `a_c(x)` be the greatest contiguous entity revision consumer `c` has durably applied for `x`. A new record with revision `r` is expected next when `r = a_c(x) + 1`.

Define the gap set:

`Gap(c,x) = {r | 1 ≤ r ≤ max_seen(c,x) and r is neither applied nor explicitly superseded}`

Let `t_eff(e)`, `t_commit(e)`, `t_pub(e)`, `t_recv(e,c)`, `t_apply(e,c)`, and `t_active(e,c)` denote effective, commit, publication, receipt, application, and activation time.

End-to-end activation lag is:

`L_active(e,c) = t_active(e,c) - t_commit(e)`

when both observations exist and their clocks or measurement boundary are sufficiently trustworthy. Separate component durations are preferable when clocks cannot be compared.

Let snapshot `S(p)` contain authoritative state through source position `p`. A sound bootstrap loads `S(p)` and then processes the same source strictly after `p` under the source's ordering contract.

Let `A_r(x)` be authoritative entity state at revision `r` and `P_c(x)` the consumer projection. A reconciliation predicate can be:

`Converged(c,x,r) = a_c(x) ≥ r ∧ normalize_c(A_r(x)) = P_c(x) ∧ policy_c(r) is active`

The normalization function is versioned and purpose-bound; equality need not mean byte equality.

Define bounded freshness for consumer class `k` with target `Δ_k`:

`Fresh_k(e,c) = active(e,c) ∧ L_active(e,c) ≤ Δ_k`

Define propagation fitness:

`FitPropagation(P) = Authority ∧ AtomicSource ∧ Identified ∧ OrderedScope ∧ Temporal ∧ Compatible ∧ Idempotent ∧ Repairable ∧ Reconciled ∧ Protected ∧ Observable ∧ Recoverable ∧ Accountable ∧ Closed`

This is an assurance structure, not a mathematical claim that all consumers become consistent within one universal time bound.

## Mechanisms, Invariants, or Proof Structure

**Authority gate.** For each operation, prove the source, approver, entity boundary, effective-time policy, and decision consequence.

**Atomic-source gate.** Prove that a committed change cannot be permanently lost between authority and publication and that an uncommitted change cannot become an accepted fact.

**Envelope gate.** Validate event ID, entity ID, revision, operation, schema, source position, relevant times, provenance, payload mode, and protection classification.

**Ordering gate.** State the ordering scope, partition rule, expected revision, merge handoff, gap response, and behavior when no total order exists.

**Consumer gate.** For every binding, prove compatible interpretation, durable idempotency, base-state checks, unknown-field policy, lifecycle semantics, and atomic local effects.

**Temporal gate.** Keep committed, published, applied, and activated distinct; test future-effective, retroactive, late, and corrected changes.

**Bootstrap gate.** Bind snapshots to exact source positions and verify counts, digests, protections, stream handoff, and replay suppression.

**Failure gate.** Inject lost acknowledgements, duplicates, reordering, missing revisions, poison records, unavailable APIs, full queues, expired retention, and partial consumer writes.

**Reconciliation gate.** Compare watermarks, gap sets, counts, identities, revisions, digests, lifecycle states, and high-consequence semantic fields independently of normal delivery.

**Protection and service gate.** Verify least privilege, tenant isolation, payload minimization, encryption, retention, redaction, capacity, latency, backpressure, repair, and disaster recovery.

**Lifecycle gate.** Trace publishers, relays, channels, schemas, mappings, consumers, caches, snapshots, histories, credentials, backups, and accountable closure.

### Executable evidence: buffering gaps and applying revisions idempotently

The following small consumer applies per-entity revisions, buffers a gap, drains it when the missing revision arrives, rejects stale duplicates, and applies a tombstone.

<!-- bijux-verify: {"id":"master-data-revision-gap-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"applied_versions=1,2,3,4\nduplicate_or_stale=2\ngaps_buffered=1\nfinal_revision=4\nfinal_status=retired\nregion=west\nname=Acme Ltd\npending=0\n","stderr":""}} -->
```python
events = [
    {"event_id": "e1", "revision": 1, "operation": "replace",
     "data": {"name": "Acme", "region": "north", "status": "active"}},
    {"event_id": "e1", "revision": 1, "operation": "replace",
     "data": {"name": "Acme", "region": "north", "status": "active"}},
    {"event_id": "e3", "revision": 3, "operation": "merge",
     "data": {"name": "Acme Ltd"}},
    {"event_id": "e2", "revision": 2, "operation": "merge",
     "data": {"region": "west"}},
    {"event_id": "e3", "revision": 3, "operation": "merge",
     "data": {"name": "Acme Ltd"}},
    {"event_id": "e4", "revision": 4, "operation": "retire", "data": {}},
]

state = {}
applied_revision = 0
applied_versions = []
pending = {}
duplicate_or_stale = 0
gaps_buffered = 0

def apply(event):
    global state, applied_revision
    if event["operation"] == "replace":
        state = dict(event["data"])
    elif event["operation"] == "merge":
        state.update(event["data"])
    elif event["operation"] == "retire":
        state["status"] = "retired"
    applied_revision = event["revision"]
    applied_versions.append(applied_revision)

for event in events:
    revision = event["revision"]
    if revision <= applied_revision or revision in pending:
        duplicate_or_stale += 1
        continue
    if revision > applied_revision + 1:
        pending[revision] = event
        gaps_buffered += 1
        continue
    apply(event)
    while applied_revision + 1 in pending:
        apply(pending.pop(applied_revision + 1))

print(f"applied_versions={','.join(map(str, applied_versions))}")
print(f"duplicate_or_stale={duplicate_or_stale}")
print(f"gaps_buffered={gaps_buffered}")
print(f"final_revision={applied_revision}")
print(f"final_status={state['status']}")
print(f"region={state['region']}")
print(f"name={state['name']}")
print(f"pending={len(pending)}")
```

This evidence is deliberately narrow. It demonstrates deterministic behavior for one in-memory entity and six deliveries; it does not establish durable transactions, authentic authority, schema compatibility, event-ID uniqueness, divergent-revision detection, retention, concurrency, multi-entity ordering, future activation, transport guarantees, protection, reconciliation, capacity, or disaster recovery.

## Alternatives and Trade-Offs

**Synchronous authoritative API versus asynchronous propagation.** Synchronous reads reduce stale-copy risk for critical decisions but add latency and availability coupling. Asynchronous copies improve local availability and throughput but require freshness budgets, idempotency, replay, and reconciliation.

**Application domain event versus CDC.** Domain events can express intent and aggregate semantics but require reliable application integration. CDC observes committed storage broadly and supports legacy sources, yet exposes physical mutations and may need semantic enrichment.

**Transactional outbox versus broker transaction.** An outbox couples business state and publish intent in one local transaction and relays at least once. Broker transactions can atomically publish within supported broker boundaries but do not usually include an unrelated authority database or external consumer effect.

**Full-state event versus delta.** Full state is self-contained and easier to repair but larger and more sensitive. Deltas reveal change detail and save bandwidth but require correct base state and stronger ordering.

**Structured patch versus domain operation.** JSON Patch or Merge Patch provides reusable mechanics. Domain operations such as merge, split, or reparent retain intent that generic paths cannot express safely.

**Payload event versus notification plus retrieval.** Payload events allow offline, low-latency application and replay but retain copies. Notifications reduce exposure and centralize representation authorization but create API dependence and races between notification and retrieval.

**Per-entity order versus global order.** Per-entity ordering scales and matches most invariants. Global ordering simplifies some audit narratives but creates coordination, availability, and throughput costs and can still fail to represent causal order across authorities.

**Queue versus retained log.** A queue supports work distribution and acknowledgement. A retained log supports independent consumer positions and replay, but retention, compaction, schema evolution, and side-effect control become explicit obligations.

**Push events versus scheduled files.** Push provides low latency and fine-grained evidence. Files can be simpler for legacy or bulk consumers but need manifests, cut boundaries, checksums, late-file policy, and snapshot/delta semantics.

**Choreography versus orchestration.** Choreography decouples consumers and scales independent reactions but disperses workflow state. Orchestration makes required steps and compensation visible but adds a coordinator whose authority and failure behavior must be governed.

**Strict gap blocking versus forward replacement.** Blocking protects patch order and invariant transitions but can spread delay. A complete later replacement can permit forward progress while recording and repairing the gap; the contract must say which history and side effects may be skipped.

**Exactly-once mechanism versus idempotent effects.** A platform can narrow duplicate windows inside its transaction boundary. End-to-end propagation across databases, APIs, files, caches, and human activation still needs identified revisions, idempotent local effects, and reconciliation.

## Failure Modes and Misconceptions

1. **“The database commit and publish call are close enough.”** A crash between them creates a lost or phantom propagation record.
2. **“CDC is the business event.”** CDC proves a storage mutation, not necessarily the approved domain decision or aggregate boundary.
3. **“The timestamp orders changes.”** Clock skew, concurrency, and late publication invalidate that assumption.
4. **“Exactly once means consumers need no idempotency.”** Guarantees are bounded; external effects, retries, replays, and manual repair can duplicate work.
5. **“A duplicate event ID can always be ignored.”** Reused IDs with different content indicate producer corruption and require quarantine.
6. **“A later revision makes every missing revision irrelevant.”** Intermediate lifecycle, merge, compliance, and side-effect semantics may still matter.
7. **“Upsert covers every change.”** Merge, split, reparent, deactivate, delete, correction, and restoration carry distinct obligations.
8. **“Missing means delete.”** Missing can mean sparse delta, redaction, unsupported field, unknown, or unavailable source.
9. **“A patch is self-contained.”** It depends on path semantics, base revision, array behavior, and authorization.
10. **“Partition order is global order.”** It applies only inside the documented partition and producer/broker contract.
11. **“Future-effective data should wait to publish.”** Early publication can support preparation; application and activation times must remain separate.
12. **“A dead-letter queue solves poison messages.”** It only relocates an unresolved propagation obligation.
13. **“Replay is just resetting an offset.”** Schemas, transformations, side effects, protections, rate, and target state must be controlled.
14. **“Equal counts prove convergence.”** Missing and extra entities or offsetting value errors can preserve totals.
15. **“Zero broker lag means fresh master data.”** Consumer storage, indexes, caches, application releases, and decision paths can remain stale.
16. **“The golden record should be broadcast whole.”** Consumers usually need purpose-limited projections, not every protected attribute.
17. **“A backup restores propagation.”** Source positions, checkpoints, schemas, keys, dedupe state, and reconciliation evidence also matter.
18. **“No subscribers means the channel can be deleted.”** Offline files, annual jobs, manual users, recovery paths, or undeclared consumers may remain.

## Worked Examples

### Example 1

A customer legal-name correction is approved at revision 42 with an earlier effective date. The publisher commits current temporal state and an outbox event atomically. Screening consumers activate immediately under correction policy; invoices preserve the name rendered at issue time while linking the corrected identity. Reconciliation checks both current projections and affected historical decisions.

### Example 2

A future warehouse address is approved today for activation next quarter. Consumers store the new revision on receipt but schedule activation by business effective time. A routing system reports receipt, application, and activation separately, and retains the prior interval for shipments planned before the boundary.

### Example 3

A product category subtree moves between reporting parents. The propagation unit is a hierarchy release, not a single product row. The event identifies changed direct edges, release version, effective interval, affected descendant scope, and rollup policy. Reporting rebuilds its closure and compares before-and-after totals before activation.

### Example 4

Two supplier masters merge into one survivor. The event carries survivor ID, absorbed IDs, alias policy, effective time, evidence reference, and relationship impact. Procurement redirects future selection, accounts payable preserves historical supplier identity, and sanctions screening reevaluates the consolidated party rather than treating the merge as a simple delete.

### Example 5

A shared risk code is deprecated and split into two successors. The vocabulary release propagates before dependent master updates. Records with distinguishing evidence migrate through explicit operations; ambiguous records enter an unresolved state. Consumers do not choose the first successor or reinterpret old facts with the latest value set.

### Example 6

A consumer misses revisions 806–811 after credential expiry but later receives 812. It quarantines a patch at 812, refreshes authorization, retrieves a snapshot through source position `p`, verifies manifest and digest, then consumes changes after `p`. Independent reconciliation proves entity revisions and selected semantic fields match before the quarantine is closed.

### Example 7

A fraud service needs risk tier and entity status but not customer name, address, or birth date. The publisher emits a purpose-specific projection and opaque subject ID, while detailed retrieval requires separate authorization. Dead-letter and trace systems inherit the same classification and retention instead of logging the wide golden record.

### Example 8

A legacy planning system receives nightly files. Each immutable file declares source cut, previous file, full-versus-delta mode, schema, record count, partition digests, effective dates, and tombstones. A missing file blocks delta activation; the consumer can bootstrap from a full snapshot and then resume numbered deltas.

### Example 9

After regional disaster recovery, a restored relay starts behind the broker while one consumer checkpoint is ahead of its restored projection. Fencing prevents the old producer from publishing, and reconciliation selects a coherent snapshot and source position. Replay suppresses external notifications, restores projections, and only then re-enables live effects.

### Example 10

An organization replaces a central MDM publish topic with domain-owned streams. During comparison, old and new records correlate to the same authoritative revisions and are checked for content, order, protection, latency, replay, and consumer activation. The old path retires only after annual file consumers, caches, dead letters, credentials, backups, and runbooks move or close.

## Cross-Program Connections

- **Data Engineering:** [DE-026](../../19-data-engineering/modules/026-database-change-data-capture.md), [DE-027](../../19-data-engineering/modules/027-idempotent-loads.md), and [DE-060](../../19-data-engineering/modules/060-handling-late-duplicate-and-out-of-order-events.md) implement capture and consumer mechanics whose architecture is governed here.
- **API and Service Engineering:** [API-006](../../28-api-and-service-engineering/modules/006-conditional-requests.md), [API-067](../../28-api-and-service-engineering/modules/067-idempotent-consumers.md), and [API-070](../../28-api-and-service-engineering/modules/070-designing-an-asynchronous-api-for-replay-and-evolution.md) connect conditional mutation, durable effects, and replayable contracts.
- **Platform Engineering:** [PLAT-052](../../29-platform-engineering/modules/052-desired-state-and-reconciliation.md), [PLAT-055](../../29-platform-engineering/modules/055-idempotent-reconciliation.md), and [PLAT-086](../../29-platform-engineering/modules/086-backup-and-restore-of-platform-state.md) provide control loops and recovery capabilities without owning master-data meaning.
- **Database Engineering:** [DBE-041](../../18-database-engineering/modules/041-acid-and-transaction-boundaries.md), [DBE-073](../../18-database-engineering/modules/073-log-sequence-numbers.md), and [DBE-074](../../18-database-engineering/modules/074-undo-and-redo-logging.md) explain transaction, log-position, and recovery boundaries.
- **Distributed Systems Engineering:** partial failure, clocks, causal and total order, queues, logs, delivery semantics, duplicate effects, and convergence deepen the guarantees used here.
- **Security Engineering:** workload identity, classification, minimization, encryption, tenant isolation, signing, audit, retention, and incident response constrain publisher identity, payload exposure, and evidence.

## References

1. Cloud Native Computing Foundation, [CloudEvents Specification 1.0.2](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md).
2. IETF, [RFC 6902: JavaScript Object Notation (JSON) Patch](https://www.rfc-editor.org/rfc/rfc6902).
3. IETF, [RFC 7386: JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7386).
4. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110).
5. Apache Software Foundation, [Apache Kafka Design: Message Delivery Semantics](https://kafka.apache.org/40/design/design/).
6. Debezium, [New Record State Extraction and Change Event Structure](https://debezium.io/documentation/reference/stable/transformations/event-flattening.html).
7. Microsoft, [Implement the Transactional Outbox Pattern by Using Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos).
8. GS1, [EPCIS Standard 2.0.1](https://ref.gs1.org/standards/epcis/2.0.1/).
9. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/).
10. National Institute of Standards and Technology, [SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final).

## Exercises

### Exercise 1

Design propagation for customer, supplier, and product masters used by online screening, operational services, search, analytics, a nightly legacy file, and an annual regulatory process. Define authority, change records, channels, ordering, time, consumer bindings, protection, reconciliation, recovery, and closure.

### Exercise 2

A service writes its master row and then publishes an event. Production has both committed changes with no event and events whose transaction rolled back. Replace this dual write and define evidence that the replacement handles crash, retry, duplicate, ordering, and repair cases.

### Exercise 3

A consumer receives entity revisions `70`, `72`, `71`, duplicate `72`, correction `73` effective in the past, and retirement `74` effective next month. Define storage, application, activation, historical interpretation, acknowledgement, and reconciliation behavior.

### Exercise 4

Compare a full-state event, changed-field event, JSON Patch, JSON Merge Patch, and notification-plus-retrieval contract for protected supplier master data. Choose a design and state its compatibility and failure behavior.

### Exercise 5

An enterprise is retiring a central propagation hub after moving publishing to domain products. Define the dependency inventory, dual-run evidence, consumer migration, recovery proof, retention actions, and closure decision.

## Answers to the Exercises

### Answer 1

Name the authoritative domain, approver, entity and aggregate boundaries, business keys, identity and survivorship policy, and effective-time rules for every operation. Define event ID, entity ID, revision, source position, operation, schema, payload mode, vocabulary and mapping versions, provenance, classification, and relevant times. Use synchronous current validation for decisions that cannot tolerate stale screening data; publish purpose-limited asynchronous projections for local operational, search, and analytical use. Give the legacy file an immutable snapshot or delta manifest and preserve a supported retrieval path for the annual consumer.

Register each consumer's owner, purpose, fields, event types, schema range, ordering scope, latency and activation target, unknown and missing-field behavior, replay position, protection level, and retirement path. Commit change and publish intent atomically or derive publication from a durable log. Partition by the identity whose revisions require order; make consumers durable and idempotent, detect gaps, and distinguish future-effective application from activation. Reconcile watermarks continuously, counts and digests periodically, and high-consequence values semantically. Test source, broker, file, cache, credential, region, replay, and restoration failures. Close only when all live, offline, annual, manual, and recovery dependencies move or end.

### Answer 2

Replace the independent writes with a transactional outbox if the service knows the domain event: in one local transaction, validate the command, write authoritative revision `r`, and append a uniquely identified outbox record containing the same entity revision. A relay reads committed outbox records, publishes with stable event identity, and records relay progress. Alternatively, capture the committed database log and enrich it at an owned semantic boundary if application modification is impractical. Do not call either approach exactly-once end to end.

Inject a crash before commit, after state and outbox commit, before publish acknowledgement, after publish but before relay checkpoint, and during consumer application. Prove no uncommitted revision is accepted, every committed revision remains discoverable, retries reuse identity, duplicate delivery yields one durable consumer effect, per-entity order and gaps are visible, and poison records quarantine without losing later evidence. Compare authority, outbox or log, broker, and consumer watermarks. Reconcile a deliberately removed publication, repair it from the durable source, and verify the consumer projection and activation. Retain failure evidence and document the exact transaction and retention boundaries.

### Answer 3

Assuming per-entity contiguous revisions and delta semantics, apply 70 durably with its event evidence. Buffer or quarantine 72 because 71 is missing; when 71 arrives, apply 71 then 72 in revision order in the same controlled processing flow. Treat the second 72 as a duplicate only after confirming event identity or canonical digest agrees; different content at the same revision is producer corruption. Store correction 73 as a new immutable revision linked to affected prior assertions. Apply its current projection according to correction policy while preserving effective and transaction time so historical consumers can distinguish as-was from restated views.

Store retirement 74 on receipt but schedule business activation for next month. Systems preparing future work may observe the scheduled state, while current decisions continue under revision 73 until the effective boundary. Acknowledge transport only after durable local application or quarantine evidence according to the channel contract. Report separate received, applied, and activated watermarks. Reconcile the authoritative revision chain, event identities, effective intervals, current projection, scheduled retirement, and any decisions affected by retroactive correction. Clock time never substitutes for the revision sequence.

### Answer 4

A full-state event is self-contained and can supersede missed intermediate states, but it maximizes payload exposure and requires precise absence semantics. A changed-field event reduces volume and exposes before/after impact, but it requires the correct base revision. JSON Patch provides ordered path operations and optional tests; it is brittle when paths or arrays evolve. JSON Merge Patch is compact for object-shaped change but treats null as removal and replaces arrays. Notification plus authorized retrieval minimizes retained event detail and centralizes current projection policy, but it adds API availability, thundering-herd, race, and historical-representation obligations.

For protected supplier data, publish a small notification containing opaque subject, entity revision, operation class, schema, relevant times, and non-sensitive routing metadata. Consumers retrieve a purpose-specific representation with authorization and `If-Match` or revision-aware semantics; the authority retains representations or complete replacements long enough for replay. For offline consumers, publish an encrypted minimal full-state projection rather than forcing unavailable retrieval. Define cache keys, representation revision, race handling when a later notification arrives first, not-found versus retired behavior, rate and backpressure limits, schema compatibility, retention, and a snapshot repair route. Measure retrieval and activation, not only notification delivery.

### Answer 5

Inventory authoritative writers, match and survivorship workflows, outboxes, CDC connectors, relays, topics, queues, APIs, files, schemas, mappings, transformations, subscriptions, consumer checkpoints, caches, indexes, snapshots, dead letters, replay stores, dashboards, alerts, credentials, network rules, histories, backups, retention rules, legal holds, deletion paths, incident duties, and recovery runbooks. Discover undeclared consumers through logs and network evidence, but require accountable owners to confirm purpose and closure. Map every operation, ordering guarantee, temporal rule, protected projection, service target, and repair responsibility to a receiving domain product or prove it is no longer required.

Dual-run old and new paths against the same authoritative revisions. Compare event identity correlation, content, schemas, ordering, gaps, latency, transformations, mappings, tenant isolation, retries, dead letters, replay, snapshots, recovery, and consequential consumer activation. Migrate consumers by cohort, including offline, annual, manual, and disaster-recovery users; prevent new legacy subscriptions. Exercise regional restore and old-backup fencing before cutover. Freeze the old publisher at an explicit source position, drain and reconcile every binding, retain or delete artifacts under policy, revoke credentials, remove routes, and verify a restored old hub cannot republish stale authority. Accountable semantic and operational owners jointly accept the closure evidence.
