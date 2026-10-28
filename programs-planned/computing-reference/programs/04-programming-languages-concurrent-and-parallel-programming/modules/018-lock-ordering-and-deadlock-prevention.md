---
module_id: CONPAR-018
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 18
title: Lock Ordering and Deadlock Prevention
status: complete
last_verified: 2026-08-29
---

# Lock Ordering and Deadlock Prevention

## One-Page Review

### Governing question

How can a program prevent circular wait across locks and other blocking dependencies by imposing a reviewable acquisition discipline, and where do dynamic resources, callbacks, conditions, upgrades, timeouts, cancellation, and distributed waits require stronger reasoning?

### Essential definitions

- **deadlock** is a reachable state in which participants wait indefinitely for events only participants in the waiting set can cause.
- A **wait-for graph** has participant nodes and an edge (u to v) when u waits for a resource or event controlled by v.
- A **resource-allocation graph** represents participants, resources, requests, and assignments.
- **circular wait** is a directed wait-for cycle.
- A **lock order/hierarchy** assigns every lock a rank and permits nested acquisition only in one strict direction.
- A **lock level** is a durable rank associated with a protected domain, not an incidental address unless that is the documented dynamic rule.
- A **dynamic lock set** is a runtime-chosen collection canonicalized before acquisition.
- **open call** releases internal locks before invoking unknown or external code.
- **try-lock rollback** releases all partial holdings when the complete set cannot be obtained.
- **deadlock avoidance** admits an acquisition only if a safe completion state remains.
- **deadlock detection** finds an existing cycle; **recovery** breaks it by aborting or rolling back a participant.
- **livelock** is continued activity without progress; **starvation** is indefinite postponement of one participant.

### Central model, mechanism, or theorem

Assign each lock (l) a rank (r(l)) in a strict total order. Require a participant already holding locks (H) to acquire (l) only when:

(for every h in H, r(h) < r(l)).

If a wait-for cycle existed, each participant would hold a lower-ranked lock while requesting the next higher-ranked lock. Traversing the cycle would imply:

(r(l_1) < r(l_2) < ... < r(l_k) < r(l_1)),

contradicting irreflexivity of a strict order. Therefore circular wait among locks governed by this discipline is impossible. The proof does not cover unranked waits, callbacks, joins, channels, conditions, or upgrades unless modeled in the same dependency system.

### Critical invariants

Every nested lock participates in one authoritative hierarchy. Acquisition moves strictly upward; release normally unwinds without exposing invalid state. Runtime lock sets are deduplicated and sorted by stable identity before acquisition. Failed or cancelled acquisition releases only confirmed holdings in reverse order. No callback, I/O, await, join, or queue operation occurs under a lock unless its dependency is proven acyclic. Read-to-write upgrade is modeled as a new wait edge. Condition waiting preserves the protected predicate protocol. Lock ranks remain stable for object lifetime. Shutdown and error paths obey the same order.

### Common failures

Teams document different local orders that form a global cycle; rank by mutable data; sort after taking the first lock; compare raw addresses whose reuse or cross-process meaning is invalid; invoke callbacks under locks; log through another locking subsystem; hold a lock while joining a worker that needs it; recursively submit to a bounded queue; acquire read then wait for write; use timeout as proof of absence; retry symmetrically and livelock; release partial sets incorrectly; omit error/shutdown paths; or detect a cycle without a safe rollback boundary.

### Compact example

Accounts have stable IDs 7 and 12. Every transfer deduplicates endpoints and acquires lower ID before higher ID. Transfer 7-to-12 and simultaneous transfer 12-to-7 both take lock 7 then 12, so one waits without holding 12 against the other. If account ID can change while locked or if fee logging acquires an unranked global lock, the proof no longer covers the full operation.

### Connections

[Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md) defines progress failures; [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) supplies ownership; [Read-Write Locks](015-read-write-locks.md) exposes upgrade and mode dependencies; [Thread-Safe Queues](017-thread-safe-queues.md) adds capacity waits. The [program roadmap](../ROADMAP.md) next covers worker pools and complete multithreaded components.

## Governing Question

How can engineers turn “always lock consistently” into a global, enforceable proof that includes runtime-selected objects, every mode and failure path, and non-lock blocking edges—while distinguishing prevention from avoidance, detection, timeout, and recovery?

The durable answer is a dependency policy plus evidence: lock catalog, ranks, acquisition sites, wait-for graphs, runtime assertions, adversarial tests, and a design that removes unnecessary nested waits.

## Why This Matters

Two individually correct critical sections can deadlock when composed. Thread A holds account X and waits for Y; thread B holds Y and waits for X. No data race occurs, no invariant need be corrupted, and every lock implementation can behave exactly as specified. The architecture is wrong.

Modern systems contain more than mutexes. A thread can hold a lock while waiting for a bounded queue slot, joining a worker, entering a barrier, awaiting a callback, acquiring a database row lock, or asking an executor to run work. These edges can close cycles across subsystems. A lock-only diagram is too narrow.

Deadlocks are schedule-sensitive and often absent in tests until load, error, or shutdown. Timeouts convert infinite waiting into failure but do not restore partial state or prove progress. Detection can identify a cycle after harm begins, but recovery needs an authorized victim and rollback.

Ordering is attractive because it prevents circular wait by construction. It scales organizationally only when ranks have durable domain meaning, libraries publish “may-call-while-held” contracts, dynamic objects use stable canonical keys, and automated checks cover all acquisition paths.

Current APIs supply mechanisms, not a global proof. Java SE 26 `Lock` offers blocking, interruptible, immediate, and timed acquisition whose exact ordering and interruption semantics may differ; `ReentrantLock` adds optional fairness but untimed try-lock can barge. Rust 1.98 and Go mutex APIs document their own ownership, poisoning, try-lock, and memory behavior. POSIX.1-2024 mutex types can detect some self-deadlock cases but do not infer an application hierarchy. Prevention remains an architecture responsibility.

## Prerequisites and Retrieval

Retrieve:

- Coffman conditions, wait-for cycles, livelock, and starvation from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- owner obligations, exception cleanup, and lifecycle from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md);
- upgrade/downgrade and mode policy from [Read-Write Locks](015-read-write-locks.md);
- bounded producer/consumer waits and shutdown from [Thread-Safe Queues](017-thread-safe-queues.md);
- join lifetime from [Creating and Joining Threads](011-creating-and-joining-threads.md); and
- directed graphs, cycles, strict orders, induction, transactions, rollback, canonical identity, and monotonic deadlines.

Retrieval prompt: draw the wait-for graph for A holding X/requesting Y and B holding Y/requesting X. Label the first event that creates a cycle. Then assign ranks X<Y and identify which acquisition must be rejected or reordered.

## Learning Objectives

After completing this module, a learner can:

1. build wait-for graphs spanning locks, queues, joins, barriers, and callbacks;
2. prove strict lock ranking excludes circular wait in its scope;
3. design stable ranks for static locks and canonical dynamic object sets;
4. include read/write modes, conditions, recursion, and upgrade in dependencies;
5. use open calls and ownership transfer to eliminate nested waits;
6. evaluate try-lock rollback, avoidance, detection, timeout, and recovery;
7. distinguish deadlock prevention from livelock, starvation, and fairness;
8. instrument and test order violations without claiming exhaustive schedules; and
9. identify safety-critical locking claims requiring named human review.

## Core Exposition

### Model every wait edge

For single-instance locks, a participant wait-for graph is convenient: edge (T_i to T_j) means T_i cannot progress until T_j releases or causes an event. A directed cycle is necessary and, under stable non-preemptible resource assumptions, characterizes deadlock.

For multiple resource instances or richer events, a cycle may be necessary but not sufficient. Record resource nodes, capacity, predicates, and which participant can enable each edge. A condition waiter releases its associated mutex, so model its predicate dependency rather than pretending it still holds the mutex. A barrier creates an all-party phase dependency. A full queue makes a producer depend on a consumer.

Draw graphs for normal operation, error cleanup, cancellation, and shutdown. The deadlock may exist only when a logger flushes, a callback reenters, or a coordinator joins under a lock.

### Coffman conditions and prevention choices

Classic deadlock requires mutual exclusion, hold-and-wait, no forced preemption, and circular wait. Preventing any one suffices within the model:

- eliminate mutual exclusion through immutability, partitioning, or lock-free ownership;
- eliminate hold-and-wait by acquiring atomically or releasing before a new wait;
- permit rollback/preemption where state is safely recoverable; or
- eliminate circular wait through ordering.

Each has costs. Copying state may be expensive. Atomic multi-acquire needs a supported algorithm. Preemption of a mutex owner is generally unsafe. Ordering is broadly applicable but constrains modular composition.

### The strict-order proof

Give each governed lock a unique or equivalence-aware rank in a well-founded strict order. Suppose a cycle contains participants (T_1...T_k). Each T_i holds lock (l_i) and waits for (l_{i+1}), with the final index wrapping. The discipline yields (r(l_i)<r(l_{i+1})) for every edge. Transitivity yields (r(l_1)<r(l_1)), impossible.

The contradiction relies on:

- every edge in the cycle being a governed acquisition;
- rank stability during each lifetime;
- no equal-rank nested acquisition unless a secondary strict key orders it;
- acquisition checks before waiting; and
- no hidden dependency reversing the order.

Ordering prevents circular wait, not starvation or long holds. A low-ranked lock can still be unavailable indefinitely under an unfair scheduler.

### Design ranks by domain

Prefer durable levels such as registry < account < transaction < entry, with one owner documenting the global relationship. Module-local integers are unsafe if two modules both call their lock “level 2” but call each other in opposite directions.

Ranks should reflect allowable dependency, not current call sequence. A lower layer generally must not call upward while holding its lock. Public APIs should state whether they acquire locks, invoke callbacks, block, or require caller-held state.

Enforce with guard metadata and a thread/task-local stack: before acquisition, compare requested rank with the highest held rank; on release, validate the matching guard. Production assertions must avoid recursively taking diagnostic locks. Static analyses or effect/type systems can encode levels where practical.

### Dynamic object sets

For two or more peer objects, use a stable canonical key: immutable unique ID or a process-local identity with documented lifetime. Gather the complete set before acquiring, reject/deduplicate aliases, sort by (domain level,key), then acquire in that order.

<!-- bijux-verify: {"id":"dynamic-lock-set-schema","mode":"schematic","language":"text","toolchain":"none","reason":"Language-neutral pseudocode illustrates canonical multi-object acquisition; exact identity, guard, exception, and mutex APIs are platform-specific."} -->
```text
objects = deduplicate_and_sort_by_stable_key(requested_objects)
guards = []
try:
    for object in objects:
        guards.append(acquire(object.lock))
    revalidate_and_commit(objects)
finally:
    release_in_reverse_order(guards)
```

Do not take one object lock and then discover/sort the rest. If object identity or membership can change, snapshot under an outer ranked lock or use version validation after acquisition. Addresses may work only within a stated lifetime and allocator model; never use mutable business values.

### Open calls and callbacks

Calling unknown code while holding an internal lock hands your dependency graph to the callee. The callback may reenter, acquire a lower-level lock, block on a queue whose consumer needs your state, log through another lock, or wait for I/O.

Use an open call: under lock, validate and capture immutable work; release; invoke external code; reacquire if needed; verify a version/predicate; then commit or reconcile. This introduces an optimistic gap, so never assume pre-call state remains current.

Destructors, observers, hooks, equality/comparison functions, allocation, and formatting can be hidden callbacks. Review language/runtime behavior, not only explicit function parameters.

### Read/write modes, upgrades, and recursion

Treat read and write requests as modes of one resource. Two read holds are compatible, but a write request depends on every active reader. A reader retaining its hold while upgrading creates a self/concurrent edge; two upgraders deadlock. Release-read, acquire-write in rank order, then recheck—or use a documented single-upgrader protocol.

Reentrancy can conceal dependency violations. Reacquiring the same lock may succeed while a wrapper later substitutes a non-reentrant lock or a queued writer blocks recursive read acquisition. Track hold counts and define whether equal-rank self-acquisition is allowed. Recursion does not permit acquiring a lower-ranked different lock.

Lock coupling in lists/trees acquires the next node before releasing the current one. Its proof requires a monotonic structural order and safe node lifetime. Traversing backward needs another design, not casual reversal.

### Conditions, joins, barriers, and queues

Condition wait atomically releases its associated mutex and later reacquires it. Before waiting, release every unrelated lock unless a wider proof covers it. On return, the reacquisition occurs before the predicate recheck and must fit the hierarchy.

Never join a thread while holding a lock it may acquire during work or cleanup. Likewise, do not enter a barrier while holding a lock needed by a later-arriving party. A producer blocking on a full queue depends on consumers; if it holds state consumers need, the cycle crosses primitive types.

Represent these dependencies in one graph. Assigning ranks only to mutexes cannot prove a graph containing queue, future, or shutdown edges.

### Try-lock, rollback, and multi-lock algorithms

When a stable total order is unavailable, attempt the full set without indefinite partial waiting: acquire one, try the next, and on failure release every acquired guard before retrying or returning. A standard multi-lock algorithm may permute attempts to avoid deadlock.

This removes permanent hold-and-wait only if rollback is complete and no side effect escapes before the full set is owned. Symmetric contenders can repeatedly collide, producing livelock. Add bounded randomized or asymmetric backoff, a coordinator, queueing, or stable tie-breaker. Specify cancellation and one monotonic deadline.

Try-lock is not automatically fair; Java's untimed `ReentrantLock.tryLock` can barge even on a fair lock. Record actual API semantics.

### Avoidance, detection, and recovery

Avoidance algorithms such as Banker's reasoning require declared maximum future demand and grant only states with a safe completion sequence. This is useful for resource pools but often impractical for open-ended lock calls.

Detection records live wait edges and finds strongly connected components or cycles. Sampling thread dumps helps diagnosis; instrumented lock graphs can detect earlier. A transient graph needs consistent-enough timestamps/identities to avoid false conclusions.

Recovery must choose a victim whose work can be rolled back, release resources, preserve invariants, and return a meaningful outcome. Databases can abort transactions because they own rollback machinery. Arbitrarily killing a thread holding in-memory locks can corrupt state. Prevention is preferable where rollback is absent.

### Timeout, cancellation, and priority

A timeout bounds one wait but does not prove deadlock freedom. If partial locks remain held or an external effect already occurred, returning can worsen the cycle. Use one absolute deadline, release only confirmed ownership, and reconcile provisional state.

Cancellation must wake blocked acquisition where supported and unwind guards in reverse order. Non-interruptible APIs need another wake/termination design. Priority inversion is distinct: a high-priority thread waits for a low-priority owner. Inheritance or ceiling protocols address scheduling priority and can interact with lock order; neither substitutes for an acyclic dependency graph.

### Lifecycle, observability, and testing

Ranks and lock identities must outlive every guard and waiter. Shutdown introduces edges among cancellation, queue closure, callbacks, joins, and destructors; audit it as a first-class operation. Fork/process or database locks require their own lifetime and recovery semantics.

Record acquisition rank violations, held-lock stacks, wait duration, owner, call site, mode, timeouts, rollbacks, and sampled wait graphs. Keep instrumentation nonblocking or strictly lower in an independent diagnostic hierarchy.

Tests should deterministically place participants after first acquisition, exercise both directions, callbacks, upgrade, recursive paths, errors, cancellation, and shutdown. A timeout detects a hang but a wait-for graph explains cause. Static order audits, runtime assertions, model checking, stress, and production dumps provide complementary evidence.

## Definitions and Notation

Let participants be (T), resources (L), held relation (H subseteq T x L), and request relation (R subseteq T x L). With exclusive single-instance locks, wait edge (t_i,t_j) exists when (t_i,l) is requested and (t_j,l) is held.

Rank function (rho:L to O) maps locks into strict ordered set (O,prec). Legal nested acquisition requires every held lock rank precede the requested rank. A dynamic key (k(l)) refines equal domain levels lexicographically.

Cycle (t_1 to ... to t_k to t_1) witnesses circular wait under stable assumptions. Wait duration, deadline, and rollback state are separate annotations, not cycle predicates.

## Mechanisms, Invariants, or Proof Structure

Use:

1. **Inventory resources.** Include modes, queues, joins, barriers, callbacks, and external locks.
2. **Draw wait graphs.** Cover normal, error, cancellation, and shutdown.
3. **Remove nesting.** Prefer ownership, snapshots, open calls, or transactions.
4. **Assign durable ranks.** Publish one global hierarchy and stable peer keys.
5. **Enforce before wait.** Assert requested rank exceeds all holdings.
6. **Canonicalize sets.** Gather, deduplicate, sort, acquire, revalidate.
7. **Handle conversions.** Model upgrades, conditions, and recursion explicitly.
8. **Unwind failures.** Release confirmed guards in reverse order without escaped effects.
9. **Address progress.** Prevent livelock/starvation separately.
10. **Observe and verify.** Combine static, runtime, modeled, and operational evidence.

Maintain strict upward acquisition, stable rank/key lifetime, unique/matched guard ownership, reverse cleanup, no hidden unranked wait under a held lock, revalidation after open-call gaps, and quiescent destruction. These invariants prevent only cycles inside their modeled scope.

The executable model considers two threads independently choosing an ordered pair from three locks. Exact reverse pairs create a two-edge precedence cycle. Restricting both threads to increasing global rank eliminates those pairs.

<!-- bijux-verify: {"id":"lock-order-pair-cycles","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_thread_pairs=36\ncyclic_order_pairs=6\nglobally_ordered_pairs=9\nglobally_ordered_cycles=0\n","stderr":""}} -->
```python
locks = ("A", "B", "C")
orders = []
for first in locks:
    for second in locks:
        if first != second:
            orders.append((first, second))

cyclic = 0
for left in orders:
    for right in orders:
        cyclic += int(left[0] == right[1] and left[1] == right[0])

rank = {"A": 0, "B": 1, "C": 2}
ranked = []
for order in orders:
    if rank[order[0]] < rank[order[1]]:
        ranked.append(order)

ranked_cycles = 0
for left in ranked:
    for right in ranked:
        ranked_cycles += int(left[0] == right[1] and left[1] == right[0])

print(f"candidate_thread_pairs={len(orders) * len(orders)}")
print(f"cyclic_order_pairs={cyclic}")
print(f"globally_ordered_pairs={len(ranked) * len(ranked)}")
print(f"globally_ordered_cycles={ranked_cycles}")
```

Limitations: the enumeration covers only two threads, two distinct exclusive locks per thread, three lock identities, and direct reversed orders. It does not run threads or model longer cycles, conditions, modes, callbacks, queues, fairness, cancellation, or implementation behavior.

## Alternatives and Trade-Offs

**Global lock order** gives a simple prevention proof but constrains layering and requires stable governance.

**Atomic multi-lock/try-lock rollback** supports dynamic sets without one exposed order, at retry, livelock, and cleanup cost.

**Coarse locking** removes nested order but reduces concurrency and can lengthen stalls.

**Partitioned ownership/message passing** eliminates shared lock cycles; queues and joins introduce their own dependency graph.

**Optimistic snapshots/transactions** move work outside locks and revalidate, trading retries and conflict handling for shorter holdings.

**Avoidance** uses maximum-demand/safe-state knowledge, which is powerful where demands are declared but awkward for general call graphs.

**Detection and rollback** fit transactional systems with durable undo; ordinary threads rarely have safe forced preemption.

**Timeouts** improve bounded failure response but can produce false aborts and require complete state reconciliation.

## Failure Modes and Misconceptions

- **“Each module has an order.”** Local orders can compose into a global cycle.
- **“Address order is universally stable.”** Lifetime, reuse, relocation, and process boundaries matter.
- **“Sort the second lock.”** The complete set must be canonicalized before any acquisition.
- **“No mutex cycle means no deadlock.”** Queues, joins, barriers, futures, callbacks, and I/O add edges.
- **“Try-lock fixes everything.”** Partial rollback can livelock or leak side effects.
- **“Timeout proves safety.”** It detects elapsed waiting and may leave damaged state.
- **“Fair locks prevent deadlock.”** Fairness orders waiters; it does not remove cycles.
- **“Reentrancy removes self-deadlock.”** It can conceal design errors and does not order other locks.
- **“Read locks cannot deadlock.”** upgrades and queued-writer policy create dependencies.
- **“Condition wait holds no locks.”** It releases one associated lock; unrelated holdings remain.
- **“Callbacks are computation.”** Unknown code is a dependency boundary.
- **“Detection implies recovery.”** Safe victim abort requires rollback authority.

## Worked Examples

### Example 1

**Question:** A holds X and requests Y; B holds Y and requests X.

**Reasoning:** Wait edges A-to-B and B-to-A form a directed cycle, with no participant able to cause its awaited release.

**Conclusion:** This reachable state is a two-party deadlock under non-preemptible locks.

### Example 2

**Question:** Every operation acquires X before Y.

**Reasoning:** A holder of Y cannot request lower-ranked X. The reverse edge needed to complete the two-lock cycle is prohibited before waiting.

**Conclusion:** The hierarchy prevents circular wait for these governed locks.

### Example 3

**Question:** Transfers sort accounts by mutable balance.

**Reasoning:** Concurrent balance changes can make two operations compute opposite orders for the same pair.

**Conclusion:** Rank by immutable unique identity, not protected mutable state.

### Example 4

**Question:** A method holds rank-30 cache lock and invokes a callback that takes rank-10 registry lock.

**Reasoning:** The hidden downward acquisition violates the global hierarchy and can close a cycle with registry-to-cache code.

**Conclusion:** Capture state, release, call openly, reacquire upward, and revalidate.

### Example 5

**Question:** Two readers each retain read mode while requesting write.

**Reasoning:** Each write waits for all readers; each requester keeps one of those blocking reads.

**Conclusion:** Model modes and upgrade edges; release/reacquire/recheck or use one supported upgrader.

### Example 6

**Question:** A thread holds a component lock and joins a worker.

**Reasoning:** If worker cleanup needs that lock, join depends on worker while worker depends on joiner-held state.

**Conclusion:** Release before join and audit shutdown as a wait graph.

### Example 7

**Question:** Two contenders acquire one dynamic lock, fail try-lock on the second, release, and immediately retry together forever.

**Reasoning:** Deadlock is avoided, but symmetric activity makes no progress.

**Conclusion:** Add asymmetry/backoff/coordinator or a canonical order; analyze livelock separately.

### Example 8

**Question:** What does the executable enumeration show?

**Reasoning:** Among 36 pairs of two-lock orders, six are exact reversals. Restricting both threads to the nine pairs of increasing-order choices yields zero reversal cycles.

**Conclusion:** It recomputes the smallest ordering theorem instance, not arbitrary deadlock freedom.

### Example 9

**Question:** A database detects a transaction cycle and aborts one participant.

**Reasoning:** The database owns durable rollback and can release the victim's locks while returning a retryable result.

**Conclusion:** Detection supports recovery only because a valid rollback boundary exists.

### Example 10

**Question:** Can a lock hierarchy alone approve concurrent route setting in railway interlocking software?

**Reasoning:** Acyclic software locks do not establish physical route exclusivity, timing, hardware failure response, fail-safe state, operating rules, or certification.

**Conclusion:** No. Named authorized railway signaling, systems, controls, hardware, real-time, functional-safety, verification, cybersecurity, human-factors, and regulatory reviewers must approve the actual system. No external review is claimed.

## Cross-Program Connections

- **Programming languages:** ownership types, effects, structured guards, exceptions, and async suspension expose lock dependencies.
- **Operating systems:** scheduling, priority inversion, robust mutexes, thread dumps, and process locks affect waiting and recovery.
- **Databases:** row/key lock order, deadlock detection, victim choice, and transaction rollback provide a recoverable model.
- **Distributed systems:** leases, partitions, fencing, and distributed wait graphs add uncertain failure and ownership.
- **Software architecture:** layering, open calls, callbacks, queues, and shutdown ownership determine global composition.
- **Formal methods:** strict orders, graph cycles, temporal progress, and refinement prove prevention within explicit scope.

## References

1. Edward G. Coffman Jr., Melanie Elphick, and Arie Shoshani, “System Deadlocks,” *ACM Computing Surveys* 3(2), 1971, [doi:10.1145/356586.356588](https://doi.org/10.1145/356586.356588).
2. James W. Havender, “Avoiding Deadlock in Multitasking Systems,” *IBM Systems Journal* 7(2), 1968, [doi:10.1147/sj.72.0074](https://doi.org/10.1147/sj.72.0074).
3. Edsger W. Dijkstra, “Hierarchical Ordering of Sequential Processes,” EWD310, 1971, [E. W. Dijkstra Archive](https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD310.html).
4. David R. Butenhof, *Programming with POSIX Threads*, Addison-Wesley, 1997.
5. IEEE and The Open Group, *POSIX.1-2024*, “pthread_mutex_lock,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html) (retrieved 2026-08-29).
6. Oracle, “Lock,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/Lock.html) (retrieved 2026-08-29).
7. Oracle, “ReentrantLock,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html) (retrieved 2026-08-29).
8. Rust Project, “Mutex,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/sync/struct.Mutex.html) (retrieved 2026-08-29).
9. The Go Authors, “sync.Mutex,” Go standard library, [official API](https://pkg.go.dev/sync#Mutex) (retrieved 2026-08-29).
10. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.

## Exercises

### Exercise 1

Define a wait-for graph and the four Coffman conditions. Explain why a cycle matters differently with single- versus multiple-instance resources.

### Exercise 2

Prove the strict-order theorem and list every assumption needed for its scope.

### Exercise 3

Diagnose a service that locks account-by-balance, logs under lock, joins workers during shutdown, and uses timed try-lock retry without backoff.

### Exercise 4

Design locking for a transaction over an arbitrary set of accounts, including aliases, deletion, cancellation, validation, and failure cleanup.

### Exercise 5

A medical device uses a global lock hierarchy for alarm configuration. State what chapter verification establishes and what needs named review.

## Answers to the Exercises

### Answer 1

Participant nodes have an edge from waiter to the participant controlling the awaited event/resource. Mutual exclusion, hold-and-wait, no forced preemption, and circular wait are jointly necessary for classic resource deadlock. With one non-preemptible instance per resource and stable requests, a wait-for cycle is sufficient: every participant awaits another in the cycle. With multiple instances, a cycle can coexist with a free or releasable instance that enables progress, so capacity/assignment state must be modeled. Conditions, queues, joins, and barriers require event predicates rather than pretending every edge is a mutex.

### Answer 2

Assume a cycle of governed lock waits. Each participant holds (l_i) and requests (l_{i+1}); the rule gives (rho(l_i)<rho(l_{i+1})). Chaining around the cycle gives (rho(l_1)<rho(l_1)), contradicting irreflexivity. Assumptions: one stable strict order; all relevant requested/held edges participate; ranks/secondary keys do not change; equality is disallowed or strictly refined; checking happens before waiting; mode/recursion/upgrade rules are represented; and no hidden callback, queue, join, condition, barrier, I/O, or external-lock edge closes an unmodeled cycle. The theorem does not prove fairness or bounded waiting.

### Answer 3

Balance is mutable, so simultaneous transfers can choose opposite account order; replace it with immutable identity after gathering and deduplicating the full set. Logging is an unknown lower/independent dependency; capture fields and log after release. Joining under component locks can deadlock worker cleanup; cancel/wake, release, then join. Timed retry bounds attempts but symmetric retries can livelock and partial effects may escape. Use canonical ordering first; otherwise complete rollback plus one deadline, bounded asymmetric backoff, cancellation, and metrics. Draw normal and shutdown wait graphs and enforce ranks at runtime.

### Answer 4

Resolve requested accounts to immutable unique IDs without holding peer locks, reject or deduplicate repeated aliases, and sort by (account-level,ID). Acquire in that order, recording guards only after success. If deletion/membership can race, use stable lifetime references and revalidate existence/version after all locks are held. Perform no callback, I/O, join, or blocking submission while held. Compute/commit the invariant-restoring transition, then release in reverse order. On timeout/cancellation/failure, release only acquired guards in reverse and return without escaped partial effects; if effects require rollback, use a transaction owner. Deletion waits for references/guards to quiesce.

### Answer 5

Internal evidence can validate the rank theorem, finite order-pair counts, wait-graph reasoning, primary-source currency, snippet output, local links, and matched exercises. It cannot establish alarm thresholds, sensor validity, clinical timing, device hazards, fail-safe behavior, hardware response, human factors, cybersecurity controls, regulatory compliance, or deployment fitness. Named authorized clinical, medical-device systems, controls, hardware, real-time, functional-safety, software verification, cybersecurity, human-factors, quality, and regulatory reviewers must approve the actual requirements, implementation, evidence, and operation. This chapter claims no external review.
