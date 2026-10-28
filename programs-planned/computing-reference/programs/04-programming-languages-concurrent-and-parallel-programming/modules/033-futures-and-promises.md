---
module_id: CONPAR-033
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 33
title: Futures and Promises
status: complete
last_verified: 2026-08-29
---

# Futures and Promises

## One-Page Review

### Governing question

How can one eventual result be represented, composed, observed, cancelled, and retired without hiding who starts the work, which scheduler runs continuations, or which component owns every terminal outcome?

### Essential definitions

- A **future** is a read-oriented handle for observing one eventual terminal outcome.
- A **promise**, **completer**, or **resolver** is the authority that settles that outcome.
- **Settlement** is the irreversible transition from pending to fulfilled or rejected; some APIs add cancellation as a distinct terminal state.
- A **continuation** is computation registered to run after settlement.
- **Flattening** makes a continuation that returns a future contribute its eventual value rather than produce a nested future.
- **Assimilation** adopts the state of another future or thenable under language-specific resolution rules.
- A **task** owns running computation; a future may merely observe it.
- A **join** waits for owned work to terminate; a race only discovers a winner.
- **Unhandled rejection/failure** is a terminal error for which no responsible observer exists at the runtime's observation point.
- **Structured ownership** bounds child lifetimes by a parent operation and joins them before the parent exits.

### Central model, mechanism, or theorem

Model a one-shot cell as `PENDING -> FULFILLED(v) | REJECTED(e)`. Exactly one transition wins. Any continuation registered before settlement is queued after publication; one registered later is still scheduled according to the API rather than run as an arbitrary special case. Composition obeys value propagation, error propagation, and flattening. The future does not, by itself, prove that computation has started, remains owned, is cancellable, or has stopped when an observer loses interest.

### Critical invariants

Settlement is single-assignment. Result publication precedes eligible continuation execution under the runtime's memory model. Continuations have a named scheduler/executor and never accidentally block it. Every started operation has an owner that awaits, returns, aggregates, or explicitly supervises it. Aggregator failure does not imply sibling cancellation. Cancellation has a direction, acknowledgement rule, and terminal precedence. Deadlines cover queued, executing, and cleanup time. A many-value source is not compressed into a one-value future. Producer admission is bounded before work starts. Late results and cleanup remain observed after timeout or race loss.

### Common failures

Code confuses a future with its task; creates all work before applying a concurrency bound; assumes `all` or `race` cancels losers; blocks an event loop with `get`; handles only fulfillment and loses rejection; returns nested futures; settles a promise twice; resolves a promise with itself; performs heavy continuation work on an internal completion thread; treats timeout as proof of termination; loses diagnostic context; or launches a detached future that outlives credentials, request state, tests, or shutdown.

### Compact example

Three already-started operations A, B, and C are passed to a fail-fast aggregate. B rejects first, so the aggregate rejects. A and C do not disappear: they can still mutate state, consume sockets, or fail later. Correct ownership cancels them if supported and then joins their terminal cleanup; alternatively it deliberately allows and observes completion. The aggregate is an observation policy, not a lifecycle boundary.

### Connections

[Callbacks and Inversion of Control](032-callbacks-and-inversion-of-control.md) supplies one-shot completion contracts. [Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md) supplies scheduling. The [program roadmap](../ROADMAP.md) next derives async/await state machines.

## Governing Question

How should engineers design and use futures and promises so that single-assignment state, continuation scheduling, failure propagation, cancellation, capacity, and computation lifetime remain explicit and testable?

A future makes an eventual result composable; it does not make the work self-owning.

## Why This Matters

Futures and promises replace callback pyramids with values that can be passed, combined, returned, and awaited. They appear in JavaScript `Promise`, Java `CompletionStage` and `CompletableFuture`, C++ `future`/`promise`, Rust `Future`, Python futures, Scala futures, and many task runtimes. The names overlap while semantics differ.

JavaScript promises are eagerly constructed and reactions become jobs. Rust futures are inert values until polled by an executor. C++ `std::future` is usually a one-consumer result handle, while `shared_future` supports multiple observers. Java `CompletableFuture` is both a completion stage and a mutable completer unless authority is narrowed. Cancellation may be absent, cooperative, advisory, or only a state transition on the handle.

Production reasoning therefore begins below syntax. Ask who owns completion authority, what starts execution, where continuations run, what settlement publishes, and what remains alive after a race, rejection, timeout, or dropped observer.

## Prerequisites and Retrieval

Retrieve:

- task ownership from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- progress and blocking from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- reproducible schedules from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- ownership transfer from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- publication ordering from [Acquire-Release Ordering](027-acquire-and-release-ordering.md);
- event-loop turns from [Event Loops and Nonblocking Execution](031-event-loops-and-nonblocking-execution.md); and
- callback cardinality from [Callbacks and Inversion of Control](032-callbacks-and-inversion-of-control.md).

Retrieval prompt: if a timeout future wins a race, identify the owner that still has to stop or join the losing operation.

## Learning Objectives

After completing this module, a learner can:

1. distinguish future observation, promise settlement authority, task execution, and structured ownership;
2. specify pending and terminal states with a single-assignment invariant;
3. reason about continuation scheduling, flattening, assimilation, and error propagation;
4. compare eager, lazy, hot, cold, single-consumer, and shared futures;
5. select and audit aggregate combinators without inferring cancellation;
6. avoid blocking event loops and completion executors;
7. define cooperative cancellation, deadline, and cleanup precedence;
8. bound producer admission rather than only already-created futures;
9. test settlement races, publication visibility, late failure, and shutdown; and
10. recognize when a stream, channel, task group, or synchronous value is the correct abstraction.

## Core Exposition

### Separate observation, completion, and execution

A future answers: “What is this one operation's eventual outcome?” A promise/completer answers: “Who may publish that outcome?” A task answers: “What computation is scheduled or running?” These may be separate objects or one object with several capabilities.

Separating them enforces least authority. A producer keeps the resolver; consumers receive only a future. If consumers can complete the public object, an unrelated component can forge success or failure. Java's `CompletableFuture` permits explicit completion, so APIs can expose a restricted `CompletionStage` view or enforce ownership convention. C++ naturally separates `promise<T>` from `future<T>`.

Dropping a future may cancel an owned computation in one system, merely unregister an observer in another, or do nothing. Never infer lifecycle from the name.

### Single-assignment state machine

The portable core is `PENDING -> FULFILLED(value) | REJECTED(error)`.

Some libraries add `CANCELLED`, but JavaScript `Promise` does not. Timeout is often a separate future that rejects, not a state change in the original work. Exactly one transition wins. Later attempts are ignored, return failure, or raise according to API.

The winner must publish payload before observers run. Threaded runtimes need a specified happens-before edge or equivalent synchronization. A custom future must use the language's synchronization primitives rather than rely on “callback happens later.” Store a terminal outcome as a tagged union, not independent `value` and `error` fields.

### Registration before and after settlement

An observer can register while pending or after terminal settlement. Both paths must preserve the scheduling contract. Running late registrations inline while early registrations are deferred recreates timing ambiguity and reentrancy defects.

ECMAScript schedules promise reactions as jobs; `then` does not synchronously call the handler even for an already-settled promise. Other APIs may run continuations inline, on the completing thread, on an explicit executor, or under implementation policy. Inline execution reduces scheduling cost but can create deep chains, priority inversion, lock reentrancy, or unexpected latency on an I/O thread.

### Mapping, chaining, and flattening

If `F` produces `A` and `f: A -> B`, mapping yields a future of `B`. If `g: A -> Future<B>`, flat-mapping/chaining yields `Future<B>`, not `Future<Future<B>>`.

Three propagation rules form the practical algebra: an ordinary return fulfills the next future; a thrown/reported failure rejects it; and a returned future is adopted. If a handler is absent, the corresponding outcome propagates. An error handler may recover with a value, translate the error, or preserve failure by rethrowing. Logging and returning normally is recovery, not transparent observation.

### Resolution is deeper than fulfillment

In ECMAScript terminology, a promise can be resolved to another pending promise and still not be fulfilled. Its final state follows the adopted object. The Promise Resolution Procedure protects against self-resolution, invokes foreign thenables carefully, and accepts only the first effective resolve/reject call.

Thenable assimilation executes foreign behavior. Reading or calling a malicious `then` can throw, call both branches, recurse, or never settle. Implementations need once guards and cycle defense. Other languages often flatten only known future types; do not apply JavaScript rules universally.

### Eager, lazy, hot, and cold

Constructing a JavaScript promise calls its executor synchronously, so side effects may begin before the promise is stored. Calling an `async` function runs its synchronous prefix and returns a promise. A Rust future normally progresses only when polled; creating it does not imply that I/O began. A library can also return a hot observation handle to external work already running.

This affects capacity. Mapping 100,000 inputs to eager producers starts 100,000 operations before `all` observes them. A semaphore acquired inside each already-started function may bound a critical section while retaining every payload and waiter.

Bound producer invocation: keep inputs or factories inert, admit a finite queue, and start at most `k` producers. Count queued, active, retrying, and cleanup work separately. Backpressure must act before an overload allocation or external side effect.

### Aggregation semantics

Aggregation is policy over terminal outcomes:

- **all** succeeds when all succeed and commonly fails when one fails;
- **all-settled** waits for every terminal outcome and preserves success/failure tags;
- **any** succeeds on the first success and fails only if all fail;
- **race** mirrors the first terminal participant; and
- **quorum** completes after a threshold under an application-defined failure rule.

Define empty-input behavior, input-order versus completion-order results, duplicate inputs, failure aggregation, and whether inputs were already started. JavaScript `Promise.all` preserves input-order results even when completion order differs. `Promise.race([])` remains pending under ECMAScript semantics; other APIs need not copy that edge case.

Most combinators do not cancel losers. Fail-fast means the aggregate settles early, not that sibling work terminated. If work is owned, signal cancellation and continue observing or joining cleanup.

### Failure ownership

Every started future needs a responsible observer. Acceptable ownership includes returning it to a caller, awaiting it, registering terminal handling, aggregating it into an owned group, or explicitly detaching it to a supervisor that records failure.

“Fire and forget” usually means “start and lose ownership.” A rejection may be reported late by a runtime, terminate a process under policy, or disappear after logging. Even if a handler is attached later, telemetry can race with unhandled-rejection detection. Every derived branch can itself fail and needs ownership.

At boundaries, preserve original error type, cause, operation identity, attempt, and trace context. Do not convert every failure to null or a generic message. Distinguish domain failure, cancellation, timeout, overload, and defect.

### Blocking versus suspension

A blocking `get` occupies a thread until terminal state. An `await`-like suspension returns control to a scheduler and later resumes a state machine. Blocking can be correct on a dedicated thread with a bounded wait. It is dangerous on an event-loop, UI, or executor thread needed to complete that same future.

Starvation deadlock occurs when every worker blocks waiting for child futures scheduled to the exhausted pool. Prefer asynchronous composition, reserve capacity, or use a scheduler with an explicit managed-blocking policy. Do not hold a mutex, transaction, borrowed buffer, or scarce permit across an unbounded wait unless that is the deliberate protocol.

### Cancellation is a protocol

Cancellation connects requester, task, future, underlying operation, and cleanup. Specify whether a request is advisory or guaranteed before start; which terminal state wins against success/failure; whether children inherit it; whether blocking I/O can be interrupted; when resources release; whether continuations still run; and how acknowledgement is observed.

Marking a future cancelled does not necessarily stop a thread or remote request. Java `CompletableFuture.cancel` treats cancellation as exceptional completion; its interrupt argument does not control underlying processing like every task implementation might. JavaScript commonly carries an `AbortSignal` separately. Rust cancellation is often dropping a future, but safety depends on which state is abandoned and who owns external effects.

Cleanup must be idempotent and observed. A result that loses to cancellation can still contain a resource that needs disposal.

### Deadlines and timeouts

A timeout bounds observer patience unless the contract links it to cancellation and join. It does not prove the producer stopped. End-to-end deadlines propagate remaining budget through admission, queues, retries, execution, and cleanup.

When deadline races completion, define one linearization rule. The winner settles the public result; the loser is still consumed. Record both public outcome and late underlying outcome without attempting a second settlement. Retries are new operations whose owner accounts for idempotency, attempt limits, shared deadline, and late responses.

### Polling futures and wakeups

Rust exposes another mechanism: `poll(Pin<&mut Self>, &mut Context)` returns `Pending` or `Ready(output)`. On `Pending`, the future arranges for the current waker to be notified when progress may be possible. Executors poll; futures must not busy-loop or block.

A wake is a hint to poll again, not a delivered value. Implementations update stored wakers and tolerate coalesced or redundant wakes. Polling after completion can violate an individual future's contract; combinators must fuse or avoid invalid repolling when necessary. This pull-driven model differs from push settlement but shares one terminal output.

### Multiple observers and consumption

Some future values can be observed repeatedly; others transfer their result once. JavaScript promises support many `then` registrations. C++ `future::get` consumes access, whereas `shared_future` permits multiple observers. Rust `Future::Output` appears once through polling; sharing is an additional abstraction.

Multiple observers raise payload questions. Is the value immutable, cloned, reference-counted, or borrowed? Does one observer's recovery affect another branch? Usually branches observe the same source outcome but create independent downstream futures. A settled future may retain a large payload, stack, closure chain, or security context until every branch is released.

### Context, security, and observability

Continuation execution crosses threads and queues. Explicitly propagate trace/span identity, request deadline, locale, authorization context, and diagnostic operation ID where required. Thread-local context may not cross an arbitrary executor. Do not retain mutable credentials beyond validity or leak secrets through aggregate errors.

Record creation, admission, start, terminal state, duration, queue delay, cancellation request/acknowledgement, timeout, late result, cleanup, and detached-failure owner. Sampling must not change ownership.

### Designing a future-returning API

State whether calling starts work; whether completion can occur before return; continuation executor/affinity; success and typed failure; cancellation and acknowledgement; deadline model; resource lifetime; admission limits; repeatability; and shutdown behavior.

Return a future for one eventual value. Return a stream/channel for many values. Return a task handle or task-group membership when lifecycle control is central. Return a synchronous result when no genuine asynchrony exists.

## Definitions and Notation

For operation `o`, let state `σ_o` be `PENDING`, `FULFILLED(v)`, or `REJECTED(e)`. With explicit cancellation, add `CANCELLED(r)`. Single assignment permits exactly one transition out of `PENDING`.

Let `A` be admitted-but-not-started operations, `R` running operations, and `K` cleanup operations. A bounded owner declares `|A| <= q`, `|R| <= k`, and usually a cleanup bound. Bounding only `R` after eager construction does not bound retained work.

For continuation `c`, define `eligible(c)` when its source settles, `start(c)` when its executor begins, and `finish(c)` after its returned outcome is assimilated. Queue delay is `Q_c=start(c)-eligible(c)`; service time is `S_c=finish(c)-start(c)`.

For aggregate inputs `F_1...F_n`, `all` succeeds iff every input fulfills. Fail-fast public settlement may precede terminal inputs, so `settled(aggregate)` does not imply `forall i, settled(F_i)`.

## Mechanisms, Invariants, or Proof Structure

Audit a future workflow in this order:

1. identify resolver, observer, task, scheduler, and parent owner;
2. state what starts execution and whether it is eager or lazy;
3. enumerate terminal states and the single winner;
4. establish publication before continuation eligibility;
5. define registration scheduling before and after settlement;
6. specify mapping, flattening, assimilation, and absent-handler propagation;
7. define aggregate empty cases, order, early settlement, and loser ownership;
8. bound admission before producer invocation;
9. define cancellation request, acknowledgement, precedence, and cleanup;
10. propagate deadline, trace, authority, and error cause;
11. join all owned work during normal exit and shutdown; and
12. test duplicate settlement, late registration, timeout races, and executor starvation.

The executable model uses a deterministic queue and single-assignment future. It demonstrates late registration, propagation through mapping, and suppression of duplicate settlement.

<!-- bijux-verify: {"id":"future-single-assignment-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source_state=fulfilled\nsource_value=21\nmapped_state=fulfilled\nmapped_value=42\nevents=['early:21', 'late:21', 'mapped:42']\nfirst_settlement_won=True\nduplicate_settlement_won=False\npending_jobs=0\n","stderr":""}} -->
```python
jobs = []

class FutureCell:
    def __init__(self):
        self.state = "pending"
        self.payload = None
        self.reactions = []

    def observe(self, reaction):
        if self.state == "pending":
            self.reactions.append(reaction)
        else:
            jobs.append(lambda: reaction(self.payload))

    def fulfill(self, value):
        if self.state != "pending":
            return False
        self.payload = value
        self.state = "fulfilled"
        reactions = list(self.reactions)
        self.reactions = []
        for reaction in reactions:
            jobs.append(lambda reaction=reaction: reaction(value))
        return True

def drain():
    while jobs:
        job = jobs[0]
        jobs[:] = jobs[1:]
        job()

events = []
source = FutureCell()
mapped = FutureCell()
source.observe(lambda value: events.append(f"early:{value}"))
source.observe(lambda value: mapped.fulfill(value * 2))
mapped.observe(lambda value: events.append(f"mapped:{value}"))

first = source.fulfill(21)
duplicate = source.fulfill(99)
source.observe(lambda value: events.append(f"late:{value}"))
drain()

print(f"source_state={source.state}")
print(f"source_value={source.payload}")
print(f"mapped_state={mapped.state}")
print(f"mapped_value={mapped.payload}")
print(f"events={events}")
print(f"first_settlement_won={first}")
print(f"duplicate_settlement_won={duplicate}")
print(f"pending_jobs={len(jobs)}")
```

Limitations: this synchronous, single-threaded teaching scheduler models fulfillment only and stipulates FIFO jobs. It does not implement rejection, thenable assimilation, thread-safe publication, polling/wakers, cancellation, deadlines, executor failure, aggregation, backpressure, or cleanup.

## Alternatives and Trade-Offs

**Direct return** has no scheduling or lifetime ambiguity when work is immediately available.

**Callback** can avoid allocation and fit OS/FFI boundaries, but composition and one-shot enforcement are manual.

**Future/promise** composes one eventual result and error. It neither represents many values nor automatically owns the task.

**Task handle** couples observation to execution lifecycle, cancellation, and join more directly. **Stream/async iterator** represents zero or many values with terminal completion and possibly demand. **Channel** decouples producers and consumers and may provide bounded capacity, but closure and multi-party ownership need protocols.

**Blocking future** is simple on dedicated threads but consumes capacity and can deadlock bounded executors. **Inline continuation** minimizes hops but exposes completing threads to untrusted cost and reentrancy. **Explicit executor dispatch** isolates cost but adds queues, context propagation, and shutdown rules.

**Fail-fast aggregation** reduces result latency. **All-settled aggregation** improves accounting and cleanup evidence. A supervisor may report early while joining in the background only when that background has a named durable owner.

## Failure Modes and Misconceptions

- “Creating a future starts work.” False for lazy/polled futures and uncertain for library handles.
- “Rejecting an aggregate cancels inputs.” Usually false.
- “Timeout means stopped.” It often means only the observer stopped waiting.
- “Await makes code sequential.” It makes one continuation readable; independently started work can overlap.
- “A semaphore around await bounds creation.” It may not if producers were already invoked.
- “Resolved means fulfilled.” Not under ECMAScript adoption terminology.
- “A future is a stream with one read.” It cannot carry repeated values or demand faithfully.
- “Cancellation is just another error.” It can require different retry, compensation, and user semantics.
- “Blocking get is equivalent to await.” One occupies a thread; the other normally suspends.
- “One handler observes every branch.” Each derived future can reject independently.
- “Dropping the handle stops the task.” Runtime-specific and often false.
- “Completion order determines aggregate result order.” Many `all` APIs preserve input order.
- “A race owns only the winner.” The caller still owns every started loser.
- “Settled values are free.” Futures retain payloads, stacks, closures, and context.
- “Async abstraction establishes memory safety.” Shared-state publication still needs language guarantees.

## Worked Examples

### Example 1

An image loader exposes its resolver publicly with the future. A consumer accidentally calls `complete(fakeImage)`. Split authority: the producer holds a private completer; consumers receive only a read-oriented handle. The type boundary now expresses ownership rather than relying on convention.

### Example 2

A cache hit returns an already-fulfilled promise, while a miss returns later. The runtime schedules both reactions through the same job mechanism. Caller initialization finishes before either continuation, eliminating the callback API's input-dependent inline path. This does not imply a universal order relative to timers or I/O.

### Example 3

`loadUser().then(loadOrders)` returns the orders future. Flattening makes the next stage yield orders. Writing `then(user => { loadOrders(user); })` forgets to return the inner future: the visible chain fulfills with an empty value while load failure becomes separately unowned.

### Example 4

Five eager upload calls are constructed and passed to `all`. The intended service limit was two, but all five opened files before aggregation. Replace eager handles with factories; let two workers invoke them; retain only a bounded pending queue. Now the bound controls actual producer start.

### Example 5

Inputs A, B, C finish in order C, A, B. An `all` combinator returns `[A-result, B-result, C-result]` because it preserves input positions. A completion-order requirement instead needs tagged results appended by an owned collector with synchronization and a deterministic tie policy.

### Example 6

An HTTP operation races a 200 ms timeout. Timeout wins, but the request later succeeds with a socket-backed response. The owner aborts if supported, continues observing the request, closes a late response, records its terminal state, and settles the public promise only once.

### Example 7

Every thread in a four-thread executor calls blocking `get` on a child scheduled to the same executor. No worker remains to run children. Compose asynchronously or use a scheduler designed for managed blocking; adding arbitrary threads masks rather than specifies capacity.

### Example 8

A Rust future returns `Pending` without registering the provided waker. No executor knows to poll it again, so progress can stop forever. Store or update the current waker when the readiness source changes and invoke it when progress may be possible; tolerate a poll that finds no new value.

### Example 9

A branch logs rejection and returns normally. Its derived future is fulfilled, so upstream failure is recovered. If policy is “log and preserve failure,” the handler must rethrow or return failure. Observing and recovering are different semantic choices.

### Example 10

A medical-device controller sends a remote stop command and races it against a deadline. Treating timeout rejection as proof that motion stopped is unsafe: execution may be delayed, completed, or unreachable. The design needs an independently specified safe-state protocol, acknowledgement identity, physical-state verification, bounded retries, and fail-safe behavior. Named controls, safety, device-domain, and regulatory reviewers must approve the hazard analysis and evidence; this chapter is not that review.

## Cross-Program Connections

- **Functional programming:** composition resembles map/flat-map, but effects, eagerness, and cancellation constrain algebraic reasoning.
- **Algorithms:** bounded scheduling is online admission; quorum/race policies require explicit threshold and failure conditions.
- **Operating systems:** futures wrap readiness/completion but do not replace kernel resource ownership.
- **Distributed systems:** local timeout cannot establish remote cancellation; retries require idempotency and deduplication.
- **Software engineering:** hiding resolver authority is interface segregation and capability security.
- **Data systems:** transaction and connection permits must not leak across abandoned chains.
- **Security:** context propagation preserves authority boundaries without retaining expired credentials.
- **Reliability:** supervisors join owned work and make shutdown finite.

## References

1. ECMA International. “ECMAScript Language Specification: Promise Objects.” <https://tc39.es/ecma262/multipage/control-abstraction-objects.html#sec-promise-objects>.
2. WHATWG. “HTML Standard: Event Loops.” <https://html.spec.whatwg.org/multipage/webappapis.html#event-loops>.
3. Promises/A+. “Promises/A+ Specification 1.1.” <https://promisesaplus.com/>.
4. Oracle. “Java Platform API: CompletionStage.” <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletionStage.html>.
5. Oracle. “Java Platform API: CompletableFuture.” <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletableFuture.html>.
6. ISO C++ Foundation. “Working Draft, Standard for Programming Language C++: Futures.” <https://eel.is/c++draft/futures>.
7. Rust Project. “std::future::Future.” <https://doc.rust-lang.org/std/future/trait.Future.html>.
8. Rust Project. “Asynchronous Programming in Rust.” <https://rust-lang.github.io/async-book/>.
9. Python Software Foundation. “concurrent.futures — Launching Parallel Tasks.” <https://docs.python.org/3/library/concurrent.futures.html>.
10. OpenJDK. “JEP 525: Structured Concurrency (Sixth Preview).” <https://openjdk.org/jeps/525>.

## Exercises

### Exercise 1

Distinguish a future, a promise/completer, and a task. Why should an API often expose only the first to consumers?

### Exercise 2

Operations A, B, and C have already started. A fail-fast aggregate rejects when B fails. State what the aggregate proves and what lifecycle work remains.

### Exercise 3

An application maps 20,000 inputs to async calls, then awaits their futures through a five-permit semaphore. Explain why resource use may remain unbounded and redesign admission.

### Exercise 4

Specify a timeout wrapper for one future. Include settlement arbitration, cancellation, late result handling, cleanup, and observability.

### Exercise 5

A railway-door controller returns a future from `closeDoors()`. A deadline rejection is currently interpreted as “doors are closed enough to depart.” Review the technical error and define the human evidence required before production use.

## Answers to the Exercises

### Answer 1

A future grants observation of one terminal outcome. A promise/completer grants authority to publish it. A task owns scheduled or running computation and often cancellation/join. Exposing only the future applies least authority: consumers cannot forge completion. The contract must still state whether dropping the handle affects the task.

### Answer 2

The aggregate proves only that its public policy selected B's rejection. It does not prove A or C stopped or settled. Their owner must allow and observe them deliberately or request cancellation and join cleanup. Late successes may contain resources; late failures require diagnostics.

### Answer 3

Calling 20,000 eager producers can allocate payloads, sockets, timers, closures, and futures before any permit controls them. Store input descriptions or factories in a bounded queue. At most five workers acquire capacity and then invoke producers. Define a finite admission limit, overload response, retry policy, and cleanup bound; count caller-side buffering separately.

### Answer 4

Create one atomic or loop-owned arbiter shared by underlying completion and deadline. If completion wins, cancel the timer and publish it. If deadline wins, publish timeout once and request cancellation if available. Continue observing the loser, dispose any late resource, and join cleanup under a bounded shutdown policy. Record operation ID, winner, cancellation request/acknowledgement, late outcome, and cleanup. Never settle publicly twice.

### Answer 5

Timeout establishes only that acknowledgement was not observed; it cannot establish physical door position or safe departure. The system needs independent sensors, correlated command identity, stale-message rejection, a fail-safe interlock, degraded behavior, bounded actuation/verification, and hazard analysis covering network, power, sensor, mechanical, and software failure. Production evidence requires named railway systems, controls, functional-safety, cybersecurity, operations, and regulatory reviewers; requirements traceability; hardware-in-the-loop and fault-injection results; applicable standards assessment; signed residual-risk acceptance; and deployment validation. This module supplies no approval.
