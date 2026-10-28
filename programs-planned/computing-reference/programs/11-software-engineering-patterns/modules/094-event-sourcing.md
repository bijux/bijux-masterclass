---
module_id: SEPAT-094
program: Software Engineering: Patterns
level: 2
module_number: 94
title: Event Sourcing
status: complete
last_verified: 2026-08-29
---

# Event Sourcing

## One-Page Review

### Governing question

When should a domain preserve its accepted facts as the authoritative history and derive current state by replay, and what constraints make that history correct, evolvable, private, and operable?

### Essential definitions

- **Event Sourcing** stores the state changes of a domain entity/aggregate as an append-only sequence of immutable domain events and reconstructs state by folding them in order.
- A **command** requests a decision; it may be rejected and is not a historical fact.
- A **domain event** is a named past-tense fact accepted by the domain under then-current rules.
- An **event stream** is the ordered history for one aggregate/subject, commonly identified by stream ID and monotonically increasing revision.
- An **aggregate** is the consistency boundary that validates a command using reconstructed state and emits zero or more new events.
- **optimistic concurrency** appends only if the persisted stream revision equals the revision the decision read.
- A **projection** folds events into a query/read model; it is derived and rebuildable, unlike authoritative event history.
- A **snapshot** caches aggregate state at a known revision to reduce replay cost; it is an optimization, not authority.
- An **upcaster** deterministically translates an old representation into a form current code can interpret without rewriting what historically occurred.
- A **correction event** records a later fact that corrects or compensates history; it does not erase the original event.
- **temporal query** reconstructs state as of a historical revision/time under stated ordering and schema semantics.

### Central model, mechanism, or theorem

For stream $E_a=\langle e_1,\ldots,e_n\rangle$ of aggregate (a), state is

$$
s_n=fold(apply,s_0,E_a).
$$

A command handler computes $decide(s_n,c)=\langle e_{n+1},\ldots,e_{n+k}\rangle$, then atomically appends those events with expected revision (n). If another writer already appended, the store rejects the append; the caller reloads and re-decides or reports conflict. Events are authority only if `apply` is deterministic, order/revision is durable, accepted events cannot be silently changed, every retained representation remains interpretable, and corrections are explicit.

### Critical invariants

- Events state accepted domain facts, not CRUD diffs, commands, transient implementation details, or consumer instructions.
- One stream revision has at most one event; appends are atomic and compare expected revision.
- Decision logic validates against state reconstructed from exactly the revision named by the append.
- Event ID, stream ID, revision, type/version, occurrence/record time, causation and actor/context are distinguished.
- Applying events is deterministic and free of network, clock, randomness and external side effects.
- Original stored bytes/meaning remain auditable; upcasters do not fabricate unavailable historical facts.
- Snapshots identify their exact stream revision and can always be discarded and rebuilt.
- Projections are versioned, checkpointed, idempotent and rebuilt without repeating external effects.
- Retention, privacy erasure, encryption/key destruction and legal/audit requirements are decided before indefinite history is promised.
- Backup/restore, corruption detection and full/bounded replay meet explicit RPO/RTO and capacity targets.

### Common failures

Common failures are event sourcing every table; naming events `EntityUpdated`; storing commands as facts; placing current-time/lookups in `apply`; generating events while replaying; omitting expected revision; one stream for an entire tenant; cross-stream invariants disguised as aggregate invariants; using snapshots as authority; rewriting event rows; dishonest upcasting; mixing projection rebuild with email/payment effects; retaining secrets forever; unbounded replay; dual-writing events and current state; assuming broker retention is an event store; and equating Event Sourcing with CQRS or event-driven architecture.

### Compact example

Wallet stream revision 0 begins empty. `Opened(100)`, `Debited(30)`, `Credited(5)` reconstruct balance 75 at revision 3. Two writers read revision 3 and decide debits 50 and 40. Only one expected-revision-3 append can succeed; the loser reloads revision 4 and discovers whether its debit remains valid. The concurrency check protects the decision invariant without locking the whole application.

### Connections

[Change Data Capture](093-change-data-capture-pattern.md) derives technical changes from another authoritative store; Event Sourcing makes domain events authoritative. [Transactional Outbox](088-transactional-outbox.md) publishes integration events without making the domain event store a public broker. [Memento](036-memento.md) and snapshots cache state but do not replace history. The successor [Command Query Responsibility Segregation](../ROADMAP.md) can separate write and read models without requiring Event Sourcing.

## Governing Question

How can a team judge whether preserving domain history is worth the semantic, evolutionary and operational burden, then implement event decisions and replay without corrupting history or duplicating effects?

Event Sourcing is attractive because it retains why current state exists, supports new projections and temporal analysis, and makes state transitions explicit. It is costly because history becomes a permanent API to future code. A mutable row lets developers repair a value; an authoritative event log demands a correction model. A simple schema migration becomes compatibility across every retained record. Privacy, backup, replay time, operational tooling and developer comprehension become first-class design constraints.

Use the pattern where history has durable business value and the domain naturally speaks in meaningful transitions: ledgers, entitlement changes, workflow decisions, inventory reservations, trading orders, collaborative operations. Avoid it for ordinary reference data, simple CRUD, derived caches, low-value histories or teams unable to operate immutable schemas and replay. Select per bounded context or aggregate, not as an organization-wide identity.

## Why This Matters

Current-state persistence destroys intermediate facts unless they are separately audited. If an account row says `balance=75`, it cannot alone answer which authorized transactions produced it, what the balance was at revision 8, or whether a newly discovered projection rule changes reporting. Event history can answer those questions by recomputation from accepted facts.

But an event log is not automatically truthful. An `AccountUpdated` payload containing every field is a serialized row diff with weak meaning. A handler that consults today's exchange rate during replay reconstructs different state tomorrow. A developer who “fixes” an old event invalidates audit hashes and previously computed decisions. A projection that emails during replay turns recovery into an incident. A stream with medical notes may conflict with erasure/minimization duties.

The pattern's value emerges only when five concerns align: domain facts are stable and meaningful; append concurrency matches the consistency boundary; event application is deterministic; retained history can evolve and be governed; and operations can restore/replay within objectives. Otherwise a current-state model plus explicit audit/outbox records is usually simpler.

## Prerequisites and Retrieval

Learners should retrieve:

- domain aggregates, invariants, commands, value objects and bounded contexts;
- append-only logs, stream order, atomic compare-and-set and optimistic concurrency;
- pure deterministic folds and state machines;
- message identity, causation, correlation and idempotent consumers;
- schema compatibility, semantic versioning and migrations;
- snapshots, checkpoints, projections and materialized views;
- backup, retention, encryption, privacy and disaster recovery;
- transactional outbox and integration-event boundaries.

Before continuing, explain why “rebuild state from messages in Kafka” is insufficient to claim Event Sourcing. Identify authority, per-aggregate concurrency, retention, immutable history and deterministic application requirements.

## Learning Objectives

After this module, learners can:

1. distinguish Event Sourcing from audit logging, CDC, messaging, CRUD history and CQRS;
2. model command-decision-event-application flow for an aggregate;
3. prove how expected revisions prevent lost-update invariant violations;
4. design event identities, metadata, stream boundaries and append semantics;
5. keep replay deterministic and separate state reconstruction from effects;
6. evolve retained event representations with honest compatibility/upcasting;
7. model correction, deletion, redaction and privacy without silent rewriting;
8. design snapshots and projections as disposable versioned derivatives;
9. test replay, concurrency, corruption, recovery and full-history operability;
10. reject Event Sourcing when its benefits do not exceed its permanent costs.

## Core Exposition

### Start from decisions, not storage technology

A client submits a command such as `DebitWallet(amount=30, command_id=x)`. The aggregate loads its event stream, folds events into state, validates that the wallet is open and funds are sufficient, and returns `WalletDebited(amount=30, command_id=x)` or a rejection. Only accepted facts append. Applying that event changes balance; it never rechecks an external service or emits another event.

Separate functions:

- `decide(state, command) -> events or rejection` may use policy inputs explicitly captured for the decision;
- `apply(state, event) -> state` is total for supported history and deterministic;
- `append(stream, expected_revision, events)` atomically succeeds or conflicts;
- publication and projections observe committed events afterward.

This split permits property tests: replaying the same events produces the same state; rejected commands append nothing; accepted events preserve invariants; and concurrent decisions cannot both append at one revision.

### Design streams around consistency ownership

One stream normally represents one aggregate instance, not one table, event type or entire application. Stream identity scopes order and optimistic concurrency. If all tenant events share one stream, unrelated commands contend and replay grows without bound. If an invariant spans multiple independent streams, Event Sourcing does not make their append atomic. Redesign the aggregate boundary, reserve through a process/saga, or use a store that supports the required transaction explicitly.

Expected revision implements compare-and-set. Writer W1 and W2 read revision (n). W1 appends at expected (n), producing (n+1). W2's append with expected (n) fails; it must reload and re-run authorization/invariants. Blind retrying the previously produced event would bypass the new decision context. Command IDs can deduplicate client retries, but expected revision protects concurrent state changes; they solve different problems.

Multiple events produced by one command must append atomically within the stream. Global ordering across streams is usually unnecessary and expensive. Cross-stream projections use store positions or per-stream revisions and must state what consistency they expose.

### Make event meaning durable

Use past-tense domain facts: `OrderPlaced`, `SeatReserved`, `AddressCorrected`. Include only information necessary to understand and apply the fact under its historical meaning. Record stable identifiers, event type/schema version, stream/revision, command/causation identity, actor/context required for audit, and occurrence/record times with clear definitions.

Avoid `CustomerUpdated` with a generic property map: future code cannot know the business decision. Avoid copying full aggregates: secrets and internal shape become permanent. Avoid events that describe UI clicks rather than accepted domain facts unless the UI interaction itself is the domain. Avoid putting a live object/class name into the durable type contract.

Domain events are often private. Public integration events have different minimization, compatibility and consumer ownership. A committed domain event can transactionally produce an outbox record or a publisher can derive a governed integration event, with idempotent publication. Do not let external consumers bind directly to every internal event merely because a broker can expose it.

### Replay must be a pure interpretation

`apply` must depend only on prior state and event. No wall clock, random ID, environment variable, database lookup, network call, feature flag or current policy. If a decision depended on exchange rate 1.09, tax rule version R or actor authorization, the accepted event must contain the relevant outcome/reference necessary for future interpretation. Replay reconstitutes what was accepted; it does not ask whether today's policy would accept it.

External effects belong to live effect handlers with stable idempotency identities and replay modes. Projection rebuilds should default to no email, payment, webhook, job launch or integration publication. A live subscription and rebuild process need explicit consumer/effect versions, independent checkpoints, bounded targets and promotion procedures.

Determinism can be tested by replaying fixtures repeatedly and across supported implementations, hashing canonical state, injecting clocks/randomness that must not be called, and rebuilding projections from zero. A passing unit fold does not prove the event store's append, durability or backup properties.

### Treat history evolution as an API

Stored events outlive code. Preserve original bytes and schema/type metadata. New readers must either understand old records or apply deterministic upcaster chains. An upcaster may rename a field when meaning is identical or provide a default only when historical absence truly implied that value. It cannot invent which tax regime applied, convert an ambiguous duration into execution time, or reinterpret a rejected command as an accepted fact.

Prefer additive compatible evolution where semantics stay stable. Create a new event type/version when meaning changes. Keep fixture corpora spanning every historical version, test adjacent and composed upcasters, and execute bounded dry-run replays before deployment. Never run network/current-time logic inside upcasting. Rewriting the event store destroys provenance unless a rare, governed legal/security migration explicitly creates a new lineage and preserves evidence of the transformation.

Corrections append. If `CustomerAddressRecorded` was wrong, append `CustomerAddressCorrected` with authority and causation. Financial reversal/compensation is a new fact, not deletion of history. Some sensitive data should never be stored in the event: use minimization, references/tokenization, encryption with controlled keys, segregated vaults and retention. Crypto-shredding may make payload unreadable but complicates replay; legal/privacy counsel and named human reviewers must decide regulated designs.

### Snapshots optimize, never authorize

Replaying 200,000 events for every command is expensive. A snapshot stores folded aggregate state plus exact stream revision and compatible snapshot schema. Load the snapshot, then replay events after that revision. On corruption or incompatibility, discard it and replay from authority. Validate its digest/revision and append expected revision against the actual stream, not merely the cached object.

Snapshot cadence can be count-, size- or latency-based. Too frequent wastes writes; too rare misses latency goals. Snapshot creation can be asynchronous if revision-tagged. Snapshotting cannot repair a giant aggregate boundary or an event stream whose retained events no longer decode. Measure p95/p99 load latency, replay event count and rebuild duration before adding it.

### Projections are replaceable products

Queries rarely replay aggregates on demand. A projection consumes committed events into a read model. It has a projector version, checkpoint, schema and idempotency rule. Build a changed projection into a new physical target, catch up to a bounded position, reconcile, then switch readers atomically; keep rollback until confidence expires. Do not mutate the sole production view in place during a full replay.

Events can arrive twice at the projector; atomically record `(projector_version,event_id)` with mutation or compare stream revision. Cross-stream ordering may be eventual. Poison events stop or quarantine under explicit policy; skipping silently invalidates completeness. Projection state is not an authority for command decisions unless the consistency model deliberately permits staleness.

### Operate the event store as irreplaceable data

An event store requires atomic append, unique stream revision, durable ordering, backup, point-in-time recovery, corruption detection, authorization, tenant isolation, encryption, capacity and observability. A general message broker may have retention/compaction and consumer semantics inconsistent with permanent authoritative history. Durable store and publication broker may be separate.

Record event count/bytes per stream, command conflict rates, append latency, unsupported schema events, projection lag, replay throughput, snapshot hit/corruption, backup age and restore verification. Define maximum rebuild time and test it at production-like history size. Archive choices must preserve readable schemas and meet retrieval RTO. If losing the event log means losing current truth, backup/restore deserves greater rigor than derived database restoration.

### A deterministic aggregate model

The following executable fold and decision model reconstructs a wallet and demonstrates expected-revision conflict reasoning. Persistence concurrency is represented, not implemented.

<!-- bijux-verify: {"id":"sepat-094-event-fold","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"revision=3 balance=75\ndecision=WalletDebited:50\nfirst-append=accepted revision=4\nsecond-append=conflict expected=3 actual=4\nreloaded-decision=rejected insufficient-funds\n","stderr":""}} -->
```python
events = [("WalletOpened", 100), ("WalletDebited", 30), ("WalletCredited", 5)]

def apply(balance, event):
    kind, amount = event
    if kind == "WalletOpened":
        return amount
    if kind == "WalletDebited":
        return balance - amount
    return balance + amount

def replay(history):
    balance = 0
    for event in history:
        balance = apply(balance, event)
    return balance

def decide_debit(balance, amount):
    if amount > balance:
        return None
    return ("WalletDebited", amount)

balance = replay(events)
expected_revision = len(events)
first = decide_debit(balance, 50)
second = decide_debit(balance, 40)
print("revision=" + str(expected_revision) + " balance=" + str(balance))
print("decision=" + first[0] + ":" + str(first[1]))

events.append(first)
print("first-append=accepted revision=" + str(len(events)))
print("second-append=conflict expected=" + str(expected_revision) + " actual=" + str(len(events)))

reloaded = replay(events)
second_after_reload = decide_debit(reloaded, second[1])
result = "rejected insufficient-funds" if second_after_reload is None else "accepted"
print("reloaded-decision=" + result)
```

The run proves the pure fold and chosen trace only. It does not implement atomic append, command deduplication, event durability, serialization, upcasting, distributed publication, privacy, snapshots, projection recovery or multi-writer concurrency.

## Definitions and Notation

Let aggregate (a) have stream $E_a=\langle e_1,\ldots,e_n\rangle$. Let (s_0) be initial state, $apply:S\times E\rightarrow S$, $D:S\times C\rightarrow E^*\cup Reject$, and (A(a,n,newEvents)) be an atomic append conditioned on current revision (n).

**Deterministic replay** requires equal supported event sequences to produce equal state: (fold(apply,s_0,E)=fold(apply,s_0,E)) across runs independent of external environment. **Linear per-stream history** requires a unique event at each revision and atomic multi-event append. **Decision safety** means emitted events follow from command rules evaluated against the exact revision used for append. **Projection completeness through position (q)** means every in-scope event at/before (q) has been applied under the projector's declared semantics.

If a snapshot is ((s_k,k)), recovery computes $fold(apply,s_k,\langle e_{k+1},\ldots,e_n\rangle)$. Snapshot correctness depends on $s_k=fold(apply,s_0,\langle e_1,\ldots,e_k\rangle)$; revision alone does not establish that equality.

Event time (t_o) (domain occurrence), recorded time (t_r) (store acceptance), stream revision (v), global/store position (g), event ID, command ID, causation ID and correlation ID are separate coordinates. None universally substitutes for another.

## Mechanisms, Invariants, or Proof Structure

1. **Specify value.** Name decisions/history questions that justify permanent event authority; document a simpler current-state alternative.
2. **Bound consistency.** Define aggregate stream identity and invariants enforceable from that stream alone.
3. **Model facts.** Review past-tense semantics, minimal payload, identities, time, actor, causation, classification and schema ownership.
4. **Split decide/apply.** Ensure decisions validate commands and application is deterministic/side-effect-free.
5. **Append conditionally.** Atomically compare expected revision, append all command events and deduplicate command identity as required.
6. **Evolve history.** Preserve original records, version schemas, retain fixtures and use honest deterministic upcasters or new types.
7. **Derive safely.** Version snapshots/projections, checkpoint idempotently, rebuild into isolated targets and suppress external effects.
8. **Correct explicitly.** Append correction/compensation facts and define privacy/redaction/key-destruction policy before sensitive history.
9. **Protect authority.** Back up, restore, integrity-check, authorize and capacity-test the event store.
10. **Prove operation.** Run concurrency, duplicate, schema-history, corruption, full replay, catch-up, reconciliation and disaster exercises.

For concurrency, assume two commands decide at revision (n). Atomic expected-revision append permits at most one to occupy (n+1). The other conflicts and cannot persist its stale decision; after reload it is evaluated against the winner. This protects stream-local invariants if every writer uses the condition and the invariant depends only on stream state. It does not prove cross-stream invariants, fairness, liveness or correct command policy.

## Alternatives and Trade-Offs

**Current-state model** stores only latest authoritative state. It is simpler to query/migrate and can add explicit audit records for selected transitions. Choose it when temporal reconstruction and alternate projections have low value.

**Audit log** records who did what around mutable state. It can satisfy investigation/compliance without becoming reconstruction authority. Audit and state can diverge unless transactionally coupled.

**CDC** captures physical committed changes from a current-state database. It helps replication/integration but lacks stable domain intent and usually cannot re-decide aggregate meaning.

**Transaction log** is an engine recovery mechanism, not necessarily domain-readable, permanently retained or schema-governed.

**Outbox/integration events** reliably publish selected facts from a normal state transaction. They serve external consumers without requiring every domain decision to be reconstructed from events.

**Bitemporal/current-state history tables** preserve valid/transaction-time versions and answer historical queries efficiently. They may fit record histories better than behavioral events.

**CQRS** separates command and query models; either side may use conventional persistence. Event Sourcing commonly feeds CQRS projections, but neither requires the other.

Choose Event Sourcing only when history/replay benefits exceed modeling, schema permanence, privacy, tooling, operational and onboarding costs. A small append-only financial subdomain can coexist with conventional CRUD elsewhere.

## Failure Modes and Misconceptions

- **“Event-driven means event-sourced.”** Messages can coordinate systems while current state remains authoritative.
- **“Events are row diffs.”** Diffs lack decision meaning and couple history to storage layout.
- **“Commands belong in history.”** Rejected requests are not accepted facts; audit them separately if needed.
- **“Replay may call current services.”** That creates nondeterministic, unavailable or historically false state.
- **“Optimistic concurrency is command dedupe.”** Revision prevents stale writes; command identity prevents retry duplication.
- **“One huge stream is simplest.”** It creates contention, massive replay and unrelated consistency coupling.
- **“Snapshot is current truth.”** It is a cache at a revision and must be discardable.
- **“Upcasting can fill any missing field.”** It may translate representation, never invent unknown historical semantics.
- **“Immutable means ungovernable.”** Corrections append, but privacy/security may require minimization, encryption or a new governed lineage.
- **“Rebuild means rerun every handler.”** Effects and projection state must be separated; replay defaults to effect-disabled.
- **“Broker equals event store.”** Retention, compaction, revision uniqueness, backups and per-stream append semantics may differ.
- **“CQRS requires Event Sourcing.”** Read/write separation works with conventional databases.
- **“All reports can replay live.”** Query projections and snapshots exist because full folds have latency/cost limits.
- **“History is automatically audit evidence.”** Identity, authorization, integrity, time semantics, access and restore evidence still matter.
- **“We can migrate later.”** Every event type is a long-lived contract from its first append.

## Worked Examples

### Example 1

**Situation.** A wallet with balance 75 receives two concurrent debits, 50 and 40; both handlers read revision 3.

**Reasoning.** Each independently sees sufficient funds. The store accepts the first append with expected revision 3 and advances to 4. It rejects the second stale append. Reloaded balance 25 causes debit 40 to be rejected. Without expected revision, both append and balance becomes -15.

**Conclusion.** Stream-local compare-and-append converts concurrent stale decisions into an explicit conflict and preserves the funds invariant.

### Example 2

**Situation.** An event's apply method uses `today()` to decide whether a membership is expired.

**Reasoning.** Replaying next month produces different state from replay today. The event should record the accepted expiry or the decision should emit `MembershipExpired` when that fact occurs. Current-time queries belong outside deterministic state application.

**Conclusion.** Replay interprets recorded facts; it must not rerun time-dependent decisions.

### Example 3

**Situation.** A schema rename changes `duration_ms` to `execution_ms`, but the old value included queue time.

**Reasoning.** Copying the number in an upcaster changes meaning. Preserve old semantic type/field, introduce a new event version where execution duration is known, or represent historical absence as unknown.

**Conclusion.** Upcasting is honest only for representation-preserving transformations.

### Example 4

**Situation.** Aggregate load exceeds a latency objective after 80,000 events.

**Reasoning.** Store a verified snapshot at revision 75,000 and replay later events. Append still uses actual stream revision 80,000. Corrupt/mismatched snapshot is discarded. If streams regularly grow this large, also review aggregate lifetime/boundary and archival rules.

**Conclusion.** Snapshots reduce replay work but never replace event authority or correct poor stream design.

### Example 5

**Situation.** A projection schema changes; engineers reset its checkpoint and run the normal subscriber.

**Reasoning.** That subscriber also sends welcome emails. Replay resends years of mail. Separate pure projector from live effect handler, build projection version 2 into a new target through a bounded position, reconcile, catch up and switch.

**Conclusion.** Replayability requires explicit effect isolation, versioned targets and promotion—not merely resettable offsets.

### Example 6

**Situation.** A customer name was recorded incorrectly six months ago.

**Reasoning.** Editing the old event makes previously observed history irreproducible. Append `CustomerNameCorrected` with authorization, reason and causation; current projections show corrected state while audit views retain the original and correction.

**Conclusion.** Corrections are new facts unless a narrowly governed privacy/security transformation creates a documented new lineage.

### Example 7

**Situation.** A reservation invariant needs available seats across a venue, but every seat has an independent stream.

**Reasoning.** Reading multiple streams then appending one does not atomically protect global capacity. Model a performance/inventory aggregate, use reservation tokens/process coordination, or select transactional current-state storage. Event Sourcing alone supplies no cross-stream transaction.

**Conclusion.** Stream boundary must contain the invariant or the design needs an explicit distributed coordination model.

### Example 8

**Situation.** Kafka retains events for seven days, while a projection's recovery objective requires replaying a year.

**Reasoning.** The topic cannot be sole authority/recovery source. Keep an event store/archive with immutable readable history, or use verified snapshots plus retained deltas that meet the horizon. Test restoration, not just normal consumption.

**Conclusion.** Transport retention and authoritative history are separate contracts.

### Example 9

**Situation.** A client times out after a successful append and retries the same command against the new revision.

**Reasoning.** Expected revision alone may treat it as a new decision and append a duplicate debit. Persist a command ID/result within the aggregate stream or transactional command ledger; return the prior outcome for the same identity and reject identity reuse with a different payload.

**Conclusion.** Command deduplication complements optimistic concurrency; neither substitutes for the other.

### Example 10

**Situation.** A clinical event stream proposes storing free-text diagnosis notes forever to support audit and replay.

**Reasoning.** Immutability, backup replication and derived projections increase exposure and complicate correction/erasure. Store the minimum durable clinical fact, segregate/tokenize sensitive content, define retention/key-destruction and access/audit controls, and prove required reconstruction without raw excess. A named human clinical, privacy and security review must approve the fact model and unresolved legal trade-offs before production.

**Conclusion.** Event history is permanent data architecture, not a license for permanent maximal payloads.

## Cross-Program Connections

- **Domain Modeling:** aggregate boundaries and domain language determine what can be decided from one stream.
- **Distributed Systems:** linearizable per-stream append, concurrency conflict, replay, ordering and idempotency define mechanics.
- **Database Engineering:** append indexes, transaction durability, backup/PITR, corruption and storage growth protect authority.
- **Data Engineering:** projections, watermarks, backfills and temporal analytics consume event history under governed schemas.
- **Security Engineering:** immutable sensitive histories require minimization, access, encryption, integrity and erasure strategy.
- **Testing and Quality:** state-machine/property tests, historical fixture corpora, deterministic replay and restore drills provide evidence.
- **Architecture:** bounded-context choices and public/private event translation prevent internal histories becoming accidental enterprise APIs.
- **Reliability Engineering:** full replay time, projection catch-up, backup age and conflict/load metrics become operational objectives.

## References

- Martin Fowler, [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html), 2005, retrieved 2026-08-29. Foundational description of capturing changes as events, reconstruction, temporal query, replay and snapshots.
- Greg Young, [CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf), 2010, retrieved 2026-08-29. Defines command/event handling, event storage, aggregate application and CQRS relationships.
- Microsoft Azure Architecture Center, [Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing), retrieved 2026-08-29. Current architectural guidance on append-only event stores, materialized views, consistency, snapshots and challenges.
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017, chapters 11–12. Durable treatment of event streams, immutable events, derived state and future-compatible data systems.
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2003. Establishes aggregates, bounded contexts and domain events' modeling foundations.
- Vaughn Vernon, *Implementing Domain-Driven Design*, Addison-Wesley, 2013, chapters 8 and 10. Practical aggregate and domain-event design with consistency boundaries.
- Pat Helland, [Immutability Changes Everything](https://www.cidrdb.org/cidr2015/Papers/CIDR15_Paper16.pdf), CIDR 2015, retrieved 2026-08-29. Analyzes immutable facts, derived state and implications for distributed data.
- Cloud Native Computing Foundation, [CloudEvents Specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), version 1.0.2, retrieved 2026-08-29. Provides an interoperable event-envelope reference; it does not define Event Sourcing semantics.

## Exercises

### Exercise 1

Distinguish a command, domain event, integration event, event stream, projection and snapshot using one order-domain example. State which artifacts are authoritative.

### Exercise 2

Two writers read inventory stream revision 12 with available quantity 7. They decide reservations of 5 and 4. Trace expected-revision append, retry and final outcomes. Identify assumptions.

### Exercise 3

Diagnose an event-sourced service whose replay produces different balances after a deployment, whose snapshot revision matches the stream, and whose projection sent duplicate invoices during rebuild.

### Exercise 4

Compare Event Sourcing, current-state plus audit log, current-state plus outbox, and bitemporal tables for an insurance-claim system. Select boundaries rather than one universal choice.

### Exercise 5

Design an event-sourced collaborative document aggregate that must support offline edits, deletion/privacy, ten-year history, new projections and region recovery. Identify where Event Sourcing is insufficient by itself.

## Answers to the Exercises

### Answer 1

`PlaceOrder` is a command requesting a decision. After validation, `OrderPlaced` is the private domain fact appended to order stream `order-42`; that stream is authoritative for the order aggregate. `OrderPlacedForFulfillmentV1` can be a minimized public integration event derived into an outbox; it is authoritative as a published contract fact but not the internal reconstruction store. `OpenOrdersByCustomer` is a projection and is rebuildable. A snapshot containing order state at revision 30 is a disposable load optimization. Authority belongs to the immutable order stream for domain state, while the integration contract has its own publication authority; neither projection nor snapshot may silently correct the stream.

### Answer 2

Both decisions are valid against revision 12. Writer A atomically appends `InventoryReserved(5)` with expected 12; stream becomes 13 and available becomes 2. Writer B's append with expected 12 conflicts. It reloads revision 13, re-runs `Reserve(4)`, and rejects for insufficient quantity; it must not blindly append the stale event. Reversing winner yields reserve 4 then rejection of 5, leaving 3. Assumptions: all inventory-changing writers use the same stream/conditional append, each append is atomic, application is deterministic, quantity is stream-local, and retry uses the original command identity/policy. The mechanism proves nonnegative stream-local quantity, not fairness or cross-stream stock correctness.

### Answer 3

Different replay suggests nondeterministic `apply`/upcasting, changed semantics, unsupported old records or corrupted history; compare original bytes, schema versions and canonical state across old/new code while injecting clocks/services that must not be called. A matching snapshot revision does not prove snapshot content: discard it and fold from zero, compare digest, then regenerate. Duplicate invoices show live external effect and pure projection rebuild were mixed. Introduce effect identities/ledger and replay-disabled mode; rebuild a versioned projection target to a bounded position, reconcile and promote. Inspect whether invoices already escaped and correct through business-approved records—not deletion. Add fixture history, repeatability/property tests, snapshot digest checks and a replay runbook.

### Answer 4

Use Event Sourcing for a bounded claim-decision stream if adjuster decisions, evidence acceptance, reserves and reversals require temporal reconstruction and alternate adjudication views. Keep large documents in governed content storage referenced minimally. A current-state claim plus transactional audit may suffice for administrative fields where reconstruction has little value. Use an outbox to publish stable claim facts to payments/notifications without exposing private domain events. Bitemporal tables fit policy/coverage facts that require valid-time and transaction-time queries but are naturally records rather than behavior. Evaluate retention/privacy, cross-claim invariants, replay RTO, schema governance and team capability. The model answer deliberately combines approaches: applying Event Sourcing to every insurance table would increase permanent coupling without proportional value.

### Answer 5

Choose a document or bounded shard as stream only if its consistency/replay size remains operable. Commands carry stable actor/operation IDs and expected causal context; accepted events contain deterministic operations, author/authorization evidence and logical position. Ordinary optimistic revision alone cannot merge offline concurrent edits: add an explicit operational-transform/CRDT or conflict-resolution algorithm, which Program 27 owns. Keep `apply` deterministic and command-deduplicate offline retries. Build search/activity projections with versioned checkpoints and effect-disabled replay; snapshot at measured operation counts while preserving stream authority.

Minimize content, segregate encrypted payloads, define tenant access, deletion/redaction/key-destruction and what ten-year audit legally requires. A deletion request may append a fact while cryptographically making content unavailable, but this can make full replay impossible; document the post-erasure reconstruction model and obtain named human privacy/legal review. Replicate and back up authoritative events across regions with integrity checks, RPO/RTO, failover lineage and full restore/replay drills. Test old schema fixtures, upcasters, duplicate/reordered offline commands, concurrent merge properties, corruption and projection catch-up. Event Sourcing supplies history and per-stream concurrency; it does not by itself solve collaborative merge semantics, global order, authorization, privacy law, cross-region consensus or disaster recovery.
