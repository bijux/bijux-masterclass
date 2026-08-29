---
module_id: CONPAR-028
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 28
title: Relaxed Atomics
status: complete
last_verified: 2026-08-29
---

# Relaxed Atomics

## One-Page Review

### Governing question

When is atomicity and per-object coherence sufficient without using an atomic operation to order other memory, and how can that independence be proved rather than assumed?

### Essential definitions

- A **relaxed atomic operation** is indivisible for its atomic object but does not itself order other memory.
- **Modification order** is the language-defined total order of modifications to one atomic object.
- **Coherence** constrains observations of one atomic object; it is not a coherent snapshot of several objects.
- An **advisory metric** tolerates a snapshot that is approximate, cross-field inconsistent, or stale within its documented purpose.
- An **authoritative invariant** decides ownership, capacity, safety, billing, or lifecycle and must not rely on an unproved advisory snapshot.
- An **independent atomic** carries no payload-publication or cross-location ordering responsibility.
- A **ticket** is a unique old value returned by an atomic RMW within a defined nonwrapping epoch.
- **Wraparound** reuses a numeric representation after its finite domain is exhausted.
- **Mixed-order protocol** uses relaxed operations for local bookkeeping and stronger operations at actual publication/lifetime boundaries.
- **Race freedom** from atomic access does not imply the surrounding algorithm is correct.

### Central model, mechanism, or theorem

A relaxed operation on atomic `x` remains atomic and participates in `x`'s modification order. Thus `fetch_add(1)` can allocate distinct old values in a nonwrapping epoch, and relaxed loads cannot tear `x`. It creates no release/acquire synchronizes-with edge for ordinary payload or a different atomic `y`. Relaxed is sufficient only when the operation's complete correctness claim is expressible using `x`'s atomic value, modification order, and separately established ordering.

### Critical invariants

Every relaxed object has one explicit owner claim. It publishes no adjacent payload. Conflicting ordinary memory is ordered elsewhere or immutable. Multiple relaxed fields are labeled non-snapshot or protected by a separate snapshot protocol. Numeric width, overflow, reset, restart, and persistence are defined. CAS recomputes from current witnesses. Reference increments begin from an already-live reference; final destruction has stronger lifetime ordering. Cancellation polling does not promise a deadline. Target support and performance are measured. A later refactor that adds payload or authoritative decisions triggers ordering review.

### Common failures

Teams use a relaxed ready flag to publish payload; infer `completed≤started` from two separately loaded metrics; decide capacity from an approximate gauge; treat atomic as durable; forget ticket wrap or process restart; use relaxed reference decrement to free storage; assume a relaxed cancellation flag must be observed promptly; mix atomic and non-atomic accesses; believe all relaxed observations share one global order; or weaken ordering because x86 tests pass.

### Compact example

Worker increments relaxed `started`, then relaxed `finished`. An observer can read `started=0` before both increments and `finished=1` afterward, producing an advisory snapshot `(0,1)` even though the worker performed started first. Each value is a valid atomic observation of its own object; the pair is not one instant. Final reconciliation after join can still prove `started=finished=1`.

### Connections

[Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md) supplies modification-order reasoning; [Acquire and Release Ordering](027-acquire-and-release-ordering.md) identifies publication edges relaxed does not provide. The [program roadmap](../ROADMAP.md) next studies false sharing and cache-line contention.

## Governing Question

How should engineers prove that a relaxed atomic's value is self-contained, distinguish advisory observation from authoritative state, and combine relaxed bookkeeping with the stronger synchronization, lifetime, persistence, and recovery protocols the surrounding system still requires?

Relaxed is not “weak and probably fine.” It is a precise claim that cross-location ordering is unnecessary at this operation.

## Why This Matters

Metrics counters, statistical sampling, sequence allocation, reference-count increments, work indexes, progress estimates, ownership-neutral flags, and some fields inside lock-free algorithms can use relaxed operations. On some targets or compiler paths, avoiding unnecessary ordering reduces constraints; more importantly, expressing the true protocol clarifies which operation actually publishes state.

Misuse is dangerous because relaxed access still looks reliable. It is atomic, it does not tear, and tests on strong hardware often show intuitive results. The missing guarantee concerns other memory. A consumer may observe a relaxed flag change without receiving the payload writes that logically preceded it. Two individually sound counters can yield an impossible-looking pair. A numeric reference count can be correct while the object is already reclaimed.

The design method is therefore subtractive. First specify the full correctness claim. Remove acquire/release only after proving that the atomic object publishes nothing, protects no unrelated ordinary access, and supplies no cross-object snapshot. Document that proof so a later payload-bearing refactor does not silently invalidate it.

## Prerequisites and Retrieval

Retrieve:

- reordering boundaries from [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md);
- global versus per-object order from [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md);
- hb and data-race reasoning from [Happens-Before Relations](023-happens-before-relations.md);
- publication and lifetime from [Visibility and Publication](024-visibility-and-publication.md);
- RMW modification-order arguments from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- CAS retry purity from [Compare-and-Swap Loops](026-compare-and-swap-loops.md); and
- release/acquire reads-from paths from [Acquire and Release Ordering](027-acquire-and-release-ordering.md).

Retrieval prompt: name one fact an atomic fetch-add proves about its own counter and one fact it cannot prove about a payload written before the increment.

## Learning Objectives

After completing this module, a learner can:

1. state the guarantees and non-guarantees of relaxed atomic access;
2. reason from one object's modification order and coherence constraints;
3. classify state as advisory, authoritative, or publication-bearing;
4. demonstrate why separate atomic loads are not a multi-field snapshot;
5. prove unique ticket allocation within bounded width, epoch, and lifetime;
6. place relaxed operations correctly inside mixed-order protocols;
7. diagnose reference-count, cancellation, wrap, reset, and persistence defects;
8. compare C++/Rust relaxed modes with Java and Go interfaces; and
9. validate correctness and performance without relying on strong-hardware accidents.

## Core Exposition

### What relaxed retains

In C++ and closely related Rust atomic interfaces, relaxed operations remain atomic. A load observes one permitted value of that atomic object; a store is one modification; an RMW performs its read and modification indivisibly. Modifications of one object participate in one modification order.

These guarantees are substantial. Concurrent relaxed fetch-add operations do not lose updates to that counter. Each RMW receives the appropriate prior value in modification order. Atomic-width and alignment requirements still apply, and an implementation may use a lock when the target lacks a lock-free instruction.

Relaxed does not mean compiler freedom to invent a torn atomic access. Nor does it mean “ordinary non-atomic but faster.”

### What relaxed removes

A relaxed operation does not itself perform acquire or release ordering. Observing its value therefore does not create the release/acquire synchronizes-with edge needed to publish ordinary memory.

Producer:

1. ordinary write `payload=42`;
2. relaxed store `ready=1`.

Consumer:

1. relaxed load ready and see one;
2. ordinary read payload.

The ready accesses are atomic, but no hb path orders the conflicting payload accesses. In C++-family models this is a data race if they can be concurrent, with the language's severe consequences. Make the store release and matching load acquire, or use a lock/channel/once abstraction.

### One-object reasoning

For atomic `x`, modification order answers questions such as:

- which successful RMW precedes another;
- which old ticket an RMW returns;
- whether a CAS comparison matched the current representation;
- how one thread's same-object observations respect language coherence rules.

It does not order atomic `y` into the same snapshot. Each object has its own modification order. Sequential consistency adds a common order for SC operations; relaxed operations do not participate in that SC order merely because they are atomic.

Be precise about “newer.” Modification order is a model relation, not a synchronized wall clock. A numeric value can decrease if the program stores a smaller value, and wrap can make a later modification look smaller.

### Advisory metrics

A request service might maintain relaxed atomics:

- accepted;
- started;
- completed;
- failed;
- active;
- queue-depth estimate.

Each update remains atomic. A scrape loading fields independently is not an instantaneous system state. It can observe completed after one worker's increment but miss that worker's earlier started increment because the accesses use different atomic objects without a cross-object observation rule.

This is acceptable only when the interface says the snapshot is advisory. Dashboards, alert smoothing, capacity trends, and debugging may tolerate it. Billing, permit conservation, data-loss detection, and final success criteria usually may not.

At quiescence—after admission stops and all workers join—a final load can be meaningful because join or another lifecycle primitive supplies ordering and no further updates occur. Even then, reconcile authoritative identities/outcomes when missing and duplicated work can cancel numerically.

### Gauges are not resource owners

An `active` gauge incremented on entry and decremented on exit can show approximate load. It should not be used as a check-then-act capacity controller:

`if active.load(relaxed) < K then active.fetch_add(1, relaxed)`.

Two callers can both pass the check. A CAS-bounded counter can atomically reserve, but waiting, cancellation, shutdown, and permit return remain. A semaphore or bounded queue usually owns capacity more clearly.

Keep an advisory mirror if observation needs it, but name the authoritative primitive. Never let a dashboard counter become an undocumented second owner of admission.

### Unique tickets and identifiers

Relaxed fetch-add can allocate unique old values in one atomic modification order. Starting at `b`, `n` successful increments by one return `b...b+n-1` in some caller assignment and leave `b+n`, assuming the arithmetic domain does not wrap.

The proof is narrower than “globally unique ID”:

- fixed-width values wrap;
- process restart can reset the counter;
- several processes have separate memory;
- snapshots/restores can replay state;
- returned IDs may be discarded;
- persistent identity needs durable allocation/recovery.

Use an epoch, durable range allocation, random identity with collision analysis, or a database sequence when the boundary exceeds one live process epoch.

### Multi-counter invariants

Suppose every worker increments started before completed. That program order does not force an observer's two relaxed loads to present `completed≤started`. The observer can load started early and completed late.

Options:

- label the pair approximate;
- read under the same mutex that updates the fields;
- pack fields into one atomic representation and update them together;
- publish an immutable snapshot root;
- use a version/seqlock-style validation protocol with correct ordering;
- collect per-operation records and aggregate after quiescence.

Repeatedly loading until two reads match is not automatically a snapshot algorithm. Prove which writers and orderings make validation sound.

### Relaxed CAS and state machines

A relaxed CAS can correctly arbitrate a transition whose entire abstract meaning lives in the atomic state. For example, `CREATED→RUNNING` may use relaxed CAS if:

- construction was already published through thread creation, ownership transfer, a lock, or another mechanism;
- observing RUNNING grants no access to unrelated mutable payload;
- the transition publishes no preceding writer state;
- later lifecycle edges handle completion and cleanup.

If RUNNING is the publication flag for configuration, the same CAS needs release on its successful write, and consumers need a qualifying acquire. Ordering follows responsibility, not the enum name.

CAS still needs witness refresh, pure recomputation, ABA/reuse analysis, and progress policy.

### Cancellation flags

A relaxed atomic boolean can communicate a request when the only shared fact is the boolean and all cleanup/data access is synchronized elsewhere. Pollers may eventually observe it in real implementations, but language memory models do not generally provide a real-time deadline or scheduler fairness.

Do not use the flag observation to consume cancellation metadata written beside it. Do not claim “cancelled” means all workers stopped, resources rolled back, or external work did not commit. Join, structured cancellation, acknowledgements, and terminal reconciliation establish those claims.

Safety-critical stop paths require bounded target evidence and often stronger platform mechanisms. Relaxed polling is not an emergency-stop circuit.

### Reference counting

Reference-count increments are often relaxed because obtaining another reference does not need to publish other memory when the caller already owns a live reference. The premise is crucial: reading an unprotected raw pointer and then incrementing its count can race with final destruction.

The decrement that may reach zero typically needs stronger ordering so prior uses become ordered before destruction, plus a proof that no new reference can appear. Exact algorithms differ by library and model. Weak counts, cycles, overflow, resurrection, and custom deleters add obligations.

Use standard reference-counted types. “The count is atomic” is not a reclamation proof, and changing all count operations to relaxed is not a safe generic optimization.

### Sharded counters

One hot atomic counter can serialize cache-line ownership. Sharding assigns each thread/core/partition a counter, then sums relaxed loads. Updates scale better, but the aggregate is even less like one instant: shards are observed at different times.

Sharding is suitable for approximate metrics. Exact bounded accounting requires a protocol for registration, shard lifetime, migration, overflow, and final reconciliation. Dynamic shard removal can lose counts unless transfer is synchronized.

Padding may prevent false sharing between shards, which the next module treats. Layout is target-specific and must be measured.

### Mixed-order protocols

Real designs often use different orderings for different facts:

- relaxed counters record attempts and completions;
- release/acquire state publishes the final immutable result;
- a mutex protects an error collection;
- join establishes quiescence;
- durable storage records external commitment.

This is not inconsistency. Each edge owns a claim. The review should contain a table or graph mapping fields to responsibilities and explaining why each relaxed field carries no publication.

Avoid “all relaxed for speed” and “all SC for safety” as substitutes for design. SC can simplify ordering but not capacity, lifetime, wrap, or durability. Relaxed can be correct but only with a narrower claim.

### Language differences

**C++** defines `memory_order::relaxed` as providing no memory ordering while atomic access remains indivisible and subject to atomic coherence/modification-order rules.

**Rust** exposes `Ordering::Relaxed` for its atomic operations, with semantics modeled closely on C++20; its ownership system does not automatically prove an atomic protocol's hb or lifetime assumptions.

**Java** VarHandle offers plain, opaque, acquire, release, and volatile access modes. “Opaque” and “plain” are Java-defined modes, not synonyms to paste into C++ reasoning. Java atomic wrapper methods often have volatile-like documented effects unless a specific weak mode is selected.

**Go** `sync/atomic` operations behave as though in a sequentially consistent order and offer no per-call relaxed selector. A relaxed C++/Rust design must be expressed using Go's actual API, not emulated with ordinary racy accesses.

Check the current selected language and library documentation. Portable pseudocode must state which model it assumes.

### Performance reality

Relaxed may reduce compiler constraints or hardware instructions on weakly ordered targets. For a simple load/store on x86-64, acquire/release may compile identically to relaxed. Hot-counter performance may instead be dominated by cache-line ownership, so ordering changes do not remove coherence traffic.

Measure optimized builds on supported targets. Record compiler, flags, architecture, topology, operation mix, contention, throughput, and tail latency. Inspect generated code to understand differences.

Do not weaken correctness based on an uncontended nanobenchmark. Sharding, batching, ownership transfer, or eliminating shared writes often produces the larger improvement.

### Testing and review

Test arithmetic boundaries, wrap, reset/restart, high contention, unsupported widths, CAS failure, sharded registration, and quiescent reconciliation. For each relaxed object, add a negative review question: what adjacent data would a maintainer expect this value to publish?

Use model checking/litmus tests for allowed weak outcomes; sanitizers/race detectors for ordinary surrounding access; stress for accounting and lifecycle; assembly inspection for mappings; performance counters for coherence traffic; fault injection for crashes between atomic and external effects.

Strong-hardware tests cannot prove an outcome forbidden. Race-detector silence cannot prove a multi-field snapshot. A correct proof states what relaxed does not claim.

## Definitions and Notation

Let atomic object `x` have modification order `mo_x`. A relaxed load/store/RMW is atomic for `x` and uses `mo_x` according to the language's rules, but adds no acquire/release sw edge for other memory.

For a nonwrapping fetch-add epoch starting at `b` with `n` successful unit increments:

`returned = {b, b+1, ..., b+n-1}` and `final=b+n`.

For advisory fields `s` and `f`, a snapshot `(load(s),load(f))` consists of two observations, not an atomic pair. Even if every writer sequences `s++` before `f++`, the observer can obtain `(0,1)` by loading `s` before both and `f` after both.

Let `Q` denote quiescence established by a documented lifecycle edge. Claims made after `Q` can use the fact that no selected writer remains; relaxed operations did not create `Q`.

## Mechanisms, Invariants, or Proof Structure

For every candidate relaxed operation:

1. **Name the value's responsibility.** Counter, ticket, state arbitration, poll hint, or local algorithm field.
2. **State the complete claim.** Express it using the atomic value and its modification order.
3. **Prove independence.** No ordinary payload or different atomic relies on observing this operation.
4. **Classify observations.** Advisory snapshot, authoritative transition, or final quiescent report.
5. **Bound the domain.** Width, signedness, overflow, wrap, reset, restart, and persistence.
6. **Check lifecycle.** Construction publication, ownership, cancellation, join, destruction, and reclamation use other edges.
7. **Check compound state.** Pack, lock, validate, or explicitly tolerate cross-field inconsistency.
8. **Check language support.** Do not translate relaxed syntax into a different model.
9. **Check target behavior.** Atomic width/lock freedom and performance are empirical.
10. **Make refactoring hazards visible.** New payload or authority requires ordering review.
11. **Exercise adversarial schedules.** Early/late loads, wrap, contention, reset, and failure.
12. **Prefer a higher-level owner when the independence proof is fragile.**

The executable model constructs an allowed advisory observation by sampling `started` before two complete worker histories and `finished` after them. It also verifies quiescent equality and nonwrapping ticket uniqueness.

<!-- bijux-verify: {"id":"relaxed-advisory-counter-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"workers=2\nadvisory_started=0\nadvisory_finished=2\nadvisory_completed_exceeds_started=True\nfinal_started=2\nfinal_finished=2\nquiescent_conservation=True\ntickets=[0, 1, 2, 3]\nunique_tickets=4\n","stderr":""}} -->
```python
workers = 2
started = 0
finished = 0

advisory_started = started
for worker in range(workers):
    started += 1
    finished += 1
advisory_finished = finished

ticket_counter = 0
tickets = []
for request in range(4):
    old = ticket_counter
    ticket_counter += 1
    tickets.append(old)

unique_tickets = 0
for ticket in tickets:
    if tickets.count(ticket) == 1:
        unique_tickets += 1

print(f"workers={workers}")
print(f"advisory_started={advisory_started}")
print(f"advisory_finished={advisory_finished}")
print(f"advisory_completed_exceeds_started={advisory_finished > advisory_started}")
print(f"final_started={started}")
print(f"final_finished={finished}")
print(f"quiescent_conservation={started == finished == workers}")
print(f"tickets={tickets}")
print(f"unique_tickets={unique_tickets}")
```

Limitations: this sequential schedule demonstrates that two samples taken at different times need not be one snapshot and recomputes ticket arithmetic. It does not execute relaxed atomics, formalize a language memory model, enumerate allowed observations, prove propagation/liveness, test wrap or restart, create contention, establish quiescence, inspect target mappings, or validate reclamation.

## Alternatives and Trade-Offs

**Acquire/release atomics** publish or consume other memory through a proven observation. Use them when the atomic is a carrier.

**SC atomics** add a common language-defined order and can simplify multi-atomic arguments, but do not automatically create a snapshot or fix lifecycle.

**Mutex-protected state** provides compound invariants, coherent snapshots, waiting integration, and a clear ownership boundary.

**Channels/actors** attach synchronization to ownership transfer rather than a detached counter.

**Packed atomic state** can update several bounded fields together, at the cost of width, wrap, encoding, and portability.

**Sharded relaxed counters** improve update scalability while weakening instantaneous aggregate meaning.

**Event logs or indexed outcomes** provide authoritative reconciliation and auditability at higher storage/processing cost.

**Higher-level reference types** encapsulate counting, lifetime, and reclamation that raw relaxed integers cannot.

## Failure Modes and Misconceptions

1. **Relaxed means non-atomic.** It retains atomicity for the object.
2. **Atomic means publication.** Relaxed observation supplies no release/acquire hb edge.
3. **One modification order means one global order.** It belongs to one object.
4. **Two atomic loads form a snapshot.** They may observe different instants.
5. **Writer program order preserves cross-counter inequalities for observers.** Different relaxed objects do not provide that snapshot guarantee.
6. **Metrics can enforce capacity.** Advisory observation is not resource ownership.
7. **Fetch-add IDs are globally unique.** Width, epoch, restart, and process scope bound the proof.
8. **Atomic values are durable.** Process memory does not establish crash persistence.
9. **Relaxed CAS can publish configuration.** It arbitrates only the atomic state without a release edge.
10. **Relaxed cancellation has bounded response.** Memory models do not guarantee scheduling or deadlines.
11. **Relaxed reference counts make reclamation safe.** Acquisition and final decrement require a lifetime protocol.
12. **Sharded totals are exact snapshots.** Shards are sampled separately.
13. **Race-free means logically consistent.** Atomic fields can encode an invalid protocol.
14. **x86 makes ordering irrelevant.** Source semantics govern compiler and portability.
15. **Go ordinary accesses emulate relaxed atomics.** They introduce races; Go atomics are specified differently.
16. **Relaxed must be faster.** Hardware code and contention may be identical.
17. **SC fixes overflow or ABA.** Ordering strength does not change representation reuse.
18. **A passing stress test proves independence.** Missing hb outcomes can be rare or target-hidden.

## Worked Examples

### Example 1

**Situation.** Eight relaxed fetch-add operations increment one metric.

**Reasoning.** Each RMW is indivisible in the counter's modification order, so no increment is lost and the final value increases by eight absent wrap.

**Conclusion.** Relaxed is sufficient for the counter's numeric update.

### Example 2

**Situation.** A producer writes payload then relaxed-stores ready; consumer sees ready and reads payload.

**Reasoning.** The ready value is atomic, but there is no release/acquire sw edge ordering payload.

**Conclusion.** Use a publication protocol, not a relaxed flag.

### Example 3

**Situation.** A scrape observes started zero and completed one although workers increment started first.

**Reasoning.** It loaded started before the worker and completed afterward. The two relaxed objects are not sampled atomically.

**Conclusion.** Label the pair advisory or introduce snapshot synchronization.

### Example 4

**Situation.** Relaxed fetch-add returns ticket 999 from a 1,000-value domain.

**Reasoning.** The next epoch wraps to zero and can collide with a live ticket. Atomicity preserves the wrap transition, not uniqueness across it.

**Conclusion.** Bound lifetime or add durable generation/exhaustion.

### Example 5

**Situation.** A relaxed CAS changes CREATED to RUNNING after an object was safely shared through thread creation.

**Reasoning.** If RUNNING publishes no payload and owns only exclusive state arbitration, relaxed ordering can suffice. If it publishes configuration, it cannot.

**Conclusion.** Classify the state transition's responsibility explicitly.

### Example 6

**Situation.** A worker polls a relaxed cancelled boolean and cleanup is coordinated by join.

**Reasoning.** The flag can communicate the standalone request without carrying payload. Join, not relaxed observation, proves termination and cleanup visibility.

**Conclusion.** Separate request, acknowledgement, and reconciliation.

### Example 7

**Situation.** Code increments a reference count through a raw pointer that may be freed.

**Reasoning.** Relaxed numeric increment cannot make the initial pointer live. The final owner may concurrently reclaim it.

**Conclusion.** Safe acquisition precedes any relaxed count optimization.

### Example 8

**Situation.** Sixty-four cores update one relaxed counter and throughput collapses.

**Reasoning.** Relaxed removes ordering of other memory, not cache-line modification ownership. Sharding or batching may reduce coherence traffic.

**Conclusion.** Ordering strength and contention topology are different dimensions.

### Example 9

**Situation.** A Go port replaces C++ relaxed atomics with ordinary integer accesses.

**Reasoning.** Ordinary concurrent access races. Go's atomic API supplies its documented SC semantics and no relaxed selector.

**Conclusion.** Port the invariant through the destination model, not the spelling.

### Example 10

**Situation.** An autonomous vehicle uses a relaxed cancellation flag as its emergency stop guarantee.

**Reasoning.** The flag proves neither bounded observation nor scheduler execution, actuator command, device acknowledgement, fault containment, or safe physical state.

**Conclusion.** Named controls, real-time, hardware, security, automotive, quality, and functional-safety reviewers need target evidence; this chapter grants no approval.

## Cross-Program Connections

- **Programming languages:** atomic modes, data-race consequences, and coherence rules are model-specific.
- **Computer architecture:** relaxed operations still incur cache coherence and may map differently by target.
- **Operating systems:** join, locks, scheduling, and wakeups provide lifecycle facts relaxed polling lacks.
- **Data systems:** in-memory atomic counters differ from durable sequences and transactional snapshots.
- **Observability:** approximate metrics need semantic labels, reset policy, and reconciliation.
- **Security:** wrap, stale state, use-after-free, and false authorization from advisory values create vulnerabilities.
- **Performance engineering:** sharding and batching often matter more than weakening ordering.
- **Safety engineering:** an atomic software request is not bounded physical control.

## References

1. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
2. Mark Batty et al. “Mathematizing C++ Concurrency.” POPL, 2011.
3. Jade Alglave, Luc Maranget, and Michael Tautschnig. “Herding Cats: Modelling, Simulation, Testing, and Data Mining for Weak Memory.” TOPLAS 36(2), 2014.
4. Maurice Herlihy and Nir Shavit. *The Art of Multiprocessor Programming*, revised first edition. Morgan Kaufmann, 2012.
5. ISO C++ working draft. “Atomic types, order and consistency.” Current draft accessed 2026-08-29.
6. Rust Project. “`std::sync::atomic::Ordering`, Rust 1.98.0.” 2026. Accessed 2026-08-29.
7. Oracle. “`VarHandle`, Java SE 26 API,” and *Java Language Specification*, section 17.4. 2026. Accessed 2026-08-29.
8. The Go Authors. “The Go Memory Model” and “Package `sync/atomic`.” Accessed 2026-08-29.
9. Paul E. McKenney. *Is Parallel Programming Hard, And, If So, What Can You Do About It?* 2023 edition.
10. Maged M. Michael. “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects.” IEEE TPDS 15(6), 2004.

## Exercises

### Exercise 1

State what a relaxed atomic load, store, and RMW guarantee and what they do not guarantee about other memory.

### Exercise 2

Trace three workers that each relaxed-increment started then completed. Construct an advisory observation with completed greater than started, and state the final quiescent values.

### Exercise 3

Diagnose a service that uses a relaxed ready flag to publish payload, a relaxed active gauge for hard capacity, and a relaxed decrement to free reference-counted objects. Repair all three boundaries.

### Exercise 4

Compare one relaxed global counter, sharded relaxed counters, a mutex-protected aggregate, and indexed terminal records for live dashboards, hard quotas, and final billing.

### Exercise 5

A medical monitoring process uses relaxed atomics for sample IDs, drop counts, cancellation, and a device-visible buffer-ready flag. Bound every valid relaxed claim and specify the evidence and human review needed for the rest.

## Answers to the Exercises

### Answer 1

A relaxed load observes one permitted indivisible value of its atomic object; a relaxed store is one atomic modification; a relaxed RMW reads and modifies that object indivisibly. Operations participate in the object's modification order and applicable coherence rules.

They do not themselves perform acquire/release ordering, publish preceding ordinary writes, consume adjacent payload, create a coherent multi-object snapshot, protect lifetime, ensure progress, or establish durability. Those claims require other language-defined synchronization and lifecycle protocols.

### Answer 2

Observer first loads started as zero. All three workers then execute started++ followed by completed++, leaving both at three. Observer finally loads completed as three. Its pair is `(started=0, completed=3)` even though no worker reversed its own program order.

Each sample is valid for its object but the pair is not one instant. After a documented quiescence edge such as joining all workers, and with no further updates, final loads return started three and completed three. Join establishes lifecycle ordering; relaxed counters do not establish the join.

### Answer 3

The relaxed ready flag does not publish payload. Complete payload construction, then release-publish a value/generation; consumer acquire-observes the matching value before reading, or use a queue/channel/lock.

The active gauge has a check-then-act race and is not authoritative capacity. Use a semaphore, bounded queue, mutex-protected invariant, or CAS reservation with complete wait/cancel/return semantics; retain the gauge only as an advisory mirror.

A relaxed final decrement alone is not generic reclamation. Use a standard reference-counted type whose safe acquisition, decrement ordering, weak counts, overflow, and destruction rules are proved. Never increment through an unprotected raw pointer. Reclaim only after the protocol proves no references/readers remain.

### Answer 4

A global relaxed counter gives atomic updates and inexpensive approximate reads but can become a hot cache line. Sharded relaxed counters improve update throughput while producing a time-skewed aggregate and requiring shard lifecycle/reconciliation.

A mutex-protected aggregate provides a coherent compound snapshot and can own a hard quota, with contention/blocking costs. Indexed terminal records cost more memory/storage but let final billing detect duplicates, omissions, retries, and identities rather than trusting cancelling totals.

Use relaxed global/sharded counters for dashboards, a semaphore/mutex/bounded queue for quotas, and durable indexed outcomes for billing. Cross-check final counters after quiescence, but do not promote them to the sole ledger.

### Answer 5

Relaxed fetch-add can allocate sample IDs only within one nonwrapping live-process epoch; it does not survive restart or prove global uniqueness. Relaxed drop counts can be advisory metrics with documented reset/overflow and quiescent reconciliation. Relaxed cancellation can carry a standalone request when acknowledgements, cleanup, and terminal state use separate synchronization; it provides no response deadline.

The device-visible ready flag is not justified by ordinary language relaxed atomics. Establish CPU payload publication, storage lifetime, DMA/cache coherence, required platform barriers and cache maintenance, descriptor generation, device doorbell order, acknowledgement, timeout, and recovery from partial commitment.

Verify source algorithms with model/race testing, IDs at wrap/restart, target assembly and atomic support, hardware-in-loop DMA traces, cache-coherence tests, timing distributions, fault injection, and terminal reconciliation. Named clinical/domain, device, driver/kernel, architecture, concurrency, real-time, cybersecurity, quality, regulatory, and functional-safety reviewers must approve target claims. This answer supplies no medical or deployment approval.
