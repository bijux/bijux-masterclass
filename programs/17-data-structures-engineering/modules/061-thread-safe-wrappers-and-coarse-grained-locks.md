---
module_id: DSE-061
program: Data Structures Engineering
level: 2
module_number: 61
title: Thread-Safe Wrappers and Coarse-Grained Locks
status: complete
last_verified: 2026-08-30
---

# Thread-Safe Wrappers and Coarse-Grained Locks

## One-Page Review

### Governing question

When does placing one mutex around a mutable data structure produce a linearizable, memory-safe, failure-safe concurrent object—and where do callbacks, leaked aliases, compound client actions, multiple wrappers, cancellation, lifecycle, and contention invalidate the simple story?

### Essential definitions

- A **thread-safe wrapper** owns or mediates a non-thread-safe core and exposes a concurrency contract.
- A **mutex** permits at most one successful holder in the protected critical section and supplies memory-ordering guarantees defined by its language/runtime.
- A **critical section** is code executed while holding the protecting lock.
- **coarse-grained locking** protects the object's whole mutable abstract state with one lock.
- A **representation invariant** is a predicate that must hold whenever the object is externally observable outside an in-progress operation.
- **linearizability** requires each completed concurrent operation to appear at one point between invocation and response while respecting real-time order.
- A **linearization point** is the proof point at which one operation's abstract effect takes place; it need not literally be the lock acquisition.
- **happens-before/synchronizes-before** is the memory-model relation that makes protected writes visible to later synchronized reads.
- **reentrancy** permits the owning thread to acquire the same lock repeatedly; it changes self-deadlock behavior, not the need for invariants.
- **lock convoying** is throughput/tail degradation when threads queue behind a delayed holder.
- **priority inversion** occurs when a high-priority thread waits for a lower-priority holder, potentially extended by unrelated runnable work.

### Central model, mechanism, or theorem

Let sequential object `S` have operations that preserve invariant `I`. A wrapper owns `S`, exposes no unsynchronized mutable aliases, and uses one mutex `L`. Every public state-reading/mutating operation acquires `L`, validates inputs as specified, executes one complete sequential operation, restores `I`, and releases `L` in all exits. Because critical sections do not overlap, order them by their protected abstract effects. That total order respects nonoverlapping real-time calls and is a legal sequential history, yielding a direct linearizability proof.

The mutex also supplies the language's release/acquire synchronization: writes before unlock become visible to a later successful lock according to the memory model. Mutual exclusion alone is not a portable visibility proof without that specified relation.

The theorem fails when callers can mutate the core directly, a returned iterator/view/reference observes later unsynchronized mutation, a read omits the lock, one method temporarily releases it, callbacks reenter/escape/block, or a client needs `get`-then-`put` to be one atomic operation. Coarse locking serializes all protected operations; its simplicity is valuable, but maximum throughput is bounded by critical-section service and queueing/tails grow under contention.

### Critical invariants

1. One documented lock protects every field participating in the abstract state and its metadata.
2. The core, mutable elements, iterators/views, and mutation-capable callbacks never escape the synchronization contract.
3. Every public read, write, size, equality, iteration/snapshot, serialization, validation, and diagnostic path uses the correct lock or an explicitly immutable snapshot.
4. Each method has a legal abstract effect and linearization point between invocation/response, including failure/no-op cases.
5. Invariant restoration and lock release occur on success, exception, cancellation, timeout, and resource failure.
6. Blocking I/O, unbounded computation, logging hooks, destructors/finalizers, and arbitrary user callbacks do not execute under the lock unless explicitly designed/audited.
7. Multi-object operations follow one global lock order or a deadlock-avoiding protocol; lock ownership is not guessed.
8. Condition waits test a predicate in a loop while holding the associated mutex and account for timeout/cancellation.
9. Close/reset/fork/serialization/destruction policy accounts for active holders, waiters, and exported snapshots/handles.
10. Correctness evidence covers histories/schedules/failures; performance evidence covers contention, hold/wait distributions, fairness/starvation, and deployment workload.

### Common failures

- Locking writes but not reads, `len`, iteration, equality, formatting, or validation.
- Returning the underlying collection, live view, iterator, mutable element, or internal node.
- Implementing `contains` plus `insert` as two individually locked calls when atomic put-if-absent is required.
- Holding the lock while invoking unknown callbacks or performing network/disk I/O.
- Forgetting release on exception because acquire/release is not structured with RAII/context/finally.
- Replacing a nonreentrant lock with a reentrant one to hide a confused call graph; invariants may be visible halfway through an operation.
- Assuming one lock prevents deadlock even when methods acquire other wrapper/resource locks or callbacks reenter.
- Treating lack of race-detector reports or one correct final count as a linearizability proof.
- Promising fairness because current scheduling appeared FIFO.
- Optimizing to fine-grained locking before specifying the abstract concurrent contract and evidence.

### Compact example

A `LockedMap` privately owns a Python dictionary and one `Lock`. `put`, `get`, `snapshot`, and `stats` acquire it with `with`, so release occurs on exceptions. Four threads begin at a barrier and write disjoint keys 0–11. After joining, a locked snapshot contains all squares; mutating the snapshot cannot mutate the wrapper. The exact finite run validates size, keys, sum, write count, join, and snapshot isolation, but does not prove arbitrary schedules, fairness, performance, language-independent memory behavior, or future methods.

### Connections

[DSE-002](002-representation-invariants.md) supplies representation ownership; [DSE-060](060-measuring-persistent-structure-time-and-memory.md) supplies rigorous contention/memory evidence; [DSE-038](038-binary-and-d-ary-heaps.md) offers a mutable core example. The [program roadmap](../ROADMAP.md) next narrows locking granularity and then studies concurrent maps, queues, atomics, nonblocking progress, reclamation, and linearizability testing.

## Governing Question

Can one private lock transform a sequential data structure into a concurrent object whose complete API is linearizable, visible under the target memory model, exception/cancellation/lifecycle safe, deadlock-aware when composed, and operationally acceptable under measured contention?

## Why This Matters

A coarse lock is often the highest-leverage concurrency design. It reuses a mature sequential representation and proof, gives one obvious synchronization domain, makes compound invariants atomic, and minimizes schedules a reviewer must consider. For low contention, administration paths, caches with expensive misses outside the lock, control planes, or an initial correct implementation, this can outperform a theoretically more concurrent design in reliability and total engineering cost.

“Put a lock around it” is nevertheless incomplete. A container API includes reads, iteration, views, callbacks, equality, hashing, serialization, diagnostics, copying, close, and methods returning element references. One unlocked surface can create data races or logical inconsistency. Individual thread-safe calls do not make client sequences atomic. A callback under lock can block, reenter, acquire another lock, leak aliases, or run adversarially long.

Concurrency correctness has at least three layers. Data-race freedom prevents conflicting unsynchronized accesses according to the language. Memory ordering ensures later synchronized readers observe protected writes. Linearizability connects overlapping calls to the sequential abstract type. A program can be race-free yet implement the wrong compound semantics; a final-state test can pass while return values cannot be linearized.

Operational behavior matters too. One slow holder stops all methods—even read-only operations. Preemption, page faults, GC/safepoints, allocator stalls, I/O, callbacks, or priority scheduling can create convoys and tail spikes. Fair locks may reduce starvation in some workloads while lowering throughput; fairness contracts differ by primitive and even acquisition method.

Coarse locking should therefore be treated as a complete design with proof obligations and metrics, not a temporary embarrassment. It supplies the correctness baseline against which fine-grained or nonblocking successors must be compared.

## Prerequisites and Retrieval

Retrieve threads, processes, shared memory, race conditions, sequential specifications, invariants, exceptions, context managers/RAII, queues, scheduling, latency distributions, and graph cycle/deadlock reasoning. From [DSE-002](002-representation-invariants.md), retrieve abstraction boundaries and representation invariants.

From [DSE-060](060-measuring-persistent-structure-time-and-memory.md), retrieve semantic-equivalent baselines, experimental units, latency tails, exact counters, and profile limitations. You should understand invocation/response histories, real-time order, mutex acquire/release, deadlock wait-for graphs, cancellation, and why interpreter/runtime implementation details such as a global interpreter lock do not replace an explicit object synchronization contract.

## Learning Objectives

After completing this module, you can:

1. specify a wrapper's sequential abstract type, concurrency semantics, ownership, and protected fields;
2. give a direct linearizability proof for complete single-lock methods;
3. connect lock/unlock to visibility using the target language memory model;
4. audit every API surface for unlocked reads, live views, iterators, aliases, and callbacks;
5. design atomic compound operations rather than forcing clients to compose individual calls;
6. make exceptions, cancellation, timeouts, conditions, and lifecycle transitions safe;
7. prevent multi-object/callback deadlocks with ordering or alternative protocols;
8. compare nonreentrant/reentrant, mutex/read-write, striping, immutable snapshot, actor, and transactional designs;
9. test histories, failures, races, schedules, and invariant preservation; and
10. measure hold/wait/queue distributions, contention, throughput, fairness/starvation, and critical-section work.

## Core Exposition

**Specify the sequential object first.** Define abstract state and legal methods before threads. For a map: `get(k)` returns value/absence; `put(k,v)` associates and returns prior value or status; `remove`; `putIfAbsent`; `compute`; `snapshot`; `size`; and close/error behavior. Define comparator/hash/equality, null/duplicate policy, iteration order, element ownership, and exceptions.

Write representation invariant `I`: table shape valid, size matches entries, keys unique under equality, metadata/cache totals correspond, closed state obeys policy. Each sequential operation assumes `I` and restores `I`. The wrapper proof will rely on that existing sequential proof rather than reason about partially overlapping mutations.

**Make ownership exclusive.** Construct the core inside the wrapper or take ownership with a documented transfer after which the caller cannot use its old reference. Keep fields private. Never provide `unsafe_core()` as convenience in a public thread-safe type. If privileged internal access exists, constrain it structurally and audit every caller.

Element mutability matters. Returning a mutable value may allow changes outside the lock that violate container-level metadata or user expectations. Options: values are immutable/thread-safe; return defensive copies; return opaque handles with synchronized methods; or explicitly state the wrapper protects only container topology, not objects stored inside. The last contract can be valid but must be unmistakable.

One lock should have a durable guard comment/invariant: “`mu` protects entries, size, version, closed, and all mutable representation reachable exclusively from entries.” The lock itself is not copied or serialized as ordinary state. Avoid multiple aliases to a copyable wrapper whose copies appear independent but share the core or vice versa.

**Lock every observation.** Reads race with structural mutation and can observe intermediate invariants even when word loads are atomic. `get`, `contains`, `size`, emptiness, equality, hashing, string formatting, validation, metrics derived from protected fields, iterator creation/advance, and serialization all participate. A debug method is still code.

Some metrics can be atomic/eventually consistent outside the primary lock, but then they are not part of the exact abstract state unless a proof composes them. Document accuracy and memory ordering. Do not silently weaken `size()` because it is “only informational.”

Use structured lock management. Python locks support the context-manager pattern; C++ uses RAII guards; Java `Lock` commonly requires `lock(); try { ... } finally { unlock(); }`. The exact idiom differs, but every path after successful acquisition releases exactly once. Release by a nonowner or double release follows primitive-specific behavior and is never a recovery strategy.

**Prove linearizability.** Consider completed wrapper calls. Mutual exclusion gives disjoint critical-section intervals. Order calls by the abstract effect of their sequential operation inside the lock. Since the core satisfies `I` at entry and exit, this is a legal sequential history. If call A returns before call B is invoked, A's critical section/effect precedes B's; real-time order holds. Each effect is between invocation and response.

The linearization point depends on method semantics. A successful `put` may linearize at the table mutation. An unsuccessful `putIfAbsent` can linearize at the protected observation of an existing key. A snapshot linearizes while copying the protected state, often at some instant within that uninterrupted copy. A method failing validation before acquisition may linearize at its validation observation or be modeled as no object operation; specify it.

Lock acquisition itself is not universally the point: validation or mutation may occur later, and a method can acquire then fail without changing state. Nor is unlock always the semantic point, although it publishes completed protected writes according to the memory model.

Pending calls in a finite history require the formal definition's completion/removal treatment. For production reasoning, specify cancellation/timeouts and whether a request can have taken effect even when a caller does not receive a response. Network/API exactly-once claims need operation IDs/idempotency beyond an in-process lock.

**Memory visibility is part of the primitive.** Locks are synchronization operations under language/runtime specifications. The Go memory model states that an earlier `Mutex.Unlock` is synchronized before a later successful `Mutex.Lock` returns in the defined order. Java lock implementations must provide memory synchronization semantics equivalent to built-in monitor locks. Use the target primitive's official guarantee.

Do not infer portability from current CPU coherence or an interpreter lock. An implementation may run Python bytecode under a GIL yet release it in I/O/C extensions, and free-threaded configurations exist; multi-step abstract operations and escaped native state still need synchronization. The wrapper's lock communicates intent and correctness across supported runtimes.

**Individual methods do not compose automatically.** Client code `if not contains(k): put(k,v)` has a gap: another thread can insert between calls. Both calls may be linearizable while the compound requirement fails. Provide `putIfAbsent(k,v)` whose test and insert occur within one acquisition.

Similarly provide `compute`, `update`, `popIf`, transfer/move, compare-and-set, or batch transaction when clients require atomic read-modify-write. Specify callback semantics carefully. A generic `withLock(core -> ...)` leaks representation authority, invites blocking/reentrancy, and prevents invariant review.

For pure bounded transformations, compute from an immutable copy outside the lock, reacquire, validate a version stamp, and commit or retry. This optimistic pattern avoids long holds but changes failure/retry/starvation and callback semantics; callback side effects cannot be replayed safely. Alternatively execute a trusted internal function under lock with a strict no-block/no-reenter/no-escape contract.

**Iteration and snapshots force a choice.** Returning a live iterator after release is unsafe if it follows mutable storage. Holding the lock for the iterator's lifetime blocks everyone and relies on caller cleanup; abandonment can deadlock the object. Fail-fast modification counters detect some misuse but are not synchronization/correctness.

A common safe design copies an immutable snapshot under lock and iterates after release. Cost is `O(n)` time/space under the lock unless representation supports cheap persistent snapshots. Chunked iteration can release between chunks but no longer represents one atomic snapshot unless versioned/cursor semantics define it. Visitor callbacks under lock inherit callback hazards.

Serialization similarly copies/encodes. Encoding under lock gives one snapshot but may block/I/O. Better capture immutable state/bytes-to-encode under lock, then perform expensive formatting/write outside; ensure captured mutable elements cannot change. Deserialization normally builds/validates a fresh core before acquiring to swap atomically.

**Callbacks are unknown code.** Equality/hash/comparator functions may be user-defined and execute while table operations hold the lock. They can block, acquire locks, call back into the wrapper, throw, or mutate keys. Restrict key/value operations, document callback-under-lock behavior, snapshot before callbacks, or select a representation that evaluates them outside with a validation/commit protocol.

Logging, tracing, metrics exporters, allocation hooks, destructors/finalizers, and error formatting are callbacks too. A log sink can acquire another lock or block on I/O. Collect minimal event data under lock and emit after release when ordering semantics permit.

Nonreentrant locks turn same-thread callback reentry into self-deadlock, making an unsafe path visible. Reentrant locks permit entry but may expose an invariant halfway through an outer operation or let callbacks make surprising nested changes. Reentrancy is a contract, not a universal fix. Track hold counts/ownership only through supported APIs.

**One wrapper can still deadlock in a system.** Internally one lock eliminates cycles consisting solely of that object's lock, but a method can hold it then acquire resource B while another thread holds B then calls the wrapper. Two wrapper transfer/compare operations can acquire A then B versus B then A.

Choose a total global lock order by stable, nonreused identity and acquire in ascending order; handle identical objects once. Or use `std::lock`-style deadlock avoidance, try-lock/backoff with bounded/cancellation behavior, a coordinator lock, immutable snapshots, actor/message ownership, or redesign to avoid simultaneous holds. Never order by attacker-controlled mutable keys or raw addresses whose reuse/lifetime makes policy ambiguous without analysis.

Document external-callback lock freedom so arbitrary code cannot add hidden edges to the wait-for graph. Static lock-order annotations/tools help but do not model every dynamic resource. Timeouts detect symptoms and bound waiting; they do not make partially executed operations safe or prove absence of deadlock.

**Failure must preserve invariant and publication.** Validate cheap untrusted arguments before locking when validation does not depend on state. Inside lock, allocations/hash/equality/core methods can fail. Sequential exception safety must leave `I` restored or unchanged. Structured release prevents a permanently held lock but cannot repair a half-mutated core.

Use transactional staging, rollback, copy-and-swap, or core operations with strong/basic exception guarantees appropriate to the abstract contract. Define whether failed methods have no effect, may make a documented partial effect, or poison/close the object. Most container APIs should prefer no visible partial mutation.

Cancellation can occur while waiting or inside the operation depending on runtime. Interruptible/timed acquisition must distinguish not-acquired from acquired. Once mutation starts, defer cancellation to a safe point or roll back. A timeout returned to a remote caller may race with successful completion; idempotency/status lookup is needed.

**Conditions coordinate predicates, not events.** A bounded wrapper may need `not_empty`/`not_full` conditions associated with the same mutex. A waiter acquires the lock, loops while the predicate is false, waits (atomically releasing/reacquiring according to the primitive), then rechecks. Loops handle spurious wakeups and another thread consuming the condition first.

Mutation establishes the predicate under lock and signals according to policy. Signal versus broadcast trades wakeups and progress. Timeout uses a monotonic deadline and recomputes remaining time; cancellation/close must wake waiters and produce specified errors. A notification without protected predicate state can be lost.

**Lifecycle is concurrent state.** `close()` should acquire the lock, atomically mark closed, preserve/read policy for existing data, and wake waiters. New operations reject after the close linearization point. Decide whether in-progress holders finish, whether close waits, and how destruction ensures no active thread can access freed mutex/core.

Forking a multithreaded process can inherit a lock held by a vanished thread; follow platform/runtime post-fork restrictions or reinitialize only under a proved protocol. Serialization stores logical state/configuration, not a live mutex/owner/wait queue. Copying may create an independent snapshot with a new lock or be forbidden; shallow copying the lock/core relationship is dangerous.

**Progress and fairness are separate from safety.** A blocking mutex implementation can suspend a contender. Linearizability says nothing about starvation, deadlock freedom, lock freedom, fairness, or bounded latency. State the primitive's guarantees rather than observing queue order.

Java `ReentrantLock` offers optional fairness, but untimed `tryLock()` can barge even on a fair lock; fairness may reduce throughput. Python's documentation does not promise which blocked waiter proceeds. Scheduler priority and mutex protocol decide priority inversion behavior; priority inheritance/ceiling are platform-specific choices.

Minimize *necessary* critical work without splitting the invariant accidentally. Precompute state-independent inputs, allocate/stage when safe, perform protected validation/commit, and move I/O/logging/destruction outside. Moving code out can introduce time-of-check/time-of-use races; use version stamps or immutable captures.

**Contention forms a single serialized service center.** If every operation holds the lock for service time `S`, protected work cannot complete faster than roughly one holder at a time; throughput cannot exceed the reciprocal of average service demand under the model, before overhead. As utilization approaches saturation, queueing and tail latency rise sharply. Actual scheduling, mixed service times, batching, NUMA, cache transfer, and think time require measurement.

Measure per-operation lock wait, hold, total latency, acquisitions, contended acquisitions/parks/spins, queue length where supported, throughput, CPU, context switches, fairness/starvation, and p50/p95/p99/max grouped by method. Instrumentation changes timing; use separate/profiled runs and mature tools. Correlate long holds with code paths without logging synchronously under the lock.

Test 1, 2, ... threads; read/write mixes; key skew; small/large state; short/long callbacks excluded or controlled; preemption/GC/allocation; burst/steady arrivals; CPU oversubscription; priorities; cancellation; and production traces. Compare semantic-equivalent alternatives. The single-lock wrapper is the correctness baseline.

**Verification must explore histories.** Unit tests cover sequential methods/invariants. Concurrent tests record invocation/response, arguments/results, and check whether a legal sequential history respecting real time exists for bounded cases. A correct final map is insufficient: returned prior values, failures, and snapshots matter.

Stress with randomized schedules, barriers, yields/delays at instrumentation points, many seeds, and repeated fresh processes. Use race detectors such as ThreadSanitizer for supported compiled languages; they find classes of data races, not linearizability/deadlock/progress proofs. Run lock-order/deadlock detection where available.

Fault inject allocation/hash/equality/callback errors, cancellation before/during wait, timeout edges, close, serialization, and thread termination. Model-check small state/schedules when risk warrants. Review every new method against the guard/escape/linearization checklist; concurrency safety is not inherited automatically by future code.

**Security shares the lock.** An attacker controlling keys, equality/hash, callback duration, input size, or a slow streaming consumer can monopolize the critical section and deny service. Bound work/size, restrict callbacks, apply deadlines outside safe atomic regions, isolate tenants, and expose contention budgets/metrics.

Do not include secrets, keys, values, memory addresses, or cross-tenant queue details in contention diagnostics. Authorization checks depending on mutable state belong atomically with the operation; slow external authorization happens before locking and may need a version/token revalidation at commit.

## Definitions and Notation

- `S`: sequential abstract object state.
- `Rep`: mutable concrete representation owned by the wrapper.
- `I(Rep)`: representation invariant.
- `L`: the one mutex guarding the declared synchronization domain.
- `inv(op)` / `res(op)`: invocation and response events of operation `op`.
- `lp(op)`: chosen linearization point satisfying `inv(op) < lp(op) < res(op)` for completed calls.
- `H`: concurrent history of invocation/response events.
- `Seq(H)`: candidate legal sequential history equivalent to completed operations and respecting real-time order.
- `W`: time from operation invocation/acquisition attempt until successful lock acquisition.
- `S_c`: time holding the coarse lock (critical-section service time).
- `R=W+S_c+outside`: response latency under the declared interval.
- `rho`: utilization of the serialized critical-section resource under a queueing model.
- **guarded-by set**: fields/reachable state whose access requires `L`.
- **escape**: exposing a reference/capability that permits observation/mutation outside the lock protocol.
- **lock-order graph**: directed graph `A->B` when code may acquire B while holding A; a cycle signals potential deadlock.
- **snapshot**: immutable/detached state corresponding to one instant/linearization point.
- **poisoning**: policy marking an object unusable after a holder fails while invariants may be suspect.

Mutual exclusion orders protected critical sections, but invocation order among overlapping calls is unconstrained. Linearizability may select any legal order for overlaps consistent with return values and nonoverlapping real-time precedence.

## Mechanisms, Invariants, or Proof Structure

**Wrapper construction.** Own `Rep`; create noncopyable/private `L`; identify every protected field/referent; expose only wrapper methods or detached immutable results. Each method validates, acquires, executes the sequential operation, restores/checks `I`, captures return data, releases, then performs safe external work.

**Linearizability proof.** Mutual exclusion gives a total order of nonoverlapping critical effects. Sequential core correctness gives a legal transition for each. Old `I` is visible at entry and restored at exit. Real-time nonoverlap forces the same order because a later invocation cannot enter before an earlier completed call released. Choose the method-specific effect/observation inside each interval.

**Visibility proof.** Cite the target lock's specified synchronization relation. All writes to guarded state occur before release; every later guarded read occurs after successful acquire. Transitivity with program order establishes visibility. Unlocked aliases/reads fall outside this proof.

**Failure proof.** Partition failure points into pre-acquire, waiting, protected pre-mutation, mutation, and post-release. Show whether no abstract effect or one committed effect occurs; release exactly once if acquired; restore `I`; and return/throw the documented result. Cancellation is enabled only at safe boundaries or has rollback/poison policy.

**Escape audit.** For every parameter, result, stored element, iterator, view, callback, exception, formatter, serializer, metric, and test hook, ask whether it can reach/observe/mutate guarded representation after release. Copy, freeze, wrap, synchronize, or reject accordingly.

**Composition proof.** List all locks/resources acquired while holding `L`. Enforce global acyclic order or show no simultaneous hold. Unknown callbacks run without `L` or meet a trusted contract. Multi-wrapper methods normalize identical objects and acquire stable order atomically/with safe cleanup.

**Condition proof.** Protected predicate derives from `Rep`; every transition and test occurs under `L`; wait atomically releases/reacquires; loop handles spurious/competing wakeups; close/cancel/timeout are predicate outcomes; notification follows state transition.

**Lifecycle proof.** Close has one protected state transition and wakes waiters. Each operation checks lifecycle inside lock. Ownership/lifetime prevents destruction while holders/waiters/callbacks may access. Copy/fork/serialization constructs new synchronization state or is forbidden.

**Progress/performance evidence.** Safety proof does not imply progress. Measure wait/hold/totals and scheduler/runtime events under contention; test starvation/deadlock/cancellation; state primitive fairness/priority guarantees. Optimization must preserve abstract history and memory relation.

**Verification stack.** Sequential oracle/invariants; deterministic finite trace; bounded history linearizability checker; race detector; randomized/fault schedule stress; lock-order/deadlock analysis; model checking for critical protocols; production-shaped performance/observability. Each has limitations.

## Alternatives and Trade-Offs

| Design | Concurrency | Reasoning | Main risk/cost |
|---|---|---|---|
| One mutex wrapper | one protected operation | simplest direct proof | convoy/contention |
| Reentrant one-lock wrapper | one protected operation | nested trusted calls possible | hides reentry/invariant exposure |
| Read-write lock | concurrent readers | more state/modes | writer starvation, upgrade deadlock |
| Lock striping/sharding | independent buckets/shards | moderate | multi-key atomicity/order/resizes |
| Fine-grained node locks | disjoint regions | difficult | lock coupling/order/lifecycle |
| Immutable snapshots + root swap | read roots concurrently | clean reads | update allocation/reclamation |
| Actor/owner thread | serialized messages | avoids shared mutation | queue/backpressure/reentrancy |
| Transaction/STM | optimistic composition | declarative atomicity | retries/side effects/runtime cost |
| Nonblocking atomics | implementation-dependent overlap | strongest complexity | ABA/reclamation/memory-order proof |

A nonreentrant mutex keeps the call graph honest and is usually preferable when public callbacks/reentry are forbidden. Reentrant locks suit deliberately nested internal APIs but require an invariant protocol: outer methods may not call code that assumes the invariant is fully restored unless it is.

Read-write locks help only when reads are sufficiently long/frequent, the implementation permits concurrency, and write/fairness behavior is acceptable. Tiny reads can lose to larger lock overhead/cache movement. Upgrade from read to write can deadlock or invalidate the observed state; release/reacquire with version validation or use supported upgrade semantics.

Striping improves unrelated-key concurrency but global resize, exact size/snapshot, multi-key operations, and iteration must coordinate stripes. A fixed global order prevents cycles. Sharding can move contention into skewed hot keys.

Immutable snapshot/root-swap designs let readers avoid the writer lock or use atomic root loads, but memory ordering and reclamation remain. Actors serialize like one lock but queue ownership changes cancellation, backpressure, and callbacks. Fine-grained/nonblocking designs require materially stronger proof/testing; adopt after coarse baseline measurements identify a real bottleneck.

## Failure Modes and Misconceptions

- **“The core is thread-safe because callers promise.”** The wrapper must own/enforce the protocol or clearly expose an external-lock API.
- **“Reads cannot corrupt state.”** They can race, observe partial invariants, or invoke mutable caches/hash/equality.
- **“The interpreter lock protects my object.”** It is runtime/version/configuration-specific and not the abstract API or native-state proof.
- **“Each call is atomic, so any sequence is.”** Check-then-act and read-modify-write need one wrapper operation.
- **“Returning an iterator after unlocking is fine.”** It retains live representation access unless snapshot/detached.
- **“`finally` proves exception safety.”** It proves release; the core may still be half-mutated.
- **“Reentrant means safer.”** It can turn self-deadlock into invariant-breaking nested behavior.
- **“One lock means no deadlock.”** External locks, multiple wrappers, callbacks, I/O, and lifecycle waits create cycles.
- **“Timeout fixes deadlock.”** It bounds/detects waiting but needs safe acquisition/effect semantics and leaves the cycle.
- **“Notify stores an event.”** Conditions coordinate protected predicates; notifications can be missed without state/loop discipline.
- **“Fair lock means strict FIFO.”** Read the primitive/method contract; try-lock or scheduling can differ.
- **“Race-free means linearizable.”** Return values/compound semantics can be wrong without data races.
- **“Correct final count proves correctness.”** Many illegal histories share the same final state.
- **“Low average wait means no contention problem.”** Tail holds, starvation, priority inversion, and burst queues matter.
- **“Fine-grained is automatically faster.”** Extra locks, cache traffic, coordination, retries, and complexity may dominate.

## Worked Examples

### Example 1

**Situation.** `put` takes the lock, but `size` reads a cached counter without synchronization.

**Reasoning.** Unless the counter is an atomic with a defined relation/accuracy contract independent of the map invariant, `size` races or can observe a count inconsistent with entries. Put the counter in the guarded set and lock `size`, or redesign it as explicitly approximate atomic metadata and prove/document that weaker result.

**Conclusion.** “Read-only” methods belong to the synchronization audit.

### Example 2

**Situation.** A wrapper returns `dict.keys()` while holding the lock, then releases it.

**Reasoning.** The keys view is live and backed by the dictionary. Later mutation can change iteration or cause runtime errors outside protection. Copy keys into an immutable tuple under lock, return an immutable persistent snapshot, or expose a bounded callback with known semantics (and callback hazards).

**Conclusion.** Locking view creation does not detach the returned capability.

### Example 3

**Situation.** Two threads execute `if balance() >= 10: withdraw(10)` through individually locked methods on a balance of 10.

**Reasoning.** Both balance calls can return 10 before either withdrawal. Depending on withdraw policy, one fails unexpectedly or balance becomes invalid. Provide `tryWithdraw(10)` that tests and updates under one acquisition and returns success. Its successful mutation or protected insufficient observation is the linearization point.

**Conclusion.** Make the required compound transition an object operation.

### Example 4

**Situation.** `compute(key, userFunction)` calls the function while holding a nonreentrant lock; the function calls `get` on the same wrapper.

**Reasoning.** `get` waits for a lock held by the same thread: self-deadlock. Switching to a reentrant lock permits entry but may expose/modify partial state and allows unbounded blocking. Restrict trusted callback behavior or snapshot value/version, call outside, reacquire, validate, and commit/retry; forbid effectful replay.

**Conclusion.** Callback semantics, not lock type alone, determine safety.

### Example 5

**Situation.** Transfer between wrappers A and B locks source then destination; concurrent reverse transfer locks B then A.

**Reasoning.** Schedule: thread 1 holds A/waits B; thread 2 holds B/waits A, forming a cycle. Normalize identical accounts, order locks by stable global ID, acquire both in that order, validate and transfer, release in reverse/structured cleanup. Authorization/callback/I/O stays outside or is revalidated.

**Conclusion.** Multi-object operations require an acyclic composition protocol.

### Example 6

**Situation.** Exercise a bounded state model of four workers using one owned lock and deterministic postconditions.

**Reasoning.** A model mutex rejects overlapping ownership and nonowner release. Four logical workers are interleaved round-robin and perform twelve disjoint puts; every state access uses the same ownership protocol. Exact values are schedule-independent, every worker completes, and mutating a detached snapshot cannot change the core. This bounded model is executable within the repository's safe verifier, which deliberately excludes thread-creation imports.

<!-- bijux-verify: {"id":"coarse-lock-serialized-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"size=12\nkeys=0,1,2,3,4,5,6,7,8,9,10,11\nsum_values=506\nwrite_operations=12\nsnapshot_is_copy=True\nworkers_completed=True\nall_invariants=True\nevidence=finite_coarse_lock_serialized_model\n","stderr":""}} -->
```python
class ModelMutex:
    def __init__(self) -> None:
        self.owner: int | None = None
        self.acquisitions = 0

    def acquire(self, worker: int) -> None:
        if self.owner is not None:
            raise RuntimeError("overlapping critical sections")
        self.owner = worker
        self.acquisitions += 1

    def release(self, worker: int) -> None:
        if self.owner != worker:
            raise RuntimeError("nonowner release")
        self.owner = None


class CoarseMapModel:
    def __init__(self) -> None:
        self._lock = ModelMutex()
        self._data: dict[int, int] = {}
        self._write_operations = 0

    def put(self, worker: int, key: int, value: int) -> None:
        self._lock.acquire(worker)
        try:
            self._data[key] = value
            self._write_operations += 1
        finally:
            self._lock.release(worker)

    def get(self, worker: int, key: int) -> int:
        self._lock.acquire(worker)
        try:
            return self._data[key]
        finally:
            self._lock.release(worker)

    def snapshot(self, worker: int) -> dict[int, int]:
        self._lock.acquire(worker)
        try:
            return dict(self._data)
        finally:
            self._lock.release(worker)

    def stats(self, worker: int) -> tuple[int, int]:
        self._lock.acquire(worker)
        try:
            return len(self._data), self._write_operations
        finally:
            self._lock.release(worker)


shared = CoarseMapModel()
programs = [[worker, worker + 4, worker + 8] for worker in range(4)]
positions = [0, 0, 0, 0]
while any(position < len(program) for position, program in zip(positions, programs)):
    for worker, program in enumerate(programs):
        position = positions[worker]
        if position < len(program):
            key = program[position]
            shared.put(worker, key, key * key)
            positions[worker] += 1

completed = positions == [3, 3, 3, 3]
snapshot = shared.snapshot(4)
size, write_operations = shared.stats(4)
snapshot[0] = -1
snapshot_is_copy = shared.get(4, 0) == 0
expected = {key: key * key for key in range(12)}
valid = (
    completed
    and size == 12
    and write_operations == 12
    and shared.snapshot(4) == expected
    and snapshot_is_copy
    and shared._lock.owner is None
    and shared._lock.acquisitions == 16
)

print(f"size={size}")
print("keys=" + ",".join(map(str, sorted(expected))))
print(f"sum_values={sum(expected.values())}")
print(f"write_operations={write_operations}")
print(f"snapshot_is_copy={snapshot_is_copy}")
print(f"workers_completed={completed}")
print(f"all_invariants={valid}")
print("evidence=finite_coarse_lock_serialized_model")
```

The model checks an explicit ownership protocol rather than using real threads. A production Python implementation must replace `ModelMutex` with `threading.Lock` and retain structured acquisition around every method, then be tested outside this restricted snippet runner with threads, recorded histories, schedule stress, and race tooling. The model does not prove runtime memory visibility, all histories, failures, fairness, external deadlock freedom, or performance.

**Conclusion.** A bounded serialization model supplies deterministic ownership/invariant evidence while real-thread evidence remains a distinct required layer.

### Example 7

**Situation.** Allocation fails after a sequential core has linked a new node but before size metadata increments.

**Reasoning.** A context manager releases the mutex, preventing permanent lock retention, but invariant `size == reachable nodes` is broken. Reorder/stage allocations before mutation, implement rollback, use a strong exception-safe core, or mark the wrapper poisoned/closed if recovery is impossible. Inject failure at every allocation/mutation boundary.

**Conclusion.** Lock-release safety and representation exception safety are different proofs.

### Example 8

**Situation.** A bounded queue waiter checks `empty`, calls condition wait once, then removes.

**Reasoning.** It can wake spuriously or another awakened consumer can remove first. Under the associated lock, loop while empty and not closed; wait with recomputed monotonic deadline; after reacquire recheck. Producer changes empty predicate under lock then signals. Close changes state and broadcasts so waiters terminate.

**Conclusion.** Condition correctness lives in the protected predicate loop, not notification alone.

### Example 9

**Situation.** Eight threads show good mean throughput but rare 500 ms operations.

**Reasoning.** Instrument separate runs for wait/hold/total distributions and correlate long holds with allocation/GC/preemption/I/O/callback paths. Inspect starvation and per-thread acquisition counts. Mean throughput can coexist with unacceptable p99/max. Shorten bounded critical work or choose another design only after semantic-equivalent evidence.

**Conclusion.** Coarse-lock decisions require tail and hold/wait evidence, not averages alone.

### Example 10

**Situation.** ThreadSanitizer finds no races in a wrapper stress test.

**Reasoning.** This supports absence of detected conflicting memory accesses in exercised instrumented paths. It does not check an atomic `contains`-then-`put` requirement, return-value history, deadlock, starvation, unexecuted methods, unsupported code, or production schedules. Add bounded linearizability checking, lock-order/fault tests, invariant assertions, coverage, and model review.

**Conclusion.** Race detection is one verification layer, not the concurrency specification.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** memory models, scheduling, conditions, cancellation, progress, and contention supply the execution foundation.
- **Software Engineering Patterns:** monitor objects, synchronized decorators, ownership, facades, and command APIs turn synchronization into a durable boundary.
- **Programming Languages:** RAII/context/finally, reentrancy, effects, alias types, and exception guarantees shape safe wrappers.
- **Operating Systems:** mutex implementation, futex/parking, priorities, preemption, signals, and fork determine operational behavior.
- **Formal Methods:** refinement/linearizability, invariant preservation, wait-for graphs, and model checking prove different properties.
- **Security Engineering:** adversarial callbacks/keys, denial of service, profiler/log leakage, authorization revalidation, and tenant isolation matter.
- **Database Engineering:** atomic read-modify-write, transactions, lock ordering, deadlock handling, isolation, and snapshots are larger-scale analogues.
- **Systems Performance:** serialized service demand, queueing, hold/wait tails, cache transfer, and instrumentation bias govern scalability evidence.

## References

1. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990, pp. 463–492. Primary definition and proof framework.
2. Python Software Foundation, [`threading` documentation](https://docs.python.org/3/library/threading.html), accessed 2026-08-30. Official `Lock`, condition, context-manager, GIL, and free-threaded-build behavior.
3. Oracle, [`java.util.concurrent.locks.Lock`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/Lock.html), Java SE 26. Official explicit-lock memory-synchronization and usage contract.
4. Oracle, [`ReentrantLock`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html), Java SE 26. Official reentrancy, fairness, interruptible/timed, and try-lock behavior.
5. The Go Project, [The Go Memory Model](https://go.dev/ref/mem), official mutex synchronizes-before guarantees and race guidance.
6. The Open Group, [`pthread_mutex_lock`, `pthread_mutex_trylock`, `pthread_mutex_unlock`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html), POSIX.1-2024. Official normal/error-checking/recursive/robust mutex behavior.
7. SEI CERT C Coding Standard, [CON35-C: Avoid deadlock by locking in a predefined order](https://wiki.sei.cmu.edu/confluence/display/c/CON35-C.+Avoid+deadlock+by+locking+in+a+predefined+order), official lock-order guidance.
8. LLVM Project, [ThreadSanitizer documentation](https://clang.llvm.org/docs/ThreadSanitizer.html), official race-detector scope, use, overhead, and limitations.

## Exercises

### Exercise 1

State sufficient assumptions and give a concise linearizability proof for a one-lock stack wrapper with `push`, `pop`, `peek`, `size`, and `snapshot`. Identify method-specific linearization points and alias requirements.

### Exercise 2

Audit an API containing `get`, `put`, `remove`, `keysView`, `forEach(callback)`, `compute(callback)`, `toString`, `serialize(stream)`, `validate`, and `rawTableForTests`. Classify each synchronization/escape/callback risk and propose safe contracts.

### Exercise 3

Design an exception-, timeout-, and cancellation-safe `putIfAbsent` plus a bounded `waitForKey` using a mutex and condition. Specify states, predicates, linearization points, cleanup, close behavior, and focused fault/schedule tests.

### Exercise 4

Design an atomic transfer between two coarse-locked account wrappers. Address same-account calls, global order, validation/authorization, overflow/insufficient funds, callbacks/audit I/O, exceptions, timeouts, close, and the proof/test plan.

### Exercise 5

A production cache wrapper is correct but saturates at 16 threads. Prepare an evidence-driven decision among keeping one mutex, reducing critical work, read-write locking, striping, immutable snapshots, and actor ownership. Include semantic requirements, measurements, workload matrix, risks, and migration verification.

## Answers to the Exercises

### Answer 1

Assume the wrapper exclusively owns a sequential stack whose invariant holds at operation boundaries; one private lock protects storage and size; every method acquires it; structured cleanup releases; sequential methods are exception-safe; elements are immutable/thread-safe or copied; snapshot is detached immutable; no live iterator/core alias/callback escapes.

Critical sections are mutually exclusive. Order completed operations by their protected abstract observations/effects. Sequential stack correctness makes this a legal LIFO history, and nonoverlapping real-time calls retain order. Successful `push` linearizes when the element becomes the top and metadata agrees. Successful `pop` linearizes when the top is removed; empty failure at the protected empty observation. `peek`/`size` linearize at their protected observation. `snapshot` linearizes at some instant during uninterrupted copying when the copied sequence equals the stack; because no mutation overlaps, any point after the last protected read consistent with the copy suffices. Returned mutable elements must not permit mutation of guarded representation/invariants after release.

### Answer 2

`get`, `put`, and `remove` lock around the complete sequential operation; returned values are copied/immutable or element-safety is explicitly separate. `keysView` cannot return a live table-backed view; return an immutable tuple/snapshot copied under lock. `toString` and `validate` read representation and must lock, but formatting arbitrary elements may invoke callbacks; capture safe snapshots then format outside or restrict element formatting.

`forEach(callback)` must not call arbitrary code under lock. Prefer snapshot entries under lock then iterate outside, explicitly giving snapshot—not live atomic—semantics. `compute(callback)` needs declared atomicity: a trusted bounded pure callback may run under lock, or snapshot value/version, call outside, reacquire/validate and commit/retry; forbid/restrict effectful replay and reentry.

`serialize(stream)` should capture immutable logical state under lock, release, then encode/write; stream I/O under lock invites convoy/deadlock. Ensure element captures cannot mutate. `rawTableForTests` is an escape; remove it, expose locked invariant/query hooks or detached copy, or constrain unsafe access to a quiescent package-private harness that cannot ship. Every callback/error/log path is included in lock-order and exception review.

### Answer 3

State includes table, closed flag, and condition `changed` associated with the table mutex. `putIfAbsent` validates state-independent key/value constraints before lock, acquires interruptibly/timed only if the API says so, checks closed, and observes membership. Existing-key failure/result linearizes at that protected lookup. For absence, stage any safe allocation, perform exception-safe insertion plus metadata under lock, restore invariant, signal/broadcast `changed`, and linearize at insertion. Structured cleanup releases exactly once. Allocation/hash/equality failure produces no abstract effect or a declared poison policy.

`waitForKey(k,deadline,cancel)` acquires, then loops: if key exists, copy/result and linearize at observation; if closed, return closed; if cancelled, return cancellation; compute remaining monotonic time and return timeout only after a final protected absence/deadline check; otherwise wait, which atomically releases/reacquires. Spurious or competing wakeups simply loop. `close` locks, marks closed at its linearization point, and broadcasts.

Tests inject failures before/after staging and at hash/equality/core steps; cancel before acquire, while waiting, and at wake; timeouts just before/with insertion; spurious/broadcast/multiple waiters; insert/remove races; close races; exceptions preserving invariant/release; bounded history linearizability; race detector; repeated schedules; and no waiter left after close.

### Answer 4

Give each account an immutable stable lock-order ID unique for its lifetime. If source and destination are the same, either return a documented no-op after one lock/authorization or reject—never acquire twice unless deliberately reentrant. Otherwise identify lower/higher ID and acquire both in that order with structured all-or-none cleanup. Validate lifecycle, currencies/schema, source authorization and destination policy atomically as required, then check insufficient funds and fixed-width overflow before changing either balance. Apply both balance changes as one protected transition; that transition is the linearization point. Failed protected checks linearize at their observations and change neither account.

Perform slow external authorization before locks using signed/versioned capability, then revalidate capability/account version inside. Capture audit event under locks and emit durable I/O after release; if audit durability must be atomic, use a transaction/log protocol rather than blocking arbitrary sink code while holding two locks. Specify exceptions as no-effect through staging/rollback, or poison both under a coordinated policy. Timed multi-lock acquisition must release any acquired lock and distinguish timeout-before-effect. Close uses the same ordering/protocol and prevents new transfers after its protected transition.

Proof: global increasing order makes the account-lock graph acyclic; mutual exclusion plus invariant-preserving paired transition yields a legal sequential transfer and preserves total funds (modulo fees explicitly modeled). Tests cover reverse simultaneous transfers, same object, IDs/order, insufficient/overflow, close, auth revocation/version, every injected failure, timeout after first acquisition, audit failures, randomized histories checked against a reference, race/deadlock detection, invariant/total preservation, and starvation/tails.

### Answer 5

First preserve the cache's abstract contract: exact/approximate size, get/put/compute semantics, eviction order, atomic loader deduplication, TTL clock, iteration/snapshot, element ownership, close, and callback behavior. Record current linearizability/invariant tests as the oracle. Measure production-shaped key skew, hit/miss, value sizes, read/write/eviction/loader mix, thread/arrival levels, callback/load time, state sizes, TTL churn, and cancellation/close—not only uniform keys.

Instrument separate runs for total latency/throughput by method and p50/p95/p99/max, lock wait/hold, contended acquisitions, per-thread progress/starvation, queue/context switches, CPU, allocations/GC, cache misses where valid, and critical-section path labels. Test 1 through oversubscribed threads, burst/steady arrivals, hot keys, expensive hashes/equality, loader failure, eviction, GC/preemption, and deployment hardware/runtime. Use independent load/process/host units, randomized candidates, raw histories, uncertainty, and prespecified SLO/cost thresholds.

First move safe state-independent allocation, loading, logging, and destruction outside while using version/reservation validation; this preserves one-lock proof but loader deduplication/cancellation needs design. Read-write locking helps only if protected reads dominate/are long and writer/fairness tails pass. Striping helps independent keys but complicates exact size, eviction, resize, snapshots, and multi-key operations with global order. Immutable root snapshots favor read-heavy workloads but add update allocation/reclamation. An actor keeps serialization while changing queue/backpressure and can move blocking load to workers with correlated replies.

Keep the one-lock implementation if it meets SLO/cost after bounded critical work; simplicity is value. Otherwise prototype the least complex design meeting measured bottleneck. For migration, run the same oracle/histories, bounded linearizability, race/fault/cancellation/close/model tests, semantic-equivalent benchmarks, shadow/dual execution with privacy controls, resource/reclamation tests, staged rollout/rollback, and production tails. Do not accept higher throughput at the cost of weaker loader/eviction/snapshot semantics without explicit product approval.
