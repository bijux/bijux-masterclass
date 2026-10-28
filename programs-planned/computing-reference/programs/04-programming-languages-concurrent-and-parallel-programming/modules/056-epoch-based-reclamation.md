---
module_id: CONPAR-056
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 56
title: Epoch-Based Reclamation
status: complete
last_verified: 2026-08-29
---

# Epoch-Based Reclamation

## One-Page Review

### Governing question

How can operations announce coarse-grained participation epochs so removed objects are reclaimed after every possibly stale participant becomes quiescent, without hiding unbounded retention, destructor, progress, or lifecycle risks?

### Essential definitions

- **Epoch-based reclamation (EBR)** defers reclamation according to participant epochs rather than naming each protected object.
- A participant is **pinned** or **active** while it may retain pointers acquired from the protected structure; it is **quiescent** when it retains none across the boundary.
- The **global epoch** is a shared generation used to classify current participation and retirement.
- A **local epoch** records the global epoch observed when a participant entered or refreshed its protected region.
- A **retire bag** contains unreachable objects tagged or grouped by retirement epoch.
- **epoch advancement** changes the global epoch only after the implementation establishes its participant condition.
- A **grace period** for a retirement ends when every participant that could have held an older reference has passed through a quiescent state.
- **deferred destruction** schedules a deleter only after safety; it does not guarantee prompt execution or execution on the retiring thread.
- **reclamation debt** is the count, bytes, or resource value retired but not destroyed.
- **quiescent-state-based reclamation (QSBR)** is a related scheme in which participants explicitly report quiescent progress; exact APIs and assumptions differ from EBR.

### Central model, mechanism, or theorem

An operation pins before loading reclaimable pointers, records an epoch, and unpins only after its last possible use. Successful removers retire nodes into the current epoch. The global epoch advances only when every registered active participant has acknowledged the required current epoch or is quiescent. Once enough epoch transitions establish that no participant capable of retaining a retirement-epoch pointer remains active, that retirement bag is safe to reclaim. A three-bag implementation often reclaims objects two global advances behind, but the number is an implementation theorem, not universal magic.

### Critical invariants

No protected pointer escapes its guard or crosses quiescence. Pin publication precedes protected loads; unpin follows the final access. Unlink precedes exact-once retirement. An epoch advances only under the implementation's complete participant test. Wrap cannot make an old local epoch appear current. Reclamation occurs only for a bag whose possible observers all passed quiescence. Registration, deregistration, nesting, migration, cancellation, panic/exception, and thread exit preserve active state. Deferred callbacks own valid data and may run elsewhere. Shutdown closes admission, waits for all guards, flushes local bags, advances/drains safely, then destroys the collector.

### Common failures

Code pins after loading; returns a borrowed pointer beyond the guard; blocks indefinitely while pinned; awaits/yields across an undocumented guard; treats a pinned flag and epoch loaded separately without a protocol; ignores nested pins; advances while a participant record is missed; uses small wrapping epochs without modular proof; retires before unlink; retires twice; leaves garbage in thread-local bags at exit; runs thread-affine destructors remotely; assumes `flush` means immediate destruction; destroys a collector while guards survive; or calls the data structure lock-free while a stalled participant can cause unbounded memory exhaustion.

### Compact example

R pins in epoch 0 and reads A. W unlinks and retires A in epoch 0. The global epoch can move to 1 after all active participants are consistent with epoch 0, but R still might hold A, so A is not reclaimed. R unpins. After the next valid advance to 2, no participant from epoch 0 can still hold A, and its bag becomes eligible. If R never unpins, advancement or eligibility stalls and retirement debt can grow.

### Connections

[Hazard Pointers](055-hazard-pointers.md) protects named objects and localizes stalled retention. [ABA Problems and Tagged References](054-aba-problems-and-tagged-references.md) explains how delayed reuse can prevent pointer ABA. The next module treats read-copy-update as a broader publication and grace-period pattern.

## Governing Question

How should an engineer derive, integrate, validate, and operate epoch-based reclamation so cheap read-side protection does not turn one delayed participant into invisible memory, resource, or shutdown failure?

EBR's elegance comes from protecting a whole operation with one participation announcement. Its central liability is equally structural: reclamation depends on collective quiescent progress.

## Why This Matters

Lock-free structures can unlink a node while another thread still holds a raw pointer. Epoch protection avoids publishing every individual pointer: a participant announces that it may hold any object reachable during a protected region, and removers defer destruction until older participants leave. This often makes read/traversal paths cheaper and simpler than hazard-pointer hand-over-hand protection.

The trade is coarse retention. One thread paused in an old epoch can prevent a large stream of unrelated retired nodes from becoming safe. Logical operations may keep completing while memory grows until the process swaps, hits a limit, blocks in allocation, or terminates. “Lock-free algorithm” is therefore not the same as bounded or survivable service.

EBR appears in Rust concurrent collections, database/index engines, allocators, and research libraries. RCU and QSBR share grace-period reasoning but expose different read-side, scheduling, and callback contracts. Production work must follow the exact collector, language, and target rather than importing a generic three-epoch story.

## Prerequisites and Retrieval

Retrieve:

- safety and progress distinctions from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- publication order from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- weak-memory analysis from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- nonblocking progress scope from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md);
- concrete retirement sites from [Implementing a Lock-Free Stack](052-implementing-a-lock-free-stack.md) and [Lock-Free Queues](053-lock-free-queues.md); and
- fine-grained comparison from [Hazard Pointers](055-hazard-pointers.md).

Retrieval prompt: pause one participant after it pins and loads a node, retire that node plus many unrelated nodes, and identify which fact must become true before any retirement from the old epoch can be deleted.

## Learning Objectives

After completing this module, a learner can:

1. distinguish pinning, epoch observation, quiescence, retirement, eligibility, and destruction;
2. derive the grace-period argument for a three-bag epoch scheme;
3. state why two epoch advances may be sufficient only under named implementation assumptions;
4. identify guard escape, nesting, async suspension, registration, and thread-exit hazards;
5. quantify reclamation debt under a stalled participant and workload rate;
6. scope safety, lock-free progress, bounded memory, and prompt destruction separately;
7. integrate cancellation, callbacks, collector ownership, and shutdown;
8. compare EBR with hazards, RCU/QSBR, reference ownership, tracing GC, and locks;
9. build deterministic, weak-memory, sanitizer, stress, and operational evidence; and
10. design safe policies for high-stakes or resource-constrained deployment.

## Core Exposition

### Object and participant states

An object transitions `private → reachable → retired(e) → reclaimable → reclaimed`. Only a successful structural update makes it reachable or removes it. Retirement labels or enqueues an unreachable object under epoch e; it transfers exactly one deferred-destruction responsibility. Reclaimable means the collector has proved absence of possible old readers, not simply that time passed.

A participant record transitions between quiescent and active. On entry, it announces an epoch in a way scanners/advancers can observe. While active, every protected pointer and borrowed reference must remain within the guard's lifetime. Exit drops those borrows before publishing quiescence. The source language's lifetime types can help enforce this boundary, but unsafe escape can violate it.

Global, local, and retirement epochs are logical generations. Implementations may encode active bits and epochs together in one word, use modular arithmetic, distribute scanning, or rotate bags. Review the implementation invariant rather than treating field names as semantics.

### Enter before acquisition

The operation must pin before loading a pointer that another thread can unlink and retire. Loading first creates the same observation gap seen with hazards: a remover can complete a grace period and reclaim before the reader announces itself. Pinning must become visible according to the collector protocol before protected loads are accepted.

Once pinned, a guard commonly permits several loads and traversals without per-pointer announcements. This is the primary performance benefit. It also broadens responsibility: every pointer derived from the protected structure must die before unpin. Returning a raw pointer, storing it in a longer-lived object, or scheduling a callback with it violates the proof even if the guard variable leaves scope correctly.

Nested entry needs defined semantics. A counter or nested guard can keep the participant active until the outermost exit; blindly unpinning on an inner guard's destruction opens a premature quiescent state. Thread migration or task scheduling matters when participant records are thread-local.

### Retirement after removal

A node is retired only after it is unreachable to new correct operations. Retiring first lets the collector eventually delete a still-published object. The winner/helper that performs the algorithm's removal must transfer retirement exactly once. Failed CAS attempts retire nothing.

Retire entries may sit in local bags before publication to a global collector. Batching improves locality and amortizes coordination, but local storage becomes part of the bound and exit protocol. A thread that exits must flush or transfer its bags; a short-lived workload may otherwise finish before callbacks run.

The deleter may run on another participant and much later. Captures must be valid and sendable under the library contract. Thread-affine handles, locks, exceptions, panics, I/O, or re-entry can make “safe to invoke” different from “safe to execute here.” Separate memory eligibility from destruction scheduling.

### Three-epoch reasoning

Consider epochs modulo at least three with retire bags labeled by current global epoch. A participant entering global epoch e announces e. An advancer may move from e to e+1 only after every active participant is observed in e (or quiescent), under a consistent protocol. Participants in earlier epochs therefore prevent advancement.

An object retired in e could be held by a participant active in e. The first advance to e+1 establishes that active participants seen for that decision were caught up to e, but those participants may still hold the object. For a second advance to e+2, they must either quiesce and later repin, or update/republish according to the implementation; after that boundary, no participant capable of retaining an e-era pointer remains. The e bag is eligible.

This is a proof sketch for a common design, not a license to reclaim on any integer difference of two. Precise advancement scans, memory orders, local refreshing, wrap comparison, bag publication, and participant registration decide whether the reasoning holds. Crossbeam documents deferred destruction after currently pinned participants unpin and uses guarded pointer lifetimes; follow its actual release, not a hand-built imitation.

### Grace periods and related schemes

A grace period separates removal from all preexisting read-side critical sections. EBR approximates this with epoch announcements. QSBR asks participants to report quiescent states and works well when loops naturally pass through them. RCU supplies a family of mechanisms with environment-specific rules about read-side blocking, preemption, callbacks, and synchronization.

The abstractions are related, not identical. User-space QSBR can stall forever if a registered thread stops reporting. Kernel RCU flavors integrate scheduler knowledge. C++ safe-reclamation RCU defines domain regions and deferred evaluations. Never transfer a claim about one flavor's blocking or progress to another without its specification.

### Reclamation debt and bounds

Suppose retirement occurs at rate λ objects per second, average retained size s bytes, and an old participant prevents eligibility for duration D. A lower-order estimate of extra debt is `λ·D` objects and `λ·D·s` bytes, plus batching and baseline bags. At 50,000 nodes/s, 128 bytes/node, and 60 seconds, that is 3,000,000 nodes or 384,000,000 bytes before allocator overhead.

If D is unbounded because a thread can pause, block, crash, or await indefinitely while active, classical EBR gives no finite debt bound. Brown highlights this vulnerability and develops variants with different signaling/neutralization assumptions. Operational timeouts cannot simply declare a paused pointer dead; reclaiming behind a live reader creates use-after-free.

Bounded products need one of: a proven bound on active-region duration; admission/backpressure on retirement or memory; neutralization/recovery supported by the environment; a hybrid/fine-grained scheme; or a failure policy such as process restart after establishing that stale address-space readers cannot resume. Each changes availability and correctness assumptions.

### Memory ordering

Entry publication, global-epoch load, protected pointer loads, removal, retirement publication, advancement scans, and exit announcement form one source-language proof. An active bit and local epoch stored separately can expose an incoherent state unless the algorithm validates it. Relaxed atomics may be correct only inside a reviewed protocol with fences.

The data structure still needs publication ordering for object contents. Epoch protection supplies lifetime, not visibility of initialization or synchronization for mutable payloads. Likewise, sequential consistency cannot repair a pointer that escapes its guard or a missing participant record.

Epoch wrap needs modular reasoning. Equality of a small counter after many advances must not make an ancient participant appear current or an old bag eligible. Practical word widths may provide enormous margin, but the proof must include maximum active duration, advance rate, restart/reset behavior, and comparison method.

### Progress and latency

Pin/unpin paths can be fast and bounded in mature implementations. An operation's data-structure kernel can remain lock-free even if a stalled peer blocks epoch advancement. Yet reclamation liveness and memory boundedness fail, and eventual allocation can block logical operations. State the surface: logical update progress, collector advancement, callback execution, allocator progress, and service survival.

Advancement scans participant records and may produce cache traffic. Batched destruction can cause latency spikes and allocator contention; recent work studies harmful interactions between batch freeing and allocators. Distributing collection smooths work but complicates ownership and shutdown.

Unpin frequently enough to allow progress but not so frequently that entry/exit overhead dominates. Never split a logically protected traversal merely to satisfy a timer unless pointers are reacquired and state revalidated at the boundary.

### Async, cancellation, and failure

Holding an epoch guard across an `await`, blocking call, or callback can stall reclamation for an unbounded duration. Some language libraries make guards non-sendable or tie them to a thread; circumventing that restriction is dangerous. Copy needed immutable data or redesign so suspension happens outside the protected region.

Cancellation before a structural commit can drop the guard and private work. After unlink, exact-once retirement remains mandatory. Scope guards must order payload ownership, retirement, and unpin correctly during exception or panic unwinding. Deferred callbacks must define panic/failure behavior so one bad deleter does not corrupt collector accounting.

Participant death is environment-specific. Thread-local destructors may deregister normal exits, but process termination, forced cancellation, signal handling, or foreign runtimes may bypass them. Do not promise recovery without an implemented neutralization or containment mechanism.

### Collector ownership and shutdown

A global collector can simplify sharing but make component teardown and tests nondeterministic. A per-instance collector improves ownership but requires every pointer/guard/retirement to use the same domain. Mixing domains can reclaim while an unobserved participant still holds a pointer.

Order shutdown: close new operations and registration; cancel/drain work without abandoning committed retirements; wait for all guards/participants to quiesce; flush local bags; perform the implementation's safe advancement/collection; run or transfer callbacks; verify debt is zero or explicitly owned; then destroy data structure and collector. A timeout requires a containment policy, not unsafe forced reclamation.

### Verification and observability

Model participants, active flags, local/global epochs, reachable/retired bags, guards, and deletion. Force entry-versus-removal, advancement scans, nested pins, missed records, wrap, local-bag exit, and stuck participants. Assert no access after reclaim, no early eligibility, exact-once destruction, and conditional eventual eligibility.

Use deterministic barriers around pin publication, epoch observation, protected load, unlink, retire, flush, advance, unpin, and callback. Poison/recycle memory, run sanitizers and weak-memory tools, inspect target atomics, and stress pause/cancel/exit/shutdown. Tests that merely call `flush` and sleep are not proof of callback completion.

Monitor registered and active participants, oldest active duration and epoch, global advance rate, local/global retire objects and bytes, oldest retirement, callbacks queued/executed/failed, collection duration, allocation pressure, pin nesting, long guards, and shutdown drain. Tie alerts to the derived memory budget.

## Definitions and Notation

- `G`: current global epoch.
- `L_i`: local epoch announced by participant i.
- `active_i`: whether participant i may retain protected pointers.
- `B_e`: retirement bag for epoch e.
- `Q_i`: a quiescent state of participant i.
- `retire(x,e)`: x becomes unreachable and is placed under epoch e.
- `eligible(x)`: the collector has proved every possible observer of x passed quiescence.
- `λ`: retirement rate in objects per second.
- `s`: average retained bytes per object.
- `D`: duration for which an old active participant blocks eligibility.
- **epoch lag**: modular/logical distance between a retirement epoch and current G under the implementation's comparison rules.

The estimate `debt_objects≈λD` and `debt_bytes≈λDs` describes steady retirement during one stall, not a universal bound. Add existing bags, bursts, allocator metadata, callbacks, and objects not governed by the collector.

## Mechanisms, Invariants, or Proof Structure

### Safety argument

Let x be retired after unlink in epoch e. Any reader that could have loaded x entered protection before or during its reachability and must remain active until its final use. Reclamation waits through the implementation's required advances. Those advances can occur only after every such participant reports a sufficiently new epoch or quiescence. A participant that repins after quiescence cannot newly acquire unreachable x. Therefore no valid reader retains x when its bag is reclaimed, assuming complete registration, correct ordering, no guard escape, exact retirement, and wrap-safe epochs.

### Stalled-participant counterargument

If participant R remains active in e, it may retain any e-reachable pointer. The collector cannot distinguish which object without finer-grained metadata. Reclaiming any potentially observed e retirement is unsafe. If others retire indefinitely, debt grows indefinitely. Logical lock-free completions do not contradict this reclamation-liveness failure.

### Executable epoch model

The model records one reader pinned in epoch 0. The first advance to 1 is allowed, but the reader prevents the next. After it unpins, the global epoch reaches 2 and epoch-0 A becomes eligible. B retired in epoch 1 becomes eligible after the next advance. This is sequential evidence for bag arithmetic, not concurrent EBR.

<!-- bijux-verify: {"id":"epoch-advance-and-debt-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"advance_to_1=True\nadvance_while_old_active=False\ndebt_before_quiescence=['A', 'B']\nadvance_to_2=True\nreclaimed_at_2=['A']\nadvance_to_3=True\nreclaimed_at_3=['B']\nremaining=[]\n","stderr":""}} -->
```python
global_epoch = 0
participants = {"reader": {"active": True, "epoch": 0}}
retired = [("A", 0)]

def try_advance():
    global global_epoch
    if all(not p["active"] or p["epoch"] == global_epoch for p in participants.values()):
        global_epoch += 1
        return True
    return False

def collect():
    safe = [name for name, epoch in retired if global_epoch - epoch >= 2]
    retired[:] = [(name, epoch) for name, epoch in retired if global_epoch - epoch < 2]
    return safe

first = try_advance()
retired.append(("B", 1))
blocked = try_advance()
debt = [name for name, _ in retired]
participants["reader"]["active"] = False
second = try_advance()
at_two = collect()
third = try_advance()
at_three = collect()
print(f"advance_to_1={first}")
print(f"advance_while_old_active={blocked}")
print(f"debt_before_quiescence={debt}")
print(f"advance_to_2={second}")
print(f"reclaimed_at_2={at_two}")
print(f"advance_to_3={third}")
print(f"reclaimed_at_3={at_three}")
print(f"remaining={retired}")
```

### Review obligations

1. Identify every protected acquisition and prove pin precedes it.
2. Prove no pointer/borrow outlives the guard or crosses quiescence.
3. Map every successful unlink to exactly one retirement.
4. Audit the exact advancement and modular-wrap algorithm.
5. Include every participant, local bag, and domain in exit/shutdown.
6. Qualify callbacks, allocation, registration, and collection progress.
7. Derive and monitor debt under worst active-region duration.
8. Test cancellation, panic, blocking, migration, restart, and target ordering.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation |
|---|---|---|
| EBR | cheap coarse protected operations and traversals | one old participant can retain unrelated debt |
| Hazard pointers | stalled reader pins only named objects | per-pointer publication, validation, slot planning, scans |
| RCU/QSBR | mature grace-period families for read-mostly use | flavor-specific scheduling/quiescence contracts |
| Atomic shared ownership | direct lifetime handle | reference traffic and acquisition contention |
| Tracing GC | automatic reachability lifetime | runtime/collector behavior; logical ABA remains |
| Quiescent phase/batch | simple bounded-job reclamation | global boundary and peak retention |
| Mutex/reader lock | direct serialization and familiar teardown | blocking; long readers can block updates |
| Hybrid/neutralization | can bound or recover stalled debt | platform signals/recovery and more proof surface |

Use EBR when protected regions are short and enforceable, traversals touch many nodes, participant lifecycle is controlled, and debt has explicit admission and monitoring. Prefer hazards when readers may block while holding a small number of nodes. Prefer a lock or managed handle when no nonblocking requirement justifies manual reclamation.

## Failure Modes and Misconceptions

- **“Pinned after load is close enough.”** Reclamation can occur in the gap.
- **“A guard protects pointers forever.”** Protection ends at quiescence; escape violates the contract.
- **“Two advances are universally safe.”** That follows only from a particular advancement/bag invariant.
- **“Current epoch means current data.”** Epochs govern possible stale references, not business freshness.
- **“Flush means destroy now.”** It may only publish work and attempt collection.
- **“One stalled thread pins one object.”** Coarse EBR can retain every later retirement.
- **“Lock-free means memory-bounded.”** Logical progress can coexist with unbounded debt.
- **“A timeout makes reclamation safe.”** Time does not invalidate a live pointer.
- **“Thread exit automatically handles bags.”** Only a specified deregistration/transfer path does.
- **“Async suspension is harmless.”** A guard across await can stall the collector and violate thread affinity.
- **“Epochs synchronize fields.”** They protect lifetime, not mutable payload access.
- **“Wide counters remove wrap proof.”** Width reduces frequency; lifecycle and comparison still matter.
- **“Callbacks run on the retiring thread.”** Deferred execution context may differ.
- **“RCU, QSBR, and EBR are synonyms.”** They have related grace-period ideas but distinct contracts.
- **“Collector drop frees everything safely.”** It must first establish domain-wide quiescence and ownership.

## Worked Examples

### Example 1

**Pin after load.**

**Situation.** R loads A, W unlinks/retires A and completes the needed grace period, then R pins and dereferences A.

**Reasoning.** R was invisible during the grace period, so reclamation was legal. Pinning afterward cannot revive A. R must enter protection before loading from the reclaimable structure.

**Conclusion.** Entry ordering is a lifetime precondition, not an optimization.

### Example 2

**Two advances.**

**Situation.** A retires in epoch 4 while R is active in 4. Global moves to 5; R then quiesces and later repins in 5; global moves to 6.

**Reasoning.** R could hold A until its quiescence between advances. After repinning it cannot newly acquire unreachable A. Under the stated three-bag advancement rule, the epoch-4 bag is eligible at 6.

**Conclusion.** Eligibility follows quiescent passage, with epoch distance serving as the implementation witness.

### Example 3

**Guard escape.**

**Situation.** A function pins, loads pointer P, stores raw P in a global cache, and returns, dropping the guard.

**Reasoning.** The participant announces quiescence while the cache can still dereference P. Later reclamation is correct according to collector metadata but unsafe for the program. Return owned/copy data or an API handle whose lifetime keeps protection.

**Conclusion.** Collector correctness cannot compensate for escaped borrows.

### Example 4

**Nested pin.**

**Situation.** Outer code pins; a helper pins again and then unpins by clearing the one active bit; outer code continues using P.

**Reasoning.** The inner exit falsely announces quiescence. Use a nesting-aware guard/count, or an API where inner guards share the outer protection and only the outermost drop unpins.

**Conclusion.** Nesting semantics belong to the participant state machine.

### Example 5

**Debt calculation.**

**Situation.** One participant stalls for 60 seconds while 50,000 nodes/s of 128 bytes retire.

**Reasoning.** The simplified debt is 3,000,000 nodes and 384,000,000 bytes, before allocator metadata and baseline bags. If the participant can stall forever, there is no finite version of this bound.

**Conclusion.** Active-region duration is a capacity assumption that must be enforced or mitigated.

### Example 6

**Async guard.**

**Situation.** A request pins, reads a node, then awaits a remote service for an unbounded time while retaining the guard.

**Reasoning.** Reclamation can stall for network duration, and the task may resume on a different thread contrary to a thread-local collector. Copy the required immutable value and unpin before await, or use an ownership scheme designed to cross suspension.

**Conclusion.** Protected regions should not silently span external latency.

### Example 7

**Thread-local retirement on exit.**

**Situation.** A worker retires 20 nodes into its local bag and exits before the collection threshold.

**Reasoning.** If exit drops metadata without transferring entries, nodes leak; if it deletes immediately, other participants may still reference them. Deregistration must flush/transfer the bag into the domain before releasing the participant record.

**Conclusion.** Batching creates lifecycle ownership, not disposable cache data.

### Example 8

**Logical progress under memory failure.**

**Situation.** CAS updates continue while an old participant blocks collection; allocation eventually fails.

**Reasoning.** The kernel may have exhibited lock-free logical progress until capacity exhaustion. The service was neither memory-bounded nor indefinitely available. Backpressure, active-duration enforcement, hybrid reclamation, or containment is required for a stronger claim.

**Conclusion.** Progress, reclamation liveness, resource boundedness, and availability are separate.

### Example 9

**Deferred thread-affine destructor.**

**Situation.** A retired object owns a GUI or device handle that must be released on its creating thread, but a collector invokes its deleter elsewhere.

**Reasoning.** Memory eligibility does not authorize wrong-thread destruction. Defer a thread-safe handoff token to the owning executor, keep that executor alive through drain, and specify failure/shutdown ordering; or do not place this resource under the collector.

**Conclusion.** Reclamation safety and resource-destruction context need compatible ownership protocols.

### Example 10

**Rail-signaling route snapshot.**

**Situation.** Readers pin immutable route snapshots while an updater retires old snapshots. A diagnostic task can block indefinitely while pinned. Is the design production-safe?

**Reasoning.** Not yet. An indefinite guard removes any finite memory/timing bound. The design needs bounded protected work with no blocking, guard-leak detection, memory admission, fail-safe response to overdue participants, exact snapshot identity, verified update publication, deterministic grace-period tests, target/runtime evidence, and shutdown/restart rules. Named signaling, safety, real-time, compiler/runtime, operations, security, and regulatory reviewers must approve the hazard analysis and residual risk.

**Conclusion.** EBR requires enforced quiescent progress inside the end-to-end safety case.

## Cross-Program Connections

- **Programming languages:** guard lifetimes, sendability, panic unwinding, and unsafe pointer escape define enforceable protection.
- **Data structures:** operation boundaries and traversal borrowing determine whether coarse epochs fit.
- **Operating systems:** scheduling, thread exit, signals, and preemption control quiescent progress.
- **Databases:** MVCC vacuum similarly waits for old snapshots and accumulates version debt behind long transactions.
- **Distributed systems:** epochs and fencing share generation language, but local grace periods do not tolerate crashed participants like durable consensus does.
- **Performance engineering:** batch collection, allocator interaction, cache scans, and tail latency can dominate throughput gains.
- **Reliability:** admission, observability, and restart containment convert debt assumptions into service policy.
- **Safety engineering:** maximum guard time and memory debt require human-owned limits and fail-safe response.

## References

1. Keir Fraser, *Practical Lock-Freedom*, University of Cambridge Technical Report UCAM-CL-TR-579, 2004, Section 5.2.3. <https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf>
2. Trevor Brown, “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way,” PODC 2015. <https://doi.org/10.1145/2767386.2767436>
3. Thomas E. Hart et al., “Performance of Memory Reclamation for Lockless Synchronization,” *Journal of Parallel and Distributed Computing* 67(12), 2007. <https://doi.org/10.1016/j.jpdc.2007.04.010>
4. Crossbeam project, `crossbeam_epoch` crate documentation, current 0.9 series; retrieved 2026-08-29. <https://docs.rs/crossbeam-epoch/latest/crossbeam_epoch/>
5. Crossbeam project, epoch GC design RFC, 2017. <https://github.com/crossbeam-rs/rfcs/blob/master/text/2017-05-23-epoch-gc.md>
6. ISO C++ working draft, “Safe reclamation” and RCU clauses, continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/saferecl>
7. Paul E. McKenney, *Is Parallel Programming Hard, And, If So, What Can You Do About It?*, current perfbook. <https://kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html>
8. Userspace RCU project, liburcu documentation and QSBR API, retrieved 2026-08-29. <https://liburcu.org/>
9. Concurrency Kit, `ck_epoch` safe-reclamation implementation overview, retrieved 2026-08-29. <https://concurrencykit.org/>
10. Daewoo Kim, Trevor Brown, and Ajay Singh, “Are Your Epochs Too Epic? Batch Free Can Be Harmful,” 2024. <https://arxiv.org/abs/2401.11347>

## Exercises

### Exercise 1

Why must EBR pin before acquiring a reclaimable pointer, and why must every such pointer die before unpin?

### Exercise 2

Trace a node retired in epoch 7 through a common three-bag scheme. State the participant facts needed for advances to 8 and 9 and why eligibility at 9 is conditional rather than universal.

### Exercise 3

A Rust-style service stores an epoch-protected `Shared` pointer in a future, drops its guard, and later dereferences after await. Diagnose the defect and redesign the boundary.

### Exercise 4

Choose between EBR, hazard pointers, atomic shared ownership, and a reader-writer lock for a cache whose reads traverse many nodes, may block on disk, and whose updates retire 5 GB/minute. Defend the operational policy.

### Exercise 5

An industrial robot uses EBR for replaceable motion-planning graphs. Design verification and operations requirements for guard duration, memory admission, cancellation, callback execution, restart, and safe shutdown. Identify mandatory human review.

## Answers to the Exercises

### Answer 1

If acquisition occurs first, a remover can unlink, retire, finish a grace period, and reclaim while the reader is invisible; later pinning cannot restore lifetime. Pin publication must precede the load under the collector's ordering. At exit, quiescence tells the collector the participant holds no older protected pointer. Any escaped pointer makes that statement false and permits legal collector reclamation followed by program use-after-free.

### Answer 2

For 7→8, every registered active participant must satisfy the implementation's observation condition for epoch 7 or be quiescent. Participants from 7 may still retain the node, so it is not yet reclaimed. For 8→9, those participants must have passed quiescence or refreshed according to the protocol; after repinning they cannot newly acquire the unreachable node. Eligibility at 9 depends on exact active/epoch publication, scan ordering, bag rotation, complete registration, no guard escape, and wrap-safe comparison. Another EBR design may use different generations or conditions.

### Answer 3

The future outlives the guard and crosses a quiescent announcement; the collector may reclaim the pointee before resumption. The task may also move threads against collector affinity. Copy or clone owned immutable data while pinned, drop all protected pointers and the guard, then await. Alternatively acquire a reference-counted/owned handle explicitly designed to cross suspension. If the operation must resume a traversal, repin, reacquire from an atomic root, and revalidate abstract state.

### Answer 4

Do not hold EBR or a reader lock across disk blocking. At 5 GB/minute, one delayed epoch creates severe debt. If readers can acquire a compact shared-ownership snapshot/handle and then block, atomic shared ownership is the safest default; measure its acquisition cost. Hazard pointers can pin named nodes during blocking but many-node traversals need many slots or redesigned ownership. EBR is suitable only if disk I/O is moved outside short protected regions by copying data and memory admission bounds retirement. A reader-writer lock held across disk blocks writers. Enforce byte-based backpressure, long-holder alarms, deterministic teardown, and benchmark the redesigned boundary.

### Answer 5

Require short nonblocking guarded regions, typed non-escaping graph borrows, immutable published graphs, exact-once retirement, byte-based admission, overdue-guard detection, bounded local/global bags, and a fail-safe that stops accepting motion updates before memory exhaustion. Cancellation before publish discards private work; after unlink it preserves retirement. Deferred graph destruction must run in a qualified context and report failures. Restart must establish old-process containment; shutdown closes motion operations, reaches quiescence, flushes/drains, verifies callbacks, then releases devices and collector. Automated evidence includes model/weak-memory tests, forced pauses, poisoned reuse, sanitizers, cancellation/panic/power-cycle tests, capacity and callback faults, and target timing telemetry. Named robotics, functional-safety, controls, real-time, compiler/runtime, cybersecurity, operations, and regulatory reviewers must approve hazards, timing/memory limits, fallback, and residual risk. No automated suite certifies safe motion.
