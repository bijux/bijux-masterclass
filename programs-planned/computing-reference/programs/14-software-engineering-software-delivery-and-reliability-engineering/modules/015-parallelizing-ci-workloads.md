---
module_id: SDRE-015
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 15
title: Parallelizing CI Workloads
status: complete
last_verified: 2026-09-06
---

# Parallelizing CI Workloads

## One-Page Review

### Governing question

How should a CI system schedule a dependency-constrained workload across finite, heterogeneous resources so that feedback becomes faster without changing what is checked, corrupting evidence, or hiding failures?

### Essential definitions

- a **job** is one schedulable CI unit with declared inputs, outputs, dependencies, resources, and result semantics;
- a **precedence graph** is a directed acyclic graph (DAG) whose edges state which jobs must finish before another may start;
- a **ready job** has every predecessor satisfied;
- **work** $W$ is the sum of all job processing times;
- **span** $S$ is the greatest total processing time along any dependency path, also called the critical-path length;
- a **critical path** is a path whose duration equals the span;
- **parallelism** is the amount of independent ready work, not merely the configured runner count;
- **makespan** $T_p$ is elapsed completion time on $p$ workers;
- a **resource constraint** limits CPU, memory, I/O, accelerator, license, environment, or another capacity;
- a **shard** is a stable partition of one logical workload with independently attributable inputs and results;
- **oversubscription** occurs when admitted work requests more effective capacity than the execution environment can supply;
- **fail-fast** cancels some remaining work after a decisive failure; **collect-all** continues to gather all planned results;
- an **evidence manifest** binds each result and artifact to the candidate, job definition, inputs, environment, and shard membership.

### Central model, mechanism, or theorem

For $p$ identical workers and an acyclic workload, every schedule obeys

$$
T_p \ge \max(W/p,S).
$$

No scheduler can process more than $p$ units of work per unit time, and no jobs on one dependency path can overlap. A practical scheduler repeatedly admits ready jobs whose resource requests fit available capacity, prioritizes latency-critical work, and records the resulting evidence. Adding workers cannot shorten the critical path or repair missing dependencies.

### Critical invariants

- schedule only the exact work selected for the exact candidate;
- encode real precedence rather than broad stage barriers or optimistic guesses;
- start a job only after all required predecessor outputs are available and verified;
- never exceed declared global and per-pool capacities;
- coordinate nested parallelism through one effective budget;
- make shards disjoint or explicitly define safe overlap;
- preserve a deterministic shard manifest and complete result aggregation;
- isolate mutable workspaces, ports, databases, credentials, and output paths;
- bind every artifact and check result to its producing job and candidate;
- distinguish queued, admitted, running, cancelled, failed, lost, timed out, and completed;
- preserve decisive diagnostics before cancellation;
- measure queue time, execution time, span, utilization, cost, and tail behavior separately.

### Common failures

Common failures include treating stages as necessary barriers, assuming worker count equals useful parallelism, splitting tests by file count rather than observed cost, starving long critical jobs, oversubscribing nested test runners, sharing mutable directories, racing on fixed ports, aggregating incomplete shards as success, mixing artifacts from candidates, cancelling away root-cause logs, retrying deterministic failures, and optimizing average duration while the slowest shard dominates feedback.

### Compact example

A build takes four minutes. Two test shards, lasting six and two minutes, depend on it; a one-minute package job depends on both. Work is $13$ minutes and span is $4+6+1=11$ minutes. With two workers, the lower bound is $\max(13/2,11)=11$ minutes, and a dependency-aware schedule attains it. A third worker cannot beat 11 minutes unless the six-minute shard or dependency chain changes.

### Connections

[SDRE-014](014-change-detection-and-selective-execution.md) determines which work is required. This module schedules that work. [SDRE-016](../ROADMAP.md) next coordinates candidate admission through merge queues, while [SDRE-018](../ROADMAP.md) treats flaky outcomes rather than scheduling them away.

## Governing Question

Parallel CI is not the act of adding a matrix keyword or purchasing more runners. It is the design of a valid schedule for an exact workload, under precedence, capacity, isolation, cost, and evidence constraints. The desired output is not merely a shorter clock time. It is the same justified decision, produced sooner and still traceable to the candidate that was evaluated.

The question therefore has three layers. What work is independent? Which ready work should run on which resources and when? How will the system prove that every required partition ran, that its outputs were not contaminated, and that cancellations did not turn missing evidence into success?

## Why This Matters

CI feedback governs integration delay. Long feedback encourages larger batches, delayed repair, and speculative work atop uncertain revisions. Yet careless parallelism can increase queueing, cost, nondeterminism, and operational load while leaving the critical path unchanged.

Mokhov, Mitchell, and Peyton Jones separate a build system's scheduler from its dependency model and rebuilder [1]. That separation is central here: SDRE-014 selected the necessary work; the scheduler decides a legal execution order. Changing scheduling policy must not silently change the selected claim set.

Current GNU Make documentation states that correct dependency declarations allow goals to be built correctly whether parallel execution is enabled, and its jobserver shares a finite job budget across recursive tools [2] and [3]. These are durable lessons beyond Make: correctness rests on dependency and isolation declarations, while nested components need coordinated resource admission.

Current GitHub Actions documentation exposes `max-parallel` and `fail-fast` as separate controls for matrix workloads [4]. Current GitLab documentation distinguishes stage barriers from explicit `needs` dependencies that let jobs start as soon as their actual predecessors finish [5]. Product syntax will change; the underlying distinctions among precedence, capacity, and failure policy remain.

## Prerequisites and Retrieval

Retrieve directed graph, vertex, edge, path, acyclic graph, topological order, dependency, transitive dependency, queue, worker, processing time, throughput, latency, utilization, CPU, memory, I/O, mutual exclusion, isolation, artifact, content digest, cache, test suite, percentile, mean, variance, retry, timeout, cancellation, and idempotence.

From SDRE-003 and SDRE-004 retrieve hermetic inputs, build reproducibility, incremental execution, and cache keys. From SDRE-011 through SDRE-014 retrieve candidate identity, fast feedback, integration delay, and affected-work selection. Algorithm Engineering owns general scheduling algorithms; Operating Systems owns processor scheduling and resource mechanisms; this chapter applies those foundations to CI decisions and evidence.

## Learning Objectives

After completing this module, you should be able to:

1. model a CI workflow as a precedence DAG with resource demands;
2. compute work, span, critical paths, and lower bounds on makespan;
3. replace accidental stage barriers with true dependencies;
4. distinguish job-level parallelism, sharding, and matrix expansion;
5. design stable, balanced shards from measured history;
6. prevent nested oversubscription and shared-state races;
7. choose fail-fast, collect-all, and cancellation policies by decision purpose;
8. preserve complete, candidate-bound evidence across parallel jobs;
9. diagnose queue, utilization, straggler, and tail-latency problems;
10. evaluate whether added concurrency improves feedback, throughput, and cost.

## Core Exposition

**Freeze the workload before scheduling it.** A scheduler consumes a workload specification: exact candidate identity, selected jobs, definitions, dependencies, required resources, shard manifests, priority class, timeouts, and result policy. It does not infer that skipped work is unnecessary. If selection changes because the candidate or merge base changes, invalidate the schedule and its evidence.

Separate four decisions. Selection decides *what* must run. Precedence decides *when a job becomes eligible*. Admission decides *whether capacity is available*. Placement decides *where an admitted job runs*. Blurring these produces familiar errors: a job omitted because no runner matched it, or a capacity throttle represented as a false dependency.

**Represent true precedence as a DAG.** Let an edge $u\rightarrow v$ mean $v$ requires a successful output or decision from $u$. A job becomes ready only after every required predecessor reaches an acceptable terminal state. The graph must be acyclic for ordinary batch scheduling. A detected cycle is a configuration error or a sign that the units were drawn at the wrong boundary.

Coarse stages impose a barrier: every job in stage one must finish before any job in stage two begins. Barriers are easy to visualize, but they serialize unrelated paths. If `docs-test` needs only checkout while `integration-test` needs a compiled service, an explicit dependency graph starts documentation checks immediately and integration checks after the build. GitLab's current `needs` guidance describes this exact distinction [5].

Do not remove a real edge merely to expose more parallelism. If a test consumes a generated client, it depends on the generator output even when the test often passes against stale files. Parallel execution is a stress test for hidden dependencies: a serial order may have accidentally made undeclared state available.

**Calculate work and span before buying capacity.** Give each job $v$ an estimated processing time $d(v)>0$. Total work is

$$
W=\sum_{v\in V}d(v).
$$

For a path $P$, its duration is $\sum_{v\in P}d(v)$; span $S$ is the maximum path duration. On $p$ identical unit-capacity workers, $T_p\ge W/p$ by conservation of work and $T_p\ge S$ by precedence. Hence the combined lower bound in the review.

The ratio $W/S$ is average available parallelism in the work-span model. It is a ceiling on useful worker growth, not a promise that every scheduler or resource pool realizes it. If $W=100$ minutes and $S=80$, the average parallelism is only $1.25$ even if a thousand jobs briefly become ready.

Estimates are evidence, not truths. Record observed queue-free durations by job definition, platform, size class, cache state, and recent revision range. Use robust statistics such as medians and high percentiles; retain cold-start and miss distributions. A changed test population or runner image can invalidate history.

**Schedule ready work, not configured work.** A basic list scheduler maintains a ready queue. When a worker becomes available, it chooses a ready job, reserves its resource vector, launches it in an isolated environment, and releases resources at termination. Completed outputs unlock successors. The policy can prefer jobs with large remaining critical-path length, short diagnostic value, age, or service-class weight.

Prioritizing the longest remaining path often protects makespan. Prioritizing quick linters can produce early failure information. These objectives can conflict. A practical policy may reserve some capacity for fast diagnostics while preventing starvation of long critical jobs. State the objective instead of hiding it in queue order.

**Model more than worker count.** Real jobs request vectors: CPU cores, memory, local disk, network bandwidth, accelerator type, licensed seats, privileged execution, architecture, secret scope, or exclusive environment. A job fits only when every required dimension and placement constraint is satisfied. Eight nominal workers do not imply that eight 8-GiB jobs fit on a 16-GiB host.

Use separate pools where trust, platform, or performance differs. Untrusted contributions should not inherit secret-bearing runners. Platform-specific jobs must not be marked skipped because their pool is unavailable; they are unavailable evidence and should block a gate that requires them.

**Coordinate nested parallelism.** A CI system may run four jobs, each launching eight compiler or test processes. The apparent parallelism is four; the host demand is 32. Oversubscription causes context switching, memory pressure, I/O contention, timeouts, and noisy duration data. Either assign each job an isolated capacity limit or propagate a shared token budget.

GNU Make's documented jobserver is a concrete implementation: recursive tools share job slots, and participants must return acquired tokens even on errors [3]. The general invariant is resource conservation. Every acquired capacity token is returned exactly once, including cancellation and crash recovery.

**Choose the right unit.** Job-level parallelism runs independent targets concurrently. Sharding partitions one large logical check. Matrix expansion evaluates combinations such as platform, runtime, or configuration. These mechanisms solve different problems.

A matrix dimension is justified when each combination represents a distinct compatibility claim. Cartesian products can explode cost; use explicit supported combinations and risk-based coverage. Current GitHub Actions supports a cap on simultaneous matrix jobs independently of matrix definition [4], demonstrating that workload shape and admitted concurrency are separate controls.

Shard membership should be explicit and reproducible. Hash partitioning is stable and cheap but can be badly imbalanced. Equal file counts ignore duration. Historical-duration bin packing improves balance but must define behavior for new tests and stale estimates. Dynamic work stealing balances tails well but requires an authoritative dispatcher and a complete record of which items ran.

Never let workers independently discover shards from mutable state. Freeze an ordered item manifest, partition it, give every shard an identity, and aggregate against the frozen manifest. Success requires every required item exactly once unless overlap is an explicit policy. A missing shard is not a passing suite.

**Control mutable state.** Parallel jobs expose races hidden by serial execution. Give jobs separate workspaces, output directories, caches with safe write semantics, temporary namespaces, databases, credentials, and port allocation. Use immutable input artifacts or content-addressed stores. If a resource is inherently exclusive, model a lock or capacity of one rather than relying on timing.

Avoid one shared “latest” artifact name. A consumer should request an artifact by candidate, producer job, configuration, and digest. Verify the digest after transfer. Aggregators should reject artifacts from another attempt or candidate, even when filenames match.

**Define failure and cancellation policy.** Fail-fast saves capacity and shortens a negative decision when one failure is decisive. Collect-all yields a fuller defect inventory and better diagnosis. Neither is universally correct. GitHub's current matrix controls make fail-fast and tolerated experimental failures independent policy choices [4].

Cancellation is a state transition, not deletion. Record why a job was cancelled, whether it started, which outputs are invalid, and whether logs were preserved. Stop downstream jobs that can no longer produce relevant evidence, but allow cleanup and root-cause capture. A cancelled shard is incomplete, not passed.

Retries address infrastructure loss or explicitly classified transient failures, not arbitrary red builds. Retrying everything biases duration and failure metrics, consumes capacity, and can conceal deterministic defects. Bind every attempt to one logical job; aggregate policy chooses which attempt, if any, satisfies the claim.

**Treat the queue as part of latency.** Feedback time includes graph construction, queue delay, provisioning, setup, execution, artifact transfer, aggregation, and reporting. Increasing per-workflow parallelism can reduce one workflow's execution while delaying every other workflow. Under sustained load, capacity, arrival rate, and service time determine queue growth.

Apply fair admission across repositories and priority classes. Bound per-candidate concurrency so one large matrix cannot monopolize the fleet. Reserve capacity for urgent repair or mainline verification only through an explicit policy with anti-starvation rules. Preempt only jobs whose cancellation and restart costs are understood.

**Measure the right boundary.** Report end-to-end feedback percentiles, not only average job duration. Measure queue time, ready-but-not-admitted time, setup, execution, critical-path estimate error, runner utilization, CPU and memory saturation, shard imbalance, cancellation waste, retry work, artifact-transfer time, and cost per accepted candidate.

Compare before and after using similar workload populations and cache conditions. More utilization is not always better: capacity headroom absorbs bursts and limits tail latency. More parallelism is valuable when it reduces the targeted decision latency or improves throughput within reliability and cost bounds.

## Definitions and Notation

Let $G=(V,E)$ be a DAG. Job $v\in V$ has duration $d(v)>0$, resource demand vector $r(v)$, and eligible worker set $M(v)$. Edge $(u,v)\in E$ means $v$ may start only after $u$ produces an acceptable terminal result and required output.

With start time $s(v)$ and finish time $f(v)=s(v)+d(v)$, precedence requires

$$
f(u)\le s(v)\quad\text{for every }(u,v)\in E.
$$

At every time $t$, admitted jobs $A_t$ must obey componentwise capacity $C$:

$$
\sum_{v\in A_t}r(v)\le C.
$$

The makespan is $T_p=\max_{v\in V}f(v)-\min_{v\in V}s(v)$. For identical workers, work $W=\sum_v d(v)$ and span

$$
S=\max_{P\text{ is a path in }G}\sum_{v\in P}d(v).
$$

Speedup relative to a recorded serial schedule is $W/T_p$ only when the serial schedule performs exactly the same work with comparable setup and cache conditions. Efficiency is $W/(pT_p)$ under the same assumptions. These ratios are invalid when work selection, retries, or environments differ.

For shards $Q_1,\dots,Q_k$ of item universe $U$, complete disjoint partitioning requires

$$
\bigcup_{i=1}^{k}Q_i=U
\quad\text{and}\quad
Q_i\cap Q_j=\varnothing\text{ for }i\ne j.
$$

An intentional replicated check relaxes disjointness but must still be labeled so duplicate results are not mistaken for extra coverage.

## Mechanisms, Invariants, or Proof Structure

**Lower-bound proof.** During $T_p$ time, $p$ identical workers provide at most $pT_p$ worker-time. Completing work $W$ requires $pT_p\ge W$, hence $T_p\ge W/p$. Jobs along a dependency path cannot overlap, so the longest path requires at least $S$. Both constraints apply simultaneously, giving $T_p\ge\max(W/p,S)$. This proves a lower bound under the model, not attainability on heterogeneous real runners.

**Readiness invariant.** Initialize indegree counts from the frozen DAG. A job enters the ready queue only when each predecessor has produced the required acceptable result. On completion, decrement each successor's remaining count exactly once. An early launch implies a missing or bypassed edge; a negative count implies duplicate completion processing.

**Capacity invariant.** Admission atomically subtracts the complete demand vector from available capacity. Termination returns exactly the reserved vector once. Partial reservation or double return can oversubscribe the pool. Lost workers require lease expiry and reconciliation, not blind token creation.

**Shard-completeness argument.** An aggregator compares result item identities against frozen $U$. It rejects any missing item, unexpected item, conflicting duplicate, wrong candidate, or wrong shard-plan digest. Thus success is derived from manifest coverage plus passing results, not merely from the number of workers that reported success.

**Executable scheduling model.** The model computes work and span, simulates a two-worker precedence schedule, balances independent shard weights greedily, and checks two conservative admission decisions. It assumes identical workers and deterministic durations; it is not a production scheduler.

<!-- bijux-verify: {"id":"ci-parallelism-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"work=13\nspan=11\ntwo_worker_lower_bound=11\nschedule_makespan=11\nspeedup=1.18\nbalanced_shards=[13, 13, 13]\nmemory_oversubscription_rejected=True\nmissing_dependency_fallback=serial\n","stderr":""}} -->
```python
jobs = {
    "build": {"duration": 4, "needs": set()},
    "unit-a": {"duration": 6, "needs": {"build"}},
    "unit-b": {"duration": 2, "needs": {"build"}},
    "package": {"duration": 1, "needs": {"unit-a", "unit-b"}},
}

def critical_finish(name, memo):
    if name in memo:
        return memo[name]
    predecessors = jobs[name]["needs"]
    prior = max((critical_finish(item, memo) for item in predecessors), default=0)
    memo[name] = prior + jobs[name]["duration"]
    return memo[name]

def schedule(worker_count):
    completed = set()
    running = []
    clock = 0
    while len(completed) < len(jobs):
        ready = sorted(
            name for name, job in jobs.items()
            if name not in completed
            and all(name != active[1] for active in running)
            and job["needs"] <= completed
        )
        while ready and len(running) < worker_count:
            name = max(ready, key=lambda item: (jobs[item]["duration"], item))
            ready = [item for item in ready if item != name]
            running.append((clock + jobs[name]["duration"], name))
        next_finish = min(finish for finish, _ in running)
        clock = next_finish
        finished = {name for finish, name in running if finish == clock}
        completed.update(finished)
        running = [(finish, name) for finish, name in running if finish != clock]
    return clock

weights = [9, 8, 7, 6, 5, 4]
bins = [0, 0, 0]
for weight in sorted(weights, reverse=True):
    index = min(range(len(bins)), key=lambda item: bins[item])
    bins[index] += weight

work = sum(job["duration"] for job in jobs.values())
span = max(critical_finish(name, {}) for name in jobs)
lower_bound = max((work + 1) // 2, span)
makespan = schedule(2)
print(f"work={work}")
print(f"span={span}")
print(f"two_worker_lower_bound={lower_bound}")
print(f"schedule_makespan={makespan}")
print(f"speedup={work / makespan:.2f}")
print(f"balanced_shards={sorted(bins)}")
print(f"memory_oversubscription_rejected={2 * 6 > 8}")
print("missing_dependency_fallback=serial")
```

The final fallback is policy, not an algorithmic result: when independence cannot be established, preserve a known safe order or leave the gate incomplete until dependencies are corrected.

## Alternatives and Trade-Offs

**Stage barriers versus a DAG.** Stages are simple and provide recognizable milestones. A DAG exposes more concurrency and more accurately models artifacts, but demands complete dependencies and better visualization.

**Static shards versus dynamic dispatch.** Static shards are reproducible and easy to rerun. Dynamic dispatch reduces stragglers when item costs vary, but adds coordination, needs durable item-level results, and can make exact reproduction harder. Freeze the work universe in both cases.

**Hashing versus measured balance.** Hashing gives stable membership with low planning cost. Historical weighting reduces expected maximum shard time but can churn membership and inherits stale measurements. Pin a plan per candidate and treat unknown tests conservatively.

**Fail-fast versus collect-all.** Fail-fast saves capacity after decisive failure. Collect-all exposes independent defects and produces better batch diagnosis. Preserve failure evidence and distinguish cancellation from success whichever policy applies.

**Local versus remote execution.** Local execution has low transfer overhead and simple trust boundaries. Remote execution expands capacity and can improve environmental consistency; Bazel's official overview lists parallel scaling and consistent environments as benefits, while also requiring rules suitable for remote execution [6]. Remote work adds queueing, transfer, authentication, and service-failure boundaries.

**Dedicated versus shared runners.** Dedicated capacity gives predictable latency and isolation but may idle. Shared fleets improve aggregate utilization but create noisy neighbors and fairness concerns. Separate trust zones regardless of utilization strategy.

**More workers versus smaller critical work.** Capacity helps when ready jobs wait for workers. Refactoring a long job, improving caching, or reducing serial setup helps when span dominates. Measure before choosing.

**Per-candidate speed versus fleet throughput.** Giving one candidate every runner minimizes its local time but can increase organization-wide queue delay. Concurrency caps and fair queues trade isolated latency for stable throughput and bounded tails.

## Failure Modes and Misconceptions

- **“Ten runners make CI ten times faster.”** Span, placement, setup, and contention bound speedup.
- **“Jobs in the same stage are independent.”** Stage membership is not a dependency proof.
- **“Removing an edge improves performance.”** It may only introduce a stale-artifact race.
- **“All ready jobs fit.”** Resource vectors and eligible pools can block placement.
- **“One runner equals one core.”** Job and host capacity are different quantities.
- **“Each job may use all CPUs.”** Nested parallelism can oversubscribe the host.
- **“Equal test counts make equal shards.”** Test durations and setup costs vary.
- **“Historical duration is exact.”** caches, inputs, runners, and tests change.
- **“A matrix is sharding.”** A matrix usually represents distinct configurations; shards partition one claim set.
- **“Four passing shards mean the suite passed.”** The frozen manifest may require five.
- **“Duplicate tests are harmless.”** They can hide missing items and distort evidence.
- **“Shared output paths are faster.”** Concurrent writers can corrupt artifacts or leak state.
- **“Fail-fast means failed jobs disappear.”** cancellation and partial outputs require records.
- **“A retry converts failure to reliability.”** It may conceal a deterministic or flaky defect.
- **“Remote execution removes bottlenecks.”** It moves some work and introduces transfer and service constraints.
- **“High utilization proves efficiency.”** Saturation can produce long queues and poor tail latency.
- **“Average duration represents feedback.”** Stragglers and queue spikes govern high percentiles.
- **“A skipped platform is a pass.”** Unavailable required evidence blocks the decision.

## Worked Examples

### Example 1

**Situation.** Build takes four minutes; test shards take six and two after build; packaging takes one after both. **Reasoning.** Work is $4+6+2+1=13$. Paths have lengths $4+6+1=11$ and $4+2+1=7$, so span is 11. With two workers, the lower bound is $\max(6.5,11)=11$ minutes. Running both tests together after build attains 11. **Conclusion.** The critical path, not worker count, fixes the optimum.

### Example 2

**Situation.** A staged pipeline has independent two-minute lint and documentation checks wait behind an eight-minute build. **Reasoning.** The stage barrier yields at least ten minutes before their results. If both depend only on checkout, explicit edges make them ready at time zero while the build runs. **Conclusion.** Replace accidental barriers with true precedence, never with deleted real dependencies.

### Example 3

**Situation.** Four CI jobs each start eight test processes on an eight-core host. **Reasoning.** Demand becomes 32 runnable processes before runtime helpers, causing contention and misleading timeouts. Give each job two cores, admit one eight-process job, or share a token budget. **Conclusion.** Coordinate nested parallelism against physical or enforced capacity.

### Example 4

**Situation.** Thirty tests are split into three shards of ten files, but one shard takes 24 minutes and the others take four. **Reasoning.** File count ignored measured cost. Use recent, context-matched duration estimates and greedy bin packing, while assigning unseen tests a conservative weight. Freeze the resulting plan for the candidate. **Conclusion.** Balance predicted work, then measure actual stragglers.

### Example 5

**Situation.** Five shards were planned; four report success and one runner is lost. **Reasoning.** Counting successful reports produces false assurance. The aggregator compares item and shard identities with the frozen manifest, marks the suite incomplete, and retries only the lost infrastructure attempt if policy permits. **Conclusion.** Completeness precedes pass/fail aggregation.

### Example 6

**Situation.** Two integration shards use the same database name and fixed port. **Reasoning.** Their tests are logically independent but the environment is not. Namespace databases and allocate ports per shard, or serialize access through an exclusive resource. **Conclusion.** Parallel safety includes environmental isolation, not only code dependencies.

### Example 7

**Situation.** A fast linter fails while eight expensive tests are running. **Reasoning.** For an admission gate where lint failure is decisive, fail-fast can cancel downstream work after preserving the linter evidence. For a scheduled diagnostic run, collect-all may be more valuable. Cancelled tests remain incomplete. **Conclusion.** Failure policy follows decision purpose.

### Example 8

**Situation.** A package job downloads `build.zip`, but a concurrent candidate published the same name later. **Reasoning.** Filename identity is insufficient. Request the artifact using candidate, producer, configuration, attempt, and digest; verify the digest before use. **Conclusion.** Parallel pipelines require immutable, subject-bound artifacts.

### Example 9

**Situation.** Doubling a project's concurrency from 20 to 40 reduces execution by two minutes but adds eight minutes to fleet queue time during peaks. **Reasoning.** Local runtime improved while end-to-end and shared throughput worsened. Cap per-candidate concurrency, apply fair admission, and compare percentile feedback and cost. **Conclusion.** Optimize at the decision and fleet boundary, not one job chart.

### Example 10

**Situation.** A remote pool has abundant CPU, but each shard transfers a 6-GiB artifact before a one-minute test. **Reasoning.** Transfer dominates useful work and can saturate the network. Reduce artifact granularity, place computation near content-addressed data, or keep these tests local. **Conclusion.** Remote capacity helps only after placement and data-movement costs are modeled.

## Cross-Program Connections

- Algorithm Engineering owns precedence-constrained scheduling algorithms, bounds, and approximation analysis.
- Data Structures Engineering owns DAG representation, ready queues, heaps, and work-stealing deques.
- Operating Systems owns process scheduling, resource accounting, isolation, and oversubscription behavior.
- Concurrent & Parallel Programming owns work/span reasoning, synchronization, races, and nested parallelism.
- Testing & Quality Engineering owns test independence, sharding validity, failure classification, and coverage claims.
- Platform Engineering owns runner fleets, admission services, autoscaling, artifact transport, and tenant isolation.
- Systems Engineering owns capacity planning, queues, bottleneck analysis, and end-to-end trade-offs.
- Security Engineering owns untrusted-code placement, secret isolation, artifact integrity, and cancellation abuse.
- Data Engineering owns lineage and completeness patterns analogous to shard manifests and result aggregation.

## References

1. Andrey Mokhov, Neil Mitchell, and Simon Peyton Jones, [Build Systems à la Carte](https://doi.org/10.1145/3236774), *Proceedings of the ACM on Programming Languages*, ICFP 2018, Article 79.
2. GNU Project, [GNU Make Manual: Parallel Execution](https://www.gnu.org/software/make/manual/html_node/Parallel.html) and [Disabling Parallel Execution](https://www.gnu.org/software/make/manual/html_node/Parallel-Disable.html), current official manual. Retrieved 2026-09-06.
3. GNU Project, [GNU Make Manual: Sharing Job Slots](https://www.gnu.org/software/make/manual/html_node/Job-Slots.html), current official jobserver documentation. Retrieved 2026-09-06.
4. GitHub, [Running Variations of Jobs in a Workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations), official documentation for matrix, failure, and maximum-parallel controls. Retrieved 2026-09-06.
5. GitLab, [Make Jobs Start Earlier with `needs`](https://docs.gitlab.com/ci/yaml/needs/), official DAG scheduling guidance. Retrieved 2026-09-06.
6. Bazel Project, [Remote Execution Overview](https://bazel.build/docs/remote-execution), official documentation. Retrieved 2026-09-06.
7. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, DAGs, critical paths, and scheduling foundations.
8. Leslie Lamport, [Time, Clocks, and the Ordering of Events in a Distributed System](https://doi.org/10.1145/359545.359563), *Communications of the ACM* 21(7), 1978, ordering foundations used when reasoning about concurrent events and evidence.

## Exercises

### Exercise 1

Define work, span, makespan, and ready job. Explain why configured runner count is not the same as parallelism.

### Exercise 2

A DAG has jobs `A=3`, `B=5`, `C=2`, and `D=4` minutes. `B` and `C` depend on `A`; `D` depends on both. Compute work, span, the two-worker lower bound, and a legal two-worker schedule.

### Exercise 3

A 16-core runner admits four CI jobs, and each job launches eight compiler processes while requesting 3 GiB on a 10-GiB host. Diagnose both CPU and memory admission defects and propose a coherent policy.

### Exercise 4

Design a sharding and aggregation scheme for 2,000 tests whose durations vary, 50 tests are new, some require an exclusive database, and workers may disappear. Include exact evidence needed for a release gate.

### Exercise 5

A team can buy twice as many runners, split a 40-minute serial integration job, or replace stage barriers with dependency edges. Design an experiment and decision rule that accounts for feedback percentiles, fleet throughput, reliability, and cost.

## Answers to the Exercises

### Answer 1

Work is the sum of processing times for the exact jobs performed. Span is the longest dependency-path duration. Makespan is elapsed time from the first job start to the final completion under a particular schedule. A ready job has all required predecessors satisfied. Runner count is capacity; parallelism exists only when independent ready jobs fit eligible resources. Ten idle runners cannot shorten a single ten-minute dependency chain.

### Answer 2

Work is $3+5+2+4=14$ minutes. The paths are `A→B→D`, lasting $3+5+4=12$, and `A→C→D`, lasting $3+2+4=9$, so span is 12. The work bound on two workers is $14/2=7$; the combined lower bound is 12. Run `A` from 0–3, `B` from 3–8 and `C` from 3–5, then `D` from 8–12. The schedule is legal and attains 12 minutes, so it is optimal under the stated deterministic identical-worker model.

### Answer 3

Four jobs can demand 32 compiler processes on 16 cores, an oversubscription factor of two before other processes. Their declared memory totals 12 GiB, exceeding 10 GiB. Admission should reserve both CPU and memory atomically: for example, admit at most two jobs, allocate each eight cores and at least 3 GiB, and enforce those limits; or reduce each job's internal compiler concurrency and memory reservation so a validated larger combination fits. A shared token mechanism prevents inner compilers from ignoring the outer budget. On cancellation, reservations must be returned exactly once.

### Answer 4

Freeze the candidate, ordered universe of 2,000 test identities, definitions, environment, and shard-plan digest. Estimate durations from context-matched recent runs; give unseen tests conservative weights and distribute items to minimize predicted maximum load. Put exclusive-database tests into a queue with database capacity one or provision isolated databases. Each worker receives explicit item identities and returns per-item result, attempt, timing, logs, environment, candidate, and shard-plan binding. A lease detects lost workers and permits a new attempt without counting both as independent coverage. Aggregation rejects missing, unexpected, conflicting duplicate, wrong-candidate, or wrong-plan results. The release gate passes only when every required item has an accepted passing result and every required platform and policy check is complete; cancelled or unavailable work is not a pass.

### Answer 5

First instrument queue, setup, execution, artifact transfer, ready-but-blocked time, critical paths, resource saturation, retries, cancellations, and end-to-end feedback percentiles by workload class. On comparable candidate populations, test each intervention within safe capacity limits. Extra runners should help when ready work waits for capacity; edge refinement should help when broad barriers delay independent jobs; splitting should help when the 40-minute job dominates span, provided partitions are complete and isolated. Compare median and high-percentile feedback, accepted-candidate throughput, failure and missing-evidence rates, shard imbalance, and total cost. Choose an intervention only if it improves the predeclared latency or throughput objective without increasing evidence defects, starvation, or cost beyond the agreed bound. Preserve candidate binding and fall back if dependency or shard correctness is uncertain.
