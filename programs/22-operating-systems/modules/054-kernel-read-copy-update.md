---
module_id: OS-054
program: Operating Systems
level: 2
module_number: 54
title: Kernel Read-Copy-Update
status: complete
last_verified: 2026-09-04
---

# Kernel Read-Copy-Update

## One-Page Review

### Governing question

How can kernel readers traverse shared objects with extremely low synchronization overhead while writers publish complete versions, serialize conflicting changes, defer reclamation, and guarantee progress across preemption, interrupts, idle CPUs, hotplug, and teardown?

### Essential definitions

- **Read-copy-update (RCU)** is a family of synchronization mechanisms that separates read-side access, update publication, and deferred reclamation.
- An **RCU read-side critical section** marks an interval during which a matching reader can retain and dereference protected objects.
- **Publication** makes a fully initialized object reachable through an RCU-protected pointer with required ordering.
- A **quiescent state** is a flavor-specific observation proving that a thread of control is not in a preexisting read-side critical section.
- A **grace period** spans enough quiescent progress to ensure all readers that began before its boundary have completed.
- An **RCU callback** schedules work, commonly reclamation, after the required grace period rather than blocking the updater.
- **Removal** makes an object unreachable to new readers; **reclamation** releases its storage only after old readers can no longer use it.
- An **RCU flavor** defines eligible reader contexts, quiescent states, blocking rules, and synchronization APIs.
- **`rcu_barrier`-style draining** waits for callbacks queued before the barrier, which is distinct from merely waiting for one grace period.

### Central model, mechanism, or theorem

An RCU update follows `initialize -> serialize writers -> release-publish new -> remove old reachability -> wait or queue grace-period reclamation -> free old`. A reader follows `enter flavor -> acquire-dereference protected pointer -> use without exceeding flavor rules -> exit`. If every preexisting reader exits before reclamation and publication ordering is paired correctly, a reader can observe an old or new complete version without using freed storage.

RCU is not “no locking.” It usually removes shared read-lock modification, while writers still need locks, atomics, or single ownership; compound snapshots may need versioning; and references that escape the read section need another lifetime protocol. Its value is asymmetric: pay update, memory, callback, and grace-period cost to make frequent reads scalable.

### Critical invariants

- An object is fully initialized before release publication, and readers use the matching protected dereference.
- Once unlinked, an object remains allocated until every reader that could have observed it has quiesced.
- Competing writers are serialized independently unless the update itself is one proven atomic transition.
- An RCU-derived pointer is used only within its read-side lifetime or converted safely to a durable reference before exit.
- The chosen flavor covers the actual task, interrupt, NMI, sleep, idle, and tracing contexts.
- Module or subsystem teardown prevents new callbacks, waits for readers and outstanding callbacks in the required order, then frees code and state.
- Grace-period progress and callback backlog remain observable and bounded enough for the deployment's memory, latency, real-time, and energy requirements.

### Common failures

Common mistakes are assigning an incompletely initialized pointer, reading a protected pointer through an ordinary load, freeing immediately after list deletion, assuming a grace period waits for readers that start later, using RCU to serialize writers, returning an unreferenced pointer beyond the read section, following a protected pointer after dropping the read lock, confusing callback draining with one grace-period wait, unloading callback code before queued callbacks run, selecting a flavor that forbids the reader's sleep or context, and ignoring a callback backlog until it exhausts memory.

### Compact example

Reader `r0` begins at logical time 1. An updater publishes a new object and removes the old at time 2. Reader `r1` begins at time 3 and can see the new version; it need not delay reclamation of the old object if it could never observe it. When `r0` exits at time 4, the grace period for the removal can end even if `r1` continues. This is why a grace period waits for preexisting readers, not for the system to have no readers at all.

### Connections

[OS-037](037-copy-on-write.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), and [OS-053](053-scalable-locking.md) establish immutable versions, distributed state, ordering, and reader-scalability motivations. [OS-057](../ROADMAP.md) and [OS-059](../ROADMAP.md) apply related ideas to scheduling and cross-CPU invalidation.

## Governing Question

Traditional reader-writer locks require readers to modify shared lock state. On a read-dominated multiprocessor workload, that cache line becomes a bottleneck even though readers do not conflict semantically.

RCU lets readers avoid that shared modification in common configurations. The governing question is how to recover the safety formerly supplied by a read lock: complete publication, stable reachability during reads, safe delayed reclamation, writer coordination, and progress across all kernel execution modes.

## Why This Matters

RCU protects routing tables, process and credential relationships, filesystem structures, networking state, tracing, and many registries. Errors become use-after-free, partial initialization, stale authority, memory exhaustion, or teardown that calls unloaded code.

Its performance effect is architectural. Read-side work can remain local while updates absorb synchronization and memory cost. On large systems that asymmetry is often the difference between scaling and cache-line collapse.

The simplicity of the read-side syntax is deceptive. Correct use requires a precise flavor, pointer discipline, writer protocol, reclamation proof, and operational plan for stalls and callback pressure.

## Prerequisites and Retrieval

Review [OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-037](037-copy-on-write.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), and [OS-053](053-scalable-locking.md).

Retrieve these distinctions:

- object reachability and object allocation lifetime are separate;
- release and acquire ordering can publish complete immutable state;
- one atomic pointer replacement does not serialize several writers' surrounding logic;
- preemption, interrupt, idle, and offline states contribute different quiescent evidence;
- asynchronous completion transfers lifetime obligations to the callback;
- a read-mostly workload can justify expensive writes but not unbounded writer failure;
- removing an item from a container does not revoke references already obtained;
- exact multi-object snapshots require more than safe traversal.

## Learning Objectives

After this module, you should be able to:

1. trace RCU publication, read-side access, removal, grace period, callback, and reclamation;
2. distinguish reachability, pointer ordering, reference ownership, writer serialization, and snapshot consistency;
3. select an RCU flavor from reader context and blocking requirements;
4. update lists and pointer-rooted structures without exposing partial state or reclaiming live objects;
5. integrate RCU with reference counts, locks, hotplug, module unload, and cancellation;
6. diagnose stalls, callback backlog, grace-period latency, and real-time or energy effects;
7. validate RCU code with static annotations, runtime checking, torture, fault injection, and model reasoning.

## Core Exposition

### The decomposition

RCU separates three jobs a reader-writer lock often combines: readers declare protected access, writers publish and remove reachability, and reclamation waits until old readers finish. This separation enables cheap reads.

Each job has its own API and failure mode. An update that publishes correctly but frees too early is unsafe; a deferred free without correct publication can expose partial state.

### Read-mostly fit

RCU fits structures read far more often than updated, especially when readers can accept an old or new complete version. Examples include lookup tables, linked registries, policy roots, and callback sets.

Frequent large updates can make copying, grace periods, and callback backlog dominate. Detailed measurement can justify unusual use, but read-side syntax alone is not a reason to choose RCU.

### Reader contract

A reader enters the matching read-side critical section, obtains protected pointers through the proper dereference primitive, uses them without violating flavor rules, and exits. It does not assume writer exclusion.

The reader can observe concurrent changes allowed by the data-structure algorithm. Safety against reclamation does not promise one instantaneous view across several independent loads.

### Nested readers

Read-side critical sections can nest under the flavor's contract. Only the outermost exit establishes that thread's quiescent transition for the nested interval.

APIs and debug checks track nesting appropriately. Code does not manually balance unrelated flavors or assume an inner exit permits reclamation.

### Writer contract

A writer allocates and initializes new state, serializes with competing writers, release-publishes new reachability, removes old reachability, and arranges a grace period before reclamation.

RCU readers do not block the update itself. They can continue using the old version while new readers discover the replacement.

### Writer serialization

RCU generally does not prevent two writers from losing each other's modifications. Use a mutex, spin lock, atomic compare-and-exchange loop, partitioned ownership, or another explicit protocol.

The writer lock can often remain uncontended because updates are rare. Its ordering and lock graph still include callbacks, teardown, and nested subsystem operations.

### Initialization before publication

Construct an unreachable object and initialize every reader-visible field, pointer, lock, count, and invariant before publishing it. Release publication prevents those writes from appearing after reachability.

Readers use the matching RCU dereference rather than a plain load. This conveys dependency and compiler constraints required across supported architectures.

### Protected dereference

An RCU dereference primitive returns a pointer under a valid read-side or lock-held condition and supplies the documented ordering. The resulting pointer has restrictions that preserve dependency and prevent compiler transformations from invalidating the proof.

Avoid casual integer manipulation, relational comparisons, or republishing of the pointer without understanding those restrictions. Use specialized access or protected variants only under their explicit conditions.

### Access without dereference

Some operations need only test or report the current pointer without dereferencing its target. A lighter access primitive can document that no target fields are consumed.

It does not grant lifetime. If code later follows the pointer, it must enter the correct reader or acquire another stable reference.

### Removal versus reclamation

Removal updates the container or root so future readers no longer discover the old object. Readers that loaded it earlier can still execute.

Reclamation destroys content or frees storage only after the chosen grace-period guarantee covers those readers. Conflating the two creates the canonical RCU use-after-free.

### Grace-period guarantee

A grace period waits until every reader that could have begun before its boundary has passed a flavor-specific quiescent state. Readers beginning after removal cannot discover the removed object through that path and need not all finish.

The implementation tracks distributed quiescent progress without a shared reader-count update on every common read. That tracking is where much implementation complexity lives.

### Quiescent states

Quiescent states depend on flavor and kernel configuration. Context switch, userspace execution, idle, offline transitions, or explicit reporting can contribute evidence when they prove no relevant preexisting reader remains.

One must not invent quiescent states at call sites. The selected API and implementation define them, including preempted reader handling.

### Blocking synchronization

A synchronize-style operation blocks the updater until a grace period covering prior readers completes. It is easy to sequence but unusable in contexts that cannot sleep and can add update latency.

It need not wait for unrelated callbacks to execute. Its completion proves the specified readers are gone, not that all deferred work system-wide has drained.

### Asynchronous callbacks

A call-style API queues a callback to run after the grace period. The updater returns promptly, transferring ownership of the old object and callback state to the RCU subsystem.

The callback cannot run before required readers finish, but scheduling delay can extend beyond the grace period. Callback context limits which operations may block or recurse.

### Direct deferred free

Purpose-built helpers can queue ordinary object freeing after a grace period without a custom callback. This reduces boilerplate and still requires removal and lifetime correctness.

Resources needing complex teardown, ordering, or sleeping destruction may need a callback that hands work to a suitable context rather than freeing directly.

### Callback draining

Module unload and subsystem destruction must wait until previously queued callbacks have executed, because they may reference code or state being removed. A callback-barrier operation supplies that drain boundary.

Waiting for one grace period is insufficient: callbacks already eligible can still be queued for later invocation. Stop new callback submission before the barrier, then free callback code and associated state.

### Linked-list traversal

An RCU list reader enters its section and uses RCU-aware traversal so concurrent deletion preserves next-pointer and ordering rules. A writer locks updates, initializes a new node, and uses an RCU insertion primitive.

Deletion unlinks with the matching primitive, waits or queues reclamation, then frees. A reader may see a deleted logical item if it obtained it before removal; application semantics decide whether an additional state check is needed.

### In-place field updates

RCU lifetime protection does not make arbitrary mutable fields race free. Fields can be immutable after publication, updated atomically, protected by a per-object lock, or replaced through a new version.

Readers need a sequence counter or lock when several mutable fields must form one coherent snapshot. RCU can protect the pointer lifetime around that separate mechanism.

### Replacement updates

Copy an old object into a candidate, apply changes privately, validate it, and publish the replacement root atomically. Old readers use old complete state, and new readers use new complete state.

Side effects outside the object are not automatically versioned. Writer serialization and rollback prevent duplicate identifiers, lost accounting, or external operations from escaping a failed replacement.

### Delete with state transition

Sometimes removal must prevent new durable references before unlinking. Mark the object dying under the writer protocol, remove it from RCU reachability, wait for readers that might be acquiring references, then drop the owner's reference.

The exact order depends on how reference acquisition checks liveness. A plain reference increment racing with final decrement is not safe merely because lookup used RCU.

### RCU and reference counts

RCU protects the interval from lookup to an attempted stable-reference acquisition. A purpose-built increment-if-live protocol ensures the object was not already terminal.

Once acquired, the reference can outlive the read-side critical section. Deletion removes lookup reachability, waits for lookup readers as required, and frees only after the final reference and RCU obligations both finish.

### RCU and locks

A reader can use RCU to find an object, then acquire its lock while still protected, validate that it remains eligible, and convert to the subsystem's ordinary protocol. Lock ordering includes the reader context and writer removal path.

Writers often use one lock for structural change and RCU for reader lifetime. These mechanisms complement rather than replace each other.

### Flavor selection

Different RCU families cover different read contexts and quiescent-state models: ordinary kernel readers, sleepable readers, tasks-based readers, tracing-sensitive readers, or other specialized domains.

Choose from actual reader context, whether readers may block, interrupt and NMI use, memory-order needs, grace-period latency, and callback availability. Matching names without a context matrix invites subtle misuse.

### Sleepable RCU

Sleepable RCU permits blocking inside its read-side critical sections under its rules and maintains an independent domain. That capability costs more than the lightest ordinary read path.

Ordinary and sleepable grace periods are not interchangeable. Data protected by one domain consistently uses that domain's publication, readers, callbacks, and teardown.

### Tasks-oriented flavors

Tasks-oriented variants wait for task behaviors suited to tracing, code removal, or other cases not covered by ordinary data-structure readers. Their quiescent conditions and latency differ.

They are specialized lifecycle tools, not drop-in faster or stronger versions. Documentation and tests identify the exact flavor associated with each pointer and callback.

### Preemptible kernels

On preemptible configurations, a task can be descheduled within an ordinary RCU read-side section. The implementation tracks blocked readers so a context switch does not falsely report completion.

High-priority workloads can delay those readers from resuming, extending grace periods. Real-time analysis includes reader length, boost or priority behavior, and callback progress.

### Interrupt and NMI readers

Interrupt and NMI contexts have distinct entry, nesting, and blocking constraints. The selected RCU flavor and kernel version must explicitly support the access pattern.

An interrupt can read an object while task code removes it; reclamation covers both only when the flavor's grace-period definition includes that context.

### Idle and no-tick CPUs

An idle CPU may stop periodic ticks, so RCU must distinguish extended quiescent states from interrupt entry that begins kernel reading. Entry and exit accounting preserves correctness without constantly waking idle CPUs.

Energy-aware implementations avoid unnecessary disturbances while still advancing grace periods. Bugs here can cause premature reclamation or stalls.

### CPU hotplug

Offline transitions report quiescent state and migrate or drain callbacks under an ordered protocol. Online initialization publishes per-CPU tracking before readers and callbacks depend on it.

Grace-period tracking stabilizes CPU membership so an offline CPU cannot disappear with an unreported reader, and a new CPU cannot inherit stale state.

### Expedited grace periods

Expedited synchronization requests faster quiescent progress, often using stronger cross-CPU action. It reduces update latency in exceptional paths at cost to CPUs, energy, jitter, and scalability.

It cannot make a truly stuck reader finish. Use requires a latency justification, rate limits, and tests under idle, hotplug, real-time, and large-system loads.

### Callback batching and offload

Implementations batch callbacks and grace periods to amortize global coordination. Callback work can be offloaded from selected CPUs to reduce jitter or isolation interference.

Batching increases individual latency, and offload queues need scheduling and capacity. Floods can consume memory even while the grace-period engine remains logically correct.

### Forward progress

Grace periods require relevant CPUs and tasks to reach quiescent states and RCU workers or soft interrupts to run. Long read sections, disabled interrupts, nonpreemptible loops, or higher-priority CPU-bound tasks can stall progress.

Callback invocation has its own progress requirement after grace-period completion. Monitor both grace-period age and callback backlog.

### Stall diagnosis

Stall reports identify CPUs or tasks delaying progress, grace-period sequence, elapsed time, quiescent-state information, and callback estimates. Stack traces often expose a long reader or disabled scheduling path.

Slow consoles, heavy tracing, thermal throttling, timer problems, overloaded interrupt handlers, and starved RCU workers can create or magnify warnings. Diagnose configuration and timing before assuming an RCU-core defect.

### Memory pressure

Each removed but unreclaimed object consumes memory. Update bursts, slow readers, stalled CPUs, and callback starvation multiply retained state.

Apply admission control, callback offload, batching, bounded update queues, and backpressure where necessary. Never free early to relieve pressure.

### Module unload

Unload first prevents new external entry and update publication, removes protected registrations, waits for current readers where needed, drains queued callbacks, cancels related work, and only then frees data and callback code.

Ordering is subsystem specific. A callback-barrier placed before stopping new producers can return while a later callback is queued, leaving an unload race.

### Static checking

Pointer annotations distinguish RCU-protected references from ordinary pointers. Sparse-like analysis, protected-dereference checks, and lock assertions catch missing reader contexts and invalid conversions.

Annotations are part of the design, not decoration. Suppressing a warning requires a durable proof at that access site.

### Runtime checking

RCU-aware lock dependency checking can verify that protected dereferences occur within recognized read-side or lock-held conditions. Debug object tracking detects callback-head lifecycle errors.

Coverage matters. Exercise read, update, deletion, failed insertion, cancellation, hotplug, suspend, teardown, and all flavors used.

### Torture testing

RCU torture workloads vary readers, writers, callbacks, idle, hotplug, expedited grace periods, stalls, memory pressure, and configurations. Long randomized runs expose rare progress and ordering defects.

Use sanitizers, concurrency checkers, weak-memory architectures, and targeted fault injection. Preserve configuration and seeds so a failure can be reproduced.

### Assurance

Record pointer ownership, flavor, writer locks, publication sites, removal sites, grace-period or callback path, teardown drain, context matrix, maximum reader duration, backlog limits, and operational alarms.

Assurance names subsystem, RCU, memory-model, scheduler, interrupt, hotplug, real-time, security, performance, and independent reviewers. A passing sequential version model does not certify kernel RCU use.

## Definitions and Notation

Let object versions be `O_0,O_1,...` and protected root `P`. Update `U_k` fully initializes `O_{k+1}`, release-publishes `P=O_{k+1}`, and removes `O_k` at boundary `u_k`.

Reader `r` has interval `[enter_r,exit_r]` and observed pointer `obs_r`. A grace period `G_k=[g_start,g_end]` covers removal when every reader that could have observed `O_k` before `g_start` exits or reaches the flavor's quiescent condition before `g_end`.

Safe reclamation requires `free(O_k) > g_end` and no independent reference or callback can still use `O_k`. Grace-period completion is necessary but not sufficient when pointers escape through reference counts, work queues, or other domains.

Let backlog `B(t)=queued_callbacks(t)-invoked_callbacks(t)`. Stability requires callback service to control `B` under expected update load and stalls; logical safety alone does not bound memory.

## Mechanisms, Invariants, or Proof Structure

1. **Prove fit.** Show reads dominate and can accept the specified old-or-new or versioned observation semantics.
2. **Choose a flavor.** Cover every task, sleep, interrupt, NMI, idle, tracing, hotplug, and real-time context.
3. **Serialize writers.** Define locks, atomics, partitioning, rollback, and the update linearization point.
4. **Initialize privately.** Complete fields, references, locks, labels, and invariants before reachability.
5. **Publish and dereference correctly.** Pair release publication with flavor-valid protected reader acquisition.
6. **Remove reachability.** Prevent new readers from discovering the retired version under the data-structure algorithm.
7. **Protect escaping users.** Acquire references, locks, or another domain before leaving the RCU read section.
8. **Wait before reclaiming.** Use blocking grace periods, callbacks, or deferred-free helpers and preserve all other lifetime obligations.
9. **Drain teardown.** Stop producers, remove registrations, wait for readers, drain callbacks and work, then free code and state.
10. **Guarantee progress.** Bound readers, schedule grace-period and callback work, control backlog, and handle idle and hotplug.
11. **Exercise configurations.** Use annotations, runtime checks, torture, sanitizers, fault injection, and weak-memory tests.
12. **Preserve evidence.** Retain flavors, configurations, pointer flows, grace periods, backlogs, stalls, seeds, traces, failures, and limitations.

<!-- bijux-verify: {"id":"rcu-preexisting-readers","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"update-epoch=2\npreexisting-readers=r0\ngrace-period-end=4\npost-update-reader-blocks=False\nsafe-to-reclaim-after=4\n","stderr":""}} -->
```python
readers = (
    {"name": "r0", "enter": 1, "exit": 4},
    {"name": "r1", "enter": 3, "exit": 6},
    {"name": "r2", "enter": 5, "exit": 7},
)
update_epoch = 2
preexisting = tuple(reader for reader in readers if reader["enter"] < update_epoch)
grace_period_end = max(reader["exit"] for reader in preexisting)

print(f"update-epoch={update_epoch}")
print("preexisting-readers=" + ",".join(reader["name"] for reader in preexisting))
print(f"grace-period-end={grace_period_end}")
print(f"post-update-reader-blocks={any(reader['enter'] > update_epoch and reader['exit'] <= grace_period_end for reader in readers)}")
print(f"safe-to-reclaim-after={grace_period_end}")
```

The executable interval model demonstrates that this simplified grace period waits for a preexisting reader rather than later readers. It does not implement RCU, model overlap at equal boundaries, publication, weak memory, preemption, interrupts, CPU tracking, callbacks, references, stalls, or real-time progress.

## Alternatives and Trade-Offs

- Reader-writer locks provide direct exclusion and immediate post-write reclamation but modify shared reader state; RCU minimizes reader coordination and defers memory release.
- Immutable whole-object replacement simplifies reader consistency but copies more state; in-place atomics or locks reduce allocation and complicate snapshots.
- Blocking synchronization gives a clear updater completion point but sleeps and raises latency; callbacks return promptly and transfer lifetime and backlog obligations.
- Ordinary RCU offers extremely cheap eligible readers but restricts blocking by flavor; sleepable RCU admits blocking readers at greater tracking cost.
- Grace-period batching amortizes coordination but increases individual callback latency; expedited periods reduce latency and disturb CPUs, energy, and scalability.
- RCU plus reference counts permits use beyond the read section but adds a delicate acquire-versus-final-release protocol; read-section-only use is simpler and narrower.
- Per-object locks allow mutable compound state and add acquisition to readers; copy-and-publish keeps readers lockless and makes writers allocate and validate versions.
- Callback offload reduces jitter on isolated CPUs but creates worker scheduling and queue-capacity dependencies; local invocation distributes service and perturbs those CPUs.
- Long readers simplify caller work but delay reclamation; short readers require explicit reference conversion or copying and improve progress.
- Strong runtime checking finds misuse but changes timing and resource demand; production configurations need independent observation and targeted validation.
- Backpressure bounds retired memory but slows updates; unrestricted update bursts preserve input rate until callback backlog threatens the system.
- RCU protects one kernel failure domain and memory lifetime; process-level epochs or garbage collection may suit userspace with different scheduling and fault assumptions.

## Failure Modes and Misconceptions

- **“RCU means no locks.”** Conflicting writers normally require separate serialization.
- **“Pointer assignment safely publishes an object.”** Use the matching ordered publication primitive after full initialization.
- **“An ordinary load safely dereferences an RCU pointer.”** It can lose required compiler or architecture constraints.
- **“Deletion means no reader has the object.”** Preexisting readers can retain it until they quiesce.
- **“A grace period waits for all readers.”** It covers readers that could predate its boundary under the chosen flavor.
- **“Grace-period completion drains callbacks.”** Callback execution can lag and needs a callback barrier for teardown.
- **“An RCU pointer can escape freely.”** Use after the section needs a stable reference or another lifetime protocol.
- **“RCU makes compound mutable reads consistent.”** It protects lifetime; versioning, sequences, or locks define snapshots.
- **“Reference increment always defeats deletion.”** Acquisition must safely reject or coordinate with the terminal zero transition.
- **“All RCU flavors are interchangeable.”** Reader contexts, sleep rules, quiescent states, and APIs differ.
- **“Expedited synchronization fixes a stuck reader.”** It cannot make an indefinitely blocked reader quiesce.
- **“Logical correctness bounds memory.”** Callback service below update rate grows retained backlog.
- **“One grace period makes module unload safe.”** Previously queued callbacks can still invoke module code.
- **“Torture success proves every access site.”** Static pointer flows and unexecuted paths still require review.

## Worked Examples

### Example 1

A routing-table writer builds a new immutable route set, publishes its root, waits for old readers through a callback, then frees the retired tree. Readers can use either complete version.

### Example 2

A list writer removes a device node while a reader already holds its pointer. The node remains allocated through a grace period, so traversal cannot touch freed memory.

### Example 3

Two writers copy the same old policy and publish different changes. A writer mutex prevents the later publication from silently losing the first update.

### Example 4

A lookup must return an object beyond the read-side section. It obtains a live reference while protected, validates nonterminal state, exits RCU, and later releases the reference.

### Example 5

A reader needs a coherent pair of mutable counters inside an RCU object. A sequence counter validates the pair while RCU protects the object's allocation lifetime.

### Example 6

A driver queues reclamation callbacks and begins unload. It blocks new queues, removes discoverability, drains outstanding callbacks, and only then unloads callback code.

### Example 7

A high-priority task prevents a preempted low-priority RCU reader from resuming. Grace-period age and callback memory grow until scheduling policy restores progress.

### Example 8

An expedited grace period sends stronger requests across a large idle system. Update latency falls, but wakeups and jitter rise, so the exceptional path is rate limited.

### Example 9

An offline CPU has queued callbacks. Hotplug transfers service responsibility and reports quiescence before destroying its tracking state.

### Example 10

Torture testing combines update floods, idle transitions, CPU hotplug, preemption, and forced stalls. A saved configuration and seed reproduce a callback-progress failure.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects epochs, immutable publication, memory models, read-mostly algorithms, and reclamation. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects linked traversal, versioned roots, reference counts, deletion, and concurrent maps.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects acquire-release ordering, cache locality, interrupts, idle states, and cross-CPU coordination. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects use-after-free, reference overflow, policy publication, and teardown attack surfaces.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies lifecycle analysis, progress hazards, configuration matrices, evidence, and assurance. Within this program, [OS-055](../ROADMAP.md) adds NUMA placement and [OS-060](../ROADMAP.md) uses RCU evidence in contention diagnosis.

## References

- Linux kernel documentation, [What is RCU?](https://docs.kernel.org/RCU/whatisRCU.html), current page checked 2026-09-04. Read-side sections, publication, dereference, grace periods, callbacks, removal, reclamation, and API foundations.
- Linux kernel documentation, [A Tour Through RCU's Requirements](https://docs.kernel.org/RCU/Design/Requirements/Requirements.html), current page checked 2026-09-04. Fundamental guarantees, parallelism, scalability, memory ordering, hotplug, idle, real-time, energy, flavors, and progress.
- Linux kernel documentation, [Review Checklist for RCU Patches](https://docs.kernel.org/RCU/checklist.html), current page checked 2026-09-04. Read-mostly fit, writer locking, publication, dereference, reader context, grace periods, callbacks, and review hazards.
- Linux kernel documentation, [Proper care and feeding of return values from rcu_dereference](https://docs.kernel.org/RCU/rcu_dereference.html), current page checked 2026-09-04. Dependency preservation, compiler transformation, comparisons, pointer use, specialized variants, and annotations.
- Linux kernel documentation, [Using RCU to Protect Read-Mostly Linked Lists](https://docs.kernel.org/RCU/listRCU.html), current page checked 2026-09-04. List traversal, insertion, deletion, replacement, reader semantics, locking, and delayed reclamation.
- Linux kernel documentation, [RCU and Unloadable Modules](https://docs.kernel.org/RCU/rcubarrier.html), current page checked 2026-09-04. Callback draining, module cleanup, grace periods versus callback execution, implementation, and unload ordering.
- Linux kernel documentation, [Reference-count design for elements protected by RCU](https://docs.kernel.org/RCU/rcuref.html), current page checked 2026-09-04. Lookup-to-reference acquisition, deletion races, terminal state, saturation, and RCU integration.
- Linux kernel documentation, [RCU and lockdep checking](https://docs.kernel.org/RCU/lockdep.html), current page checked 2026-09-04. Protected dereference validation, recognized reader contexts, conditions, lock-held variants, and runtime diagnostics.
- Linux kernel documentation, [Using RCU's CPU Stall Detector](https://docs.kernel.org/RCU/stallwarn.html), current page checked 2026-09-04. Stall causes, configuration, grace-period workers, real-time starvation, idle and timer faults, output, and diagnosis.
- Linux kernel documentation, [RCU Torture Test Operation](https://docs.kernel.org/RCU/torture.html), current page checked 2026-09-04. Reader and writer stress, callbacks, hotplug, idle, stalls, configurations, sanitizers, output, and reproducibility.

## Exercises

### Exercise 1

Design RCU protection for a read-mostly routing table with concurrent replacement, deletion, per-entry counters, and lookups that sometimes return durable references.

### Exercise 2

Specify safe module unload for a callback registry that uses RCU lists and asynchronous reclamation. Distinguish reader waits from callback draining.

### Exercise 3

Choose among ordinary, sleepable, and tasks-oriented RCU domains for task, softirq, NMI, sleeping, tracing, and code-lifecycle readers. State evidence needed.

### Exercise 4

Diagnose growing callback backlog and stall warnings on a real-time, no-tick, CPU-isolated system under update bursts.

### Exercise 5

Build a validation and assurance plan for an RCU conversion from a reader-writer lock. Include semantics, ordering, lifetime, progress, configurations, and performance.

## Answers to the Exercises

### Answer 1

Serialize route writers with a mutex or partitioned writer locks. Build an immutable table or bucket version privately, initialize every route and reference field, then release-publish the new root. Readers enter the selected RCU flavor, protected-dereference the root and route pointers, and may observe an old or new complete version. Per-entry statistics use independent atomics or per-CPU counters and do not mutate structural fields without their own protocol.

Deletion marks a route terminal under writer serialization if new durable references must stop, removes its reachability, and queues reclamation after a grace period. A returning lookup attempts a purpose-built increment-if-live while inside the read section, validates eligibility, then exits; the stable reference carries lifetime afterward. Final free waits for both removal's RCU obligation and the last durable reference. Tests race duplicate writers, replace, delete, lookup, reference acquisition, counter reads, resize, callback delay, allocation failure, and teardown without claiming one cross-table snapshot unless versioning provides it.

### Answer 2

First block new registry operations and callback submissions at the external entry boundary. Under writer serialization, unlink every registration with the RCU-aware deletion operation and publish terminal subsystem state. Wait for current readers when teardown needs proof that no read-side code retains registry objects. Release noncallback work only after its own cancellation and join protocol.

Then invoke the callback-barrier operation for the selected domain so every reclamation callback queued before the boundary has actually run. A grace-period wait alone is insufficient because an eligible callback may remain pending. No producer can queue a later callback after the barrier begins. Only then free registry storage, callback-owned resources, synchronization objects, and module code. Test unload during readers, updater rollback, callback floods, delayed callback workers, hotplug, and repeated load-unload.

### Answer 3

Build a context matrix rather than selecting by strength. Ordinary RCU serves supported kernel read contexts with its very cheap read-side path; check current rules for task preemption, softirq, hardirq, and NMI access. Sleepable RCU serves readers that must block or sleep and uses its matching independent domain and synchronization APIs. Tasks-oriented and tracing-sensitive variants serve code-lifecycle or tracing cases whose quiescent-state requirements concern task transitions rather than ordinary data traversal.

For every pointer, document flavor, reader entry and exit, blocking behavior, interrupt and NMI support, publication and dereference, updater context, grace-period or callback API, teardown drain, and configuration dependencies. Verify against current primary documentation and implementation, compile-time annotations, runtime RCU checking, configuration builds, targeted interrupt and sleep tests, hotplug and idle tests, and torture scenarios. Never mix a reader from one domain with reclamation from another merely because both APIs contain RCU in their names.

### Answer 4

Correlate grace-period sequence and age, CPUs or tasks awaiting quiescence, callback counts and age, RCU worker and softirq runtime, priorities, affinity, idle transitions, interrupts-disabled time, preempt-disabled regions, thermal state, timer delivery, and update source. Repeated stack traces can reveal a reader that cannot resume, a CPU-bound higher-priority task starving RCU service, an interrupt storm, a long nonpreemptible loop, or tracing and console overhead.

Separate grace-period stall from post-grace callback starvation. Reproduce with the same real-time priorities, no-tick and offload settings, isolation masks, CPU frequency, hotplug, tracing level, and update burst. Bound reader duration, give required RCU workers viable affinity and priority, offload callbacks deliberately, apply backpressure to update producers, and rate-limit expedited periods. Do not free retired state early. Validate fixes against latency, energy, isolation, memory backlog, and application throughput rather than merely suppressing warnings.

### Answer 5

Record the reader-writer-lock baseline: protected fields, legal reader snapshots, writer linearization, lock graph, lifetime, errors, contexts, and performance. For RCU, define immutable or independently synchronized fields, writer lock, full initialization, release publication, matching dereference, list or root removal, grace-period or callback reclamation, escaping reference acquisition, callback context, and unload drain. Model old-or-new observations and reject any newly possible mixed state outside the contract.

Use pointer annotations, static analysis, RCU lock checking, dependency and race detection, address and undefined-behavior sanitizers, callback-object debugging, memory-model litmus tests, and operation-history checking. Torture updates, readers, deletion, cancellation, callback floods, memory pressure, preemption, interrupts, idle and no-tick, CPU hotplug, suspend, real-time priorities, stalls, allocation failure, and unload. Measure read and write latency, grace periods, backlog and memory, CPU and cache traffic, energy, expedited effects, and tails across CPU and socket counts. Preserve code, configuration, flavors, topology, workload and seeds, pointer-flow review, traces, raw results, failures, reviewers, and limitations.
