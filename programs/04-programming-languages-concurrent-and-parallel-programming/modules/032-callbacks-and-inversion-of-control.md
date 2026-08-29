---
module_id: CONPAR-032
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 32
title: Callbacks and Inversion of Control
status: complete
last_verified: 2026-08-29
---

# Callbacks and Inversion of Control

## One-Page Review

### Governing question

When control is transferred to a framework or library, which callback contract makes timing, cardinality, ordering, ownership, errors, cancellation, reentrancy, and terminal outcomes safe and composable?

### Essential definitions

- A **callback** is behavior supplied now for invocation by another owner under a stated contract.
- **Inversion of control (IoC)** means the framework controls when and under what context application behavior runs.
- **Invocation cardinality** is zero-or-one, exactly-one, zero-or-many, or another explicit count.
- A **completion callback** reports one operation's terminal outcome.
- An **event listener/subscriber** handles a potentially unbounded series until removal or source termination.
- **Reentrancy** occurs when controlled code calls back into an object before its current operation returns.
- A **trampoline/scheduler boundary** defers invocation to prevent same-stack reentrancy.
- An **unsubscribe/cancellation handle** requests that future delivery cease.
- **Terminal arbitration** chooses exactly one success, error, cancellation, or timeout outcome.
- **Callback context** includes receiver, captured environment, thread/loop, trace, authority, and borrowed data.

### Central model, mechanism, or theorem

A safe callback API defines a state machine. For a one-shot operation: `PENDING → SUCCEEDED(result) | FAILED(error) | CANCELLED(reason)`, with exactly one terminal transition and at most one callback delivery. For a subscription: `ACTIVE → CLOSING → CLOSED`, with event delivery allowed only in ACTIVE and one terminal signal. The function type alone cannot prove timing, ordering, affinity, ownership, or error semantics.

### Critical invariants

Invocation timing is always synchronous, always deferred, or explicitly separated by method. Cardinality and terminal precedence are stated. Callback arguments and borrowed buffers remain valid for a documented duration. Receiver/context and thread/loop affinity are known. State is set to a reentrancy-safe value before invoking untrusted code. Listener-list mutation has snapshot/live semantics. Exceptions/rejections cannot cross forbidden boundaries. Removal/cancellation races with already queued delivery are defined. Each registration has one owner and release path. Duplicate terminal delivery is suppressed and observable.

### Common failures

An API sometimes calls synchronously and sometimes later; calls completion twice; reports both error and result; throws asynchronously where caller's `try` cannot catch; invokes user code while internal state is half-mutated; retains borrowed memory; leaks captured objects by forgotten listeners; removes listeners while iterating without policy; assumes unsubscribe retracts queued work; calls a UI callback from a worker; lets panic/unwind cross FFI; or converts a many-event stream into one promise and loses data/errors.

### Compact example

A dispatcher snapshots listeners A,B,C. During delivery A removes B and adds D. Snapshot semantics still deliver A,B,C for this emission; the next snapshot is A,C,D. The rule makes mutation deterministic. A live-array iteration might skip B, run D immediately, or depend on indices, exposing internal representation as public behavior.

### Connections

[Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md) supplies scheduling and reentrancy context; [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies ownership. The [program roadmap](../ROADMAP.md) next develops futures and promises.

## Governing Question

How should engineers specify, implement, adapt, test, and retire callbacks so that handing control to another component does not hide temporal coupling, duplicate outcomes, lifetime violations, unfair work, or unhandled failures?

A callback parameter is a small type with a large protocol.

## Why This Matters

Callbacks power event emitters, GUI actions, OS completions, network libraries, visitors, comparators, middleware, foreign-function interfaces, hooks, and asynchronous APIs. They decouple the component that detects an event from application behavior.

The inversion is useful because the framework can schedule, retry, multiplex, or emit many events. It is hazardous for the same reason: the caller no longer controls stack, time, thread, count, or surrounding state. A function signature such as `(Error?, Value?) -> void` does not say whether invocation is immediate, whether both values can appear, whether it happens once, or whether the buffer may be retained.

Production callback design therefore starts with a temporal contract and ownership state machine. Futures can simplify a one-shot result; streams can represent many values; structured tasks can own cancellation. Yet callbacks remain beneath many abstractions and at FFI/OS boundaries, so their rules must be explicit.

## Prerequisites and Retrieval

Retrieve:

- task/thread context from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- starvation and progress from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- deterministic traces from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- ownership transfer from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- component lifecycle from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md); and
- run-to-completion, queueing, and cancellation from [Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md).

Retrieval prompt: if a callback can run before its registration function returns, list the caller state that may still be only half-initialized.

## Learning Objectives

After completing this module, a learner can:

1. distinguish one-shot completion, event subscription, visitor, predicate, and hook callbacks;
2. write a complete callback contract beyond its function type;
3. prevent sync/deferred ambiguity and reentrancy corruption;
4. arbitrate success, failure, cancellation, timeout, and duplicate completion;
5. define listener ordering and mutation-during-dispatch semantics;
6. manage captures, borrowed arguments, unsubscription, and FFI context lifetime;
7. contain exceptions, rejected async handlers, and foreign unwinding;
8. adapt callbacks to futures/streams without changing cardinality; and
9. test temporal, ownership, overload, and shutdown boundaries.

## Core Exposition

### Inversion of control

In an ordinary call, caller chooses time, stack, arguments, and continuation. With a callback, the caller supplies behavior but the callee chooses some of those dimensions. The callee becomes scheduler and protocol owner.

Examples differ:

- `sort(compare)` calls a comparator synchronously many times during one call;
- `enumerate(visitor)` may synchronously borrow each item;
- `read(path, completion)` invokes once later;
- `on(event, listener)` invokes zero or many times;
- an interrupt/FFI hook may run on a restricted thread or foreign stack.

Calling all of them “a function parameter” erases decisive guarantees.

### Contract axes

Document:

1. trigger and eligibility;
2. sync, deferred, or caller-selected timing;
3. exact cardinality;
4. ordering among callbacks/events;
5. execution thread, loop, executor, and receiver;
6. argument ownership, mutability, and validity duration;
7. result/error/exception channel;
8. reentrancy and allowed operations during invocation;
9. registration/removal mutation policy;
10. cancellation/unsubscribe semantics;
11. terminal event and cleanup ownership;
12. work/latency limits and observability.

If one method can return either before or after calling the callback, callers must defend against both. Prefer always-deferred completion or separate `try_*` synchronous and `*_async` operations.

### Cardinality determines abstraction

A one-shot operation naturally has one terminal result. Its callback should be at most once or exactly once after accepted submission. If initiation can fail synchronously, state whether the callback still occurs.

A subscription emits zero or many values and eventually error/complete/close. A visitor can stop early based on return. A predicate may be called repeatedly and must be pure. An allocator/deleter callback has paired ownership.

Choose future/promise for one value, stream/async iterator for many, and callback only when direct invocation or interoperability is the real boundary. Do not adapt many values into one future by silently taking the first.

### The “sometimes synchronous” hazard

Suppose cached data invokes callback inline, but a cache miss invokes later:

1. caller sets `initializing=true`;
2. calls API;
3. expects to store cancellation handle;
4. API invokes inline;
5. callback sees no handle and calls close;
6. registration returns a now-orphaned handle.

This is historically called “releasing Zalgo”: timing becomes input-dependent. Always deferring creates one predictable boundary, though it adds queueing and lifetime. A deliberately synchronous API can be safe if it never retains the callback and documents reentrancy.

### Reentrancy-safe mutation

Before invoking untrusted callback:

- move internal state to a valid observable state;
- detach or snapshot data the callback may mutate;
- establish recursion/dispatch guard;
- release locks unless the contract specifically forbids reentry and proves no callback cycle;
- retain lifetime through invocation; and
- decide how exceptions affect remaining listeners.

After return, re-check because callback may unregister, close, recursively emit, or destroy owner. Do not keep raw iterators/pointers into mutable listener storage unless mutation is forbidden and enforced.

### Listener dispatch semantics

Common policies:

**Snapshot:** copy stable listener identities at emission start. Adds/removes affect later emissions; listeners removed mid-dispatch may still receive current event.

**Live:** each mutation affects remaining current dispatch. This needs exact cursor rules and is harder to reason about.

**Tombstone/generation:** stable slots are marked inactive; dispatch checks generation before call. Removal can suppress not-yet-started delivery without invalidating iteration.

Node's current `EventEmitter` documents synchronous registration-order invocation. Other event systems differ. State whether duplicate registrations are allowed, once-listeners are removed before or after invocation, and recursive emit starts nested delivery or queues.

### Exactly-once terminal arbitration

One-shot states:

`PENDING → SUCCEEDED | FAILED | CANCELLED | TIMED_OUT`.

Use an atomic/loop-owned state transition before callback delivery. Only the winner owns result publication and capacity release. Losers dispose of late resources and record duplicate/late completion.

Do not invoke success and then error when callback throws; callback failure belongs to the consumer execution boundary, not operation outcome. Do not call completion from both immediate error and later cleanup.

“Exactly once” includes shutdown and initiation failure. If the API instead promises at-most-once, callers need timeout/recovery for missing completion.

### Error channels

Callback APIs use several incompatible models:

- error-first `callback(error, value)`;
- tagged result `callback(Result)`;
- separate success/error callbacks;
- event streams with `error` events;
- thrown exception for immediate argument errors;
- rejected future returned by an async listener.

Define exclusive states. In error-first style, error non-null means value is absent/unusable. A `try/catch` around registration cannot catch an exception thrown in a deferred callback.

For listener fan-out, decide whether one throw stops dispatch, is aggregated, is reported to an error hook, or terminates process. Never silently swallow. Node `EventEmitter` and `EventTarget` have different current error behavior; consult exact API docs.

### Async callbacks inside synchronous dispatch

A synchronous emitter calling an `async` listener receives a promise immediately and continues. It does not automatically wait for the listener. Ordering after the first suspension differs from synchronous registration order, and rejection may become unhandled unless captured.

If dispatch must await listeners, expose an asynchronous dispatch returning a future and define sequential versus concurrent awaiting, failure aggregation, cancellation, and listener mutation. Do not overload a synchronous `emit` with accidental promises.

### Captures and memory lifetime

A closure retains captured objects as long as the registration retains the closure. Long-lived publishers can therefore retain sessions, UI trees, buffers, or credentials after their logical lifetime.

Registration should return a disposable subscription token. Owners unregister during close. Weak references can avoid retention but introduce nondeterministic disappearance and are not a substitute for lifecycle design.

Borrowed callback arguments are valid only for the stated duration. A synchronous FFI enumeration may pass pointer+length valid until callback returns; retaining it is invalid even if the parent handle remains live.

### Thread and executor affinity

Callbacks may run:

- on caller's stack;
- on one event loop;
- on a worker that completed I/O;
- on a UI/main thread;
- on an interrupt/signal context;
- concurrently on several threads.

The contract must say. Thread-safe registration does not imply serialized delivery. UI callbacks may need marshaling. Worker callbacks need publication/synchronization and cannot mutate loop-owned state directly.

If order matters across executors, assign sequence IDs and serialize at an owner. Scheduling order is not completion order.

### Cancellation and unsubscription

Unsubscribe can mean:

- no future emissions will be selected;
- no callback will begin after the method returns;
- queued callbacks may still run;
- current callback may finish;
- method blocks until in-flight callbacks drain.

These guarantees have different costs. A token with generation lets queued delivery check active status. A strong synchronous unregister needs coordination and can deadlock if called from the callback itself.

Cancellation of one-shot work races with completion. One terminal state wins. Keeping capture/context memory alive until all queued/in-flight paths retire is mandatory.

### Foreign callbacks

FFI contracts add calling convention, function-pointer validity, context pointer type, thread, alignment, panic/exception/unwind, and library unload.

Never unwind across a C ABI unless explicitly supported. Catch and convert failures inside the language boundary. The foreign library may retain the function/context after registration returns; pin/allocate it accordingly and unregister/drain before freeing or unloading code.

Signal/interrupt callbacks permit only restricted operations. Allocation, locks, logging, or language runtime entry can be unsafe.

### Backpressure and listener work

A callback that emits faster than consumers process can accumulate queued work. Synchronous emission instead transfers latency to publisher and lets a slow listener delay all others.

Define whether delivery:

- blocks producer;
- buffers with capacity;
- drops/coalesces;
- samples;
- applies per-listener queues;
- disconnects slow consumers; or
- exposes demand/credits.

Event callbacks are not automatically streams with backpressure. The later backpressure module develops this boundary; here every pending delivery must be bounded and owned.

### Callback composition

Nested callback chains obscure:

- which scope owns cancellation;
- which error path fires;
- whether branches join;
- which resources release;
- whether a callback is called twice; and
- how stack traces/trace context propagate.

Name operations and centralize terminal arbitration. Futures/promises flatten one-shot composition; async iterators/streams model sequences; structured concurrency owns child tasks. Adapters must preserve original timing and cardinality or document deliberate change.

### Compatibility and contract evolution

Changing callback timing, order, cardinality, receiver, or error delivery is an observable API change even when the static function signature is identical. Moving a formerly synchronous callback to a queue can change stack-based transactions, exception capture, object lifetime, and test completion. Moving deferred delivery inline introduces reentrancy. Running listeners concurrently changes mutation order and requires thread safety. Adding retries changes how often side effects occur.

Evolve such contracts deliberately. Add a new method or explicit scheduler option rather than silently changing timing. Version event payloads and make new fields ignorable where compatibility requires it. Preserve old listener order unless the API declared it unspecified. If cancellation becomes stronger, check deadlock and callback-self-removal. If it becomes weaker, callers may free state too early.

Deprecation evidence should include old/new temporal traces, adapter behavior, duplicate/error cases, and supported runtime versions. State which observations were never guaranteed so tests can stop depending on accidents without pretending that documented behavior was absent.

### Safe callback-to-future adaptation

An adapter:

1. creates pending future;
2. installs a once-guard before registration;
3. catches synchronous initiation failure;
4. handles callback that may run inline;
5. translates exactly one result/error;
6. disposes late duplicate values;
7. connects cancellation/unsubscribe; and
8. retains registration/context until terminal.

If original callback can fire many times, return a bounded stream, not a future. If it can never fire, future needs cancellation/timeout from the operation contract.

### Testing

Test:

- callback before registration returns;
- callback deferred;
- zero, one, duplicate, and many invocations;
- success/error exclusivity;
- callback throws/rejects;
- recursive invocation;
- add/remove during dispatch;
- unsubscribe before selection, while queued, and in flight;
- completion versus cancel/timeout;
- close/destroy inside callback;
- wrong-thread invocation;
- retained/expired borrowed data;
- pool/queue overload; and
- shutdown at every state.

Use deterministic schedulers/fake executors and explicit barriers rather than arbitrary sleeps. Property-test state transitions and count terminal deliveries.

### Observability

Record operation/registration ID, event sequence, callback kind, enqueue/start/end, executor/thread, queue delay, service duration, terminal winner, duplicate/late suppression, error channel, cancellation, listener count, retained subscription age, and trace context.

Avoid logging sensitive callback payloads. Instrumentation callbacks must not recursively trigger the same emitter without guards.

## Definitions and Notation

For one-shot operation `o`, terminal count:

`T_o = S_o + F_o + C_o + D_o`

where success, failure, cancellation, and deadline indicators are each zero or one. Exactly-once requires `T_o=1`; at-most-once requires `T_o≤1`.

For subscription `q`, event deliveries `E_q≥0` precede one optional terminal signal; no event begins after strong-close linearization. A weaker unsubscribe must state which queued/in-flight set remains.

Let callback queue delay `L=start-eligible` and service `C=end-start`. Invocation order does not imply asynchronous completion order.

## Mechanisms, Invariants, or Proof Structure

For each callback surface:

1. **Classify it:** one-shot, many-event, visitor, predicate, hook, allocator/deleter.
2. **State timing:** synchronous, always deferred, phase/executor, and reentrancy.
3. **State cardinality and ordering.**
4. **Define argument/receiver/context ownership and validity.**
5. **Define result, error, throw/reject, and terminal precedence.**
6. **Move state before calling untrusted behavior.**
7. **Define dispatch mutation/recursive-emission policy.**
8. **Define unsubscribe/cancel versus queued/in-flight delivery.**
9. **Bound work, pending deliveries, and slow consumers.**
10. **Contain thread/FFI/unwind boundaries.**
11. **Test every temporal race and duplicate outcome.**
12. **Choose future/stream/structured ownership when it better matches cardinality.**

The executable dispatcher snapshots listeners. Listener A removes B and adds D during the first emission; mutations affect the next emission only.

<!-- bijux-verify: {"id":"callback-snapshot-dispatch-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first_dispatch=['A', 'B', 'C']\nsecond_dispatch=['A', 'C', 'D']\nregistrations=4\nremovals=1\nactive_listeners=3\nsnapshot_policy=True\n","stderr":""}} -->
```python
listeners = ["A", "B", "C"]
registrations = 3
removals = 0
mutated = False

def dispatch():
    global listeners, registrations, removals, mutated
    snapshot = list(listeners)
    delivered = []
    for listener in snapshot:
        delivered.append(listener)
        if listener == "A" and not mutated:
            updated = []
            for current in listeners:
                if current != "B":
                    updated.append(current)
            updated.append("D")
            listeners = updated
            registrations += 1
            removals += 1
            mutated = True
    return delivered

first = dispatch()
second = dispatch()
print(f"first_dispatch={first}")
print(f"second_dispatch={second}")
print(f"registrations={registrations}")
print(f"removals={removals}")
print(f"active_listeners={len(listeners)}")
print("snapshot_policy=True")
```

Limitations: this synchronous single-threaded model stipulates snapshot semantics. It does not model a real runtime, recursion, errors, async listeners, thread affinity, weak references, queued delivery, cancellation, FFI, backpressure, memory reclamation, or terminal arbitration.

## Alternatives and Trade-Offs

**Direct synchronous call** is clearest when caller owns timing and stack.

**Completion callback** interoperates broadly with low allocation, but inversion and error/cardinality rules remain.

**Future/promise** represents one eventual result and supports flat composition; cancellation and producer ownership are not automatic.

**Stream/async iterator** represents many values and terminal completion, with potential demand/backpressure semantics.

**Observer/event emitter** supports fan-out and dynamic membership, at ordering, retention, failure, and slow-listener cost.

**Channel/mailbox** makes delivery queued data with explicit ownership/capacity.

**Visitor/predicate** is efficient synchronous inversion when borrowing and reentrancy are tightly documented.

**Structured task API** owns child lifetime, cancellation, and error propagation better than detached callbacks.

## Failure Modes and Misconceptions

1. **The function type is the callback contract.** Timing, count, ownership, and errors are missing.
2. **Callback implies asynchronous.** Many dispatchers invoke synchronously.
3. **Async API may call inline as an optimization.** It creates reentrancy/timing ambiguity.
4. **One-shot means exactly once automatically.** All terminal races need arbitration.
5. **Error and result can both be meaningful.** Usually they must be exclusive.
6. **Caller `try/catch` catches deferred throw.** The stack has already returned.
7. **Registration order means async completion order.** Listener continuations can diverge.
8. **An async listener is awaited by synchronous emit.** Often its promise is ignored.
9. **Remove during dispatch has obvious behavior.** Snapshot/live/tombstone policy decides.
10. **Unsubscribe retracts queued callback.** Only if the contract and generation check say so.
11. **One loop eliminates reentrancy bugs.** Inline callbacks and suspension still expose state.
12. **Closures release with logical owner.** Publisher retention can leak them.
13. **Borrowed data can be retained because callback has a pointer.** Validity may end on return.
14. **Thread-safe registration means serialized delivery.** These are different guarantees.
15. **Foreign callbacks may throw/panic normally.** Unwind across ABI can be invalid.
16. **Callbacks provide backpressure.** Fan-out can be unbounded.
17. **A future can wrap every callback.** Many-event sources need stream semantics.
18. **Duplicate suppression hides provider defects.** Suppress safely and report evidence.

## Worked Examples

### Example 1

**Situation.** Cache hit calls completion inline; miss defers.

**Reasoning.** Caller cannot know whether callback runs before cancellation handle/state initialization.

**Conclusion.** Make completion always deferred or split synchronous and asynchronous APIs.

### Example 2

**Situation.** Timeout and I/O completion each call the same callback.

**Reasoning.** Atomic/loop-owned terminal state lets one transition win; loser disposes late result.

**Conclusion.** Exactly-once is a state-machine property.

### Example 3

**Situation.** Listener A removes B and adds D during snapshot dispatch.

**Reasoning.** Current snapshot remains A,B,C; next membership is A,C,D.

**Conclusion.** Mutation semantics are deterministic and testable.

### Example 4

**Situation.** Async listener rejects during synchronous emit.

**Reasoning.** Emit receives a promise and continues unless API captures/awaits it; rejection uses another error channel.

**Conclusion.** Do not mix synchronous fan-out with implicit async completion.

### Example 5

**Situation.** Callback closes its own component while dispatch state is half-updated.

**Reasoning.** Recursive close observes invalid intermediate state.

**Conclusion.** establish stable state and guards before invoking user code.

### Example 6

**Situation.** Unsubscribe occurs after delivery is queued.

**Reasoning.** Weak unsubscribe permits it; generation-checked queued delivery can suppress it; strong drain waits with deadlock caveats.

**Conclusion.** Name the guarantee and lifetime cost.

### Example 7

**Situation.** Long-lived emitter retains a closure capturing a 1 GB session cache.

**Reasoning.** Registration is a strong ownership edge until unsubscribe/emitter destruction.

**Conclusion.** Return disposable tokens and audit subscription age.

### Example 8

**Situation.** C library retains Rust context pointer and later calls from worker thread.

**Reasoning.** Context must remain pinned/live, callback ABI/thread-safe, unwind contained, and unregister drained before free.

**Conclusion.** FFI callback contract owns code and data lifetime.

### Example 9

**Situation.** High-rate emitter queues one callback per event for a slow listener.

**Reasoning.** No demand/capacity exists; memory and latency grow.

**Conclusion.** Bound, coalesce, drop, disconnect, or use a backpressured stream.

### Example 10

**Situation.** A clinical alarm framework says its callback fires “exactly once.”

**Reasoning.** This does not prove sensor validity, scheduler deadline, UI/audio delivery, acknowledgement, persistence, or hazard recovery.

**Conclusion.** Named clinical, concurrency, UI, real-time, hardware, security, quality, and functional-safety reviewers need target evidence; no approval is implied.

## Cross-Program Connections

- **Programming languages:** closure capture, variance, receivers, exceptions, and FFI shape callback safety.
- **Operating systems:** completion, signal, interrupt, and UI callbacks impose context restrictions.
- **Software architecture:** IoC frameworks move scheduling and lifecycle ownership.
- **Distributed systems:** callbacks after timeouts can represent committed remote work.
- **Security:** callback complexity, unbounded fan-out, retained authority, and native boundaries create attack surfaces.
- **Testing:** deterministic executors expose inline/deferred and terminal races.
- **Observability:** invocation IDs and terminal winners reconstruct inverted control.
- **API design:** cardinality determines callback, future, stream, or channel choice.

## References

1. Martin Fowler. “Inversion of Control Containers and the Dependency Injection pattern.” 2004.
2. Erich Gamma et al. *Design Patterns*. Addison-Wesley, 1994.
3. Douglas Schmidt et al. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000.
4. Node.js Project. “Events,” Node.js 26.8.1 API. 2026. Accessed 2026-08-29.
5. Node.js Project. “Errors,” Node.js 26 API. 2026. Accessed 2026-08-29.
6. WHATWG. “DOM Standard: event listeners and dispatch.” Living Standard accessed 2026-08-29.
7. libuv Project. “Requests and `uv_cancel`,” libuv 1.x documentation. Accessed 2026-08-29.
8. Rust Project. “`Fn`, `FnMut`, `FnOnce`, and `AsyncFnOnce`,” Rust 1.98.0. 2026.
9. ISO C. *Programming Languages — C*, callback function-pointer and object-lifetime provisions. Current edition.
10. Herb Sutter. “Interrupt Politely.” Dr. Dobb's Journal, 2008.

## Exercises

### Exercise 1

List the callback-contract axes and distinguish completion, subscription, visitor, predicate, and FFI callbacks.

### Exercise 2

Trace snapshot dispatch of A,B,C when A removes B and adds D. Compare first and second emissions and explain a live-policy alternative.

### Exercise 3

Diagnose an API that sometimes invokes inline, calls both error and result, can complete twice after timeout, and lets unsubscribe free captured state while delivery is queued. Repair it.

### Exercise 4

Compare callbacks, futures, streams, channels, and structured tasks for one file result, a sensor sequence, fan-out notifications, and child-operation ownership.

### Exercise 5

A surgical device SDK invokes C callbacks from worker and interrupt contexts. Specify ABI, thread, ownership, error, cancellation, timing, verification, and human-review boundaries.

## Answers to the Exercises

### Answer 1

State trigger, timing, cardinality, order, thread/executor/receiver, argument ownership/validity, result/error channel, reentrancy, dispatch mutation, cancellation/unsubscribe, terminal cleanup, and work bounds.

A completion reports one terminal operation; subscription emits many until terminal/removal; visitor synchronously sees borrowed items and may stop; predicate returns a decision and may repeat; FFI callback additionally fixes calling convention, context pointer, code/data lifetime, thread, and unwind restrictions.

### Answer 2

At emission start snapshot is A,B,C. A runs, mutates underlying membership to A,C,D, but current snapshot remains unchanged; B and C run. Second emission snapshots A,C,D and runs them. The executable model records four registrations, one removal, and three active listeners.

A live policy could suppress B and possibly include D immediately, but must specify cursor behavior, duplicate prevention, recursive emission, and mutation ordering. Snapshot costs copying/stable identities but avoids exposing container indices.

### Answer 3

Sometimes-inline timing creates reentrancy. Use always-deferred completion or separate `try_get` and `get_async`. Replace ambiguous error/result arguments with a tagged result and require exactly one variant.

Create PENDING before registration; success, failure, timeout, and cancellation race through one atomic/loop-owned terminal transition. Winner invokes at most once and releases capacity; losers dispose late values and increment duplicate evidence. Unsubscribe marks generation inactive but retains capture/context until queued and in-flight references drain. Define whether queued delivery is suppressed. Initiation failure follows the same terminal contract.

### Answer 4

One file result is one-shot: future/promise provides composition and tagged error, though a low-level callback may underlie it. Sensor sequence is many-valued: bounded stream/async iterator with terminal error/close and demand. Fan-out notifications fit an event emitter when membership/order/error and slow-listener policies are explicit; per-subscriber channels isolate queues.

Related child operations need structured tasks so parent scope owns join, cancellation, and error propagation. Detached callbacks obscure this. Channels suit explicit ownership transfer and capacity. Choose by cardinality and lifetime, not syntax preference.

### Answer 5

Document calling convention, function/context pointer types, alignment, validity, retained ownership, unregister/drain, library unload, and prohibition/containment of C++ exception or Rust panic across C ABI. State which callbacks run on workers versus interrupt context; marshal UI/control work and permit only interrupt-safe operations in the latter.

Use one terminal state for cancel/complete, keep buffers/context live through in-flight callbacks, bound queues and callback work, define ordering and duplicate delivery, and provide monotonic timestamps/sequence IDs. Interrupt notification is not device acknowledgement or safe physical state.

Verify C/host-language smoke tests, race/sanitizer tests, callback-after-unregister attempts, recursive/duplicate/error paths, worker affinity, interrupt-safe static review, overload, shutdown/unload, hardware-in-loop timing, device faults, and restart. Named ABI/language, driver, hardware, concurrency, real-time, clinical/domain, cybersecurity, quality, regulatory, and functional-safety reviewers must approve target claims. This answer is not deployment approval.
