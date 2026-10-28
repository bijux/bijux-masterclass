---
module_id: OS-057
program: Operating Systems
level: 2
module_number: 57
title: Load Balancing Across Cores
status: complete
last_verified: 2026-09-04
---

# Load Balancing Across Cores

## One-Page Review

### Governing question

How should a multiprocessor scheduler distribute runnable work across eligible processors so that capacity, fairness, latency, locality, energy, and isolation objectives are met without spending more on observation and migration than the imbalance costs?

### Essential definitions

- **Run queue** is scheduler state representing runnable entities associated with a processor or scheduling context.
- **Load** is a weighted history of runnable demand; it is not simply a task count.
- **Utilization** estimates the fraction of processor capacity a task or queue consumes over time.
- **Capacity** estimates the useful compute available from a processor under architecture, frequency, thermal, and interference conditions.
- **Imbalance** is a policy-relevant difference between demand and capacity across eligible scheduling groups.
- **Wakeup placement** selects a CPU when a blocked task becomes runnable.
- **Idle balancing** searches for work when a CPU is idle or newly idle.
- **Periodic balancing** evaluates domains at bounded intervals while CPUs continue running work.
- **Active balancing** can arrange migration when ordinary pulling cannot move a suitable queued task.
- A **misfit task** has utilization that does not fit the capacity of its current CPU when a more capable eligible destination may exist.

### Central model, mechanism, or theorem

For eligible CPU `c`, compare normalized pressure `rho_c=u_c/h_c`, where `u_c` is estimated runnable utilization and `h_c` is effective capacity. A balancing action moves an eligible task only when the predicted reduction in a service objective exceeds migration, cache, NUMA, synchronization, energy, and observation costs. A useful conceptual objective is `J=max_c rho_c + fairness_penalty + latency_penalty + energy_penalty + locality_penalty + migration_cost`, subject to affinity, cpuset, scheduling-class, admission, and isolation constraints.

The scheduler cannot obtain a free, instantaneous, exact view of a changing system. It uses decayed signals, per-CPU state, topology domains, locks, and event-triggered sampling. Consequently, balancing is a feedback-control problem: estimates lag, actions perturb locality, workloads change phase, and multiple controllers can interact.

### Critical invariants

- A task migrates only to a CPU allowed by its effective affinity, cpuset, scheduling class, and current online topology.
- Migration preserves task state, scheduling accounting, wakeup ordering obligations, and one-run-queue ownership.
- Capacity-normalized demand, not raw task count alone, drives comparisons on asymmetric or dynamically scaled CPUs.
- Balancing across a wider topology domain is attempted less eagerly than cheap local balancing unless policy requires otherwise.
- Cache-hot, NUMA-bound, device-coupled, real-time, deadline, and per-CPU work obey explicit movement constraints.
- Isolated and exclusive partitions are not silently crossed to improve global utilization.
- Failure to find a movable task leaves queues coherent and triggers only bounded retry or escalation.
- Performance claims include queue delay, utilization, migrations, cache and NUMA effects, capacity, energy, and workload phase.

### Common failures

Common mistakes are balancing task counts instead of demand, comparing utilization without normalizing capacity, migrating the cache-hottest task because it is easiest to find, treating a sampled imbalance as stable truth, ignoring affinity and cpuset boundaries, moving compute away from its pages or device queue, forcing balance across isolated partitions, assuming an idle CPU can run every queued task, overreacting to short bursts, making all CPUs contend on global scheduler state, interpreting fewer migrations as better scheduling, and evaluating throughput without fairness, queue delay, energy, or tail latency.

### Compact example

Four CPUs have capacities `{1024,1024,512,512}` and utilizations `{900,700,200,100}`. Their normalized pressures are about `{0.879,0.684,0.391,0.195}`. Moving a 200-unit eligible task from CPU 0 to CPU 3 produces `{0.684,0.684,0.391,0.586}`, reducing the maximum and the spread. This arithmetic only identifies a load-shaped candidate; locality, affinity, runnable state, priority, migration safety, and energy can still reject it.

### Connections

[OS-016](016-scheduling-objectives.md), [OS-019](019-fair-scheduling.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-055](055-numa-memory-placement.md), and [OS-056](056-processor-affinity.md) connect balancing to objectives, fairness, evidence, memory locality, and eligibility.

## Governing Question

A multiprocessor scheduler faces two bad extremes. Leaving runnable work on a busy processor while an eligible peer is idle wastes capacity and lengthens queue delay. Moving work too eagerly destroys warm cache and translation state, increases shared-state traffic, detaches tasks from memory and devices, and consumes scheduler time.

The governing question is when, where, and what to move. The answer depends on scheduling class, topology, measured demand, capacity, locality, policy boundaries, and how long the workload phase will persist.

## Why This Matters

Load balancing determines whether adding cores improves service or merely adds coordination. It affects interactive wakeup latency, batch throughput, real-time interference, power, thermal concentration, and the scalability of the scheduler itself.

The system is only partially observable. Runnable demand changes while it is measured, short sleepers look different from CPU-bound tasks, and frequency or thermal limits change effective capacity. Global precision would require synchronization that can cost more than small imbalance.

Balancing also crosses ownership boundaries. Affinity, cgroups, virtual machines, NUMA policies, device queues, and isolation partitions can deliberately make global utilization uneven. Correctness means honoring those constraints before pursuing an attractive aggregate graph.

## Prerequisites and Retrieval

Review [OS-013](013-threads-and-execution-contexts.md), [OS-014](014-context-switching.md), [OS-015](015-process-states-and-wait-queues.md), [OS-016](016-scheduling-objectives.md), [OS-017](017-round-robin-and-priority-scheduling.md), [OS-019](019-fair-scheduling.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-055](055-numa-memory-placement.md), and [OS-056](056-processor-affinity.md).

Retrieve these distinctions:

- runnable demand, running time, blocked time, queue length, load, and utilization are different signals;
- one logical CPU can share a physical core with an SMT sibling;
- processors can differ in original and current capacity;
- per-CPU queues improve scalability but require placement and migration;
- a task's effective affinity bounds all legal destinations;
- fairness over time does not imply equal instantaneous queue lengths;
- CPU migration and memory locality can pull in opposite directions;
- real-time and deadline classes have constraints beyond ordinary fair balancing.

## Learning Objectives

After this module, you should be able to:

1. distinguish load, utilization, runnable count, capacity, pressure, spare capacity, and service delay;
2. explain wakeup, idle, newly-idle, periodic, passive, and active balancing paths;
3. reason across hierarchical scheduling domains, groups, SMT, caches, NUMA nodes, and asymmetric CPUs;
4. select migration candidates while respecting affinity, policy, priority, locality, and synchronization;
5. analyze oscillation, stale signals, overload, isolation, hotplug, nohz, and controller interaction;
6. compare push, pull, stealing, static partitioning, and energy-aware placement;
7. validate balancing with scheduler, hardware, topology, energy, and application evidence.

## Core Exposition

### Why per-CPU queues

A single global run queue gives a simple view of runnable work but becomes a shared lock and cache-line hotspot as processors grow. Per-CPU queues let most enqueue, dequeue, accounting, and selection operations remain local.

Local queues trade global simplicity for distributed imbalance. The scheduler must place newly runnable tasks and occasionally transfer work without turning the balancing mechanism into the global bottleneck it replaced.

### What is being balanced

Raw task count is rarely enough. One queue with a single CPU-bound task can have more demand than another with ten mostly sleeping tasks. Priorities and weights change expected shares, and group scheduling aggregates demand hierarchically.

Define the objective before choosing a signal. Throughput, queue delay, fairness, deadline feasibility, power, and cache locality can prefer different distributions.

### Load and utilization

Load represents weighted runnable demand over history. Utilization estimates actual execution demand. A task that alternates short computation and sleep contributes differently from a continuously runnable task even when both appear once in a queue snapshot.

Decayed histories suppress noise but lag phase changes. Recent demand can be underestimated after wakeup and overestimated after a task blocks, so placement includes margins and event-specific logic.

### Capacity normalization

Capacity gives the denominator for utilization. A utilization of 400 fits comfortably on a capacity-1024 CPU and nearly saturates a capacity-512 CPU.

Normalize before comparing heterogeneous processors. Current capacity can reflect frequency, thermal pressure, and time stolen by higher scheduling classes or interrupts, while original capacity describes architectural potential.

### Spare capacity

Spare capacity is approximately available capacity minus estimated utilization, within the scheduler's model. It helps distinguish a truly useful target from a CPU that is idle at one instant but heavily committed by periodic tasks.

Spare-capacity estimates are not reservations. Simultaneous wakeups can all observe the same apparent headroom and create a herd unless placement distributes or rechecks decisions.

### Wakeup placement

When a blocked task becomes runnable, the scheduler can keep it near its previous CPU, place it near the waker, or choose another eligible CPU with capacity. This path can prevent imbalance before a task enters a long queue.

Wake affinity benefits communicating tasks and warm cache state. It can also concentrate a fan-out workload on the waker's CPU, so the decision considers shared-cache topology, utilization, and the task's previous behavior.

### Fork and execution placement

Task creation offers another placement point. Parent locality can help shared state, whereas spreading CPU-bound children prevents one queue from receiving the entire parallel job.

The program can change character at execution. Placement heuristics should not assume that a child continues its parent's demand profile after loading a different image.

### Newly-idle balancing

When a CPU becomes idle, it can immediately search nearby domains for movable work. Pulling reduces idle time and responds faster than waiting for the next periodic interval.

The search itself consumes time and shared-state accesses. Repeated failed searches on a lightly loaded or constrained system waste energy, so the scheduler bounds scope and uses topology and recent state.

### Idle balancing

An idle CPU is motivated to pull because it has no local work to disrupt. It must still distinguish queues with transferable tasks from queues whose work is running, pinned, higher priority, cache-sensitive, or otherwise unsuitable.

An idle destination does not prove a legal migration exists. Affinity, cpusets, scheduling class, cookie or security policy, and capacity can leave the CPU intentionally idle.

### Periodic balancing

Periodic balancing detects persistent skew among non-idle CPUs and across domains that wakeup placement did not repair. Intervals can grow with topology distance because cross-socket scans and migrations are more expensive.

Too-frequent checks waste cycles and cause churn; slow checks leave long queues beside underused capacity. Adaptive intervals need caps and observable reasons for escalation.

### Active balancing

Ordinary balancing prefers moving queued tasks that are not currently executing. If the only suitable task is running continuously, active balancing can arrange for work on the source CPU to push or stop and migrate it.

This path requires stronger coordination and is reserved for meaningful persistent imbalance, such as a misfit task. Failed active attempts leave both queues and task ownership coherent.

### Pull versus push

Pull balancing lets an idle or less-loaded CPU search sources. It naturally distributes search work and starts from known destination capacity. Push balancing lets an overloaded source identify work to shed.

Hybrid systems use both at appropriate events. A pure pull design can miss imbalance when no CPU goes idle; a pure push design can make busy CPUs spend scarce time searching and contending.

### Scheduling domains

Processors are organized into a hierarchy reflecting topology and balancing policy. A low domain might cover SMT siblings, then cores sharing a cache, then a package, then NUMA or system-wide groups.

Balancing locally first limits migration cost and search scope. Domain flags and groups express which behaviors are meaningful on a platform; they are policy inputs, not a promise that firmware topology perfectly predicts measured cost.

### Domain groups

A domain partitions its span into groups whose aggregate demand and capacity can be compared. Selection first identifies an imbalanced group and then a source queue and task.

Aggregation prevents every decision from scanning every task. It also loses detail, so a group that looks busy may contain no task eligible for the selected destination.

### Topology distance

Migration among SMT siblings, cores sharing cache, packages, and NUMA nodes has different costs. Wider movement can lose more cache state and change memory or device distance.

Do not assign cost solely from labels. Measure the relevant workload, because cache footprint, sharing, interconnect contention, and page placement determine realized impact.

### Cache-hot tasks

A recently running task may retain valuable cache and translation state. Delaying its migration can avoid warming costs, especially for short imbalances.

Hotness is a heuristic, not immunity. A persistently overloaded source or idle high-capacity target can justify movement when remaining benefit exceeds locality loss.

### Choosing a candidate

A candidate must be eligible on the destination, movable under its class and policy, and useful enough to reduce the identified imbalance. Its weight, utilization, priority, cache state, memory, and communication relationships matter.

Moving the largest task can overshoot and reverse the imbalance. Moving many small tasks increases locking and warm-up. Candidate selection evaluates the post-move state rather than just removing source load.

### One-run-queue ownership

A runnable scheduling entity belongs to one appropriate queue at a time. Migration coordinates source and destination locks, task state, CPU ownership, clocks, accounting, and concurrent wakeups.

Lock ordering and validation prevent deadlock, duplication, loss, and moving a task whose state changed during selection. Failed validation restarts or abandons the attempt without corrupting ownership.

### Affinity constraints

Effective processor affinity bounds legal destinations. A system-wide graph showing idle CPUs is irrelevant when none belong to a queued task's mask.

Balancing statistics should distinguish no imbalance from imbalance with no movable task. The latter signals policy fragmentation or overconstrained placement rather than scheduler success.

### Cpuset boundaries

Cpusets create hierarchical CPU envelopes and can form partitions with distinct balancing behavior. A child cannot borrow a CPU outside its effective parent allowance.

Partitioned imbalance can be intentional isolation. Capacity planners, not the scheduler, decide whether to resize the boundary; silently crossing it violates the resource contract.

### Isolated processors

An isolated partition can disable ordinary load balancing, leaving applications or specialized runtimes responsible for placement within it. This reduces scheduler disturbance but permits avoidable idle time when user policy is wrong.

Assurance verifies both sides: general balancing stays out, and the owner has a safe strategy for skew, worker failure, and overload.

### SMT balancing

Two runnable tasks on sibling hardware threads can contend while a separate physical core is idle. Topology-aware balancing can prefer spreading across cores before filling siblings for CPU-bound work.

For throughput under shared stalls, SMT packing may still help. Capacity signals and workload measurements should guide policy rather than treating every logical CPU as independent.

### Shared-cache balancing

Communicating threads may benefit from remaining in one last-level-cache domain. Independent memory-bandwidth-heavy tasks may benefit from spreading across caches or memory controllers.

The scheduler lacks full semantic knowledge of an application's sharing graph. Runtimes can contribute partitioning and affinity, but their decisions must compose with system load and administrative boundaries.

### NUMA balancing

Moving a task across nodes changes its relationship to physical pages. Moving pages toward tasks is another controller with a longer and more expensive action path.

Coordinate task and page placement so each does not invalidate the other's observation. Use phase epochs, hysteresis, migration budgets, and a consistent ownership model.

### Device locality

Network, storage, and accelerator queues have interrupt, DMA, polling, and completion topology. A globally underused CPU can be a poor target if it is remote from the task's dominant device path.

Measure end-to-end queue latency and interconnect traffic. Task balancing, IRQ steering, queue selection, and buffer placement form one system.

### Asymmetric processors

Heterogeneous processors have unequal original capacity. Dynamic frequency and thermal pressure further change current capacity.

Balance normalized demand rather than equalizing task counts or raw utilization. Preserve sufficient high-capacity headroom for work whose service requirement cannot fit elsewhere.

### Misfit tasks

A task is a misfit when its demand exceeds what its current lower-capacity CPU can provide and a higher-capacity eligible CPU exists. A CPU-bound misfit rarely sleeps, so wakeup placement alone cannot repair it.

Active load balancing can move the continuously running task. Utilization clamping and affinity affect what counts as a fit and which destinations are acceptable.

### Energy-aware placement

At light or moderate demand, consolidating suitable tasks on efficient CPUs can let other power domains idle. The energy model compares predicted arrangements while protecting throughput constraints.

When a domain is overutilized, performance-oriented load balancing can take precedence. Energy, power, and performance are separate quantities, and a prediction must be validated on real hardware.

### Utilization clamping

Utilization clamps let user space express minimum or maximum performance hints that affect task fitting and frequency selection. They change scheduler signals without changing the task's actual instructions.

Bad clamps can waste energy or force important work onto inadequate processors. Observe effective values through hierarchy and validate both latency and energy outcomes.

### Fair scheduling interaction

Fair scheduling accounts entitlement over time within groups and weights. Load balance should make that entitlement realizable across processors without giving a migrated sleeper an unintended advantage.

Equal instantaneous utilization is neither necessary nor sufficient for fairness. Inspect service received, runnable delay, weights, hierarchy, and time horizon.

### EEVDF interaction

An eligible virtual deadline and lag guide which fair-class entity runs next on a queue. Multiprocessor placement still decides which queue contains the entity and which capacity can serve it.

Balance preserves accounting semantics across migration. A destination should not treat moved work as newly entitled merely because its local ordering differs.

### Real-time classes

Fixed-priority real-time balancing must respect priority, affinity, overload handling, and bounded interference. Moving lower-priority ordinary work does not solve a CPU whose admitted real-time utilization is impossible.

Push and pull mechanisms for real-time work follow class-specific rules. Validate priority inversion, interrupt load, migration latency, and fallback CPUs under failure.

### Deadline scheduling

Deadline tasks carry runtime, period, and deadline reservations. Placement and migration must preserve admission feasibility and bandwidth accounting.

An idle CPU outside the admitted root domain or affinity set is not usable. Overload and hotplug require explicit recovery rather than ordinary fair-class heuristics.

### Group scheduling

Cgroup scheduling distributes processor service among hierarchical groups. A queue's aggregate load can contain entities representing groups rather than only leaf threads.

Balancing must preserve group shares across CPUs, while quotas can throttle a group even when physical capacity is idle. Diagnose policy bandwidth separately from placement imbalance.

### Bursty tasks

Short sleepers can wake with stale or low utilization estimates. Placing every wakeup on an apparently idle CPU may spread cache state; keeping all wakeups near one waker may create a burst queue.

Use signals that capture historical behavior and test fan-out, synchronized timers, and request bursts. No single sampling half-life fits every workload.

### Work stealing runtimes

User-space runtimes often maintain one deque per worker and steal when local work is empty. Their scheduler sees application tasks that the kernel may see only as a fixed pool of runnable threads.

Coordinate worker affinity and steal topology. Kernel balancing of workers and runtime stealing of jobs can both move the same computation, doubling locality loss.

### Static partitioning

Static assignment makes ownership predictable and avoids balancing overhead. It works well for regular parallel loops, sharded state, and carefully admitted real-time systems.

Skew, blocking, failures, and phase changes leave capacity idle. Controlled overflow or hierarchical stealing supplies resilience without discarding the common-case locality plan.

### No-tick and idle CPUs

Tick suppression reduces periodic activity on idle or isolated CPUs. It also changes where and when balancing maintenance can run, so remote CPUs may need to initiate or coordinate work discovery.

Do not infer lack of demand from lack of a recent local tick. Instrument the actual balancing paths supported by the active kernel configuration.

### Overload

When total eligible demand exceeds capacity, balancing cannot eliminate queueing. It can distribute pain according to weights, priorities, and topology, but it cannot manufacture service.

Report saturation explicitly. Autoscaling, admission control, load shedding, quota changes, or capacity reallocation belong above the scheduler's migration mechanism.

### Oscillation

Noisy measurements and aggressive actions can bounce tasks between CPUs or nodes. Each move changes the next observation and pays cache, TLB, and NUMA costs.

Hysteresis, minimum residence, asymmetric thresholds, bounded batches, and cost-aware rejection stabilize the loop. Track migrations per useful unit of work, not migrations alone.

### Herding and synchronized decisions

Many waking tasks or balancing CPUs can select the same target from a stale snapshot. By arrival time, the target is overloaded while another remains idle.

Reservations, target accounting, randomized tie-breaking, serialized domain leadership, or revalidation reduce herding. The coordination cost must remain below the avoided imbalance.

### Hotplug and failure

CPU offlining removes capacity and forces eligible work to migrate or exposes an invalid policy. Online additions need topology and domain reconstruction before receiving ordinary work.

Recompute capacity, masks, groups, reservations, per-CPU state, and device routing by generation. Test rollback when callbacks fail and retain a destination for control and recovery threads.

### Observability

Collect per-CPU runtime, runnable delay, utilization, capacity, queue length, idle time, migrations, wakeups, failed balances, domain scans, active balance, and throttling.

Correlate those signals with affinity, cpusets, topology, scheduling class, weights, cache misses, NUMA traffic, interrupts, frequency, thermal pressure, energy, and application latency. Version-specific scheduler counters need documented interpretation.

### Experiment design

Compare default balancing with static partitioning, affinity-constrained groups, runtime stealing, and deliberately adverse placement. Preserve kernel configuration, topology, frequency policy, quotas, memory placement, interrupts, input, and phase boundaries.

Test uniform and skewed work, CPU-bound and bursty tasks, SMT contention, asymmetric capacity, NUMA distance, device traffic, overload, hotplug, and isolation. Randomize run order, repeat, and retain raw traces and uncertainty.

### Assurance

An assurance case maps each objective to evidence: fairness to received service and waits, utilization to capacity-normalized demand, locality to cache and NUMA evidence, isolation to boundary tests, and resilience to failure injection.

Reviewers include scheduler, architecture, runtime, NUMA, device, real-time, performance, and operations specialists. A toy utilization calculation is not evidence that a production migration is legal or beneficial.

## Definitions and Notation

Let `T` be runnable tasks, `C` online CPUs, `E_t` the effective eligible CPUs for task `t`, `u_t` estimated utilization, `w_t` fair weight, and `h_c` effective capacity. Let `U_c` aggregate runnable utilization assigned to CPU `c` and `rho_c=U_c/h_c` normalized pressure.

For a candidate migration of task `t` from source `s` to destination `d`, compare the predicted objective before and after. One illustrative objective is `J=max_c rho_c + lambda*spread(rho) + F + L + N + G`, where `F` is fairness penalty, `L` locality loss, `N` latency or service penalty, and `G` migration and synchronization cost. The move must satisfy `d in E_t` and class-specific safety. Coefficients and signals require empirical calibration; this is not a closed-form scheduler proof.

Load, utilization, runnable count, weight, capacity, spare capacity, pressure, latency, fairness, and energy are separate variables. A useful design names which one a counter approximates and over what time window.

## Mechanisms, Invariants, or Proof Structure

1. **State objectives.** Rank throughput, latency, fairness, locality, energy, isolation, and resilience for each workload class.
2. **Discover constraints.** Capture online topology, capacities, affinity, cpusets, partitions, quotas, classes, priorities, devices, and memory.
3. **Maintain local state.** Keep common queue operations per CPU and aggregate only the signals required for wider decisions.
4. **Place on wakeup.** Select an eligible target using previous locality, waker relation, capacity, utilization, and policy.
5. **Pull when idle.** Search cheap nearby domains first and stop when no legal beneficial candidate exists.
6. **Check periodically.** Detect persistent non-idle skew at topology-aware intervals without global synchronization.
7. **Escalate carefully.** Use active movement for meaningful imbalance or misfit work that ordinary queued migration cannot repair.
8. **Validate candidates.** Recheck eligibility, state, queue ownership, capacity, priority, locality, and post-move improvement under locks.
9. **Preserve semantics.** Transfer accounting and ownership without loss, duplication, unfair credit, or policy-boundary violation.
10. **Control feedback.** Bound scan and migration cost, prevent herding, coordinate NUMA and runtime controllers, and apply hysteresis.
11. **Test lifecycle.** Cover burst, overload, isolation, quota, hotplug, failure, rollback, and teardown.
12. **Retain evidence.** Preserve topology generations, configuration, signals, traces, service results, failures, reviewers, and limitations.

<!-- bijux-verify: {"id":"capacity-normalized-balance","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before-pressure=0.879,0.684,0.391,0.195\nafter-pressure=0.684,0.684,0.391,0.586\nbefore-spread=0.684\nafter-spread=0.293\nselected-target=3\n","stderr":""}} -->
```python
capacities = [1024, 1024, 512, 512]
utilization = [900, 700, 200, 100]
task_utilization = 200
source = 0
target = 3

def pressure(values):
    return [value / capacity for value, capacity in zip(values, capacities)]

def spread(values):
    return max(values) - min(values)

before = pressure(utilization)
after_utilization = utilization.copy()
after_utilization[source] -= task_utilization
after_utilization[target] += task_utilization
after = pressure(after_utilization)
print("before-pressure=" + ",".join(f"{value:.3f}" for value in before))
print("after-pressure=" + ",".join(f"{value:.3f}" for value in after))
print(f"before-spread={spread(before):.3f}")
print(f"after-spread={spread(after):.3f}")
print(f"selected-target={target}")
```

The executable example recomputes one capacity-normalized candidate. It assumes divisible utilization and ignores affinity, runnable state, priorities, cache and NUMA locality, energy, synchronization, concurrent changes, scheduling classes, quotas, and measurement error.

## Alternatives and Trade-Offs

- Per-CPU run queues scale common operations but require migration; one global queue simplifies visibility and creates contention.
- Wakeup placement prevents queues from forming but relies on lagging task estimates; periodic balancing sees aggregates and reacts later.
- Pulling from an idle CPU protects busy sources but can scan fruitlessly; pushing exposes source knowledge and consumes overloaded CPU time.
- Local-domain balancing preserves cache and NUMA locality but can leave remote capacity idle; wide balancing improves utilization and pays distance.
- Moving one large task repairs imbalance quickly but can overshoot and lose a large working set; moving small tasks adds coordination and warm-up.
- Static partitioning minimizes scheduler movement but wastes capacity under skew; dynamic balancing adapts and creates variance.
- SMT packing can improve throughput and package idleness but increases core interference; spreading uses more cores and power domains.
- NUMA-local placement protects memory locality but tolerates queue skew; cross-node migration reduces delay and can make accesses remote.
- Capacity-aware placement fits work to heterogeneous CPUs but depends on accurate topology and signals; symmetric assumptions are simpler and wrong on asymmetric systems.
- Energy-aware placement can reduce joules under spare capacity but may concentrate demand; performance balancing handles overload and uses more energy.
- Long averaging windows suppress noise but lag bursts; short windows react quickly and oscillate.
- Exclusive partitions protect tenants and timing analysis but strand capacity; shared domains improve utilization and expand interference.
- Runtime work stealing understands application jobs but duplicates kernel movement; kernel balancing understands host contention but not application dependencies.
- Detailed domain scans improve candidate choice but cost locks and cache traffic; approximate summaries scale and can miss movable work.

## Failure Modes and Misconceptions

- **“Equal task counts mean balanced CPUs.”** Tasks differ in demand, weight, priority, and blocking.
- **“Equal utilization means equal pressure.”** CPU capacities can differ or change.
- **“An idle CPU can run any waiting task.”** Affinity, cpusets, class, admission, isolation, and capacity restrict it.
- **“Migration is free after ownership changes.”** Cache, TLB, memory, device, locking, and warm-up costs remain.
- **“The busiest queue always has a movable task.”** Its work can be running, pinned, or ineligible for the destination.
- **“Fresh counters are exact global truth.”** Distributed observations race workload changes.
- **“More frequent balancing always reacts better.”** Scanning and churn can dominate the saved delay.
- **“No migrations proves ideal locality.”** Work may be stranded or overload may persist.
- **“Maximum utilization proves throughput.”** Throttling, priorities, inefficient CPUs, and useless spinning can produce it.
- **“Partition imbalance is a scheduler bug.”** Isolation and ownership can make it intentional.
- **“Wakeup balancing handles CPU-bound tasks.”** A continuously running misfit rarely wakes.
- **“Energy-aware means slow.”** The objective seeks energy efficiency while preserving applicable throughput constraints.
- **“NUMA page balancing and task balancing naturally converge.”** Independent feedback loops can chase each other.
- **“One benchmark fixes scheduler settings.”** Workload phase, kernel, topology, devices, power, and contention matter.
- **“Task movement alone completes rollback.”** Affinity, cpusets, runtime queues, memory, IRQs, and reservations may remain changed.

## Worked Examples

### Example 1

One CPU runs a single continuous task while a peer holds six sleeping services. Task counts favor moving from the peer, but utilization shows the continuous task is the real source of pressure.

### Example 2

A newly idle CPU searches its shared-cache domain and pulls an eligible cold worker. It avoids a remote-socket task whose working set would cost more to warm than the predicted queue delay.

### Example 3

All children of a fan-out request wake near one waker and overload its queue. Capacity-aware wakeup placement distributes them among eligible cache-local cores.

### Example 4

A CPU-bound task remains on a low-capacity processor and never blocks. Active misfit migration moves it to an eligible high-capacity processor because wakeup placement has no event to use.

### Example 5

A scheduler sees idle CPUs outside a tenant's exclusive cpuset. It preserves the boundary and reports constrained overload so the resource manager can resize or reject work.

### Example 6

Kernel balancing moves worker threads while their runtime steals jobs in the opposite direction. Pinning workers to cache groups and making steals hierarchical removes the double movement.

### Example 7

A task migration balances CPU pressure but moves a database thread away from 40 GiB of local pages. The combined service objective rejects the move until the projected phase is long enough.

### Example 8

Short utilization windows alternately identify two CPUs as busiest. Hysteresis and a minimum residence interval reduce migrations and improve tail latency despite a slightly larger instantaneous spread.

### Example 9

A four-CPU group is fully runnable but throttled by a one-CPU quota. Load balancing cannot use idle host time after budget exhaustion; policy bandwidth must change.

### Example 10

Hot-unplug removes a high-capacity CPU. The system reconstructs domains and capacities, migrates eligible work, detects one invalid affinity, and invokes its prevalidated fallback rather than assuming ordinary balance succeeds.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects SMT, cache hierarchies, coherence, capacity, frequency, thermal pressure, NUMA, interrupts, and energy. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects worker pools, work stealing, deques, task graphs, locality, synchronization, and skew.

[Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects quotas, tenancy, vCPU placement, autoscaling, admission, noisy neighbors, and service objectives. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes feedback control, stability, objective functions, lifecycle hazards, trade studies, and assurance. Within this program, [OS-055](055-numa-memory-placement.md) covers pages, [OS-056](056-processor-affinity.md) covers eligibility, and [OS-060](../ROADMAP.md) covers contention diagnosis.

## References

- Linux kernel documentation, [Scheduler Domains](https://docs.kernel.org/scheduler/sched-domains.html), current page checked 2026-09-04. Domain hierarchy, groups, topology flags, balancing intervals, capacity and architecture inputs.
- Linux kernel documentation, [Capacity Aware Scheduling](https://docs.kernel.org/scheduler/sched-capacity.html), current page checked 2026-09-04. Original and current CPU capacity, utilization fitting, asymmetric systems, wakeup selection, load balance and misfit migration.
- Linux kernel documentation, [Energy Aware Scheduling](https://docs.kernel.org/scheduler/sched-energy.html), current page checked 2026-09-04. Energy models, performance domains, spare capacity, wakeup placement, overutilization and performance fallback.
- Linux kernel documentation, [Scheduler Statistics](https://docs.kernel.org/scheduler/sched-stats.html), current page checked 2026-09-04. Per-CPU runtime and wait statistics, domain balance attempts, imbalance, task movement, active balance and wakeups.
- Linux kernel documentation, [EEVDF Scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html), current page checked 2026-09-04. Lag, eligibility, virtual deadlines, latency, sleeping tasks and fair-class selection.
- Linux kernel documentation, [CFS Scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html), current page checked 2026-09-04. Virtual runtime, weighted fair service, run-queue accounting, granularity and SMP balancing context.
- Linux kernel documentation, [Schedutil](https://docs.kernel.org/scheduler/schedutil.html), current page checked 2026-09-04. Scheduler utilization signals, frequency selection, rate limits, I/O waiting and deadline bandwidth interaction.
- Linux kernel documentation, [Utilization Clamping](https://docs.kernel.org/scheduler/sched-util-clamp.html), current page checked 2026-09-04. Task and cgroup performance hints, effective clamps, capacity fitting, frequency effects and limitations.
- Linux kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. CPU weight and bandwidth, hierarchical cpusets, effective CPUs, exclusive allocation, partitions, isolation and hotplug.
- Linux man-pages project, [cpuset(7)](https://man7.org/linux/man-pages/man7/cpuset.7.html), current page checked 2026-09-04. Affinity composition, scheduler load balancing, scheduling domains, memory nodes, migration and administrative constraints.

## Exercises

### Exercise 1

Design load balancing for a two-socket server with SMT, asymmetric queue demand, NUMA-local memory, network queues, and a strict tail-latency objective.

### Exercise 2

Compare wakeup, newly-idle, periodic, and active balancing for bursty services, continuously runnable batch jobs, and a misfit task on a heterogeneous system.

### Exercise 3

Specify candidate-selection and migration invariants for per-CPU run queues. Include races, locks, affinity, accounting, priority, failure, and rollback.

### Exercise 4

Design a stable controller shared by kernel balancing, a work-stealing runtime, and automatic NUMA placement. Prevent oscillation while retaining overload response.

### Exercise 5

Build an experiment and assurance plan for a proposed balancing change. Include topology, capacity, fairness, locality, energy, isolation, overload, lifecycle, and reproducibility.

## Answers to the Exercises

### Answer 1

Discover logical CPUs, SMT siblings, physical cores, caches, sockets, NUMA distances, capacity, NIC locality, IRQs, queues, frequency and thermal policy. Partition receive queues across NIC-local physical cores, align polling and interrupt paths, and place queue buffers and worker-owned data locally. Give compute workers a wider socket-local eligibility set with local-first stealing, while control and recovery work retains redundant housekeeping CPUs.

Balance normalized utilization rather than queue count. Preserve cache-local candidates for short skew and allow measured cross-socket overflow only when predicted queue-delay reduction exceeds cache and remote-memory cost. Test uniform traffic, one hot flow, synchronized bursts, CPU and queue failure, remote pages, SMT contention, housekeeping overload, and total saturation. Observe effective masks, run-queue wait, wakeups, pulls, active migrations, cache and NUMA traffic, IRQs, drops, throughput, and tail latency. Rollback restores wider safe eligibility before dismantling queue and memory placement.

### Answer 2

Wakeup placement is the cheapest prevention path for bursty services: it uses previous CPU and waker locality while distributing fan-out according to spare capacity. Newly-idle balancing reacts immediately after a CPU drains, but bounded scans are important when burst tasks block again quickly. Periodic balancing detects persistent skew among busy CPUs and across wider domains, at the cost of delayed reaction and repeated observation.

A continuously runnable batch task rarely wakes, so wakeup placement cannot correct its stale location; periodic movement can handle ordinary imbalance. A misfit task on a low-capacity CPU may be the only running movable work, requiring active balance after a persistent, capacity-aware test. Every path still checks affinity, cpuset, class, priority, topology, locality, and post-move benefit. Use hysteresis so a short utilization fluctuation does not trigger the stronger paths.

### Answer 3

Select source and destination from the same current domain generation, normalize aggregate demand by capacity, and require predicted objective improvement. Under the appropriate ordered queue locks, revalidate that the task remains runnable, belongs only to the source, is not currently executing unless the active protocol covers it, permits the destination in its effective mask, fits class and admission rules, and has unchanged identity and state.

Detach exactly once, transfer fair, real-time, deadline and group accounting without new credit or lost debt, update CPU and migration metadata, attach exactly once, and trigger required preemption or rescheduling. Concurrent wakeup, exit, affinity, cpuset, priority, hotplug, or throttling changes cause bounded retry or abandonment. On failure, the task remains reachable on one valid queue and all partial accounting is unwound. Tracepoints and assertions verify conservation of runnable entities, utilization, weights, reservations and queue ownership.

### Answer 4

Assign one coordinator the workload-phase and topology generation. The kernel owns physical-thread placement inside administrative constraints, the runtime owns application-job placement over stable worker groups, and the NUMA controller owns page actions based on the same published worker group and phase. Runtime stealing stays within a cache or node first; cross-group steals and kernel mask changes require a persistent overload signal.

Use decayed measurements with confidence, distinct enter and exit thresholds, minimum task and page residence, bounded migration count and bytes, randomized or serialized target selection, and a convergence interval after action. Compare queue-delay savings against task warm-up and page-copy cost. On saturation, widen within preapproved envelopes before moving pages; on short phases, do neither. Record every decision's observations, generation and rejected alternatives, and disable adaptation safely when telemetry is stale or authorities disagree.

### Answer 5

Preserve kernel and scheduler configuration, topology and generations, affinity, cpusets, partitions, weights, quotas, classes, priorities, capacity data, frequency and thermal policy, IRQ and device routing, memory policy and residency, runtime configuration, binaries, inputs, seeds and workload phases. Compare the baseline against the change, static partitioning and deliberately adverse placement in randomized repeated runs.

Measure per-CPU runtime, runnable wait, utilization, capacity, queues, idle time, wakeups, local and remote placements, periodic and active attempts, failures, migrations, throttling, received fair service, deadline misses, cache and coherence events, NUMA traffic, interrupts, frequency, temperature, power, energy, throughput and latency distributions. Test uniform and skewed demand, bursts, continuous tasks, SMT, heterogeneous capacity, remote memory, device traffic, quotas, isolation, overload, CPU hotplug and rollback. Retain raw traces, version-specific counter interpretation, uncertainty, negative results, reviewer roles and limitations; a reduction in imbalance or migration counts alone does not establish better service.
