---
module_id: SEPAT-078
program: Software Engineering: Patterns
level: 2
module_number: 78
title: Future and Promise
status: complete
last_verified: 2026-08-29
---

# Future and Promise

## One-Page Review

### Governing question

How can one producer publish exactly one eventual value, failure, or cancellation to one or more consumers without conflating result state with computation lifetime, blocking the wrong executor, losing wakeups, leaking losers, or hiding continuation and effect semantics?

### Essential definitions

- A **promise/completer** is the write-side capability for one shared result state.
- A **future** is the read/observation-side capability for that state; it does not necessarily own the computation producing it.
- The **shared state/result cell** transitions once from pending to terminal success, failure, or cancellation.
- **single assignment** means exactly one terminal completion attempt wins; later attempts fail/are ignored under the API contract.
- A **waiter/awaiter** suspends or blocks until terminal; a **continuation** schedules computation triggered by terminal completion.
- **exceptional completion** stores/propagates failure as data in the result protocol rather than throwing on the producer thread alone.
- **broken promise/abandonment** terminally reports that the producer capability disappeared without a value where the runtime supports it.
- **cancellation request** expresses lost interest or an attempt to stop work; future cancellation does not universally interrupt/rollback the producer.
- **composition** derives futures through transform, flatten, combine-all, first-success, race, recovery, or finalization operators.
- **structured lifetime** scopes child computations so the parent cannot silently abandon unfinished futures/resources.

### Central model, mechanism, or theorem

For result cell (F_r), state machine is

\[
pending\xrightarrow{CAS/serialized\ winner}
\{success(v),failure(e),cancelled(c)\}.
\]

Exactly one completion wins locally. Publishing the terminal state must make the stored value/failure safely visible before waking/scheduling all registered observers. Registration races with completion: either registration is included in the waiter set before the winner publishes, or it observes terminal state and schedules itself; no observer can be stranded between check and registration.

This theorem is deliberately narrow. It proves neither that underlying work ran once, stopped on cancel/timeout, nor produced exactly one external effect. Computation state (C_r), future state (F_r), client interest (I_r), and external effect (E_r) must be modeled separately.

### Critical invariants

- Promise and future share one stable identity and state; only authorized completers can attempt terminal mutation.
- The result cell is single-assignment and every completion/cancel/abandon race has one documented winner.
- Value/failure data is fully initialized and safely published before terminal visibility and observer wakeup.
- Registration and completion cannot lose a waiter; observers added after completion are scheduled exactly under the API contract.
- Every accepted computation eventually completes its future or is explicitly reported unresolved; producer exceptions/abandonment cannot leave silent pending state.
- Cancellation/timeout of observation is distinguished from queued/running computation and external effect outcome.
- Continuation execution context, ordering, error propagation, blocking allowance, authority context, and resource ownership are explicit.
- Composition accounts for every branch, including losers, partial successes, multiple failures, cancellation and cleanup.
- Blocking waits never occupy the only thread/worker/event loop required to complete the awaited future.
- Futures, dependency graphs, captured values, waiters and continuations are bounded/scoped and observable through shutdown.

### Common failures

Common failures include multiple completion races without a winner contract, setting terminal before storing the value, check-then-register lost wake, a promise destroyed while consumers wait forever, unobserved exceptions, blocking `get` on an event loop or same saturated pool, mapping when flattening is required and producing nested futures, inline continuations blocking the producer, default executors creating hidden interference, timeout/cancel assumed to stop a database write, `race` leaking losing tasks/resources, `all` hiding multiple failures, callback exceptions swallowed, captured contexts/large graphs retained, future chains with unbounded concurrency, and shutdown abandoning pending results.

### Compact example

Two consumers register on a pending cell. A producer completes it successfully with 42 and wins; both consumers are notified. A racing cancellation loses because success is terminal, and a second producer completion is ignored. Both observers read 42 and a pure mapped continuation derives 84. The trace establishes one local terminal result, not real concurrency or cancellation of underlying work.

### Connections

[SEPAT-075](075-thread-pool.md) executes computations that often return futures; [SEPAT-076](076-active-object.md) returns futures from queued method requests; [SEPAT-077](077-monitor-object.md) underlies blocking shared-state implementations. Future and Promise also connects to [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

When a result becomes available on a different timeline from its consumer, how should the system separate producer authority, observation, completion, cancellation, continuation execution, and effect truth so asynchronous composition remains safe and comprehensible?

Future and Promise create a one-shot communication channel. The producer holds the promise/completer; consumers hold a future or restricted stage. The shared result state carries a value or failure and wakes/continues observers exactly once. The abstraction decouples timing, but does not create execution capacity, backpressure, durability, cancellation or exactly-once effects automatically.

## Why This Matters

Thread pools, asynchronous I/O, actors, Active Objects, RPC clients, caches and structured tasks all need to return results later. Futures replace ad hoc callback ownership with an inspectable result cell and enable graphs of dependent computation.

That graph can become a hidden distributed scheduler. Inline callbacks run on surprising threads, blocking waits consume completion capacity, exceptions cross wrappers, cancellation races effects, losers remain active, and thousands of pending nodes retain memory. Production use demands explicit semantics for shared state and the computation behind it.

## Prerequisites and Retrieval

You should understand threads/event loops, memory visibility, atomic state transitions, exceptions, cancellation, deadlines, task executors, callbacks, resource ownership, idempotency and dependency graphs. Retrieve these facts:

1. A future represents a result, not necessarily a running task; APIs differ in how tightly they bind the two.
2. Terminal outcomes usually include normal value, exceptional failure and cancellation.
3. Completing or cancelling an already-terminal result must not overwrite the winner.
4. Blocking wait consumes a thread; asynchronous await suspends logical work but still needs an executor/runtime to make progress.
5. A timeout on waiting can leave computation/effect running.
6. Continuations may run inline, on an event loop, a default/common pool, or an explicit executor.
7. “Any/race” returns one winner but does not automatically clean up losers.
8. Result publication needs a language/runtime memory-order guarantee for initialized values.

## Learning Objectives

After completing this module, you should be able to:

- identify promise, future, shared state, producer, observers, waiters, continuations, computation and executor;
- specify pending-to-terminal transitions and the exact winner behavior for value/failure/cancel/abandon races;
- distinguish future completion, computation termination, client interest, deadline and external effect;
- explain safe publication and lost-wakeup-free observer registration;
- choose blocking get, callback, async await/poll and completion-queue consumption without deadlocking progress;
- design map/flat-map, combine, race, recovery and cleanup with explicit failure/cancellation semantics;
- control continuation execution context, stack/reentrancy, authority context and resource lifetime;
- detect orphaned futures, unobserved failures, dependency cycles, retention and unbounded fan-out;
- integrate structured cancellation, deadlines, loser cleanup, shutdown and restart reconciliation;
- verify result cells using state models, race schedules, memory/race tools, executor saturation and fault injection.

## Core Exposition

### Separate the write and read capabilities

The promise/completer has authority to publish one terminal outcome. The future permits observation, waiting and perhaps cancellation request, but clients should not be able to forge success/failure. Expose a restricted read-only stage where the library allows it.

Both reference shared state with stable operation identity. That state includes pending/terminal tag, value or exception/cancel reason, waiter/continuation registrations, synchronization, producer/computation linkage where applicable, deadlines/tracing and cleanup metadata.

Do not expose a completable future to untrusted consumers if they can call completion methods. Java's `minimalCompletionStage`/copy-style restrictions illustrate capability separation; exact guarantees remain implementation-specific.

### Define terminal state precisely

Allowed terminal states should be mutually exclusive. “Done” often includes success, exceptional failure and cancellation. A result value can validly be `null`/unit in some APIs, so absence cannot identify pending. Store an explicit tag.

All contenders—producer success, producer exception, cancellation, timeout wrapper, abandonment, shutdown—attempt one serialized transition. Record which winner is authoritative. Later completion attempts must return false/throw/ignore in a way the producer observes; silently accepting double-completion hides logic defects.

Cancellation may itself be represented as a specialized exceptional completion. Do not infer computation interruption from future state unless the API explicitly couples them and the operation honors it.

### Publish values before readiness

The producer fully constructs result data, then publishes it into shared state with the synchronization semantics required by the runtime, then marks terminal/wakes. A waiter observes terminal through the matching acquire/lock/event mechanism before reading value.

If terminal is visible before the object graph is safely published, consumers can see partial/stale data. Immutability helps but still needs safe publication. Do not mutate a returned collection after completing unless its concurrent ownership contract permits it.

C++ promises specify synchronization between making ready and successful waiter return; Java concurrency stages have their documented memory-consistency/runtime rules; asyncio futures are event-loop objects and explicitly not thread-safe. Verify exact API rather than importing assumptions.

### Prevent lost observer registration

The dangerous sequence is: observer checks pending; producer completes and scans no waiter; observer registers and sleeps forever. Correct implementations linearize registration with completion under a lock/atomic protocol.

Conceptually, observer either registers while state is pending, after which winner wakes/schedules it, or observes terminal and schedules/returns immediately. Handle removal/cancellation races without freeing a waiter node still reachable by completion. Memory reclamation is part of correctness in low-level implementations.

Polling futures add a related contract: if poll returns pending, it must arrange a wake when progress may be possible; the executor later polls again. Poll must not block and consumers must tolerate spurious/coalesced wakes. The Rust `Future`/`Waker` contract is one example.

### Complete failures and abandonment

Producer exceptions must cross into the shared state. Catch at the computation boundary and complete exceptionally while preserving safe cause/context. Do not merely log and leave pending. Consumer APIs may wrap failures (`ExecutionException`, completion wrapper) or rethrow directly; preserve root cause and operation identity without leaking secrets.

If the producer capability is destroyed/abandoned before completion, some systems produce `broken_promise`; others require explicit cleanup. Define abandonment so consumers cannot wait forever. Process crash cannot update in-memory futures, so higher-level timeout/supervision/durable recovery is required.

Unobserved exceptional futures need reporting. A fire-and-forget result still needs a supervisor/error sink. Garbage collection/finalization timing is not a reliable operational alert.

### Choose observation mode

Blocking `get/wait` is suitable only on threads allowed to block with independent completion capacity and deadlines/cancellation. It is unsafe on UI/event loops, a single Active Object scheduler, or a saturated pool whose queued child must complete the future.

Async `await` suspends the logical task and returns its execution thread to the runtime. This avoids thread blocking but not dependency cycles, memory retention or absent producers. Callback/continuation style avoids waits but exposes execution context and reentrancy.

Completion queues/as-completed iteration let consumers process whichever result arrives first rather than submission order. This improves latency and resource release but needs correlation and explicit output ordering when required.

### Control continuation execution

A non-async continuation may run in the completing thread. If it blocks, calls untrusted code, takes locks, performs I/O or recursively completes long chains, it delays producer cleanup and other completions. Async continuation without an explicit executor may use a common pool shared with unrelated workloads.

Specify an executor/loop for each class of continuation. Keep inline stages tiny, pure and nonblocking. Isolate blocking or tenant-controlled work behind bounded execution. Propagate only intended security/tracing/context values; thread-local context at eventual execution may be stale or belong to another request.

Long synchronous completion chains can overflow stacks or monopolize a thread. Use trampolining/scheduling/batch budgets where the runtime does not. Preserve ordering and exception semantics when introducing async boundaries.

### Compose values, not nested futures

`map/thenApply` transforms (T\to U). When function returns a future (T\to Future<U>), use `flatMap/thenCompose` to flatten; otherwise consumers receive `Future<Future<U>>`, cancellation/failure ownership fragments and completion timing is misleading.

Sequential composition passes success forward and propagates failure/cancel unless recovered. Recovery operators must distinguish expected domain fallbacks from programmer/fatal failures; broad recovery can silently convert outages/corruption into plausible values. Finalization/`whenComplete` must not replace the original failure accidentally unless specified.

Model the dependency graph. Cycles (`A` awaits `B`, `B` awaits `A`) cannot complete. Graph nodes consume memory even without threads. Bound depth, fan-out, captured data and concurrent roots.

### Combine multiple futures

`all/zip` waits for all and returns ordered results under a declared failure policy: fail fast versus collect all, cancellation propagation, partial-result availability and cleanup. Fail-fast result completion does not mean sibling tasks stopped. Await/reap losers to release resources and capture additional failures.

`any/first-success` differs from `race/first-terminal`. A race may return the fastest failure even if a later success would be useful. First-success must define aggregate failure when all fail. If two complete concurrently, winner selection may be nondeterministic.

Hedging/speculation creates duplicate work/effects. Use only idempotent/read operations or stable effect identity/conditional writes. Cancel and reap losers, limit duplicate load, and measure tail benefit versus downstream cost.

### Make timeout semantics explicit

A timed `get` commonly times out the waiting thread only; future and computation remain pending/running. A timeout combinator may win the shared result with exceptional timeout while underlying work continues. A deadline propagated into the computation may request cooperative cancellation. These are different contracts.

Use one monotonic end-to-end deadline and remaining budget across stages. On timeout, stop new dependent work, request cancellation if safe, continue reaping actual outcome, and reconcile effects. Late success may be ignored for response but still release resources/update effect ledger.

Do not schedule one timer per future without capacity analysis. Timer queues, callbacks and cancellation tombstones are resources.

### Treat cancellation as a protocol

Identify who may cancel and scope: observer alone, shared result for all, or underlying computation tree. One consumer of a shared future cancelling should not necessarily cancel work needed by others. Reference/interest counting may help but races with completion and new observers.

Queued work can often be removed/skipped. Running work cooperatively checks a token or operation-specific cancellation. External calls may finish. The terminal future winner and actual effect can diverge; retain stable operation/effect identity.

Structured concurrency makes parent cancellation propagate to children and requires join/reap before scope exit. This improves ownership but precise failure/cancellation rules vary by runtime. A detached future needs an explicit supervisor.

### Avoid executor and lock deadlocks

Never block while holding a lock needed by the producer/continuation. Never run a callback under the result-cell internal lock. Copy/schedule registrations after safely detaching them.

Pool starvation occurs when all workers wait for futures whose producers are queued in the same pool. Active Object self-wait is the single-thread case. Use asynchronous composition, structured task scopes, separate/accommodating executors, inline/helping semantics known to the runtime, or reserve capacity. Increasing pool size is not a general proof.

Cross-executor cycles need a wait-for graph. Timeouts do not undo already-acquired resources/effects.

### Bound concurrency and retention

Futures do not provide backpressure. Creating a million futures can launch/queue a million computations and retain inputs, result cells, callbacks, traces and outputs. Limit in-flight roots, executor queues, bytes, dependencies, per-tenant work and completion backlog.

Consume results promptly and release captured data after terminal delivery. Shared futures can retain large results until the last observer releases. Cache futures carefully: failed/cancelled entries, stampedes, expiry and tenant authorization need policy. A future graph can retain whole request contexts through one closure.

### Integrate authority and security

Capture minimal explicit principal/tenant/authorization metadata. Revalidate current authority before sensitive effect or delivery when time can pass. Do not let completion on a reused session reveal another tenant's data; correlate owner/generation.

Exceptions/traces can contain secrets. Sanitize cross-boundary failures while preserving protected diagnostics. Limit observer registration and continuation code to prevent memory/CPU denial. A client should receive a read capability, not producer completion authority.

### Shut down and recover

Close creation/admission, cancel or drain computations by policy, complete/reject promises that will never run, propagate cancellation through owned scopes, keep executors/event loops/result delivery alive, reap every branch, record unresolved external effects, then destroy shared infrastructure.

A promise whose producer is removed during shutdown must become terminal, not remain pending. Do not stop the continuation executor before cleanup stages run. Restart cannot restore arbitrary in-memory futures; durable operations need an operation/status store and clients reconnect by stable ID.

### Observe and verify

Measure created/pending/terminal counts/bytes/age; outcomes and double-completion attempts; producer/queue/service-to-completion latency; waiter/continuation count, scheduling delay, executor and inline duration; blocked gets by thread class; graph depth/fan-out/cycles; cancellations/timeouts versus actual outcomes; unobserved failures; race/all losers; retained results; broken/abandoned promises; external effects; and shutdown residue.

Model the cell. Test every pair/order of complete-value, failure, cancel, timeout, abandon, register, unregister and shutdown. Use barriers to race registration/completion, memory/race tools, spurious wakes, callback exception/reentrancy, inline recursion, pool starvation, graph cycles, loser cleanup, result retention, event-loop thread checks, process crash and restart reconciliation.

### A finite executable model

This deterministic result cell demonstrates registration, single-assignment winner, losing cancellation/double completion, shared observation and pure mapping. It does not execute threads, atomics, memory ordering, blocking, executors, computation cancellation or external effects.

<!-- bijux-verify: {"id":"sepat-078-single-assignment","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"state=pending waiters=2\ncomplete=value:42 winner=producer notified=2\ncancel=lost state=success\ncomplete_again=ignored\nobserve=c1:42,c2:42\nmapped=84\ninvariant=single_assignment:true terminal:true\n","stderr":""}} -->
```python
class ResultCell:
    def __init__(self):
        self.state = "pending"
        self.value = None
        self.waiters = []
        self.wins = 0

    def add_waiter(self, name):
        self.waiters.append(name)

    def complete(self, value):
        if self.state != "pending":
            return False
        self.value = value
        self.state = "success"
        self.wins += 1
        return True

    def cancel(self):
        if self.state != "pending":
            return False
        self.state = "cancelled"
        self.wins += 1
        return True

    def observe(self, name):
        if name not in self.waiters or self.state != "success":
            return None
        return self.value


cell = ResultCell()
cell.add_waiter("c1")
cell.add_waiter("c2")
print(f"state={cell.state} waiters={len(cell.waiters)}")

won = cell.complete(42)
print(f"complete=value:{cell.value} winner={'producer' if won else 'none'} notified={len(cell.waiters)}")
cancelled = cell.cancel()
print(f"cancel={'won' if cancelled else 'lost'} state={cell.state}")
again = cell.complete(99)
print(f"complete_again={'won' if again else 'ignored'}")

first = cell.observe("c1")
second = cell.observe("c2")
print(f"observe=c1:{first},c2:{second}")
print(f"mapped={first * 2}")
single = str(cell.wins == 1).lower()
terminal = str(cell.state != "pending").lower()
print(f"invariant=single_assignment:{single} terminal:{terminal}")
```

## Definitions and Notation

Let result state (F_r\in\{pending,success(v),failure(e),cancelled(c)\}); computation state (C_r\in\{not_started,running,stopped,completed\}); client interest (I_r); and external effect state (E_r). Let (W_r) be observers/continuations and (X_r) their executors.

Dependency graph (G=(V,E)) contains one node per computation/result stage and edge (u\to v) when v requires u. `map` adds value transformation; `flatMap` adds and flattens an asynchronous dependency. Deadline (D) is monotonic; result/computation/effect identities remain stable across retries/reconciliation.

## Mechanisms, Invariants, or Proof Structure

### Single-assignment argument

Assume every terminal mutation uses one linearized compare/lock transition from pending and no terminal-to-terminal overwrite is exposed. At most one contender observes/changes pending successfully, so exactly one local terminal outcome wins when at least one valid completion occurs. This says nothing about how many computations/effects occurred.

### Publication argument

Assume value/failure initialization happens before the release/terminal publication and observer terminal read uses the matching acquire/synchronization. Then observers that see terminal also see initialized result state. This depends entirely on the language/runtime primitive and correct alias ownership.

### Registration argument

Assume registration is linearized with completion. A registrar either joins pending waiter state before completion scans/detaches it, or observes terminal and schedules immediately. Thus no accepted observer remains pending solely because completion occurred between check and registration. Safe node reclamation and callback scheduling remain implementation obligations.

### Composition and liveness limits

An acyclic dependency graph whose producers eventually run/terminate and whose executors make progress can complete under operator failure rules. A cycle or exhausted worker set of blocking waiters can prevent progress. Single assignment is safety, not liveness, capacity, fairness or structured cleanup.

### Evidence boundaries

Finite models can check terminal races and operator state tables. Race/memory tests sample concrete schedules. Runtime specifications establish only their APIs. Latency, cancellation effectiveness, executor fairness, security, durability and external effects require empirical/system evidence.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Appropriate use |
| --- | --- | --- | --- |
| Future/promise | One-shot typed result and composition | Hidden execution/cancel/context unless specified | Eventual single result |
| Callback | Minimal abstraction/streaming integration | Inversion, lifetime/error nesting | Low-level event APIs |
| Async/await | Sequential syntax over futures | Backend/cancellation/context still present | Structured asynchronous flows |
| Completion queue | Process results in completion order | Correlation and output reorder | Many independent tasks |
| Channel/stream | Multiple values and backpressure potential | Close/error/subscription semantics | Repeated results/events |
| Actor reply message | Ownership and supervision | Message correlation/mailbox semantics | Actor systems |
| Blocking direct call | Simple stack/error ownership | Temporal coupling/thread blocking | Fast local bounded work |
| Durable operation resource | Survives restart/status lookup | Storage/distributed state complexity | Long-running external operations |
| Structured task scope | Owned cancellation/join/failure policy | Runtime-specific constraints | Bounded child parallelism |

Shared futures support many readers but retain result and complicate cancellation interest. Lazy futures defer work but need polling/executor and may never start. Eager futures reduce latency but consume resources immediately. Default executors are convenient but create hidden coupling.

## Failure Modes and Misconceptions

- **“Future means work is running.”** It may be lazy, queued, completed or disconnected from execution.
- **“Done means success.”** Failure and cancellation are terminal too.
- **“Cancel stops the operation.”** It may only complete observation exceptionally.
- **“Timeout cancels work.”** Timed waiting often leaves work/effect running.
- **“Single assignment means exactly-once effect.”** It constrains one result cell only.
- **“Await cannot deadlock.”** Cyclic dependencies and executor starvation remain.
- **“Callbacks run later elsewhere.”** They may run inline on the completing thread.
- **“Async suffix means dedicated resources.”** It may use a shared default/common executor.
- **“Map handles async functions.”** It produces nested futures unless flattened.
- **“All fail-fast stops siblings.”** Losers usually require explicit cancellation/reaping.
- **“Race cleans losers.”** It chooses a result; resources/effects remain.
- **“One exception is the whole failure.”** Multi-branch composition can have multiple causes.
- **“Future values are immutable.”** Publication does not prevent later producer mutation.
- **“Dropping the future stops work.”** Detached work may continue and failures vanish.
- **“A million futures use no threads, so they are cheap.”** Cells, captures, timers, tasks and results retain memory/resources.
- **“Process restart can resume the future.”** In-memory identity/state is gone without durable operation protocol.

## Worked Examples

### Example 1

**Situation.** Success, timeout and cancellation attempt to complete one result concurrently.

**Reasoning.** One atomic terminal transition wins. Record loser attempts for diagnosis. If timeout/cancel wins the result, the successful underlying write may still be real; reap it under stable effect identity.

**Conclusion.** Terminal arbitration and effect reconciliation are separate.

### Example 2

**Situation.** A consumer checks `pending`, then the producer completes before the consumer adds itself to a callback list.

**Reasoning.** An unsynchronized implementation loses the callback. Linearize registration with completion: register-before-winner or observe-terminal-and-schedule. Test with controlled barriers and safe reclamation.

**Conclusion.** Result cells require atomic check/register semantics.

### Example 3

**Situation.** A worker in a one-thread pool submits child work to the same pool and blocks on its future.

**Reasoning.** The child cannot start while its only worker waits. Compose asynchronously, execute child inline under safe semantics, use a structured/helping scheduler, or separate capacity. A timeout only delays failure.

**Conclusion.** Blocking wait must not consume required completion capacity.

### Example 4

**Situation.** A non-async continuation performs a slow database call when the I/O completion thread fulfills the future.

**Reasoning.** The completion thread executes it inline under the runtime policy and stops reaping unrelated I/O. Keep inline transformation tiny or specify a bounded blocking executor; propagate deadline/context explicitly.

**Conclusion.** Continuation executor is part of the API contract.

### Example 5

**Situation.** `map(user -> fetchProfile(user))` returns a future-valued function.

**Reasoning.** Mapping creates `Future<Future<Profile>>`; outer success only means inner creation. Use flat-map/compose so result, error and cancellation chain match intended profile outcome. Still define cancellation propagation.

**Conclusion.** Asynchronous dependencies require flattening.

### Example 6

**Situation.** `all` over five writes fails fast on one future while four writes continue.

**Reasoning.** Preserve first/aggregate failure policy, request safe cancellation, await/reap every sibling, release buffers and reconcile each write effect. Do not return while orphaned resources remain if scope owns them.

**Conclusion.** Aggregate terminal state does not clean child computations automatically.

### Example 7

**Situation.** A hedge races two replicas and returns the first successful read.

**Reasoning.** Limit hedges, share stable request identity, cancel/reap loser and measure downstream amplification. Hedging writes can duplicate effects and is unsafe without conditional/idempotent protocol.

**Conclusion.** Race improves tails only with loser and effect control.

### Example 8

**Situation.** A promise owner exits exceptionally without completing the future.

**Reasoning.** The boundary catches and completes failure, or a runtime broken-promise state wakes observers. Log/trace protected cause. Never leave pending state dependent on garbage collection.

**Conclusion.** Producer abandonment needs terminal semantics.

### Example 9

**Situation.** A session closes, but its old future later completes with sensitive account data.

**Reasoning.** Correlate owner/generation and revalidate delivery authority. Reap/release result but do not deliver to a reused session. Clear captured principal/payload and bound future retention.

**Conclusion.** Future identity must include lifecycle and authority context.

### Example 10

**Situation.** An emergency-control command future times out before device acknowledgement.

**Reasoning.** Timeout stops waiting/response, not necessarily command effect. Track command, controller/device generations, authority, sequence and effect ID in a durable ledger; query physical outcome, prevent unsafe retry, and enter defined fail-safe state. Named safety review validates policy.

**Conclusion.** High-stakes futures require durable effect truth beyond local completion.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md): type systems, exceptions, async lowering, pinning/wakers and memory models implement futures.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): controlled races, virtual time, executor saturation, fault injection and model checking verify cells/graphs.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): completion authority, context capture, stale delivery, exception leakage and resource exhaustion constrain futures.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): deadlines, cancellation, hedging, ambiguous effects, durable operations and reconciliation extend local state.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): asynchronous operation resources, status/cancel endpoints and polling/webhooks expose future semantics remotely.
- [SEPAT-075](075-thread-pool.md) supplies execution; [SEPAT-076](076-active-object.md) returns futures; [SEPAT-077](077-monitor-object.md) can implement blocking state coordination.

## References

1. Oracle. “CompletableFuture,” Java SE 25 API. Completion arbitration, execution policy, cancellation and timeouts. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletableFuture.html>. Accessed 2026-08-29.
2. Oracle. “CompletionStage,” Java SE 25 API. Composition, failure and execution semantics. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletionStage.html>. Accessed 2026-08-29.
3. Python Software Foundation. “Futures,” Python 3.14 asyncio documentation. <https://docs.python.org/3/library/asyncio-future.html>. Accessed 2026-08-29.
4. Python Software Foundation. “concurrent.futures,” Python 3.14 documentation. <https://docs.python.org/3/library/concurrent.futures.html>. Accessed 2026-08-29.
5. Rust Project. “Trait Future,” Rust standard-library documentation, 1.97. <https://doc.rust-lang.org/stable/std/future/trait.Future.html>. Accessed 2026-08-29.
6. ISO C++ Working Draft. “Futures,” current draft section 32.11. <https://eel.is/c++draft/futures>. Accessed 2026-08-29.
7. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000. Futures in Active Object and asynchronous patterns.
8. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Futures, task cancellation, liveness and executor deadlock.
9. Lea, Doug. *Concurrent Programming in Java*, 2nd ed. Addison-Wesley, 1999.
10. Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*, revised 1st ed. Morgan Kaufmann, 2012.
11. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018. Timeouts, resource control and stability.
12. Adya, Atul, et al. “Cooperative Task Management without Manual Stack Management.” USENIX ATC, 2002. Event-driven asynchronous control.

Future thread-safety, memory visibility, wake/poll, cancellation, completion/continuation context, default executors, timeout, abandonment and shutdown vary by runtime/library version. Current official specifications were checked on 2026-08-29; verify exact deployed semantics.

## Exercises

### Exercise 1

Specify a Future/Promise shared-state protocol for multiple observers. Define states, capabilities, publication, registration, completion/cancel/abandon races, observer removal, continuation execution, cleanup and at least eight invariants.

### Exercise 2

A service creates 2,000 pending futures. Each retains at most 24 KiB input and 8 KiB result/metadata budget. Stable completion rate is 500/s and mean future residence is 3 s. Compute declared maximum retained bytes and average resident futures from Little's Law; interpret the mismatch and limitations.

### Exercise 3

Design a composition that queries three replicas, returns the first valid success before a 200 ms end-to-end deadline, aggregates failures if all fail, cancels/reaps losers, bounds hedges and preserves authority/trace. Cover every outcome.

### Exercise 4

Diagnose a system that exposes completers to clients, mutates results after completion, uses check-then-register callbacks, blocks event loops and same-pool workers, relies on common-pool continuations, maps async functions without flattening, assumes timeout cancels writes, leaks race losers and abandons futures at shutdown. Provide remediation/tests.

### Exercise 5

Design future/promise semantics for a safety-critical air-traffic command system. Address identity, authority, single assignment, execution/effect states, deadlines/cancellation, composition, fail-safe behavior, persistence/restart, security, observability, verification and named external review.

## Answers to the Exercises

### Answer 1

One shared state has stable operation ID/generation, tag `pending|success|failure|cancelled`, value/error/reason, protected observer registrations, authorized promise capability, restricted futures, computation link, deadline, trace and cleanup. Producer initializes value/error then atomically transitions pending terminal with release semantics; observers register atomically with completion and observe terminal with matching acquire. Exactly one terminal contender wins; losers observe failure. Producer exception/abandonment/shutdown completes failure rather than pending forever.

Observers can await repeatedly where the API supports shared observation. Removal/cancel marks a registration without freeing reachable state unsafely; cancelling one observer does not cancel shared computation unless policy/interest count permits. Continuations detach/schedule outside internal lock on explicit bounded executors, with bounded context and exception propagation. Cleanup releases captures/result after all owned observers/branches are terminal.

Invariants include restricted completion authority; one terminal state; initialized-before-ready visibility; no lost registration; exactly-once scheduling per registered continuation contract; every accepted producer terminal/abandoned; future cancel separate from computation/effect; no callback under cell lock; no blocking on required completion executor; bounded registrations/captures/graph; explicit branch loser cleanup; generation/current-authority delivery; and shutdown terminally resolves every owned cell.

### Answer 2

Per future budget is (24+8=32\) KiB, so declared maximum is

\[
2000\times32\text{ KiB}=64{,}000\text{ KiB}=62.5\text{ MiB}.
\]

Little's Law predicts

\[
L=\lambda W=500\times3=1500
\]

average resident futures for the stable measured boundary. Two thousand capacity provides 500 above that average, not a tail guarantee. The gap may absorb bursts or reflect overprovisioning; it cannot be judged without distributions/deadlines.

The byte budget excludes object graphs, waiters, continuations, timers, executor queues, threads, external resources, allocator overhead and shared results. Stable averages do not bound bursts/correlations or prove completion capacity. The math verifies no publication, race, cancellation, failure, security, fairness or effect property.

### Answer 3

Create one parent scope with request/tenant/authority/generation, monotonic 200 ms deadline and three child identities. Global/per-tenant hedge admission limits concurrency/bytes and downstream load. Start permitted replica reads with remaining deadline, validate each result schema/integrity/freshness/authorization before it can win a first-valid-success cell. Failures are recorded by replica; a raw fastest response cannot win before validation.

On first valid success, atomically complete parent, request cancellation of other children, but continue reaping them and release sockets/buffers. Deliver only if owner generation/current authority remains valid. If all terminal without valid success, complete aggregate typed failure preserving bounded protected causes. If deadline wins, complete timeout, cancel/request stop, reap late outcomes and do not cache/deliver stale data. If cancellation wins, follow shared-versus-single-observer policy.

Use explicit nonblocking executors/loop, no common hidden blocking, stable trace IDs and sanitized errors. Tests cover every order of three success/failure/invalid/timeout/cancel outcomes, simultaneous wins, deadline boundary, late valid success, loser ignoring cancel, one/all replicas down, overload rejection, auth/session change, memory/resource cleanup and executor saturation.

### Answer 4

Exposed completers allow forged/double outcomes; post-completion mutation breaks value ownership; check/register loses callbacks; blocking consumes progress capacity; common pool causes interference; map creates nested futures; timeout/future state does not stop writes; race losers leak; shutdown strands waiters.

Expose restricted read stages only. Copy/freeze/exclusively transfer values and publish before terminal. Implement/use a proven atomically registered cell. Replace event-loop/same-pool blocking with await/composition or independent structured capacity; set explicit bounded executors and keep inline stages tiny. Flat-map asynchronous functions. Carry monotonic deadlines/cancel tokens into work but reconcile actual writes under stable effect ID. Every race/all branch is cancelled where safe and always reaped.

Shutdown stops roots, terminally fails never-started promises, propagates cancellation, awaits owned branches, keeps continuation/result paths alive, records unresolved effects, then tears down. Test completion/register/cancel/timeout/abandon pairs with barriers; memory publication/alias sentinels; event-loop checks; one/saturated pool deadlocks; callback exceptions/recursion; nested flattening; common-pool isolation; late writes; loser cleanup; retention; process crash/restart and zero pending residue.

### Answer 5

Assign command/flight/controller/session/device and future/computation generations, authenticated authority/policy version, monotonic sequence/deadline, effect/idempotency identity, classification and audit trace. Restricted observers receive a read-only future; only the command coordinator can complete. One result cell arbitrates accepted/rejected/issued/acknowledged/failed/cancelled observation, but maintain separate computation, transport, device and physical-effect states in a protected durable ledger.

Deadline/cancellation stops new work and requests safe cancellation but cannot erase issued effects. Query/reconcile late/ambiguous acknowledgements; retries use stable identity/sequence and conditional device protocol. Composition of redundant channels uses first *validated* outcome, aggregates failures, bounds duplicate load and reaps all losers. Authority/session/generation is revalidated before delivery/effect; uncertainty triggers hazard-approved fail-safe behavior.

Persist command/effect status rather than future objects; after restart reconstruct read/status handles from stable IDs and reconcile controller/device physical state before commands resume. Apply mutual authentication, least privilege, replay protection, encryption, sanitized failures, protected/tamper-evident audit, quotas and context minimization. Observe every result/computation/effect transition, completion races, deadline slack, channel/continuation latency, cancel/late/duplicate, authority changes, unresolved effects and recovery.

Verification includes formal state/sequence models, model checking of winner and channel composition, hardware-in-the-loop, concurrent completion races, scheduler/network/device/power/process failure, overload, stale/duplicate/late acknowledgements, security/adversarial tests, fail-safe and restart drills, and worst-case timing. Production claims require named air-traffic/domain/safety, controls/concurrency, communications, human-factors, security, reliability/operations and regulatory reviewers with traceable hazards and acceptance evidence.
