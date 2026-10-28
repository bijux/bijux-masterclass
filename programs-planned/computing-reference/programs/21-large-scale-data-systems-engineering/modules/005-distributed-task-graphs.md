---
module_id: LSDS-005
program: Large-Scale Data Systems Engineering
level: 1
module_number: 5
title: Distributed Task Graphs
status: complete
last_verified: 2026-09-03
---

# Distributed Task Graphs

## One-Page Review

### Governing question

How should a distributed computation be represented as tasks and dependencies so that parallelism, communication, scheduling, retries, state, side effects, and completion are explicit and correct?

### Essential definitions

- A **task graph** is a directed graph whose vertices represent executable work units and whose edges represent declared dependencies or channels.
- A **logical graph** describes operators and semantic dependencies before parallel expansion and physical placement.
- A **physical execution graph** expands logical operators into partition-level tasks, attempts, exchanges, and runtime resources.
- A **data dependency** requires an upstream value, partition, stream, or materialized artifact.
- A **control dependency** constrains execution order without necessarily carrying application data.
- A **ready task** has every required predecessor outcome available under the graph's execution semantics.
- **Work** is total task cost; **span** or **critical-path length** is the greatest dependency-chain cost.
- **Lineage** records how an output can be derived from prior data and transformations.

### Central model, mechanism, or theorem

For a finite directed acyclic task graph `G=(V,E)`, edge `(u,v)` means `v` cannot complete correctly before the required outcome of `u` exists. With vertex duration `c(v)`:

`ES(v)=max_(u in pred(v)) EF(u)` and `EF(v)=ES(v)+c(v)`, with an empty maximum equal to zero.

Total work is `W=sum_v c(v)` and span is `S=max_v EF(v)`. On `p` ideal identical workers, execution time is bounded below by `max(W/p,S)`. Communication, placement, resource constraints, skew, failures, and scheduler overhead can only raise observed time. Cyclic and unbounded computations need progress semantics richer than ordinary DAG completion.

### Critical invariants

- Every vertex, output, logical partition, and execution attempt has a stable distinct identity.
- Edges state whether they carry data, order, state, barrier, resource, or side-effect constraints.
- A task becomes ready only under the declared availability/materialization semantics of every required input.
- Graph construction rejects unintended cycles; intended iteration has explicit epoch/progress rules.
- Retryable tasks are deterministic or otherwise reconcile repeated attempts and external effects.
- Materialized outputs are versioned, complete, validated, and retained for their declared consumers.
- Graph rewrites preserve observable results, side-effect order, partitioning, and failure behavior.
- Completion is defined for the computation model rather than inferred from scheduler idleness.

### Common failures

Frequent failures are confusing an operator with one task, treating graph edges as mere visualization, omitting hidden dependencies, assuming DAG means deterministic, retrying side effects blindly, materializing every edge, losing lineage too early, counting total work without the critical path, representing an infinite stream as a completing batch DAG, and adapting a running graph without versioned semantics.

### Compact example

Two scans can run concurrently. A join waits for both, then an aggregate and audit branch can run concurrently, and publication waits for both branches. Adding workers cannot reduce runtime below the longest scan-to-publication chain. If the join's output is lost, lineage identifies which downstream results are invalid and what must be recomputed.

### Connections

[LSDS-004](004-data-locality.md) prices vertex placement and edge movement. [LSDS-006](../ROADMAP.md) develops stages, tasks, and dependency categories in greater detail. [LSDS-007](../ROADMAP.md) distinguishes narrow from wide transformations. Task graphs also connect to [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Data Engineering](../../19-data-engineering/ROADMAP.md).

## Governing Question

A distributed program is not just a list of functions sent to workers. Some work can proceed concurrently, some requires data produced elsewhere, some exchanges partitions, some maintains state across records, and some performs effects that cannot safely repeat. A graph makes these relationships available to a planner, scheduler, recovery controller, operator, and reviewer.

The useful graph is more than boxes and arrows. Each vertex needs semantic identity, code/version, input contract, partitioning, resources, retry behavior, and output rules. Each edge needs a dependency kind, transport or materialization behavior, ordering, partition relation, and lifetime. The runtime then expands the logical program into task instances and execution attempts whose state changes over time.

The governing question is: what graph representation exposes enough structure to execute and recover the computation without pretending that every dependency is identical? For bounded acyclic work, topological readiness provides a clear basis. Iterative, recursive, stateful streaming, and dynamically generated work require explicit progress or epoch semantics rather than being forced into a misleading static DAG.

## Why This Matters

Graphs reveal parallelism. Independent source partitions or branches can run together, while a join, barrier, or aggregate constrains readiness. An imperative submission sequence can hide this concurrency; a graph allows the runtime to schedule any ready vertices subject to resources and policy.

Graphs expose communication. An edge may carry a local iterator, a pipeline, a network stream, a materialized file, a shuffle partition, or a small control token. Dryad described distributed applications as computational vertices connected by communication channels, allowing the runtime to choose mechanisms and placement. The arrow therefore has storage, transport, backpressure, failure, and cleanup consequences.

Graphs bound ideal completion. Total work describes aggregate resource demand, but the critical path describes the dependency chain that no amount of parallel hardware can shorten without changing the graph or vertex costs. A job with thousands of independent tasks and one long serial finalize step can have high apparent parallelism and a stubborn tail.

Graphs support optimization. A planner can fuse adjacent operators, push filters, eliminate unused branches, choose exchange strategies, adjust parallelism, or reuse common subgraphs. Such rewrites are correct only if they preserve semantics, including side effects, ordering, nondeterminism, state, failure behavior, and resource feasibility.

Graphs support recovery. If a materialized partition is lost, lineage can identify its producing task and dependencies. Spark's RDD paper uses restricted transformations and lineage for recovery without requiring every intermediate to be durably replicated. Recomputability is conditional: sources must remain available, transformations must be reproducible, external effects must be controlled, and the recovery cone must be affordable.

Graphs support operations. Runtime state can locate queued, running, blocked, failed, retried, or completed attempts; identify a critical or skewed vertex; attribute transfer; and explain why a sink is not ready. A static logical diagram alone cannot do that. Operators need mappings from logical operator to physical task, attempt, worker, input partition, output, and epoch.

Finally, the graph encodes correctness boundaries. A missing edge can let a consumer observe incomplete input. An unnecessary edge serializes independent work. A cycle in a batch DAG can deadlock readiness. An untracked side effect can repeat after retry. Graph design is therefore part of the execution contract, not merely a performance representation.

## Prerequisites and Retrieval

You should understand directed graphs, vertices, edges, paths, cycles, topological ordering, partitions, processes, files, streams, retries, and basic asymptotic reasoning. Recall from [LSDS-003](003-range-hash-and-consistent-partitioning.md) that logical partitions differ from placement, and from [LSDS-004](004-data-locality.md) that a data dependency carries a location-sensitive cost.

Retrieve two graph facts. A finite directed graph has a topological ordering exactly when it is acyclic. In a DAG, repeatedly removing all vertices with no remaining predecessors either consumes every vertex or reveals a cycle. Also recall that graph reachability differs from immediate adjacency: losing one output can invalidate all reachable descendants even when they do not read it directly.

## Learning Objectives

After completing this module, you should be able to:

- distinguish program, logical operator, physical task, and execution-attempt graphs;
- classify data, control, barrier, state, resource, and side-effect dependencies;
- derive stable topological readiness levels or diagnose a cycle;
- compute total work, earliest finishes, critical path, and ideal lower bounds;
- explain pipelined versus materialized edges and their failure implications;
- trace lineage and bound a lost output's recomputation cone;
- specify task identity, output commit, retry, cancellation, and speculation semantics;
- explain graph fusion, expansion, pruning, and adaptive rewrites;
- represent bounded, unbounded, iterative, and dynamically generated work honestly;
- design graph-level observability, tests, and high-consequence review.

## Core Exposition

### From program to logical graph

A user program may be imperative, functional, relational, declarative, or event-driven. The system extracts or constructs a logical graph of sources, transformations, stateful operators, and sinks. A SQL query can become a relational operator graph. Collection transformations can build a lazy lineage graph. An asynchronous task API can create dependencies as object references are passed.

Logical vertices express semantic operations such as scan, filter, join, aggregate, model inference, or publish. They need not be one process or one scheduled unit. A scan vertex over 1,000 partitions can become 1,000 physical tasks; a chain of map-like operators can be fused into one task; a join can introduce several producer and consumer task sets.

Logical edges describe required relationships. A relational edge may carry a partitioned dataset with schema and distribution. A stream edge may carry unbounded records plus watermarks. A control edge may require successful validation before publication. A graph that records only labels but omits schemas, partitioning, ordering, and completion conditions is insufficient for execution.

Graph construction should validate stable identifiers, unique vertices, valid endpoints, input arity, type/schema compatibility, partition contracts, resource declarations, and allowed cycles. Diagnostics should identify the actual dependency path, not merely say “invalid graph.”

### Physical expansion

The planner lowers logical operators into a job or physical graph. Parallelism expands a logical vertex into task vertices indexed by partition or subtask. Exchanges add intermediate result partitions and consumers. Fusion or chaining can combine compatible operators to avoid serialization and scheduling overhead.

An execution attempt is not the task itself. Task `join[17]` may have attempts `a0` and `a1` because of failure or speculation. The scheduler must distinguish task outcome identity from attempt identity so duplicate attempts do not create duplicate logical output. Flink's current `ExecutionGraph` documentation explicitly distinguishes job vertices, parallel execution vertices, and attempts.

Physical edges encode transport. A pipelined edge can allow the consumer to process records while the producer runs. A blocking/materialized edge requires a complete output or partition set before consumers proceed. A broadcast edge replicates one result to many tasks. A shuffle routes records by a new partition function. Later modules develop stage and exchange mechanics; here the central point is that these choices change readiness and recovery.

Physical graphs also include resource and placement constraints. A GPU task, co-located actor group, node-local state, or isolation boundary restricts candidates. These are not necessarily data edges, but they affect whether ready work is runnable. Distinguish dependency readiness from resource availability.

### Dependency semantics

A **data dependency** means the consumer needs a producer's value or partition. It should define whether partial/pipelined consumption is permitted, how completeness is signaled, what version is required, and whether the data survives producer failure.

A **control dependency** requires an event such as successful validation, approval, lease acquisition, or prior completion. It can carry no large dataset but still constrain correctness. Hidden control through shared external state is dangerous because the scheduler cannot reason about it.

A **barrier dependency** requires a group of tasks or epochs to reach a point before progress. Barriers simplify some global coordination and can amplify the slowest task. They require membership and failure semantics: what happens if one participant is lost or replaced?

A **state dependency** binds a task or operator to prior state, checkpoint, or ordered event history. State may constrain placement and recovery beyond ordinary immutable inputs. Stateful streaming cannot be modeled as independent one-shot functions without losing its correctness conditions.

A **resource dependency** requires a capability or reservation rather than a predecessor value. A graph should not fake this as a data edge; schedulers need resource feasibility, gang requirements, and capacity separately.

A **side-effect dependency** constrains observable external operations. Publishing, charging, sending a command, or mutating a nontransactional service may need an idempotency key, transaction/outbox protocol, or separately committed sink boundary. DAG acyclicity does not make repeated execution safe.

### Readiness and topological execution

For a bounded DAG with blocking edges, a vertex is ready when all required predecessors have valid committed outputs. A stable topological algorithm begins with zero-indegree vertices, removes them, and exposes new ready vertices. If vertices remain but none is ready, the declared graph has a cycle or unresolved external dependency.

Pipelined graphs use finer readiness. A consumer can start after channels exist or first records arrive even though producers have not completed. Completion still depends on end-of-input signals and channel failure semantics. Treating start-readiness and completion-readiness as the same loses concurrency or correctness.

Readiness does not imply immediate execution. Resources, locality, fairness, quotas, priorities, and admission constraints decide which ready tasks run. Conversely, an idle worker does not make a dependency-blocked task ready. Observability should distinguish blocked-on-input, ready-queued, resource-infeasible, admitted, and running.

### Work, span, and achievable parallelism

Let each vertex have modeled duration `c(v)`. Earliest start is the greatest predecessor earliest finish, and earliest finish adds its duration. The maximum earliest finish is the critical-path length or span `S`. Total work `W` sums vertex durations.

With `p` identical ideal workers, runtime cannot be below `W/p` because workers must perform all work, nor below `S` because critical-path vertices are sequentially constrained. Thus `T_p >= max(W/p,S)`. This is a lower bound, not a schedule prediction. Resource heterogeneity, edge transfer, skew, queueing, failures, and overhead raise actual runtime.

Average parallelism `W/S` indicates how much concurrency the graph exposes over its critical duration in the ideal model. A wide layer count is not enough: task durations differ, edges can pipeline, and resource constraints overlap. Critical paths can change at runtime when estimates are wrong or retries occur.

Optimization should target the limiting term. More workers help when `W/p` dominates and ready parallelism exists. They do not shorten a serial critical vertex. Reducing noncritical work may save cost without improving completion. Shortening or restructuring the critical path can improve latency even if total work changes little.

### Materialization, lineage, and recovery

Materializing an edge writes a named result with completeness and retention semantics. It allows producer and consumer lifetimes to decouple, supports reuse, and limits recomputation after failure. It adds storage, serialization, I/O, cleanup, and commit overhead. Materializing every edge can dominate the computation.

Pipelining reduces latency and storage but couples producer/consumer lifetimes and propagates backpressure. A consumer failure may require replay; a producer failure can invalidate in-flight downstream state. The graph must say which intermediate results are replayable or durably available.

Lineage records derivation. If output `y` came from deterministic transformation `f` over available inputs `x`, the runtime can reconstruct `y`. This avoids replicating every intermediate, but recovery cost can grow along a long lineage. Periodic checkpoints or materialized cut points trade normal-path overhead for bounded recovery.

Recomputation needs exact source versions, code and configuration, partition function, nondeterminism policy, and external dependency snapshots. “Run the same task again” is not meaningful if it reads the current time, mutable table, random generator without a seed, or changing service. Lineage is a recipe only when its ingredients remain identifiable.

When output is lost, invalidate reachable descendants that depended on it unless they consumed a committed equivalent. The actual recovery cone depends on materialization boundaries and partition-level dependencies, not only logical-operator reachability. A wide dependency may require many producer partitions; a narrow dependency may need one lineage chain.

### Attempts, retries, speculation, and commit

A task can have several attempts but one accepted logical outcome. Each attempt records input versions, code, placement, start/end, status, and produced candidate artifacts. A commit protocol determines which attempt wins and prevents losers from overwriting or duplicating output.

Pure deterministic tasks are easiest to retry. Nondeterministic computation may still be retryable if outcomes are recorded or equivalence is defined. External effects require stronger protocols. An attempt that sends an irreversible instruction before failing cannot be made safe by discarding its data output.

Speculation launches another attempt for a suspected straggler. It can reduce tail latency and consumes extra input, compute, network, and sink capacity. Candidate outputs must remain isolated until one commits. Poor straggler detection can duplicate normal work and worsen overload.

Cancellation propagates through the graph only under declared ownership. Cancelling one consumer should not cancel a shared upstream result still needed elsewhere. Cleanup should use reference/lifetime information and tolerate late attempts.

### Graph rewrites and adaptive execution

High-level graphs preserve structure that a flat task dictionary can lose. Dask documents layers so systems and humans can inspect and optimize collections without expanding every task immediately. Logical structure supports filter pushdown, projection pruning, common-subexpression reuse, fusion, and parallelism choice.

A rewrite must preserve observable semantics. Moving a filter before an operation is invalid if the operation has effects, the predicate observes generated values, errors are observable, or ordering matters. Fusing tasks changes retry boundaries, memory, pipelining, metrics, and failure blast radius. Correct values alone may not capture the required behavior.

Adaptive execution changes a physical plan from runtime evidence such as partition sizes, skew, available resources, or completed materialization. Record the graph version, decision inputs, compatibility boundary, and which running outputs remain valid. Unversioned mutation makes incidents and reproduction nearly impossible.

Dynamic task systems can create vertices during execution. The control plane must bound admission, deduplicate creation, retain parentage, handle creator retries, and know when no further tasks can appear. A static snapshot may be useful for one epoch without describing the whole computation.

### Cycles, iteration, and unbounded streams

A batch DAG rejects cycles because predecessor completion cannot bootstrap itself. Iterative algorithms can unroll a bounded number of iterations into a DAG, but large or data-dependent iteration makes that graph huge or unknown. A structured cyclic dataflow can represent loops while attaching logical timestamps or iteration coordinates and a progress protocol.

Naiad's timely dataflow model supports structured cycles and tracks whether more records can arrive at a logical time. This illustrates why “the graph is a DAG” is an engine design choice, not a universal property of distributed data processing.

An unbounded stream does not globally complete under normal operation. Sources, operators, and sinks make progress through offsets, event-time frontiers, watermarks, checkpoints, or epochs. Completion may apply to a bounded snapshot, a window, a checkpoint, or graceful termination. Scheduler idleness is not proof that no future input exists.

Recursive queries and feedback control also need semantics for convergence, duplicates, ordering, and failure. Simply drawing a back edge supplies none of them. State the progress measure and termination or continuing-service condition.

### Observability and graph evidence

Retain both logical and physical graphs with stable IDs and versions. Map operators to tasks, partitions, attempts, workers, inputs, outputs, and materialization. Record state transitions, queue reasons, edge bytes, backpressure, retries, speculation, cancellations, and accepted commits.

Critical-path analysis should use actual event timing and dependency causality, not only plan estimates. Compare estimated and observed work/span, locate skew, and explain changes after adaptive rewrites. Aggregate stage metrics can hide one partition that gates every descendant.

Graph visualization must remain navigable. Thousands of flat vertices require grouping by logical operator, stage, partition range, or failure domain, with drill-down. A pretty diagram without exact IDs and event correlation is not operational evidence.

## Definitions and Notation

Let logical graph be `G_L=(V_L,E_L)` and physical graph version `G_P^q=(V_P^q,E_P^q)`. Expansion map `pi:V_P^q->V_L` associates every physical task with its logical operator. Task identity is distinct from attempt identity `a=(v,n)`.

For a DAG and vertex cost `c(v)>=0`, predecessor set is `pred(v)={u | (u,v) in E}`. Define `ES(v)=0` for sources and otherwise `max EF(u)` over predecessors. Then `EF(v)=ES(v)+c(v)`, total work `W=sum c(v)`, and span `S=max EF(v)`. Ideal runtime on `p` workers obeys `T_p>=max(W/p,S)`.

The ready set for blocking dependencies is `R(t)={v not committed | every required predecessor outcome is committed and valid at t}`. Runnable tasks are the feasible subset after resource, policy, and placement constraints. For pipelined edges, readiness is a predicate over channel establishment, available records, and protocol state rather than predecessor completion alone.

Descendants `desc(v)` are vertices reachable by one or more directed edges. Loss of an unmaterialized outcome can invalidate a subset of `desc(v)` determined by partition dependencies and surviving cut points. Recovery cost is the work and movement needed to reconstruct required committed outcomes, not merely descendant count.

## Mechanisms, Invariants, or Proof Structure

A task-graph design has eight obligations.

**1. Semantic identity.** Define graph version, logical vertices, physical tasks, partitions, attempts, code/configuration, and output identities.

**2. Edge contract.** Classify data, control, barrier, state, resource, and side-effect relationships; declare schema, partitioning, ordering, availability, transport, and lifetime.

**3. Structural validity.** Validate endpoints, arity, compatibility, and acyclicity for DAG regions. Give intended cycles explicit progress and termination semantics.

**4. Readiness and completion.** Define when tasks can start, consume, commit, and complete; distinguish blocking from pipelined inputs and bounded from unbounded work.

**5. Cost and schedule.** Estimate work, span, transfer, materialization, resources, locality, skew, and overhead. Compare estimates with actual critical paths.

**6. Failure semantics.** Specify retry, speculation, attempt isolation, winner commit, cancellation, lineage, cut points, source retention, side-effect reconciliation, and cleanup.

**7. Rewrite and evolution.** Prove semantic preservation for fusion, pruning, exchange changes, adaptive parallelism, and dynamic graph growth; retain graph versions and decision evidence.

**8. Operations and review.** Make every blocked/running/failed outcome explainable and retain graph, trace, metrics, recovery drills, exceptions, and consequence-appropriate approval.

The executable fixture performs a stable topological traversal, earliest-finish computation, critical-path reconstruction, and descendant search over one finite blocking DAG.

<!-- bijux-verify: {"id":"task-graph-invariants","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"topological_order=('read_customers', 'read_orders', 'filter', 'join', 'aggregate', 'audit', 'format', 'publish')\nlevels=(('read_customers', 'read_orders'), ('filter',), ('join',), ('aggregate', 'audit'), ('format',), ('publish',))\ntotal_work=19\ncritical_path=read_orders->filter->join->aggregate->format->publish\ncritical_path_length=15\nmax_level_width=2\njoin_descendants=('aggregate', 'audit', 'format', 'publish')\n","stderr":""}} -->
```python
tasks = {
    "read_orders": (4, ()),
    "read_customers": (2, ()),
    "filter": (1, ("read_orders",)),
    "join": (5, ("filter", "read_customers")),
    "aggregate": (3, ("join",)),
    "audit": (2, ("join",)),
    "format": (1, ("aggregate",)),
    "publish": (1, ("format", "audit")),
}

remaining = {
    name: set(dependencies)
    for name, (_duration, dependencies) in tasks.items()
}
order = []
levels = []
while remaining:
    ready = tuple(sorted(name for name, deps in remaining.items() if not deps))
    if not ready:
        raise ValueError("task graph contains a cycle")
    levels.append(ready)
    order.extend(ready)
    for name in ready:
        del remaining[name]
    for dependencies in remaining.values():
        dependencies.difference_update(ready)

finish = {}
predecessor = {}
for name in order:
    duration, dependencies = tasks[name]
    if dependencies:
        parent = max(dependencies, key=lambda item: (finish[item], item))
        finish[name] = finish[parent] + duration
        predecessor[name] = parent
    else:
        finish[name] = duration
        predecessor[name] = None

end = max(finish, key=lambda item: (finish[item], item))
critical_path = []
while end is not None:
    critical_path.append(end)
    end = predecessor[end]
critical_path.reverse()

descendants = set()
frontier = {"join"}
while frontier:
    parent = frontier.pop()
    children = {
        name
        for name, (_duration, dependencies) in tasks.items()
        if parent in dependencies
    }
    unseen = children - descendants
    descendants.update(unseen)
    frontier.update(unseen)

print(f"topological_order={tuple(order)}")
print(f"levels={tuple(levels)}")
print(f"total_work={sum(duration for duration, _deps in tasks.values())}")
print(f"critical_path={'->'.join(critical_path)}")
print(f"critical_path_length={finish['publish']}")
print(f"max_level_width={max(map(len, levels))}")
print(f"join_descendants={tuple(sorted(descendants))}")
```

The checker proves these results only for the declared finite graph and integer costs. Levels assume blocking dependencies and unbounded workers; they are not physical stages. Descendants overapproximate recomputation because the fixture has no partition-level edges or materialized cut points. It does not model resources, transfer, pipelining, failures, retries, side effects, dynamic vertices, cycles, or unbounded input.

## Alternatives and Trade-Offs

**Imperative orchestration versus explicit dataflow.** Imperative control is flexible and familiar but can hide dependencies. Explicit graphs enable global reasoning and optimization while constraining dynamic behavior or requiring graph expansion.

**Logical layers versus flat tasks.** High-level structure is compact and rewrite-friendly. Low-level tasks expose exact scheduling and recovery. Durable systems retain mappings between both.

**Pipelined versus materialized edges.** Pipelining lowers latency and storage but couples failures and backpressure. Materialization decouples lifetimes and bounds recomputation at I/O and storage cost.

**Fine versus coarse vertices.** Fine tasks expose parallelism and narrow retry but add scheduling, serialization, metadata, and tiny-output overhead. Coarse tasks reduce overhead and enlarge failure/retry units.

**Fusion versus isolation.** Fusion avoids edge overhead and can improve locality. It enlarges code/resource footprints, retry blast radius, and metric aggregation, and can prevent independent scaling.

**Static versus dynamic graphs.** Static graphs are easy to validate and optimize globally. Dynamic creation expresses data-dependent work but complicates deduplication, admission, termination, and reproducibility.

**DAG unrolling versus structured cycles.** Unrolling gives ordinary DAG semantics for bounded iteration but can explode graph size. Structured cycles remain compact and require timestamps, frontiers, or convergence protocols.

**Lineage recomputation versus replicated intermediates.** Lineage saves normal-path storage. Replication or checkpoints shorten recovery. Choose from failure rate, recomputation cone, source lifetime, and deadline.

**Deterministic tasks versus recorded nondeterminism.** Determinism simplifies retry and comparison. Recorded seeds, snapshots, or accepted-result identities can govern necessary nondeterminism at metadata and storage cost.

**Plan-time versus adaptive optimization.** Plan-time decisions are reproducible with incomplete evidence. Adaptive changes use actual sizes and skew but need versioned rewrite safety and operational explanation.

## Failure Modes and Misconceptions

1. **An operator is one task.** Parallel expansion can create thousands of partition tasks and several attempts each.
2. **A task is an attempt.** Retries and speculation create several attempts for one logical outcome.
3. **Every edge means predecessor completion.** Pipelined consumers may start on partial data; barriers may impose stronger rules.
4. **Edges carry only data.** Control, state, resource, barrier, and side-effect constraints also matter.
5. **Acyclic means deterministic.** Tasks can read clocks, randomness, mutable services, or unordered inputs.
6. **Topological order is the schedule.** It captures dependency legality, not resources, placement, fairness, or concurrency timing.
7. **More workers beat the critical path.** Dependency-constrained span remains a lower bound.
8. **Maximum layer width is available parallelism.** Durations, pipelining, resources, and dynamic readiness can differ.
9. **Total work predicts completion.** Skew, span, movement, retries, and overhead matter.
10. **Materialize every edge for safety.** I/O and storage can dominate while unnecessary copies accumulate.
11. **Pipeline every edge for speed.** Failure coupling, memory pressure, and backpressure can become unmanageable.
12. **Lineage guarantees cheap recovery.** Long chains, unavailable sources, and wide dependencies can make recomputation prohibitive.
13. **Same code means same retry result.** Inputs, configuration, time, randomness, and external state may change.
14. **Discarding loser output cancels its effects.** External actions may already be irreversible.
15. **Speculation is free.** Duplicate attempts consume shared resources and can amplify sink load.
16. **Cancelling a consumer cancels its producers.** Shared ancestors may serve other outputs.
17. **Fusion is semantics-neutral.** It changes retry boundaries, resources, ordering, errors, and metrics.
18. **A filter can always move earlier.** Effects, errors, nondeterminism, and generated values can make reordering observable.
19. **Adaptive rewrites need no version.** Without one, outputs and incidents cannot be attributed to a graph.
20. **A creator retry can safely recreate dynamic tasks.** It may duplicate vertices or effects without stable IDs.
21. **Every dataflow is a DAG.** Iteration and streaming can use structured cycles or evolving graphs.
22. **An idle stream has completed.** More records may arrive; progress needs offsets, frontiers, watermarks, or termination.
23. **A drawn graph is operational evidence.** Exact identities, attempts, events, bytes, and commits are required.
24. **Aggregate vertex metrics reveal the tail.** One partition can gate all descendants.
25. **A valid graph proves domain correctness.** It cannot validate clinical, financial, safety, or other domain semantics alone.

## Worked Examples

### Example 1

**Question:** Can two source scans run concurrently?

**Reasoning:** Yes when neither depends on the other and resources permit. A downstream join remains blocked until its required input semantics are satisfied.

**Conclusion:** Graph independence exposes potential, not guaranteed, concurrency.

### Example 2

**Question:** Why is `join[17]` different from attempt `join[17]/a1`?

**Reasoning:** The task names one required partition outcome; attempts are executions competing or retrying to produce it. Only an accepted attempt commits.

**Conclusion:** Stable outcome identity prevents retries from becoming duplicate logical tasks.

### Example 3

**Question:** What does a topological traversal prove?

**Reasoning:** It proves a finite declared graph is acyclic and supplies a legal dependency order. It does not prove type compatibility, determinism, resource feasibility, or output correctness.

**Conclusion:** Structural validity is one graph obligation.

### Example 4

**Question:** A graph has work 100 and span 30 on four workers. What is the ideal lower bound?

**Reasoning:** `max(100/4,30)=30`; the critical path dominates. Actual runtime is at least 30 and includes overhead.

**Conclusion:** Work and span bound different limitations.

### Example 5

**Question:** Should a small map-filter edge be materialized?

**Reasoning:** Usually pipelining or fusion avoids unnecessary I/O, unless reuse, recovery, lifetime decoupling, memory, or audit requirements justify a cut point.

**Conclusion:** Edge materialization is a lifecycle and recovery trade.

### Example 6

**Question:** Can a task that sends an email be retried like a pure filter?

**Reasoning:** Not blindly. Use a durable idempotency key, transactional outbox, deduplicating receiver, or separate committed effect protocol.

**Conclusion:** Data-output isolation does not undo external effects.

### Example 7

**Question:** What happens when an unmaterialized join partition is lost?

**Reasoning:** Its needed descendants become invalid; the runtime follows partition lineage to surviving source/cut-point data and reconstructs the partition before consumers commit.

**Conclusion:** Recovery scope follows exact lineage and materialization, not just operator names.

### Example 8

**Question:** May a planner fuse scan, filter, and projection?

**Reasoning:** Yes when types, order, errors, effects, resources, retry boundaries, and output semantics remain compatible. Fusion is not justified solely by adjacency.

**Conclusion:** Rewrites carry semantic and failure obligations.

### Example 9

**Question:** How can an iterative graph know an epoch is complete?

**Reasoning:** It needs a progress protocol over logical timestamps or equivalent accounting that proves no messages capable of affecting the epoch remain. Empty queues alone are insufficient under in-flight messages.

**Conclusion:** Cyclic progress requires more than DAG readiness.

### Example 10

**Question:** Can a task-graph validator approve a national organ-allocation computation?

**Reasoning:** No. Structural checks cannot validate allocation policy, medical urgency, compatibility, consent, geography, fairness, emergency override, privacy, or clinical consequences. Named transplant clinicians, allocation-policy owners, ethics and equity reviewers, patient-safety and quality officers, privacy/security, distributed-systems and operations engineers, accessibility experts, and independent assurance authorities must review representative and failure exercises. No external review is claimed here.

**Conclusion:** High-consequence graphs require domain and independent assurance beyond runtime invariants.

## Cross-Program Connections

[LSDS-004](004-data-locality.md) supplies placement and transfer costs for vertices and edges. [LSDS-006](../ROADMAP.md) deepens stages, tasks, dependency boundaries, and scheduling. [LSDS-007](../ROADMAP.md) explains how narrow and wide transformations change partition dependencies, while later shuffle and checkpoint modules develop materialization and recovery.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies graph traversal, topological sorting, reachability, and critical-path foundations. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns graph representations and queues. [Operating Systems](../../22-operating-systems/ROADMAP.md) contributes process scheduling, pipes, I/O, and resource isolation.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline intent, contracts, orchestration, and durable outputs. This program owns the cluster execution graph underneath. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns failure, clocks, coordination, delivery, and consistency mechanisms relied upon by retries and progress.

Dryad provides the canonical vertex/channel execution formulation. Spark RDDs demonstrate lineage-based recovery. Dask preserves logical layers above flat tasks. Flink distinguishes job vertices, parallel execution vertices, attempts, and intermediate results. Naiad demonstrates that structured cyclic dataflow can support iteration and streaming when progress is explicitly modeled.

## References

- Michael Isard et al., [*Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks*](https://www.microsoft.com/en-us/research/publication/dryad-distributed-data-parallel-programs-from-sequential-building-blocks/), EuroSys, 2007. Primary vertex/channel graph and dynamic execution design.
- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary task, partition, scheduling, retry, and commit design.
- Matei Zaharia et al., [*Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary lineage and partition-recomputation abstraction.
- Derek G. Murray et al., [*Naiad: A Timely Dataflow System*](https://www.microsoft.com/en-us/research/wp-content/uploads/2013/11/naiad_sosp2013.pdf), SOSP, 2013. Primary structured-cycle, logical-time, and progress-tracking design.
- Apache Flink Project, [*Jobs and Scheduling*](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/), checked 2026-09-03. Official current JobGraph, ExecutionGraph, parallel subtask, and intermediate-result documentation.
- Apache Flink Project, [*ExecutionGraph API*](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/runtime/executiongraph/ExecutionGraph.html), checked 2026-09-03. Official current task and execution-attempt identity documentation.
- Dask Project, [*Task Graphs*](https://docs.dask.org/en/latest/graphs.html), checked 2026-09-03. Official current low-level graph representation and optimization documentation.
- Dask Project, [*High Level Graphs*](https://docs.dask.org/en/stable/high-level-graphs.html), checked 2026-09-03. Official current layered logical-graph design.
- Apache Spark Project, [*RDD Programming Guide*](https://spark.apache.org/docs/latest/rdd-programming-guide.html), checked 2026-09-03. Official current lazy transformation, action, persistence, and shuffle behavior.
- Ray Project, [*Ray Core Key Concepts*](https://docs.ray.io/en/latest/ray-core/key-concepts.html), checked 2026-09-03. Official current dynamic task, actor, object-reference, resource, and placement concepts.

## Exercises

### Exercise 1

For tasks `A=3`, `B=2`, `C=4` after `A`, `D=5` after both `B` and `C`, and `E=1` after `D`, derive a topological order, total work, critical path, span, and ideal lower bound on three workers.

### Exercise 2

Distinguish logical operator, physical task, and attempt for a join with 200 output partitions where partition 17 is speculated once. State commit invariants.

### Exercise 3

Compare pipelining and materializing an edge that carries 2 TB, is consumed twice, and takes 40 minutes to recompute. Include normal execution, memory/backpressure, recovery, and cleanup.

### Exercise 4

A dynamic task creates ten children, crashes after submitting six, and is retried. Design identity and admission semantics that prevent duplicate logical children and permit completion detection.

### Exercise 5

A hospital builds a graph for medication-dose recommendations and clinician delivery. Specify graph, retry, effect, provenance, failure-test, and named human-review evidence required before operation.

## Answers to the Exercises

### Answer 1

One topological order is `A,B,C,D,E`; `B,A,C,D,E` is also legal. Work is `3+2+4+5+1=15`. The longest chain is `A->C->D->E` with length `3+4+5+1=13`; `B->D->E` is 8. On three ideal workers the lower bound is `max(15/3,13)=13`, so span dominates. Actual communication, resources, and overhead can only increase runtime.

### Answer 2

The logical join is one semantic operator. Physical expansion creates tasks `join[0]` through `join[199]`, each with declared input partitions and output identity. Task `join[17]` has original attempt `a0` and speculative attempt `a1`. Both may compute candidates, but exactly one compatible complete output may commit for the task epoch; losers cannot overwrite, append duplicate sink effects, or delete the winner. Attempt records retain exact input/code versions and cancellation/cleanup remains safe under late completion.

### Answer 3

Pipelining avoids writing and rereading 2 TB and can overlap producer/consumer, but two consumers need multicast/replay or independent flows, slow consumers cause backpressure, and producer or consumer loss can force up to 40 minutes of recomputation. Materialization pays serialization, 2-TB storage writes, later reads, commit metadata, and cleanup, but decouples lifetimes, supports both consumers, and bounds recovery if the artifact is durable. Choose using measured network/storage bandwidth, concurrent memory, consumer timing, failure probability, source retention, reuse, deadline, and storage lifecycle. A hybrid can materialize partitioned cut points while pipeline-compatible chains remain fused.

### Answer 4

Derive child IDs deterministically from `(parent_logical_id,parent_epoch,child_index)` for all ten children before submission. Admission is idempotent: repeated create with the same identity and specification returns the existing child; a conflicting specification fails. Persist the intended child set or a sealed count transactionally with creation progress. The retry reconciles all ten IDs and submits missing children rather than inventing new ones. Completion requires the parent to be sealed and every declared child to reach an accepted terminal outcome; scheduler idleness is insufficient. Attempt identities remain separate, and child effects use their logical idempotency keys.

### Answer 5

Record exact patient/encounter, medication, lab, model/rule, formulary, units, and reference versions; logical/physical graph versions; task/attempt lineage; validation gates; and the committed recommendation identity. Pure calculations may retry against immutable snapshots, while clinician notification or order mutation needs idempotency, transaction/outbox, acknowledgment, and reconciliation. Test missing/stale inputs, unit mismatch, duplicate and reordered attempts, worker/region loss, partial effects, model-service failure, cancellation, rollback, audit replay, and downtime workflow. Named reviewers include pharmacists and prescribing clinicians, medication-safety and clinical-informatics owners, nursing/workflow representatives, patient-safety and quality, privacy/governance, cybersecurity, distributed-systems/operations and disaster recovery, accessibility, ethics/equity where recommendations affect access, and the applicable independent clinical-safety authority. Local validators and this answer do not provide external approval.
