---
module_id: SEPAT-037
program: Software Engineering: Patterns
level: 1
module_number: 37
title: Observer
status: complete
last_verified: 2026-08-28
---

# Observer

## One-Page Review

### Governing question

How can one subject announce committed changes to an open set of dependents without knowing their concrete behavior, while lifecycle, order, reentrancy, failure, consistency, demand, delivery, and security remain explicit?

### Essential definitions

- A **subject/publisher** owns state or occurrences and a subscription/notification protocol.
- An **observer/subscriber** registers interest and receives notifications through a narrow interface.
- A **subscription** is a lifecycle capability with registration, activation boundary, cancellation, and ownership.
- **push** notifications carry state/change data; **pull** notifications say what changed and let observers query authoritative state.
- An **invalidation** says cached data may be stale; it is not the replacement value.
- A **snapshot dispatch** freezes the observer set for one notification so additions/removals during callbacks affect later dispatches.
- **backpressure** is a demand/capacity protocol preventing a producer from overwhelming a consumer.
- A **durable event** records a fact for transport/replay; a local callback is not durable delivery.

### Central model, mechanism, or theorem

For committed subject transition $s_v\xrightarrow{a}s_{v+1}$, construct immutable event (e=(id,source,type,version,payload)), snapshot active observers (L), then invoke each according to the documented dispatch policy. For observer projection (q), update is

$$
q' = U(q,e),\qquad e.version>q.version,
$$

with duplicate/stale handling defined. This provides one-to-many notification structure; it does not by itself provide transactionality, asynchronous capacity, durable delivery, total order, exactly-once effects, or subscriber correctness.

### Critical invariants

- Notifications describe committed facts or explicit pre-commit proposals; the two are never confused.
- Event identity, source/type/schema, subject version/order key, and payload ownership are explicit.
- Subscription activation and initial snapshot cannot leave an undocumented lost-update gap.
- Dispatch defines observer-set snapshotting, order, reentrancy, additions/removals, and exception isolation.
- Observers do not mutate the subject through hidden callback cycles; commands enter through validated APIs.
- Subscription ownership/cancellation prevents stale callbacks and memory/resource leaks.
- Async/durable delivery defines queues, demand/backpressure, duplicates, retry, dead-letter/reconciliation, and lag.
- Authorization, tenant scope, minimization, redaction, and current access checks apply at publication and consumption.

### Common failures

Common failures include string topics with `any` payloads, notification before commit, mutable events, observers querying half-updated state, holding locks during callbacks, subscriber-order dependence, one exception aborting silently, recursive feedback loops, duplicate registration, leaked strong references, unsubscribe races, initial-query/subscribe lost updates, unbounded executor queues, slow subscribers blocking producers, trusting event roles, broadcasting secrets, assuming in-process callbacks survive crashes, assuming a broker supplies exactly-once effects, replaying external side effects, and treating cache invalidation as authoritative data.

### Compact example

A catalog commits a versioned immutable price-change event and dispatches over a tuple snapshot. One observer unsubscribes during version one but still receives that in-progress dispatch; only the remaining observer receives version two. This makes mutation-during-notification semantics deterministic.

### Connections

[SEPAT-036](036-memento.md) captures prior state; [SEPAT-038](../ROADMAP.md) changes behavior by state. Observer connects to [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md).

## Governing Question

What fact should be observed, when does it become visible, who owns subscriber lifetime, and which ordering, failure, consistency, capacity, and authority guarantees can the mechanism actually support?

Observer replaces concrete dependent calls with a subscription protocol. The interface is small; the system consequences—especially when callbacks become queues or networks—are not.

## Why This Matters

User interfaces, caches, domain projections, monitoring, plugins, device views, and integration consumers all react to change. The subject should not depend on every display, metric, or extension.

Poor observer designs create invisible control flow, leaks, recursion, stale views, data exposure, and overload. Production designs distinguish local synchronous notification, asynchronous streams, and durable messaging because each has different evidence and failure semantics.

## Prerequisites and Retrieval

You should understand encapsulation, immutable values, transactions, callbacks, concurrency, queues, versioning, idempotency, authorization, and cache consistency. Retrieve these facts:

1. A notification sent before commit can report a state that later rolls back.
2. Calling unknown observer code while holding a subject lock risks deadlock and reentrancy.
3. Query-then-subscribe can miss a change between the two operations.
4. At-least-once delivery requires duplicate-safe consumers; it does not imply exactly-once effects.
5. A fast producer plus unbounded buffering converts slowness into memory exhaustion and stale work.
6. Possession of an event does not permanently authorize access to its current subject.

## Learning Objectives

After completing this module, you should be able to:

- derive Observer from one-to-many dependency inversion;
- design typed immutable event and subscription contracts;
- choose push, pull, invalidation, snapshot, and delta semantics;
- control dispatch order, reentrancy, callback mutation, and failures;
- close initial-state/subscription races and manage lifecycle;
- distinguish local callbacks, reactive streams, and durable events;
- design backpressure, duplicate/order/retry, security, and observability;
- test protocol laws, races, leaks, overload, replay, and recovery.

## Core Exposition

### Publish domain or presentation facts

Name occurrences precisely: `SelectionChanged`, `OrderAccepted`, or `CatalogPriceChanged`. Avoid `Updated` when consumers need to guess what and why. An event reports a fact; a command requests an action and can be rejected.

Do not use Observer to bypass an aggregate's command API. Observers may issue new commands, but those pass through current validation/authorization and create new transitions.

### Establish the visibility boundary

Build the notification from committed state. For a single in-memory object, update invariants before dispatch. For database state plus durable events, commit state and an outbox record atomically, then publish asynchronously.

Pre-commit notifications are occasionally valid for cancellable proposals, but name them as proposals, define veto/order/failure, and never let consumers mistake them for facts.

### Make events immutable and typed

Include stable event identity, source, type/schema version, subject/aggregate ID, subject version or ordering key, occurrence/record metadata as needed, and minimal owned payload. Do not hand observers a live mutable subject or caller-owned buffer.

An event may carry a full snapshot, a delta, keys to pull current state, or invalidation. Full snapshots simplify consumers but cost data and exposure; deltas require a correct base; pull can race and load the subject; invalidation tolerates coalescing but needs refresh policy.

### Define subscription activation

`subscribe()` should return a subscription/cancellation handle. Define duplicate registration, filters, priority/order if any, activation point, idempotent cancellation, cancellation during dispatch, and callback-after-cancel boundaries.

To combine initial state and updates, use an atomic `snapshotAndSubscribe`, a versioned snapshot then replay events strictly after its version, or subscribe first and buffer/deduplicate while loading. Plain query then subscribe has a lost-update window.

### Snapshot the observer list

Copy/freeze the active observer list before invoking callbacks. Then a cancellation during dispatch affects subsequent notifications, not which callbacks remain in the current snapshot; a new subscriber starts later. This avoids iterator invalidation and hidden order changes.

Snapshotting does not make callbacks thread-safe or immortal. Validate lifetime/cancellation at the chosen boundary and document whether a callback already queued may still run.

### Avoid subject locks around callbacks

Under ownership/lock, commit subject state, construct event and listener snapshot, then release before calling unknown code. Otherwise observers may block, re-enter, deadlock, or access partially restored invariants.

If exact coordination with unsubscribe is required, use generation tokens, serial executors, or reference-counted in-flight work rather than holding a broad state lock across arbitrary code.

### Specify order and failure

Common local policies are registration order, explicit priority, or unspecified order. Reliance on order couples observers; if B must run after A for correctness, model a workflow/mediator/chain instead of independent observers.

Choose exception behavior: isolate and report each failure, stop and return aggregate failure, or fail the transaction for a pre-commit proposal. Never silently catch. Record event/subscriber identity, bounded error, and retry ownership without exposing payload secrets.

### Bound reentrancy and feedback

Observer A may issue a command that causes another notification before the outer dispatch ends. Define immediate nested dispatch, queue-until-current-completes, or reject cycles. A serialized queue makes breadth-first ordering visible and avoids stack overflow.

Use causation/correlation IDs, subject versions, no-op suppression, deduplication, and hop/work limits. A global `notifying` flag that drops nested changes loses legitimate state transitions.

### Own lifecycle

Strong subject-to-observer references leak screens, plugins, tenants, or sessions unless explicitly cancelled. Weak references reduce retention but can make subscription disappear nondeterministically and do not release external resources.

Tie cancellation to lexical/component lifecycle, return explicit handles, make disposal idempotent, and measure live subscriptions. Clean up queued tasks, timers, network streams, and durable consumer leases too.

### Add asynchronous demand honestly

Moving callbacks to a thread pool changes ordering, concurrency, completion, and error observation. Define per-subscriber serial or parallel execution, queue capacity, overflow action, cancellation, shutdown, and whether the producer waits for acceptance.

For streams, demand/backpressure lets subscribers request bounded items. Policies such as block, reject, drop latest/oldest, sample, coalesce, or disconnect have different correctness. Never drop commands/audit facts merely because dropping UI refresh invalidations is acceptable.

### Design durable delivery separately

A brokered event needs serialization/schema evolution, transactional publication, identity, partition/order key, retention, consumer offsets, duplicate handling, retry/backoff/dead letter, poison-data remediation, replay, and lag/capacity operations.

At-least-once consumers store event identity or domain version with their state change transaction. Exactly-once broker processing labels do not automatically include external APIs. Reconcile indeterminate effects using stable provider identity.

### Protect consistency

Per-subject monotonically increasing versions let projections detect stale, duplicate, and gap cases. On a gap, fetch/rebuild a versioned snapshot or replay from durable history. Do not apply delta v12 to projection v9 as though v10–v11 did not matter.

Global order is rarely available or needed. Partition by the narrow entity whose transitions require order; cross-entity observers must tolerate interleaving or use a higher-level protocol.

### Secure publication and consumption

Authorize subscriptions and filters, constrain tenant/source/type, minimize payload, and avoid secrets in routable metadata. Authenticate transport/producers for durable events and validate size, depth, schema, identifiers, and provenance.

Consumers recheck current permission before sensitive pulls/actions; old events may outlive access. Logs/traces should use event IDs/types and redacted bounded fields. Retention, deletion, encryption, and key policy include broker backups and dead-letter storage.

### Operate for slow and failing observers

Measure publish/dispatch latency, subscriber latency/failure, queue depth/age, demand, drops/coalescing, live subscriptions, event lag, duplicates, gaps, retries, dead letters, replay rate, and outbox backlog. Set per-subscriber/tenant limits and circuit/isolation policies.

One optional analytics observer should not block the subject's critical transition. Conversely, a required invariant-maintaining action should not be modeled as an optional observer.

### Test the full protocol

Test zero/one/many and duplicate subscribers, ordering policy, event immutability, state-before-notify, subscribe/cancel during dispatch, cancel race, exception isolation, reentrant changes, no-op suppression, and collection/leak behavior.

For async/durable paths, test initial-snapshot races, queue overflow, slow/crashed subscribers, duplicate/reorder/gap, outbox crash windows, poison messages, replay, migration, authorization revocation, tenant isolation, redaction, partitions, restart, and load/soak.

## Definitions and Notation

Let subject states be (s_v) with monotonically increasing per-subject version (v). Committed action (a) yields $s_v\xrightarrow{a}s_{v+1}$ and event (e_{v+1}). Active observer set at dispatch start is (L_{v+1}=snapshot(L)).

For projection state (q=(v_q,data)), apply rule:

$$
v_e\le v_q\Rightarrow duplicate/stale;\quad
v_e=v_q+1\Rightarrow apply;\quad
v_e>v_q+1\Rightarrow gap/recover.
$$

This assumes contiguous per-subject versions and events for every relevant transition. If coalescing/invalidation is allowed, use a different explicitly stated rule.

For bounded queue capacity (B), safety requires $0\le |Q|\le B$; liveness needs a demand/service assumption or explicit overflow outcome. A bound alone does not guarantee delivery.

## Mechanisms, Invariants, or Proof Structure

### Observer design procedure

1. Name the fact/proposal, subject boundary, visibility/commit point, and consumers.
2. Define immutable typed/versioned event identity, order key, and minimal payload semantics.
3. Specify subscription activation, initial-state handshake, ownership, and cancellation.
4. Define listener snapshot, callback order, exception, reentrancy, and concurrency policy.
5. Choose push/pull/invalidation and gap/rebuild semantics.
6. For async/durable use, define capacity/demand, publication atomicity, duplicates, retry, replay, and lag.
7. Apply current authorization, tenant scope, minimization, redaction, retention, and quotas.
8. Test state laws, lifecycle/races, overload/faults, migrations, recovery, and security.

### Executable mechanism

This local catalog commits state/version first, creates an immutable tuple event, and iterates a tuple snapshot of subscribers. One subscriber cancels itself during version one. It does not model threads, failures, durability, authorization, or backpressure.

<!-- bijux-verify: {"id":"observer-snapshot-dispatch","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"audit=v1:book=12\nonce=v1:book=12\naudit=v2:book=15\ncounts audit=2 once=1 subscribers=1\n","stderr":""}} -->
```python
class Catalog:
    def __init__(self):
        self.prices = {}
        self.version = 0
        self.subscribers = []

    def subscribe(self, observer):
        if observer not in self.subscribers:
            self.subscribers.append(observer)

    def unsubscribe(self, observer):
        self.subscribers = [item for item in self.subscribers if item is not observer]

    def set_price(self, item, price):
        if self.prices.get(item) == price:
            return
        self.prices[item] = price
        self.version += 1
        event = (self.version, item, price)
        for observer in tuple(self.subscribers):
            observer.on_event(event)


class AuditObserver:
    def __init__(self, name):
        self.name = name
        self.events = []

    def on_event(self, event):
        version, item, price = event
        self.events.append(event)
        print(f"{self.name}=v{version}:{item}={price}")


class OnceObserver(AuditObserver):
    def __init__(self, name, catalog):
        self.name = name
        self.events = []
        self.catalog = catalog

    def on_event(self, event):
        super().on_event(event)
        self.catalog.unsubscribe(self)


catalog = Catalog()
audit = AuditObserver("audit")
once = OnceObserver("once", catalog)
catalog.subscribe(audit)
catalog.subscribe(once)
catalog.set_price("book", 12)
catalog.set_price("book", 15)
print(f"counts audit={len(audit.events)} once={len(once.events)} subscribers={len(catalog.subscribers)}")
```

### Local dispatch argument

Before callbacks, state and version are updated and event is an immutable tuple. The tuple listener snapshot contains both observers for version one, so self-cancellation cannot alter that traversal; the live list then contains only audit for version two. Thus audit receives versions one/two and once receives only one in registration order.

The argument assumes serialized calls, nonfailing callbacks, immutable scalar payloads, and no external mutation of public lists. It proves no cancellation race, exception isolation, thread safety, durability, or delivery effect.

### Evidence layers

Review local state/dispatch, lifecycle/reentrancy, asynchronous capacity, durable publication/delivery, consumer idempotency/gap recovery, and security/operations independently. An executable callback trace is evidence only for the first layer.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Direct call | Visible required control flow | Concrete coupling | One required stable dependent |
| Local Observer | Extensible in-process reactions | Hidden flow, lifetime/reentrancy | Optional cohesive local dependents |
| Mediator | Owns combined collaboration invariant | Central policy concentration | Participants require coordinated decisions |
| Pull polling | Consumer pace and failure isolation | Latency/load and missed transient facts | Fresh state matters more than every change |
| Reactive stream | Async demand/backpressure | Larger lifecycle/protocol | Continuous asynchronous data |
| Durable pub/sub | Replay, process decoupling | Delivery/schema/ops complexity | Facts cross process/time boundaries |
| Event log/sourcing | Authoritative ordered history | Replay/evolution/effect complexity | Complete change history is core |
| Cache invalidation | Compact/coalescible | Requires refresh; stale windows | Current value can be reread safely |

## Failure Modes and Misconceptions

- **“Observer decouples everything.”** It removes concrete publisher knowledge while retaining semantic/schema/timing coupling.
- **“Events are commands in past tense.”** Facts cannot demand success from every consumer.
- **“Notify means delivered.”** It may mean callback attempted, queued, broker-accepted, or persisted; name the milestone.
- **“Registration order is harmless.”** Correctness dependence on it signals hidden workflow coupling.
- **“Weak references solve lifecycle.”** They do not cancel queued work or external resources and create nondeterministic disappearance.
- **“Async is the same behavior on another thread.”** It changes order, concurrency, failure, completion, and capacity.
- **“Unbounded queues avoid drops.”** They defer overload into memory failure and obsolete lag.
- **“At-least-once plus dedupe is exactly once.”** External effects and retention windows remain outside the claim.
- **“Pull after notification returns that version.”** Concurrent changes may return newer state unless versioned snapshot semantics exist.
- **“Event access equals action authority.”** Consumers recheck current authorization at protected actions/resources.
- **“Replay is safe.”** Side effects must be suppressed, idempotent, or reconciled.
- **“Observer tests prove cache coherence.”** Gap, ordering, invalidation, partition, and rebuild evidence remains.

## Worked Examples

### Example 1

No observers are registered, so a subject transition still commits correctly. Notification infrastructure must not be required for the subject's own invariant. **Conclusion:** Observers are dependents, not hidden owners of essential state.

### Example 2

An observer unsubscribes during dispatch. Snapshot semantics let it finish the current event and exclude it from the next, producing deterministic counts. **Conclusion:** Mutation-during-notification needs an explicit boundary.

### Example 3

A subject notifies while holding a lock; observer queries the subject and deadlocks. Commit/snapshot under lock and invoke after release. **Conclusion:** Do not call unknown observers while holding subject locks.

### Example 4

Client queries snapshot v10, update v11 commits, then client subscribes; it never sees v11. Atomic snapshot-and-subscribe or replay `>10` closes the gap. **Conclusion:** Initial state and subscription need one versioned handshake.

### Example 5

Projection at v9 receives v12. Applying the delta corrupts state; detecting the gap and rebuilding/replaying v10–v12 preserves its model. **Conclusion:** Versions turn silent omission into recoverable evidence.

### Example 6

A UI invalidation producer emits 10,000 changes/second while display renders 60 frames/second. Coalescing to latest invalidation is valid; dropping audit facts would not be. **Conclusion:** Overflow policy follows message semantics.

### Example 7

State commits but process crashes before broker publication. An outbox row committed with state and retried later closes that loss window, while duplicate publication remains. **Conclusion:** Durable Observer requires transactional publication and idempotent consumers.

### Example 8

A duplicate event repeats a payment-provider call after a lost response. Local event dedupe cannot determine provider outcome; stable provider identity and reconciliation are needed. **Conclusion:** Exactly-once external effects do not follow from event IDs alone.

### Example 9

A tenant-wide event includes personal data for convenience. Subject/type filtering and encryption do not repair over-disclosure to legitimate subscribers; minimize payload and authorize scope. **Conclusion:** Pub/sub fan-out magnifies data exposure.

### Example 10

A patient-monitor observer displays an alert after a delayed queue but lacks freshness, alarm-priority, fail-safe, human workflow, and validated clinical thresholds. **Conclusion:** Notification delivery is not clinical safety evidence.

## Cross-Program Connections

- **Object-Oriented Programming:** interfaces, callbacks, ownership, weak/strong references, and variance shape local Observer.
- **Software Design and Domain Modeling:** domain events, aggregate commit boundaries, application commands, and projections locate meaning.
- **Concurrency and Parallelism:** locks, reentrancy, serial executors, queues, atomics, and memory visibility constrain dispatch.
- **Distributed Systems Engineering:** logs, brokers, ordering, duplicates, partitions, replay, and partial failure govern remote observers.
- **API Engineering:** webhooks, streams, subscription resources, schemas, signatures, retries, and cursor recovery expose events.
- **Database Engineering:** transactions, outboxes, change-data capture, versions, and materialized views align facts and state.
- **Cloud and Platform Engineering:** backpressure, quotas, lag, dead letters, autoscaling, and observability operate fan-out.
- **Security Engineering:** producer trust, subscription authorization, tenant isolation, minimization, and retention protect data.
- **Testing and Quality:** model/race/fault/load/leak tests and replay fixtures provide layered evidence.
- **Systems Engineering:** alarms and control notifications require timing, hazard, human-factors, and independent safety evidence.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Observer intent, structure, applicability, and consequences.
2. Frank Buschmann et al., *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996, ISBN 978-0-471-95869-7. Provides event-driven architectural pattern foundations and trade-offs.
3. WHATWG, [DOM Standard: Events and `EventTarget`](https://dom.spec.whatwg.org/#interface-eventtarget), Living Standard updated 2026-08-25, accessed 2026-08-28. Defines listener registration/removal, dispatch paths, cancellation, and mutation-observer mechanisms for the web platform.
4. Reactive Streams, [Reactive Streams specification](https://www.reactive-streams.org/), version 1.0.4, accessed 2026-08-28. Defines asynchronous stream processing with non-blocking demand and terminal/cancellation protocol scope.
5. Gregor Hohpe and Bobby Woolf, [Publish-Subscribe Channel](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html), *Enterprise Integration Patterns*, 2003. Distinguishes integration pub/sub fan-out and delivery topology.
6. Cloud Native Computing Foundation, [CloudEvents specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), version 1.0.2, 2022. Defines portable event context, source/ID duplicate identity, type/schema-related metadata, size, and privacy/security considerations.
7. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides durable foundations for logs, messaging, ordering, stream processing, and distributed failure.
8. Michael T. Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018, ISBN 978-1-68050-239-8. Provides stability, backpressure, timeout, circuit, capacity, and production-operations guidance.

## Exercises

### Exercise 1

Trace the executable dispatch and prove its listener-snapshot outcome under stated assumptions.

### Exercise 2

Design a race-free initial snapshot plus subscription protocol for a versioned projection.

### Exercise 3

Specify a bounded asynchronous local Observer with failure, cancellation, reentrancy, and overflow semantics.

### Exercise 4

Design durable events for updating a cache and audit projection after a database commit, comparing their delivery needs.

### Exercise 5

Review an unfamiliar safety-critical alarm Observer without claiming safety or clinical/industrial validity.

## Answers to the Exercises

### Answer 1

Both observers are registered before version one. `set_price` writes price 12, increments version to one, constructs `(1,"book",12)`, and snapshots both observers. Audit receives it first. Once receives it second and removes itself from the live list, but the tuple snapshot is unchanged. Version two writes 15 and snapshots only audit, which receives `(2,"book",15)`. Counts are audit two, once one, live subscribers one.

This proves registration-order behavior for one serialized, nonfailing run with tuple snapshot and immutable scalar event fields. It does not prove thread safety, callback-after-cancel races, exception isolation, encapsulation of the public list, durability, authorization, or downstream effect delivery.

### Answer 2

Option one is a storage API that atomically registers a durable subscription at position (p) and returns snapshot at the same (p); consume events strictly after (p). Option two reads a versioned snapshot (v), then attaches to a retained log and requests every event with subject version (>v); the log retention must cover the handshake. Option three subscribes first, buffers versioned events, reads snapshot (v), discards buffered versions (le v), applies contiguous versions after (v), then enters live mode.

Define per-subject version/order, duplicate/stale/gap behavior, snapshot identity, retention/expiry, authorization at both operations, buffer bound/overflow, and restart cursor. Test commits before/during/after each handshake step, duplicate/reorder/gap, snapshot failure, buffer overflow, reconnect, retention loss, authorization revocation, and schema migration. A timestamp alone is insufficient unless it defines the same total commit order.

### Answer 3

Give each subscription a bounded serial queue of immutable typed events, capacity (B), demand or worker ownership, generation token, and idempotent cancellation. Subject commit snapshots subscription handles and attempts nonblocking enqueue outside the state lock. Preserve per-subscription order; invoke only one callback at a time; nested subject changes enqueue behind current dispatch. Cancellation marks generation closed, rejects future enqueue, and defines whether already-running callback completes while queued items are discarded/drained.

Select overflow by semantics: coalesce latest keyed invalidation, sample telemetry, reject producer work, or disconnect/flag lag; never silently drop required facts. Isolate callback exceptions, record bounded failure, and apply explicit retry/quarantine only for safe observers. Bound callback time/work, queue bytes/items, subscriptions/tenant, and shutdown drain. Tests cover zero/full boundaries, slow/crashed/reentrant observer, cancel/enqueue race, duplicate subscription, exception, order, overflow policy, starvation, shutdown, and leak/soak.

### Answer 4

Commit domain state and an outbox event with source/type/schema, aggregate ID/version, event ID, minimal change/invalidation, and correlation in one database transaction. A publisher retries outbox delivery; consumers expect duplicates and partition/order by aggregate when needed. The cache consumer may treat events as coalescible invalidations: on any version above cached version, evict/refetch authoritative state; gaps can be harmless if refresh obtains current version. Its priority is bounded staleness and overload-safe coalescing.

The audit projection must not drop/coalesce required facts. It transactionally records event ID/source and ordered projection change, detects gaps, pauses/replays/rebuilds, retains provenance, and alerts/quarantines poison data. Both validate schema/tenant/source and redact operations, but retention/access differ. Test crash before/after state/outbox/publish/ack, duplicate/reorder/gap, cache stampede, audit poison, replay, migration, lag/overflow, authorization scope, and recovery. Neither consumer should perform unreconciled non-idempotent external effects during replay.

### Answer 5

Define hazard/clinical purpose, source sensors and calibration/provenance, thresholds/rules and authority, freshness/timing/priority, alarm states, acknowledgement/escalation, suppression/inhibition, degraded/fail-safe behavior, human workflow, and independent protective controls. Model end-to-end state and timing from measurement through display/actuation; a callback receipt is not the safety outcome. Authenticate sources/operators, authorize configuration/action, protect integrity, bound queues, detect loss/gaps/staleness, and make overload visible.

Evidence requires hazard/risk analysis, requirements traceability, independent threshold/domain review, formal state/timing/invariant analysis where tractable, calibrated reference cases, simulator/hardware-in-loop tests, duplicate/reorder/loss/delay/partition/clock/overload/failure injection, cybersecurity/privacy assessment, usability/human-factors trials, alarm-fatigue and operational drills, maintenance/configuration/version validation, and controlled release/rollback. Named domain/clinical or controls experts, safety, software verification, cybersecurity, human factors, quality/regulatory, and operations reviewers approve. Observer structure and ordinary delivery tests establish no safety integrity, clinical validity, or regulatory conformity.
