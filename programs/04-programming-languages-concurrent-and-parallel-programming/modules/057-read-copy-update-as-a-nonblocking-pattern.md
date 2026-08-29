---
module_id: CONPAR-057
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 57
title: Read-Copy-Update as a Nonblocking Pattern
status: complete
last_verified: 2026-08-29
---

# Read-Copy-Update as a Nonblocking Pattern

## One-Page Review

### Governing question

How can readers traverse stable old versions while updaters publish new state and defer destruction through a grace period, without overstating consistency, progress, memory, callback, or lifecycle guarantees?

### Essential definitions

- **read-copy-update (RCU)** is a family of synchronization mechanisms that combines read-side critical sections, publish/subscribe pointer access, removal or replacement, and grace-period-based deferred reclamation.
- A **read-side critical section** is a region during which references acquired through the RCU protocol remain valid under that RCU flavor's scheduling rules.
- **copy-update** constructs or prepares replacement state without mutating the reader-visible old version in place.
- **publication** atomically makes a fully initialized new version reachable with the required ordering.
- **removal** prevents new readers from acquiring an old object through the protected structure.
- A **grace period** ends after every reader that could have acquired the removed object before removal has completed its relevant read-side critical section.
- **synchronous reclamation** waits for a grace period; **asynchronous reclamation** schedules a callback after it.
- **existence guarantee** means an object remains alive; **content consistency** describes which fields/version a reader observes. RCU lifetime does not automatically give a transactionally consistent snapshot.
- **flavor** denotes a concrete RCU implementation and contract, such as Linux Tree RCU, SRCU, Tasks RCU, userspace QSBR, or a C++ RCU domain.
- A **reclamation barrier** waits for earlier callbacks as specified; it is not necessarily the same operation as starting one grace period.

### Central model, mechanism, or theorem

A reader enters the chosen RCU read-side region, uses the matching dereference primitive to acquire published pointer p, reads only according to p's stability rules, and exits before p can escape. An updater creates initialized replacement q, atomically publishes q (or unlinks p), and then either waits for a grace period or schedules p's cleanup after one. Readers overlapping publication may legally see old p or new q; readers starting after removal cannot newly acquire p. Once all pre-removal readers finish, p can be reclaimed. This proves lifetime only under the exact flavor, publication, traversal, and callback rules.

### Critical invariants

Replacement state is initialized before publication. Reader acquisition pairs with publication according to the language/API. Reader-visible fields are immutable or separately synchronized. Removed objects are not reclaimed before a grace period covering all possible old readers. References and dependent pointers do not escape the read-side region unless converted to an independent lifetime handle. Update-side locks protect writer-writer invariants when needed; RCU does not provide writer mutual exclusion. Removal/retirement occurs exactly once. Callback ownership, context, ordering, batching, module/component lifetime, and shutdown are explicit. Every claim names the RCU flavor and target configuration.

### Common failures

Code publishes partial initialization; reads an RCU pointer without the matching dereference primitive; mutates old reader-visible fields in place; assumes one reader sees an all-or-nothing multi-object snapshot; holds a forbidden lock, blocks, sleeps, or awaits in a flavor that disallows it; returns a raw pointer after unlock; frees immediately after unlink; confuses `call` with callback completion; unloads code before its callbacks drain; shares objects across domains; omits writer serialization; assumes readers are universally wait-free; or calls RCU a memory collector for arbitrary unreachable objects.

### Compact example

R1 enters and acquires configuration A. W builds B privately, publishes B, and schedules A after a grace period. R2 enters after publication and acquires B. R1 may continue reading immutable A; R2 reads B. When R1 exits and every other pre-publication reader has exited, A's callback becomes eligible. No reader observes partially built B, but R1 and R2 need not observe the same version.

### Connections

[Acquire and Release Ordering](027-acquire-and-release-ordering.md) supplies publish/subscribe reasoning. [Epoch-Based Reclamation](056-epoch-based-reclamation.md) supplies coarse quiescence and debt analysis. [Hazard Pointers](055-hazard-pointers.md) gives a fine-grained alternative. The next module formalizes linearizability proofs.

## Governing Question

How should engineers use RCU as a nonblocking read-mostly design pattern while keeping lifetime, version consistency, writer serialization, grace-period progress, callback execution, and shutdown as separate proof obligations?

The word “nonblocking” belongs to a specific operation under a specific flavor. It must never be inferred merely from the name RCU.

## Why This Matters

Read-mostly structures—routing tables, configuration snapshots, registries, caches, policy maps, kernel metadata—often suffer when every reader writes a shared lock or reference count. RCU makes synchronization asymmetric. Readers usually perform extremely cheap entry, ordered pointer acquisition, local traversal, and exit; writers pay for copying, publication, removal, grace-period coordination, and reclamation.

The pattern can dramatically reduce reader contention, but it changes semantics. A reader can observe an old version while a concurrent update has already published a new one. Different pointer acquisitions can span versions unless the structure preserves traversal invariants. Updates may need a mutex. A delayed reader can retain old state and callbacks. Memory ordering primitives and compiler dependencies are part of the API.

RCU is a family, not one portable pseudocode algorithm. Linux offers several flavors for different scheduling contexts. Userspace libraries expose signal, memory-barrier, bulletproof, and QSBR variants. C++ safe reclamation defines domain regions and scheduled evaluations. The correct flavor comes before performance claims.

## Prerequisites and Retrieval

Retrieve:

- happens-before from [Happens-Before Relations](023-happens-before-relations.md);
- publication from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- weak-memory obligations from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- progress scopes from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md);
- remove-versus-reclaim from [Hazard Pointers](055-hazard-pointers.md); and
- grace-period debt from [Epoch-Based Reclamation](056-epoch-based-reclamation.md).

Retrieval prompt: place one reader before publication and one after; state which version each may see, when the old version becomes reclaimable, and what additional guarantee would be required for a multi-object atomic snapshot.

## Learning Objectives

After completing this module, a learner can:

1. decompose RCU into read, copy/update, publish, remove, grace, and reclaim phases;
2. distinguish lifetime safety from snapshot/content consistency;
3. derive the old-or-new reader argument for immutable replacement;
4. map publish/subscribe and dependent reads to a concrete API;
5. explain why writers often still require mutual exclusion;
6. select synchronous versus callback reclamation and specify execution ownership;
7. qualify blocking, preemption, async, and progress by RCU flavor;
8. audit callback barriers, module unload, cancellation, and shutdown;
9. design model, weak-memory, stress, latency, and debt evidence; and
10. decide when RCU, EBR, hazards, shared ownership, or locks best match a workload.

## Core Exposition

### The three relationships

RCU coordinates three relationships. Publish/subscribe makes initialized replacement state visible to readers. Read-side protection prevents reclamation while a reader may hold a reference. Grace-period detection orders deferred destruction after pre-removal readers. Conflating them produces bugs: a grace period does not publish fields, and acquire ordering does not extend object lifetime.

The typical lifecycle is `private q → publish q/remove p → p retired → grace complete → p reclaimed`. Old p can remain physically valid and readable while unreachable to new readers. New readers follow q. The updater must preserve any structural invariants that let old and new traversals coexist.

### Read: enter, acquire, use, exit

A reader enters the matching flavor's read-side critical section, obtains a pointer through its RCU dereference primitive, and uses the pointee under documented stability rules. The pointer and dependent references die before exit unless the reader safely converts them into independent ownership, often by acquiring a reference count and revalidating identity.

Entry/exit mechanics vary. Some kernel RCU read-side sections cannot voluntarily block; SRCU has different rules. Userspace QSBR requires explicit quiescent reports. A C++ RCU domain defines lock/unlock regions. Never put `await`, blocking I/O, foreign callbacks, or arbitrary scheduler transitions inside a region until the selected flavor explicitly permits them.

RCU guarantees existence, not immutability. A reader may safely dereference a live object but still race with in-place mutation. Prefer immutable reader-visible versions. If fields change, use atomics, locks, sequence validation, or another protocol and define the resulting consistency.

### Copy and update

“Copy” can mean copying an entire snapshot, path-copying modified nodes, allocating one replacement element, or preparing a new link. It need not mean duplicating the whole data structure. The essential point is that readers continue using stable old state while the writer prepares new state privately.

Writer-writer concurrency is separate. Two writers that both copy from A and publish replacements can lose an update. Use a mutex, CAS retry with refreshed base, single-writer ownership, or a transactional protocol. RCU removes reader-writer exclusion from selected paths; it does not automatically serialize writers.

Copy cost scales with version granularity. Whole snapshots simplify reader consistency but make large updates expensive and can multiply retained bytes. Fine-grained replacement reduces copy cost but makes traversal and multi-field invariants harder.

### Publish and subscribe

The updater fully initializes q before the publication primitive. The reader uses the paired subscription/dereference operation before reading q. In Linux these roles are represented by APIs such as `rcu_assign_pointer` and `rcu_dereference`; in another environment, follow its specification rather than translating them to plain loads/stores.

Publication commonly resembles release/acquire, but compiler dependency handling and API-specific guarantees matter. Publishing q with a relaxed/plain store can expose partial initialization or permit invalid compiler transformations. An acquire does not make later concurrent in-place writes safe.

One aligned pointer publication creates a clear old-or-new choice. Publishing multiple independent roots does not create an atomic multi-root snapshot. Put related state behind one immutable root or add version validation if readers require cross-object consistency.

### Remove and preserve traversals

Removal makes p unavailable to readers that start/acquire afterward. Existing readers may still traverse p. Linked algorithms must ensure their view remains structurally valid: initialize new links before publication, preserve reader-used old links until grace, and use RCU-safe list operations rather than ordinary pointer surgery.

A reader overlapping an insertion or deletion may observe old or new membership according to the algorithm. That can be acceptable for lookup but insufficient for linearizable enumeration or policy decisions. Document the abstract consistency model: per-lookup linearizability, weak iteration, version snapshot, or something else.

Exact-once ownership remains. The update/helper that removes p transfers it once to the callback or synchronous cleanup path. A losing updater must discard only its private replacement; it cannot retire the shared old object.

### Grace-period argument

Partition readers into those whose critical sections began before removal and those starting after. New readers cannot acquire p through the removed publication path. Preexisting readers may hold p, so reclamation waits until every such reader exits. At grace completion, neither class can validly hold p: old readers are finished and new readers could not acquire it. Reclamation is safe under complete tracking and no escape.

This argument establishes lifetime, not that callbacks run immediately, readers see a latest version, or the update was linearizable as a multi-object operation. Flavor-specific implementation determines how quiescent progress is observed and whether preemption/blocking delays grace.

### Synchronous and callback cleanup

A synchronous grace operation waits, so it can block the updater even when readers never block each other. An asynchronous call queues a callback and lets the updater continue; callback latency and debt then become operational concerns. Neither choice makes the writer path automatically lock-free.

Callback functions must obey execution-context restrictions, own valid captured state, run exactly once, and tolerate batching. They may execute on a different CPU/thread after the initiating component expects to stop. Callback code, deleters, allocators, logging, and nested synchronization can block or re-enter.

Shutdown may need a callback barrier that waits for previously queued callbacks, not merely one new grace period. Linux documents `rcu_barrier` for unload scenarios; exact operations differ by environment. Unloading callback code before queued callbacks finish is an execution-after-unload defect.

### Consistency models

For one immutable root, each subscription obtains either an old or new version. If a reader loads the root once and traverses only that immutable graph, it has a version-consistent snapshot. If it reloads roots or follows mutable cross-links, it can see a mixture.

RCU does not make all read operations linearizable. A lookup may linearize at root acquisition or link read if the algorithm proves it. Enumeration may be weakly consistent. A reader needing “all policies from one release” should acquire one versioned root. A reader needing the newest state may need retry/version checks.

Staleness is semantic policy, not memory safety. An old route or authorization rule can be perfectly safe to dereference yet unacceptable to use. Define maximum acceptable version age and whether a grace period, acknowledgment, or stronger coordination is required before an update becomes externally effective.

### Progress and retention

Some RCU flavors make read-side primitives wait-free or extremely lightweight under stated configurations. The update can allocate, copy, lock writers, retry CAS, wait for grace, enqueue callbacks, or block in memory management. State progress per operation and configuration.

A delayed reader retains removed versions and callbacks, similarly to coarse epoch protection. If updates produce λ bytes/s and a grace period is delayed D seconds, extra debt is approximately λD plus batching. At 20 MB/s for 30 seconds, that is roughly 600 MB before overhead. Whole-version copying can amplify debt beyond node counts.

Backpressure, callback batching, expedited grace operations, and flavor changes affect latency and system load. Expedited grace is not a free safety button; use it only under documented operational policy. Monitor the assumptions rather than masking stalls with forced freeing.

### Flavor selection

Linux Tree RCU integrates kernel scheduling and configuration. SRCU supports different reader behavior at different cost. Tasks RCU tracks task-level quiescence. Userspace liburcu offers multiple implementations, including QSBR, each trading reader overhead, registration, signals, barriers, and quiescent reporting.

C++ safe reclamation describes RCU domains and scheduled evaluations in the language library model. An application-level homegrown epoch counter is not thereby equivalent. Select by execution environment, permitted reader actions, participant lifecycle, latency, target support, and maintained tooling.

Keep flavor names in APIs and documents when rules differ. A generic wrapper that erases whether blocking is legal makes review harder and can create unsound reuse.

### Cancellation, failure, and shutdown

Cancellation inside a reader must still execute read unlock before dropping the last protected use. Exceptions/panics need scope guards. After updater publication, cancellation cannot report “no effect”; old-state cleanup still owns one callback or synchronous retirement.

Allocation/copy failure before publication leaves old state authoritative and frees private q. Failure after publication requires a compensating update if rollback is desired; never restore p after it has been scheduled for reclamation without a new lifetime proof.

Shutdown closes new readers and writers, waits for operations, unpublishes/removes roots as required, completes grace periods, drains callbacks with the environment's barrier, verifies debt, releases version-owned resources, then unloads code and domains. Restart/shared-memory cases require containment of old readers before reuse.

### Verification and observability

Model one old reader, publication, one new reader, removal, grace, and callback. Add multiple roots, writer races, escaped references, blocked readers, callback ordering, cancellation, and unload. Assert no partial publication, no early reclaim, exact callback, and the promised consistency model.

Use schedule barriers around enter, dereference, publish, unlink, exit, grace completion, callback, and unload. Run weak-memory/litmus tools, sanitizers, poisoned reuse, writer-conflict tests, and target/configuration checks. Exercise permitted and forbidden blocking behavior for the chosen flavor.

Monitor active/longest readers, grace latency distribution, grace/callback backlog and bytes, oldest callback, publication/update rate, copy bytes, writer-lock/CAS contention, callback duration/failure, expedited operations, quiescent-report lag, and shutdown barrier time. Version identifiers reveal staleness without logging addresses.

## Definitions and Notation

- `P`: the atomically published root.
- `p`: old version/reference acquired before or during removal.
- `q`: privately initialized replacement.
- `R`: set of read-side critical sections relevant to one grace period.
- `remove(p)`: event after which new correct readers cannot acquire p through the protected path.
- `end(r)`: exit of reader r.
- `GP(p)`: grace period covering every r that could hold p at removal.
- `CB(p)`: exact-once cleanup scheduled after `GP(p)`.
- `V(p)`: immutable/version identity of p.
- `λ_b`: retirement/copy debt rate in bytes per second.
- `D`: grace-period delay.

The rough debt `λ_bD` excludes baseline queues, bursts, allocator overhead, callback resources, and sharing between versions. A safety proof uses reader coverage, not elapsed time.

## Mechanisms, Invariants, or Proof Structure

### Old-or-new publication proof

q is fully initialized before atomic publication. A reader's matching subscription either observes P=p before publication and uses stable p, or observes P=q and acquires q's initialization. No reader obtains a partially initialized q through the protocol. This proof does not cover later mutable writes or multiple independent roots.

### Grace-period lifetime proof

At removal, any reader that can hold p is already in the relevant reader set R. New readers cannot acquire p from P. GP waits until every relevant r ends. With no pointer escape, after GP no valid reader holds p; exact-once callback can reclaim it. The implementation must correctly identify R under its scheduling/configuration semantics.

### Executable version model

The sequential model records an old reader on A, publication of B, a new reader on B, retirement of A, and callback eligibility only after the old reader exits. It demonstrates version/accounting semantics, not concurrent RCU or memory ordering.

<!-- bijux-verify: {"id":"rcu-version-grace-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"old_reader=A\nnew_reader=B\nretired_before_grace=['A']\ncallback_before_exit=[]\ncallback_after_exit=['A']\ncurrent=B\n","stderr":""}} -->
```python
current = "A"
active_readers = {"old": current}
retired = []
callbacks = []
old_reader = active_readers["old"]
current = "B"
retired.append("A")
active_readers["new"] = current
new_reader = active_readers["new"]

def collect():
    protected = set(active_readers.values())
    ready = [version for version in retired if version not in protected]
    retired[:] = [version for version in retired if version in protected]
    callbacks.extend(ready)
    return ready

before = collect()
del active_readers["old"]
after = collect()
print(f"old_reader={old_reader}")
print(f"new_reader={new_reader}")
print("retired_before_grace=['A']")
print(f"callback_before_exit={before}")
print(f"callback_after_exit={after}")
print(f"current={current}")
```

### Audit obligations

1. Name the exact RCU flavor, domain, target, and reader scheduling rules.
2. Pair every publication with the specified subscription primitive.
3. Define which reader-visible fields are immutable or synchronized.
4. Prove no RCU-derived reference escapes without independent ownership.
5. Define writer serialization and observable consistency.
6. Map each removal to one grace/callback ownership path.
7. Bound or govern reader duration, debt, and callback latency.
8. Prove cancellation, failure, barrier, unload, and shutdown order.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation |
|---|---|---|
| RCU immutable replacement | extremely cheap read-mostly access and old-version coexistence | writer/copy/grace complexity and version debt |
| EBR | generic coarse operation protection | stalled participant retains broad retirement debt |
| Hazard pointers | fine-grained blocking-safe named protection | per-pointer protocol and slot/scan cost |
| Atomic shared ownership | lifetime can cross async/blocking boundaries | reference traffic and contention |
| Reader-writer lock | simple strong in-place coordination | readers write/contend; long readers block writers |
| Sequence lock | very cheap consistent small-copy reads | reader retry; unsuitable for pointer lifetime alone |
| MVCC/version snapshots | explicit transactional/version semantics | version management and cleanup |
| Tracing GC | automatic reachability lifetime | runtime costs; not update consistency |

Choose RCU when reads dominate, immutable/copy update is natural, stale old versions are acceptable, the environment supplies a mature flavor, and callback debt is governable. Choose shared ownership when references must cross blocking/async boundaries. Choose locks when update simplicity and strong consistency matter more than measured reader contention.

## Failure Modes and Misconceptions

- **“RCU is one algorithm.”** It is a family with flavor-specific contracts.
- **“Read lock means ordinary lock.”** It may be scheduler/compiler protocol rather than mutual exclusion.
- **“Readers always see newest.”** Overlapping readers may legally see old versions.
- **“Existence means consistency.”** Live mutable fields can still race or mix versions.
- **“Copy means copy everything.”** Replacement granularity is a design choice.
- **“RCU serializes writers.”** Writer conflicts still need a protocol.
- **“Publish is a plain store.”** Initialization visibility requires the API's publication primitive.
- **“One root load gives a multi-root snapshot.”** Independent publications can mix releases.
- **“Grace starts reclamation immediately.”** Callback scheduling/execution can lag.
- **“One grace drains old callbacks.”** Use the environment's callback barrier semantics.
- **“All RCU readers may block.”** Legality depends on flavor/configuration.
- **“A raw pointer can escape unlock.”** Lifetime protection ends with the region.
- **“Nonblocking readers make nonblocking updates.”** Copy, locks, waits, allocation, and callbacks remain.
- **“Timeout permits free.”** Grace safety depends on reader completion, not wall time.
- **“Module unload is ordinary shutdown.”** Queued callbacks may still execute its code.

## Worked Examples

### Example 1

**Old and new configuration.**

**Situation.** R1 acquires A; W publishes B; R2 then acquires B.

**Reasoning.** With immutable versions and correct publication, R1 safely finishes on A and R2 sees initialized B. No rule requires R1 to switch mid-region. A remains alive until a covering grace period.

**Conclusion.** RCU supports safe version overlap, not instantaneous reader convergence.

### Example 2

**Partial publication.**

**Situation.** W stores pointer to B before initializing `B.limit`; R acquires B and reads the field.

**Reasoning.** Grace periods concern old-reader completion, not B initialization. The reader can see invalid contents or a data race. Initialize privately, then use the required publication primitive; subscribe through its pair.

**Conclusion.** Publish/subscribe correctness is independent of reclamation.

### Example 3

**Lost writer update.**

**Situation.** W1 and W2 copy A. W1 adds rule X and publishes B; W2 adds Y to its A copy and publishes C.

**Reasoning.** C can omit X. Readers are memory-safe but the writer invariant is wrong. Serialize writers, or CAS expected A and make W2 refresh/reapply Y after failure.

**Conclusion.** RCU removes selected reader-writer conflicts, not writer-writer conflicts.

### Example 4

**Multi-root mixture.**

**Situation.** Policy and routing roots are published separately from release 8 to 9. A reader loads policy 9 and routing 8.

**Reasoning.** Each load is individually valid. If cross-root consistency matters, place both behind one immutable release root or validate a common version and retry. A grace period does not create atomic multi-root publication.

**Conclusion.** Define snapshot boundaries in representation.

### Example 5

**Synchronous versus callback reclaim.**

**Situation.** An updater cannot block but must remove A.

**Reasoning.** It schedules A with the flavor's asynchronous callback rather than waiting synchronously. The update can return after queueing, but A's bytes and deleter work remain debt. Queue failure, ownership, callback context, and shutdown barrier must be specified.

**Conclusion.** Asynchrony moves waiting and ownership; it does not erase them.

### Example 6

**Reference beyond read unlock.**

**Situation.** A lookup returns a pointer to A, exits its RCU region, and the caller later reads A.

**Reasoning.** A grace period may complete immediately after exit and reclaim A. Copy needed data inside the region or acquire an independent counted/owned reference before exit and revalidate according to the object's protocol.

**Conclusion.** API return types must encode the lifetime boundary.

### Example 7

**Debt estimate.**

**Situation.** Replacements retire 20 MB/s and a reader delays grace by 30 seconds.

**Reasoning.** Simplified extra debt is about 600 MB, plus queues, allocator overhead, and shared/copy amplification. If delay is unbounded, no finite estimate suffices.

**Conclusion.** Reader duration and callback debt are capacity SLOs.

### Example 8

**Callback and module unload.**

**Situation.** A plugin queues callbacks whose deleter function lives in the plugin, waits one grace period, then unloads.

**Reasoning.** Earlier callbacks might remain queued after that grace. Unloading makes their function address invalid. Close new work and use the flavor's callback barrier/drain guarantee before unloading code and data.

**Conclusion.** Grace completion and callback-queue drainage are distinct lifecycle events.

### Example 9

**Flavor mismatch.**

**Situation.** Code written for sleepable SRCU is ported to a non-sleepable read-side flavor without changing a blocking call.

**Reasoning.** The algorithm violates the new scheduling contract even though API names look similar. Review preemption, blocking, nesting, interrupt context, and quiescence for the target flavor; restructure blocking outside the region if needed.

**Conclusion.** Flavor is part of correctness, not a backend toggle.

### Example 10

**Air-traffic policy publication.**

**Situation.** Controllers read RCU-published separation-policy snapshots while updates roll out. Can old-or-new memory safety justify operational use?

**Reasoning.** No. The safety case must define whether an old policy is acceptable and for how long, make each decision use one version, validate policy content, authenticate releases, bound grace/debt, prevent blocking readers, specify failover and callback drain, and record the version used per decision. Named air-traffic-domain, safety, real-time, formal-methods, compiler/runtime, security, operations, and regulatory reviewers must approve requirements and evidence.

**Conclusion.** Safe reclamation is not policy correctness or certification.

## Cross-Program Connections

- **Programming languages:** dependency, acquire/release, lifetimes, and unsafe escape govern publish/subscribe correctness.
- **Data structures:** path copying and stable old links determine reader traversal semantics.
- **Operating systems:** scheduler-integrated RCU flavors define blocking, preemption, interrupt, and callback behavior.
- **Databases:** MVCC likewise serves old versions and delays cleanup behind active snapshots, but offers transactional semantics RCU alone does not.
- **Distributed systems:** immutable configuration versions resemble replicated snapshots; local grace periods do not establish distributed agreement.
- **Security:** stale authorization policy can be memory-safe yet unacceptable; version/audit policy is required.
- **Performance engineering:** copy amplification, grace tails, and callback batching determine the real read/write trade.
- **Safety engineering:** staleness bounds and version-consistent decisions require human-owned hazards and fail-safe policy.

## References

1. Paul E. McKenney and John D. Slingwine, “Read-Copy Update: Using Execution History to Solve Concurrency Problems,” 1998. <https://www.eecg.toronto.edu/~amza/ece1747h/papers/rcu.pdf>
2. Linux Kernel documentation, “What is RCU? — Read, Copy, Update,” current `next`; retrieved 2026-08-29. <https://www.kernel.org/doc/html/next/RCU/whatisRCU.html>
3. Linux Kernel documentation, “RCU Concepts,” current; retrieved 2026-08-29. <https://docs.kernel.org/RCU/rcu.html>
4. Linux Kernel documentation, “Using RCU to Protect Read-Mostly Linked Lists,” current; retrieved 2026-08-29. <https://docs.kernel.org/RCU/listRCU.html>
5. Linux Kernel documentation, “A Tour Through RCU's Requirements,” current; retrieved 2026-08-29. <https://docs.kernel.org/RCU/Design/Requirements/Requirements.html>
6. Mathieu Desnoyers et al., “User-Level Implementations of Read-Copy Update,” *IEEE TPDS* 23(2), 2012. <https://doi.org/10.1109/TPDS.2011.159>
7. Userspace RCU project, liburcu documentation, retrieved 2026-08-29. <https://liburcu.org/>
8. ISO C++ working draft, “Safe reclamation: Read-copy update,” continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/saferecl.rcu>
9. Paul E. McKenney, *Is Parallel Programming Hard, And, If So, What Can You Do About It?*, current perfbook. <https://kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html>
10. Jade Alglave et al., “Frightening Small Children and Disconcerting Grown-ups: Concurrency in the Linux Kernel,” ASPLOS 2018. <https://doi.org/10.1145/3173162.3177156>

## Exercises

### Exercise 1

Separate the three RCU relationships—publication, read-side lifetime, and grace-period reclamation—and state one bug caused by confusing each pair.

### Exercise 2

Trace R1 entering before publication A→B and R2 entering afterward. Identify allowed versions, removal, grace coverage, and callback eligibility.

### Exercise 3

Diagnose an API that returns an RCU-derived raw pointer after read unlock and sometimes stores it across await. Redesign the type/operation boundary.

### Exercise 4

Choose between RCU, atomic shared ownership, EBR, and a reader-writer lock for a 100 MB configuration updated every minute, read millions of times per second, with readers that may perform network I/O. Defend version and debt policy.

### Exercise 5

A power-grid controller publishes RCU-protected topology and protection-policy snapshots. Design a review for atomic snapshot scope, stale-version limits, writer conflict, callbacks, failover, and shutdown. Separate automation from human approval.

## Answers to the Exercises

### Answer 1

Publication orders private initialization before a subscribing reader; without it, a new object can be live but partially observed. Read-side lifetime keeps an acquired old object alive; acquire ordering alone cannot prevent its deletion. A grace period orders reclamation after pre-removal readers; it does not publish new fields or synchronize in-place payload mutation. Each edge needs the chosen flavor's API and a distinct proof.

### Answer 2

R1 may acquire immutable A and finish on A. W initializes B, publishes B atomically, and removes A from new acquisition. R2 entering/subscribing afterward acquires B. The grace period covers R1 and every other reader that could have acquired A before removal; it need not wait for R2 with respect to A. After those old readers exit, A's callback is eligible, though actual execution may lag. Both versions must remain internally valid during overlap.

### Answer 3

Unlock ends A's RCU lifetime; a grace period may reclaim it before the caller or resumed task dereferences it. The task may also cross a flavor's thread/scheduling restrictions. Return copied immutable data, an owned snapshot, or an independently reference-counted handle acquired and identity-validated inside the region. For traversal after await, save stable keys/version, unlock, await, re-enter, reacquire, and validate/restart. Make the raw protected type borrow the guard so escape does not type-check.

### Answer 4

Do not hold an RCU/EBR region or reader lock across network I/O. Use RCU for a short acquisition/copy of a compact decision or acquire an atomic shared-ownership handle to the immutable 100 MB snapshot, then leave RCU before I/O. Shared ownership directly supports long-lived readers but a stalled request retains 100 MB; cap request duration/count and monitor version bytes. RCU can optimize millions of acquisitions if profiling warrants it, with one immutable root and callback debt/backpressure. EBR has similar coarse-stall risk; a reader lock would block minute updates across I/O. Define acceptable stale release, maximum retained versions/bytes, writer serialization, and shutdown drain.

### Answer 5

Place topology and policy required for one decision behind one immutable, authenticated release root or validate a common release and retry. Serialize/reconcile writers so no update is lost. Record release identity per control decision and define a domain-approved stale-version bound; memory safety alone is insufficient. Queue old releases exactly once, bound callback bytes/age, contain delayed readers, and drain callbacks before code/domain unload. Failover must preserve release authority and prevent old controller actions; shutdown closes decisions, completes readers/grace/barrier, then releases resources. Automation includes model and weak-memory tests, multi-root counterexamples, writer races, poisoned reuse, callback faults, delay/failover/power tests, and live staleness/debt telemetry. Named grid-protection, electrical-safety, real-time, formal-methods, compiler/runtime, cybersecurity, operations, and regulatory reviewers must approve hazards, snapshot semantics, limits, fallback, and residual risk. No test suite certifies grid control.
