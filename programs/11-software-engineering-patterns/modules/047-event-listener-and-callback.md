---
module_id: SEPAT-047
program: Software Engineering: Patterns
level: 1
module_number: 47
title: Event Listener and Callback
status: complete
last_verified: 2026-08-28
---

# Event Listener and Callback

## One-Page Review

### Governing question

How can a source notify zero or more interested collaborators without knowing their concrete behavior, while subscription ownership, delivery order, mutation during dispatch, reentrancy, threading, failures, backpressure, security, and durability remain explicit?

### Essential definitions

- An **event** is an immutable fact/notification that something occurred, with a stable type and bounded payload.
- A **listener** is an object or function registered to receive a class of events.
- A **callback** is executable behavior passed for later invocation under a declared call contract.
- A **subscription** is the lifecycle relationship between source, event type, callback, and cancellation/cleanup handle.
- **dispatch** is one source invocation of the current eligible listener set.
- **snapshot semantics** freezes the listener set for one dispatch; mutations affect subsequent dispatches.
- **reentrancy** occurs when a callback synchronously calls back into the source or triggers nested dispatch.
- **failure policy** defines whether one listener error stops, aggregates, isolates, retries, or escalates dispatch.
- **backpressure** lets a consumer bound or signal how much asynchronous work it can accept.
- **durable event delivery** persists event/subscription progress across process failure; an in-memory callback normally does not.

### Central model, mechanism, or theorem

For source state (q), event (e), and registration-ordered snapshot (L_e=(\ell_1,...,\ell_n)), synchronous dispatch is a trace

\[
D(q,e,L_e)=invoke(\ell_1,e);\ldots;invoke(\ell_n,e).
\]

This model is deterministic only if listener selection/order, mutation snapshot, callback effects, and failure/reentrancy rules are fixed. Successful return proves at most that the declared callbacks completed under this process; it does not prove durable receipt, exactly-once external effects, or eventual processing.

### Critical invariants

- Event schema, source identity, ordering scope, mutability, sensitivity, and lifetime are explicit.
- Registration returns an idempotent cleanup handle owned by a bounded lifecycle; listeners cannot leak indefinitely.
- Dispatch defines listener order and whether attach/detach during dispatch affects the current snapshot.
- Thread/executor, serialization, reentrancy, cancellation, and callback duration/blocking contracts are documented.
- One listener's failure follows a declared policy and cannot silently corrupt source state or masquerade as successful delivery.
- Async queues have capacity, overflow, fairness, shutdown, and backpressure rules; slow consumers cannot grow memory without bound.
- Callbacks receive least-authority immutable views, and untrusted code cannot register arbitrary executable behavior.
- In-process notification is never described as durable, exactly-once, transactional, or cross-service delivery without matching evidence.

### Common failures

Common failures include anonymous callbacks that cannot be unsubscribed, strong references retaining screens/tenants, duplicate registration, unspecified order, iterating a live collection while it mutates, deadlock from invoking under a lock, recursive event storms, listener exceptions aborting unrelated callbacks, swallowing errors, blocking I/O on a UI/event-loop thread, unbounded async tasks/queues, stale callbacks after owner disposal, payload mutation between listeners, secrets in event data, trusting remote callback endpoints, lost notifications on crash, and calling “exactly once” after one successful local run.

### Compact example

An event source returns stable subscription tokens and dispatches over a registration-ordered snapshot. The first listener unsubscribes itself while handling event A; both snapshot members receive A, but only the second receives B.

### Connections

[SEPAT-046](046-double-dispatch.md) selects pair-specific behavior; [SEPAT-048](../ROADMAP.md) encapsulates changeable decisions. Event listeners connect to [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

Which occurrence should be announced, to which bounded audience, on what execution and ordering model, with what ownership and failure semantics—and does the requirement actually need an in-memory callback, a backpressured stream, or durable messaging?

Listeners reduce direct coupling between a source and optional reactions. They do not remove temporal coupling: callbacks still run according to a lifecycle, thread, timing, and failure contract that every participant must honor.

## Why This Matters

User interfaces, domain objects, frameworks, device APIs, caches, metrics, and plugin systems frequently need one-to-many notification. A listener lets the source publish a stable occurrence while consumers evolve independently.

Without precise semantics, the pattern becomes a hidden call graph. A harmless-looking `emit` can block, recurse, mutate source state, retain an entire object graph, leak data, or lose business-critical work at process failure.

## Prerequisites and Retrieval

You should understand function values, Observer, ownership/lifetime, exceptions/results, threads/event loops, queues, transactions, and distributed delivery. Retrieve these facts:

1. A function reference may strongly retain its captured object graph.
2. Iterating a collection while callbacks mutate it needs a specified snapshot or mutation algorithm.
3. Invoking user code while holding an internal lock can deadlock or violate invariants.
4. Asynchronous execution changes ordering, failure propagation, cancellation, and memory use.
5. “At most once,” “at least once,” and “exactly once effect” are different claims.
6. An event payload can be an information-disclosure and capability surface.

## Learning Objectives

After completing this module, you should be able to:

- distinguish event, listener, callback, subscription, observer, stream, and durable message;
- define subscription identity, ownership, idempotent cleanup, and retention behavior;
- choose dispatch snapshot, ordering, reentrancy, and failure semantics;
- design safe synchronous and bounded asynchronous execution;
- separate notification from transactional/durable workflow obligations;
- constrain payloads, callback authority, plugin/remote registration, and observability;
- test lifecycle, mutation, nested dispatch, concurrency, backpressure, shutdown, and faults;
- limit delivery and high-stakes correctness claims to demonstrated evidence.

## Core Exposition

### Name an occurrence, not an instruction

Prefer past-tense facts such as `OrderAccepted` or state-specific notifications such as `SelectionChanged`. `SendInvoiceNow` is a command and needs one accountable handler/result; broadcasting it obscures ownership.

Define source/aggregate identity, event ID if meaningful, occurrence time source, sequence/version, schema version, and bounded payload. Do not include entire mutable domain objects merely for convenience.

### Define callback signature

Specify input view, return value, error model, allowed blocking/effects, deadline/cancellation, thread/executor, reentrancy, and lifetime. A `void callback(Event)` signature alone does not answer these questions.

If listener results affect the source decision, this may be a chain of responsibility, validation pipeline, policy query, or command aggregation—not a notification event.

### Return a subscription handle

Registration should return a stable token/disposable/abort handle so ownership is explicit and cleanup is idempotent. Tie it to component/request/session scope using structured resource management where the language supports it.

Removing by re-creating an “equal” anonymous lambda often fails because callback identity differs. The handle avoids callers reconstructing internal keys/options.

### Decide reference strength

Strong listener references keep callbacks/captured owners alive until unsubscribe/source disposal. This is appropriate when subscription owns participation but leaks if lifecycle cleanup is missed.

Weak listeners avoid some retention but can disappear nondeterministically and hide ownership errors. Prefer explicit lifecycle; use weak references only with defined collection timing and tests.

### Prevent duplicate ambiguity

Define whether the same callback/event/options tuple is deduplicated, reference-counted, or registered multiple times with separate handles. DOM prevents duplicate listeners for equal type/callback/capture, while other APIs differ.

Do not infer portability across frameworks. Record subscription identity and make idempotent attach behavior intentional.

### Snapshot dispatch membership

Copy/freeze the eligible listener entries at dispatch start, then invoke outside the registry lock. Under snapshot semantics, unsubscribe during A affects the next event but not remaining membership for A; subscribe during A starts with the next event.

Alternative live semantics are possible but must define index movement, skip/repeat behavior, and concurrency. Snapshot cost is (O(n)) references and provides a simpler invariant.

### Specify ordering

Synchronous emitters often invoke in registration order, but do not assume this without a contract. Priority ordering needs stable tie-breaking; parallel listeners cannot promise completion order.

Define ordering scope: per source, event type, key/entity, subscription, or globally. Global order across threads/processes is expensive and rarely implied by a listener API.

### Keep locks away from callbacks

Lock only to update/read registry and create the snapshot; release before invoking callbacks. Listener code may subscribe, unsubscribe, acquire other locks, or call source operations.

If source state must be observed consistently, pass an immutable/versioned snapshot. Do not hold a source mutation lock across untrusted callback execution.

### Define reentrancy

A listener can synchronously emit the same or another event. Choose: allow nested depth-first dispatch, queue nested events until current completion, reject reentrancy, or coalesce by key. Bound depth/work in every design.

Guard flags without `finally`/structured cleanup can permanently block dispatch after failure. Event cycles across sources require correlation/path/depth budgets or architectural decoupling.

### Choose failure policy

Options include fail-fast, continue-and-aggregate, isolate/log, or route errors to an explicit supervisor. Select by contract: validation callbacks may fail-fast; optional telemetry listeners may isolate; mandatory local participants may aggregate and make the publisher fail.

Never both swallow and report success. Do not recursively emit error events through the same broken path without bounds. Preserve callback identity/event correlation while redacting sensitive data.

### Keep synchronous work bounded

Synchronous callbacks run on the publisher's thread and contribute directly to latency. Event-loop/UI callbacks must not block on file/network/database work. Budget listener count and duration, instrument slow callbacks carefully, and define whether timeouts are enforceable.

A timeout cannot safely kill arbitrary in-process code in many runtimes. Isolation may require a worker/process boundary rather than a timer around a callback.

### Design asynchronous dispatch explicitly

Submitting each event/listener to an executor changes order and failures and can create unbounded tasks. Define queue capacity, per-key serialization, concurrency limit, overflow policy (reject/drop/coalesce/block), fairness, retry, cancellation, and shutdown drain/abort.

Backpressure is a protocol, not merely logging queue depth. Reactive Streams lets subscribers signal demand; use a tested streaming abstraction when sustained producer/consumer rate mismatch matters.

### Preserve payload immutability and privacy

Create immutable event values or per-listener read-only snapshots. One listener must not modify payload seen by later listeners. For large data, use bounded references with explicit lifetime/authorization rather than mutable shared buffers.

Apply data minimization and audience filtering. Metrics/debug representations must not expose tokens, personal data, medical facts, or hidden entity existence.

### Restrict untrusted callbacks

In-process callbacks are code execution with the host process's ambient capabilities. Do not load/register untrusted code based only on an event interface. Use signed/allowlisted plugins, sandbox/process boundaries, narrow capabilities, resource limits, and version negotiation.

Remote “callbacks” are outbound endpoints/webhooks and require URL/tenant allowlists, SSRF defenses, authentication/signatures, replay protection, timeouts, retries, idempotency, delivery records, and privacy controls.

### Separate local notification from durability

If a business action must survive crashes, persist source state and an outbox/event record atomically, then deliver through a durable broker/worker with idempotent consumers and observable retries/dead letters. An in-memory listener can update ephemeral UI/cache/metrics after commit but cannot be the only durable obligation.

Do not publish a durable event before transaction commit or claim atomic database-plus-callback effects. The outbox closes the persistence gap, not every downstream exactly-once effect.

### Design shutdown and disposal

Source disposal prevents new registration/emission, atomically closes subscriptions, cancels/finishes queued work according to policy, and releases captured objects/executors. Concurrent unsubscribe/emit/dispose needs linearizable or documented weaker semantics.

Late callbacks after owner shutdown must be impossible or harmless through generation tokens/cancellation. Tests should detect retained listeners and work after disposal.

### Observe without creating storms

Track bounded counts: active subscriptions by stable type, emits, listener failures, slow callbacks, queue depth/capacity, drops/coalesces, and shutdown backlog. Avoid listener IDs, user IDs, URLs, or raw event types from untrusted input as unbounded metric labels.

Sampling/tracing must not alter order or recursively emit through the same source. Establish a separate emergency error path for dispatcher failure.

### Test temporal behavior

Test zero/one/many/duplicate listeners, exact ordering, self/other unsubscribe, subscribe during dispatch, nested same/different events, listener throw/timeout/block, source mutation, concurrent emit/cleanup/dispose, payload mutation attempts, queue saturation, fairness, cancellation, shutdown, memory retention, and version skew.

Use deterministic schedulers/fakes for async ordering and model-based transition tests for lifecycle. Stress tests find races but do not prove absence; pair them with ownership and synchronization reasoning.

## Definitions and Notation

Let registry at time (t) be (R_t), eligible registration-ordered snapshot for event (e) be (L_e=snapshot(R_t,e)), and invocation outcome for listener (\ell_i) be (o_i\in\{ok,failed,cancelled,skipped\}).

Under snapshot semantics, registry mutation during dispatch produces (R_{t+1}) but leaves (L_e) unchanged. For a bounded async queue with capacity (K), invariant is

\[
0\le queued(t)\le K,
\]

and every enqueue at capacity follows the declared block/reject/drop/coalesce rule rather than allocating without bound.

## Mechanisms, Invariants, or Proof Structure

### Listener design procedure

1. Define immutable event fact/schema, audience, identity/version/order, sensitivity, and durability need.
2. Specify callback result/error, executor, blocking, reentrancy, cancellation, and authority contract.
3. Return an idempotent subscription handle with explicit owner/source disposal lifecycle.
4. Define duplicate, registration order, snapshot mutation, nested dispatch, and failure policy.
5. Invoke outside locks and bound listener count, work, recursion, queues, and metrics.
6. Separate local ephemeral notification from durable transactional outbox/messaging.
7. Secure plugin/remote callbacks and minimize payload/capabilities.
8. Test lifecycle interleavings, errors, saturation, shutdown, retention, compatibility, and effects.

### Executable finite model

The following synchronous source uses stable numeric tokens and registration-ordered snapshots. The first listener unsubscribes itself during A. It demonstrates current-versus-next dispatch membership only—not concurrency, exception isolation, durability, backpressure, or effect safety.

<!-- bijux-verify: {"id":"listener-snapshot","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"A=first:A,second:A\nB=second:B listeners=1\n","stderr":""}} -->
```python
class EventSource:
    def __init__(self):
        self.listeners = {}
        self.next_token = 1

    def subscribe(self, callback):
        token = self.next_token
        self.next_token += 1
        self.listeners[token] = callback
        return token

    def unsubscribe(self, token):
        if token not in self.listeners:
            return False
        del self.listeners[token]
        return True

    def emit(self, event):
        snapshot = tuple(self.listeners.items())
        for token, callback in snapshot:
            callback(event)


source = EventSource()
seen = []
first_token = {"value": 0}


def first(event):
    seen.append("first:" + event)
    source.unsubscribe(first_token["value"])


def second(event):
    seen.append("second:" + event)


first_token["value"] = source.subscribe(first)
source.subscribe(second)
source.emit("A")
print("A=" + ",".join(seen))
seen.clear()
source.emit("B")
print("B=" + ",".join(seen) + " listeners=" + str(len(source.listeners)))
```

The snapshot contains both callbacks for A before the first unsubscribes. Registry state then contains only the second listener, so B reaches one callback. A production API would hide the registry and return an idempotent subscription object rather than a bare token.

## Alternatives and Trade-Offs

- **Direct call:** strongest clarity and result ownership for one required collaborator.
- **Observer object:** often synonymous structural family; may couple subject/observer state synchronization more explicitly.
- **Signal/slot:** framework-supported typed many-to-many callbacks with framework-specific thread/lifetime rules.
- **Reactive stream:** adds composition, terminal/error signals, demand/backpressure, and cancellation; greater semantic/tooling weight.
- **In-process event bus:** central routing reduces direct references but can hide dependencies and broaden failure/data scope.
- **Domain event plus outbox/broker:** durable cross-boundary processing with retries/idempotency; operational complexity is real.
- **Command/queue:** one accountable action handler and result/lifecycle; better when occurrence is actually an instruction.
- **Polling/change feed:** consumer-controlled pace and recovery; adds latency and cursor/storage semantics.

Choose by ownership, latency, rate mismatch, failure boundary, and durability—not by a generic desire for “decoupling.”

## Failure Modes and Misconceptions

- **“Callbacks are decoupled.”** They retain temporal, schema, execution, and failure coupling.
- **“Unsubscribe is optional with garbage collection.”** Source-to-listener references can keep whole owners alive.
- **“Async means non-blocking.”** Queue submission can block, and workers can saturate without backpressure.
- **“Order is registration order everywhere.”** Framework, executor, and distributed boundaries differ.
- **“Snapshot solves concurrency.”** It clarifies membership for one emit; registry synchronization/disposal still need design.
- **“Catching exceptions makes delivery successful.”** Failure must be reported, supervised, retried, or explicitly isolated.
- **“One callback per event is exactly once.”** Crash/retry/external effects invalidate that claim.
- **“Weak listeners fix leaks.”** They replace explicit ownership with nondeterministic disappearance.
- **“Event payloads are internal.”** Plugins, logs, metrics, and remote endpoints can expose them.
- **“Tests prove timing.”** Deterministic traces plus concurrency reasoning and stress evidence are still scoped.

## Worked Examples

### Example 1

A dialog registers a closure capturing itself every open and never cleans up. The long-lived source retains all dialogs. **Conclusion:** Subscription ownership is memory ownership.

### Example 2

Listener A unsubscribes B while iterating a snapshot. B still receives the current event but not the next. **Conclusion:** Mutation semantics must be contractual.

### Example 3

A callback emits the same event recursively until stack overflow. A queued nested-dispatch policy with work bound stops the storm. **Conclusion:** Reentrancy needs an explicit bounded model.

### Example 4

Publisher holds registry lock while a listener unsubscribes and waits on the same lock. Snapshot-under-lock/invoke-after-unlock removes the deadlock. **Conclusion:** Never invoke external code under internal locks.

### Example 5

One listener throws before two mandatory listeners run. Continue-and-aggregate reports all three outcomes. **Conclusion:** Failure policy determines delivery semantics.

### Example 6

An event loop listener performs a 2-second network call and freezes UI. It instead emits a bounded work request to an owned worker. **Conclusion:** Publisher thread is part of callback contract.

### Example 7

Producer emits 100,000 updates/s to a slow consumer and creates one task each. A capacity-1 latest-value coalescing policy bounds memory. **Conclusion:** Overflow semantics follow domain meaning.

### Example 8

An untrusted webhook URL targets cloud metadata. Endpoint allowlists, DNS/IP validation, egress controls, signing, and delivery records prevent naive callback SSRF. **Conclusion:** Remote callbacks are security protocols.

### Example 9

An in-memory listener sends a receipt after database mutation, but the process crashes between them. Transactional outbox makes the durable obligation recoverable. **Conclusion:** Local callbacks are not durable messaging.

### Example 10

A medical alarm callback returns successfully in a simulation but actual device/network/operator paths are untested. **Conclusion:** Callback success is not end-to-end safety evidence.

## Cross-Program Connections

- **Object-Oriented Programming:** function objects, interfaces, ownership, weak/strong references, and encapsulation shape listeners.
- **Functional Programming:** higher-order functions, immutable events, effects, and stream combinators model callbacks.
- **Concurrency Engineering:** threads, executors, locks, reentrancy, cancellation, queues, and backpressure govern execution.
- **Distributed Systems:** brokers, outbox, delivery guarantees, retries, idempotency, ordering, and partitions govern durability.
- **API Engineering:** webhooks, schemas, versioning, authentication/signatures, replay, and compatibility expose callbacks remotely.
- **Security Engineering:** least authority, sandboxing, SSRF, secrets, tenant isolation, and data minimization constrain listeners.
- **Performance Engineering:** listener cardinality, latency budgets, queue capacity, allocation, and slow-consumer behavior matter.
- **Testing and Quality Engineering:** lifecycle models, deterministic schedulers, faults, stress, mutation, and retention tests provide evidence.
- **Cloud and Platform Engineering:** event loops, workers, shutdown, health, metrics, and broker operations own runtime behavior.
- **Safety and High-Assurance Engineering:** alarms/interlocks require independent end-to-end timing, failure, and human-response evidence.

## References

1. Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Defines Observer and related callback collaboration foundations.
2. WHATWG, [DOM Living Standard, §2 Events and EventTarget](https://dom.spec.whatwg.org/#events), updated 2026-08-25, accessed 2026-08-28. Defines event listener lists, registration/removal, once, signal, and dispatch semantics.
3. Node.js Project, [Events documentation](https://nodejs.org/api/events.html), Node.js 26.8.1, accessed 2026-08-28. Documents EventEmitter/EventTarget order, synchronous invocation, async interactions, and error behavior.
4. Reactive Streams, [Specification and JVM interfaces](https://www.reactive-streams.org/), version 1.0.4, accessed 2026-08-28. Defines asynchronous stream interoperability with non-blocking backpressure.
5. Brian Goetz et al., *Java Concurrency in Practice*, Addison-Wesley, 2006, ISBN 978-0-321-34960-6. Provides publication, locking, cancellation, executor, and callback safety foundations.
6. Herb Sutter, [“Prefer Using Futures or Callbacks to Communicate Concurrently”](https://herbsutter.com/2010/09/24/effective-concurrency-prefer-using-futures-or-callbacks-to-communicate-concurrently/), 2010. Discusses callback/future concurrent communication trade-offs.
7. Chris Richardson, [Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html), accessed 2026-08-28. Describes atomic persistence of state and messages without distributed transactions.
8. OWASP Foundation, [Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), accessed 2026-08-28. Provides controls relevant to untrusted remote callback/webhook destinations.

## Exercises

### Exercise 1

Trace the executable snapshot example and state exactly which lifecycle, ordering, concurrency, and delivery claims it does and does not establish.

### Exercise 2

Design a synchronous listener API with explicit subscription, snapshot, reentrancy, and failure semantics.

### Exercise 3

Design a bounded asynchronous latest-state notification path and contrast it with a lossless business-event stream.

### Exercise 4

Plan migration from an in-memory business-critical callback to transactional outbox and durable consumers.

### Exercise 5

Review a listener-based high-stakes alarm path without claiming safety or regulatory suitability.

## Answers to the Exercises

### Answer 1

Two callbacks are registered with tokens 1 and 2. `emit("A")` snapshots both. First appends `first:A` and deletes token 1 from the live registry; snapshot still contains second, which appends `second:A`. After clearing observations, `emit("B")` snapshots only token 2, appends `second:B`, and registry count is one.

This establishes one single-threaded registration order, start-of-dispatch snapshot membership, self-unsubscribe effect on the next event, and exact output. It does not establish idempotent cleanup, duplicate policy, exception handling, nested dispatch, locking/concurrency/disposal, payload immutability, memory retention, async capacity/backpressure, effects, durability, or exactly-once processing.

### Answer 2

Define `subscribe(event_type, listener, owner_scope)->Subscription`, where `Subscription.close()` is thread-safe/idempotent and source disposal closes all. Immutable event includes stable type/schema/source/version/correlation and bounded audience-filtered data. Register deduplicates exact `(type,listener,options)` or documents separate handles. Emit locks only to validate source and capture registration-ordered snapshot, then unlocks.

Choose queued nested dispatch with FIFO per source and depth/work budget. During current dispatch, attach/detach affects only future snapshots. Each callback receives the publisher thread, must be nonblocking/bounded, and returns `ok` or typed failure; dispatcher continues and aggregates mandatory listener failures, isolates explicitly optional telemetry, and reports through a nonrecursive supervisor. Define source-state snapshot, cancellation/disposal, concurrent linearization points, slow-callback metrics, sensitive diagnostics, and tests for every lifecycle/reentrancy/failure interleaving.

### Answer 3

For a UI sensor display needing only newest state, use one bounded slot per sensor/key. Producer atomically replaces pending value and increments a bounded coalesced counter; one worker drains latest snapshots at a configured rate. Capacity is one/key with bounded key cardinality/expiry, fairness, generation token, cancellation, and shutdown policy. Dropped intermediate states are explicitly acceptable; sequence/version reveals skipped updates.

For payments/audit/order events, coalescing is invalid. Persist each event atomically with source state, use durable ordered partitions/cursors, bounded consumer demand/concurrency, retry/backoff/dead-letter/reconciliation, idempotent effect keys, retention, and lag health. Backpressure may slow intake or shed upstream traffic according to policy, but it must not silently delete committed obligations. Test saturation, hot keys, fairness, crash/restart, duplicates, gaps/order, poison events, schema skew, and recovery.

### Answer 4

Inventory the callback's business obligation, transaction point, payload/schema, ordering key, effects, retries, error handling, consumers, privacy/retention, and current loss/duplication windows. Define stable event ID, aggregate/version/sequence, occurred time, schema, minimal data/reference, and consumer idempotency key. In the source database transaction update state and insert outbox record; a relay leases/publishes, records progress, retries, and exposes lag/failure.

Deploy consumers idempotently with inbox/effect deduplication or naturally idempotent conditional writes; handle duplicates, ordering, poison/dead-letter, replay, schema compatibility, authorization/tenant, deletion/retention, and reconciliation. Shadow/dual-observe without applying duplicate effects, compare counts/IDs/outcomes, then switch authoritative path behind a controlled flag. Fault-inject crashes before/after commit/publish/consume/effect, broker outage, duplicates, reorder, and version skew; retain rollback and drain/reconcile plan before removing callback.

### Answer 5

Define hazard, trigger source, thresholds/hysteresis, event timing/ordering, recipients/channels, acknowledgement/escalation, safe state/interlock independence, power/network/process failure, human workflow, maintenance suppression, cybersecurity, audit/retention, and exact claim. Distinguish alarm generated, dispatched, delivered, presented, perceived, acknowledged, and acted upon; one callback return proves only a local stage.

Evidence requires requirements/hazard traceability, independent domain/controls/safety review, worst-case timing and capacity analysis, sensor/threshold and false-positive/negative validation, fault injection across process/network/power/device/channel, redundancy/common-cause review, alarm-flood/human-factors/usability drills, cybersecurity and access/configuration tests, end-to-end site trials, monitoring/proof tests/maintenance, incident/rollback, and applicable quality/regulatory records. Named domain/clinical/controls, safety, verification, security, human-factors, quality/regulatory, and operations reviewers approve. Listener tests alone establish no functional safety or regulatory fitness.
