---
module_id: CONPAR-025
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 25
title: Atomic Read-Modify-Write Operations
status: complete
last_verified: 2026-08-29
---

# Atomic Read-Modify-Write Operations

## One-Page Review

### Governing question

When does one indivisible read-modify-write action correctly arbitrate a shared state transition, and which larger correctness obligations remain outside that action?

### Essential definitions

- An **atomic read-modify-write (RMW)** reads a location and conditionally or unconditionally writes its successor as one atomic action.
- **fetch-add/sub** applies arithmetic and returns either the old or new value according to the API.
- **exchange** unconditionally installs a value and returns the previous value.
- **test-and-set** writes a set state and reports the prior state.
- **compare-and-swap/exchange (CAS)** installs a desired value only if the current value matches an expected value.
- The **linearization point** is the successful atomic transition in the object's abstract history.
- **modification order** orders atomic modifications of one location.
- **contention** occurs when agents compete for the same location/cache line.
- **overflow/wraparound** is the type/API-specific result beyond the numeric range.
- A **compound invariant** relates multiple locations or steps and is not automatically protected by one RMW.

### Central model, mechanism, or theorem

For atomic x and RMW operation f, each successful action observes some old value v in x's modification order, returns the API-defined result, and installs f(v) without another modification interleaving between its read and write. Six fetch-add(1) operations starting at zero therefore receive distinct old values 0 through 5 in some caller order and leave x=6. Six separate atomic loads of zero followed by six stores of one can legally leave x=1.

### Critical invariants

The location, width, alignment, type, and lifetime support atomic access. All conflicting access follows the source model; atomic and unsynchronized non-atomic access is not mixed. The returned-value convention is explicit. Overflow is defined and handled. One successful RMW corresponds to one abstract transition. Ordering is derived from publication needs, not from atomicity alone. Retried update functions are side-effect-free. A counter is not treated as a snapshot of other state. Contention, fairness, and progress are measured separately. Reference RMW includes generation and reclamation protection where needed.

### Common failures

Teams replace an atomic increment with atomic load plus store; confuse get-and-increment with increment-and-get; ignore signed/unsigned overflow; use a ticket after wrap without generation; publish payload through a relaxed counter; call I/O from an update function that may retry; assume lock-free means wait-free; build a spin lock from test-and-set without backoff or ownership; update two atomics and call the pair transactional; use approximate counters for final reconciliation; or swap pointers without protecting lifetime.

### Compact example

An atomic fetch-add returns 41 and installs 42. The caller owns ticket 41. Another caller must observe a later modification-order value and cannot receive 41 from the same nonwrapping epoch. This proves unique allocation for that epoch, not that ticket service is fair, tickets cannot wrap, or downstream work completes.

### Connections

[Visibility and Publication](024-visibility-and-publication.md) distinguishes atomic state from payload publication; [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md) shows why separate load/store is not compound atomicity. The [program roadmap](../ROADMAP.md) next develops compare-and-swap loops and acquire/release ordering.

## Governing Question

How should engineers derive an RMW operation from an abstract state transition, choose its returned value and memory ordering, and prove that overflow, contention, retries, multi-location state, and lifetime do not invalidate the larger protocol?

An RMW is a powerful linearization mechanism for one location. Its proof begins—not ends—at indivisibility.

## Why This Matters

Counters, sequence generators, reference counts, bit flags, state machines, work indices, ownership markers, and lock-free structures rely on RMW. Replacing a load-compute-store sequence with one RMW prevents lost updates on that location and creates a natural linearization point.

The apparent simplicity can obscure system defects. A unique sequence number can wrap. A reference count can reach zero while a new acquirer races through an unprotected pointer. An atomic “completed” count can advance before result publication. A test-and-set lock can be correct under light load yet collapse cache traffic and starve waiters.

The right question is which abstract transition the operation owns. Numeric atomicity is enough for advisory metrics; publication needs ordering; resource reservation needs bounds and rollback; lifetime needs reclamation; multi-field invariants often need a lock, descriptor, or combined representation.

## Prerequisites and Retrieval

Retrieve:

- atomicity violations from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- lock and semaphore conservation from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) and [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- bounded component accounting from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md);
- modification order and SC from [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md);
- hb and publication from [Happens-Before Relations](023-happens-before-relations.md) and [Visibility and Publication](024-visibility-and-publication.md).

Retrieval prompt: trace two threads that load atomic x=0, each computes 1, and each stores 1. Then replace both pairs with fetch-add(1), naming returned and final values.

## Learning Objectives

After completing this module, a learner can:

1. distinguish atomic load/store from atomic RMW;
2. specify fetch-add, exchange, test-and-set, and CAS semantics;
3. identify an RMW linearization point and modification-order argument;
4. select old-versus-new returned-value conventions correctly;
5. prove unique ticket allocation within a nonwrapping epoch;
6. handle integer overflow, ABA-like reuse, and reference lifetime;
7. separate atomicity from acquire/release/SC ordering;
8. analyze contention, false sharing, progress, and fairness; and
9. identify when a lock or combined state representation is safer.

## Core Exposition

### Separate atomic access from atomic transformation

An atomic load is one indivisible observation. An atomic store is one indivisible modification. A load followed by local computation and store is two memory actions; another thread can modify the location between them. Making each action sequentially consistent still permits that interleaving.

An RMW joins the read and write of one location into one atomic action. It observes the immediately preceding value in that location's modification order and installs its successor without an intervening modification. This supplies a per-location serialization point.

The computation may be built into hardware, synthesized with an exclusive-load/store pair, or implemented by a runtime lock. Source semantics matter; “atomic” does not necessarily mean one machine instruction or lock-free.

### Fetch arithmetic

Fetch-add(delta) atomically installs old+delta and usually returns old. APIs may also provide add-and-get, which returns new. Get this boundary right:

- old value is useful for zero-based tickets and array indices;
- new value is useful for post-update counts;
- final value alone does not identify which caller received which ticket.

For n successful increments starting from b without wrap, modification order gives old values b through b+n-1 exactly once and final b+n. Caller-to-ticket order depends on which RMW linearizes first, not thread creation or arrival timestamps.

Fetch-sub supports decrementing counts, but zero-crossing protocols require care. Two callers cannot both observe old=1 on the same atomic modification order; the one observing 1 may own transition to zero. It still needs a lifetime proof before destroying a resource.

### Exchange and test-and-set

Exchange installs new unconditionally and returns old. It can hand off pointers, detach a list, reset a batch counter, or replace state while allowing the caller to process the previous value. Any pointer exchange needs publication and reclamation.

Test-and-set is exchange with a boolean/set bit. A simple spin lock repeatedly sets true until it observes false. Correct use also needs acquire on successful entry, release on unlock, ownership rules, bounded critical sections, pause/backoff/parking, and failure policy.

Aggressive test-and-set writes on every failed attempt, causing cache-line invalidation. Test-test-and-set first reads while locked, then attempts RMW when availability appears; it reduces writes but does not guarantee fairness.

### Compare-and-swap

CAS conditionally changes expected to desired. Success is an RMW and natural linearization point; failure observes a current value but performs no desired modification. Strong and weak forms, expected-argument mutation, and success/failure ordering vary by API.

CAS enables arbitrary state transformations in retry loops, which the next module treats. The update computation can run multiple times. It must not perform unrecoverable external side effects before success.

CAS compares a representation. If a pointer/value changes A->B->A, a stale CAS can succeed despite an intervening history: the ABA problem. Stamps, generations, nonreuse, and reclamation address different parts of it.

### Modification order and linearization

Each atomic object has an ordered history of modifications under the language model. A successful RMW reads the value preceding its modification as specified. Map that point to one abstract operation.

For a ticket dispenser:

abstract state next=N
`fetch_add(1)` returning N linearizes allocate(N), then abstract state is N+1.

This proof needs a domain bound. If arithmetic wraps from maximum to zero while old tickets remain live, uniqueness across the system fails even though every RMW is atomic.

The proof also identifies operation ownership: the caller receiving N owns only that allocation result. It does not inherit fairness, queue position, completion, cancellation, or downstream capacity merely from the ticket's numeric order.

### Overflow and numeric domains

Overflow semantics differ. Rust unsigned atomic fetch-add wraps; signed behavior and other languages must be checked. Java integer atomic arithmetic uses fixed-width two's-complement behavior. A C++ atomic integer operation has its specified arithmetic rules. Never extrapolate from debug builds or ordinary arithmetic.

Choose:

- a domain large enough with a proved lifetime/throughput horizon;
- checked reservation via CAS;
- saturating behavior;
- generation plus counter;
- explicit exhaustion failure; or
- a durable identity service.

For capacity, `fetch_add` followed by “if old>=limit, fetch_sub” temporarily exceeds the bound and rollback can interact badly with observers. CAS-reserve only when below limit, or use a semaphore/lock whose invariant directly enforces capacity.

### Memory ordering has two sides

Atomicity says the RMW is indivisible for its location. Ordering says how it relates to other memory. A relaxed fetch-add is appropriate for a standalone advisory count that publishes no payload. It is not a general publication event.

An acquire/release RMW can both observe prior published state and publish preceding local writes, subject to the exact reads-from/release-sequence rules. Some APIs note that using acquire on an RMW leaves its store side relaxed, while release leaves its load side relaxed; acq_rel covers both roles.

Sequential consistency adds the RMW to the language-defined SC order. It can simplify multiple-atomic reasoning, but it does not make non-atomic races safe or combine several atomics into a transaction.

Derive ordering from a path:

payload write -> release-capable RMW -> matching acquire observation -> payload read.

If the counter publishes nothing, do not add ordering by habit.

### Update functions and replay

High-level APIs such as Java `getAndUpdate` may internally retry a CAS when contention wins. The supplied function can be applied more than once. It must be side-effect-free: compute only the desired value from the old input.

Do not log, charge a card, enqueue work, increment another independent counter, allocate an externally visible ID, or free a resource inside a replayable updater. Perform external effects after successful atomic commitment, with idempotency/failure handling if the later effect can fail.

Even allocation inside a retry can cause pressure; ensure abandoned temporary values are cleaned by the language/runtime.

### Multi-location invariants

Two atomic counters can each be correct while their pair is impossible as one logical snapshot. Suppose accepted increments before queued, and worker decrements queued before incrementing active. An observer can sample values between transitions.

Options include:

- one lock protecting the full invariant;
- pack fields into one atomic word and update together;
- immutable descriptor/root replacement;
- sequence/version validation around reads;
- tolerate and document approximate observations; or
- reconcile at quiescence from authoritative identities.

Do not use a chain of RMW operations and call it atomic. A crash, cancellation, or preemption can occur between them.

### Reference counting

Increment/decrement are atomic numeric transitions, but acquiring a reference requires a live reference-counted handle. Reading a raw pointer, then incrementing its count can race with a final decrement and deallocation.

The decrement that observes old=1 may own destruction only after ordering guarantees make prior object uses visible and the counting model proves no new references can appear. Weak references, cycles, resurrection, and custom deleters add state.

Use established reference-counted types rather than inventing a counter. Their correctness spans pointer publication, atomic order, layout, overflow, weak/strong counts, and reclamation.

### Bitsets and state machines

Fetch-or can claim independent flags; fetch-and can clear them; fetch-xor toggles. Returned old bits show which transitions this caller caused. If several bits form one invariant, a single word RMW can update them consistently.

Encoding has limits: state explosion, wrap, reserved bits, portability, and readability. Make illegal combinations unrepresentable or validate every transition. A bit becoming set does not prove its associated payload was published unless ordering does.

Exchange and CAS can implement state transitions such as IDLE->RUNNING. Reject transitions from unexpected states and define terminal monotonicity. Numeric success is not authorization: caller identity/ownership must permit the transition.

### Contention and scalability

All writers to one atomic location contend for its cache line and modification order. Throughput may flatten as cores increase. A globally unique counter can become a serialization bottleneck even when each operation is lock-free.

Use sharded counters for approximate sums, per-thread ranges for IDs, batching, combining, distributed allocation, or a lock with parking when contention is high. Sharding trades instantaneous exactness for scalability and reconciliation complexity.

False sharing occurs when unrelated hot atomics occupy one cache line. Padding/alignment may help, but architecture-specific layout and memory cost require measurement.

### Progress and fairness

Lock-free means system-wide progress under a formal definition, not that each caller completes quickly. One thread can repeatedly lose RMW contention. A hardware atomic can be unavailable for a width and implemented with locks. Compare runtime/target guarantees.

Ticket values can impose service order only if the waiting protocol honors them and cancellation does not leave holes. Fetch-add itself does not wake waiters or guarantee scheduler fairness.

Backoff reduces contention but adds latency and tuning. Parking saves CPU but needs a lost-wakeup-safe predicate and wake protocol.

### Observability and reconciliation

Metrics counters may use relaxed RMW when they publish no state. Label them approximate: a snapshot across counters may not correspond to one instant, and increments can race with scrape.

Authoritative accounting uses identities and lifecycle states. At shutdown, after no new transitions and all workers join, reconcile accepted identities and terminal outcomes. Atomic totals can cross-check but must not hide missing obligations.

Instrument attempts, successes, failures, retries, contention latency, overflow proximity, wrap epoch, and hot-line behavior. Sampling must not introduce the synchronization being investigated.

### Verification

Test zero, one, maximum-minus-one, maximum, wrap, negative delta where allowed, old/new return conventions, concurrent uniqueness, CAS failure, updater replay, capacity rollback, final reference decrement, ABA reuse, mixed atomic/non-atomic misuse, and unsupported widths/targets.

Use model checking for state transitions, sanitizers/race tools for surrounding data/lifetime, stress across core counts, optimized assembly for mappings, and performance counters for cache traffic. Fault injection covers interruption between multi-location updates and after atomic commit before external effects.

Finite tests do not prove universal lock-free progress, fairness, or absence of wrap.

## Definitions and Notation

Let atomic location x have modification order (mo_x). An RMW R observes old value v and installs f(v) as one modification; API result is old or f(v). For fetch-add delta:

(x' = x + delta mod 2^w)

when the specified unsigned width-w arithmetic wraps. Do not apply this formula to a language/type without checking its rules.

Linearization map L assigns each successful RMW to its atomic modification. Attempts (A), successes (S), retries (Q), and failures (F) satisfy A=S+F for one-shot conditional operations; retry-loop accounting additionally records repeated internal attempts per logical call.

Contention factor can be described by successful RMW throughput and retry/latency distributions, not just mean operation time.

## Mechanisms, Invariants, or Proof Structure

Use this derivation:

1. **Name abstract state and transition.** Define legal old and new values.
2. **Choose the RMW.** Fetch arithmetic, exchange, bit operation, or CAS.
3. **Fix return semantics.** Old/new value, success flag, and expected-value update.
4. **Prove modification-order uniqueness.** Map success to one linearization point.
5. **Bound the domain.** Overflow, wrap, exhaustion, and generation are explicit.
6. **Derive memory ordering.** State which payload, if any, crosses the operation.
7. **Protect replay and effects.** Updater computation is pure; effects follow commitment.
8. **Handle lifetime.** Pointer/reference transitions include reclamation.
9. **Evaluate progress.** Target support, contention, fairness, backoff, and parking.
10. **Reconcile broader state.** Multi-location invariants and terminal outcomes use a suitable protocol.

The executable model contrasts six atomic fetch-add operations with six split loads/stores and shows unsigned 8-bit wrap.

<!-- bijux-verify: {"id":"rmw-ticket-and-lost-update-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rmw_operations=6\nreturned_old_values=[0, 1, 2, 3, 4, 5]\nunique_tickets=6\nrmw_final=6\nsplit_load_store_final=1\nlost_updates=5\nu8_wrapped_final=3\n","stderr":""}} -->
```python
operations = 6
rmw_value = 0
tickets = []
for operation in range(operations):
    old = rmw_value
    rmw_value = old + 1
    tickets.append(old)

unique_tickets = 0
for ticket in tickets:
    if tickets.count(ticket) == 1:
        unique_tickets += 1

split_reads = [0] * operations
split_value = 0
for observed in split_reads:
    split_value = observed + 1

u8_value = 253
for operation in range(operations):
    u8_value = (u8_value + 1) % 256

print(f"rmw_operations={operations}")
print(f"returned_old_values={tickets}")
print(f"unique_tickets={unique_tickets}")
print(f"rmw_final={rmw_value}")
print(f"split_load_store_final={split_value}")
print(f"lost_updates={operations - split_value}")
print(f"u8_wrapped_final={u8_value}")
```

Limitations: this sequential arithmetic model stipulates RMW serialization and a worst-case split-load/store schedule. It does not execute threads, atomic instructions, a language memory model, contention, retries, fairness, compiler/hardware mappings, failure, or reclamation.

## Alternatives and Trade-Offs

**Fetch arithmetic** is simple for independent counters/tickets, but domain wrap and hot-line contention remain.

**Exchange/test-and-set** provides direct handoff or lock state, with fairness and cache-traffic costs.

**CAS** supports conditional arbitrary transitions but adds retry, ABA, replay, and ordering complexity.

**Mutexes** make compound invariants, blocking, ownership, and condition waits easier to review, often outperforming hot spin protocols.

**Semaphores** directly express bounded permits and waiting rather than optimistic increment/rollback.

**Sharded counters** scale writes but offer approximate or expensive aggregate snapshots.

**Packed atomic words** update several small fields together at encoding, overflow, portability, and maintainability cost.

**Immutable descriptor swapping** handles larger state transitions with publication and reclamation obligations.

## Failure Modes and Misconceptions

1. **Atomic load plus atomic store is an RMW.** Another modification can interleave.
2. **Old and new return values are interchangeable.** Off-by-one ownership errors result.
3. **Atomic implies no overflow.** Arithmetic domain rules still apply.
4. **Unique until wrap means globally unique.** Live old generations can collide.
5. **Relaxed RMW publishes payload.** Atomicity alone supplies no such edge.
6. **AcqRel is automatically correct.** Ordering follows the actual publication relation.
7. **Update callbacks execute once.** CAS-backed APIs may replay them.
8. **One atomic makes several fields transactional.** Cross-location invariants remain exposed.
9. **Test-and-set lock is fair.** Repeated winners and starvation are possible.
10. **Lock-free means every call completes.** Individual starvation can remain.
11. **Reference count prevents use-after-free.** Acquisition itself needs a live-handle proof.
12. **CAS prevents ABA.** Equal representations can hide intervening histories.
13. **Counters are authoritative lifecycle records.** Missing identities can cancel numerically.
14. **More atomics improve scalability.** One hot cache line can serialize the system.
15. **RMW correctness proves safety-critical control.** Timing, devices, hazards, and authorization remain.

## Worked Examples

### Example 1

**Situation.** Two split load/store increments read zero and both store one.

**Reasoning.** Each individual access can be atomic and SC, but the four actions interleave R0,R1,W0,W1. One update is lost.

**Conclusion.** Use one RMW when increment is the abstract operation.

### Example 2

**Situation.** Fetch-add(1) returns 9.

**Reasoning.** It installs 10 atomically. For an old-value API, caller owns ticket 9; interpreting 10 as the ticket skips/reassigns identities.

**Conclusion.** Encode the returned-value convention in the API contract.

### Example 3

**Situation.** Six RMW increments start at zero.

**Reasoning.** Modification order serializes them. Old values are exactly 0..5 in some caller assignment, and final value is 6.

**Conclusion.** RMW proves nonwrapping epoch uniqueness independent of caller schedule.

### Example 4

**Situation.** An 8-bit ticket counter begins at 253 and allocates six tickets.

**Reasoning.** Old values cross 253,254,255,0,1,2 and final becomes 3. Tickets 0..2 may collide with still-live older tickets.

**Conclusion.** Add generation/exhaustion policy; atomic wrap is not identity safety.

### Example 5

**Situation.** A relaxed completed counter advances after writing a result, and another thread uses the count to decide the result is visible.

**Reasoning.** Numeric atomicity does not necessarily publish the result. Use release/acquire tied to the result state, a future/channel, or lock.

**Conclusion.** Metrics and publication carriers need separate contracts.

### Example 6

**Situation.** Java `getAndUpdate` callback sends an email.

**Reasoning.** Contention can reapply the callback before one CAS succeeds, causing duplicate email. Compute desired value purely; send only after commitment with idempotency.

**Conclusion.** Replayable update functions cannot own irreversible effects.

### Example 7

**Situation.** Fetch-add reserves capacity, discovers old>=limit, then subtracts.

**Reasoning.** The count temporarily exceeds the bound and other observers act on it; cancellation before rollback leaks a permit.

**Conclusion.** Use CAS-below-limit, semaphore, or lock with conserved permits.

### Example 8

**Situation.** Final reference decrement observes old=1 and immediately frees.

**Reasoning.** Destruction is safe only if no thread can acquire through an unprotected raw pointer and prior uses are properly ordered.

**Conclusion.** Numeric zero transition is one part of reclamation.

### Example 9

**Situation.** Eighty cores increment one exact global metric.

**Reasoning.** The single modification order/cache line becomes a bottleneck. Sharded relaxed counters can trade exact instantaneous reads for throughput.

**Conclusion.** Lock-free syntax does not eliminate serialization cost.

### Example 10

**Situation.** An industrial robot uses an atomic state word and claims collision safety.

**Reasoning.** The RMW can linearize software state, but not validate sensors, actuator response, deadlines, mechanical envelopes, device order, security, or hazard recovery.

**Conclusion.** Named robotics, controls, hardware, real-time, security, and functional-safety reviewers need target evidence; this chapter grants no approval.

## Cross-Program Connections

- **Algorithms:** fetch-add allocates work indices and CAS builds concurrent structures.
- **Computer architecture:** cache coherence and exclusive operations determine contention cost.
- **Programming languages:** atomic width, overflow, ordering, and progress guarantees are source-specific.
- **Operating systems:** parking and futex-style waits complement RMW state.
- **Data systems:** atomic counters differ from transactional multi-record updates and durable sequences.
- **Security:** wrap, ABA, and state authorization can become privilege or lifetime defects.
- **Performance engineering:** sharding, batching, padding, and backoff trade exactness for scalability.

## References

1. Maurice Herlihy and Nir Shavit. *The Art of Multiprocessor Programming*, revised first edition. Morgan Kaufmann, 2012.
2. Maged M. Michael. “High Performance Dynamic Lock-Free Hash Tables and List-Based Sets.” SPAA, 2002.
3. Edsger W. Dijkstra. “Cooperating Sequential Processes.” 1965.
4. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
5. Paul E. McKenney. *Is Parallel Programming Hard, And, If So, What Can You Do About It?* 2023 edition.
6. ISO C++ working draft. “Atomic types, order and consistency.” Current draft accessed 2026-08-29.
7. Oracle. “`java.util.concurrent.atomic`, Java SE 26 API.” 2026. Accessed 2026-08-29.
8. Rust Project. “`std::sync::atomic`, Rust 1.98.0.” 2026. Accessed 2026-08-29.
9. The Go Authors. “Package `sync/atomic` and The Go Memory Model.” Accessed 2026-08-29.
10. Intel. *Intel 64 and IA-32 Architectures Software Developer's Manual*, version 092, 2026. Accessed 2026-08-29.

## Exercises

### Exercise 1

Define an atomic RMW and explain why separate SC load/store is not equivalent.

### Exercise 2

Trace four fetch-add(3) operations starting at 10 for old-value and new-value APIs. State final value and overflow assumption.

### Exercise 3

Diagnose an RMW-backed bounded counter that increments, checks capacity afterward, rolls back on rejection, and publishes queued payload through a relaxed count. Repair capacity and publication.

### Exercise 4

Compare fetch-add, CAS, semaphore, mutex, and sharded counters for allocating request IDs and limiting in-flight work. Choose separate mechanisms for the two requirements.

### Exercise 5

A medical dosing scheduler uses one atomic word for command state and references counted buffers. Specify what the RMW proof covers, the lifetime and ordering evidence still required, and the human-review boundary.

## Answers to the Exercises

### Answer 1

An RMW reads one atomic location and performs its specified modification as one indivisible atomic action in that location's modification order. A separate load and store are two actions: another thread can read/modify between them. Even if both are SC, two incrementers can both load zero and store one. One fetch-add prevents that lost update for the location.

### Answer 2

Starting at 10, the four atomic transitions are 10->13, 13->16, 16->19, and 19->22. An old-value API returns 10,13,16,19; a new-value API returns 13,16,19,22. Final value is 22. This assumes the numeric type represents all values and its arithmetic does not wrap; otherwise the exact language/type overflow rule must be applied.

### Answer 3

Post-increment checking violates a hard bound transiently; rollback can be skipped by failure and can confuse observers. A relaxed count also does not publish queue payload.

Use a semaphore or lock to conserve permits, or a CAS loop that changes count only when old<capacity. Transfer payload through a bounded thread-safe queue whose enqueue/dequeue contract publishes it, or use explicit release/acquire state tied to the exact slot/generation. If enqueue fails after reservation, release the owned permit in guaranteed cleanup. Keep advisory metrics separate from authoritative capacity state.

### Answer 4

Request IDs need unique nonwrapping allocation: fetch-add is simple if width, wrap horizon, restart, and durability are acceptable; otherwise allocate generation/ranges or use a durable sequence. CAS adds no benefit for unconditional increments. Sharding improves throughput but complicates global uniqueness unless shards own disjoint ranges.

In-flight capacity needs a conserved permit with waiting/cancellation/shutdown semantics: use a semaphore or mutex/condition. A CAS-bounded counter works only with a complete wait/wake and failure protocol. Do not use the same unbounded ID counter as capacity. Separate mechanisms align each invariant with its owner.

### Answer 5

The RMW proof can establish one atomic transition of the encoded word, returned prior state, and ordering of word modifications. It must also validate legal bit combinations, caller authority, overflow/generation, and the chosen memory order's publication path.

Reference-counted buffers require safe acquisition from a live handle, strong/weak-count invariants, visibility before use, final-decrement ordering, prevention of new acquisition, and reclamation after all readers. The scheduler additionally needs command identity, bounded admission, cancellation, device acknowledgement, deadlines, fault containment, and terminal reconciliation.

Named clinical/domain, controls, concurrency, hardware, real-time, cybersecurity, quality, regulatory, and functional-safety reviewers must approve system-specific claims with target and hazard evidence. This answer does not establish dosing or deployment fitness.
