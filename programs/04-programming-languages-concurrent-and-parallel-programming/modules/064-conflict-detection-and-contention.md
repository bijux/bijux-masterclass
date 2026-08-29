---
module_id: CONPAR-064
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 64
title: Conflict Detection and Contention
status: complete
last_verified: 2026-08-29
---

# Conflict Detection and Contention

## One-Page Review

### Governing question

How should a transactional runtime identify incompatible concurrent attempts, preserve safety independently of victim policy, and resolve contention without turning rare conflicts into starvation, retry storms, priority failure, or resource collapse?

### Essential definitions

- A **transactional conflict** occurs when concurrent attempts access one logical location and at least one access writes, subject to the system's serialization model.
- **read-after-write (RAW)**, **write-after-read (WAR)**, and **write-after-write (WAW)** name access-order dependencies; read-read overlap alone does not conflict in a single-version read model.
- **conflict detection** discovers actual or potential incompatible attempts; **validation** establishes that one attempt's observations remain consistent.
- **eager detection** notices conflicts during transactional access; **lazy detection** defers them toward validation/commit.
- A **visible read** records shared reader metadata; an **invisible read** normally records only private metadata.
- **ownership granularity** is the amount of state represented by one conflict/lock record: word, object, stripe, page, partition, or global state.
- A **false conflict** is an implementation-level collision between semantically compatible operations; a **missed conflict** can admit an illegal history.
- A **contention manager** chooses delay, abort, priority, helping, or fallback after a conflict; it must not define safety.
- **wasted work** is speculative computation discarded on abort, including validation and cache effects.
- **starvation** means one enabled logical operation is repeatedly denied completion while others progress.

### Central model, mechanism, or theorem

Derive conflicts from the abstract serialization condition, map every read and write to metadata, and detect incompatible overlap before illegal publication or unsafe speculative observation. Once a real or conservative conflict is identified, a separate policy selects which attempt proceeds. Safety must hold for every permitted victim choice. Eager detection limits doomed work but adds access-path metadata and early arbitration; lazy detection reduces coordination but discovers conflicts after more speculation. No policy is universally optimal: workload topology, transaction length, priority, oversubscription, retry cost, and lifecycle determine the outcome.

### Critical invariants

Every conflict capable of violating the stated isolation/opacity condition is detected or prevented. Metadata identity, lifetime, granularity, and memory ordering match the data it represents. Aborted attempts cannot publish. Arbitration cannot allow both incompatible attempts to commit. Safety does not depend on timing, fairness, or a preferred policy. Transaction priority is authenticated and bounded. Retry has admission/backoff/fallback limits. Cancellation, exceptions, nesting, irreversible effects, thread pauses, and shutdown release ownership and preserve one terminal result. Metrics distinguish logical operations from attempts.

### Common failures

Systems treat a metadata collision as a semantic conflict without measuring false aborts; detect WAW but omit read dependencies; validate only at commit while doomed unmanaged code executes; make all readers visible and create a reader-list hotspot; use one global clock/lock that serializes disjoint work; let a paused transaction retain ownership; always let requester win and livelock; always favor oldest and block urgent work; trust client-supplied priority; retry immediately under saturation; average abort rates across hot and cold keys; or route to a fallback that optimistic attempts ignore.

### Compact example

T reads x and will write y; U reads y and will write x. Each sees the old state. Their dependency graph contains a cycle if both commit, so at least one must abort under serializable semantics. Choosing T because it is older may improve starvation resistance, while choosing U because it is urgent may meet policy. Either choice is safe only if the loser cannot publish and the winner revalidates as required.

### Connections

[Software Transactional Memory](061-software-transactional-memory.md) supplies transactional atomicity and opacity. [Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md) supplies dependency completeness. [Transactional Retry and Composition](063-transactional-retry-and-composition.md) distinguishes semantic waiting from conflict abort. [Contention Management in Nonblocking Algorithms](059-contention-management-in-nonblocking-algorithms.md) provides broader retry-control foundations.

## Governing Question

Which conflicts must be represented, when should they be detected, and how can the runtime choose a loser under real workloads without smuggling correctness into a heuristic or making liveness claims stronger than its assumptions?

The answer separates semantics, detection mechanism, and resolution policy. An implementation can change policy without changing legal histories; if changing policy changes safety, its core protocol is incomplete.

## Why This Matters

Optimistic concurrency buys parallelism by permitting overlapping attempts. Conflicts are the bill. Detect too little and illegal states commit. Detect too much and independent work aborts. Detect too late and the system wastes expensive computation or lets doomed code encounter inconsistent state. Detect too early and every access pays shared metadata traffic.

Contention is workload-shaped. A uniform benchmark can look excellent while one production key collapses. A short transaction repeatedly kills a long one; a long old transaction blocks fresh work; all threads retry in synchrony; a preempted owner stalls a partition; a high-priority control action waits behind low-priority speculation. Average throughput hides per-key tails, wasted CPU, retained versions, and starvation.

Transactional syntax does not choose a policy. The system needs an explicit contract: correctness condition, conflict scope, progress class, priority authority, resource bounds, fallback, observability, and shutdown. This chapter develops that contract.

## Prerequisites and Retrieval

Retrieve:

- conflict-free serial histories from [Linearizability Proofs](058-linearizability-proofs.md);
- progress vocabulary from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md);
- retry/backoff evidence from [Contention Management in Nonblocking Algorithms](059-contention-management-in-nonblocking-algorithms.md);
- STM metadata from [Software Transactional Memory](061-software-transactional-memory.md); and
- complete read/predicate sets from [Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md).

Retrieval prompt: for two transactions that each read one account and write the other, draw the dependency edges for both possible serial orders and explain why a victim heuristic cannot repair a missed edge.

## Learning Objectives

After completing this module, a learner can:

1. derive RAW, WAR, WAW, predicate, and lifecycle conflicts from an abstract history;
2. distinguish conflict detection, validation, arbitration, and semantic retry;
3. compare eager, lazy, and mixed detection with visible or invisible readers;
4. reason about ownership granularity and false/missed conflicts;
5. construct and analyze transaction conflict graphs;
6. compare requester-wins, holder-wins, timestamp, work, priority, randomized, and serialized policies;
7. specify starvation, priority, admission, backoff, and fallback behavior;
8. design safe metadata/lifetime, cancellation, and shutdown protocols;
9. build representative correctness and performance evidence; and
10. demand additional human review for real-time and safety-critical contention policy.

## Core Exposition

### Begin from legal histories

Let T and U overlap. Their physical accesses matter only through the abstract transaction specification and correctness condition. If they can be placed in either serial order with the same results and invariant, their overlap need not force abort. If no legal order contains both, the concurrency-control protocol must delay or abort at least one.

For single-version locations, read-read overlap is compatible. WAW requires a defined order so one write is not silently lost. If T reads a version that U later overwrites, the RAW/WAR naming depends on which temporal or dependency perspective is used; always state edge orientation instead of relying on the acronym. Predicate reads add conflicts with inserts, deletes, or reclassification that change membership.

Conflict is not identical to a host-language data race. Correct STM instrumentation can coordinate physical data accesses; uninstrumented racy access may remain undefined. Conversely, two properly atomic metadata operations can expose a transactional conflict that must be resolved at the abstract level.

### Conflict graphs

A serialization graph has one vertex per committed or candidate transaction and a directed edge for each dependency that constrains order. An acyclic graph admits a topological serial order under the graph's model. A cycle shows those candidates cannot all commit under serializability.

Suppose T reads x before U writes x, giving T-before-U. U reads y before T writes y, giving U-before-T. The cycle requires aborting or reexecuting at least one. If T aborts, its next attempt reads U's state and may commit in U-before-T order.

Graph reasoning depends on complete dependencies and the selected isolation level. Snapshot isolation often resolves WAW conflicts but can admit a cycle formed through disjoint writes and shared reads—write skew. Range and absence dependencies need index/predicate authorities. A graph over only explicit write targets can falsely appear acyclic.

Online STM rarely builds a complete graph literally. Versions, locks, timestamps, ownership records, read markers, and validation encode enough ordering to prevent forbidden cycles. The proof connects that local metadata to the global history.

### Detection versus validation

Conflict detection answers “are these attempts incompatible or potentially so?” Validation answers “does this attempt still have a consistent justification?” A writer can detect ownership conflict immediately, while an invisible reader discovers a conflicting commit by version validation later. An opacity mechanism may validate incrementally even when no arbitration is yet needed.

Semantic `retry` is different again: the program says its guard is false and waits for state. A conflict abort is imposed because another attempt invalidated or reserved state. Recording them as one metric hides hot predicates, scheduler wakes, and actual intertransaction interference.

### Eager detection

Eager systems acquire or announce ownership on first write and may publish visible read markers. A conflicting access discovers the other attempt immediately. The manager can abort or delay one before it performs more work. This benefits expensive transactions or high conflict, and can support targeted reader invalidation.

Costs include atomic metadata operations on the access path, larger shared reader structures, cleanup after abort, and exposure to preempted owners. Acquiring several objects can deadlock in blocking designs unless ordered, try-acquire-and-abort, or otherwise coordinated. In obstruction-free designs, an active attempt may abort another's descriptor rather than wait, but liveness still needs policy.

Eager acquisition is not automatically pessimistic locking: the loser can abort and a nonblocking algorithm can take over. Nor does early conflict imply incremental opacity validation for every fractured-read hazard.

### Lazy detection

Lazy systems keep tentative writes private and defer write ownership/conflict checks to commit. Disjoint or ultimately aborted transactions avoid shared ownership traffic, and invisible readers remain cheap. Commit acquires the write set, validates reads, and chooses a serial order.

The risk is wasted work and a burst of acquisition at commit. Two long transactions can compute for seconds before one loses. Doomed unmanaged code needs consistent-read protection before final validation. Large write sets create lock-order/cache storms. Commit latency can dominate tails.

Lazy detection can be attractive when conflicts are rare and attempts are short or expensive shared metadata would dominate. It is not “no conflict detection”; it moves the point and changes evidence.

### Mixed strategies and reader visibility

A mixed design can detect WAW conflicts eagerly while allowing a reader/writer overlap until version validation, or use a global commit counter to trigger detailed read-set scans only after some writer commits. It can switch policy by access type or workload, but every mode transition belongs to the proof.

Visible readers announce themselves per object or stripe. A writer can identify/abort/wake readers and reason about some privatization cases, but read-heavy workloads write shared cache lines and need bounded reader metadata. Invisible readers store their read sets privately, improving read scalability but forcing writers to be oblivious and readers to validate.

No combination dominates. The 2006 RSTM study found strategy results workload-dependent on its historical platform; that is evidence about a design space, not a current universal ranking. Modern hardware, runtimes, topology, and payload require new measurement.

### Granularity and false conflicts

Per-word metadata approximates semantic conflicts closely but costs memory and locality. Object granularity is natural when operations own objects. Hash-striped ownership reduces metadata but unrelated locations mapped to one stripe conflict. Page or global granularity is simpler and more conservative.

False conflicts preserve safety when the protocol aborts extra attempts, but can destroy scaling or fairness. Missed conflicts violate correctness. Measure stripe occupancy, false-abort samples, and hot metadata separately from actual application-key conflicts.

Changing granularity at runtime is delicate. Remapping while transactions hold old stripe identities can make conflicts invisible. Use quiescence, versioned tables, dual checking during transition, or process-level configuration with proof and tests.

### Executable arbitration model

The following model derives pairwise conflicts from read/write sets and applies three deterministic victim policies. It demonstrates that policy changes the survivor, not the conflict relation. It does not implement concurrent STM, validation, serialization, waiting, or a progress theorem.

<!-- bijux-verify: {"id":"transaction-conflict-arbitration","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"conflicts=[('T_old', 'U_urgent')]\nrequester_wins=U_urgent\noldest_wins=T_old\npriority_then_age=U_urgent\ndisjoint_conflict=False\nloser_oldest=U_urgent\n","stderr":""}} -->
```python
transactions = {
    "T_old": {"reads": {"x"}, "writes": {"y"}, "age": 12, "priority": 1},
    "U_urgent": {"reads": {"y"}, "writes": {"x"}, "age": 3, "priority": 5},
    "V_disjoint": {"reads": {"z"}, "writes": {"w"}, "age": 7, "priority": 2},
}


def conflicts(left, right):
    return bool(
        (left["writes"] & (right["reads"] | right["writes"]))
        | (right["writes"] & left["reads"])
    )


names = list(transactions)
pairs = []
for index, left_name in enumerate(names):
    for right_name in names[index + 1:]:
        if conflicts(transactions[left_name], transactions[right_name]):
            pairs.append((left_name, right_name))

print(f"conflicts={pairs}")
print("requester_wins=U_urgent")
oldest = max(("T_old", "U_urgent"), key=lambda name: transactions[name]["age"])
print(f"oldest_wins={oldest}")
priority = max(
    ("T_old", "U_urgent"),
    key=lambda name: (transactions[name]["priority"], transactions[name]["age"]),
)
print(f"priority_then_age={priority}")
print(f"disjoint_conflict={conflicts(transactions['T_old'], transactions['V_disjoint'])}")
loser = "U_urgent" if oldest == "T_old" else "T_old"
print(f"loser_oldest={loser}")
```

Real arbitration cannot trust arbitrary client priority and must ensure exactly the chosen loser is prevented from publishing. Age units and tie-breaking require a specified authority.

### Victim policies

**Requester wins (aggressive):** abort the current holder. It clears obstacles quickly but two requesters can repeatedly kill each other; preemption timing affects results.

**Holder wins (timid):** requester waits or aborts. It protects invested holder work but a paused or failed holder can dominate, and late high-priority work suffers.

**Oldest/timestamp wins:** preserve an age across retries so repeatedly aborted operations eventually dominate. It can reduce starvation, but one old long transaction may convoy younger work. Timestamp generation/wrap and restart semantics need definition.

**Work/karma-based:** favor the attempt with more completed accesses, accumulated conflict credits, or estimated remaining cost. This can protect investment but rewards bloated transactions, is gameable, and measures work imperfectly.

**Priority/deadline-aware:** favor authenticated criticality or slack. It is necessary in some real-time contexts but can starve background work, create priority inversion in allocators/reclaimers, and needs bounded admission. An ordinary user must not label every request critical.

**Randomized/backoff:** break symmetry and reduce synchronized collision. It supports probabilistic, not deterministic, guarantees and needs injected randomness for reproducible testing.

**Serialize/fallback:** after repeated aborts, route through a lock, owner queue, or single-transaction lane. Optimistic attempts must observe the fallback gate. This bounds waste but changes blocking and can create a bottleneck.

Policies can be hybrid: spin briefly, back off, age, then serialize. Every threshold is workload policy, not a correctness constant.

### Safety independent of policy

When T encounters U, both may tentatively believe they won under races. Arbitration needs atomic status transitions or an ownership protocol so at most one incompatible attempt remains commit-eligible. An abort status is terminal for that attempt; it cannot later publish from a delayed core.

If a manager callback can wait, allocate, log, or call user code while holding metadata, it expands deadlock, reentrancy, and progress obligations. Keep safety state minimal and manager decisions bounded. A manager crash/exception must default to a safe outcome.

Helping transfers responsibility for completing another transaction. It can strengthen progress but requires immutable/published descriptors, exactly-once logical completion, safe payload effects, and reclamation. It is not merely “choose the other winner.”

### Starvation and livelock

Immediate symmetric retry can livelock: transactions repeatedly collide and abort without commit. System throughput can remain nonzero while one hot operation starves. Measure per-logical-operation attempts and oldest age, not only global commits.

Preserving age across retries, queueing contenders, randomized delay, or serialized fallback can improve progress. Backoff must respect one total deadline and cancellation; sleeping threads retain state and memory. Oversubscription can make spin/backoff worse by delaying the transaction that must release ownership.

An obstruction-free core guarantees completion only after an attempt runs in isolation long enough. A contention manager is intended to create such intervals in practice; empirical success is not a universal lock-free/wait-free theorem. State scheduler and failure assumptions.

### Priority, deadlines, and inversion

Transactional abort avoids one kind of lock-holder blocking but not all priority inversion. A high-priority attempt can repeatedly conflict with low-priority writers; runtime workers, allocation, GC, validation, and fallback locks can block it. Aborting a low-priority holder can waste near-complete work and increase overall deadline misses.

Real-time contention management needs admission, bounded transaction length/access sets, priority propagation, abort/cleanup bounds, retry limits, and schedulability analysis. Deadline order alone is not proof. If a transaction can perform unbounded user computation, no victim rule creates a response-time bound.

Priority is an authorization surface. Map trusted operation classes to bounded internal priority, rate-limit critical lanes, audit overrides, and prevent cross-tenant priority theft.

### Nested and composed transactions

Flattened nesting inherits the outer transaction's conflicts and priority. Closed nesting may retry an inner transaction without discarding all outer work, changing accounting and victim policy. Open nesting publishes inner effects and needs semantic compensation; physical conflict freedom does not ensure the outer invariant.

`orElse` branch attempts can read large alternative sets, widening later validation and wake behavior. Do not let speculative branch priority or work credits leak after branch retry unless semantics explicitly merge them.

Composition can create a transaction much larger than component designers measured. APIs should expose or bound transactional footprint, not hidden global reads.

### Effects, cancellation, and lifecycle

Conflict abort can rerun code, so external effects remain prohibited or deferred as in module 061. Contention-manager logging must be bounded and must not alter scheduling accidentally through blocking I/O. Use in-memory counters/traces with logical and attempt identities.

Cancellation racing arbitration needs one terminal attempt status. If commit won before cancellation, report committed/uncertain according to API; do not resurrect and publish a cancelled loser. Release ownership, visible-reader entries, waiters, hazards/epochs, versions, timers, and priority tokens on every path.

Shutdown stops admission, resolves active attempts, opens any fallback gate, wakes/cancels waiters, drains committed effect intents, and reclaims metadata only after no thread can access it. A paused thread or foreign callback must not retain an unloadable manager indefinitely.

### Operational measurement and adaptation

Record logical transactions, attempts, commits, semantic retries, conflict aborts by RAW/WAR/WAW/predicate/metadata cause, victims/winners by policy, read/write sizes, duration at conflict, discarded CPU, validation work, false-conflict samples, ownership wait, backoff, fallback entries, oldest age, priority class, and retained bytes.

Slice by transaction type, key/partition bucket, topology, and lifecycle state without exposing sensitive keys or exploding cardinality. An overall 2% abort rate can hide a tenant at 95%. Report p50/p95/p99 attempts and latency, not averages alone.

Adaptive switching needs hysteresis, minimum sample size, bounded modes, versioned configuration, and a safe transition protocol. The controller itself can oscillate when conflict causes latency, latency triggers mode changes, and mode changes move contention. Shadow decisions and compare before actuation.

### Evidence plan

Prove complete conflict representation, metadata/data pairing, exactly-one winner, loser nonpublication, validation/opacity, cleanup, and policy-independent safety. State progress assumptions per mode. Model small histories with cycles, aliases, predicate phantoms, simultaneous status changes, and nested branches.

Test every access-type pair, conflict timing, read visibility, detection mode, ownership stripe collision, version wrap/reuse, manager exception, cancellation at arbitration/commit, paused winner/loser, fallback overlap, shutdown, and reclamation. Inject deterministic scheduling and randomness.

Benchmark low/medium/high/skewed conflict, short/long/mixed transactions, read/write-set distributions, disjoint false-sharing, oversubscription, NUMA, priority classes, bursts, overload, failure, and close. Compare identical semantics with a competent lock, sharding, owner queue, snapshot, and relevant STM policies. Historical policy rankings do not replace current evidence.

## Definitions and Notation

- `R(T)`, `W(T)`: semantic read and write sets of attempt T.
- `C(T,U)`: conflicts when `W(T) ∩ (R(U) ∪ W(U))` or `W(U) ∩ R(T)` is nonempty.
- `G=(V,E)`: transaction serialization/conflict graph with directed dependency edges.
- `T → U`: the defined dependency requires T before U.
- `owner(m)`: attempt currently owning metadata record m.
- `status(T)`: active, committed, or aborted; terminal states do not reverse.
- `age(T)`, `priority(T)`, `work(T)`: policy inputs with declared authority and units.
- `A(T)`: attempts consumed by one logical transaction.
- `W_lost(T)`: measured speculative work discarded.
- `F`: fallback state that optimistic commits must observe.

The conflict expression assumes single-version read/write semantics and complete logical sets. Multi-version, predicate, commutative, or weakened-isolation designs need a different relation.

## Mechanisms, Invariants, or Proof Structure

### Detection soundness and completeness

Soundness in the conservative implementation sense permits reported false conflicts; completeness requires every pair/cycle whose joint commit violates the stated correctness condition to be prevented. Map each abstract dependency to one metadata/version/validation event and prove identity, lifetime, and ordering.

### Arbitration invariant

For any incompatible active T and U, the status/ownership protocol permits at most one to remain commit-eligible. Atomic state transitions linearize victim selection. Once aborted, an attempt cannot acquire new ownership or publish. The survivor still performs all required validation; winning arbitration is not automatic commit.

### Graph argument

Show each committed dependency edge is represented in G and the commit protocol admits only an acyclic graph (or the selected correctness model's equivalent). Assign a topological serialization. If a candidate edge closes a cycle, abort/delay one candidate before publication.

### Liveness argument

Separate obstruction-free core progress from manager policy. State finite-delay, scheduler, priority, allocation, cleanup, and fallback assumptions. Show symmetry is eventually broken or contenders are serialized; then bound or explicitly decline to bound per-transaction completion.

## Alternatives and Trade-Offs

| Design choice | Advantage | Principal cost |
|---|---|---|
| Eager writer ownership | early waste avoidance | access metadata, paused owners |
| Lazy commit acquisition | cheap speculation at low conflict | late abort and commit burst |
| Visible readers | targeted conflicts/invalidation | read-side writes and cleanup |
| Invisible readers | scalable read path | validation and writer blindness |
| Fine ownership granularity | fewer false conflicts | metadata/cache footprint |
| Coarse/striped ownership | compact and simple | false aborts/hot stripes |
| Age/priority policy | starvation or deadline control | convoying, authorization, complexity |
| Randomized backoff | symmetry breaking | probabilistic behavior and delay |
| Serialized fallback | bounded repeated waste | blocking/bottleneck and coordination proof |
| Partition/owner architecture | removes cross-partition conflict | skew, migration, global operations |

Detection and policy choices form a matrix. Evaluate complete combinations; a good manager cannot compensate for pathological metadata, and precise detection cannot guarantee fair resolution.

## Failure Modes and Misconceptions

- **“Any overlap is a conflict.”** Read-read and semantically commutative operations can be compatible.
- **“Physical words define semantics.”** Predicates and logical objects may span or share metadata.
- **“False conflicts are harmless.”** Safe, yes; operationally potentially disastrous.
- **“Validation and detection are the same.”** They answer related but different questions.
- **“Eager is always faster.”** Shared metadata can dominate low-conflict work.
- **“Lazy means no coordination.”** Commit must still acquire, validate, and publish.
- **“The winner may commit.”** It must still satisfy full validation.
- **“The manager makes the STM correct.”** Safety must survive every allowed victim decision.
- **“Oldest wins prevents all starvation.”** It can convoy and depends on bounded delays/scheduling.
- **“Priority eliminates inversion.”** Runtime, allocator, reclaimer, and fallback paths remain.
- **“Backoff guarantees liveness.”** It is probabilistic/policy behavior under assumptions.
- **“Average abort rate is enough.”** Hot keys and individuals can collapse.
- **“Fallback is separate.”** Both paths need one serialization protocol.
- **“Abort is free.”** Work, cache, allocation, versions, and energy are consumed.
- **“One benchmark selects a policy.”** Transaction mix and hardware change the ranking.

## Worked Examples

### Example 1

**Read-read compatibility.** T and U read x and write disjoint y/z without cross-dependencies. Their x reads alone need no victim; complete validation decides whether the writes remain legal. **Conclusion:** overlap does not imply conflict.

### Example 2

**WAW lost update.** T and U both propose replacing x from version 4. Write ownership/compare-version permits one commit; the loser recomputes from the winner's version. **Conclusion:** WAW arbitration must establish an order.

### Example 3

**Write-skew cycle.** Each on-call doctor sees the other active and deactivates itself. Disjoint writes hide the shared-read cycle from WAW-only detection. Validate an invariant/predicate authority or serializable dependencies. **Conclusion:** write sets alone are incomplete.

### Example 4

**False stripe conflict.** Addresses x and y hash to stripe 9 though operations are independent. One abort is safe but reduces concurrency. Increase or repartition metadata only with quiescent/versioned transition. **Conclusion:** granularity is measurable policy with proof constraints.

### Example 5

**Eager versus lazy.** Two transactions conflict in their first access then compute for 500 ms. Eager detection can avoid most losing work; lazy detection wastes it but might be cheaper for the other 99.9% disjoint workload. **Conclusion:** expected conflict timing and cost choose the mechanism.

### Example 6

**Aggressive livelock.** T requests U's object and aborts U; restarted U requests T's other object and aborts T. Preserved age, randomized asymmetry, or serialization can break the cycle. **Conclusion:** requester-wins alone offers weak practical progress.

### Example 7

**Paused oldest transaction.** Oldest-wins protects T, but T is descheduled while younger operations repeatedly abort. Scheduler-aware delay/fallback or bounded ownership is necessary. **Conclusion:** timestamp policy cannot defeat scheduler pauses by itself.

### Example 8

**Priority abuse.** Tenants label all writes urgent, starving maintenance. Authenticate priority from operation class, cap urgent admission, age background work, and audit overrides. **Conclusion:** contention priority is security and capacity policy.

### Example 9

**Uncoordinated fallback.** T takes a global fallback lock after retries while optimistic U ignores it and publishes. Subscribe optimistic begin/commit to F or serialize construction at an owner. **Conclusion:** a slow path outside the proof is unsafe.

### Example 10

**Industrial robot collision envelope.** Competing trajectory transactions update shared workspace reservations under deadlines. Conflict resolution cannot rely only on throughput: it needs authenticated criticality, bounded computation/abort, independent physical interlocks, stale-sensor handling, fail-safe stop, deterministic fallback, and named robotics, controls, real-time, formal-methods, hardware, cybersecurity, human-safety, operations, regulatory, and independent assurance review; none is claimed here. **Conclusion:** high-stakes priority policy needs end-to-end safety evidence beyond STM arbitration.

## Cross-Program Connections

- **Databases:** conflict graphs, isolation, write skew, OCC, locking, and predicates share foundations.
- **Computer architecture:** cache lines, atomics, NUMA, HTM capacity, and preemption shape metadata cost.
- **Operating systems:** scheduling and priority determine holder delay and inversion.
- **Formal methods:** graph acyclicity, opacity, status invariants, and liveness assumptions make claims reviewable.
- **Security:** priority authority and adversarial hot keys are attack surfaces.
- **Performance engineering:** skew, discarded work, false sharing, tails, and overload determine policy.
- **Software architecture:** partitioning, owners, admission, fallback, and shutdown can remove or contain contention.
- **Safety engineering:** deadline arbitration must coexist with independent physical protection.

## References

1. Maurice Herlihy, Victor Luchangco, Mark Moir, and William N. Scherer III, “Software Transactional Memory for Dynamic-Sized Data Structures,” PODC 2003. <https://doi.org/10.1145/872035.872048>
2. William N. Scherer III and Michael L. Scott, “Advanced Contention Management for Dynamic Software Transactional Memory,” PODC 2005. <https://doi.org/10.1145/1073814.1073861>
3. Rachid Guerraoui, Maurice Herlihy, and Bastian Pochon, “Toward a Theory of Transactional Contention Managers,” PODC 2005. <https://doi.org/10.1145/1073814.1073863>
4. Rachid Guerraoui, Maurice Herlihy, and Bastian Pochon, “Polymorphic Contention Management,” DISC 2005. <https://doi.org/10.1007/11561927_23>
5. Michael F. Spear, Virendra J. Marathe, William N. Scherer III, and Michael L. Scott, “Conflict Detection and Validation Strategies for Software Transactional Memory,” DISC 2006. <https://doi.org/10.1007/11864219_13>
6. Dave Dice, Ori Shalev, and Nir Shavit, “Transactional Locking II,” DISC 2006. <https://doi.org/10.1007/11864219_14>
7. Rachid Guerraoui and Michał Kapałka, *Principles of Transactional Memory*, 2010. <https://doi.org/10.1007/978-3-031-02002-5>
8. Rachid Guerraoui and Paolo Romano, editors, *Transactional Memory: Foundations, Algorithms, Tools, and Applications*, 2015. <https://doi.org/10.1007/978-3-319-14720-8>
9. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
10. Nir Shavit and Dan Touitou, “Software Transactional Memory,” PODC 1995. <https://doi.org/10.1145/224964.224987>

## Exercises

### Exercise 1

Classify read-read, RAW/WAR, WAW, predicate, false-stripe, and host-language data-race cases. State which layer must handle each.

### Exercise 2

Build the dependency graph for T reading x/writing y and U reading y/writing x. Show why both cannot commit and how reexecution after either victim yields a serial order.

### Exercise 3

A runtime uses eager striped writer ownership, invisible readers, and commit validation. Diagnose a hot stripe with high aborts but disjoint application keys; design safe evidence and a granularity change.

### Exercise 4

Choose detection and contention policy for a workload with 99% short disjoint reads and 1% long hot-key writes under oversubscription. Include admission, starvation, priority, fallback, and metrics.

### Exercise 5

A power-grid controller uses transactional updates for competing switching plans with deadlines. Specify correctness, arbitration, liveness, failure/fallback evidence, and mandatory human review.

## Answers to the Exercises

### Answer 1

Read-read overlap is normally compatible under single-version semantics. RAW/WAR and WAW can constrain serialization and must be represented by STM metadata/validation; predicate conflicts require an index/range/invariant authority. A false stripe conflict is an implementation collision: safely aborting is conservative but should be measured and reduced without missing conflicts. A host-language data race is governed by the language memory model and cannot be repaired merely by a transactional graph. Exact edge orientation must be declared, and multi-version or commutative semantics may change compatibility.

### Answer 2

T's read of x before U's write requires T before U; U's read of y before T's write requires U before T. The two-edge cycle has no topological serial order, so a serializable protocol must reject at least one candidate. If T aborts, U can commit x, then T reruns, reads U's x, and commits y in U-before-T order. If U aborts, the symmetric T-before-U order results. The loser must publish nothing, and the winner still validates other dependencies.

### Answer 3

The stripe maps unrelated write locations to one ownership record, creating false WAW conflicts; invisible readers add validation but are not the source of this observed writer collision. Confirm with privacy-safe samples mapping transaction types/logical partitions to stripe IDs, actual read/write-set intersection, conflict timing, discarded work, and cache/NUMA metrics. Test a larger or partition-aware table under identical histories/workloads. Do not remap live ownership in place: quiesce attempts and replace the table, use generation-tagged tables with dual checking during migration, or deploy a process-level configuration. Reprove metadata identity, wrap/lifetime, acquisition, validation, and shutdown; compare memory/cache cost and adversarial skew.

### Answer 4

Use invisible reads with a cheap global-change filter/per-object validation for the dominant disjoint reads, and lazy or mixed writer acquisition so reads avoid shared markers. Partition the hot key or route its writes through a coordinated owner/serialized lane if semantics permit. Preserve age across aborts, bound attempts and total deadline, add randomized/injected backoff only below saturation, and make fallback visible to optimistic commits. Authenticate any urgent class and cap its admission; ensure background aging. Measure by transaction/key bucket: attempts, RAW/WAR/WAW and false conflicts, conflict point, discarded CPU, validation scans, p99/max latency, oldest age, fallback, queue depth, CPU, versions/memory, and shutdown. Compare against a lock/owner design; 99% mix must not hide hot-write collapse.

### Answer 5

Specify switching-plan state, topology, measurements and freshness, permissions, interlocks, legal transitions, and invariants preventing unsafe energization. Derive all predicate/conflict authorities and prove opacity/serialization, exactly-one winner, loser nonpublication, bounded cleanup, and coordinated fallback. Deadline-aware arbitration needs authenticated criticality, bounded transaction work/access sets, scheduler/allocator/reclaimer bounds, admission and schedulability analysis; timeout or controller failure selects a fail-safe physical state, not an optimistic retry. Test dependency cycles, simultaneous plans, stale/lost sensors, priority inversion/abuse, paused owners, overload, cancellation at commit, restart/reconciliation, network partition, hardware-in-loop, and independent protection. Named power-systems protection, control/real-time, electrical safety, formal-methods, hardware, cybersecurity, human-factors, grid operations, regulatory, and independent assurance reviewers must approve requirements, evidence, fallback, and residual risk. No internal module review is deployment approval.
