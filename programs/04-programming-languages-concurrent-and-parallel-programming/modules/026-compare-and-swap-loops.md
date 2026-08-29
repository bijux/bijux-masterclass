---
module_id: CONPAR-026
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 26
title: Compare-and-Swap Loops
status: complete
last_verified: 2026-08-29
---

# Compare-and-Swap Loops

## One-Page Review

### Governing question

How can a compare-and-swap loop implement one conditional abstract transition despite interference, spurious failure, weak memory, representation reuse, and unbounded contention?

### Essential definitions

- **Compare-and-swap/exchange (CAS)** conditionally replaces an atomic value when its current representation equals an expected representation.
- An **attempt** is one CAS invocation; a **logical call** can contain many attempts.
- A **witness** is the value observed by a failed comparison, returned directly or written into the expected argument by the API.
- **Strong CAS** fails only when comparison fails; **weak CAS** may also fail spuriously and is intended for retry loops.
- **Recomputation** derives a new desired state from the latest witness after failure.
- The **linearization point** is the successful CAS that commits the abstract transition; a precondition failure may linearize at its decisive observation.
- **ABA** is a representation history A→B→A that makes equality conceal intervening change.
- **Reclamation** determines when removed storage can be reused or freed.
- **Lock-free** progress guarantees system-wide progress, not completion of every caller.
- **Backoff** delays retries to reduce destructive contention.

### Central model, mechanism, or theorem

For a pure transition function T and atomic state x, repeatedly observe e=x, reject if T(e) is undefined, compute d=T(e), and attempt CAS(x,e,d). A success commits exactly T(e) at that CAS. A failure commits nothing: refresh e from the witness, recheck the precondition, and recompute d. The proof requires one encoded state, correct success and failure orderings, representation/lifetime validity, and a progress policy.

### Critical invariants

Expected and desired refer to the same comparison domain. Desired is recomputed after every conflicting witness. Computation before success is replay-safe and has no irreversible external effect. Exactly one successful CAS owns each committed transition. Failure performs no release publication. A failed witness is given acquire semantics only when the retry or return consumes data published through that value. State encoding cannot silently wrap into a live generation. Pointer identity is protected independently from storage reclamation. Cancellation and retry bounds have defined outcomes. Multi-location invariants are not claimed from a single-location CAS.

### Common failures

Code retries the same stale desired value; charges or logs inside the loop; confuses a failed attempt with a failed logical call; assigns release ordering to the read-only failure path; assumes weak failure proves interference; uses representation equality as historical identity; adds a tag but ignores tag wrap and memory reuse; dereferences an unprotected pointer; calls lock-free wait-free or fair; spins without backoff; abandons a reserved transition on cancellation; or composes several CAS operations and calls the sequence transactional.

### Compact example

Four callers initially observe two permits. A succeeds changing 2→1. B, C, and D fail, receive witness 1, and recompute 1→0. B succeeds; C and D fail with witness 0 and reject. Seven attempts implement four logical calls: two committed reservations and two rejections, while the invariant `0 ≤ remaining ≤ 2` holds.

### Connections

[Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md) supplies the atomic transition model; [Visibility and Publication](024-visibility-and-publication.md) supplies ordering obligations. The [program roadmap](../ROADMAP.md) continues with acquire/release ordering and ABA.

## Governing Question

How should engineers derive a CAS retry loop from an abstract state machine, identify every possible linearization point, and decide when retry, ordering, lifetime, or contention complexity makes another synchronization mechanism preferable?

A CAS loop is best understood as an optimistic transaction over one encoded value. Its success is small and atomic; its surrounding proof is not.

## Why This Matters

CAS loops implement bounded counters, reference-state transitions, lock-free stacks and queues, immutable-root updates, lazy initialization, bit-packed state machines, and many standard-library atomics. They allow an arbitrary pure transformation where fetch-add or exchange would be too rigid.

The familiar loop can look self-evident: load, compute, compare, retry. Yet nearly every word hides a design decision. What does failure return? Must desired be recomputed? Can the computation run more than once? Which ordering applies to a successful read-write and which to a failed read? Does equality imply that the object is unchanged? What happens under sustained interference? Can cancellation occur after a logical commitment? Who reclaims a removed node?

These questions separate a correct single-word transition from a production protocol. CAS prevents a lost update only for the compared representation. It does not make external effects atomic, coordinate multiple objects, protect memory lifetime, ensure fairness, or prove that retries terminate.

## Prerequisites and Retrieval

Retrieve:

- atomicity violations from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- mutex and semaphore invariants from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) and [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- component lifecycle accounting from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md);
- modification order from [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md);
- happens-before and safe publication from [Happens-Before Relations](023-happens-before-relations.md) and [Visibility and Publication](024-visibility-and-publication.md); and
- atomic RMW semantics from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md).

Retrieval prompt: two callers observe `remaining=1` and both propose zero. Explain why only one CAS succeeds, what the loser learns, and why the loser must not retry `1→0` unchanged.

## Learning Objectives

After completing this module, a learner can:

1. derive a CAS loop from a partial abstract transition;
2. distinguish logical calls, CAS attempts, success, comparison failure, and spurious failure;
3. locate linearization points for success and precondition rejection;
4. prove safety by invariant preservation and witness refresh;
5. select strong or weak CAS and success/failure memory orderings;
6. keep replayable computation separate from external side effects;
7. diagnose ABA, tag wrap, and reclamation defects;
8. analyze lock-free progress, starvation, backoff, and bounded retry; and
9. choose a direct RMW, lock, semaphore, channel, or descriptor when CAS is a poor fit.

## Core Exposition

### Begin with a partial transition

Define abstract state `S` and a partial transition `T : S ⇀ S × R`. “Partial” means some observed states reject the operation. For permit reservation:

- if `remaining > 0`, transition to `remaining - 1` and return reserved;
- if `remaining = 0`, leave state unchanged and return unavailable.

The CAS loop refines this definition:

1. observe an expected value;
2. decide whether the operation is enabled;
3. compute the desired successor and return value;
4. compare the shared value with expected;
5. on success, return the committed result;
6. on failure, obtain the current witness and start the decision again.

This ordering matters. Failure means the premise used to derive desired may no longer hold. A correct loop revalidates the precondition and recomputes the transition.

### Attempts are not operations

A logical call is the client-visible operation. It can make zero attempts when an initial observation proves rejection, one attempt when uncontended, or many attempts under interference or spurious failure.

Let `A` be attempts, `C` successful commits, and `F` failed comparisons/spurious failures for an execution. Then `A = C + F` for attempted CAS actions. Logical calls `L` additionally include calls rejected before an attempt. Metrics and tests must not equate `F` with failed client requests.

This distinction also governs effects. The candidate computation may execute repeatedly. A successful CAS occurs at most once per well-formed call because the call returns after success. Only that success authorizes the abstract effect.

### API shapes and witnesses

CAS APIs expose related but different interfaces:

- C++ `compare_exchange_*` takes an expected object; on failure it replaces expected with the actual value.
- Rust `compare_exchange` and `compare_exchange_weak` return a result containing either the previous matching value or the current nonmatching value.
- Java `compareAndSet` returns a boolean, while compare-and-exchange forms return the witness value.
- Go `CompareAndSwap` returns a boolean, so a loop normally performs another load after failure.

Do not transliterate syntax without preserving semantics. Ask whether failure refreshes expected automatically, returns a witness, or requires an explicit load. The proof needs a fresh observation, not one particular API shape.

### Strong and weak comparison

Strong CAS fails when the current value does not compare equal to expected. Weak CAS may also fail spuriously. A spurious failure changes no shared state and does not prove another thread won.

Weak CAS is appropriate inside a loop that already refreshes/retries; on some architectures it maps naturally to load-exclusive/store-exclusive attempts. Strong CAS is useful for a one-shot conditional action where a spurious negative result would alter the API, or when the language/runtime recommends it.

Neither form eliminates interference. A strong CAS can repeatedly fail because other callers keep changing the state. A weak CAS must not be used as “try once means absent” unless the interface explicitly allows false negatives.

### Linearization

On success, the CAS modification is the natural linearization point. The loop's earlier loads and computation are speculative.

Rejection needs its own point. If a load observes `remaining=0` and zero is stable for the relevant instant, the load can linearize an unavailable result. If failure returns witness zero, that failed CAS observation can be the point. If the predicate depends on several locations, one CAS witness may not justify a coherent rejection.

Linearizability proof:

1. map each successful call to its successful CAS;
2. map each rejecting call to an atomic observation that proves the predicate false;
3. order calls by these points;
4. show each point applies the sequential specification to the state immediately before it; and
5. preserve real-time order for nonoverlapping calls.

The proof concerns observable history. It does not imply fairness or a bound on attempts.

### The loop invariant

For a capacity `K`, choose invariant `I(s) ≜ 0 ≤ s ≤ K`. Suppose observed `e` satisfies `I`.

- If `e=0`, rejection leaves `I` unchanged.
- If `e>0`, desired `d=e-1` satisfies `0≤d<K`.
- A successful CAS changes exactly `e→d`, preserving `I`.
- A failed CAS does not write `d`, so this caller does not violate `I`; it must check `I` for the new witness.

Induction over the modification order proves the bound if initialization satisfies it and every modifier follows a preserving transition. It does not prove that external permit ownership is returned on every exceptional path; that is a lifecycle invariant outside the atomic word.

### Pure recomputation and effect placement

Everything before success is speculative and replayable. It may validate input, inspect expected, allocate a private candidate, or compute desired. It must not send mail, charge money, acknowledge a message, publish a pointer elsewhere, free shared storage, or increment an authoritative separate counter.

After success, the logical state is committed. External work can still fail. Use a durable intent/outbox, an idempotency key, compensation, or a stronger transaction boundary when atomic memory and an external system must agree. CAS cannot roll back a remote side effect, and a process crash cannot be hidden by an in-memory retry loop.

Even a pure but expensive computation can be problematic: contention multiplies its cost. Cache derived immutable candidates carefully, or move to a lock that computes once when wasted work dominates.

### Success and failure ordering

A successful CAS both reads and writes the atomic location. Its ordering must cover each role required by the protocol. A release-capable success can publish preceding writes; an acquire-capable success can consume data associated with the value it replaced; acquire-release may be needed for both. Sequential consistency additionally joins the language's SC order.

A failed CAS performs a read and no desired write. Therefore its failure ordering cannot contain release semantics. Relaxed failure is enough when the witness is used only to derive the next numeric candidate. Acquire failure is needed when the failed witness itself identifies published data that the caller will read before retry or return.

Do not choose acquire merely because failure is possible. Draw the required synchronizes-with/read-from path. Also obey API restrictions: language interfaces constrain which failure orderings can accompany which success orderings.

Ordering does not repair an invalid algorithm. Sequential consistency cannot make stale desired computation correct, solve ABA, or join multiple atomics into a transaction.

### Reservation rather than decrement-and-rollback

For a hard bound, a CAS loop should test before modifying:

`remaining > 0 ? remaining - 1 : reject`.

This never installs a negative or overcommitted state. By contrast, unconditional fetch-sub followed by rollback may temporarily violate the bound, expose invalid state to observers, and leak capacity if interruption occurs before compensation.

Once reservation succeeds, the caller owns one permit. Its later failure must return that permit exactly once through a separate defined transition. CAS protects acquisition, not the full resource lifecycle.

### ABA: equality is not history

Suppose a stack head is address A. One thread pauses after reading A. Another removes A, removes B, and later installs A again. The paused thread's CAS sees A and succeeds, although the structure passed through a different history and A's links or identity may have changed.

CAS compares the current representation, not a versioned history. A tag pairs the value with a generation so A:7 differs from A:9. Tags reduce ABA only if the pair changes on every relevant transition, the comparison is atomic, and the tag cannot wrap while stale observations remain live.

Logical ABA can also affect integer state machines. If state `READY` cycles through `RUNNING` back to `READY`, a stale transition may require an epoch even without pointers.

### Reclamation is separate

Tags do not make memory safe. Before dereferencing an observed node, a caller must establish that it cannot be reclaimed and reused. Hazard pointers publish protected addresses and require validation; epoch-based reclamation delays reuse until earlier readers quiesce; reference counting requires safe acquisition; garbage collection supplies a different lifetime mechanism.

Each technique has assumptions and costs. Use mature libraries for nontrivial lock-free structures. A pointer CAS proof without a reclamation proof is incomplete even when tests never reuse addresses.

### Contention, progress, and backoff

CAS concentrates modifications on a cache line. Under contention, many agents read the same value, one succeeds, and the rest invalidate work and retry. Coherence traffic, scheduler preemption, and NUMA placement can dominate instruction cost.

A lock-free algorithm guarantees that some operation completes in a finite number of its system steps under its model. It can starve one caller indefinitely. Wait-free gives a per-operation bound; obstruction-free assumes eventual solo execution. Hardware support, runtime fallback, and reclamation can change the end-to-end guarantee.

Backoff can pause, yield, randomize, or eventually park. It reduces simultaneous retries but adds latency and policy. Use measured contention, cancellation-aware waiting, and a lost-wakeup-safe notification design. A mutex may provide better throughput, energy use, observability, and fairness when the critical section is not tiny.

### Cancellation and bounded retry

Checking cancellation before an attempt is safe if no commitment occurred. Checking immediately after success cannot report “cancelled without effect”: the transition already happened. The API must either return success, compensate according to an owned protocol, or expose an outcome that says commitment may have occurred.

A retry limit changes semantics. “Give up after ten failures” is not the same as unavailable; it means contention or spurious failure prevented commitment. Return a distinct retryable outcome and never infer the abstract predicate was false.

Deadlines use the same rule. At the boundary, identify whether a successful CAS occurred. Ambiguous external effects require idempotent request identity or durable outcome lookup.

### Multiword state

One CAS can preserve a compound invariant only if all relevant fields fit in the compared representation or are referenced by one immutable root whose lifetime is protected. Packing adds bit-width, overflow, portability, and maintainability costs.

Two CAS operations on separate locations expose an intermediate state. Helping descriptors and multiword algorithms can make more elaborate transitions linearizable, but their proof and reclamation burden is substantial. For ordinary application invariants, one mutex around a clear state object is often the rigorous choice.

### Verification strategy

Unit tests cover zero, one, maximum, rejection, witness refresh, spurious-failure injection, cancellation before success, cancellation after success, and updater replay. Deterministic schedulers/model checkers enumerate small interleavings. Stress tests measure retry distributions and starvation symptoms. Sanitizers find surrounding data races; target tools inspect atomic width and mappings.

ABA tests must force remove/reuse histories, not merely repeat values accidentally. Reclamation tests delay readers across retire/reuse boundaries. Fault injection stops execution after successful commitment but before external follow-up.

Finite testing does not prove linearizability, lock-free progress for every environment, absence of tag wrap, or safety for an unmodeled allocator. State assumptions and supplement tests with invariant and history review.

## Definitions and Notation

Let `x` be one atomic representation and `T(e)` a partial transition producing desired `d` and result `r`. Write:

- `CAS(x,e,d)=success` when `x=e` and the atomic action installs `d`;
- `CAS(x,e,d)=failure(w)` when it installs nothing and observes witness `w`;
- `L` for logical calls, `A` attempts, `C` commits, and `F` failed attempts;
- `mo_x` for the modification order of `x`; and
- `I(s)` for the representation invariant.

For attempted actions, `A=C+F`. There is no equation `L=A` because one call may retry and a rejecting call may make no CAS attempt.

ABA is a trace `x=A; x=B; x=A` during one stale observation interval. A tagged representation is `(value,generation)`. A finite generation field still wraps; safety needs a bound connecting wrap time to maximum stale-observation lifetime.

“Proof” below means an argument under stated source-model and state assumptions. Performance claims are empirical and target-specific.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Specify the abstract operation.** Define enabled states, successor, result, and rejection.
2. **Choose the representation.** Include every field needed for one atomic invariant.
3. **State `I`.** Prove initialization and every successful transition preserve it.
4. **Define the observation path.** Load, failure witness, and refresh semantics are explicit.
5. **Require pure recomputation.** Desired is a function of the latest expected value.
6. **Assign linearization points.** Cover success, rejection, timeout, and cancellation.
7. **Derive ordering.** Separate successful read/write roles from read-only failure.
8. **Prove identity and lifetime.** Address ABA, generation wrap, dereference, retirement, and reuse.
9. **State progress assumptions.** Scheduler, contention, spurious failure, backoff, and target support.
10. **Place external effects.** Commitment, follow-up, crash recovery, and idempotency are distinguished.
11. **Test adversarial traces.** Force conflicts, reuse, interruption, boundary values, and starvation pressure.
12. **Choose the simpler primitive when the proof does not fit.**

The executable model fixes a deterministic interleaving of four logical reservation calls. It models comparison failure and witness refresh, not real threads.

<!-- bijux-verify: {"id":"cas-permit-retry-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical_calls=4\ninitial_permits=2\ncas_attempts=7\ncas_successes=2\ncas_failures=5\nrecomputations=3\nrejected_at_zero=2\nremaining=0\nunique_reservations=2\n","stderr":""}} -->
```python
remaining = 2
initial_permits = remaining
expected = [remaining, remaining, remaining, remaining]
active = [True, True, True, True]
schedule = [0, 1, 2, 3, 1, 2, 3]
attempts = 0
successes = 0
failures = 0
recomputations = 0
rejected = 0
reservations = []

for caller in schedule:
    if not active[caller]:
        continue
    attempts += 1
    observed = expected[caller]
    desired = observed - 1
    if remaining == observed:
        remaining = desired
        successes += 1
        reservations.append(caller)
        active[caller] = False
    else:
        failures += 1
        expected[caller] = remaining
        if remaining == 0:
            rejected += 1
            active[caller] = False
        else:
            recomputations += 1

print(f"logical_calls={len(active)}")
print(f"initial_permits={initial_permits}")
print(f"cas_attempts={attempts}")
print(f"cas_successes={successes}")
print(f"cas_failures={failures}")
print(f"recomputations={recomputations}")
print(f"rejected_at_zero={rejected}")
print(f"remaining={remaining}")
print(f"unique_reservations={len(set(reservations))}")
```

Limitations: the model stipulates atomic comparison and a strong-CAS schedule. It does not execute concurrent threads, weak spurious failures, a language memory model, cache coherence, backoff, cancellation, ABA, pointer lifetime, target lock-freedom, or external effects.

## Alternatives and Trade-Offs

**Direct fetch operations** are clearer for unconditional arithmetic or bit changes. Avoid a retry loop when the abstract transition already matches a standard RMW.

**Mutexes** serialize arbitrary multi-field state, allow one-time computation, support conditions, and often behave better under contention. They add blocking, ownership, and failure-policy considerations.

**Semaphores** directly represent conserved capacity plus waiting. They are preferable to a bare CAS counter when callers need blocking, wakeup, cancellation, and shutdown semantics.

**Channels or actors** transfer ownership and serialize state transitions at an owner. They add queueing and scheduling but reduce shared-memory proof surface.

**Immutable-root CAS** computes a new immutable structure and swaps one root. Readers get coherent snapshots, while allocation, retry waste, and reclamation remain.

**Packed state** can atomically update several bounded fields. It trades a local linearization point for encoding limits, wrap, portability, and difficult evolution.

**Descriptors/helping** can implement multiword nonblocking protocols. Use them only when their progress and reclamation proofs are justified by requirements.

**Transactional systems** coordinate durable/external state. An in-memory CAS cannot substitute for database atomicity, idempotency, or recovery.

## Failure Modes and Misconceptions

1. **Retrying the same desired value is safe.** A new witness requires a new transition calculation.
2. **A CAS failure means the operation failed.** It usually means only one attempt failed.
3. **Weak failure proves interference.** It may be spurious.
4. **Strong CAS guarantees progress.** Other agents can cause unlimited comparison failures.
5. **The updater executes once.** Speculative computation can replay.
6. **A side effect before CAS is rolled back on failure.** CAS controls only the atomic representation.
7. **Release is useful on failure.** Failure is read-only and cannot publish.
8. **Acquire is always required on failure.** It follows only from consuming published data.
9. **SC fixes an incorrect retry loop.** Ordering cannot repair stale computation or missing state.
10. **CAS equality proves no change happened.** ABA hides intervening histories.
11. **A version tag solves ABA permanently.** Tags wrap and do not reclaim storage.
12. **A protected integer makes pointer dereference safe.** Lifetime needs its own protocol.
13. **Lock-free means every caller completes.** Individual starvation remains possible.
14. **Backoff is only a performance tweak.** Its cancellation, latency, and parking behavior is policy.
15. **A retry limit proves unavailable.** It proves only that commitment was not observed within the policy.
16. **Two CAS operations form a transaction.** Other agents observe the intermediate state.
17. **Success before timeout can be reported as cancellation.** Commitment already occurred.
18. **Passing stress tests proves correctness.** Rare ABA, wrap, and progress traces require explicit reasoning.

## Worked Examples

### Example 1

**Situation.** Two callers observe one remaining permit and propose zero.

**Reasoning.** The first successful CAS linearizes `1→0`. The other CAS compares expected one with current zero and fails, then treats the witness zero as rejection.

**Conclusion.** Exactly one success owns the permit; failed comparison is not rollback.

### Example 2

**Situation.** A balance updater reads 10, proposes 15, loses to a change to 12, and retries `10→15`.

**Reasoning.** Installing 15 would discard the concurrent addition. Refresh to 12 and recompute `12→17`.

**Conclusion.** Desired must be derived from the latest witness.

### Example 3

**Situation.** Weak CAS fails while the shared value still equals expected.

**Reasoning.** This is permitted spurious failure. The loop may retry; a one-shot “not acquired” response would be a false negative unless its contract allows it.

**Conclusion.** Match weak CAS to retryable semantics.

### Example 4

**Situation.** A replayable updater sends an invoice before attempting CAS.

**Reasoning.** Three conflicts can send four invoices before one state transition commits. Move invoicing after commitment and use a durable idempotency key/outbox.

**Conclusion.** Speculative computation is pure; irreversible effects require another protocol.

### Example 5

**Situation.** A failed CAS returns a pointer to an immutable configuration, and the caller reads that configuration before retry.

**Reasoning.** If the pointer publishes initialized data, the failure observation needs the acquire semantics required by that publication path. Relaxed failure is enough only if the witness is used as an opaque comparison candidate.

**Conclusion.** Failure ordering is derived from witness use, not from failure itself.

### Example 6

**Situation.** Stack head changes A→B→A while a thread pauses with expected A.

**Reasoning.** Its CAS can succeed despite intervening removals. A generation distinguishes histories, while hazard/epoch/reference protection separately prevents A from being freed and reused.

**Conclusion.** Solve logical ABA and reclamation as distinct obligations.

### Example 7

**Situation.** A service aborts after ten CAS failures and reports “capacity exhausted.”

**Reasoning.** Every failure may be interference while capacity remained positive. The outcome is contention/retry-budget exhaustion, not a predicate observation.

**Conclusion.** Retry policy needs a distinct client-visible result.

### Example 8

**Situation.** Hundreds of threads update one immutable registry root with expensive copying.

**Reasoning.** Losers discard candidate copies, increasing allocation and tail latency. A mutex computes once per serialized update and may outperform the nonblocking design.

**Conclusion.** Evaluate wasted speculative work and contention, not atomic instruction count.

### Example 9

**Situation.** A state change needs both `available--` and `leased++` in separate atomics.

**Reasoning.** Two CAS operations expose a state between them and interruption can make it permanent. Pack the bounded pair, use one immutable root, or protect both with a mutex.

**Conclusion.** Single-location CAS does not compose automatically.

### Example 10

**Situation.** An infusion controller uses CAS to reserve a dosing command and claims the device cannot double-dose.

**Reasoning.** CAS can prove one software transition for one encoded state. It does not prove durable command identity, restart recovery, actuator acknowledgement, timing, sensor validity, authorization, electromagnetic behavior, or hazard mitigation.

**Conclusion.** Named clinical, controls, hardware, real-time, security, quality, and functional-safety reviewers need target evidence; this chapter makes no deployment claim.

## Cross-Program Connections

- **Programming languages:** API witness shapes, ordering constraints, representation comparison, and progress guarantees differ.
- **Algorithms:** linearizability and lock-free structures use CAS as one proof mechanism.
- **Computer architecture:** exclusive operations, cache coherence, NUMA, and spurious failure shape behavior.
- **Operating systems:** parking, wakeups, scheduling, and preemption determine contention policy.
- **Data systems:** optimistic concurrency control similarly validates a version before commitment, but durable transactions add recovery.
- **Security:** ABA, use-after-free, wrap, authorization, and ambiguous completion can become vulnerabilities.
- **Software engineering:** idempotency, outboxes, explicit outcomes, metrics, and simpler ownership boundaries make protocols operable.
- **Performance engineering:** retry distributions and tail latency matter more than uncontended microbenchmarks.

## References

1. Maurice Herlihy. “Wait-Free Synchronization.” *ACM Transactions on Programming Languages and Systems* 13(1), 1991.
2. Maurice Herlihy and Nir Shavit. *The Art of Multiprocessor Programming*, revised first edition. Morgan Kaufmann, 2012.
3. R. Kent Treiber. “Systems Programming: Coping with Parallelism.” IBM Research Report RJ 5118, 1986.
4. Maged M. Michael. “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects.” *IEEE Transactions on Parallel and Distributed Systems* 15(6), 2004.
5. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
6. ISO C++ working draft. “Atomic types and `compare_exchange` operations.” Current draft accessed 2026-08-29.
7. Oracle. “`AtomicReference` and `VarHandle`, Java SE 26 API.” 2026. Accessed 2026-08-29.
8. Rust Project. “`std::sync::atomic`, Rust 1.98.0.” 2026. Accessed 2026-08-29.
9. The Go Authors. “Package `sync/atomic` and The Go Memory Model.” Accessed 2026-08-29.
10. Paul E. McKenney. *Is Parallel Programming Hard, And, If So, What Can You Do About It?* 2023 edition.

## Exercises

### Exercise 1

Define a CAS loop's logical call, attempt, witness, successful linearization point, and rejection linearization point.

### Exercise 2

Trace callers A, B, and C reserving from `remaining=2` when all first observe two. A attempts first, then B, then C; retry in alphabetical order. Count attempts, failures, recomputations, successes, and rejections.

### Exercise 3

Diagnose a weak-CAS loop that computes desired once, logs inside the loop, uses release ordering on failure, and reports unavailable after eight failures. Repair each defect.

### Exercise 4

Compare a CAS counter, semaphore, mutex-protected state, and immutable-root CAS for a bounded job service with cancellation, payload publication, and three related counters. Select a design and justify progress and failure semantics.

### Exercise 5

A lock-free medical telemetry list uses pointer CAS plus a 16-bit tag. State the safety proof, ABA/wrap and reclamation evidence, ordering/progress tests, external-effect boundary, and required human review before deployment.

## Answers to the Exercises

### Answer 1

The logical call is one client-visible invocation; it may contain many attempts. An attempt invokes CAS with expected and desired. On failure, the witness is the current value observed by the comparison, returned directly, written into expected, or obtained by a new load according to the API.

Success linearizes at the atomic CAS that installs desired. Rejection linearizes at an atomic observation that proves the abstract predicate false, such as loading zero or receiving witness zero. A retry-budget outcome is not predicate rejection unless such an observation occurred.

### Answer 2

Initial expected values are all two. A succeeds `2→1`: one attempt, one success. B attempts `2→1`, fails with witness one, and recomputes `1→0`. C does the same. On retry, B succeeds `1→0`. C retries expected one, fails with witness zero, and rejects.

Totals are six attempts: two successes and four failures. There are two recomputations from witness one (B and C), one rejection at zero, and remaining is zero. C does not compute `0→-1`. The two successful CAS actions uniquely own the permits.

### Answer 3

Desired computed once becomes stale after interference and can overwrite a newer transition; recompute it from every fresh witness. Logging can repeat on conflict or spurious failure; record the logical result after success, using idempotency/durability if the log is authoritative.

Failure is read-only, so release ordering is invalid/useless there. Choose relaxed when the witness is only numeric, or acquire when it publishes data that is consumed. Eight failed attempts prove retry-budget exhaustion, not unavailability; return a distinct contention/retryable outcome. Weak CAS is acceptable once the loop treats spurious and comparison failures as noncommitting retries and rechecks cancellation safely.

### Answer 4

A bare CAS counter can preserve `0≤remaining≤K` but does not by itself wait, wake, publish payload, return permits on every failure path, or atomically maintain three counters. An immutable-root CAS can update all fields coherently, but copying and discarded candidates may be expensive and reclamation must be solved.

For an ordinary bounded service, use a semaphore or one mutex/condition around capacity, lifecycle, and related authoritative counters, plus a bounded queue whose enqueue/dequeue publishes payload. Define cancellation before admission, ownership after admission, shutdown wakeups, and exact permit return. A semaphore is strongest when capacity is the dominant invariant; the mutex is clearest when the three counters and job lifecycle must change together. Keep approximate metrics separate. Choose CAS only after measured nonblocking requirements justify its larger proof.

### Answer 5

For the encoded head, prove initialization, legal next pointers/tags, one successful CAS per abstract insertion/removal, rejection points, and linearizable histories. Bound the 16-bit tag: show it cannot wrap while any stale observation can remain, or enlarge/change the protocol. The tag alone does not prevent reuse.

Protect every observed node before dereference using a validated hazard-pointer, epoch, reference-count, garbage-collected, or equivalent scheme. Prove retirement and delayed reuse, publication of initialized node fields, and success/failure orderings. Force A→B→A and tag-wrap-adjacent traces; delay readers across retirement; inspect target atomic-width/lock-free support; stress contention, starvation, backoff, cancellation, and shutdown.

Keep network alerts, durable acknowledgements, and device actions outside speculative retries, with idempotent identity and recoverable outcome records. Named concurrency, language/runtime, memory-reclamation, clinical/domain, cybersecurity, real-time, hardware, quality, regulatory, and functional-safety reviewers must examine target traces and hazards. This model answer supplies no medical or deployment approval.
