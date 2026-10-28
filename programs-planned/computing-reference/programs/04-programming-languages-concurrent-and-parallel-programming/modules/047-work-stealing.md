---
module_id: CONPAR-047
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 47
title: Work Stealing
status: complete
last_verified: 2026-08-29
---

# Work Stealing

## One-Page Review

### Governing question

How can idle workers obtain ready tasks from busy workers without centralizing every dispatch, while preserving exactly-once ownership, locality, progress, bounded overhead, deterministic meaning, and complete termination?

### Essential definitions

- **Work stealing** is decentralized load balancing in which an idle worker (thief) takes ready work from another worker (victim).
- A **work-stealing deque** supports fast owner operations at one end and concurrent thief steals at the other.
- **Owner push/pop** commonly follows LIFO order for locality; **steal** commonly takes older/coarser work from the opposite end.
- A **steal attempt** selects/probes a victim; it can fail because the victim is empty or loses a race.
- The **last-item race** occurs when owner pop and thief steal contend for the sole remaining task.
- **Victim selection** is the policy for choosing which worker or hierarchy to probe.
- A **work-first** policy minimizes overhead on the ordinary work path, often placing overhead on steals/critical path under a specific runtime design.
- A **fully strict computation** joins children within their parent’s dynamic extent; classical work-stealing bounds rely on this structure.
- **In-transit work** has been logically transferred but not yet visible/executing at the destination.
- **Termination detection** distinguishes globally no possible work from temporarily empty local queues.

### Central model, mechanism, or theorem

Each ready task has one logical deque/worker owner. The owner pushes/pops one end; thieves contend at the other. Successful steal linearizes one ownership transfer, so only thief or owner receives a last task. For fully strict computations under the cited randomized scheduler/cost model, expected execution time is `T1/P+O(T_infinity)` and expected steals scale with critical-path opportunity rather than total work. These are scoped theoretical results, not guarantees for arbitrary deques, blocking I/O, general DAGs, priorities, weak-memory bugs, NUMA, or real runtimes.

### Critical invariants

Every ready task is reachable from exactly one owned queue, running worker, transfer, or terminal ledger state. Push, pop, and steal have declared linearization and visibility. The last item cannot execute twice or disappear. Buffer resize/reclamation cannot expose freed or stale storage. Task identity and result meaning never depend on worker or execution order. Steal probing is bounded/backed off and does not starve local or priority work. Blocking tasks do not consume all workers needed for ready compute. Cancellation settles queued, stolen, and running tasks. Global termination requires no active, queued, spawning, or in-transit obligations.

### Common failures

Code uses a normal deque concurrently; races owner and thief on the last slot; publishes an index before task storage is visible; reuses a ring slot while a thief can read it; frees an old resize buffer too early; assumes stealing is FIFO globally; stores semantic state in thread-local worker identity; steals tiny cache-hot tasks; probes empty victims in lockstep; treats local emptiness as completion; adds priorities that thieves ignore; blocks every worker on I/O/child joins; cancels only the source deque after tasks were stolen; or quotes a work-stealing theorem for a general networked service.

### Compact example

Worker 0 owns deque `[A,B,C,D]`, worker 1 owns `[E]`, worker 2 is empty. Owners pop right; thieves steal left. Worker 2 steals older task A; worker 1 executes E; worker 0 executes D. Worker 1 then steals B, while worker 0 executes C. Every task executes once, all deques empty, and stolen work is coarse/old while owner work remains depth-first/local. This deterministic teaching trace models neither concurrent deque races nor runtime speedup.

### Connections

[Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md) supplies the benefit/cost ledger; [Fork-Join Computation](043-fork-join-computation.md) supplies fully strict spawn trees. The [program roadmap](../ROADMAP.md) next develops pipeline parallelism.

## Governing Question

How should a work-stealing runtime and its clients define task ownership, deque concurrency, victim search, progress, lifecycle, and evidence so decentralized balancing improves irregular finite computation without weakening correctness?

Stealing transfers an obligation, not merely an array element.

## Why This Matters

Static assignment performs well for predictable uniform work but strands capacity when recursive or irregular tasks vary. A global ready queue permits redistribution but can become a synchronization and locality bottleneck. Work stealing puts most scheduling operations on private/local deques and invokes cross-worker coordination mainly when a worker lacks local work.

This is a natural fit for recursive fork-join, parallel collections, search trees, compilers, rendering, and finite task graphs with enough overdecomposition. Depth-first owner execution preserves locality/space, while thieves take older subtrees with enough work to amortize migration.

The mechanism is deceptively subtle. A concurrent deque is a memory-ordering/reclamation algorithm. A worker can appear empty while work is being spawned or transferred. Blocking can exhaust the worker set. Random victim probing can waste significant capacity near termination. Client code can be race-free yet nondeterministic because it assumes stable worker identity. Correct use needs both runtime invariants and application result/lifecycle contracts.

## Prerequisites and Retrieval

Retrieve:

- atomic ownership transitions from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- safe visibility and task publication from [Visibility and Publication](024-visibility-and-publication.md);
- bounded worker pools from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md);
- cancellation from [Cancellation and Timeouts](036-cancellation-and-timeouts.md);
- fork/join structure from [Fork-Join Computation](043-fork-join-computation.md);
- partition grain from [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md); and
- scheduler accounting from [Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md).

Retrieval prompt: trace one task through created, owner deque, last-item contention, stolen/in-transit, running, spawning children, cancellation, and terminal states; at every transition name the sole owner and visibility edge.

## Learning Objectives

After completing this module, a learner can:

1. explain why owner LIFO and thief opposite-end access support locality and coarse steals;
2. specify task/deque ownership and the last-item linearization race;
3. identify publication, resize, wraparound, ABA, and reclamation obligations;
4. state the assumptions and meaning of classical expected work-stealing bounds;
5. compare randomized, round-robin, load-aware, and hierarchical victim selection;
6. choose task grain and backoff from successful/failed steal and locality evidence;
7. preserve deterministic public results despite nondeterministic task placement;
8. integrate blocking, priorities, fairness, cancellation, and exceptions safely;
9. design correct global termination detection with spawned/in-transit work; and
10. verify protocol state with model checking/stress plus causal runtime measurements.

## Core Exposition

### Local deques and decentralized balance

Each worker maintains a deque of ready tasks. A running worker pushes newly exposed tasks and selects local work without contending on a global queue in the common case. An idle worker chooses another deque and attempts to steal.

The design distributes both state and synchronization. It avoids one central head/tail but adds victim discovery, failed probes, cross-core cache traffic, and distributed termination. It is not “no scheduler”; scheduling work moves into worker loops and deque protocols.

External submissions, priorities, timers, I/O readiness, and pinned tasks may still use injection queues or specialized lanes. Define how external work becomes visible and how workers are awakened.

### Owner LIFO, thief FIFO-like stealing

Recursive computation often pushes a child/continuation and follows depth-first work. Popping newest local tasks improves cache/stack locality and limits live frontier. Thieves take oldest work from the opposite end, often obtaining a larger upper-tree subtree rather than a tiny leaf.

The terms LIFO/FIFO describe operations relative to one deque, not a global execution order. Concurrent pushes, pops, and steals create many legal orders. Runtime variants may use different continuation policy or batch steals.

Application correctness cannot assume the owner executes its newest task, that a stolen task runs immediately, or that older tasks finish first. Stable logical IDs carry ordering semantics.

### Abstract deque state

A common bounded-ring abstraction has bottom index primarily owned by the local worker and top index shared with thieves. Owner push stores task then publishes new bottom. Owner pop tentatively decrements bottom; if more than one item remains it owns the item, but at one item it races thieves through an atomic top update. Thief reads top/bottom and atomically claims top.

Exact algorithms differ. Treat this as an explanatory state machine, not copy-ready implementation. Index arithmetic, signed/unsigned overflow, memory-order fences, buffer pointers, and resize rules are platform/language-specific.

Empty means `bottom<=top` under a consistent observation. A stale snapshot can report empty/nonempty incorrectly unless algorithm proofs and atomic ordering cover it.

### The last-item race

With one task, owner pop and one or more thieves may concurrently attempt to claim it. There must be one winner. A compare-and-swap on top or equivalent linearization decides. The loser restores/observes empty state and cannot return the task.

If both return it, execution duplicates. If neither returns it, work disappears and termination can be wrong. If task publication is not visible before index publication, thief can read uninitialized/stale storage.

This race is the core boundary between single-owner fast operations and multi-party synchronization. It deserves state-machine tests and weak-memory proof, not just load testing.

### Memory ordering and publication

Task fields and deque slot must be initialized before thieves can observe the published boundary. Release/acquire or stronger synchronization provides visibility as required by the algorithm. Relaxed atomics may manage indices only where proof establishes ordering through other fences.

Compiler/hardware memory models differ. An algorithm correct under sequential consistency can fail on ARM/POWER or compiler reordering. Use a validated implementation for the language/platform. Unsafe low-level code needs a written proof tied to specification and architecture plus tooling/model tests.

Stealing a task publishes its owned inputs/results according to the task runtime contract. Shared mutable references inside the task still require their own synchronization.

### Resize and memory reclamation

A ring becomes full and may grow. Owner allocates a larger buffer and copies logically live slots, then publishes the new buffer. Thieves holding the old buffer pointer may still read it. Immediate free causes use-after-free.

Strategies retain old buffers until pool destruction, use epochs/hazards/reference counting, or prove quiescence. Retention simplifies safety but can grow memory across repeated expansions. Bound maximum deque/tasks or reclaim safely.

Indices can wrap, and slot reuse creates ABA-like ambiguity. Use sufficiently wide monotonic indices with proved lifetime bounds or generation/version techniques. “It will not wrap in practice” needs a quantified run-rate/lifetime bound.

### Task creation and work-first policy

Forking exposes a child and a continuation. Runtime design chooses which runs now and which becomes stealable. Work-first principles place minimal overhead on the work term `T1`, accepting overhead on steals/span paths because successful steals are expected to relate to `P*T_infinity` under the model.

This principle guides runtime engineering; it is not a license for unbounded task creation. Sequential cutoffs and lazy spawning keep work and memory bounded. User callbacks, allocation, and effect costs can dwarf deque operations.

The public program must behave identically whether a task executes inline/local or is stolen. Any stable-worker assumption violates substitutability.

### Classical expected bounds

Blumofe and Leiserson analyze randomized work stealing for fully strict multithreaded computations. Under their model, expected time is `T1/P+O(T_infinity)`; expected communication/steal behavior and space also receive scoped bounds.

Interpretation: total work amortizes across processors, while critical-path structure bounds the extra successful-steal opportunity. It does not say every run meets the expectation, every victim policy works, or steals are free.

Assumptions exclude arbitrary general DAG dependencies, blocking system calls, long-lived services, priority constraints, heterogeneous processors, external effects, garbage-collection pauses, memory bandwidth, NUMA, weak-memory implementation bugs, and adversarial scheduler/runtime interactions. State the theorem's model whenever using it.

### Victim selection

Uniform random victim selection underpins classic analysis and avoids deterministic lockstep patterns. It can repeatedly probe empty workers and cross NUMA boundaries. Pseudorandom generators, seeds, and concurrent correlations affect implementation evidence, not program semantics.

Round-robin is predictable but idle workers can synchronize into convoys. Load-aware selection needs current summaries whose measurement/communication cost and staleness may outweigh benefit. “Power of two choices” samples candidates and chooses a more loaded one under a proxy.

Hierarchical policies search local core/socket/NUMA group before remote groups, trading locality against balance. Backoff after failed attempts avoids burning capacity but increases wake latency. Record policy, probe counts, success, victim distance, and stolen task size.

### Steal granularity

Stealing one task minimizes transfer but can cause repeated probes. Stealing half or a batch amortizes victim synchronization and supplies local work, but may over-transfer, worsen locality, or recreate imbalance.

Recursive old-end tasks often represent large subtrees. Flat microtask workloads may need batch stealing. Bound batch by queue length, estimated cost, bytes, destination capacity, and priority.

Grain is inseparable: if tasks are smaller than steal/cache costs, dynamic balance loses. Measure successful and failed steal resource-time, task useful time, cache/NUMA after steal, and critical-path benefit.

### Contention and scalability

Multiple thieves targeting one victim contend on top/index/cache lines. Popularity can arise when load-aware state identifies one busy worker. Randomization and backoff spread probes. Batch transfer reduces frequency but holds more work locally.

Owner operations are not free: top/bottom share cache lines unless layout separates them; last-item synchronization adds a slow path. False sharing with unrelated worker metadata matters.

Lock-free deque progress does not imply starvation-free task scheduling. A particular thief can fail repeatedly; a task buried under local LIFO spawning can wait unless stealing/fairness exposes it. Define fairness requirements separately.

### Deterministic program meaning

Worker assignment, stealing, and completion order are intentionally nondeterministic. Pure tasks with disjoint outputs can store by logical index. Reductions need valid algebra and order policy. Diagnostics/errors carry source identity and are sorted/selected deterministically if the product requires it.

Thread-local random streams, caches, or accumulators must not make meaning depend on worker. Counter-based/splittable random streams derive from task identity. Worker-local scratch may optimize only if initialized/cleared and invisible to semantics.

“First result” in parallel search is schedule-dependent. Use minimum/priority result with proved pruning if deterministic choice matters.

### Priorities and fairness

Plain deque order does not provide global priority. High-priority task on one worker can wait while others steal lower work elsewhere. Priority-aware multiple deques, global injection, donation, or reserved lanes complicate theft and theoretical assumptions.

Strict priority can starve ordinary or cleanup tasks. Aging/quotas/reservations protect progress. Pinned tasks cannot be stolen and can imbalance. Deadline-aware work may require another scheduler.

Do not retrofit priorities by reordering tasks whose program semantics require dependencies. Readiness and scheduling priority remain separate.

### Blocking, suspension, and helping

A CPU work-stealing worker waiting at a fork/join may help execute ready tasks, avoiding fixed-pool child starvation. Blocking on I/O/locks can still remove capacity because the runtime may not know it can help.

Managed-blocking APIs can compensate with workers, but compensation must be bounded and cannot fix locks/resources required by other tasks. Prefer async suspension or dedicated blocking resources for long waits.

Async runtimes also use local queues/stealing, but pollable tasks, wakers, I/O drivers, cooperative budgets, and thread-affine resources change the model. Do not transfer strict fork-join theorem claims automatically.

### Cancellation and failure

Once a task is stolen, cancelling only the origin deque misses it. Cancellation belongs to task/scope identity, observed regardless of current worker. Queued cancellation either removes safely or leaves a tombstoned task that becomes terminal when claimed.

Running tasks cooperate at safe points. On failure, structured scope signals siblings, stops spawning, joins/settles all descendants, aggregates errors stably, and reclaims deque/task state. Panics/exceptions follow runtime contracts.

Steal transfer races cancellation: define whether cancellation mark travels with task, lookup is shared, and which terminal ledger transition wins. Never execute effects twice after uncertain transfer/retry.

### Termination detection

One empty deque does not imply global completion. Other workers can hold queued/running tasks or spawn future work. A steal can be in progress; externally injected work can arrive; a worker can be between creating a task and publishing it.

Finite runtime termination needs an obligation count/protocol covering active, queued, and in-transit/spawning work, plus closure of external admission. Distributed variants need stronger algorithms because observations are delayed and messages in transit.

Sleep/park requires a wake protocol: a producer that changes global work state wakes sufficient idle workers after publication. Lost wake means stranded work; waking all for one task creates a herd.

### Locality and NUMA

Owner depth-first processing benefits caches. Stealing transfers computation, not automatically data placement. A stolen subtree may read remote pages and compete for shared caches. Local-first victim hierarchy and coarse steals can help.

NUMA affinity can leave workers idle while remote queues grow. Compare estimated remaining local time with steal/migration cost. Hardware counters and page placement evidence are required; steal counts alone are weak.

Some tasks are thread-affine or device-specific and cannot be stolen. Separate capable queues and ensure pinned work cannot starve the overall scope.

### Observability and verification

Trace stable task/attempt IDs, parent/scope, ready/push/pop/steal-start/steal-success/failure/start/finish/cancel, owner/victim/thief, deque end/size snapshot, task size, worker/NUMA, wake/park, and terminal outcome. Avoid logging sensitive payloads.

Metrics include local pops, successful/failed steals, probes per success, victims, distance, bytes/task cost stolen, deque depths, idle search, wake latency, contention retries, cache/NUMA effects, active obligations, and critical-path contribution. Normalize by useful outcomes and interval.

Deque implementation verification uses state-machine/model checking, linearizability histories, weak-memory tools, sanitizers where applicable, wrap/resize/reclamation tests, and adversarial last-item races. Runtime tests use one worker, many workers, empty/one task, rapid spawn, skew, blocking, failure/cancel during transfer, sleep/wake, and shutdown. Do not implement a lock-free deque casually when validated libraries exist.

## Definitions and Notation

Let `P>=1`, work `T1`, and span `T_infinity` refer to a finite computation in a declared cost model. Classical expected `T_P=T1/P+O(T_infinity)` is cited only under its randomized fully strict scheduler assumptions.

Worker `j` owns deque `Q_j`. Abstract task-state set includes `created`, `queued(j)`, `in_transit(j,k)`, `running(k)`, and terminal outcomes. Exactly one state/owner applies at a logical transition.

Let `A` be steal attempts and `S` successes. Probe efficiency `S/A` is defined for `A>0`; it does not measure whether successful steals improved critical completion.

For task `x`, successful steal linearization changes ownership `queued(victim)->in_transit(victim,thief)->queued/running(thief)` once. Cancellation/failure transitions must commute or resolve by a declared terminal-state protocol.

Termination requires external admission closed and obligation count `O=queued+running+spawning+in_transit=0` under a consistent protocol, not a nonsynchronized sum of observations.

## Mechanisms, Invariants, or Proof Structure

Audit a work-stealing design in this order:

1. define task identity, scope, readiness, ownership states, and terminal outcomes;
2. specify owner push/pop, thief steal, linearization, publication, and last-item race;
3. prove index/wrap, resize, buffer publication, and reclamation safety under memory model;
4. state spawn/continuation policy, strictness, grain, and exactly which theoretical bounds apply;
5. choose randomized/round-robin/load-aware/hierarchical victims and bounded backoff;
6. choose steal unit/batch from task cost, locality, queue contention, and destination capacity;
7. preserve logical result/error/randomness independently of worker and execution order;
8. integrate priority, fairness, pinned work, blocking, async, and nested runtime budgets;
9. propagate cancellation/failure across queued, in-transit, and running ownership;
10. detect termination across active/queued/spawning/in-transit work and closed admission;
11. model-check deque races and stress runtime schedules, wakeups, resize, wrap, and shutdown; and
12. measure probes, success, contention, task size, locality, idle search, critical benefit, and perturbation.

The executable model demonstrates logical owner-right pops, thief-left steals, stable task identities, exact-once execution, and empty final deques without simulating concurrency.

<!-- bijux-verify: {"id":"work-stealing-ownership-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_deques=[['A', 'B', 'C', 'D'], ['E'], []]\nevents=['w2 steals A from w0', 'w1 pops E', 'w0 pops D', 'w1 steals B from w0', 'w0 pops C']\nexecution=[('w2', 'A'), ('w1', 'E'), ('w0', 'D'), ('w1', 'B'), ('w0', 'C')]\nsteal_attempts=2\nsuccessful_steals=2\nall_tasks_once=True\nqueues_empty=True\n","stderr":""}} -->
```python
deques = [["A", "B", "C", "D"], ["E"], []]
initial_deques = [queue[:] for queue in deques]
events = []
execution = []
steal_attempts = 0
successful_steals = 0

def pop_local(worker):
    if not deques[worker]:
        return None
    task = deques[worker].pop()
    events.append(f"w{worker} pops {task}")
    execution.append((f"w{worker}", task))
    return task

def steal(thief, victim):
    global steal_attempts, successful_steals
    steal_attempts += 1
    if not deques[victim]:
        return None
    task = deques[victim][0]
    deques[victim][:] = deques[victim][1:]
    successful_steals += 1
    events.append(f"w{thief} steals {task} from w{victim}")
    execution.append((f"w{thief}", task))
    return task

steal(2, 0)
pop_local(1)
pop_local(0)
steal(1, 0)
pop_local(0)

executed_tasks = [task for _, task in execution]
print(f"initial_deques={initial_deques}")
print(f"events={events}")
print(f"execution={execution}")
print(f"steal_attempts={steal_attempts}")
print(f"successful_steals={successful_steals}")
print(f"all_tasks_once={sorted(executed_tasks) == ['A', 'B', 'C', 'D', 'E']}")
print(f"queues_empty={all(not queue for queue in deques)}")
```

Limitations: this sequential list model performs no concurrent deque operations, atomics, last-item race, visibility, resize, wrap, reclamation, victim randomness, backoff, wakeup, spawning, blocking, cancellation, failure, or termination detection. It demonstrates one logical ownership trace, not work-stealing implementation correctness or performance.

## Alternatives and Trade-Offs

**Central ready queue** simplifies global order/priority but contends; **work stealing** decentralizes common operations with probe/termination complexity.

**Static assignment** preserves placement and low overhead; **stealing** reacts to irregular realized work and changes execution locality.

**Owner LIFO/opposite-end steal** favors depth-first locality/coarse theft; other deque/batch policies change space and fairness.

**Random victims** support classic analysis/spread contention; **load-aware victims** use stale/costly signals; **hierarchical victims** preserve locality but may delay global balance.

**Single-task steals** limit transfer; **batch/half steals** amortize contention but can over-transfer and hide work.

**Spin/search** lowers response with resource cost; **backoff/park** saves CPU/power with wake latency and termination complexity.

**CPU fork-join pool** fits finite compute; **async stealing runtime** handles pollable tasks but has different wake/blocking/theorem assumptions.

**Validated runtime deque** supplies reviewed low-level correctness; **custom deque** may tune special needs but creates a major memory-model/reclamation proof obligation.

## Failure Modes and Misconceptions

- “Work stealing is a queue policy.” It is a distributed ownership, search, wake, and termination protocol.
- “Any deque is safe.” Owner/thief concurrency needs a proved specialized implementation.
- “Owner and thief use opposite ends, so they never race.” They meet at the last item.
- “Atomic indices publish task contents automatically.” Memory ordering must establish visibility.
- “Resize is only copying.” Old-buffer readers and reclamation remain.
- “64-bit indices never wrap.” Quantify rate/lifetime or handle generations.
- “Successful steal means performance gain.” Migration/locality and criticality decide.
- “Random stealing is fair.” Expected balance does not guarantee per-task/thief fairness.
- “Local LIFO preserves global FIFO.” No global order is implied.
- “Thread-local means task-local.” Tasks migrate.
- “Work-stealing bounds apply to async/network services.” Fully strict/cost assumptions differ.
- “Empty local queues mean done.” Work can run, spawn, transfer, or enter externally.
- “Cancellation at victim removes stolen work.” Scope/task identity must follow transfer.
- “Helping fixes all blocking.” I/O/locks/resources can still exhaust progress.
- “Lock-free means no starvation or contention.” Progress levels and cache traffic differ.
- “More stealing fixes coarse tasks.” Indivisible work cannot be split by transfer.

## Worked Examples

### Example 1

Owner has `[A,B,C,D]`; it pops D while thief steals A. Both ends remain disjoint while size exceeds one. With sole C, owner/thief must use the algorithm's atomic last-item arbitration; array-end intuition alone is insufficient.

### Example 2

Owner writes task pointer then publishes bottom using release; thief acquires published state before reading the slot. Publishing bottom first can expose an uninitialized pointer on weak memory. Exact fences follow the validated deque algorithm.

### Example 3

Owner doubles a full ring and publishes it. A thief already captured old ring pointer. Runtime retains old ring until epoch/quiescence or uses another safe reclamation scheme. Immediate free creates use-after-free despite correct indices.

### Example 4

Balanced recursive sort has work `T1`, logarithmic span, and sufficiently coarse leaves. Randomized stealing can distribute subtrees; theorem applies only under strict model. Blocking file reads inside leaves invalidate the simple cost/scheduler assumption.

### Example 5

Thirty idle workers all probe the visibly busiest victim. CAS contention and remote cache traffic overwhelm it. Randomize or sample victims, add backoff/hierarchy, and measure failed probes plus stolen work size—not only success count.

### Example 6

Tasks are 200 ns while a failed steal/probe costs more. Fine-grained imbalance relief loses. Increase sequential cutoff/batch steal or redesign bulk operation, retaining enough work units for expected variance.

### Example 7

A stolen task writes diagnostics keyed by current worker, causing output changes across runs. Key by logical source/task ID, return owned results, and render stably after join. Worker ID belongs only in trace metadata.

### Example 8

One worker blocks on network I/O and retains many local tasks. Other workers can steal queued tasks, but the blocking task still consumes a worker and may hold resources. Move I/O to async/dedicated bounded executor and keep CPU decomposition finite.

### Example 9

Cancellation races steal. Victim removes nothing because thief claimed task; thief sees scope cancellation before start and records cancelled terminal outcome. A shared/stable task state and exactly-once terminal transition prevent execution/leak.

### Example 10

An autonomous surgical robot uses a work-stealing pool for motion-planning branches and treats a completed plan as proof of safe actuation. Scheduler completion proves neither physical safety nor deadline adequacy. Named surgical/clinical, robotics/control, real-time, hardware, numerical, cybersecurity, human-factors, quality, verification, operations, and regulatory reviewers must approve models, timing, hazards, interlocks, fallback, validation, and residual risk. This chapter cannot authorize clinical operation.

## Cross-Program Connections

- **Algorithms:** randomized selection, deques, divide-and-conquer, search, and amortized analysis underpin stealing.
- **Programming languages:** atomics, memory models, ownership, scopes, exceptions, and task APIs define correctness.
- **Operating systems:** affinity, parking/wakeup, preemption, blocking, and NUMA constrain workers.
- **Computer architecture:** cache coherence, weak memory, TLB/cache migration, and topology determine costs.
- **Formal methods:** linearizability, model checking, progress, and reclamation proofs validate deques.
- **Distributed systems:** remote stealing adds messages, leases, failures, work-in-transit, and termination detection.
- **Data systems:** irregular stages and speculation use related balancing but stronger durability/identity semantics.
- **Reliability:** cancellation, panic/failure aggregation, obligation ledgers, and wake/termination protect cleanup.
- **Security/fairness:** tenant priorities, pinned work, and resource quotas prevent stealing from bypassing policy.
- **Performance:** probe efficiency, task grain, locality, idle search, and critical-path benefit make claims measurable.

## References

1. R. D. Blumofe and C. E. Leiserson. “Scheduling Multithreaded Computations by Work Stealing.” Journal of the ACM 46(5), 1999. <https://doi.org/10.1145/324133.324234>.
2. N. S. Arora, R. D. Blumofe, and C. G. Plaxton. “Thread Scheduling for Multiprogrammed Multiprocessors.” SPAA, 1998. <https://doi.org/10.1145/277651.277678>.
3. D. Chase and Y. Lev. “Dynamic Circular Work-Stealing Deque.” SPAA, 2005. <https://doi.org/10.1145/1073970.1073974>.
4. N. M. Lê et al. “Correct and Efficient Work-Stealing for Weak Memory Models.” PPoPP, 2013. <https://doi.org/10.1145/2442516.2442524>.
5. M. Frigo, C. E. Leiserson, and K. H. Randall. “The Implementation of the Cilk-5 Multithreaded Language.” PLDI, 1998. <https://doi.org/10.1145/277650.277725>.
6. Oracle. “Java Platform API: ForkJoinPool.” <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ForkJoinPool.html>.
7. Rayon Project. “Rayon FAQ: How does Rayon work?” <https://github.com/rayon-rs/rayon/blob/main/FAQ.md>.
8. Intel oneAPI Threading Building Blocks. “How Task Scheduler Works.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/How_Task_Scheduler_Works.html>.
9. Crossbeam Project. “crossbeam_deque.” <https://docs.rs/crossbeam-deque/latest/crossbeam_deque/>.
10. OpenCilk Project. “Introduction to Cilk Programming: Parallel Tasks.” <https://www.opencilk.org/doc/tutorials/introduction-to-cilk-programming/>.

## Exercises

### Exercise 1

Specify abstract owner push/pop and thief steal states for zero, one, and multiple items. Identify the last-item linearization and loser behavior.

### Exercise 2

Explain why `T1/P+O(T_infinity)` does not automatically apply to an async web service whose tasks block, use priorities, and call external systems.

### Exercise 3

Design victim selection and backoff for a two-socket NUMA machine. State locality, fairness, termination, and evidence trade-offs.

### Exercise 4

Specify cancellation, failure, and termination accounting for tasks that can be queued, stolen/in-transit, running, or spawning children.

### Exercise 5

A railway-control optimizer uses work stealing and meets average timing. Explain why this is insufficient and define required human evidence.

## Answers to the Exercises

### Answer 1

At zero items, owner pop/thief steal observe empty and return none without changing ownership. With multiple items, owner claims newest bottom item and thief atomically advances top to claim oldest, preserving one queued owner per remaining task. At one item, owner and thieves contend on the same top generation/index using the validated atomic transition; exactly one CAS/equivalent wins and returns task. Owner loser restores/normalizes bottom to empty; thief loser retries or returns failure from a fresh state. Task contents are initialized before published bounds and reclaimed only after no reader can hold the buffer.

### Answer 2

The theorem assumes a finite fully strict computation, a particular randomized work-stealing scheduler, processor/cost model, and task dependencies. An async service is long-lived/open, has I/O suspension and wakeups, arbitrary request relationships, priorities/admission, external latency/effects, cancellation, and possibly thread-affine drivers. Its `T1`/span may not be defined over one closed computation and blocked time is not ordinary work. Use runtime-specific queue/waker/backpressure and service queueing/tail evidence; apply strict bounds only to an isolated finite CPU subcomputation satisfying assumptions.

### Answer 3

Prefer local-core/socket victims for a bounded number of randomized probes, then sample remote socket with backoff; occasionally force remote/global probing so isolated work is discoverable. Steal older/coarser tasks or bounded batches whose estimated work amortizes remote cache/page cost. Randomize seeds to avoid synchronized convoys, cap spin/probes, park with a publication-before-directed-wake protocol, and include pinned/capability queues. Measure attempts/success, victim distance, stolen cost/bytes, remote memory/cache misses, idle search, wake latency, makespan/tails, starvation intervals, and semantic equivalence across skew/grain.

### Answer 4

Use stable task/scope identity and one atomic logical state among queued(owner), transfer(victim,thief), running(worker), spawning with registered child obligations, and terminal. Cancellation marks the scope/task regardless of location; queue claims either execute/check token or transition to cancelled exactly once. A steal that already linearized owns settlement. Failure stops further spawning, signals owned descendants/siblings, and aggregates by stable identity. Parent registers child before publication and decrements obligation only after child terminal cleanup. Termination requires admission closed and a consistent protocol showing no queued, running, spawning, or in-transit obligations; then workers can park/exit without lost wake.

### Answer 5

Average timing omits worst-case deadlines, optimization/model validity, stale inputs, schedule variance, hardware faults, cancellation, and physical interlocking. Production requires named railway signalling/control, optimization/domain, systems, functional-safety, real-time, hardware, cybersecurity, human-factors, operations, quality, independent verification, and regulatory reviewers; requirements/hazard traceability; applicable-standard assessment; model/input provenance; deterministic/tolerance policy; worst-case timing and resource analysis; simulation, hardware-in-the-loop, saturation, fault-injection, failover, recovery, environmental, and operational evidence; independent interlocks/fail-safe state; and signed residual-risk acceptance. This answer is not deployment authorization.
