---
module_id: SEPAT-076
program: Software Engineering: Patterns
level: 2
module_number: 76
title: Active Object
status: complete
last_verified: 2026-08-29
---

# Active Object

## One-Page Review

### Governing question

How can concurrent clients invoke object-like operations without executing them in their own threads, while a scheduler serializes servant state, evaluates guards, bounds pending requests, returns truthful futures, and preserves ordering, cancellation, authority, and shutdown semantics?

### Essential definitions

- An **Active Object** decouples method invocation from method execution and owns a thread/control domain for its servant state.
- The **proxy** exposes the client interface, validates/captures arguments, constructs a method request, submits it, and returns a future or explicit one-way acceptance result.
- A **method request** reifies operation, immutable/exclusively owned arguments, identity, deadline, authority/effect context, guard, invocation, result cell, and cleanup.
- The **activation queue** stores accepted but unexecuted requests under finite capacity and declared ordering/fairness.
- The **scheduler** selects an eligible request, invokes it against the servant, and completes its result.
- A **guard** is a bounded, side-effect-free eligibility predicate evaluated against scheduler-owned servant state.
- The **servant** implements sequential object behavior and mutable state; clients do not access it directly.
- A **future/promise** exposes eventual success, failure, or cancellation observation without implying that cancellation stopped a running effect.
- A **one-way request** provides no value future, but still needs admission, failure observation, lifecycle, and effect accounting if loss matters.
- **run-to-completion** means one selected request retains servant mutation ownership until its bounded invocation finishes or reaches an explicit safe suspension protocol.

### Central model, mechanism, or theorem

Invocation becomes

\[
client\xrightarrow{proxy}MethodRequest(r)\xrightarrow{accept}Q_a
\xrightarrow{guard/scheduler}servant\xrightarrow{terminal}future_r.
\]

For one non-reentrant scheduler executing requests to completion, servant operations are linearized at scheduler-defined points, so observable servant mutation is serial even when clients invoke concurrently. This does not imply FIFO execution: if head request (r_1) has false guard and later (r_2) is enabled, a work-conserving scheduler may execute (r_2) first.

With activation capacity (K), at most one running request, and bounded request payload (b_{max}), pending/running request count is at most (K+1) and queued payload at most (Kb_{max}), provided no hidden queue, recursive unbounded continuation, or leaked future retains additional state. Safety through serial ownership does not prove liveness: an unsatisfiable guard can wait forever unless expiry, cancellation, failure, or rejection makes it terminal.

### Critical invariants

- Proxy submission has exactly one outcome: rejected with client ownership retained or accepted with active-object ownership and one stable request identity.
- Only the scheduler/control domain invokes the servant or reads mutable servant state used by guards.
- Activation count, bytes, per-client/operation work, futures/results, continuations, and external dependencies are finite.
- Guards are deterministic relative to protected state, side-effect-free, bounded, and reevaluated after every state-changing event without busy polling.
- Every accepted two-way or consequential one-way request reaches one observable terminal classification.
- One request mutates servant state at a time unless an explicitly verified reentrant/suspension protocol preserves invariants.
- Arguments and results cross the boundary by value, immutability, or exclusive lease; caller mutation after acceptance cannot race.
- Future cancellation is separated from queued reclamation, running computation, and external effect truth.
- Ordering, guard bypass, priority, fairness, deadline, and starvation policy are explicit API semantics.
- Shutdown closes proxy admission, resolves guarded/queued requests, finishes or reconciles running work, completes futures, retires the scheduler, and then destroys servant resources.

### Common failures

Common failures include exposing the servant behind the proxy, an unbounded mailbox, mutable captured arguments, a blocking proxy enqueue on an event/UI thread, guards that perform I/O or mutate state, checking only the queue head, busy-loop guard scanning, starvation behind never-enabled requests, assuming invocation order equals execution order, blocking servant code that halts all methods, waiting on the same active object's future from its scheduler thread, reentrant callbacks into the object, one-way requests whose exceptions disappear, future cancellation mistaken for rollback, leaked caller thread-local authority, and shutdown leaving guarded futures unresolved.

### Compact example

An account servant starts at 40. Requests arrive `withdraw(70)`, `deposit(50)`, and `withdraw(60)`. The first withdrawal guard is false, so the scheduler executes the enabled deposit, producing balance 90; it then executes the first withdrawal, producing 20. The second withdrawal remains guarded until another `deposit(50)` raises balance to 70, then completes at 10. Servant mutation is serialized, but execution is not FIFO; every accepted request gets one future result.

### Connections

[SEPAT-075](075-thread-pool.md) supplies general execution capacity; [SEPAT-077](../ROADMAP.md) protects a Monitor Object synchronously; [SEPAT-078](../ROADMAP.md) studies Future and Promise semantics independently. Active Object also connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

When many threads need an object whose state is easiest to reason about sequentially, how can an object-like interface turn calls into scheduled requests so callers do not share its servant state or control its execution thread?

Active Object moves synchronization from every method body into an invocation boundary and scheduler. Clients call a proxy. The proxy packages the call as a Method Request, places it on an Activation Queue, and returns a Future if a result matters. A scheduler in another control domain selects requests whose guards permit execution, invokes a sequential Servant, and completes results. The pattern improves isolation only when the proxy is exclusive and the request lifecycle is explicit.

## Why This Matters

Communication gateways, devices, GUI models, per-connection agents, workflow coordinators, caches, and domain aggregates often need sequential mutable state while their callers are concurrent. Locking every caller to the object couples caller latency and exposes lock ordering. An Active Object can preserve a single mutation owner and allow clients to continue asynchronously.

Decoupling also introduces temporal semantics. The proxy return means accepted, not executed. A guard can reorder work. A future can block a caller later. The queue retains memory and authority. A slow servant method stops all operations on that object. Process failure can lose accepted requests. Production design must make these consequences visible rather than disguising remote/asynchronous behavior as an ordinary local call.

## Prerequisites and Retrieval

You should understand Command/Method Object, proxy, queues, threads/event loops, mutual exclusion, futures/promises, cancellation, deadlines, backpressure, idempotency, linearizability, and basic fairness. Retrieve these facts:

1. Returning from an asynchronous proxy means submission outcome, not servant method completion.
2. A queue's thread safety establishes handoff visibility but not safe continued caller mutation of arguments.
3. Serial servant execution can avoid internal data races while still producing wrong scheduling, authorization, or external effects.
4. A guard that depends on servant state must be evaluated in the servant's ownership domain.
5. Skipping a disabled queue head can improve progress but reorder requests and starve some of them.
6. A future can complete exceptionally/cancelled and dependent continuations may run on implementation-defined executors or completing threads.
7. Blocking within one active object blocks every later request to that servant unless work is explicitly split/offloaded.
8. Durable acceptance and in-memory enqueue are different guarantees.

## Learning Objectives

After completing this module, you should be able to:

- identify client, proxy, method request, activation queue, scheduler, servant, guard, and future;
- trace two-way and one-way invocation from argument capture through terminal cleanup;
- specify servant confinement, request ownership, finite admission, result uniqueness, guard purity, and shutdown invariants;
- design a scheduler with enabled-set selection, wakeups, fairness, priorities, deadlines, and starvation handling;
- distinguish invocation, acceptance, selection, linearization, execution, future completion, delivery, and external effect;
- reason about ordering, reentrancy, callbacks, self-wait deadlock, blocking servants, continuations, and composition;
- compare Active Object with Monitor Object, Actor, Thread Pool, Half-Sync/Half-Async, Command, and durable workflow;
- define cancellation by queued/running/completed state and reconcile ambiguous effects;
- secure proxy authority, payload/result retention, tenant quotas, and thread/context boundaries;
- verify finite state, guards, concurrency confinement, overload, failure, shutdown, persistence, and performance claims.

## Core Exposition

### Identify and separate the participants

The proxy is the only client-visible route. It resembles the servant interface but its methods validate/capture calls rather than directly mutate servant state. Each method creates a Method Request with operation-specific guard/call logic and a result cell. The Activation Queue owns accepted requests. The Scheduler repeatedly selects an enabled request. The Servant owns the actual sequential state and methods. The Future lets a client observe a two-way result later.

These can be implemented as separate classes or collapsed safely, but the responsibilities remain. If clients can reach the servant, confinement fails. If method requests call arbitrary public callbacks while holding servant invariants, reentrancy returns. If the queue is hidden in a generic executor, guard and ordering semantics may be lost.

### Define the proxy contract

The proxy validates method name/version, argument schema/size, caller authorization sufficient for acceptance, deadline and capacity. It creates stable request/effect identities, freezes or transfers arguments, reserves queue/result resources, and tries bounded submission. Exactly one of rejection or acceptance wins against shutdown.

For a two-way method, return a future only after acceptance is established. On rejection, return/throw a typed immediate outcome rather than a future that can never complete. For one-way methods, return an acceptance receipt if delivery matters. “Void” cannot mean exceptions and overload disappear.

Do not block an event-loop/UI caller on a full activation queue. Use nonblocking offer, asynchronous capacity wait, backpressure, or typed rejection. Caller-runs would execute the servant outside its scheduler and violate confinement.

### Reify the complete method request

A request contains request ID, object ID/generation, operation/version, immutable arguments or leases, caller/tenant and authority reference policy, accepted time/deadline, priority/class/sequence, idempotency/effect identity, guard, invocation, cancellation state, result cell, trace, and cleanup.

Avoid closures that accidentally retain a large object graph, request-scoped credentials, mutable buffers, locks, database sessions, or a dead caller. Make retention visible. If values are borrowed, their lease survives until actual request terminal state, not merely caller future cancellation.

### Constrain the servant

Only the scheduler invokes servant methods and reads mutable state used for scheduling. Methods can therefore be written sequentially, with invariants established at each request boundary. This is confinement, not immunity: servant methods can still violate domain invariants, block indefinitely, perform ambiguous effects, leak aliases, or throw.

Keep methods bounded and run-to-completion. A long database/network call blocks later reads, cancels, and health operations for this object. Split into state-machine steps: record intent, initiate bounded external work, then enqueue a correlated continuation/result back to the active object. Revalidate object generation, authority and state before applying it.

Never publish a mutable servant collection/reference in a future. Return immutable snapshots, copies, value objects, or controlled capabilities. External mutation would bypass serialization.

### Make guards pure and scheduler-owned

A guard answers whether a request may execute in the current servant state: sufficient balance/capacity, prior sequence complete, resource available, lifecycle open, or protocol precondition. It runs in the scheduler's ownership domain and must be fast, deterministic for the examined state, side-effect-free and exception-safe.

A guard must not call a network, wait for a lock controlled by clients, consume a resource, mutate state, or complete the future. Otherwise repeated evaluation changes behavior or blocks the scheduler. If eligibility depends on an external event, represent that event as a request/state update that wakes scheduling.

### Schedule enabled work without spinning

The scheduler waits until the queue changes, servant state changes, a deadline/cancellation occurs, or shutdown begins. It computes/selects from enabled requests and executes one. After a state-changing request, it reevaluates relevant guards. Use condition/event notification rather than continuous full scans.

Checking only the FIFO head can cause head-of-line blocking: a disabled withdrawal prevents a later deposit that would enable it. Scanning for the first enabled request improves progress but reorders. Index requests by guard dependency/state class for scale, while ensuring index maintenance and wakeups cannot miss an enable transition.

Set a finite scan/evaluation budget so malicious or expensive guards cannot monopolize scheduling. Guard exceptions terminally fail/quarantine their request according to policy; they do not kill the active object silently.

### Specify ordering and fairness

Concurrent invocation has no universal total order unless the proxy defines a linearized acceptance sequence. Even with FIFO activation, guards, priorities, cancellations and deadlines change execution. Completion delivery and external effects can reorder further.

State the guarantee: FIFO among simultaneously enabled requests, per-client FIFO, sequence/version order, priority with aging, or another policy. Track bypass count/age and deadline slack. An unsatisfiable request must eventually expire, cancel, reject due to lifecycle change, or produce a domain failure; infinite silent waiting is usually unacceptable.

Strict priority can starve lower classes, and a high-priority request can depend on a lower-priority state-changing request. Use dependency-aware scheduling, aging, weighted/reserved shares, or explicit prerequisite linkage. Fairness is empirical/policy evidence, not inferred from a queue type.

### Choose linearization points precisely

Possible facts differ:

- invocation: client called proxy;
- acceptance: queue/result capacity reserved and ownership transferred;
- selection: scheduler chose an enabled request;
- effect linearization: servant state/effect changed at an operation-defined instant;
- local completion: result cell won one terminal state;
- client observation: continuation/get observed it;
- durable/external effect: storage/device/remote system met its own contract.

Document the relevant point for each method. A `deposit` may linearize at servant balance mutation; a remote payment may be ambiguous until external reconciliation. Future completion is not automatically the domain linearization point.

### Bound activation and retained state

Bound request count and bytes globally, per active object, tenant/client, operation and priority. Also bound futures, continuations, response snapshots, deferred/guarded age, external work and retries. An object with capacity 1,000 and 10 MiB arguments can retain far more than expected.

Use admission based on memory and useful deadline wait. When saturated, reject, pause producers, coalesce replaceable state updates, or route explicitly durable work. Coalescing is valid only when intermediate operations are observationally irrelevant and effect/audit semantics permit it; never coalesce commands casually.

Many active objects each with a dedicated thread/queue multiply idle stacks and capacity. A shared scheduler can multiplex object mailboxes while preserving one active request per servant, but needs fair per-object scheduling, object lifecycle fencing and protection from one blocking servant. A single shared executor queue does not itself preserve per-object serialization.

### Treat futures as result protocols

The future carries success value, typed failure or cancellation. Exactly one terminal completion wins. Clients should compose asynchronously where possible; blocking `get` can consume a thread or deadlock.

If the scheduler thread calls the proxy on the same Active Object and waits for that future, the new request cannot run until the current method returns, producing self-deadlock. Reentrant inline execution changes ordering/invariants and should not be an accidental workaround. Provide private servant methods for same-turn logic, or explicit nonblocking continuations.

Continuation execution context matters. A continuation may run on the completing scheduler thread and block/reenter it unless an executor is specified. Keep completion callbacks bounded and dispatch untrusted/client work outside servant ownership.

### Define cancellation truthfully

A queued request can be marked cancelled and skipped/reclaimed, completing its future once. A selected/running servant operation may observe cooperative cancellation at safe points, may finish normally, or may complete an external effect. A completed request cannot be undone through its future.

Record `cancel_requested` separately from actual outcome. Cancellation can withdraw interest in a response without rolling back state. Stable effect identity, conditional state, compensation or inquiry handles ambiguity. Deadline is similar: expire disabled/queued work, but reap/reconcile running continuations.

Cancellation itself is a scheduler event and must wake guard selection. Do not require a cancelled client to remain alive to release payload/result resources.

### Handle failure without losing the object

Catch method/guard exceptions at the scheduler boundary, complete the request exceptionally, restore or quarantine servant state, release resources, and continue only if invariants remain trustworthy. Use transactional/rollback structures for mutations that can fail midway; a generic catch cannot repair corruption.

If the scheduler thread dies, accepted futures otherwise remain unresolved. Supervision must detect failure, fence the object generation, classify the running request/effect, recover servant state from a valid source, fail/replay queued requests under stable identities, and start a new generation. In-memory Active Object offers no durable acceptance by itself.

### Avoid unsafe reentrancy and callbacks

A servant callback into client code can synchronously call back into the proxy, block on a future, mutate shared data or throw. Do not execute arbitrary callbacks inside servant state mutation. Produce an immutable event/result and deliver it after the request reaches a stable boundary on a separate controlled executor.

If reentrancy or coroutine suspension is supported, every suspension exposes servant state to another request. Define which invariants hold, which requests may interleave, how cancellation resumes cleanup, and how stale continuations are fenced. This is a different, more complex model than simple run-to-completion.

### Secure the boundary

Capture authenticated identity, tenant and authorization-relevant facts explicitly; never inherit stale thread locals. Decide whether authorization is snapshotted at acceptance or revalidated at effect/delivery. Long guard waits often require current-authority checks before sensitive effect.

Limit method names, arguments, queue shares, guard cost and response size. Protect payloads/futures/traces at rest in memory and logs, clear sensitive servant/scheduler context, and prevent one client from probing state via timing or queue priority. Object IDs/generations prevent results from an old tenant/session reaching a reused active object.

### Shut down every request

Shutdown linearizes proxy closure, so later calls reject. The scheduler wakes and applies policy: drain eligible safe requests, cancel/fail disabled or all queued requests, or persist transferable work. Every accepted future completes. Running work finishes/cancels to deadline and external effects are reconciled.

No old request may enqueue a continuation into a stopped/new servant generation. Stop result delivery only after terminal cells and cleanup. Join scheduler/shared execution, release activation/result resources, then destroy servant/dependencies. Record unresolved durable effects and restart procedure.

### Observe and verify

Measure invocation/accept/reject; queue count/bytes/oldest age; enabled/disabled counts and guard evaluation/bypass; selection/fairness/priority; request queue wait, servant service, continuation/result/client delay; cancellations by state/outcome; guard/method/scheduler failures; current object generation; external work/effects; per-tenant usage; future retention; scheduler utilization; and shutdown residue.

Model request/servant state and guards. Test concurrent proxy invocation, exact capacity, mutable-argument sentinels, unsatisfiable/enabling guards, bypass/starvation/priority, cancellation/deadline at every state, self-wait/reentrant callback, method/guard/scheduler failure, external continuation reorder, object close/reuse, result-consumer stall, shared-scheduler fairness, shutdown and crash recovery. Performance claims need declared workloads and tail evidence.

### A finite executable model

This deterministic account models guard-aware selection and serialized servant mutation. It does not run threads, locks, futures, cancellation, deadlines, external effects, failures or persistent recovery.

<!-- bijux-verify: {"id":"sepat-076-guarded-scheduler","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"enqueue=w1,d1,w2 pending=3 balance=40\ndispatch=d1 result=90 pending=w1,w2\ndispatch=w1 result=20 pending=w2\nenqueue=d2 pending=w2,d2\ndispatch=d2 result=70 pending=w2\ndispatch=w2 result=10 pending=none\nfutures=w1:20,d1:90,w2:10,d2:70\ninvariant=serialized=True balance=10\n","stderr":""}} -->
```python
class ActiveAccount:
    def __init__(self, balance):
        self.balance = balance
        self.pending = []
        self.futures = {}
        self.running = False

    def enqueue(self, request, operation, amount):
        self.pending.append({"request": request, "operation": operation, "amount": amount})

    def runnable(self, item):
        if item["operation"] == "deposit":
            return True
        return self.balance >= item["amount"]

    def dispatch(self):
        chosen = None
        for item in self.pending:
            if self.runnable(item):
                chosen = item
                break
        if chosen is None:
            return None
        self.pending = [item for item in self.pending if item is not chosen]
        self.running = True
        if chosen["operation"] == "deposit":
            self.balance += chosen["amount"]
        else:
            self.balance -= chosen["amount"]
        self.futures[chosen["request"]] = self.balance
        self.running = False
        return chosen["request"], self.balance


account = ActiveAccount(balance=40)
account.enqueue("w1", "withdraw", 70)
account.enqueue("d1", "deposit", 50)
account.enqueue("w2", "withdraw", 60)
print(f"enqueue=w1,d1,w2 pending={len(account.pending)} balance={account.balance}")

request, result = account.dispatch()
print(f"dispatch={request} result={result} pending={','.join(item['request'] for item in account.pending)}")
request, result = account.dispatch()
print(f"dispatch={request} result={result} pending={','.join(item['request'] for item in account.pending)}")

account.enqueue("d2", "deposit", 50)
print(f"enqueue=d2 pending={','.join(item['request'] for item in account.pending)}")
request, result = account.dispatch()
print(f"dispatch={request} result={result} pending={','.join(item['request'] for item in account.pending)}")
request, result = account.dispatch()
pending = ",".join(item["request"] for item in account.pending) if account.pending else "none"
print(f"dispatch={request} result={result} pending={pending}")

order = ("w1", "d1", "w2", "d2")
values = ",".join(f"{item}:{account.futures[item]}" for item in order)
print(f"futures={values}")
print(f"invariant=serialized={not account.running} balance={account.balance}")
```

## Definitions and Notation

Let (Q_a) be activation queue with capacity (K); (S) servant state; (r=(id,op,args,guard,result,deadline,effect)) a Method Request; and (E(S,Q_a)) the enabled request subset. Selection function σ chooses an element of (E) under ordering/fairness policy.

Request states are

\[
created\rightarrow\{rejected,accepted\rightarrow queued\rightarrow selected
\rightarrow running\rightarrow terminal\}.
\]

Cancellation/expiry can be requested in nonterminal states; actual outcome remains distinct. Let (lin(r)) be the operation-defined servant/effect linearization point, not automatically proxy return or future completion. Object lifecycle identity is `(object_id,generation)`.

## Mechanisms, Invariants, or Proof Structure

### Servant-safety argument

Assume clients access state only through the proxy; arguments do not retain mutable aliases; one non-reentrant scheduler selects/invokes one request at a time; servant references never escape; and each method restores invariants before return. Then servant mutations are serial and data-race-free within this model. This does not prove method/domain correctness, external effects, runtime memory safety or process recovery.

### Guard-safety and progress argument

If guards are pure functions of scheduler-owned state and request data, repeated evaluation cannot itself mutate servant state. If every state change/cancel/deadline wakes scheduling, selection examines eligible requests, and every persistently enabled request is eventually selected under the fairness policy, enabled requests progress. A false forever guard needs a terminal expiry/cancel/lifecycle policy; serialization alone gives no liveness.

### Capacity argument

With activation capacity (K), one running request, bounded (b_{max}), no hidden queue and finite result/continuation retention, the active object owns at most (K+1) requests and (Kb_{max}) queued payload. Dedicated threads/queues multiplied across objects and external continuations require separate global bounds.

### Terminal-result argument

If acceptance creates one result cell; rejection creates none/typed immediate outcome; scheduler success/failure, queued cancellation/expiry and shutdown all attempt one serialized terminal transition; then each accepted request has at most one logical result. A completed external effect can differ from cancelled/timeout client observation and requires its own reconciliation.

### Evidence boundaries

Finite automated models can check guard selection, serialization, capacity and terminal cells. Schedule/race tests sample concrete interleavings. Source review establishes runtime future/queue semantics for declared versions. Performance, fairness, availability, security and domain correctness remain empirical/human-reviewed claims.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Appropriate use |
| --- | --- | --- | --- |
| Active Object | Sequential servant plus asynchronous clients, guard scheduling | Queue/future/lifecycle complexity; one slow method blocks object | Stateful object with asynchronous operations |
| Monitor Object | Direct synchronous calls under monitor | Caller blocks; lock/reentrancy/condition complexity | Short synchronous protected operations |
| Actor | Message isolation, supervision/distribution ecosystems | Different interface/state/message semantics | Message-oriented isolated components |
| Thread Pool + locks | Shared capacity and familiar tasks | State ownership/locking remains with tasks | Independent tasks or explicit synchronization |
| Half-Sync/Half-Async | Protects async I/O from synchronous layer | Queue handoff but not per-object method semantics | Protocol/service layer boundary |
| Event-loop state machine | Efficient many-object multiplexing | Explicit continuations and no blocking | Many small nonblocking entities |
| Immutable copy-on-write state | Simple readers and snapshots | Copy/update contention and memory | Read-heavy small state |
| Durable workflow/queue | Persistence, retries, long waits | Distributed delivery/idempotency/latency | Long-lived durable commands |

One thread per active object provides simple ownership but scales poorly for many idle objects. Shared execution scales threads but needs one-at-a-time object scheduling. Guards express state conditions elegantly but complicate fairness and indexes. Futures resemble local returns but can hide asynchronous latency and failure.

## Failure Modes and Misconceptions

- **“The proxy call executed the method.”** It usually establishes submission/acceptance only.
- **“Active Object is just a thread-safe object.”** It reifies and schedules asynchronous method requests in another control domain.
- **“FIFO queue guarantees FIFO execution.”** Guards, priority, cancellation and deadlines may bypass.
- **“Serial servant means whole system is safe.”** Authorization, scheduling, effects and leaked aliases can still fail.
- **“A guard may reserve resources.”** Repeated evaluation must be side-effect-free; reservation belongs in selected execution.
- **“Polling guards is harmless.”** It wastes CPU and can starve execution; wake on relevant state changes.
- **“Disabled work can wait forever.”** It retains memory/authority/future and needs a terminal policy.
- **“Mutable arguments are safe after enqueue.”** The caller can race unless ownership/value is transferred.
- **“One-way means failures do not matter.”** Consequential accepted work still requires observation/audit.
- **“Future cancellation rolls back servant state.”** Running/completed effects remain actual outcomes.
- **“Blocking get is always safe.”** Scheduler self-wait or saturated executor dependencies can deadlock.
- **“Callbacks may run inside the servant.”** They can reenter, block or leak state unless isolated.
- **“Async servant methods may freely suspend.”** Interleaving at suspension changes the run-to-completion model.
- **“Dedicated thread guarantees capacity.”** Thousands of active objects multiply threads/queues and retain work.
- **“Restart can replay everything.”** Only durable accepted identity/effect/recovery protocols support replay.
- **“Shutdown may abandon false guards.”** Every accepted future and resource still needs terminal handling.

## Worked Examples

### Example 1

**Situation.** Two clients concurrently call `reserve` on an inventory Active Object.

**Reasoning.** The proxy captures immutable SKU/quantity, authority, request/effect ID and deadline. The scheduler invokes one request at a time; its guard checks current stock. The first mutation changes stock before the second guard executes. Each future reports its own serialized outcome.

**Conclusion.** Concurrency enters at invocation, while servant state mutation remains sequential.

### Example 2

**Situation.** `withdraw(70)` heads a queue at balance 40; `deposit(50)` is behind it.

**Reasoning.** Head-only scheduling deadlocks progress even though deposit enables withdrawal. Select the first enabled request, execute deposit, then reevaluate. Document that guarded selection can reorder and audit sequence where domain semantics require it.

**Conclusion.** Guard-aware scheduling separates queue order from execution order.

### Example 3

**Situation.** A low-priority request has remained enabled for ten minutes while urgent traffic stays continuous.

**Reasoning.** Strict priority violates liveness. Apply aging/weighted shares or reserved capacity, unless domain policy explicitly expires/rejects the lower class. Measure enabled age and bypass count under adversarial sustained load.

**Conclusion.** Persistent enablement needs an eventual-selection or terminal policy.

### Example 4

**Situation.** A caller mutates a byte buffer immediately after proxy acceptance while the servant later parses it.

**Reasoning.** Queue visibility does not prevent concurrent mutation. Copy bounded input, freeze an immutable value, or transfer an exclusive lease that the caller cannot reuse until actual terminal cleanup.

**Conclusion.** The asynchronous boundary requires explicit argument ownership.

### Example 5

**Situation.** A servant method calls its own proxy and synchronously waits for the returned future.

**Reasoning.** The nested request sits behind the currently running method; the single scheduler cannot execute it until the waiter returns. Call a private sequential servant operation directly within the same invariant boundary or compose a nonblocking later request without waiting.

**Conclusion.** Self-future waiting deadlocks a run-to-completion Active Object.

### Example 6

**Situation.** A method invokes a remote payment service for 20 seconds while status and cancel requests queue.

**Reasoning.** One blocking servant freezes the whole object. Record a payment-pending state and effect ID, initiate external work via a bounded subsystem, return/yield at a defined stable boundary, then enqueue a generation-checked completion request. Cancellation changes desired state but reconciles actual payment outcome.

**Conclusion.** Long external work should become an explicit state transition and continuation.

### Example 7

**Situation.** Cancelling a future races with a servant method that has already debited balance.

**Reasoning.** Only one future terminal status may win, but balance effect has its own linearization. Record cancel request, actual debit/effect ID and client observation separately. Reconcile/refund by domain policy rather than pretending cancellation undid history.

**Conclusion.** Result-cell state and domain effect truth are different.

### Example 8

**Situation.** A future completion runs an untrusted continuation inline on the scheduler thread.

**Reasoning.** The continuation blocks and calls the proxy, delaying all servant work and risking reentrancy. Complete the result cell at a stable boundary, but dispatch client continuations through a bounded separate executor or require bounded nonblocking callbacks under a documented contract.

**Conclusion.** Future completion context is part of servant isolation.

### Example 9

**Situation.** Shutdown finds three false-guard requests and one running external write.

**Reasoning.** Close admission; terminally cancel/fail guarded requests and release their payloads; request cooperative cancel of the write but reap its actual effect; complete futures; prevent stale continuation into a new generation; then stop scheduler and destroy servant resources.

**Conclusion.** Guarded and running requests require different shutdown outcomes.

### Example 10

**Situation.** A clinical medication-order Active Object outlives the clinician session that submitted an order.

**Reasoning.** Request captures order/patient/principal/session and object generations, policy version, deadline and effect identity. Before irreversible commit, scheduler revalidates current authority and clinical state. A stale session cannot receive protected results; a committed order remains auditable/reconciled. Bounded priority/fairness and named clinical review govern urgent versus routine work.

**Conclusion.** Active-object confinement complements but does not replace current authority and clinical safety controls.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): component boundaries, temporal coupling, deployment and failure domains place active objects in systems.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): model-based guards, controlled concurrency, overload, race/fault and recovery tests verify behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): authority freshness, tenant quotas, payload retention, context isolation and stale-generation suppression protect the boundary.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): durable commands, idempotency, ambiguous effects, supervision and reconciliation extend in-memory semantics.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): acceptance receipts, asynchronous operations, status/cancel APIs, deadlines and overload expose temporal contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): scheduler pools, resource limits, telemetry, rolling generations and shutdown make active objects operable.
- [SEPAT-075](075-thread-pool.md) supplies execution; [SEPAT-077](../ROADMAP.md) contrasts synchronous monitor calls; [SEPAT-078](../ROADMAP.md) deepens result-cell semantics.

## References

1. Lavender, R. Greg, and Douglas C. Schmidt. “Active Object: An Object Behavioral Pattern for Concurrent Programming.” *Pattern Languages of Program Design 2*. Addison-Wesley, 1996. <https://www.dre.vanderbilt.edu/~schmidt/PDF/Act-Obj.pdf>. Accessed 2026-08-29.
2. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000.
3. Gamma, Erich, Richard Helm, Ralph Johnson, and John Vlissides. *Design Patterns*. Addison-Wesley, 1994. Command, Proxy and related object patterns.
4. Oracle. “CompletableFuture,” Java SE 25 API. Terminal completion, dependent actions and cancellation semantics. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletableFuture.html>. Accessed 2026-08-29.
5. Oracle. “BlockingQueue,” Java SE 25 API. Capacity and memory-consistency semantics. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/BlockingQueue.html>. Accessed 2026-08-29.
6. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Task execution, cancellation, confinement and liveness.
7. Lea, Doug. *Concurrent Programming in Java*, 2nd ed. Addison-Wesley, 1999.
8. Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*, revised 1st ed. Morgan Kaufmann, 2012.
9. Hewitt, Carl, Peter Bishop, and Richard Steiger. “A Universal Modular ACTOR Formalism for Artificial Intelligence.” IJCAI, 1973. Actor comparison.
10. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018. Stability, timeouts and bulkheads.
11. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003. Message channels, commands and asynchronous boundaries.
12. Little, John D. C. “A Proof for the Queuing Formula: L = λW.” *Operations Research* 9, no. 3 (1961): 383–387.

Future completion context, queue visibility/capacity, cancellation, scheduler threading, coroutine interleaving and shutdown vary by runtime/library version. Current official specifications were checked on 2026-08-29; verify exact deployed behavior.

## Exercises

### Exercise 1

Name every Active Object participant and design Method Requests for `deposit`, guarded `withdraw`, and `snapshot`. Define invocation, acceptance, selection, linearization, future completion and observation separately, with at least eight invariants.

### Exercise 2

An Active Object has activation capacity 120, one running request, maximum queued payload 32 KiB, accepted rate 400/s, and stable measured mean residence 0.15 s. Compute declared maximum queued payload, maximum local request count, and average resident requests using Little's Law. Explain what these quantities do not prove.

### Exercise 3

Design a shared scheduler for 10,000 mostly idle per-device Active Objects. Cover per-object serialization, global/per-device capacity, guard indexes/wakeups, fair selection, long external work, generations, futures, cancellation, security, shutdown and observability.

### Exercise 4

Diagnose an Active Object with direct servant access, unbounded queue, mutable closures, I/O guards, head-only selection, self-future waits, blocking callbacks, unobserved one-way errors, future-only cancellation and abandoned guarded futures at shutdown. Provide remediation and verification.

### Exercise 5

Design an Active Object for a safety-critical infusion-pump controller. Address command/authority identity, servant invariants, guard policy, ordering/priorities, finite capacity, deadlines/cancellation, device effects, fail-safe behavior, persistence/restart, security, observability, testing and required external review.

## Answers to the Exercises

### Answer 1

Participants are clients, exclusive proxy, concrete deposit/withdraw/snapshot Method Requests, finite Activation Queue, guard-aware Scheduler, sequential account Servant and one result cell/future per two-way request. All requests carry request/object generation, immutable arguments, deadline, principal/authority, effect ID, sequence/class and cleanup. Deposit and snapshot guards are normally lifecycle-open; withdrawal additionally requires sufficient balance/current policy.

Invocation is entering proxy; acceptance is atomic capacity reservation/enqueue/ownership transfer; selection is scheduler choice from enabled requests; deposit/withdraw linearize at serialized balance mutation and snapshot at the serialized state read; future completion publishes the typed outcome; observation is client get/continuation. Invariants include exclusive proxy/servant confinement, one running mutation, finite queue/bytes/results/tenants, immutable inputs/snapshots, pure bounded guards, wake after relevant state/cancel/deadline, one terminal result per accepted identity, explicit non-FIFO guard policy/fairness, deadlines including wait, cancellation separate from effect, no scheduler self-wait/callback reentrancy, and complete shutdown terminal accounting.

### Answer 2

Maximum declared queued payload is

\[
120\times32\text{ KiB}=3840\text{ KiB}=3.75\text{ MiB}.
\]

With one running request, maximum local queued-plus-running count is (120+1=121). Little's Law gives

\[
L=\lambda W=400\times0.15=60
\]

average resident requests for the stable measured boundary.

These exclude running payload, object/servant state, request object graphs, futures/continuations/results, dedicated thread stack/TLS, external work, producers, shared-scheduler queues and overhead. Averages do not bound bursts/tails, guard starvation or deadline success. The arithmetic proves neither servant correctness, fair scheduling, adequate service capacity, durability, security nor external-effect uniqueness.

### Answer 3

Do not allocate 10,000 dedicated platform threads. Maintain one finite mailbox/state record per live device and a bounded shared executor with an atomic “scheduled/running” token per object. Proxy admission enforces global count/bytes/tenant plus per-device capacity and generation. Enqueue transitions an idle eligible object onto a finite ready-object scheduler once; a worker executes a bounded number/time slice of enabled requests serially, then reschedules if work remains, preventing concurrent servant access and one hot device monopolizing workers.

Index guards by state dependency and wake only affected devices/requests on state, cancel, deadline or external-result events. Use weighted fair/aged object selection and bounded scan. Long device/network work records stable pending intent/effect ID and runs in a dependency-bounded async subsystem; its immutable completion reenters the matching device generation. Futures complete once on separate safe continuation execution; queued cancellation reclaims, running cancellation reconciles actual effect.

Authenticate each proxy request, revalidate authority before sensitive effect, use immutable protected payloads, clear worker context and enforce per-device/tenant quotas. Shutdown closes all proxy generations, cancels/drains/persists by operation, rejects stale continuations, completes futures, reconciles device effects, drains ready/external/result paths, joins workers and persists/reloads valid servant state. Observe ready objects, mailbox bytes/age/guards, per-object fairness, token violations, service/external/result tails, stale/cancel/effect outcomes, memory and residue. Verify finite token/state models, adversarial hot devices, guard transitions, race/stress, object close/reuse, external reorder/failure, overload, context isolation and crash recovery.

### Answer 4

Direct servant access defeats confinement; unbounded/mutable requests defeat capacity and ownership; I/O guards block/repeat effects; head-only selection can prevent enabling work; self-wait deadlocks; inline callbacks reenter/block; one-way failures vanish; future cancellation may not stop effects; shutdown leaks accepted requests/futures.

Make proxy exclusive and servant private. Use finite count/byte/tenant admission with typed nonblocking rejection; capture immutable values/leases and stable identity. Make guards pure scheduler-owned state predicates; choose enabled requests under documented fairness with event-driven wakeups and expiry. Replace self-waits with private servant calls or asynchronous continuation. Complete futures at stable boundaries but run client callbacks on a bounded separate executor. Give one-way work receipts/error sinks/audit. Track cancellation by lifecycle/effect and reconcile.

Shutdown closes admission, terminally resolves guarded/queued requests, drains/cancels/reconciles running work, completes results and joins scheduler before destruction. Verify state/guard models, exact capacity, mutable sentinels, enabling/bypass/starvation, I/O-guard prohibition, self-wait detection, callback reentrancy, one-way exception, every cancellation race, stale generation, result stall, shutdown and crash recovery; add real concurrency/race/memory and workload tail tests.

### Answer 5

Use immutable command ID, pump/patient/therapy/prescription/session and object generations, authenticated clinician/system authority, policy/configuration version, monotonic sequence, deadline, effect/idempotency identity, payload classification and audit trace. The private servant owns therapy state, dosage/rate bounds, reservoir/line/sensor/alarm state and transition invariants. Guards are pure bounded checks of lifecycle, validated prescription, sequence, interlocks and device readiness; they never read hardware directly. Hardware observations enter as authenticated generation-qualified requests.

Serialize safety-relevant commands with explicit priorities and starvation analysis; reserve alarm/stop capacity without letting lower work block prerequisites. Bound global/pump/principal queue count/bytes, guard age and external device operations. Expired queued commands fail terminally. Running cancel is an explicit safe transition, not future state; distinguish requested, device-accepted and physically confirmed effect in a protected durable ledger. On uncertainty enter hazard-approved fail-safe mode and reconcile before further dosing.

Persist minimal validated servant/effect state and sequence; shutdown stops admission or transfers to safe controller, resolves queues, drives device safe state, reaps effects, completes audit/futures and fences old generation. Restart authenticates hardware/configuration and reconciles before accepting commands. Apply least privilege, mutual device identity, replay protection, encrypted/minimized data, key/log integrity, quotas and tamper evidence.

Observe every command state/deadline/guard/bypass, servant transition, device acknowledgement/physical feedback, alarm/fail-safe, queue/resource saturation, stale/cancel/duplicate and recovery residue. Verification requires formal/state-machine safety analysis, model checking of guards/order, hardware-in-the-loop, sensor/actuator/network/power/process fault injection, overload/priority tests, security/adversarial tests, restart reconciliation and clinical simulation. Production claims require named clinical/medication-safety, biomedical/device, controls/concurrency, human-factors, security/privacy, reliability/operations and regulatory reviewers with traceable hazards and acceptance evidence.
