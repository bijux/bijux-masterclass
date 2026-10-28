---
module_id: CONPAR-055
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 55
title: Hazard Pointers
status: complete
last_verified: 2026-08-29
---

# Hazard Pointers

## One-Page Review

### Governing question

How can a thread announce exactly which removable objects it may dereference so other threads defer reclamation, while preserving validation, bounded resources, memory ordering, progress, and safe lifecycle semantics?

### Essential definitions

- A **hazard pointer** is a publicly scannable protection slot owned for mutation by one participant and containing either null or the address of an object that participant may access.
- **Protection** publishes an observed address in a hazard slot and validates that the source still denotes that address before dereference.
- **Retirement** transfers an unlinked object's eventual reclamation responsibility to a reclamation domain; retirement is not deletion.
- A **retire list** contains retired objects not yet proven absent from every relevant hazard slot.
- A **scan** takes a suitable snapshot of hazard slots and reclaims retired objects whose addresses are absent, subject to the protocol's ordering proof.
- A **hazard domain** owns participant records, retire queues, scan policy, deleters, and shutdown rules.
- A **protection window** begins only after publication and validation and ends before the slot is cleared or reused.
- A **hazard budget** is the maximum simultaneously protected nodes needed by one operation.
- **Reclamation lag** is the time or count between retirement and actual destruction/reuse.
- **lifetime safety** prevents access after reclamation; it does not by itself synchronize mutable object fields or prove data-structure linearizability.

### Central model, mechanism, or theorem

A reader repeatedly loads candidate `p` from an atomic source, publishes `p` to its hazard slot, and reloads the source. If the source changed, it clears or replaces protection and retries without dereferencing `p`; if unchanged, removal either occurred before publication and validation detects it, or occurs afterward and any scanner must observe the hazard before reclaiming. A remover first unlinks an object, then retires it. A scan reclaims only retired objects absent from the protected set. Correctness requires a source-language ordering argument connecting publication, validation, retirement, scan, and deletion; the folklore loop alone is not a proof.

### Critical invariants

Each slot has one writer and scanners only read it. A thread dereferences a removable object only inside a validated protection window. The source publication/load and hazard publication/scan orders close the protect-versus-retire race. Unlink happens before retirement; retirement occurs exactly once; reclamation occurs exactly once and only after absence from all relevant hazards is established. Failed data-structure CAS refreshes protection and all derived links. The hazard budget covers every simultaneously dereferenced node. Deleters do not violate progress or re-enter an unsafe domain. Participant exit clears slots; domain destruction waits for admission closure, operations, scans, and retired objects.

### Common failures

Code dereferences before publishing; publishes but does not validate; scans before unlink; deletes instead of retires; clears protection while still using a borrowed field; protects a predecessor but dereferences an unprotected successor; reuses one slot for two live nodes; loads slots with unjustified relaxed ordering; assumes a scan is a global memory fence; retires twice; leaks retire lists on thread exit; lets an abandoned participant retain arbitrary objects; invokes a blocking or re-entrant deleter in a lock-free path; ignores fixed slot exhaustion; destroys a domain while holders survive; or claims hazard pointers make payload mutation race-free.

### Compact example

R loads root A and pauses. W exchanges root to B and retires A. Before W reclaims, R publishes A then reloads root and sees B, so R must not dereference A and clears the slot. A later scan finds no hazard A and reclaims it. If R had published and validated A before W's exchange, the scan would find A and defer it until R clears. Both orderings preserve lifetime.

### Connections

[Lock-Free Queues](053-lock-free-queues.md) motivates sentinel lifetime. [ABA Problems and Tagged References](054-aba-problems-and-tagged-references.md) separates change detection from lifetime. The next module contrasts epoch-based reclamation; later modules use reclamation in nonblocking structures and production audits.

## Governing Question

How should an engineer derive, integrate, verify, and operate a hazard-pointer domain so a raw pointer obtained from a changing atomic source remains valid for exactly the accesses that use it?

The key difficulty is the gap between observing an address and announcing it. Protection must be published, then the observation must be validated, before the first dereference.

## Why This Matters

An atomic root protects only its own bits. A thread can load pointer A while another unlinks and frees A before the first thread reads `A.next` or `A.payload`. The later CAS may fail safely, but the earlier dereference is already invalid. Immediate deletion therefore breaks many otherwise linearizable stack, queue, list, and registry algorithms.

Never reclaiming avoids use-after-free but can exhaust memory. Reference counting adds an acquisition race when the count lives in an object reached through an unprotected raw pointer, plus contended read-modify-write operations. Epoch schemes protect groups of read-side operations efficiently but one stalled participant can retain all later retired objects. Hazard pointers offer fine-grained protection: a stalled participant normally pins only the bounded objects named in its slots.

That benefit requires infrastructure. A domain must provision and recycle records, batch scans, manage per-thread retirement, execute deleters, handle participant death and process shutdown, and publish observable capacity/lag. Integration mistakes are often in traversal or lifecycle rather than the basic scan. Use a mature implementation whose API makes protected lifetimes hard to escape.

## Prerequisites and Retrieval

Retrieve:

- atomicity and linearization from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- publication from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- weak-memory proof obligations from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- progress quantifiers from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md);
- retirement sites from [Implementing a Lock-Free Stack](052-implementing-a-lock-free-stack.md) and [Lock-Free Queues](053-lock-free-queues.md); and
- pointer-generation distinctions from [ABA Problems and Tagged References](054-aba-problems-and-tagged-references.md).

Retrieval prompt: pause a reader immediately after loading a removable pointer; schedule unlink and attempted reclamation; then place hazard publication and validation in the only order that can make the first dereference safe.

## Learning Objectives

After completing this module, a learner can:

1. distinguish removal, retirement, reclamation, reuse, and destruction;
2. derive the publish-then-validate protection loop from the observation race;
3. state scanner and memory-order obligations without relying on hardware folklore;
4. calculate per-operation hazard-slot needs for linked traversals;
5. integrate exact-once retirement and deleter ownership with data-structure CAS;
6. explain reclamation thresholds, lag, batching, and bounded-memory conditions;
7. scope lock-free and wait-free claims across record acquisition, scans, allocation, and deletion;
8. specify participant registration, thread exit, cancellation, close, and domain shutdown;
9. design deterministic, sanitizer, weak-memory, stress, and operational evidence; and
10. choose among hazards, epochs/RCU, reference counting, garbage collection, quiescence, and locks.

## Core Exposition

### State and ownership model

Let atomic sources publish pointers to objects. Each object moves through `private → reachable → retired → reclaimed`. Construction is private. A successful data-structure update makes it reachable. Another successful update can unlink it, after which no new correct traversal should acquire it from the structure. Retirement transfers responsibility to the domain. Reclamation runs its deleter or makes storage reusable only after protection is absent.

The domain contains hazard records and retire lists. A record has one slot owner at a time; scanners read it concurrently. Null means no object protected. A retired entry contains address, deleter, and any domain metadata. The protected set `H` is the set of non-null addresses read from the relevant records during a scan.

Do not store ownership in the hazard slot. It announces a temporary possible dereference; it neither keeps an abstract element present nor transfers its payload. The successful data-structure operation still decides logical ownership. Multiple hazard slots may protect one object, and clearing one never authorizes deletion while another remains.

### Deriving publish then validate

The naive sequence `p = source.load(); use(*p)` has an interval where a remover can unlink and reclaim p. Publishing after the use is too late. Publishing before the initial load cannot name the unknown object. The repair is a validation loop:

1. load candidate p from source;
2. publish p into the owned hazard slot;
3. reload source with the required ordering;
4. if the reload differs, clear/replace the slot and retry;
5. if it matches, dereference p only while the slot remains p.

If removal linearizes before hazard publication, validation must observe that the source changed before allowing dereference. If validation establishes p before removal, a scanner must treat the published hazard as preventing reclamation. The memory model must rule out the bad combined execution in which reader validates old p while scanner misses the hazard and frees p.

For null, protection can usually remain null and the validated source observation may linearize an empty result according to the data structure. A spurious CAS or changed source triggers retry, not an unprotected use.

### Scanner reasoning

A remover unlinks node n before retiring it. A scan gathers hazard addresses, partitions a retire list into protected and unprotected entries, keeps the protected entries, and reclaims the rest. An address absent from a correct scan is reclaimable only if no reader can still validate and begin using it from a reachable source.

The two-sided proof couples reader validation with scanner observation. It is not enough to say “hazards use release and scans use acquire” in isolation. Identify the atomic source operations, hazard-slot modification order, unlink, retirement publication, and scan loads under the source language. Published algorithms or standard-library APIs may impose stronger fences than a local intuition expects.

A scan snapshot need not be simultaneous if the protocol proves safety for individually loaded slots. Conservative false protection merely delays reclamation. A false absence can free a live object. Accordingly, implementation optimizations may increase retention but must never turn uncertainty into deletion.

### Traversal and hazard budgets

Protecting a root is easy; traversing links is harder. A linked-list operation may need predecessor, current, and successor simultaneously: current remains protected while successor is loaded and protected, then the relevant link is revalidated before protection advances. Reusing current's slot for successor before the last current dereference opens a gap.

Count the maximum live pointer set along every control-flow edge, including helping, marked nodes, restart, exception cleanup, and comparisons. Fixed records make resource bounds explicit but can make a generic traversal unavailable when it needs more slots. Dynamically acquiring records can allocate, block, or fail and therefore changes progress and error semantics.

Pointers stored inside a protected immutable node are readable while that node lives, but following one to a separately reclaimable successor generally requires protecting the successor before the predecessor protection is surrendered. An API that returns a raw pointer beyond its holder's lifetime defeats the type-level boundary.

### Retirement and exact-once reclamation

Only the operation that wins logical removal transfers a node to retirement. Losing helpers and failed CAS attempts must not retire it again. If helpers can complete another operation's removal, the algorithm needs one exact retirement owner or an idempotent handoff protocol. Double retirement can execute a deleter twice; missing retirement leaks.

Batching amortizes scans. A common policy scans after a local retire list reaches a threshold proportional to the total hazard-slot count. If there are P participant records and K slots each, a scan reads roughly P·K slots. Choosing a threshold of similar order makes amortized scanning per retired node bounded in the simplified model.

The original hazard-pointer analysis gives bounded unreclaimed objects under stated participant, slot, threshold, and progress assumptions. A production bound must also cover unregistered retire queues, objects pending expensive deleters, domain sharding, stalled scans, and allocation beyond the domain. Record acquisition and deletion policy may not inherit the core method's progress.

### Memory ordering and object contents

Publishing a hazard announces lifetime; acquiring the original data-structure publication makes initialized fields visible. These can involve different synchronization edges. A protected object's mutable fields still need atomics, locks, immutability, or exclusive ownership. Lifetime protection is not a data-race waiver.

Slot clearing must not move before the final protected access. Compiler reordering matters just as hardware reordering does. Retirement publication and scan must retain the protocol's required order. Rather than selecting orders instruction by instruction from intuition, start from a reviewed implementation or formal proof and map every ordering to a named happens-before or modification-order obligation.

Sequential consistency can simplify an initial implementation but cannot repair missing validation, insufficient slots, double retirement, or use after clearing. Later relaxation requires model/litmus evidence and target testing, not only benchmarks.

### ABA relationship

Hazard pointers can prevent dangerous address reuse while a stale observation is protected: a retired object at address A cannot be reclaimed and reused as a later object while A appears in a hazard slot. Validation closes the pre-protection gap. This can make a data structure that is ABA-safe under garbage collection safe with explicit reclamation, as scoped by the algorithm.

They do not prevent every logical A→B→A state cycle. They also do not help an unprotected cached pointer or a pointer retained after clearing. Tagged state may still be required for history distinction, while hazards supply lifetime. Never infer one proof from the other.

### Progress and failure scope

Publishing and clearing a pre-owned slot are normally bounded atomic stores; protection may retry because the source changes. Michael's method supplies strong core progress properties under its assumptions. End-to-end claims must include record acquisition, retire-list allocation, scans, deleters, allocator behavior, target atomics, and domain coordination.

A delayed thread pins only the objects in its active slots, which is a major advantage over epoch-wide retention. It can still exhaust a scarce hazard-record pool, retain a critical resource, or delay synchronous destruction. Scans consume CPU proportional to records and can create latency spikes. Distribute or schedule reclamation only with a proof that retirement ownership and shutdown remain correct.

If a deleter locks, blocks on I/O, throws/panics, or re-enters the same structure, it can break latency, progress, and invariants. Separate the fact “safe to reclaim” from the policy “where and when destruction runs.”

### Registration and lifecycle

Participant records need a durable state machine such as `free → owned → released`. Acquisition must not let two writers share a slot. Thread-local caching improves speed but requires cleanup on normal exit and defined behavior for abnormal termination. Slots must be cleared before records return to the pool.

Cancellation before data-structure commitment clears protection and abandons private work. After successful removal, the node must still be retired exactly once even if cancellation arrives. Scope guards can encode these obligations. An exception or panic must not leak an active slot or skip ownership transfer.

Domain shutdown first closes new registration and new protected operations, then waits for all owned holders/operations to leave, completes retirement and scans, verifies all slots null, reclaims remaining eligible objects, and destroys domain metadata. A global process-lifetime domain has different destruction semantics from a per-component domain; document which applies.

### Operational policy and observability

Define maximum participants, slots per participant, acquisition failure, retire threshold, scan trigger, deleter context, synchronous reclamation option, shutdown deadline, and response to stuck holders. These are product semantics, not tuning trivia.

Monitor allocated/owned records, active non-null hazards, retire-list length and bytes, oldest retirement age, scan duration/frequency, objects protected per scan, reclamation count, deleter latency/failure, record-acquisition failures, retries, and shutdown drain time. Alert on assumptions, such as retirement growth beyond the derived bound, rather than only process memory.

Redact pointer values in logs. Addresses can expose layout and are rarely useful as stable identifiers. Use domain, participant, operation, and object-generation identifiers designed for telemetry.

### Verification strategy

Model the two decisive schedules: removal before publication, where validation must fail; and validation before removal, where scanning must defer. Add multiple hazards, slot reuse, traversal handoff, double retirement, scan interleavings, and exact-once deletion. Assert that no reclaimed object is accessed and every retired unprotected object is eventually eligible under fairness assumptions.

Use a test allocator that poisons and immediately recycles storage. Place deterministic barriers after source load, hazard store, validation, unlink, retirement, scan snapshot, slot clear, and before delete. Combine address/thread sanitizers where applicable, weak-memory model checking, randomized stress, and long pauses. Inspect generated atomics and lock-free support on each target.

No finite test proves safety. Evidence should state which schedules, language rules, targets, and lifecycle paths it covers. Prefer established libraries and preserve their holder types rather than wrapping them in raw-pointer convenience APIs.

## Definitions and Notation

- `S`: an atomic source/root from which a candidate is acquired.
- `HP[i,j]`: hazard slot j owned for writes by participant i.
- `H`: set of non-null addresses observed across relevant hazard slots during a scan.
- `Ret`: multiset/list of retired entries awaiting reclamation.
- `p`: candidate pointer loaded from S.
- `K`: maximum hazard slots per participant.
- `P`: number of visible participant records.
- `T`: retire threshold that triggers or schedules a scan.
- `protected(p)`: p appears in a live validated holder whose slot still equals p.
- `reachable(p)`: a correct new traversal can still acquire p from the data structure.
- `retired(p)`: p is no longer reachable and its one reclamation responsibility belongs to the domain.
- `reclaimable(p)`: p is retired and the protocol proves no valid access can occur.

The simplified scan cost is `O(P·K + |Ret|)`. This is not a latency guarantee: cache topology, inactive records, synchronization, deleters, and scheduling affect observed cost.

## Mechanisms, Invariants, or Proof Structure

### Protection safety cases

For a candidate p, removal either linearizes before the reader's validation or after it. If before, correct ordering makes validation observe that S no longer supplies p, so the reader does not dereference. If after, the validated hazard publication precedes any safe scan decision about p, and the scanner retains p. Clearing occurs after the final dereference. Therefore reclamation cannot precede a valid protected access, subject to the exact memory-model assumptions.

### Reclamation invariant

At each deletion, p was retired exactly once and is absent from all hazards that could authorize an access. Unlink prevents new protection from the data structure; validation rejects readers caught between load and publication; existing validated readers remain visible. Conservative scans may retain extra objects but cannot delete a protected one.

### Executable scan model

This sequential model demonstrates partitioning, not concurrent memory ordering. A and C retire while A is protected; the first scan reclaims only C. Clearing A makes it reclaimable on the second scan. Exact output records retained and reclaimed sets.

<!-- bijux-verify: {"id":"hazard-retire-scan-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scan1_reclaimed=['C']\nscan1_retained=['A']\nscan2_reclaimed=['A']\nretired_remaining=[]\nreclaimed_once=['A', 'C']\n","stderr":""}} -->
```python
hazards = {"reader-1": "A", "reader-2": None}
retired = ["A", "C"]
reclaimed = []

def scan():
    protected = {value for value in hazards.values() if value is not None}
    safe = [node for node in retired if node not in protected]
    retained = [node for node in retired if node in protected]
    for node in safe:
        if node in reclaimed:
            raise AssertionError("double reclamation")
        reclaimed.append(node)
    retired[:] = retained
    return safe, retained

safe1, kept1 = scan()
hazards["reader-1"] = None
safe2, _ = scan()
print(f"scan1_reclaimed={safe1}")
print(f"scan1_retained={kept1}")
print(f"scan2_reclaimed={safe2}")
print(f"retired_remaining={retired}")
print(f"reclaimed_once={sorted(reclaimed)}")
```

### Audit obligations

1. Map every dereference to a live holder and slot.
2. Map every protection to source validation and required ordering.
3. Map every successful unlink to one retirement owner.
4. Prove scanners cannot miss a protection that validation accepted.
5. Prove slot handoff covers simultaneously live nodes.
6. Qualify allocation, record acquisition, scan, and deleter progress.
7. Prove exit, cancellation, exception, close, and destruction cleanup.
8. Measure capacity and lag assumptions used by the bound.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation |
|---|---|---|
| Hazard pointers | fine-grained, stalled reader pins bounded named objects | per-object publication/validation and scanning |
| Epoch/RCU | very cheap grouped read-side protection | stalled reader can retain all later retirement |
| Atomic shared ownership | familiar lifetime handle | reference acquisition/update traffic and algorithm-specific race |
| Tracing garbage collection | automatic reachable-object lifetime | runtime dependency; pauses; logical ABA remains |
| Quiescent batch deletion | simple for bounded phases | memory retained until global phase boundary |
| Never reclaim | simplest short-run reasoning | unbounded/retained memory; shutdown burden |
| Mutex/shared lock | straightforward lifetime serialization | blocking and contention; often best absent nonblocking need |
| Immutable copy-and-swap | simple reader contents | copy/publication cost; old versions still need reclamation |

Hazards are attractive when reads greatly outnumber writes, threads may block while holding individual objects, and a bounded set of nodes can be named. Epochs can be better for short traversals protecting many nodes. A mutex or managed handle is often the production choice when simplicity outweighs measured contention.

## Failure Modes and Misconceptions

- **“Loaded means protected.”** Removal can occur between load and hazard publication.
- **“Published means protected.”** Validation is required to close the pre-publication race.
- **“Protected root means protected graph.”** Separately reclaimable successors need safe handoff.
- **“Retired means unreachable to every reader.”** Existing protected readers may still access it.
- **“Unprotected in one slot means safe.”** Every relevant participant and slot must be considered.
- **“Hazards synchronize payload mutation.”** They extend lifetime, not mutual exclusion.
- **“Acquire/release labels are a proof.”** The full source/slot/retire/scan execution must forbid false absence.
- **“A failed CAS keeps protection useful.”** Links derived from the old snapshot may require complete refresh.
- **“One slot is always enough.”** Traversal, helping, and comparison can require several simultaneous nodes.
- **“Thread-local retire lists disappear safely.”** Exit must transfer or drain them under domain rules.
- **“Scanning immediately is optimal.”** It can make every update pay O(PK); batching changes time/space balance.
- **“A stalled holder is free.”** It retains named resources and perhaps scarce records indefinitely.
- **“The paper's progress covers my deleter.”** Allocation, logging, locks, callbacks, and destruction are separate.
- **“Domain destruction is ordinary delete.”** It requires admission closure and global holder/reclaimer quiescence.
- **“Hazards certify the data structure.”** Linearizability, ABA, ordering, ownership, and API semantics remain.

## Worked Examples

### Example 1

**Removal before publication.**

**Situation.** R loads A, pauses; W replaces root with B, retires and scans A; then R publishes A.

**Reasoning.** R did not yet establish protection, so W may reclaim A. R must reload root before dereferencing. It sees B, clears/replaces A, and retries. Publishing A after reclamation does not revive it, but validation prevents access.

**Conclusion.** Publication without subsequent validation is insufficient.

### Example 2

**Publication before removal.**

**Situation.** R loads A, publishes A, reloads root A, then W replaces root and retires A.

**Reasoning.** R's validated window is live. W's scan includes A in H and retains it. After R's final access, R clears its slot; a later scan can reclaim A.

**Conclusion.** A validated hazard turns concurrent removal into deferred physical reclamation.

### Example 3

**Two readers, one object.**

**Situation.** R1 and R2 both protect A. R1 clears; the scanner runs while R2 continues.

**Reasoning.** H still contains A from R2, so reclamation is forbidden. Hazards do not count owners; set membership across all slots is enough. Only after R2 clears may a later correct scan reclaim.

**Conclusion.** Clearing one holder never implies global absence.

### Example 4

**List hand-over-hand protection.**

**Situation.** Traversal protects current A and wants successor B. It overwrites its only slot with B before its last read from A.

**Reasoning.** A becomes reclaimable during that final read. Use a second slot: protect A, load B, publish B, validate `A.next`, finish every A access, then clear/reuse A's slot. If links can change, restart on failed validation.

**Conclusion.** Slot budget follows simultaneously live dereferences, not pointer variable count.

### Example 5

**Exact-once retirement with helpers.**

**Situation.** P marks node N logically deleted; helper Q wins the physical unlink. Both call retire.

**Reasoning.** The domain can execute N's deleter twice. Define physical-unlink winner as retirement owner, or publish a one-time retirement handoff whose transition is itself proven. Logical marking alone must not give both callers ownership.

**Conclusion.** Helping requires explicit retirement ownership.

### Example 6

**Scan threshold arithmetic.**

**Situation.** A domain exposes 64 records with two slots each and scans a local list at 256 retirees.

**Reasoning.** One scan reads 128 slots and partitions 256 entries, a simplified 384 units of work. Spread over 256 retirees, that is 1.5 units per retirement, excluding caches, synchronization, and deleters. Scanning each retirement would repeatedly read all 128 slots.

**Conclusion.** Thresholds amortize scan cost but increase temporary retention.

### Example 7

**Payload race despite safe lifetime.**

**Situation.** R protects configuration A while W mutates `A.limit` non-atomically in place.

**Reasoning.** Hazard protection prevents deletion, not concurrent data races. Publish immutable replacement B, or synchronize `limit` with a lock/atomic and prove its semantics. The holder alone does not make the read valid.

**Conclusion.** Lifetime safety and content synchronization are orthogonal.

### Example 8

**Cancellation after unlink.**

**Situation.** A pop wins head CAS, then observes cancellation before calling retire on the old head.

**Reasoning.** Logical ownership already transferred. Returning cancelled and skipping retire leaks the node; deleting immediately risks readers. A scope guard transfers the old head to the domain exactly once, while the API reports committed success or a documented committed-with-cancellation state.

**Conclusion.** Cancellation cannot abandon post-linearization reclamation duty.

### Example 9

**Stalled participant comparison.**

**Situation.** One thread blocks for an hour protecting A while a million other nodes retire.

**Reasoning.** A correct fine-grained hazard scheme pins A (and any other active slots), not necessarily the million unrelated nodes; scans can reclaim those. The stalled thread still holds a record and A's resources. An epoch scheme could retain the whole post-entry retired population.

**Conclusion.** Hazard pointers localize retention, but do not make stalled holders costless.

### Example 10

**Aircraft routing-table reclamation.**

**Situation.** Flight-control readers use a hazard-protected routing table while an updater publishes a replacement and retires the old table. May a green stress test authorize deployment?

**Reasoning.** No. Evidence must cover immutable table contents, acquire/release publication, protect/validate ordering on every target, fixed holder capacity, worst-case reader pause, exact-once retire, deleter execution context, memory bounds, degraded behavior, startup/shutdown, and fault injection. Named avionics, real-time, compiler/architecture, formal-methods, operations, and certification reviewers must approve requirements and evidence. The chapter supplies no timing analysis or certification.

**Conclusion.** Hazard reclamation is one reviewed subsystem within an end-to-end safety case.

## Cross-Program Connections

- **Programming languages:** unsafe pointer validity and happens-before rules determine whether the abstract protection proof maps to source.
- **Data structures:** traversal topology determines slot budget and retirement ownership.
- **Operating systems:** schedulers, thread exit, allocators, and signals shape progress and lifecycle.
- **Distributed systems:** hazard announcements resemble leases only superficially; shared-memory scans have different failure and authority models.
- **Databases:** snapshot visibility and vacuum similarly separate logical removal from later physical reclamation.
- **Security:** address logging, attacker-forced retention, and deleter callbacks expand the threat surface.
- **Performance engineering:** scan thresholds exchange update work for retained bytes and tail latency.
- **Safety engineering:** bounded holders, memory, and timing are assumptions requiring monitored human approval.

## References

1. Maged M. Michael, “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects,” *IEEE TPDS* 15(6), 2004. <https://doi.org/10.1109/TPDS.2004.8>
2. Trevor Brown, “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way,” PODC 2015. <https://doi.org/10.1145/2767386.2767436>
3. Maged M. Michael, “Safe Memory Reclamation for Dynamic Lock-Free Objects Using Atomic Reads and Writes,” PODC 2002. <https://doi.org/10.1145/571825.571829>
4. ISO C++ working draft, “Safe reclamation” and “Hazard pointers,” continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/saferecl>
5. WG21 P2530R3, “Hazard Pointers for C++26,” 2023. <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2530r3.pdf>
6. Meta, Folly hazard-pointer implementation documentation, retrieved 2026-08-29. <https://github.com/facebook/folly/blob/main/folly/docs/Hazptr.md>
7. Paul E. McKenney, *Is Parallel Programming Hard, And, If So, What Can You Do About It?*, current perfbook. <https://kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html>
8. Keir Fraser, *Practical Lock-Freedom*, University of Cambridge Technical Report UCAM-CL-TR-579, 2004. <https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf>
9. ISO C++ working draft, atomic ordering and compare-exchange clauses, continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/atomics>
10. Rust Project, Rustonomicon chapter “Atomics,” retrieved 2026-08-29. <https://doc.rust-lang.org/nomicon/atomics.html>

## Exercises

### Exercise 1

Why must a reader validate the atomic source after publishing a candidate hazard? Give the decisive schedule.

### Exercise 2

A traversal needs predecessor P while reading current C, then must protect successor S before validating `C.next`, and may compare P and C during unlink. Determine the minimum simultaneous hazard budget and justify it.

### Exercise 3

Diagnose an implementation that unlinks N, appends it to a thread-local retire list, scans only that thread's hazard slots, and exits without transferring the list. Give a corrected domain-level design.

### Exercise 4

Select a reclamation approach for a read-mostly service configuration where readers may block for minutes, updates occur hourly, objects are large, and no nonblocking requirement exists. Compare hazards, epochs, shared ownership, and a mutex.

### Exercise 5

A surgical robot uses hazard-protected immutable calibration objects. Design a review for update, cancellation, process restart, bounded memory, and shutdown. Separate automated evidence from required human review.

## Answers to the Exercises

### Answer 1

Between initial load and hazard publication, a remover can unlink, retire, scan, and reclaim the candidate. Publishing afterward cannot restore lifetime. The reader must reload the source; if removal happened first, it observes a different pointer and performs no dereference. If validation succeeds before removal, the scanner must observe the hazard and defer. The proof also needs source-language ordering to rule out validation of old state combined with scanner false absence.

### Answer 2

Three slots are required at the peak: P remains live for possible unlink comparison, C remains live while its link and metadata are read, and S must be announced before `C.next` is validated. After validation and the final C/P accesses, one slot may be released or rotated. Two slots suffice only if the algorithm is redesigned so P is no longer dereferenced or compared while C and S are simultaneously live; that must be proven on every branch including retry/helping.

### Answer 3

Scanning only local slots can miss another participant protecting N and free it. Exiting with the retire list leaks its exact-once responsibility. A domain exposes every relevant record to scanners; publishes retirement according to the protocol; scans all records with required ordering; retains protected entries; and reclaims only absent ones. Thread exit clears owned slots, releases records, and transfers or drains its retire list into a domain-owned queue. Shutdown closes registration and waits for holders/scans before final drain.

### Answer 4

Use immutable objects behind atomic shared ownership or a mutex-protected shared handle unless measurements reject them. Updates are rare and no nonblocking guarantee exists, so simpler lifetime semantics dominate. A reader-held shared handle supports minute-long use while old large objects are reclaimed when the last reader releases; atomic acquisition cost should be measured. A mutex/read-lock can also work but holding it for minutes blocks update, so copy the handle under a short lock. Epochs risk retaining every later object behind a stalled reader, though hourly updates limit count; hazards can pin only named versions but add unnecessary domain complexity. Verify ownership, publication, update failure, destructor context, and shutdown.

### Answer 5

Publish a fully validated immutable calibration with release semantics and protect/acquire it through a reviewed holder. Bind every operation to calibration identity; cancellation before publication discards the private version, while after exchange the old object is retired exactly once and the update is reported committed. Restart establishes domain quiescence or a persisted/versioned handoff; shutdown closes operations, drains holders/retirement, and verifies bounded records and bytes. Automated evidence includes deterministic protect/remove schedules, forced reuse, sanitizers, weak-memory/model tests, power-cycle and cancellation tests, capacity exhaustion, target atomic inspection, and latency/memory monitoring. Named robotics, clinical, controls, real-time, compiler/architecture, cybersecurity, operations, and regulatory reviewers must approve hazards, calibration validity, timing, fallback, deployment targets, and residual risk. The chapter does not certify surgery or calibration.
