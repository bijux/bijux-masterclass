---
module_id: CONPAR-008
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 8
title: Critical Sections and Shared-State Invariants
status: complete
last_verified: 2026-08-29
---

# Critical Sections and Shared-State Invariants

## One-Page Review

### Governing question

Which shared-state invariant must appear true at every externally observable boundary, which operations may temporarily break it, and what synchronization discipline makes every interference step preserve the abstraction?

### Essential definitions

- A **shared-state invariant** is a predicate that must hold for every state observable outside a protected transition.
- A **critical section** is a region whose interfering executions are restricted so its protected transition appears indivisible at the chosen abstraction boundary.
- **Mutual exclusion** permits at most one participant in a protected region at a time; it is a mechanism property, not by itself a correctness proof.
- A **representation invariant** constrains the concrete fields of one abstraction; a **global invariant** spans multiple owners or resources.
- A **precondition** must hold when an operation is invoked; a **postcondition** describes its completed result.
- An **abstraction function** maps concrete representation state to the abstract value exposed by the component.
- A **linearization point** is the event at which an operation can be viewed as taking effect between invocation and response.
- **Interference freedom** means each atomic action of one participant preserves the assertions on which other participants rely.
- A **lock invariant** is the predicate associated with a synchronization authority: it holds when the lock is free and whenever ownership is transferred.
- **Exception safety** requires failure or cancellation to restore the invariant and release ownership according to a declared guarantee.
- An **open call** invokes unknown or external code without holding an internal lock, avoiding reentrancy and latency hazards after capturing or reserving safe state.

### Central model, mechanism, or theorem

Let concrete state (s) satisfy invariant (I(s)). Operation (O) has precondition (P_O), protected transition (delta_O), and postcondition (Q_O). A critical-section proof shows:

(I(s) and P_O(s)) implies I(delta_O(s)) and Q_O(s,delta_O(s)).

It also shows every access that relies on (I) uses the same synchronization authority, the region has exclusive ownership or an equivalent serializing rule, internal states that violate (I) are not observable, and release publishes the restored state according to the language memory model.

### Critical invariants

The protected scope follows the predicate, not a convenient field. Every reader and writer obeys the same authority. The invariant holds at acquisition and is restored before every release, return, exception, cancellation, callback, wait, or publication boundary. Lock identity and object lifetime are stable. Compound conditions are checked and changed under one serialization rule. External calls do not run while a private invariant is broken. Memory visibility accompanies exclusion. Nested locks follow a declared order. Metrics and debug paths do not bypass protection.

### Common failures

Teams lock individual fields while the invariant spans several; protect writers but not readers; use different locks for the same state; expose mutable aliases; release before restoring all fields; call user code while holding the lock; wait while retaining resources needed by the awaited work; make a lock reentrant to hide an ownership mistake; forget failure cleanup; use a read-write lock for “reads” that mutate caches; copy a pointer under lock and use it after reclamation; or infer correctness from the absence of concurrent entry alone.

### Compact example

Inventory has fields `available` and `reserved` with invariant `available + reserved = capacity`. Reservation decrements `available` and then increments `reserved`. The intermediate representation violates the invariant. If an observer can run between the writes, it sees impossible inventory. One critical section around both writes and every dependent read permits internal repair while ensuring observers see only the before or after abstract state.

### Connections

[Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md) identifies compound transactions; [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md) constrains nested locking and waiting; [Determinism and Reproducibility](007-determinism-and-reproducibility.md) distinguishes semantic results from schedules. The [program roadmap](../ROADMAP.md) next contrasts message ownership, workload-driven model choice, threads, mutexes, and condition variables.

## Governing Question

How do we derive the smallest correct protected region from an abstract state invariant, prove that every possible interference preserves that abstraction, and retain safety across errors, callbacks, cancellation, and memory visibility?

“Put a lock around it” is not a proof. The engineering task is to identify the state predicate, name its synchronization authority, define the boundaries at which the predicate must hold, show all participants follow the protocol, and evaluate the progress and performance consequences.

## Why This Matters

Most shared-state bugs do not arise because a single assignment is intrinsically difficult. They arise because a useful abstract transition spans several concrete events. A queue changes storage, head, tail, and count. A cache changes entries, eviction order, and byte budget. A subscription registry changes membership and reverse indexes. A reservation changes availability, ownership, expiry, and audit state. Other participants must not observe a mixture from two abstract moments.

Critical sections let an implementation temporarily violate its representation invariant while rebuilding a new valid state. That privilege is safe only if all observations that depend on the invariant are excluded and the state is restored before ownership transfers. A lock protecting only the first assignment can make each field data-race-free while leaving the abstract value impossible.

The consequences are both safety and liveness. Oversized regions serialize unrelated work, hold scarce resources during I/O, amplify priority inversion, and create deadlock edges. Undersized regions expose intermediate state. A correct design minimizes the region subject to preserving the complete transition, not subject to minimizing line count.

Language memory semantics matter. Mutual exclusion in source must also establish visibility of writes to the next owner. Java SE 26 specifies that monitor unlock happens-before a subsequent lock of the same monitor. POSIX.1-2024 specifies memory synchronization for successful mutex acquire and release operations. A home-grown Boolean “lock” without correct atomic and ordering semantics may fail both exclusion and publication.

## Prerequisites and Retrieval

Retrieve:

- states, transitions, invariants, induction, safety, and liveness from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- race classification, atomic regions, serialization authority, and linearization from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- wait-for graphs, strict lock ordering, starvation, and cancellation completeness from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- observational equivalence and deterministic aggregation from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- Hoare triples, abstraction functions, representation invariants, and proof by induction; and
- practical understanding of exceptions, resource cleanup, callbacks, iterators, and object lifetime.

Retrieval prompt: an object stores `capacity`, `available`, and a set of reservation IDs. Write two plausible invariants. Then mark which statements in reserve and cancel operations may temporarily violate each invariant and which boundary must restore it.

## Learning Objectives

After completing this module, a learner can:

1. derive a critical-section scope from a representation or global invariant;
2. distinguish mutual exclusion, atomicity, memory visibility, and progress guarantees;
3. write preconditions, postconditions, abstraction functions, and lock invariants;
4. prove invariant preservation for each protected transition and relevant interference action;
5. identify inconsistent lock identity, escaped aliases, unsafe callbacks, and check-then-act gaps;
6. design failure, cancellation, and owner-death recovery that restores protected state;
7. compare coarse, fine-grained, striped, read-write, optimistic, transactional, and ownership designs;
8. construct deterministic observation tests without treating them as universal proofs; and
9. recognize high-consequence invariant decisions requiring named authorized review.

## Core Exposition

### Begin with the abstract value

Write what the component means before selecting a lock. A bounded queue's abstract value may be a finite sequence with length at most capacity. Its concrete representation might use an array, head index, tail index, count, and generation. The abstraction function reconstructs the logical sequence. The representation invariant constrains index ranges, count, occupied slots, and wraparound relationships.

An operation is correct when it maps a valid concrete representation to another valid representation whose abstract value satisfies the sequential specification. Concurrency adds the obligation that interference cannot expose internal repair states or invalidate assumptions between steps.

For inventory, let (C) be capacity, (A) available units, and (R) a mapping from reservation IDs to positive quantities. A useful invariant is (0 <= A <= C) and (A + sum(R.values()) = C), excluding fulfilled or expired units if the state model represents them elsewhere. “A is nonnegative” alone misses duplication and leaks. The protected region must cover every field in the conservation equation and every path that changes it.

Distinguish invariants from preconditions. “Requested quantity is positive” is an input precondition. “Enough units exist” may be a guarded operation condition checked at the linearization point. “Conservation holds” is a state invariant. Confusing them causes implementations to assume a condition remains true after an unprotected check.

### A lock owns a predicate

Associate each lock with a documented invariant, not merely a list of variables. The predicate explains why apparently unrelated fields share a lock and which future fields must join its scope. When a thread acquires the lock, it may assume the lock invariant. It may temporarily break the invariant while it holds exclusive ownership. Before release, it must reestablish the invariant.

The discipline has four obligations:

1. **Authority:** every participant that reads or writes dependent state uses the same lock or a proven compatible mechanism.
2. **Exclusion:** no conflicting participant enters while the invariant may be false.
3. **Restoration:** all exits, including failures, restore the invariant.
4. **Publication:** release and subsequent acquisition make the restored writes visible under the memory model.

Locking writers but not readers violates authority unless reads use a safe immutable snapshot, atomic version protocol, or other proved design. A “diagnostic only” read can still crash, leak impossible values, or create false operational decisions. Metrics belong in the protocol if they touch protected representation.

Lock identity must remain stable. Locking on a replaceable field, boxed value, publicly reachable object, or freshly allocated mutex means participants may synchronize on different authorities. Prefer private final/immutable lock identity or synchronization embedded in the owning abstraction. Do not expose the lock unless external composition is an explicit, documented protocol.

### Derive the critical-section boundary

Start at the first observation whose validity must persist, include the authoritative commit, and end only after the invariant is restored and the result is safely captured. A check of `available >= quantity` and the decrement belong to one region because another reservation can invalidate the check. Updating the reservation index and conservation counters belongs in the same abstract transition.

Keep preparation that uses private immutable data outside. Validate syntax, allocate reversible local structures, and compute hashes before acquisition when those steps do not depend on shared state. Inside, revalidate shared premises, make the minimal authoritative transition, capture the immutable result or work token, and restore the invariant. After release, perform slow external work using that token.

This “prepare, commit, publish effect” shape reduces hold time without splitting atomicity. If the external effect can fail, model a reserved or pending state and add compensation/retry; never pretend a database transaction can roll back an email already sent.

Critical sections are semantic, not lexical. A helper called inside the region participates even if its code is elsewhere. An iterator or pointer returned from a protected method may carry access beyond lexical unlock. Prove the lifetime of every alias. Return immutable copies, stable handles with independent ownership, or operations that remain under the authority.

### Invariant preservation proof

For every operation, assume invariant (I) and precondition (P) on entry. Enumerate branches and show successful transition establishes (I and Q), rejected transition leaves the abstract state unchanged, and failure establishes the declared exception guarantee.

For reserve quantity (q):

- require (q > 0);
- while holding the authority, if (A < q), reject without mutation;
- otherwise set (A' = A-q) and add a fresh mapping entry with value (q);
- calculate (A' + sum(R') = A-q + sum(R)+q = C);
- establish uniqueness of the new ID and all range constraints; and
- release only after every representation field agrees.

Base case proves initialization satisfies (I). Inductive step proves each public transition preserves (I). Concurrency proof shows public transitions are serialized or that every finer-grained interference action preserves the assertions used by the other transitions.

Owicki-Gries-style interference reasoning asks whether every atomic assignment in one parallel component preserves assertions attached to another. Rely/guarantee reasoning states what interference a component assumes and what state changes it promises. These methods expose an important fact: an assertion checked outside the lock cannot be relied on inside unless the rely condition preserves it.

### Mutual exclusion is not the whole contract

A mutex can prevent overlapping entry and still leave the component wrong. The sequential transition may violate the invariant. A path may use another lock. A reference may escape. The wrong state may be protected. Release may lack the needed visibility in a broken custom primitive. The operation may deadlock or starve. The public contract may require a transaction across a database that the process mutex cannot govern.

Likewise, atomic variables do not automatically preserve a multi-field invariant. Individual atomic updates can expose intermediate combinations. A versioned optimistic protocol may work: read an even version, copy fields, reread the same version, and accept only if unchanged; writers mark mutation and publish a new version with correct ordering. That is a different proof, not “lock-free reading” by intuition.

### Reentrancy and callbacks

Calling unknown code while holding an internal lock is an open-ended dependency. The callback may call back into the component, acquire locks in another order, block on work that needs this lock, retain mutable references, or take unbounded time. Reentrant locks prevent self-deadlock for some same-thread recursion, but they do not make the invariant valid at callback time and do not prevent cross-thread cycles.

Use open calls: under lock, validate and capture an immutable notification, register a pending state if needed, then release and invoke the callback. If callback results change state, reacquire, revalidate a version or token, and commit a new transition. Define ordering, duplication, cancellation, and callback failure.

Reentrancy can be part of a deliberate monitor abstraction, but track recursion semantics and release counts. POSIX mutex types differ: recursive, error-checking, normal, and default behaviors are not interchangeable. Java monitors are reentrant, with each unlock reversing an acquisition. Portable reasoning follows the specified primitive rather than assumed behavior.

### Exceptions, cancellation, and owner death

Structured cleanup must release the lock on every path: language-managed monitor blocks, `defer`, `finally`, or scoped guards are preferable to hand-matched unlocks. Releasing is insufficient if an exception occurs after half a representation update. Either make intermediate operations nonthrowing, compute before mutation, use rollback, or enter an explicit recoverable state.

State the exception guarantee. A **strong guarantee** leaves the abstract state unchanged on failure. A **basic guarantee** preserves invariants but may change the abstract value. “No guarantee” is rarely acceptable for shared infrastructure. Cancellation is another failure edge and must not interrupt at an invariant-broken point unless cleanup repairs it.

Robust mutex owner death illustrates the distinction. POSIX.1-2024 may return `EOWNERDEAD` while granting ownership; the new owner must make protected state consistent. Acquiring the mutex does not magically restore the representation. Recovery needs durable intent, validation, rollback/roll-forward rules, and a decision for unrecoverable state.

### Waiting and condition predicates

Never hold a lock while waiting for an event whose producer needs that lock. Condition variables solve a specific pattern by atomically releasing the associated mutex while enrolling the waiter, then reacquiring before return. The invariant must hold before the wait releases ownership. On wake, recheck the predicate in a loop because notifications can be spurious or another consumer can invalidate it before reacquisition.

A condition predicate is shared state protected by the mutex. Notify after changing the predicate according to the primitive's protocol. Do not use notification as remembered state; the predicate is the truth. Later modules develop this mechanism fully.

### Granularity and composition

A coarse lock simplifies the invariant proof and supports atomic multi-field snapshots. It reduces parallelism and increases contention and failure radius. Fine-grained locks permit independent work but partition invariants, require ordering, and complicate operations spanning partitions.

Split locks only after defining separate owned predicates and a composition protocol. If a global invariant remains, use an ordered multi-lock transaction, a coordinator, immutable snapshots, or a transactional authority. Lock striping hashes many keys to fewer locks; it bounds lock count but creates collisions and needs a stable rule for multi-key operations.

Read-write locks help only when read operations truly do not mutate protected state, read duration is controlled, and fairness fits the workload. Lazy caches, access timestamps, iterators, and reference counts can turn “reads” into writes. Optimistic reads require validation before every dependent use.

## Definitions and Notation

Let concrete states be (S_c), abstract states (S_a), abstraction function (alpha: S_c -> S_a), and representation invariant (I subseteq S_c). Public operation (O) has precondition (P_O), transition relation (Delta_O), and postcondition (Q_O).

A critical region guarded by authority (L) is correct when all conflicting accesses participate; at most one exclusive owner may execute invariant-breaking events; (I) holds whenever (L) is unowned or ownership transfers; and acquire/release supply required visibility.

A Hoare-style sequential obligation is ({I and P_O} O {I and Q_O}). For concurrency, add interference freedom: each atomic action allowed outside (O)'s exclusive region preserves the assertions used by (O), or exclusion prevents it from occurring.

The lockset (Locks(e)) records authorities held at event (e). A nested acquisition rule uses strict rank (rho) and requires newly acquired rank to exceed all held ranks. This is a progress constraint distinct from invariant preservation.

An escaped alias is a reference that permits protected representation access without reestablishing the authority. A snapshot is safe only if immutable, independently owned, or validated against a version before every use covered by the claim.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Specify the abstract state and operations.** Do not start from existing fields.
2. **Define the abstraction function and invariant.** Include conservation, uniqueness, ranges, indexes, and lifecycle.
3. **Name one authority per predicate.** Document every reader, writer, and alias.
4. **Mark observable boundaries.** Acquisition, release, return, callback, wait, publication, failure, and cancellation matter.
5. **Derive the region.** Include check, commit, index maintenance, and result capture; move private preparation and slow effects out.
6. **Prove sequential preservation.** Cover success, rejection, exception, rollback, and recovery.
7. **Prove interference control.** Check common authority or each allowed fine-grained action.
8. **Check visibility and lifetime.** Use specified synchronization and prevent post-release dangling access.
9. **Analyze progress.** Add lock ordering, hold-time budgets, fairness, cancellation, and condition-predicate rules.
10. **Test and observe.** Force the intermediate window, assert invariant boundaries, instrument hold and wait time, and preserve limitations.

Maintain these invariants:

- the lock protects a named predicate rather than a historical code region;
- all dependent readers and writers use the same authority;
- invariant-breaking state never crosses an observable boundary;
- shared premises are revalidated at the serialization point;
- unlock publishes every field comprising the restored abstract state;
- aliases cannot outlive protection without independent ownership;
- callbacks, I/O, and waits do not occur while private state is inconsistent;
- every exit restores state and releases ownership exactly once;
- nested acquisition follows one strict order; and
- tests distinguish a witnessed violation from universal correctness.

## Alternatives and Trade-Offs

**One coarse mutex** gives a compact proof and consistent snapshots but serializes unrelated operations. **Fine-grained locks** improve concurrency only when ownership predicates can be partitioned; cross-partition operations add ordering and rollback.

**Read-write locks** admit concurrent readers but add state, fairness policy, and upgrade hazards. They lose value for short sections or write-heavy workloads. **Optimistic versioned reads** avoid reader locking on stable data but must discard every value derived from a failed validation.

**Atomic variables** are effective when the complete invariant fits one atomic transition. Packing fields into one word can enable compare-and-swap but constrains ranges and complicates decoding. Several atomics need a compositional proof.

**Transactions** serialize broader state and support rollback. Isolation phenomena, aborts, external effects, and distributed ownership remain. **Single-owner message processing** moves the critical section into an event loop; mailbox capacity, message order, and owner failure replace lock concerns.

**Immutable snapshots** make reads simple and publication explicit. Copy cost and reclamation can be high. Persistent structures share safely when their implementation and lifetime rules are correct.

**Reentrant locking** supports recursive abstractions but can expose broken invariants to callbacks and hide excessive coupling. Non-reentrant locks expose accidental recursion earlier. Choose from the component contract, not convenience.

## Failure Modes and Misconceptions

- **“The lock protects this variable.”** Correct scope follows the full predicate and every dependent access.
- **“Only writers need locks.”** Readers can observe partial state or race with lifetime changes.
- **“Each field is atomic.”** Multi-field conservation and ordering may still fail.
- **“Mutual exclusion proves correctness.”** The sequential transition, visibility, cleanup, and progress still need proof.
- **“A private method is safe.”** Call context, escaped aliases, and alternate entry paths determine protection.
- **“Reentrancy makes callbacks safe.”** It avoids one self-blocking case, not invariant exposure or lock cycles.
- **“Unlock in finally is sufficient.”** State may remain inconsistent before release.
- **“Read locks never modify.”** Lazy caches, statistics, iterators, and reference counts may write.
- **“Copying a pointer under lock is safe.”** The pointee may be reclaimed or mutated after unlock.
- **“Short critical sections cannot deadlock.”** Duration does not remove circular wait.
- **“A timeout repairs the invariant.”** It only triggers a policy; cancellation and recovery must restore state.
- **“Stress tests prove the lock scope.”** They cover observed schedules only.

## Worked Examples

### Example 1

**Question:** A queue protects `tail` with one mutex and `count` with another, but enqueue changes both.

**Reasoning:** The abstraction invariant relates position, occupied slots, and count. Independent observations can see a mixed transition.

**Conclusion:** Either one authority covers the predicate or a proven multi-authority protocol is required.

### Example 2

**Question:** Is reading `available` without the reservation lock harmless because the field is word-sized?

**Reasoning:** Atomic width does not ensure current visibility or consistency with the reservation map.

**Conclusion:** The read must join the authority or consume a validated immutable snapshot.

### Example 3

**Question:** Why must the invariant hold before a condition wait?

**Reasoning:** Waiting releases the mutex and transfers authority. Another participant may immediately acquire and rely on the predicate.

**Conclusion:** Repair the state, then atomically enroll and release through the condition protocol.

### Example 4

**Question:** A callback is invoked while the registry lock is held and calls `unsubscribe`.

**Reasoning:** Reentrancy may permit entry while iteration state is incomplete; a non-reentrant lock may self-deadlock.

**Conclusion:** Capture an immutable notification under lock and make an open call after release.

### Example 5

**Question:** An exception occurs after removing an entry but before decrementing its byte counter.

**Reasoning:** Releasing the lock exposes a broken conservation equation.

**Conclusion:** Precompute nonthrowing changes, roll back, or establish an explicit recoverable state before release.

### Example 6

**Question:** Does a robust mutex restore data after owner death?

**Reasoning:** POSIX can transfer ownership with `EOWNERDEAD`, but protected state may reflect an interrupted transition.

**Conclusion:** The new owner must validate and make state consistent or mark it unrecoverable.

### Example 7

**Question:** What does a strict nested-lock rank prove?

**Reasoning:** Increasing ranks exclude circular wait among compliant acquisitions.

**Conclusion:** It addresses deadlock; it does not prove each protected transition preserves its invariant.

### Example 8

**Question:** Can observers witness the inventory transition?

<!-- bijux-verify: {"id":"critical-section-observation-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unprotected_schedules=3\nunprotected_violations=1\nprotected_schedules=2\nprotected_violations=0\n","stderr":""}} -->
```python
unprotected = [
    ["observe", "decrement", "increment"],
    ["decrement", "observe", "increment"],
    ["decrement", "increment", "observe"],
]
protected = [
    ["observe", "decrement", "increment"],
    ["decrement", "increment", "observe"],
]

def violations(schedules):
    count = 0
    for schedule in schedules:
        available = 5
        reserved = 0
        for event in schedule:
            if event == "decrement":
                available -= 1
            elif event == "increment":
                reserved += 1
            elif available + reserved != 5:
                count += 1
    return count

print(f"unprotected_schedules={len(unprotected)}")
print(f"unprotected_violations={violations(unprotected)}")
print(f"protected_schedules={len(protected)}")
print(f"protected_violations={violations(protected)}")
```

**Conclusion:** The model shows one violating observer position and none when observation cannot enter the two-event region. It does not prove a real lock, memory model, inventory implementation, or exhaustive production schedule correct.

### Example 9

**Question:** A versioned reader copies fields, sees the same even version twice, then uses a mutable referenced object later.

**Reasoning:** Validation covered the copied references, not later pointee lifetime or mutation.

**Conclusion:** Copy immutable value data or retain safe ownership through use.

### Example 10

**Question:** Can this invariant method approve a concurrent radiation-treatment state machine?

**Reasoning:** Device modes, physical interlocks, timing, hazards, independent protection, regulatory evidence, and clinical operation exceed a software predicate.

**Conclusion:** No. Named authorized safety, clinical, and regulatory reviewers must approve the actual design. No external review or deployment fitness is claimed.

## Cross-Program Connections

- **Formal methods:** Hoare logic, Owicki-Gries interference freedom, rely/guarantee reasoning, and separation logic structure proofs.
- **Algorithms:** abstraction functions and representation invariants connect concurrent implementation to sequential specifications.
- **Operating systems:** mutex ownership, memory synchronization, priority protocols, and owner death define primitive behavior.
- **Databases:** transactions, isolation, constraints, and rollback provide broader serialization authorities.
- **Distributed systems:** one process lock cannot protect replicated authority; consensus or conditional storage may own the invariant.
- **Security:** authorization checks and state changes must share a serialization boundary to prevent stale authority.
- **Software architecture:** encapsulation, immutable snapshots, open calls, and ownership boundaries determine enforceability.

## References

1. Edsger W. Dijkstra, “Solution of a Problem in Concurrent Programming Control,” *Communications of the ACM* 8(9), 1965, [doi:10.1145/365559.365617](https://doi.org/10.1145/365559.365617).
2. Leslie Lamport, “A New Solution of Dijkstra's Concurrent Programming Problem,” *Communications of the ACM* 17(8), 1974, [doi:10.1145/361082.361093](https://doi.org/10.1145/361082.361093).
3. Susan Owicki and David Gries, “An Axiomatic Proof Technique for Parallel Programs I,” *Acta Informatica* 6, 1976, [doi:10.1007/BF00268134](https://doi.org/10.1007/BF00268134).
4. C. A. R. Hoare, “Monitors: An Operating System Structuring Concept,” *Communications of the ACM* 17(10), 1974, [doi:10.1145/355620.361161](https://doi.org/10.1145/355620.361161).
5. Cliff B. Jones, “Tentative Steps Toward a Development Method for Interfering Programs,” *ACM TOPLAS* 5(4), 1983, [doi:10.1145/69575.69577](https://doi.org/10.1145/69575.69577).
6. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.
7. Brian Goetz et al., *Java Concurrency in Practice*, Addison-Wesley, 2006.
8. Oracle, *Java Language Specification, Java SE 26*, Chapter 17, [official specification](https://docs.oracle.com/javase/specs/jls/se26/html/jls-17.html) (retrieved 2026-08-29).
9. IEEE and The Open Group, *POSIX.1-2024*, “pthread_mutex_lock,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html) (retrieved 2026-08-29).
10. Peter W. O'Hearn, “Resources, Concurrency, and Local Reasoning,” *Theoretical Computer Science* 375, 2007, [doi:10.1016/j.tcs.2006.12.035](https://doi.org/10.1016/j.tcs.2006.12.035).

## Exercises

### Exercise 1

Define an abstraction function and at least four representation invariants for a bounded circular queue with array, head, tail, and count. Derive the enqueue critical section.

### Exercise 2

A cache updates its entry map, LRU list, and byte counter under three locks. Explain why field ownership is insufficient and propose coarse and fine-grained proof strategies.

### Exercise 3

Design exception-safe reservation logic when audit-record allocation can fail. Compare strong and basic guarantees and place external publication.

### Exercise 4

A registry invokes listeners under a reentrant lock. Construct two failures and redesign it using open calls, versions, and immutable notifications.

### Exercise 5

An autonomous braking controller shares mode, sensor freshness, command, and fault state. State what internal invariant review can establish and which safety claims require named authorized human review.

## Answers to the Exercises

### Answer 1

Map the concrete ring to the sequence of `count` elements starting at `head` modulo capacity. Invariants include positive fixed capacity, indices within range, `0 <= count <= capacity`, `tail = (head + count) mod capacity`, and occupied-slot ownership matching the logical range. Under one authority, reject when full; write the value at `tail`; advance tail modulo capacity; increment count; and restore every relation before release. Publication must make both element and metadata visible. Returning a mutable slot reference would escape the abstraction.

### Answer 2

The abstract cache requires map membership, exactly one LRU node per entry, and counter equal to retained bytes. Separate field locks permit mixed states and ambiguous multi-lock order. A coarse proof uses one lock for the full predicate and performs eviction atomically. A fine-grained proof partitions entries while a coordinator owns global LRU and budget, defines strict acquisition order, and specifies rollback for cross-partition eviction. If no compositional invariant can be written, the split is unjustified.

### Answer 3

Allocate and validate the audit representation before acquiring the lock when it depends only on private data. Under lock, revalidate availability and atomically install reservation plus audit intent, restoring conservation. Release, then publish external audit effects through an idempotent outbox. For a strong guarantee, allocation or commit failure leaves abstract state unchanged. A basic guarantee may retain an explicit failed/pending reservation while preserving conservation and recoverability. Never emit an irreversible effect before an abortable state transition is durable.

### Answer 4

A listener can recursively unsubscribe while iteration metadata is inconsistent, or acquire another lock and create a cross-thread cycle. Under the registry lock, commit membership change, increment a version, and build immutable notification values. Release before callbacks. If callback results matter, reacquire and accept them only when their token/version remains valid, otherwise retry or reject under documented semantics. Define listener ordering, duplicate delivery, exception isolation, and cancellation.

### Answer 5

Internal review can define allowed software states, prove each serialized transition preserves relationships, test observation boundaries, and verify cleanup under modeled failures. It cannot establish sensor validity, braking-distance physics, actuator timing, hazard coverage, independence, fail-safe behavior, or regulatory compliance. Those claims and deployment decisions require named authorized automotive functional-safety, controls, hardware, validation, and regulatory reviewers under the applicable assurance process. This chapter provides no external review.
