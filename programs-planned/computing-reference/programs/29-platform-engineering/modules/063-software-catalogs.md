---
module_id: PLAT-063
program: Platform Engineering
level: 2
module_number: 63
title: Software Catalogs
status: complete
last_verified: 2026-09-02
---

# Software Catalogs

## One-Page Review

### Governing question

How should a platform build a trustworthy software catalog from heterogeneous sources so people can discover ownership, systems, APIs, dependencies, and lifecycle state without confusing a derived graph with universal truth or letting stale metadata drive unsafe automation?

### Essential definitions

- A **software catalog** is a governed, queryable model of selected software entities, relationships, metadata, and provenance assembled for defined user journeys.
- An **entity** is an identified catalog subject such as a component, API, resource, system, domain, group, user, or template.
- An **entity reference** is a canonical kind/namespace/name identity; display title, repository URL, provider ID, and database UID serve different roles.
- A **source of authority** owns a fact; an **ingestion source** merely delivers facts and may not be authoritative for all fields.
- An **entity provider** supplies a declared set or stream of source entities and owns its ingestion bucket and deletion semantics.
- A **processor** validates, transforms, enriches, or emits relations/children during catalog processing; it is not generally the best remote inventory poller.
- **stitching** combines processed fragments according to deterministic ownership/conflict rules into the final entity view.
- **provenance** records where, when, and at which revision a field or relation was observed or derived.
- An **orphan** is an entity no longer connected to its former ingestion/parent path; orphan status is evidence requiring policy, not automatic proof of nonexistence.
- A **catalog coverage denominator** is the independently derived population against which catalog completeness is evaluated.

### Central model, mechanism, or theorem

For catalog fact $f$ about entity $e$, model a candidate assertion as

$$
a=(e,f,v,s,r,t,q),
$$

where $v$ is value, $s$ source, $r$ source revision, $t$ observation time, and $q$ quality/confidence evidence. A deterministic resolution policy $R_f$ selects or rejects assertions based on field ownership, source priority, freshness, validation, and conflict—not arrival order. If an independent inventory contains $N$ in-scope subjects and $M$ match canonical catalog identities, measured coverage is $C=M/N$; catalog count alone is not coverage. The ingestion pipeline discovers, normalizes, validates, resolves identity, enriches, derives bounded relations, stitches, indexes, serves permission-filtered views, measures freshness/conflicts/orphans, and reconciles deletion. Consequential automation rereads the owning authority.

### Critical invariants

- Catalog scope and user journeys are explicit; the graph models useful mental/domain relationships rather than every observable object.
- Each entity kind, identity, namespace, lifecycle, owner, schema version, and deletion/recreation behavior is defined.
- Every authoritative or derived field/relation has source, ownership, precedence, revision/time, validation, conflict, and staleness semantics.
- Two providers cannot silently claim one identity; duplicate/collision is quarantined or resolved by deliberate policy.
- Ownership displayed in the catalog is contact/accountability metadata unless a separate authoritative policy explicitly grants permissions.
- Missing, stale, unprocessed, unauthorized, conflicted, and orphaned are distinct states; none silently becomes “does not exist.”
- Relations state direction, semantics, producer, target resolution, and freshness; catalog dependency edges are not automatically runtime readiness or deletion authority.
- Search and graph views filter authorization before disclosure and cannot bypass field/entity-level access policy.
- Ingestion, processing, stitching, indexing, and queries have bounded work, backpressure, cardinality control, observability, and replay/rebuild paths.
- Non-derivable annotations, manual decisions, provenance, and audit are backed up; derived views are reproducibly rebuilt and verified.

### Common failures

Calling the catalog a universal source of truth; registering everything that has an API; identifying by display title; allowing duplicate providers to race; last-writer-wins ownership; parsing repository URL as service identity; group membership from stale YAML; catalog ownership as runtime authorization; free-form types without governance; annotations as arbitrary data dump; inferred relations without provenance; dependency graph as call graph; deleting orphans immediately; absence as decommissioned; search before authorization; one processor calling slow providers for every entity; full scans without provider buckets/deltas; coverage from catalog count; freshness from row update time; and retiring a source without disposing its entities.

### Compact example

Repository YAML owns a service’s description, lifecycle, system, and API declarations; the identity directory owns teams and membership; the production registry owns deployment/runtime facts; the incident system enriches current support state. All assertions normalize to `Component:payments/ledger-api` with source revision and observed time. A conflict in `ownedBy` between repository and directory policy produces `OwnershipConflict`, not last-write victory. Relations distinguish `partOf`, `providesApi`, `dependsOn`, and observed runtime links. Search filters entities before ranking. A 24-hour-stale deployment fact remains visibly stale and cannot authorize deletion. When the repository disappears, the entity becomes source-missing/orphaned, enters a retention and owner-notification workflow, and is deleted only after authoritative decommission evidence. Coverage compares the catalog to an independent repository/runtime inventory.

### Connections

This module deepens the portal read-model boundary from [PLAT-062](062-developer-portal-architecture.md) and layered authority from [PLAT-061](061-platform-api-layers.md). It uses identity, conditions, dependencies, and recovery principles from [PLAT-057](057-status-conditions-and-drift.md), [PLAT-058](058-cross-resource-dependencies.md), and [PLAT-059](059-control-plane-failure-and-recovery.md). PLAT-064 specializes ownership and metadata governance.

## Governing Question

How can a catalog integrate human-maintained and machine-observed knowledge into a dependable discovery graph while keeping provenance, uncertainty, authority, and lifecycle visible?

Catalog usefulness comes from coherence, not volume. A user wants to find the service behind an alert, its owner, documentation, API, dependencies, and lifecycle. Recording every Pod, branch, dashboard, job, and cloud object can bury that mental model and create unsustainable processing.

Catalog trust fails when a derived view pretends to be truth. Repository metadata, identity directories, runtime registries, cloud APIs, domain control planes, finance, and incident systems own different facts. The catalog resolves and presents them, but dangerous decisions must respect those ownership boundaries.

## Why This Matters

At organizational scale, software becomes invisible. Unknown owners delay incidents and security remediation; duplicate capabilities waste work; undocumented APIs increase coupling; undecommissioned resources cost money and retain risk.

A catalog can create shared vocabulary and navigation. It also creates attractive automation hooks. If stale or ambiguous metadata triggers access, deletion, compliance, or paging, a convenience database becomes a control-plane hazard.

Ingestion sources fail and disagree. Repositories move, teams rename, organizations merge, provider inventories lag, webhooks duplicate, and processors change. Explicit identity and provenance let the system surface disagreement rather than silently rewrite history.

Catalog scale is graph and pipeline scale. One slow enrichment on every entity or one high-cardinality relation can overload processing, indexing, and portal pages. Bounded models and incremental providers matter early.

## Prerequisites and Retrieval

Retrieve entity-relationship and graph models, bounded contexts and ubiquitous language, identifiers and namespaces, schemas and versioning, metadata/labels/annotations, systems of record, provenance and lineage, ingestion and ETL, snapshots versus deltas, idempotency, deduplication and entity resolution, validation, processing/stitching/materialized views, conflict resolution, eventual consistency and freshness, orphan/tombstone lifecycle, search/indexing/ranking, authorization and information disclosure, ownership and organizational directories, APIs and software systems, dependency semantics, SLOs/data quality, queues/backpressure, audit, backup/restore, migration, and decommissioning.

You should distinguish catalog entity from runtime resource; kind from type; canonical reference from display title; source authority from transport provider; raw assertion from resolved field; provider from processor; enrichment from ownership; declared from observed relation; graph navigation from reachability proof; catalog owner from authorization principal; absent from unknown; stale from false; orphan from deleted; entity UID from stable external reference; processing time from source observation time; count from coverage; and reconstructible data from non-derivable catalog state.

## Learning Objectives

After completing this module, you should be able to:

1. define catalog scope, personas, journeys, entity kinds, identities, namespaces, and lifecycle;
2. assign authoritative sources and deterministic field/relation resolution with provenance;
3. design snapshot, delta, webhook, and human ingestion with provider ownership and deletion semantics;
4. separate providers, processors, stitching, indexes, caches, and canonical views;
5. model ownership, systems, APIs, resources, dependencies, and observed relationships without semantic collapse;
6. secure entity ingestion, queries, search, annotations, links, and cross-tenant disclosure;
7. measure freshness, validity, conflict, orphan rate, coverage, usefulness, and processing health;
8. test scale, replay, duplicates, source outage, schema change, restore, merge/split, and retirement; and
9. use the catalog safely as discovery/read model while rereading authority for consequential action.

## Core Exposition

### Start from catalog journeys and boundaries

Identify questions the catalog must answer: What does this team own? Who supports this service? Which API should I use? What depends on this system? Which production services lack runbooks? What is being retired? Where is authoritative documentation?

Define personas and freshness needs. An onboarding discovery view can tolerate hours of lag; an incident owner lookup may require minutes; runtime access authorization may not belong in the catalog at all. One “fresh” label is insufficient.

Select domain-level entities that match organizational mental models. Components, APIs, resources, systems, domains, groups, users, templates, and capability offerings are common. Avoid mirroring every ephemeral runtime object; link to a suitable inventory/observability system instead.

State non-goals: the catalog is usually not configuration deployment, primary identity, metrics storage, CMDB replacement for every asset, secret store, or transactional runtime dependency. It can index/link these authorities.

Write success outcomes such as time to find correct owner/API, percent of in-scope production systems with fresh support metadata, or incident routing accuracy. Entity count alone rewards noise.

### Define kinds and semantic identities

Each kind has purpose, schema, required fields, lifecycle, relationships, authority, and consumers. `Component` should not mean repository in one team, deployment in another, and business application in a third.

Canonical identity commonly uses kind, namespace, and name. Normalize case and syntax deterministically. Display title is mutable and nonunique. Repository URL can change. Database-generated UID can change on reingestion. Provider IDs identify external effects, not necessarily the catalog concept.

Namespaces partition names and sometimes organizational domains; they are not automatic tenant security. Define defaulting rules so shorthand references resolve predictably. Fully qualify stored relations.

Decide rename, move, merge, split, and recreation behavior. Maintain aliases/tombstones and redirects for a bounded period; do not silently reuse an old identity while consumers cache it. Link successor/predecessor with explicit migration evidence.

Avoid identity derived from mutable owner or source path unless changes are modeled. Persist stable source keys and compare before treating a newly observed record as a new entity.

### Assign authority field by field

No source owns an entire entity merely because it first registered it. Repository maintainers may own description and API declaration; identity directory owns team membership; domain API owns environment status; security inventory owns classification findings.

Create an authority matrix per field/relation: source(s), precedence, allowed writers, merge operation, validity, freshness, conflict policy, sensitivity, and fallback. “Last writer wins” substitutes network timing for governance.

Some facts combine. A displayed owner may resolve a repository-declared team reference against the directory’s current identity. Preserve both assertion and resolution evidence. If the team is missing, report unresolved ownership rather than inventing a user.

Enrichment must not overwrite declared authority without a defined rule. Generated annotations need owned prefixes and provenance. Manual exceptions require accountable editor, reason, expiry, and audit.

For high-consequence facts, expose the authority link and observation. The catalog can show “production,” but compliance/deletion must query the authoritative lifecycle system.

### Represent assertions and provenance

Store enough provenance to explain every resolved field: provider/source identity, source object/key, revision or ETag, observation and processing time, transformation/processor version, confidence/validation, and conflict disposition.

Separate source observation time from catalog write time. Reprocessing yesterday’s snapshot today does not make the fact fresh. Preserve tombstone/removal time and source cursor for deltas.

Provenance can be bounded. Repeated identical observations need not produce unbounded history in the hot entity. Keep current assertion set and route history/audit to retained storage according to need.

Do not expose sensitive source paths, group membership, vulnerabilities, or internal IDs to unauthorized users. Provenance itself has classification and access policy.

Use stable processor/provider identifiers and versions so an incident can identify which transformation emitted a bad relation.

### Choose the right ingestion mechanism

Use source-controlled descriptors when domain owners can maintain durable metadata alongside code and review changes. Do not force machine-owned runtime facts into hand-edited YAML.

Use entity providers for remote systems or inventory. A provider owns a stable bucket, scheduling, full/delta semantics, pagination, cursor/checkpoint, rate limits, authentication, retry, and removal. Two providers claiming one identity must not race silently.

Use incremental providers for large paged sources. Persist cursors only with a coherent ingestion contract; handle page retry, source mutation between pages, duplicate record, and incomplete sweep. Periodic full reconciliation repairs missed deltas.

Use processors for validation, normalization, enrichment, relation derivation, and child emission inside the processing loop. Avoid slow remote calls per entity in a globally scheduled processor; bulk/provider read models scale better.

Webhooks reduce latency but are hints unless the source guarantees delivery/history. Authenticate, deduplicate, order by source revision, and reconcile periodically. Manual registration remains governed ingestion with provenance and lifecycle.

### Normalize before resolving identity

Decode against versioned schemas, reject or quarantine malformed input, canonicalize names/references, validate bounds, and preserve raw evidence for diagnosis. Do not let one hostile/oversized descriptor exhaust the pipeline.

Resolve a source record to canonical identity using kind-specific rules and stable source keys. Detect ambiguous matches rather than fuzzy-merging two payment services because names look similar.

Deduplicate within a provider by source ID/revision. Across providers, apply declared identity ownership. If two authorities legitimately contribute, keep separate assertion namespaces and stitch by field policy.

Treat normalization changes as migrations. A new lowercasing, separator, or namespace rule can collide formerly distinct entities. Preview collision sets and provide redirects/disposition.

Quarantine invalid/colliding records with source, reason, first/last observation, retryability, and owner. Silent drop makes coverage unknowable.

### Process and stitch deterministically

Processing validates kind policy, enriches fields, derives relations, and emits children/fragments. Order and version matter; record them and test fixtures. Avoid processors that depend on incidental registration order without explicit contract.

Stitching selects assertions by deterministic per-field rules. If equally authoritative fresh sources disagree, publish a conflict state rather than choose by timestamp. Consumers need to know the value is unresolved.

Make processing idempotent. Reprocessing unchanged source at the same revisions yields semantically identical entity and relations. Stable canonical serialization/digests help detect unnecessary churn.

Keep last-known-good output only under explicit policy. Show that processing now fails and when the last valid source was observed. For security-critical facts, stale fallback may be forbidden.

Index only stitched, authorized-ready representations or keep unprocessed/quarantine views separately permissioned. Operators need pipeline evidence that ordinary users should not see.

### Model the catalog graph precisely

Define relation direction and meaning: `ownedBy/ownerOf`, `partOf/hasPart`, `providesApi/apiProvidedBy`, `consumesApi/apiConsumedBy`, `dependsOn/dependencyOf`, and domain-specific edges. Generate inverse edges consistently.

A declared `dependsOn` means a catalog relationship under its definition; it may not prove runtime traffic, readiness, lifecycle ownership, or deletion order. Observed call/data-flow relationships need source, window, confidence, and expiration.

Resolve references to canonical kind/namespace/name. Missing target produces unresolved relation evidence, not an invisible dropped edge. Avoid selectors across large mutable sets unless bounded and owned.

Detect self-edges, duplicate edges, impossible kind pairs, and unexpected cycles where semantics require a DAG. General software dependency graphs can have cycles; report strongly connected components rather than pretending topological order exists.

Bound graph queries and visualization. High fan-out dependencies, organization groups, and generated resources need pagination/depth limits. “Show everything” can become denial of service and cognitive overload.

### Separate ownership metadata from authorization

Catalog ownership supports discovery, accountability, and routing. It may name one ultimate owner while contributors/operators are separate. The field is not automatically proof that the current user may mutate runtime resources.

Resolve owner references against a current authoritative directory and display whether the group exists, is active, has contacts/escalation, and when membership was observed. Do not expose membership broadly without policy.

Authorization systems may consume carefully governed ownership facts, but must bind to authoritative identity, freshness, approval, and failure behavior. A repository author should not grant production access merely by editing `spec.owner`.

Model transfer as workflow: current/new owners, approvals, effective time, repository/provider/catalog changes, on-call/support, cost, credentials, and audit. Avoid temporary unowned states.

PLAT-064 deepens ownership fields, metadata stewardship, validation, and organizational change.

### Govern metadata vocabulary

Core envelope fields and kinds form a versioned public model. Types, lifecycle values, tags, annotations, link types, and status items also need registries/owners where consumers interpret them.

Use DNS-like prefixes for extension ownership. An annotation used only as an opaque link can be looser than a field driving UI, policy, or automation. Document value schema, sensitivity, producer, consumer, and retirement.

Avoid uncontrolled synonyms such as `prod`, `production`, `live`, `prd`. Canonicalize governed values and retain aliases only during migration. Free-form tags remain useful for discovery but should not secretly drive security policy.

Descriptions and links are untrusted display content. Validate schemes/hosts as needed, sanitize rendering, detect broken links, and avoid secret-bearing URLs.

Extend kinds only when the conceptual model requires it and downstream clients can handle it. A new kind has schema, processors, permissions, presentation, relations, ownership, versioning, and migration cost.

### Express uncertainty and freshness

Entity existence, field validity, relation resolution, processing health, source reachability, and freshness are separate. Publish machine-readable states plus actionable explanations.

Define freshness per fact/source. Team membership might expire in hours; repository description in days; deployment health in minutes. Set `observedAt` from source observation and track last successful synchronization separately from last attempt.

When a source is down, retain last-known values only if policy permits, mark them stale, and avoid mass deletion. A complete-snapshot provider must distinguish authoritative empty snapshot from failed/incomplete fetch.

Use hysteresis or confirmation for removals from eventually consistent sources. Tombstones protect against reappearance/reordering and support redirects/audit.

Consumers declare their tolerance. A portal can display stale description; incident paging may fall back to an on-call authority; destructive automation must reread and may block.

### Handle orphan and deletion lifecycle

Orphan causes include parent no longer emitting a child, source move, processor change, missing location, permissions, rename, decommission, or ingestion bug. They are not equivalent.

Record cause, source/parent, first/last seen, last successful processing, owner, policy, and deadline. Notify owner and provide reclaim, redirect, transfer, archive, or delete actions.

Provider full-sync deletion must be atomic enough to avoid deleting the unseen tail after a partial page failure. Delta deletion uses versioned tombstones and periodic reconciliation.

Deleting a catalog entity removes a view, not necessarily code, service, data, cloud resources, or legal records. Never infer runtime deletion authority from catalog cleanup.

Retain aliases/tombstones for deep links and dependent references as policy requires. Verify reverse relations and search documents are removed or redirected.

### Secure ingestion and querying

Authenticate providers/webhooks and authorize locations/sources. Restrict arbitrary URL ingestion to prevent SSRF, credential forwarding, or untrusted template/plugin discovery. Validate redirects, schemes, hosts, sizes, and content.

Treat all descriptors, annotations, links, status, and provider error text as untrusted input. Sanitize presentation and logs; prevent formula injection in exports; do not fetch active content implicitly.

Apply entity/field/relation authorization before query results, aggregations, graph traversal, and search indexing/disclosure. Counting unauthorized entities or exposing autocomplete names can leak sensitive systems.

Provider credentials are scoped by source and read need. Separate identity-directory, repository, cloud, and security inventories. Audit registration, provider changes, manual mutations, conflict overrides, deletes, and sensitive reads.

Set quotas and limits for entities per provider/tenant, descriptor size, relations, tags, annotations, locations, queries, pagination, depth, and processing emissions.

### Scale the ingestion and query planes

Partition provider work by source/tenant and use snapshot/delta contracts, pagination, checkpoints, backoff, jitter, and rate limits. One failing source should not starve others.

Processing queues coalesce repeated updates by source/entity revision. Bound processor time and emitted children/relations. Move expensive remote enrichment into a provider or bulk cache.

Stitch incrementally from changed fragments and relation neighborhoods where correct. Avoid rebuilding the full graph for one description edit. Maintain reverse indexes for references and source ownership.

Query APIs require pagination, field selection, bounded filters, authorization-aware indexes, and cancellation. Graph traversal has depth/node/time budgets. Search indexes update asynchronously with lag metrics.

Separate ingestion SLOs from query SLOs and isolate their resource pools so a large sync does not make discovery unavailable.

### Measure quality with independent denominators

Measure schema validity, processing success, source lag, field freshness, unresolved references, conflicts, duplicates, orphans, missing owner/contact/docs, relation churn, and query/search latency/errors.

Coverage needs an independently derived denominator. If cloud/repository inventory identifies $N$ in-scope subjects and $M$ map uniquely to catalog entities, $C=M/N$. Catalog entity count divided by itself proves nothing.

Assess precision too: catalog entities that map to no current in-scope subject, duplicates, or incorrect relations. Sample and review mappings; automated matching can inflate coverage by false merges.

Measure user outcomes: time/correctness finding owner/API/runbook, search success, incident routing, reuse, decommission completion, and metadata repair burden. Mandatory registration can produce high coverage and low trust.

Segment by source, kind, lifecycle, business domain, and criticality. Publish data-quality ownership and remediation queues, not only dashboards.

### Test evolution and organizational change

Use fixtures for every entity version/source shape and golden stitched outputs. Test additive/removal/default/type/identity/relation changes, old processors, cached clients, and search migrations.

Simulate team rename/split/merge, repository transfer/rename/archive, system decomposition, API version migration, service acquisition/divestiture, and source-provider replacement. Preserve redirects, provenance, approvals, and dependent references.

Test full snapshot interruption, delta gap, webhook reorder/duplicate, source clock skew, conflicting sources, poison record, provider restart, processor upgrade, high fan-out, graph cycle, authorization change, and mass orphan prevention.

Schema migration includes validation of all stored/unprocessed/quarantined records. Do not tighten rules and strand entities invisibly.

Track consumer usage before retiring fields, kinds, types, relations, annotations, or APIs. Portal plugins and automation may depend on semantics not apparent from schema.

### Recover and retire catalog components

Classify catalog state as reconstructible versus non-derivable. Source descriptors and inventories can rebuild raw assertions if still available; manual annotations, conflict decisions, source cursors/tombstones, aliases, audit, and some relationship evidence may require backup.

On restore, freeze destructive cleanup, restore schemas/config/provider identities and non-derivable state, then reingest sources by revision. Compare restored assertions with sources and external reality; do not publish mass deletions from an incomplete first sync.

Reprocess/stitch deterministically and rebuild search/caches. Validate entity counts by provider, coverage sample, conflicts, orphans, permissions, relation integrity, and deep links before declaring recovery.

To retire a source/provider, inventory its bucket, co-owners, assertions, emitted children/relations, consumers, credentials, cursors, and tombstones. Transfer identities/provenance atomically or archive/delete by explicit disposition.

To retire the catalog, migrate discovery consumers and non-derivable decisions, preserve redirects/audit, disable writes/providers, verify zero use, revoke credentials, and only then remove databases, indexes, backups, and integrations. Runtime capability continuity must not depend on the catalog UI.

## Definitions and Notation

Let $E$ be canonical entities, $F_e$ fields/relations for entity $e$, and $S$ ingestion/authority sources. A candidate assertion is $a=(e,f,v,s,r,t,q)$ for entity, fact, value, source, source revision, source observation time, and quality evidence.

Let $A_{e,f}$ be the set of assertions for a fact and $R_f(A_{e,f})$ its field-specific resolution. $R_f$ must account for authority/ownership, validation, freshness, and conflict. It may return a value with provenance, `Unknown`, or `Conflict`; it need not force a single value.

For source $s$, let last successful authoritative observation be $t_s$, allowed fact staleness $\Delta_f$, and current time $t$. A fact is within its simple freshness bound when $t-t_s\leq\Delta_f$. Source-specific revisions remain stronger than clocks for ordering where available.

Let independent inventory $I$ contain $N=|I|$ in-scope subjects, $m:I\rightarrow E\cup\{\bot\}$ a reviewed identity mapping, and $M=|\{i\in I:m(i)\neq\bot\}|$. Coverage is $C=M/N$ for $N>0$. Precision and mapping correctness need separate evidence.

Let graph $G=(E,R)$ contain typed directed relations. Reachability in $G$ proves only catalog-path existence under those relation semantics, sources, and freshness—not runtime calls, readiness, authority, or deletion order unless explicitly modeled.

## Mechanisms, Invariants, or Proof Structure

### Catalog construction protocol

1. Define journeys, scope, kinds, non-goals, freshness needs, and independent coverage denominators.
2. Specify canonical identity, namespace, rename/recreation, aliases, and source keys.
3. Create per-field/relation authority, merge, validation, sensitivity, freshness, and conflict policies.
4. Register provider buckets with snapshot/delta/checkpoint/deletion and credential contracts.
5. Normalize, validate, resolve identity, quarantine collisions, and preserve raw provenance.
6. Process/enrich/derive with bounded versioned code; stitch deterministically and idempotently.
7. Serve authorization-filtered APIs, search, and graphs with freshness and quality evidence.
8. Reconcile orphans/tombstones and organizational/source changes through owned workflows.
9. Measure coverage, precision, validity, freshness, conflicts, usefulness, scale, and SLOs.
10. Test replay/restore/migration/retirement and rebuild derived views from authority.

### Single-authority-resolution invariant

Each fact has a documented authority or deterministic multi-source resolution. Arrival time, processor order, and database update time never silently decide ownership. Unresolvable equal-authority disagreement becomes explicit conflict.

### Identity invariant

Canonical identity is stable across presentation and ordinary source movement. Rename/merge/split/recreation produce explicit alias, mapping, successor, or new identity behavior; fuzzy matching cannot authorize automatic merge.

### Provenance/freshness invariant

Resolved facts preserve source revision and observation time. Reprocessing does not refresh the source clock. Consumers can distinguish current, stale, unknown, conflicted, and unauthorized.

### Safe-removal invariant

One failed or partial provider sync cannot mass-delete its bucket. Orphan or missing-source state precedes destructive catalog cleanup unless an authenticated complete snapshot/tombstone and policy justify removal.

### Coverage denominator argument

If completeness is estimated using only catalog entities, missing subjects are absent from both numerator and denominator and cannot reduce the score. Therefore an independent in-scope inventory or statistically sound sample is necessary to estimate coverage. This is a proof sketch of denominator necessity, not proof that a chosen inventory is complete.

### Executable assertion inventory

The following synthetic example resolves ten assertions by declared source ownership/freshness. It does not connect to a catalog, directory, repository, runtime, or authorization system.

<!-- bijux-verify: {"id":"catalog-assertion-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"resolved=5\nstale=2\nconflict=2\nunauthorized=1\n"}} -->
```python
assertions = [
    ("description", "repo", True, True),
    ("lifecycle", "repo", True, True),
    ("membership", "directory", True, True),
    ("deployment", "runtime", True, True),
    ("api", "repo", True, True),
    ("deployment", "runtime", False, True),
    ("oncall", "incident", False, True),
    ("owner", "repo", True, False),
    ("owner", "directory", True, False),
    ("classification", "repo", True, True, "denied"),
]

counts = {"resolved": 0, "stale": 0, "conflict": 0, "unauthorized": 0}
for assertion in assertions:
    _, _, fresh, agreement, *access = assertion
    if access and access[0] == "denied":
        counts["unauthorized"] += 1
    elif not fresh:
        counts["stale"] += 1
    elif not agreement:
        counts["conflict"] += 1
    else:
        counts["resolved"] += 1

for state in ("resolved", "stale", "conflict", "unauthorized"):
    print(f"{state}={counts[state]}")
```

The two owner assertions are modeled as conflicts rather than allowing arrival order to pick one. Authorization is evaluated before disclosure, and stale facts remain distinct from false values.

### Verification matrix

Test kind/version/schema fixtures; case/default namespace and reference normalization; provider duplicate/collision; full snapshot partial failure; delta gap/reorder/duplicate; clock skew; poison/oversized input; processor determinism/version skew; conflicting authorities; stale source; unresolved and cyclic/high-fan-out relations; source move/rename/split/merge; orphan/tombstone; entity/field/relation/search authorization; ingestion SSRF/content injection; query/graph bounds; coverage mapping; backup restore; provider retirement; and catalog replacement.

## Alternatives and Trade-Offs

### Repository descriptors versus automated inventory

Descriptors put domain intent near code and review but become stale/manual. Inventory is broad/current for machine facts but often lacks meaning. Combine per-field authority rather than selecting one universal source.

### Push/webhook versus polling

Push lowers latency but can lose, duplicate, or reorder. Polling reconciles completeness but costs and lags. Use authenticated deltas plus periodic full reconciliation where source supports both.

### Provider versus processor integration

Providers control remote scheduling, buckets, deltas, and deletion. Processors fit bounded validation/enrichment but run broadly. Choose by lifecycle and scale, not convenience.

### Strict schema versus extensible metadata

Strict fields support quality and consumers but slow novel use. Extensions enable discovery but create vocabulary and security debt. Govern prefixes and promote proven semantics.

### One global namespace versus bounded namespaces

Global names are simple but collide and centralize naming. Namespaces scale ownership but complicate references and are not automatic security. Define canonical resolution.

### Declared versus observed relations

Declared edges express design intent but drift. Observed edges show behavior but are sampled/noisy. Preserve both with distinct type, source, window, and confidence.

### Last-known-good versus remove on source failure

Retention supports discovery during outages but becomes stale. Immediate removal hides useful entities and can cause mass churn. Label staleness and choose fact-specific failure policy.

### Soft orphaning versus eager deletion

Soft orphaning enables diagnosis/reclaim but accumulates clutter. Eager deletion keeps catalog clean but magnifies ingestion defects. Use retention, notification, and authoritative tombstones.

### Central catalog versus federated domain catalogs

Central query/vocabulary aids discovery but can bottleneck ownership. Federation preserves domain autonomy but complicates identity, schema, search, and authorization. Federate sources behind shared contracts.

### Precomputed graph versus live joins

Precomputation gives fast bounded queries but lags. Live joins can be current but couple sources and scale poorly. Use stitched views with source freshness and authoritative deep links.

### Broad visibility versus least disclosure

Broad discovery promotes reuse and incident response but exposes sensitive systems/topology. Filter entities and fields by policy while publishing safe capability metadata deliberately.

### Rebuildable catalog versus backed-up database

Rebuild simplifies recovery for fully derived state but loses manual decisions, cursors, aliases, and audit. Classify and back up non-derivable state; test deterministic rebuild.

## Failure Modes and Misconceptions

1. **“The catalog is the source of truth.”** Authority is fact-specific and often external.
2. **“More entities mean better coverage.”** Noise and duplicates can rise while subjects remain missing.
3. **“Repository equals component.”** One repository can hold many components or vice versa.
4. **“Display title is identity.”** Titles change and collide.
5. **“Database UID is a stable external reference.”** Reingestion or migration can change storage identity.
6. **“Last writer wins resolves ownership.”** It lets timing override governance.
7. **“Provider owns the full entity.”** Different sources can own different facts.
8. **“Processors are general integration workers.”** broad repeated invocation makes remote polling expensive.
9. **“Webhooks guarantee freshness.”** Delivery can fail, duplicate, and reorder.
10. **“Catalog owner grants access.”** Accountability metadata is not runtime authorization.
11. **“Missing relation means no dependency.”** target/source/processing/authorization may be missing.
12. **“Declared dependency is runtime traffic.”** intent and observation have different semantics.
13. **“No search result means no entity.”** indexing, permission, and freshness affect results.
14. **“Updated today means observed today.”** reprocessing stale input changes catalog time only.
15. **“Orphan means safe to delete.”** source move or processor failure may be the cause.
16. **“Empty full sync means delete all.”** incomplete/failing enumeration can look empty.
17. **“Tags are harmless.”** consumers may turn uncontrolled strings into policy accidentally.
18. **“The graph should contain every runtime object.”** that destroys the useful mental model and scale.
19. **“Backup is unnecessary because sources exist.”** manual decisions, cursors, aliases, and audit may not.
20. **“Stopping a provider retires it.”** its bucket, relations, consumers, credentials, and recovery remain.

## Worked Examples

### Example 1

**Situation.** Repository YAML and identity directory name different owners.

**Reasoning.** Preserve both assertions/provenance; apply field policy. If repository selects team and directory says it is inactive, emit unresolved/conflict and notify rather than overwrite.

**Conclusion.** Disagreement is catalog data, not a race to hide.

### Example 2

**Situation.** Two providers emit `Component:default/payments`.

**Reasoning.** Provider bucket collision is quarantined. Operators decide canonical namespace/source or model distinct entities; timestamps do not choose.

**Conclusion.** Identity ownership precedes stitching.

### Example 3

**Situation.** A full cloud inventory fails after page one and omits 90% of records.

**Reasoning.** Do not commit snapshot removal until enumeration completes coherently. Retain old assertions stale and retry from safe checkpoint/full sweep.

**Conclusion.** Partial snapshot failure must not mass-delete.

### Example 4

**Situation.** A processor calls the incident API once for each of 100,000 entities.

**Reasoning.** Move to a scheduled/delta provider or bulk cache keyed by entity; bound requests and let processing join local facts.

**Conclusion.** Integration placement determines scale and blast radius.

### Example 5

**Situation.** Runtime telemetry observes a call absent from declared dependencies.

**Reasoning.** Publish a distinct observed relation with time window/confidence; do not overwrite declared architecture. Investigation may update intent.

**Conclusion.** Preserve declared and observed epistemology.

### Example 6

**Situation.** A sensitive internal system appears in search autocomplete to an unauthorized user.

**Reasoning.** Authorization must filter before indexing/query aggregation/disclosure; hiding the result page is too late. Audit access tests.

**Conclusion.** Metadata existence is protected information.

### Example 7

**Situation.** A repository is renamed and its old catalog entity becomes orphaned.

**Reasoning.** Match stable source identity, migrate canonical name with alias/redirect and relations, or explicitly create successor. Do not delete/recreate blindly.

**Conclusion.** Source movement is an identity migration.

### Example 8

**Situation.** Catalog shows 10,000 entities and claims 100% coverage.

**Reasoning.** Independent repository/runtime inventory has 12,000 in-scope subjects; 9,600 map uniquely, so measured coverage is 80%, before precision sampling.

**Conclusion.** Completeness needs an external denominator.

### Example 9

**Situation.** Restored catalog is one day old while sources continued changing.

**Reasoning.** Freeze deletions, restore provider IDs/cursors and decisions, reenumerate by revision, reconcile conflicts/orphans, restitch, rebuild search, and validate permissions/coverage.

**Conclusion.** Recovery is controlled reingestion, not merely database startup.

### Example 10

**Situation.** An acquired business uses the same component names and different lifecycle terms.

**Reasoning.** Introduce bounded namespaces/source keys, map vocabulary through reviewed migration, detect collisions, preserve aliases/provenance, and update consumers gradually.

**Conclusion.** Organizational integration is schema and identity evolution.

## Cross-Program Connections

1. **Data Engineering:** ingestion, schemas, lineage, quality, checkpoints, materialized views, and backfills directly shape catalogs.
2. **Database Systems:** identity, constraints, transactions, indexes, temporal facts, migration, and restore govern catalog state.
3. **Distributed Systems:** eventual consistency, duplicate/reordered delivery, partitions, idempotency, and reconciliation govern sources.
4. **Graph Engineering:** typed edges, reachability, cycles, fan-out, traversal limits, and graph quality shape relationships.
5. **Domain-Driven Design:** bounded contexts, ubiquitous language, entities, systems, and domains define the model.
6. **Security Engineering:** least disclosure, source authentication, SSRF/content safety, authorization, credentials, and audit protect metadata.
7. **API & Service Engineering:** versioned schemas, references, pagination, filtering, errors, and deprecation define consumption.
8. **Reliability Engineering:** freshness SLOs, backpressure, bulkheads, source failure, observability, and recovery protect usefulness.
9. **Organizational Design:** team identity, accountability, ownership transfer, acquisitions, splits, and escalation shape metadata.
10. **Product Management:** user journeys, discovery success, trust, coverage denominators, and repair burden measure value.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Backstage. [Software Catalog](https://backstage.io/docs/features/software-catalog/). Retrieved 2026-09-02.
3. Backstage. [The Life of an Entity](https://backstage.io/docs/features/software-catalog/life-of-an-entity/). Retrieved 2026-09-02.
4. Backstage. [System Model](https://backstage.io/docs/features/software-catalog/system-model/). Retrieved 2026-09-02.
5. Backstage. [Descriptor Format of Catalog Entities](https://backstage.io/docs/features/software-catalog/descriptor-format/). Retrieved 2026-09-02.
6. Backstage. [Entity References](https://backstage.io/docs/features/software-catalog/references/). Retrieved 2026-09-02.
7. Backstage. [Creating the Catalog Graph](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/). Retrieved 2026-09-02.
8. Backstage. [External Integrations](https://backstage.io/docs/features/software-catalog/external-integrations/). Retrieved 2026-09-02.
9. Backstage. [Custom Processors](https://backstage.io/docs/next/features/software-catalog/external-integrations/processors/). Retrieved 2026-09-02.
10. Backstage. [Extending the Model](https://backstage.io/docs/features/software-catalog/extending-the-model/). Retrieved 2026-09-02.
11. Backstage. [Catalog Audit Events](https://backstage.io/docs/features/software-catalog/audit-events/). Retrieved 2026-09-02.
12. Backstage. [Permission Framework Overview](https://backstage.io/docs/permissions/overview/). Retrieved 2026-09-02.
13. Kubernetes. [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). Retrieved 2026-09-02.
14. Kubernetes. [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define a catalog model for components, APIs, resources, systems, domains, groups, and users. Specify canonical identity, namespaces, kind/type vocabulary, lifecycle, relations, and non-goals.

### Exercise 2

Build a field/relation authority and conflict matrix for repository descriptors, identity directory, runtime inventory, cloud provider, incident system, and manual annotations.

### Exercise 3

Design ingestion of 2 million records using full snapshots, deltas, webhooks, pagination, providers, processors, checkpoints, duplicates, removals, poison records, and backpressure.

### Exercise 4

Define quality/security verification for coverage, precision, freshness, conflicts, orphans, ownership, relation graphs, search authorization, content safety, and organizational rename/merge.

### Exercise 5

Design recovery from a 36-hour-old catalog backup and later retirement of one provider and one entity kind while sources, consumers, aliases, relations, and audit remain active.

## Answers to the Exercises

### Answer 1

Use canonical `kind:namespace/name` with normalized case and fully qualified stored references. Components are deployable/owned software units, APIs are published contracts, resources are significant supporting capabilities, systems encapsulate collaborating components/resources/APIs, domains group systems by business bounded context, and groups/users mirror current organizational identity. Types refine kinds through governed registries; lifecycle uses a small controlled vocabulary such as experimental, production, deprecated, and retired with defined semantics.

Repository path and display title are attributes, not identity. Maintain stable source keys, aliases/tombstones, and explicit rename/merge/split behavior. Relations include ownedBy, partOf, provides/consumesApi, and declared/observed dependency as distinct types with provenance.

Non-goals include every Pod/cloud object, runtime authorization, secrets, high-volume telemetry, deployment configuration, or automated deletion from catalog absence. The catalog optimizes discovery, navigation, accountability, reuse, and metadata-quality journeys.

### Answer 2

Repository owns description, source/document links, declared component/API/system/lifecycle, and intended owner reference. The identity directory owns group/user existence, membership, active state, canonical contacts, and aliases. Runtime inventory owns current deployment observations; cloud provider owns provider object existence/IDs/observed region; incident system owns current on-call/escalation; manual annotations own only approved extension keys with editor/reason/expiry.

For each assertion store source object/revision/observed time/provider/transform version. Repository owner reference is resolved through directory; inactive/missing target becomes unresolved, not a replacement. Runtime cannot overwrite declared lifecycle. Equal-authority disagreement emits conflict. Manual data cannot override protected fields. Stale facts retain last-known values only by fact policy.

Relations preserve producer and declared versus observed semantics. Source priority is explicit; arrival and processing time never decide. Conflicts route to accountable remediation with audit and no destructive automation.

### Answer 3

Partition entity providers by source/tenant and stable bucket. For sources with consistent snapshot tokens, stream pages into a staged generation, validate/deduplicate by source ID/revision, checkpoint resumable cursor, and atomically publish additions/updates/removals only after a complete snapshot. An interrupted enumeration never deletes unseen tail records.

Apply authenticated ordered deltas/webhooks by source revision into an inbox; deduplicate event ID/source key, detect gaps, and schedule reconciliation. Periodic full snapshots repair missed events. Use incremental providers for pagination/scheduling/removal ownership. Processors only normalize, validate, locally enrich, and derive bounded relations; remote bulk data arrives through providers/caches.

Quarantine poison/oversized/colliding records with bounded payload evidence and owner. Enforce per-provider entity/byte/relation quotas, queue coalescing, rate limits, backoff/jitter, circuit breakers, and independent worker pools. Stitch incrementally, index asynchronously, and expose source lag/backlog/invalid/conflict/removal metrics. Load-test worst-case fan-out and restore/replay from checkpoints.

### Answer 4

Construct independent in-scope inventories per domain and map them to canonical identities. Report coverage $M/N$, unmapped subjects, catalog-only entities, duplicates, and sampled mapping precision. Measure validity, source observation freshness by fact, processing lag, conflict/unresolved/orphan rates, missing active owner/contact/docs, relation churn, and time to repair.

Test entity/reference normalization, collisions, aliases, schema versions, declared/observed edges, missing targets, cycles, and graph depth/fan-out budgets. Compare owner references with active directory identities and incident-routing exercises; never turn catalog owner directly into access.

Test unauthorized entity/field/relation/search/autocomplete/count queries, ingestion SSRF/redirect/oversize, malicious Markdown/links/annotations, export injection, provider credential scope, and audit. Simulate team/service/repository rename, split, merge, acquisition namespaces, stale sources, partial snapshots, and processor upgrades. Validate user outcomes by finding correct owner/API/runbook, not dashboard greenness alone.

### Answer 5

Freeze deletion/orphan cleanup and provider cursors. Restore schemas, provider identities/config, field policies, manual decisions, aliases/tombstones, audit, and keys. Reenumerate each authority using source revisions, retaining restored assertions as stale until a complete source sync. Detect external-ahead renames/removals/conflicts rather than overwriting by time. Reprocess and stitch with pinned compatible versions, then rebuild search/caches.

Validate counts per provider bucket, independent coverage/precision sample, ownership resolution, conflicts/orphans, permissions, graph integrity, deep links, and source freshness. Renew backup after reconciliation.

To retire a provider, stop new schema use, inventory bucket/assertions/children/relations/cursors/credentials/consumers, migrate source ownership and provenance to a successor with collision preview, or archive/delete through explicit entity disposition. Measure zero provider-specific dependencies, then revoke credentials and remove code/config/recovery artifacts.

To retire a kind, migrate entities/references/search/UI/automation, preserve aliases or successor relations, measure client/query use, and keep old decoders for retained events/backups until safe. Catalog deletion must not delete runtime effects. Record every unresolved entity and audit obligation before final removal.
