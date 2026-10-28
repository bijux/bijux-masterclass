---
module_id: OS-025
program: Operating Systems
level: 1
module_number: 25
title: Deadlock Conditions and Avoidance
status: complete
last_verified: 2026-09-04
---

# Deadlock Conditions and Avoidance

## One-Page Review

### Governing question

How can an operating system prevent, avoid, detect, diagnose, or recover from cycles in which tasks hold resources while waiting for one another, without confusing deadlock with slow progress or turning recovery into corruption?

### Essential definitions

- A **deadlock** is a state in which a set of participants cannot progress because each waits for an event that only another participant in the set can cause.
- A **resource-allocation graph** contains task and resource nodes with request and assignment edges.
- A **wait-for graph** projects dependencies among participants; a directed cycle is sufficient for deadlock when each modeled resource has one relevant instance under the graph assumptions.
- **mutual exclusion**, **hold and wait**, **no preemption**, and **circular wait** are the classic necessary conditions for resource deadlock.
- **prevention** structurally breaks at least one necessary condition.
- **avoidance** grants requests only when the resulting state remains safe under declared maximum claims.
- **detection and recovery** permits deadlock, identifies it, then aborts, rolls back, preempts, or restarts selected work.
- **livelock** changes state without useful progress; **starvation** indefinitely denies one participant despite progress elsewhere.

### Central model, mechanism, or theorem

Let directed edge `T_i -> T_j` mean task `i` waits for a resource or event controlled by task `j`. A cycle `T_0 -> ... -> T_k -> T_0` demonstrates circular wait. With reusable single-instance resources and stable ownership, the cycle establishes deadlock; with multiple instances or transient dependencies, additional state is required.

Prevention can impose a global resource order, request all resources together, remove exclusive ownership where safe, or permit revocation with rollback. Avoidance needs maximum future claims and a safe-state test. Detection needs complete, current dependency evidence. Recovery needs a transaction or idempotence boundary; killing a holder does not automatically repair shared state.

### Critical invariants

- Every blocking edge names the waiter, resource generation, current owner or producer, and cancellation semantics.
- Global lock-class ordering is acyclic across normal, interrupt, callback, error, and teardown paths.
- Avoidance decisions use validated capacity, allocation, remaining need, and maximum-claim data from one coherent snapshot.
- Timeout and cancellation release or transfer every partially acquired resource exactly once.
- Detection distinguishes stable cycles from stale identifiers, missing events, and legitimate long waits.
- Recovery restores all shared invariants and external effects before resources become reusable.
- Watchdogs retain enough independent capacity and authority to observe and act during the failure.

### Common failures

Common mistakes are calling every long wait deadlock, checking only pairwise lock order, using trylock loops that livelock, treating timeout as prevention, assuming priority inheritance breaks cycles, applying Banker's algorithm without credible maximum claims, declaring any graph cycle sufficient with multiple resource instances, killing a task while it owns inconsistent state, ignoring callbacks and process-exit locks, and deploying a watchdog that depends on the same exhausted scheduler, allocator, or lock.

### Compact example

Task A holds R1 and waits for R2; task B holds R2 and waits for R1. The wait-for graph has `A -> B -> A`. A global rule `R1 < R2` permits acquiring R1 before R2 and rejects the reversed request, breaking circular wait for compliant paths. If dynamic transactions cannot know order, a wound/wait-style age policy can cause one transaction to back off and retry, but retry cleanup, starvation, and side effects still require proof.

### Connections

[OS-021](021-critical-sections-in-the-kernel.md) defines lock-class graphs, [OS-023](023-mutexes-semaphores-and-condition-variables.md) defines blocking primitives, and [OS-024](024-atomic-operations.md) distinguishes deadlock-free from stronger progress. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) extends dependency cycles across nodes and partial failure.

## Governing Question

Deadlock is a global property emerging from individually plausible actions. One function takes A then B; another callback takes B then A. Each lock works correctly and every thread sleeps as designed, yet the system reaches a state with no enabled transition.

Dependencies extend beyond mutexes. Tasks wait for semaphore capacity, condition predicates, child exit, file locks, memory reclaim, I/O completion, work queues, RPC replies, and teardown callbacks. A thread can wait on a future whose worker is queued behind the thread's own bounded executor.

The governing question is how to model the whole dependency graph, select an explicit prevention or management strategy, and prove that timeout, cancellation, and recovery preserve resource and data invariants.

## Why This Matters

Deadlock can freeze one request, a subsystem, or an entire machine. In privileged code it can block interrupt handling, memory reclaim, storage completion, or administrative recovery. Rare orderings make reproduction expensive.

Overly conservative prevention also costs. One global lock removes cycles but serializes work. Acquiring all resources up front lowers utilization. Avoidance needs claims that dynamic workloads may not know. Detection consumes state and recovery may discard work.

The right strategy depends on reversibility and consequences. A database transaction can roll back; a device command may not. A user job can be killed; a kernel lock holder may have left global state inconsistent. Assurance must name these boundaries.

## Prerequisites and Retrieval

Recall wait queues from [OS-015](015-process-states-and-wait-queues.md), lock-class graphs from [OS-021](021-critical-sections-in-the-kernel.md), blocking primitive ownership from [OS-023](023-mutexes-semaphores-and-condition-variables.md), and progress terms from [OS-024](024-atomic-operations.md).

Retrieve these distinctions:

- deadlock has no enabled progress inside a dependency set; starvation permits others to progress;
- livelock executes and changes state but fails to complete useful work;
- a timeout limits one wait duration but does not prove cycle freedom;
- lock ordering prevents circular wait only when every acquisition path complies;
- a safe state has some completion sequence; an unsafe state need not already be deadlocked;
- priority inheritance addresses inversion but cannot dissolve a circular dependency;
- detection and victim selection do not make recovery correct.

## Learning Objectives

After this module, you should be able to:

1. construct resource-allocation and wait-for graphs with correct resource multiplicity assumptions;
2. distinguish deadlock, livelock, starvation, long wait, and priority inversion;
3. apply each necessary condition to prevention designs;
4. perform a safe-sequence avoidance check from capacity, allocation, and maximum claims;
5. design detection evidence robust to stale identities, distributed snapshots, and missing events;
6. evaluate victim selection, rollback, revocation, restart, timeout, and watchdog recovery;
7. validate lock ordering with static review, lockdep, stress, fault injection, and scoped claims.

## Core Exposition

### Dependency graphs

A resource-allocation graph uses task-to-resource request edges and resource-to-task assignment edges. Resource instances matter: one mutex has one owner, while a semaphore or pool can have several units. A wait-for graph collapses a request through the current owner into a task dependency.

Graph identity needs generations. Task IDs, file descriptors, object addresses, and lock instances can be reused. Stale edges can create a false cycle; missing edges can hide a real one. Capture under synchronization or attach timestamps and validation rules.

### The four necessary conditions

Mutual exclusion means at least one resource cannot be shared compatibly. Hold and wait means a participant retains resources while requesting more. No preemption means resources are released voluntarily rather than safely revoked. Circular wait means a closed dependency chain exists.

All four are necessary in the classic reusable-resource model. Breaking one prevents that class of deadlock, but the chosen transformation must preserve application semantics. Making a non-shareable device “shareable” is not a valid proof.

### Preventing mutual exclusion

Immutable snapshots, copy-on-write data, message passing, lock-free reads, or multiplexed ownership can remove exclusive sharing. A spooler serializes a physical device behind a queue so clients need not hold it directly.

These designs move, rather than erase, coordination. The spooler can deadlock on storage or bounded queues. Lock-free structures need ordering and reclamation. State the new dependency graph.

### Preventing hold and wait

Acquire all required resources atomically or release held resources before requesting another. This can prevent cycles but lowers utilization, expands acquisition scope, and may require knowing the complete resource set.

Rollback must undo partial effects, not merely unlock. External device, network, and persistent side effects may be irreversible or require compensation.

### Permitting preemption

CPU time and memory pages can sometimes be revoked or rescheduled. Mutex-protected in-memory invariants generally cannot be taken from an arbitrary owner safely. Transactional state can be aborted if undo or redo is complete.

Wound/wait policies use transaction age to decide who waits or backs off when multiple locks are acquired without a fixed order. The victim releases all acquired resources, rolls back, and retries under starvation controls.

### Preventing circular wait

Assign every lock class a durable rank and acquire in increasing order. Include callbacks, interrupts, error paths, and teardown. For dynamic sets, sort by stable identity under rules that handle key reuse and object destruction.

One order must cover the transitive graph. Reviewing only A-B pairs independently misses A-to-B, B-to-C, C-to-A. Condition waits release one mutex but can introduce event dependencies outside lock order.

### Avoidance and safe states

Avoidance reasons about future claims. Given available vector `V`, current allocation `A_i`, and maximum claim `M_i`, remaining need is `N_i=M_i-A_i`. Repeatedly find a task with `N_i <= V`, assume it finishes, and add its allocation back to `V`. If all tasks can finish, the snapshot is safe.

An unsafe state has no demonstrated safe sequence but may still complete depending on future requests. Maximum claims must be credible and stable. Dynamic resources, unknown callbacks, interrupts, and external services often make classic avoidance impractical.

### Detection

For single-instance reusable resources, a wait-for cycle is sufficient under stable ownership assumptions. With multiple instances, use allocation and request matrices or another model; a cycle alone may be only necessary. Distributed detection must build a consistent-enough snapshot despite messages in flight and participant failure.

Detection interval trades overhead against outage duration. Event-driven tracking is current but invasive; periodic scanning can miss transient cycles or report stale ones. Validate suspected cycles with stacks, owners, state, and generations.

### Recovery and victim selection

Choose a victim based on reversibility, priority, completed work, resources held, restart cost, deadline, tenant policy, and safety consequences. Fairness and repeated-victim starvation matter. Never make victim choice from PID order alone without a documented reason.

Recovery can roll back a transaction, cancel an operation, revoke a recoverable resource, restart a service, fence a node, or reboot a subsystem. Shared invariants, durable effects, locks, callbacks, and peer-visible results must reach a consistent terminal state.

### Timeouts

A timeout converts an infinite local wait into an outcome after a deadline. It can aid detection and containment, but all participants can time out, retry in synchrony, and recreate the cycle. Partial ownership can leak unless cleanup is exact.

Use randomized or ordered backoff where appropriate, bounded retries, idempotent operations, and one-winner resolution. A timeout value is an operational policy tied to service objectives, not proof of deadlock avoidance.

### Livelock and starvation

Two polite tasks can repeatedly release and reacquire resources for each other, producing livelock. Trylock loops with identical backoff can synchronize collisions. Randomization, priority, tokens, or ordered contention can enable progress.

Starvation occurs when policy continuously favors others. A deadlock detector may see no cycle. Measure per-participant progress and maximum denial; fairness mechanisms differ from cycle prevention.

### Priority inversion

High task H waiting on low holder L is inversion. Priority inheritance can accelerate L. If L waits for H through another resource, donation raises priorities but the cycle remains. Deadlock and inversion can coexist.

Response-time analysis includes bounded blocking from acyclic resource protocols. An unbounded cycle invalidates the task model rather than becoming a larger blocking term.

### Kernel lock dependency analysis

Linux lockdep models lock classes, nesting dependencies, and context state along executed paths. It can report circular dependencies before a runtime deadlock occurs. Correct class annotations and broad path coverage are essential.

Lockdep does not model every event, userspace resource, external service, or unexecuted path. A clean run complements design review and static analysis.

### Wound/wait mutexes

Linux wound/wait mutex documentation addresses transactions that need multiple locks in arbitrary order, such as shared buffer reservations. An acquisition context carries ordering information; conflicts can cause younger contexts to back off under the selected algorithm.

Callers must follow slow-path and retry rules, release acquired locks, and avoid side effects that cannot be rolled back. The mechanism is not a generic replacement for simple global ordering.

### File and process locks

Record locks and file locks have process, open-file-description, inheritance, conversion, and network-filesystem semantics. Linux documents deadlock detection for selected blocking record-lock cases, with limitations. Mixing `flock`, record locks, and application mutexes creates dependencies one subsystem may not see.

Process exit can release some locks, but robust application invariants still need recovery. Fork, exec, duplicated descriptors, and remote servers change ownership semantics.

### Executor and callback deadlocks

A task in a bounded worker pool can submit work to the same pool and wait while all workers do likewise. No mutex cycle is required; each waits for queued work that cannot start. Reserve capacity, avoid synchronous nested waits, or use work-first execution.

Callbacks called under a lock can acquire unknown resources or reenter the subsystem. Invoke external code outside internal locks or specify strict callback contracts and ownership snapshots.

### Memory reclaim and I/O dependencies

Kernel allocation can trigger reclaim or writeback, which may need locks or I/O held by the allocator. Allocation modes and reserve pools encode dependency constraints. Sleeping allocation under a lock can create a cycle far outside the local source file.

Device completion may require interrupts or workers starved by current priority or CPU affinity. Dependency review must include execution capacity, not only objects.

### Watchdogs and diagnosis

Lockup watchdogs, hung-task reports, SysRq stack dumps, lock owners, scheduler traces, and wait-channel data provide evidence. A watchdog must run independently enough to observe the stuck system and have bounded memory, CPU, lock, and logging dependencies.

Capture task stacks, lock classes and owners, wait queues, IRQ state, work queues, resource counters, recent events, and configuration. Protect sensitive data and avoid making logging part of the deadlock.

### Distributed deadlock

RPC and lease dependencies cross machines. Network delay and partition make “waiting” ambiguous. Detection needs a snapshot or probe algorithm, unique transaction generations, and failure-detector assumptions. Leases bound ownership only if clocks, renewal, fencing, and external side effects are controlled.

Fencing prevents a recovered or partitioned participant from continuing with stale authority. Killing one client without fencing can create split-brain corruption rather than recovery.

### Security and assurance

Attackers can exhaust pools, acquire file locks, trigger nested callbacks, or force diagnostic storms. Admission, quotas, ownership, timeouts, and recovery authority are security controls.

Safety-relevant systems need bounded resource graphs, recovery effects, independent monitoring, and named acceptance. A cycle detector or watchdog is evidence, not certification.

## Definitions and Notation

Let tasks be `T={T_1,...,T_n}` and resource types `R={R_1,...,R_m}`. In a wait-for graph `G=(T,E)`, edge `(T_i,T_j)` means `T_i` awaits progress controlled by `T_j`. Let available vector be `V`, allocation vector for task `i` be `A_i`, maximum claim `M_i`, and remaining need `N_i=M_i-A_i`.

A safe sequence is a permutation of tasks such that each next task's remaining need is no greater componentwise than current available plus allocations returned by earlier completions. Safety is relative to truthful maximum claims and the modeled resource system.

Let recovery cost `C_i` include lost work, rollback, resources, priority, safety, and repeated-victim history. A cost function cannot replace policy ownership or prove rollback correctness.

## Mechanisms, Invariants, or Proof Structure

A deadlock review follows eight obligations:

1. Inventory reusable resources, capacities, owners, waiters, generations, and non-resource event dependencies.
2. Build the global graph across tasks, interrupts, callbacks, executors, I/O, reclaim, processes, and nodes.
3. Choose prevention, avoidance, detection and recovery, or a justified combination for each domain.
4. Prove global ordering or safe-state arithmetic with every required assumption.
5. Distinguish cycles, multiple instances, stale evidence, livelock, starvation, and inversion.
6. Define timeout, cancellation, rollback, victim, retry, fencing, and exactly-once cleanup.
7. Ensure diagnostics and watchdogs retain independent execution and storage capacity.
8. Validate paths and failures while labeling detection coverage and assurance limits.

The executable graph model shows circular wait and a rank rule that rejects the reversed acquisition.

<!-- bijux-verify: {"id":"toy-deadlock-cycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"wait-for-cycle=A->B->A\norder-policy=R1<R2\nreversed-request=rejected\n","stderr":""}} -->
```python
edges = {"A": "B", "B": "A"}
path = []
seen_at = {}
node = "A"
while node not in seen_at:
    seen_at[node] = len(path)
    path.append(node)
    node = edges[node]
cycle = path[seen_at[node]:] + [node]

rank = {"R1": 1, "R2": 2}
held = "R2"
requested = "R1"
allowed = rank[held] < rank[requested]

print("wait-for-cycle=" + "->".join(cycle))
print("order-policy=R1<R2")
print("reversed-request=" + ("allowed" if allowed else "rejected"))
```

The toy assumes two single-instance resources, stable ownership, complete edges, and compliant rank checks. It does not implement locks, multiple instances, distributed detection, or recovery.

## Alternatives and Trade-Offs

- Global ordering is auditable but can force awkward acquisition and reduce modularity.
- All-at-once allocation prevents hold-and-wait but lowers utilization and needs known resource sets.
- Revocation improves progress only for resources with correct rollback or compensation.
- Avoidance preserves safe states but needs credible maximum claims and coherent snapshots.
- Detection permits concurrency and simple acquisition while accepting outage and recovery cost.
- Timeouts bound local waits but introduce false aborts, retry storms, and cleanup complexity.
- Wound/wait supports dynamic lock sets but requires transactional retry discipline.
- Coarse locking shrinks graph complexity while serializing unrelated work.
- Watchdogs improve detection but need independent capacity and safe recovery authority.

## Failure Modes and Misconceptions

1. **“A long wait is deadlock.”** slow I/O, starvation, or overload can eventually progress.
2. **“Any cycle proves deadlock.”** resource multiplicity and transient edges affect sufficiency.
3. **“No mutex cycle means no deadlock.”** executors, conditions, I/O, and RPC create event cycles.
4. **“Pairwise order review is enough.”** longer global cycles remain.
5. **“Trylock prevents deadlock.”** retry can livelock or starve.
6. **“Timeout prevents cycles.”** it detects or aborts one wait after the cycle formed.
7. **“Priority inheritance resolves deadlock.”** it accelerates holders but cannot break circular wait.
8. **“Unsafe state is deadlocked.”** it lacks a guaranteed safe sequence but may still finish.
9. **“Banker's algorithm always applies.”** dynamic systems may lack truthful maxima and revocable assumptions.
10. **“Kill one task and continue.”** protected and external state may be inconsistent.
11. **“Process exit cleans every lock.”** ownership and recovery semantics vary.
12. **“Lockdep proves global freedom.”** external and unexecuted dependencies remain.
13. **“Watchdog guarantees recovery.”** it may share the failed resources or worsen corruption.
14. **“No detected cycle proves no deadlock.”** evidence can be stale, incomplete, or scoped.

## Worked Examples

### Example 1

A holds R1 and waits R2; B holds R2 and waits R1. With one instance each and stable ownership, the wait-for cycle is sufficient. Ordering R1 before R2 rejects B's earlier reversed acquisition.

### Example 2

Two tasks both wait for a semaphore with two instances, while a third holder will release one. A projected cycle-like resource graph does not prove deadlock without instance and holder state.

### Example 3

A safe-state check finds task C's remaining need fits available resources, then returns C's allocation, enabling A, then B. Granting a new request that removes all possible completion sequences would be denied.

### Example 4

Two trylock loops acquire opposite first locks, fail the second, release, and retry on identical timers. They run continuously without useful progress: livelock, not blocked deadlock.

### Example 5

High H and low L form a lock cycle. Priority inheritance raises L, but L waits for H, so neither releases. The resource graph, not priority, determines deadlock.

### Example 6

All four executor workers submit child work to the same queue and synchronously wait. Children cannot start. Reserving a worker or executing nested work inline breaks the capacity dependency.

### Example 7

A wound/wait transaction loses a conflict and releases three reservation locks before retry. If it sent an irreversible device command before the conflict, lock release alone cannot roll back the transaction.

### Example 8

A record-lock detector reports a cycle among local processes, but one application mutex and a remote NFS dependency complete a larger cycle outside its model. Cross-layer diagnostics are required.

### Example 9

A hung-task warning triggers a stack dump, but logging allocates memory while reclaim is part of the cycle. Preallocated bounded diagnostic buffers preserve evidence without joining the deadlock.

### Example 10

A distributed recovery fences an old storage owner before promoting a replacement. Without fencing, the partitioned old owner could resume and corrupt shared state despite the detector choosing a victim.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops distributed snapshots, failure detection, leases, fencing, transactions, and partial failure. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames resource exhaustion and recovery authority.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies hazard analysis, degraded modes, independent monitors, and assurance. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops progress, lock ordering, and transactional retry.

Within this program, later IPC, memory, filesystem, driver, and virtualization modules apply these dependency and recovery models to broader resources.

## References

- Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, [Common Concurrency Problems](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf), *Operating Systems: Three Easy Pieces*, current PDF checked 2026-09-04. Deadlock conditions, prevention, ordering, all-at-once acquisition, trylock, and scheduling control.
- POSIX via Linux man-pages, [pthread_mutex_lock(3p)](https://man7.org/linux/man-pages/man3/pthread_mutex_lock.3p.html), current page checked 2026-09-04. Mutex types, ownership, deadlock errors, robust state, and priority protocols.
- POSIX via Linux man-pages, [pthread_mutex_timedlock(3p)](https://man7.org/linux/man-pages/man3/pthread_mutex_timedlock.3p.html), current page checked 2026-09-04. Timed acquisition, timeout, priority effects, clock, robust state, and errors.
- Linux man-pages project, [fcntl_locking(2)](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html), current page checked 2026-09-04. Advisory record locks, blocking, deadlock detection, open-file-description locks, signals, and limitations.
- Linux man-pages project, [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html), current page checked 2026-09-04. Whole-file locking, descriptor and process behavior, conversion, fork, exec, and network filesystem semantics.
- Linux Kernel documentation, [Lockdep Design](https://docs.kernel.org/locking/lockdep-design.html), current page checked 2026-09-04. Lock classes, dependency chains, circular validation, context state, recursion, and annotations.
- Linux Kernel documentation, [Generic Mutex Subsystem](https://docs.kernel.org/locking/mutex-design.html), current page checked 2026-09-04. Ownership, fast and slow paths, optimistic spinning, implementation, and API rules.
- Linux Kernel documentation, [RT-mutex Implementation Design](https://docs.kernel.org/locking/rt-mutex-design.html), current page checked 2026-09-04. Priority inheritance, waiter graphs, owner state, chain walking, and locking.
- Linux Kernel documentation, [Wound/Wait Mutex Design](https://docs.kernel.org/locking/ww-mutex-design.html), current page checked 2026-09-04. Arbitrary lock sets, acquisition contexts, wound-wait and wait-die, retry, and API use.
- Linux Kernel documentation, [Unreliable Guide To Locking](https://docs.kernel.org/kernel-hacking/locking.html), current page checked 2026-09-04. Contexts, locks, callbacks, reference counting, deadlocks, and common failure patterns.
- Linux Kernel documentation, [Softlockup and Hardlockup Watchdogs](https://docs.kernel.org/admin-guide/lockup-watchdogs.html), current page checked 2026-09-04. Watchdog mechanisms, thresholds, configuration, hard and soft lockup detection, and CPU scope.
- Linux Kernel documentation, [Linux Magic System Request Key Hacks](https://docs.kernel.org/admin-guide/sysrq.html), current page checked 2026-09-04. Emergency task, lock, memory, CPU, and system diagnostic and control commands.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching lock ordering, sleep and wakeup, file and process locks, buffer cache, logging, and deadlock cautions.

## Exercises

### Exercise 1

Build a resource-allocation and wait-for graph for tasks using mutexes, semaphore units, executor slots, and I/O completion. State exactly when a cycle is sufficient.

### Exercise 2

Apply a safe-state avoidance check to a three-resource, five-task snapshot. Validate totals, compute remaining need, find all safe sequences, then evaluate one additional request.

### Exercise 3

Redesign an AB-BA callback and teardown system using global order, ownership transfer, or transactional retry. Prove cleanup and lifetime.

### Exercise 4

Design deadlock, livelock, starvation, and inversion diagnostics using lockdep, watchdogs, stacks, trace events, and progress counters. State false-positive and false-negative risks.

### Exercise 5

Construct an assurance review for deadlock management in a safety-relevant distributed controller. Cover fencing, rollback, monitoring, overload, evidence, and human judgment.

## Answers to the Exercises

### Answer 1

Create task nodes and resource-instance nodes. Assignment edges point from each concrete mutex, semaphore unit, executor worker, or device completion owner to its task; request edges point from waiter to the exact resource or event. Project to task edges only when the current owner or required producer is known. Include queued child work as dependent on an available worker.

A wait-for cycle is sufficient when each dependency is stable, exclusive, and cannot be resolved by a participant outside the cycle, commonly single-instance reusable resources. Multiple semaphore units, time-varying producers, cancellation, and external interrupts require allocation counts and transition state. Unique generations prevent stale PID or object reuse from fabricating edges.

### Answer 2

First verify for each resource that total capacity equals available plus all allocations, and `0 <= A_i <= M_i`. Compute `N_i=M_i-A_i`. Starting with work vector V, repeatedly choose every unfinished task whose need is componentwise no greater than work, append it, and add its allocation to work. Backtrack choices to enumerate all safe sequences.

For an additional request, require request no greater than remaining need and available, tentatively subtract it from V and add it to allocation, then rerun the safe-sequence search. Grant only if the resulting snapshot is safe under the declared maximum-claim model. Missing or dishonest maxima invalidate the conclusion.

### Answer 3

Do not call external callbacks under internal locks. Under A, snapshot callback references and required immutable state; release A; invoke callbacks; reacquire only to commit under a generation check. Teardown closes callback registration, removes discoverability, waits for snapshot references, then destroys state. Internal paths acquire A before B everywhere if both remain necessary.

If operations require dynamic sets, attach a wound/wait acquisition context, acquire with the documented retry protocol, and keep effects rollback-safe until all locks are held. On conflict, release every acquired lock, undo provisional state, back off under starvation policy, and retry. Exactly-once external effects occur only after the transaction can no longer abort or use idempotent identifiers.

### Answer 4

Deadlock evidence combines lockdep class cycles, task stacks, current owners, wait queues, executor occupancy, I/O state, and a stable wait-for snapshot. Livelock needs execution and state-change counters without completion. Starvation needs per-task eligible time and service while peers progress. Inversion needs priority and resource-owner chains plus blocking duration.

Watchdogs record bounded preallocated evidence and must retain CPU and logging capacity. Trace correlation uses generations and detects loss. Lockdep misses unexecuted and external dependencies; periodic graphs can be stale; watchdog thresholds flag legitimate long work; sampling misses brief states. Fault injection and deterministic model tests expand coverage without proving absence.

### Answer 5

Inventory local locks, executor pools, devices, network calls, leases, and external actuators. Prevent cycles with ranked local resources and bounded admission; use transactional retry only where rollback is complete. Distributed detection states snapshot and failure-detector assumptions. Fence old authority before replacement and use idempotent generation-tagged commands.

Define overload, partition, lost monitor, false suspicion, rollback failure, repeated victim, actuator uncertainty, and safe-state behavior. Keep independent watchdog capacity and protected evidence. Combine static graph review, model checking, lockdep, stress, fault injection, partition tests, and recovery drills; observations remain scoped. Named kernel, distributed-systems, concurrency, device, real-time, security, safety, independent-verification, and acceptance owners assess assumptions and residual risk. This chapter claims no certification.
