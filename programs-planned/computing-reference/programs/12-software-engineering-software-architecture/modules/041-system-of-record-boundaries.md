---
module_id: SARCH-041
program: Software Engineering: Software Architecture
level: 1
module_number: 41
title: System-of-Record Boundaries
status: complete
last_verified: 2026-09-06
---

# System-of-Record Boundaries

## One-Page Review

### Governing question

Where should authority for accepting, correcting, versioning, retaining, and publishing consequential state reside when many systems store, transform, cache, or display related data?

### Essential definitions

- A **system of record (SoR)** is the authorized decision boundary for specified facts or state transitions within a declared scope and time; it is not necessarily the only physical copy.
- **Write authority** is permission and accountability to accept a state transition. Physical write access without that mandate is an architectural defect, not authority.
- A **fact** is a scoped assertion; **state** is the current accepted representation under a model; an **event** records that something occurred under an authority.
- A **system of entry** captures intent or observations; it may submit commands without owning the accepted result.
- A **projection** is a derived consumer-oriented representation whose meaning depends on sources, transformation, version, and freshness.
- **Provenance** records origins, responsible agents, and transformations needed to assess a claim.
- **valid time** says when a fact applies in the domain; **transaction time** says when a system recorded it.
- A **correction** supersedes or qualifies a prior assertion while preserving required history; it is not necessarily destructive overwrite.
- An **authority transfer** is a controlled change in which boundary may accept specified writes.
- **reconciliation** compares representations or outcomes and applies a declared rule to explain or repair divergence.

### Central model, mechanism, or theorem

Assign authority at fact-and-operation granularity:

$$
Authority(f,o,p,j,t)=s,
$$

where fact family $f$, operation $o$, population $p$, jurisdiction $j$, and effective interval $t$ resolve to one accountable system boundary $s$. Other copies carry source identity, version or event position, observed time, freshness, and derivation.

For optimistic update of entity $x$, command with expected version $v$ is accepted only when current version equals $v$ and all invariants hold; the commit produces $v+1$ and one authoritative outcome. A retry uses stable operation identity. These mechanisms prevent lost updates only within their declared scope; cross-system invariants require colocated authority or an explicit coordination and recovery protocol.

### Critical invariants

- scope authority by fact, operation, population, jurisdiction, lifecycle, and time rather than labeling an entire product “the truth”;
- give each accepted transition one accountable decision boundary at a time;
- distinguish system of entry, system of record, preserved legal record, replica, cache, projection, archive, and analytical output;
- route writes through commands that enforce identity, authorization, preconditions, invariants, idempotency, and audit;
- prohibit consumers from depending on or mutating private SoR storage;
- attach provenance, version, valid time, transaction time, and freshness to consequential copies;
- preserve correction, dispute, deletion, retention, and legal-hold semantics across replicas and derived data;
- define behavior for stale, unavailable, partitioned, conflicting, and unknown state;
- publish changes with explicit atomicity or reconciliation between local commit and notification;
- make backup, restore, failover, and disaster recovery preserve logical authority rather than create competing writers;
- transfer authority through a versioned cutover with one write owner, reconciliation, rollback, and retirement;
- observe accepted commands and domain outcomes, not merely database writes or message delivery.

### Common failures

Common failures include calling a warehouse the universal source of truth; treating the most complete copy as authoritative; assigning authority per application instead of per fact; allowing several writers during migration; equating database primary with business identity; exposing tables as public contracts; making caches decide writes; losing source versions in projections; using wall-clock “latest wins” without clock and authority rules; publishing events before commit or losing them after commit; restoring an old backup as a second master; overwriting disputed history; forgetting derived copies during deletion; and assuming an SoR designation proves accuracy, legality, availability, or security.

### Compact example

A mobile app captures an address-change request offline. It is the entry boundary, not the address authority. On reconnect, it sends stable operation ID, customer identity, proposed address, evidence, and expected profile version. The profile service authenticates, authorizes, validates, checks concurrency, and either commits version 18 or returns a conflict. An outbox publishes the accepted change; search and analytics update projections carrying version and provenance. The app never declares success merely because it stored the request locally.

### Connections

[SARCH-026](026-data-and-information-views.md) supplies semantic and lifecycle views; [SARCH-035](035-event-driven-architecture.md) supplies publication and delivery reasoning; [SARCH-038](038-service-oriented-architecture.md) and [SARCH-039](039-microservices-architecture.md) supply service authority. [SARCH-042](../ROADMAP.md) next compares shared databases with database-per-service authority. Data Architecture develops record, engagement, insight, master-data, and governance concerns in depth.

## Governing Question

Real systems rarely have one database containing one uncontested truth. A customer profile exists in operational services, mobile caches, search indexes, support tools, warehouses, backups, events, partner systems, and documents. Some values are observations; some are accepted decisions; some are estimates; some apply only within one jurisdiction or interval.

The architectural problem is not eliminating every copy. It is making authority unambiguous: which boundary may accept which transition, under what rules, and how every other representation obtains, qualifies, corrects, and retires its copy. Without that boundary, partial failure and organizational change create competing masters precisely when correctness matters most.

## Why This Matters

Authority controls invariants, concurrency, audit, privacy, recovery, and evolution. If two services can change an account balance independently, no interface diagram can guarantee consistency. If an analytical projection silently becomes an operational write path, model or pipeline changes become policy changes. If a migration leaves dual writers, reconciliation becomes permanent business risk.

Clear SoR boundaries enable specialized copies. Search can denormalize, analytics can retain history, mobile clients can operate offline, and caches can reduce latency because each representation states its authority and freshness. Teams can replace storage or deployment without changing consumer meaning.

The designation has limits. An authoritative system can contain an incorrect fact supplied by a user or sensor. It can be unavailable, insecure, or noncompliant. A separate archive may hold legally preserved evidence. Architecture must avoid turning “system of record” into an unsupported guarantee.

## Prerequisites and Retrieval

Retrieve fact, assertion, state, event, command, query, identity, authority, invariant, transaction, concurrency, version, idempotency, provenance, lineage, valid time, transaction time, replica, cache, projection, consistency, freshness, partition, correction, reconciliation, audit, retention, deletion, backup, recovery, migration, cutover, and rollback.

From SARCH-017 retrieve semantic interoperability; SARCH-018 provides observability; SARCH-026 provides data views; SARCH-032 provides module and write boundaries; SARCH-035 provides event authority and transactional publication; SARCH-036 provides remote ambiguity; and SARCH-038 through SARCH-040 provide services, deployment boundaries, and force-based selection.

## Learning Objectives

After completing this module, you should be able to:

1. define a system of record at fact, operation, population, jurisdiction, and time granularity;
2. distinguish authority from physical storage, entry, engagement, insight, preservation, replication, and caching;
3. place commands, invariants, concurrency checks, transactions, and idempotency at an authority boundary;
4. design queries, projections, events, and replicas with provenance and freshness;
5. reason about cross-boundary invariants, unknown outcomes, and reconciliation;
6. model valid time, transaction time, correction, dispute, and historical reconstruction;
7. preserve security, privacy, retention, deletion, and audit across copies;
8. design backup, restore, failover, and disconnected operation without competing writers;
9. transfer authority incrementally with explicit cutover and rollback;
10. test and observe authority using business outcomes rather than storage activity alone.

## Core Exposition

**Scope authority before naming a system.** “CRM is the source of truth” is too broad. One platform may govern contact preference, another legal identity, another credit decision, and an order service the shipping address captured for a particular order. Authority can differ by country, customer population, operation, and valid interval.

Write an authority statement as a tuple: fact family, allowed operations, population, jurisdiction, lifecycle states, effective time, owner, and system boundary. This makes overlaps and gaps testable. A product name is then an implementation of one or more authority assignments, not a universal label.

**Prefer “authoritative for” to “true.”** A system of record accepts the organization's official state transition under a defined policy. The accepted value can still be wrong in the real world. A mistyped address remains the current accepted address until correction. A sensor reading carries calibration and uncertainty. An identity match may remain disputed.

Avoid the phrase “single source of truth” unless its exact scope is stated. Logical single write authority can coexist with replicas, histories, legal records, and purpose-specific views. The goal is not one physical copy; it is one unambiguous acceptance rule at a given scope and time.

**Distinguish the roles around authority.** A system of entry captures intent or observation. A system of engagement presents workflow. A system of insight derives measures or recommendations. An archive preserves evidence. A projection serves a read purpose. Any one product can play several roles for different facts.

Do not infer authority from proximity to a user or completeness of a dataset. A mobile app can capture an offline command without being allowed to decide it. A warehouse may contain more columns and history than an operational service while remaining nonauthoritative for operational writes. Data Architecture examines record, engagement, and insight roles more broadly in DARCH-004.

**Place domain invariants with write authority.** The authority validates identity, authorization, preconditions, state transitions, and invariants before commit. Consumers request outcomes rather than manipulating private tables. If every caller reimplements eligibility or balance rules, authority exists only nominally.

Atomic invariants should live within one transactional boundary where feasible. If credit limit and balance must be checked together for every charge, splitting them across independent writers creates coordination or inconsistency. Redraw the boundary or specify a reservation, escrow, consensus, or workflow mechanism whose assumptions meet the consequence.

**Use commands for intent.** A command says what outcome a caller requests and targets the authority that can decide it. Include principal, target identity, operation identity, parameters, expected version or precondition, and context required by policy. The response distinguishes committed, rejected, conflict, invalid, unavailable, and unknown.

A system of entry must not convert local persistence into authoritative success. It records `pending` until the authority supplies a terminal outcome. User experience can remain responsive by showing local intent and reconciliation state honestly.

**Separate operation identity from entity version.** A stable operation ID deduplicates or retrieves one requested effect. An entity version detects whether state changed since observation. They answer different questions. Retrying operation `op-91` against profile version 17 can return its prior result; submitting a new operation with expected version 17 can conflict after someone commits version 18.

Version checks prevent lost updates only when every relevant writer uses the same authority and comparison. A database row version cannot protect a second system that writes independently. Define request fingerprint, identity scope, retention, and outcome storage for idempotency.

**Expose queries without transferring authority.** Consumers can query the SoR directly through a contract or use replicas and projections. A response needs semantics, version or event position, observation time, and freshness when consequential. The consumer decides whether that evidence is adequate for its purpose.

Read APIs should avoid leaking storage schemas. A stable capability query can survive normalization, sharding, archival, or product replacement. Bulk and streaming access can be separate contracts with privacy and capacity limits.

**Build projections as derived products.** Search indexes, caches, materialized views, mobile stores, warehouses, and feature datasets transform authoritative changes for a purpose. Record source identities, input positions, transformation version, build time, completeness, and correction behavior. A projection can be internally authoritative for its own computed artifact while not owning source facts.

Kleppmann distinguishes systems of record from derived data systems and explains why derived data can be rebuilt from authoritative sources when transformations and logs are retained [1]. Rebuildability is a design goal, not an automatic property. External enrichment, nondeterministic code, expired source data, or missing versions can make exact reconstruction impossible.

**Define freshness rather than saying synchronized.** Let authoritative commit time be $t_c$ and projection observation time be $t_r$ under a compatible clock model; observed lag is $\Delta=t_r-t_c$. Consumers need a maximum-age or version policy, not a promise that all copies are “real time.” Clock skew can make wall-time subtraction misleading; event positions or source versions may be stronger.

Freshness is purpose-specific. A product description can tolerate minutes; a revocation or dosage limit may require direct authority or a tightly bounded safety cache. When authority is unavailable, choose fail closed, safe stale use, queued intent, degraded operation, or manual procedure based on consequence.

**Publish accepted changes atomically enough.** If a service commits state and then publishes an event, a crash between steps can lose notification. If it publishes first and then rolls back, consumers can observe a fact that never became authoritative. A transactional outbox records state and pending publication in one local transaction; a relay publishes and retries.

At-least-once delivery creates duplicates; consumers use event identity and idempotent projection updates. The outbox supports local atomicity and recoverable publication, not exactly-once business processing across the world. Consumers still handle delay, reordering, schema evolution, and poison messages.

**Make events authoritative assertions.** An event names the authority, entity, fact, version, occurrence and record times, schema, and meaning. `CustomerChanged` without which attributes, authority, or version forces consumers to query private state or guess. Prefer domain facts such as `ContactPreferenceAccepted` when that semantic precision is durable.

Not every database change deserves an external event. Internal storage updates can be implementation details. Publish facts consumers legitimately depend on, with an owner and compatibility policy.

**Treat history as more than current state.** Current value, valid-time history, transaction-time history, audit evidence, and event history serve different purposes. Valid time answers when a fact applied in the domain. Transaction time answers when a recording system knew or stored it. Bitemporal models preserve both [2].

A correction entered today may state that an address was valid starting last month. Overwriting the old row destroys the ability to reconstruct what the system believed yesterday. Preserve supersession, reason, actor, and policy where consequence requires it.

**Model dispute and uncertainty.** Some assertions cannot be collapsed immediately. Two agencies can provide conflicting birth dates; two sensors can disagree; a customer can dispute a charge. The SoR may be authoritative for case status and accepted resolution while retaining competing source assertions.

“Latest wins” is not a universal conflict rule. Wall clocks can skew, late messages can carry older valid time, and a later writer may have weaker authority. Resolve by domain authority, version, evidence, merge policy, or human adjudication. Preserve provenance.

**Respect external authorities.** A product may consume facts governed by a bank, government registry, supplier, or device. A local cache cannot become the external authority. Record the external identifier, contract, retrieval time, evidence, expiry, correction, and unavailable behavior.

Sometimes an organization deliberately adopts an external fact into a local decision. For example, a licensing service may record “validated license as of time T” and own the local permission decision. Distinguish imported assertion from local decision so later external correction can be reconciled.

**Secure the write boundary.** Authenticate principals and workloads, authorize every operation, enforce separation of duties where required, validate inputs, and audit decisions. Database network access is not a substitute for domain authorization. Give projections read-only, scoped feeds rather than general credentials.

Protect integrity and confidentiality in transit, storage, logs, events, backups, and derived copies. Minimize attributes. A service that publishes an entire customer record for one status bit expands privacy and breach risk.

**Propagate retention and deletion semantics.** The SoR owns or coordinates lifecycle rules for authoritative facts, but copies have their own media and legal obligations. Define retention clock, deletion trigger, legal hold, tombstone, backup expiry, projection cleanup, and proof of completion. Immediate physical erasure may conflict with immutable audit or statutory preservation; the responsible authorities must decide.

Derived data can retain sensitive information even after source columns disappear. Feature vectors, aggregates, logs, search indexes, and exports need lineage sufficient to determine applicability. Do not promise deletion across unknown copies.

W3C PROV-O provides a standard vocabulary for entities, activities, and agents involved in provenance [3]. It can support representation, but a vocabulary does not capture evidence automatically or decide retention policy.

**Design replication without multiplying authority.** Replicas can serve reads and survive failure. One logical authority may use consensus or primary election internally so only an eligible leader accepts writes for a term. That is one distributed SoR boundary, not several independent masters, when fencing and consistency rules hold.

Multi-primary designs can be valid for commutative or mergeable operations, partitioned ownership, or explicitly resolved conflicts. State the mathematical or domain merge rules. Calling every replica authoritative without convergence and conflict semantics hides the real decision.

**Plan failover and fencing.** After a leader fails, an old process may still be alive but disconnected. If both old and new leaders accept writes, split brain creates competing history. Use leases only with their clock and pause assumptions, or use consensus terms, fencing tokens, and storage enforcement. Clients must reject stale authority where possible.

Failover changes endpoint, not logical ownership. Record term, version, and operation identity across retries. Test partitions and delayed old writers, not only clean process termination.

**Treat backup restore as authority recovery.** Restoring bytes does not automatically restore a correct SoR. The backup has a capture position; logs may need replay; projections may be ahead; messages may be redelivered; external effects may have occurred. Reconcile from the recovery point to current authoritative outcomes.

Never expose a restored copy as a second writer while the original can return. Fence credentials and endpoints, establish the authoritative term, validate invariants, and communicate lost or unknown intervals. Recovery point and recovery time objectives do not prove business reconciliation.

**Design disconnected operation explicitly.** A field device or mobile client may need to work without the central authority. Classify operations. Some can be queued as intent; some can reserve a partitioned budget; some can be commutative and merged; some must be prohibited or use a local safety authority.

On reconnect, submit stable identities, source versions, valid times, and evidence. The central authority accepts, rejects, or routes conflicts. A local “success” label must mean local acceptance only unless authority was delegated.

**Avoid hidden write paths.** Data repair scripts, administrative consoles, ETL jobs, support tools, triggers, and vendor batch loaders often bypass service contracts. Inventory every writer at database, file, topic, and external API boundaries. Either route it through the authority or govern it as a privileged command path with equivalent validation and audit.

Read-only access can also couple consumers to schemas and load. Use replicas or governed views when direct analytical queries threaten operational capacity. Track consumers so fields can evolve and stores can be retired.

**Move authority through a protocol.** Migration has a source authority, target authority, mapping, backfill, change capture, verification, cutover criterion, rollback window, and retirement. At every moment, exactly one boundary accepts each scoped write unless a proven multi-writer protocol applies.

Dual writes from application code are vulnerable to partial failure and ordering differences. Prefer one authoritative commit plus a durable change log, or a controlled write router during cutover. Shadow the target, compare outcomes, and repair discrepancies before authority transfer.

**Make the cutover observable.** Record an authority epoch or effective time. Reject stale writes aimed at the old owner after cutover. Consumers learn the new contract through routing or explicit version migration. The old system becomes read-only for a bounded reconciliation period, then is archived or retired under policy.

Rollback after target writes is not just reversing traffic. Either the old system can ingest new authoritative changes, or rollback means restoring the target implementation while retaining its authority. Define this before cutover.

**Model cross-system invariants honestly.** A rule spanning two SoRs cannot be enforced by each independently without a protocol. Options include moving the invariant into one authority, reserving rights, serializing through a coordinator, using distributed transactions, accepting temporary violation with compensation, or redesigning the rule.

Choose based on consequence, latency, availability, participants, and failure model. A nightly reconciliation is not suitable for a hard safety invariant. A globally synchronous transaction may be excessive for an analytical count.

**Observe domain transitions.** Database metrics show storage behavior; message counters show transport. Record command identity, principal, precondition, authority epoch, prior and new version, decision, commit, publication, projection application, reconciliation, and user-visible outcome. Protect sensitive audit data and use append-only integrity where required.

Measure rejected conflicts, duplicate commands, unknown outcomes, projection lag, reconciliation drift, unauthorized write attempts, stale readers, cutover discrepancies, and restoration gaps. A zero-drift dashboard can reflect a broken comparison job, so monitor evidence pipelines too.

**Test authority, not just CRUD.** Tests cover valid and invalid transitions, authorization, concurrent updates, retries before and after commit, lost response, publication crash windows, duplicate and reordered events, projection rebuild, stale reads, partitions, leader fencing, backup restore, correction, deletion, legal hold, migration, rollback, and retirement.

Use an independent model or ledger for critical reconciliation. Verify that no alternate credentials can mutate private stores. Test consumers against contract versions rather than one shared database snapshot.

**Govern the boundary.** Assign domain owner, technical owner, data steward where needed, security and privacy authorities, operations, consumers, and migration owner. Document service, facts, writers, contracts, versions, SLOs, retention, and incident process in a discoverable catalog.

Govern exceptions. Emergency repair may need a break-glass path with approval, bounded credentials, validation, audit, review, and replay into the authoritative history. An undocumented SQL update is not acceptable merely because it was urgent.

**Know the limits of the term.** SoR does not imply a relational database, event sourcing, one service, one region, or one vendor. It does not guarantee correctness, legal admissibility, durability, security, availability, or freshness. Those are separate claims with separate mechanisms and evidence.

Use the term only when it clarifies decision rights. If facts remain contested, federated, or jointly governed, model those realities instead of forcing a fictional master.

## Definitions and Notation

Let fact families be $F$, operations $O$, populations $P$, jurisdictions $J$, time intervals $T$, and system boundaries $S$. Authority assignment is a partial function

$$
Auth:F\times O\times P\times J\times T\rightarrow S.
$$

It is partial because some combinations are invalid or unresolved. For any valid point in scope, one value names the accountable acceptance boundary unless a separately specified joint or multi-writer protocol applies.

For entity $x$, authoritative version $v(x)$ increases monotonically under its scope. Command $c$ carries operation identity $id(c)$ and optionally expected version $ev(c)$. Optimistic acceptance requires $ev(c)=v(x)$, authorization, and invariants; the commit records outcome and next version.

Projection $r$ records source authority $s(r)$, source position or version $pos(r)$, transformation version $tr(r)$, observation time $obs(r)$, and purpose. If compatible clocks exist, lag from authoritative commit $t_c$ to projection observation $t_r$ is $\Delta=t_r-t_c$. Otherwise compare logical positions or bound lag through another measured protocol.

Authority epoch $e$ identifies a cutover generation. A writer authorized under epoch $e-1$ is fenced after epoch $e$ becomes effective. Fencing must be enforced at the write resource or another nonbypassable boundary.

## Mechanisms, Invariants, or Proof Structure

**Scoped-authority invariant.** For every accepted transition, fact, operation, population, jurisdiction, and effective time resolve to one accountable authority or a declared multi-writer protocol. Product-wide “truth” labels cannot substitute.

**Write-path invariant.** Every writer passes identity, authorization, precondition, invariant, idempotency, commit, and audit controls. Administrative and migration paths are included.

**Version argument.** If all writers compare expected version with the current authoritative version atomically, two commands based on the same version cannot both commit as its immediate successor. One changes the version; the other observes conflict. This does not protect uncoordinated external writers.

**Publication invariant.** A committed change and its obligation to publish are recorded atomically or reconciled by a declared recovery protocol. Delivery and projection application remain separately idempotent.

**Copy invariant.** Every consequential nonauthoritative copy exposes origin, source position or version, transformation, observation time, freshness, and correction semantics appropriate to use.

**Temporal invariant.** Corrections distinguish when a fact applies from when it was recorded and preserve required prior assertions. Later transaction time does not automatically mean later valid time or stronger authority.

**Recovery invariant.** Failover or restore establishes one current authority epoch and fences stale writers before accepting new commands. Bytes restored without business reconciliation do not prove current authority.

**Migration invariant.** Each scoped fact has one write authority throughout cutover; shadow copies and comparisons do not accept independent decisions. Rollback accounts for changes accepted after cutover.

**Lifecycle invariant.** Retention, deletion, legal hold, correction, and retirement propagate to known replicas, projections, logs, exports, and backups under explicit policy and evidence.

**Evidence invariant.** A successful database write, cache hit, message acknowledgment, replica health signal, or reconciliation count supports only its observed layer. None alone proves a correct domain outcome.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Direct authoritative query | current decision at the owner; simple provenance | availability and latency coupling; load | consequence requires current authority |
| Read replica | scalable reads and familiar query model | lag, failover ambiguity, schema coupling | bounded-stale operational reads under governed schema |
| Consumer projection | purpose-specific shape, isolation, offline use | lag, duplicate handling, rebuild and lineage | consumers can state freshness and derivation |
| Shared writable database | local-style joins and transactions | ambiguous ownership, release coupling, bypass | one authority and deployment genuinely own the schema |
| Service-owned write boundary | clear invariants, policy, audit, evolution | remote interaction and availability dependency | ownership crosses process or team boundaries |
| Snapshot synchronization | simple bulk transfer and recovery baseline | staleness, large comparisons, missed interim history | periodic state is sufficient |
| Change/event feed | incremental low-lag projections and audit | ordering, duplicates, schemas, retention | consumers can process and reconcile changes |
| Single logical leader | simple ordered writes and conflict model | leader availability and failover | operations are not safely mergeable |
| Partitioned authority | scale and offline locality | routing, movement, cross-partition invariants | facts partition cleanly by stable key or rights |
| Multi-writer merge | disconnected availability | conflict semantics and convergence proof | operations commute or domain merge is explicit |
| Destructive overwrite | simple current state | lost evidence and poor correction | prior state has no required consequence |
| Bitemporal history | reconstruct valid and recorded beliefs | schema, query, storage, correction complexity | retroactive facts and audit matter |

## Failure Modes and Misconceptions

1. **“The SoR is the database with the most data.”** Completeness does not grant decision authority.
2. **“One enterprise source of truth is always desirable.”** Authority is scoped; one universal model can erase legitimate differences.
3. **“Authoritative means accurate.”** It means authorized acceptance under policy, not correspondence to reality.
4. **“The primary database is the business authority.”** Primaries are replication roles; business authority requires ownership and rules.
5. **“A system of entry owns what it captures.”** It may only submit intent for later acceptance.
6. **“Replicas are synchronized.”** Freshness, position, conflict, and unavailable behavior must be measured.
7. **“Newest timestamp wins.”** Clock, valid time, transaction time, and authority may disagree.
8. **“Events are automatically the source of truth.”** Publisher authority, commit, semantics, retention, and correction must be defined.
9. **“An outbox gives exactly-once business effects.”** It closes one local publication gap; consumers still face duplicates and outcomes.
10. **“Optimistic versions solve distributed concurrency.”** They work only at one atomic authority boundary.
11. **“A restored backup can immediately become primary.”** Replay, fencing, external effects, and reconciliation remain.
12. **“Dual writes are a safe migration bridge.”** Partial failure creates divergence without a coordination protocol.
13. **“Soft deletion satisfies every retention rule.”** Legal, privacy, backup, and derived-copy duties differ.
14. **“A projection can decide because it is fast.”** Speed does not transfer write or policy authority.
15. **“Failover creates another SoR.”** A correct distributed authority changes active writer while preserving logical ownership.
16. **“SoR designation proves compliance.”** Legal preservation, privacy, security, quality, and availability need separate evidence.

## Worked Examples

### Example 1

**Situation.** Sales calls CRM “the customer source of truth,” while billing and identity teams object.

**Reasoning.** Split the claim. CRM owns sales-contact notes and pipeline stage. Identity owns legal-party identifiers and verified name. Billing owns invoice address for each account. A consent service owns marketing permission by channel and jurisdiction. Every system may cache selected fields, but its contract names source and version. No platform is authoritative for the compound word “customer.”

**Conclusion.** Fact-level authority resolves an apparent product dispute that one global label cannot.

### Example 2

**Situation.** Two agents edit profile version 17 concurrently. Each sends a different address with expected version 17.

**Reasoning.** The authority atomically checks the first command, commits version 18, and records its operation outcome. The second command no longer satisfies $ev=17$ and returns conflict with current version. The agent reloads and decides whether to resubmit a new operation. If either request response is lost, retry uses its original operation ID rather than creating another update.

**Conclusion.** Version comparison prevents a lost update inside one authority; operation identity handles ambiguous retry.

### Example 3

**Situation.** Search receives a profile change committed at 10:00:00 and applies it at 10:00:12 under clocks known synchronized within one second.

**Reasoning.** Observed projection lag is $12$ seconds with roughly one-second clock uncertainty. Search records profile version and source position. A directory search allowing 60-second staleness may use it. An access revocation requiring 2-second enforcement cannot; that path queries or receives a higher-assurance authority signal. The search hit does not become write authority.

**Conclusion.** Freshness is measured and judged against purpose rather than hidden behind “eventual.”

### Example 4

**Situation.** A service commits order version 31, crashes before publishing `OrderAccepted`, and restarts.

**Reasoning.** Without a recoverable publication obligation, consumers never learn the fact. The service writes order state and an outbox row in one local transaction. After restart, a relay publishes the stable event ID and marks delivery progress. Duplicate publication is possible; inventory projection applies version 31 idempotently and rejects an older version 30 update. Business completion still depends on downstream authoritative outcomes.

**Conclusion.** An outbox closes the commit-notification gap while preserving explicit at-least-once consumer work.

### Example 5

**Situation.** A corrected birth date entered on 12 June is valid from 4 May, replacing an assertion recorded on 7 May.

**Reasoning.** A current-only overwrite loses what the organization believed between 7 May and 12 June. Store the original assertion's valid and transaction intervals, the correction's transaction time, retroactive valid time, source evidence, actor, and supersession link. Queries can answer “current accepted birth date,” “what applied on 5 May under today's knowledge,” and “what did we believe on 8 May.”

**Conclusion.** Valid and transaction time support correction and historical reconstruction without treating the newest record time as the newest domain fact.

### Example 6

**Situation.** A field inspection app approves work offline in a jurisdiction where only the central regulator can authorize completion.

**Reasoning.** The device can store signed inspection evidence and a pending submission, but cannot display regulatory approval. On reconnect it sends stable submission ID, inspector identity, device state, evidence hashes, valid time, and expected case version. The regulator accepts, rejects, or requests review. If local safety requires immediate action, a separate delegated emergency authority and bounded operation must be explicitly defined.

**Conclusion.** Offline capture does not silently transfer legal decision authority.

### Example 7

**Situation.** During failover, an isolated old database primary and a promoted new primary can both reach some clients.

**Reasoning.** Endpoint switching alone permits split brain. Promotion establishes authority epoch 44 and a fencing token enforced by the storage or write proxy. Writes carrying epoch 43 are rejected even if the old process is healthy. Clients retry stable operations against the new authority and query ambiguous outcomes. Reconciliation checks the final log position and external effects before declaring recovery.

**Conclusion.** Fencing preserves one logical write authority across failover; health checks alone do not.

### Example 8

**Situation.** A privacy deletion removes a customer row, but name and behavior remain in search, features, logs, exports, and backups.

**Reasoning.** The architecture maps lineage and applicable policy to each copy. Search receives a tombstone and proves index removal; feature datasets rebuild or apply deletion under model-governance rules; logs minimize or tokenize identity according to retention; exports notify accountable recipients; backups expire or support deletion-on-restore under approved policy. Legal holds can override ordinary deletion only through authorized recorded decisions.

**Conclusion.** Deletion is a lifecycle process across known derivations, not one SQL statement.

### Example 9

**Situation.** A company migrates account authority from system A to B and proposes writing both for three months.

**Reasoning.** Independent dual writes can diverge. Keep A authoritative while B is backfilled and consumes A's durable changes. Compare balances, versions, and invariants. At cutover, establish epoch 9, route and fence all writes to B, make A read-only, and continue one-way comparison. Rollback either restores B's implementation or sends post-cutover authoritative changes through a tested reverse path before A can accept writes. Retire old credentials and feeds after the window.

**Conclusion.** Authority transfer is a fenced state transition, not prolonged duplication.

### Example 10

**Situation.** A medical device, hospital record, and national registry disagree about an implanted-device serial number.

**Reasoning.** Preserve three provenance-bearing assertions rather than selecting the latest timestamp. The device observation includes hardware identity and calibration; the hospital record includes procedure and operator; the registry includes manufacturer issuance. A clinical reconciliation case owns dispute status and safe-use decision under qualified human authority. Until resolved, downstream systems receive `disputed` plus allowed actions, not a fabricated golden value. Corrections append evidence and notify affected projections.

**Conclusion.** The SoR can govern adjudication while retaining competing claims when premature collapse could cause harm.

## Cross-Program Connections

- **Data Architecture Engineering:** owns systems of record, engagement, insight, master data, golden records, governance, lineage, and enterprise data lifecycle in depth.
- **Database Engineering:** transactions, MVCC, constraints, logging, replication, temporal data, backup, and recovery implement local authority guarantees.
- **Distributed Systems Engineering:** leader election, consensus, fencing, partitions, clocks, consistency, replication, and coordination govern distributed authority.
- **API and Service Engineering:** command, query, event, schema, compatibility, identity, error, idempotency, and outcome contracts expose the boundary.
- **Data Engineering:** CDC, outbox relays, projections, backfills, lineage, reconciliation, and deletion propagation operate derived copies.
- **Security Engineering:** authentication, authorization, separation of duties, integrity, confidentiality, audit, and break-glass controls protect authority.
- **Software Delivery and Reliability Engineering:** migration, rollout, rollback, observability, backup, restore, incident response, and retirement verify lifecycle behavior.
- **Systems Engineering:** decision authority, interface control, configuration baselines, evidence, risk acceptance, and lifecycle governance apply beyond software.

## References

1. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
2. Richard T. Snodgrass, *Developing Time-Oriented Database Applications in SQL*, Morgan Kaufmann, 1999. <https://www2.cs.arizona.edu/~rts/tdbbook.pdf>
3. W3C Provenance Working Group, *PROV-O: The PROV Ontology*, W3C Recommendation, 30 April 2013. <https://www.w3.org/TR/prov-o/>
4. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
5. Philip A. Bernstein and Eric Newcomer, *Principles of Transaction Processing*, 2nd ed., Morgan Kaufmann, 2009.
6. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM* 21(7), 1978. <https://doi.org/10.1145/359545.359563>
7. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002.
8. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.

## Exercises

### Exercise 1

Define system of record, write authority, system of entry, projection, provenance, valid time, transaction time, correction, and authority transfer. Explain why “the warehouse is the source of truth” is incomplete.

### Exercise 2

A projection has applied authoritative version 820. The authority is at version 847. Commits occurred at a measured mean of 3 per second over the interval. Estimate the version-based lag in seconds, state the calculation, and give three reasons it is not an exact freshness guarantee.

### Exercise 3

A service's operations team repairs records directly with SQL, while application commands enforce authorization, invariants, versioning, and audit. Diagnose the authority defect and design a break-glass repair path.

### Exercise 4

Compare direct authoritative queries, read replicas, event-built projections, and periodic snapshots for a product catalog, access revocation list, and monthly finance report. Assign freshness and unavailable behavior.

### Exercise 5

Design an authority model for a cross-border cargo system involving shippers, customs agencies, ports, carriers, and insurers. Cover scoped facts and operations, external assertions, identity, time, events and projections, partitions, disputes, privacy, recovery, migration, and evidence.

## Answers to the Exercises

### Answer 1

A **system of record** is the authorized decision boundary for specified facts or transitions in a declared scope and time. **Write authority** is permission and accountability to accept a transition. A **system of entry** captures intent or observation without necessarily deciding it. A **projection** is a derived consumer representation. **Provenance** records source agents and transformations. **Valid time** states when a fact applies; **transaction time** states when it was recorded. A **correction** supersedes or qualifies an assertion while preserving required history. An **authority transfer** changes the boundary allowed to accept writes through controlled cutover. A warehouse may contain broad history yet lack authority for operational writes; the statement omits fact family, operation, population, jurisdiction, time, owner, freshness, and derivation.

### Answer 2

The version gap is $847-820=27$ commits. At a mean 3 commits/s, a rough estimate is $27/3=9$ seconds. It is not exact because commit rate can vary; versions may cover unrelated entities or operations; projection processing and authoritative commit clocks or positions differ; batches or gaps can change version increments; and the projection may have received later versions out of order. A version position proves ordering only under its source contract. Exact freshness needs a compatible measurement protocol and purpose-specific bound.

### Answer 3

Direct SQL is an alternate writer that bypasses the declared authority controls, so the application cannot guarantee invariants, versions, or audit. Build an authenticated repair command owned by the domain, with case or incident reference, narrowly scoped target, expected version, explicit correction semantics, invariant validation, separation-of-duties approval where needed, idempotency, dry-run or preview, atomic commit, audit event, publication through the normal outbox, and post-change reconciliation. Credentials are short-lived, purpose-bound, monitored, and revoked after use. If a database-level repair is unavoidable during disaster recovery, fence normal writes, execute a reviewed script against a recorded snapshot, validate invariants, advance versions and authoritative history, replay derived notifications, and obtain accountable sign-off before reopening.

### Answer 4

Product catalog browsing can use an event-built projection or cache with displayed or governed freshness and fall back to a snapshot; product publication commands still go to catalog authority. An access revocation list needs a tightly bounded signed projection or direct authority query, fails closed or follows an approved short offline grace policy, and prioritizes low-lag revocation distribution; a monthly snapshot is inadequate for immediate revocation. A monthly finance report can use a period-closed snapshot with source positions, definitions, reconciliation totals, and approval because reproducibility matters more than current operational latency. Read replicas suit bounded-stale operational queries when schema and failover are governed, but they do not own writes. Full credit requires different choices by consequence rather than one universal mechanism.

### Answer 5

Shippers own declared cargo contents and packing assertions; customs agencies own clearance, hold, and release decisions in their jurisdictions; ports own physical receipt and gate events; carriers own custody and movement events; insurers own coverage decisions. Each assertion includes scoped identifier, issuer, valid and transaction time, jurisdiction, evidence, version, and correction. A cargo-case service can own composite workflow and dispute state without rewriting external authorities. Federated identities bind organizations, people, devices, and delegated roles; messages are signed or integrity-protected and disclose only purpose-required data. Durable idempotent events build port and insurer projections with freshness and provenance. During partitions, local safety and custody events continue under delegated authority, while clearance-requiring movement is queued, prohibited, or handled through an explicit emergency rule. Conflicts preserve source assertions and enter accountable adjudication. Recovery fences stale writers, replays from recorded positions, reconciles physical custody and external effects, and reports unknown intervals. Migration establishes one write authority per scoped fact and epoch, backfills and compares, cuts over with fencing, and retires old credentials. Evidence includes contract conformance, authorization and privacy tests, duplicate/reorder/partition tests, clock and time semantics, restore drills, dispute exercises, cutover rehearsal, and end-to-end reconciliation. A valid alternative may allocate more authority to a treaty-operated platform, but it must preserve sovereign jurisdiction and source provenance.
