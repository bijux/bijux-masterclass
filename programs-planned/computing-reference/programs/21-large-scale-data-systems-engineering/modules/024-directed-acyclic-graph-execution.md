---
module_id: LSDS-024
program: Large-Scale Data Systems Engineering
level: 1
module_number: 24
title: Directed Acyclic Graph Execution
status: complete
last_verified: 2026-09-03
---

# Directed Acyclic Graph Execution

## One-Page Review

### Governing question

How should a large-scale data system turn a declarative or programmatic pipeline into an executable directed acyclic graph whose dependencies, stages, retries, materialization, resource use, and externally visible effects remain correct under parallel and partial execution?

### Essential definitions

- A **directed acyclic graph**, or DAG, is a finite set of vertices and directed edges with no directed cycle.
- A **logical graph** describes transformations and data dependencies; a **physical graph** adds concrete exchanges, partitions, tasks, resources, and runtime operators.
- A **topological order** lists every vertex after all of its predecessors.
- A **source** has no incoming dependency; a **sink** has no outgoing consumer in the selected computation.
- A **narrow edge** lets one downstream partition depend on a bounded number of upstream partitions; an **exchange edge** redistributes data and usually creates a stage boundary.
- A **stage** is a set of taskable operators that can execute without crossing an unresolved materializing exchange boundary.
- **operator fusion** or **pipelining** executes compatible adjacent operators together without materializing their entire intermediate dataset.
- **lineage** records how a partition or result can be reconstructed from immutable inputs and transformations.
- The **critical path** is a dependency path with maximum modeled duration; it lower-bounds completion time even with unlimited parallel resources.

### Central model, mechanism, or theorem

Let `G=(V,E)` be a finite DAG. An edge `(u,v)` means `v` cannot produce its required result until the relevant output of `u` is available. A topological order exists exactly when the directed graph is acyclic. A ready scheduler may run a vertex when all required predecessors have satisfied their edge contracts, but graph readiness is not resource feasibility, data availability, or authorization.

For vertex duration `d(v)`, unlimited-resource earliest finish is `EF(v)=d(v)+max(EF(u))` over predecessors, with an empty maximum of zero. The graph critical-path length is `max(EF(v))`. Real elapsed time is at least both the critical path and a resource-work bound such as total CPU work divided by usable CPU capacity. Exchange edges, materialization, queueing, skew, retries, and side effects add constraints absent from the abstract DAG.

### Critical invariants

- Every consumed artifact identifies the exact producing attempt, schema, partitioning, and integrity state intended by the edge.
- A task becomes ready only after every required predecessor contract is satisfied; speculative or failed output is not silently mixed.
- The physical graph preserves logical semantics across fusion, reordering, exchange insertion, and stage construction.
- Cycles are rejected or represented through an explicit iterative/streaming abstraction rather than hidden in a DAG.
- Retryable vertices read immutable/versioned inputs and isolate attempt output until commit.
- Side-effecting sinks use idempotency, transactions, or an atomic commit protocol; lineage alone cannot undo an external effect.
- Materialization and caching decisions have explicit lifetime, ownership, consistency, capacity, and eviction semantics.
- Scheduling evidence includes critical path, total work, parallelism width, skew, data movement, memory, queueing, and recovery.
- Graph and plan versions are preserved so an observed run can be explained and replayed.

### Common failures

Frequent failures are confusing dataflow direction with control-flow order, treating an API call sequence as the executed graph, accepting a hidden cycle, topologically sorting only a selected fragment while omitting dependencies, fusing across a required exchange or failure boundary, assuming all ready tasks can fit, counting vertices instead of partition tasks, optimizing total work while lengthening the critical path, materializing every edge, caching without capacity or snapshot semantics, recomputing a nondeterministic ancestor, publishing speculative output, and retrying a non-idempotent sink.

### Compact example

Two source branches read and parse data before a wide join. A second exchange feeds an aggregate, and a narrow publish step follows. Deterministic topological traversal yields seven vertices. Stage assignment places the four source/parse vertices in stage 0, the join in stage 1, and aggregate plus publish in stage 2. With modeled durations, the critical path follows the slower parse branch through join, aggregate, and publish for 18 units. The example proves graph arithmetic only; it does not predict production duration without partition, resource, movement, and failure evidence.

### Connections

[LSDS-005](005-distributed-task-graphs.md) introduces task graphs, [LSDS-006](006-stages-tasks-and-dependencies.md) introduces stages, and [LSDS-007](007-narrow-and-wide-transformations.md) distinguishes dependency width. [LSDS-021](021-mapreduce-execution-model.md) provides a two-stage special case. [LSDS-025](../ROADMAP.md) continues with lazy plan construction, and [LSDS-026](../ROADMAP.md) deepens stage scheduling.

## Governing Question

Real pipelines rarely fit a single map and reduce boundary. A source may feed validation, enrichment, audit, and aggregate branches. A join may require two independently prepared inputs. A reused intermediate may serve several sinks. Directed acyclic graphs express these dependencies without forcing unrelated work into a linear script.

The graph is not merely a picture. It is the runtime's contract for readiness, parallelism, data movement, recovery, and commit. Missing an edge allows a consumer to run before required data is valid. Adding a false edge serializes independent work. Misclassifying an exchange changes stage boundaries and resource needs. A correct logical graph can still become an unsafe physical plan when retries duplicate effects or materialization exceeds capacity.

The governing question is therefore how to preserve the intended computation while translating between user program, logical operators, physical exchanges, partition tasks, and attempts. The answer must distinguish structural facts proved from the graph from empirical claims that depend on data, cluster resources, and runtime behavior.

## Why This Matters

A DAG exposes parallel branches that a sequential script hides. Independent inputs can be read concurrently; narrow transformations can be fused; shared ancestors can be computed once and retained; and only exchange boundaries need global coordination. The graph also gives a precise basis for progress, critical-path analysis, failure propagation, and selective recomputation.

The same flexibility creates large blast radii. One high-fan-out intermediate may retain terabytes because several consumers finish at different times. One skewed exchange partition can hold an entire downstream stage. A seemingly harmless sink can send duplicate notifications during retry. A graph with millions of fine-grained tasks can cost more to construct, serialize, schedule, and observe than to execute.

DAG execution also determines what operators and users can explain. When the submitted graph, optimized plan, runtime graph, and attempt history are versioned, an engineer can answer why a task ran, what it consumed, and whether an output is valid. Without those records, a green job status can conceal partial publication, stale cached state, or a different optimized plan than the one reviewed.

Graph reasoning applies across batch engines, workflow orchestrators, query systems, build systems, machine-learning pipelines, and bounded portions of stream processing. Their edge semantics differ, but all must decide dependency, readiness, resource admission, retry, and publication.

## Prerequisites and Retrieval

Recall partitioning from [LSDS-003](003-range-hash-and-consistent-partitioning.md), data locality from [LSDS-004](004-data-locality.md), distributed task graphs from [LSDS-005](005-distributed-task-graphs.md), stages/tasks/dependencies from [LSDS-006](006-stages-tasks-and-dependencies.md), narrow and wide transformations from [LSDS-007](007-narrow-and-wide-transformations.md), serialization from [LSDS-008](008-serialization-across-workers.md), and work/movement/state accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve distributed storage, immutable object publication, multipart commit, and metadata consistency from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md). Retrieve MapReduce attempts and commit from [LSDS-021](021-mapreduce-execution-model.md), processing placement from [LSDS-022](022-map-side-and-reduce-side-processing.md), and partitioner/combiner contracts from [LSDS-023](023-partitioners-and-combiners.md).

You should be able to read directed graphs; distinguish vertices, edges, paths, cycles, indegree, and outdegree; reason about partitions and attempts; compute maxima and sums; and separate semantic correctness from performance evidence.

## Learning Objectives

After this module, you should be able to:

1. distinguish user-program order, logical dataflow, optimized physical graph, stages, tasks, and attempts;
2. verify acyclicity and compute a deterministic topological order;
3. define edge contracts for pipelined, materialized, broadcast, and partitioned dependencies;
4. construct stages without fusing across required exchanges or semantic barriers;
5. compute critical-path and work lower bounds while stating their assumptions;
6. reason about fan-in, fan-out, shared intermediates, recomputation, caching, and lifetime;
7. design retry and publication semantics for pure transformations and side-effecting sinks;
8. test graph rewrites for semantic equivalence and operational feasibility;
9. diagnose skew, stragglers, graph-size overhead, blocked readiness, and recovery amplification; and
10. record sufficient graph, data, code, resource, security, and governance evidence for replay and review.

## Core Exposition

A DAG consists of vertices `V` and directed edges `E`. Depending on the abstraction, a vertex may represent a logical transform, a physical operator, a partition task, or a workflow activity. Never mix these levels in one count. A logical join vertex may expand into two exchanges, hundreds of map tasks, hundreds of reduce tasks, and multiple attempts.

An edge must say more than "before." In dataflow, it normally identifies data produced by one vertex and consumed by another. The edge can carry partitioning, ordering, schema, cardinality expectation, boundedness, transport, materialization, and availability semantics. In a workflow graph, an edge may instead express only a control precondition. Treating control success as proof that the correct data exists is unsafe unless the artifact contract is explicit.

### Logical, physical, and runtime graphs

The user constructs operations in some host-language order. An engine captures a logical graph of sources, transformations, and sinks. An optimizer may eliminate dead branches, push filters, combine operators, reuse common subexpressions, change join strategy, and insert exchanges. A planner then expands physical operators by partition count into tasks. During execution, each task can have multiple attempts and state transitions.

These graphs answer different questions. The logical graph supports semantic review. The physical graph explains data movement and stage boundaries. The runtime graph explains placement, queueing, failure, speculation, and committed attempt choice. Record mappings between them; otherwise an operator cannot trace a failed runtime task back to the reviewed transformation.

### Acyclicity and topological order

A topological order respects every edge: `u` appears before `v` whenever `(u,v)` is an edge. Kahn's algorithm initializes a ready set with all zero-indegree vertices, repeatedly removes one, and decrements its children's indegrees. If fewer than `|V|` vertices are emitted, a directed cycle exists.

Multiple topological orders can be valid. Deterministic tie-breaking is useful for plan digests, tests, diffs, and explanations, but it does not impose a required runtime serial order between independent vertices. A scheduler is free to run any ready vertices concurrently subject to resource and policy constraints.

A repeated computation can still be represented by a DAG after bounded unrolling: iteration 1 feeds iteration 2 as distinct vertices. Unbounded feedback, event-time loops, and continuously updating state require a cyclic, streaming, or fixed-point model outside a finite DAG. Hiding feedback through an external mutable table does not make it safe.

### Edge contracts and availability

For a pipelined narrow edge, a downstream task may consume records incrementally from its corresponding upstream task. For a blocking exchange, downstream partitions usually wait until upstream map outputs needed for the exchange are committed or discoverable under the engine's protocol. A broadcast edge may require one bounded artifact to be available on every consumer worker. A materialized edge publishes an immutable dataset with a manifest.

Readiness must match the edge. "Producer process exited successfully" is weaker than "the expected partition set, schema, digest, and commit record are valid." If partial consumption is allowed, failure semantics must say whether consumers roll back, restart, or tolerate duplicate/retracted records.

### Stage construction and operator fusion

Adjacent narrow, compatible operators can often run in one task pipeline: read, parse, filter, project, and map. Fusion avoids intermediate serialization, storage, and scheduling. An exchange, required checkpoint, resource incompatibility, loss of pipelining, side-effect boundary, or engine-specific barrier separates stages.

A useful abstract rule assigns a vertex to the maximum predecessor stage, adding one across an exchange edge. This captures the compact example, but production stage construction also accounts for multi-consumer reuse, broadcast production, barriers, and operator capabilities. A stage is not automatically a transaction or a failure domain.

Over-fusion can be harmful. A CPU-heavy transform fused before a selective filter may delay the filter if reordering is unsafe. Fusing operators with incompatible memory or accelerator needs reduces placement choices. Long fused pipelines enlarge retry work and obscure per-operator metrics. Materialization can be intentional when it reduces recovery cost, decouples consumers, or creates a governed checkpoint.

### Tasks, attempts, and state machines

A physical stage expands into tasks, usually one per input or output partition. A task is a logical unit of work; an attempt is one execution of that task. State transitions may include pending, admitted, running, successful-uncommitted, committed, failed, canceled, or lost. Exact names vary, but success and commitment must not be conflated.

The scheduler tracks which predecessor partitions each task needs, which attempts produced them, where bytes reside, and whether the outputs remain valid. If an executor disappears, lineage may recreate lost partitions. If the ancestor read mutable input or used nondeterministic code, recomputation may not reproduce the same data, so input/version determinism is part of fault tolerance.

### Work, span, and usable parallelism

Let `d(v)` be modeled duration and `w(v)` be resource work. The critical path or span is the maximum sum of durations along any dependency path. Total work is the sum across all task executions, including failed and speculative attempts when measuring an observed run. With `P` identical fully usable processors, elapsed time cannot beat approximately `max(span,work/P)` even before movement and overhead.

That bound is deliberately simple. Real vertices demand multiple resources, tasks have unequal durations, parallelism is partition-limited, workers are heterogeneous, locality restricts placement, and exchanges wait for data. Queueing, cold starts, control-plane rate limits, garbage collection, spill, and stragglers all add time.

Critical-path optimization differs from work optimization. Removing ten seconds from a parallel branch that already finishes early does not shorten the job. Adding a cache may add work on the first run yet shorten repeated critical paths. Report both structural model and observed traces.

### Fan-in, fan-out, and shared intermediates

Fan-in vertices such as joins and unions synchronize multiple branches. One slow branch can block downstream readiness even if others finished long ago. Fan-out lets multiple consumers share an ancestor, but creates lifetime questions: retain the intermediate until all consumers finish, recompute it, or persist a governed artifact.

Reference counts alone may be insufficient because failed consumers retry, new sinks may be submitted later, or the scheduler can lose cached blocks. Durable artifacts need retention and deletion rules; ephemeral caches need eviction and recomputation plans. A high-fan-out dataset can multiply network reads and access exposure even when computed once.

### Materialization, caching, and checkpointing

Materialization writes an intermediate representation; caching retains it in a faster tier; checkpointing establishes a recovery boundary with defined durability. These terms are not synonyms. A cache may vanish. A materialized file may lack an atomic manifest. A checkpoint may capture runtime state that is not a reusable business dataset.

Choose boundaries using recomputation cost, fan-out, failure probability, storage and serialization cost, lineage length, deterministic replay, data sensitivity, and operational isolation. "Cache everything" exhausts memory and makes eviction unpredictable. "Recompute everything" can amplify a late failure through an expensive ancestor chain.

### Retry, speculation, and side effects

Pure deterministic tasks over immutable inputs are easiest to retry: discard the failed attempt and accept one successful attempt's output. Speculation starts another attempt for the same task to reduce straggler tails. Both attempts may run concurrently, so their output paths and metrics must remain isolated until one wins commit.

External effects need stronger design. Sending mail, charging an account, mutating a database, publishing a model alias, or acknowledging a message cannot be made safe merely by storing lineage. Use a transactional sink, an idempotency key based on stable job/task/output identity, a write-ahead outbox, or a separately reconciled publish step. Decide whether duplicate requests, partial batches, and ambiguous timeouts are detectable.

### Graph rewriting and equivalence

Optimization rewrites one graph into another. A rewrite is correct when the observable outputs and required effects remain equivalent under the declared data model. Filter pushdown must respect null and outer-join semantics. Common-subexpression reuse requires identical code, inputs, configuration, nondeterminism, and authorization context. Fusion must preserve exceptions, ordering, and resource behavior promised by the interface.

Test rewrites against a reference evaluator on empty, singleton, duplicate, null, skewed, malformed, and adversarial data. Compare multisets unless ordering is part of the contract. For approximate operators, compare error distributions under a pinned seed and confidence method rather than demanding bit equality.

### Observability and replay

Persist a canonical logical-plan digest, optimizer and runtime versions, physical-plan digest, stage/task mapping, code and dependency artifacts, configuration, input and side-input snapshots, schema/key versions, resource requests, placement constraints, security context, attempts, produced artifact digests, and chosen commits.

Metrics should distinguish queued from running time; computation from serialization, spill, and transfer; successful from failed/speculative work; and logical progress from materialized bytes. Graph visualizations are useful only when their vertex level and edge meaning are labeled.

Replay is not "rerun the command." It requires that referenced inputs and code still exist, nondeterminism is controlled, external services are versioned or captured, credentials authorize the intended scope, and sinks publish to an isolated destination until comparison succeeds.

### Security, governance, and human impact

The graph determines where data flows. Every edge and cache can cross a trust, tenant, region, residency, retention, or purpose boundary. Authorization at submission time does not automatically authorize every worker, spill device, log, cache, or downstream reuse. Plan validation should reject illegal placement before execution and runtime admission should enforce it again.

Lineage is sensitive: keys, paths, schema, counts, and error samples can reveal protected information. Apply least privilege, encryption, scoped logs, retention, deletion propagation, and auditable access. When a pipeline affects people, graph review must include sampling exclusions, dropped-error branches, subgroup skew, timeliness, accessibility, appeal/correction mechanisms, and named domain and affected-party oversight where appropriate.

## Definitions and Notation

- `G=(V,E)`: directed graph with finite vertices `V` and edges `E`.
- `pred(v)`: direct predecessors of vertex `v`; `succ(v)` are direct successors.
- `indegree(v)`: number of incoming edges; `outdegree(v)` is the number of outgoing edges.
- **path**: a sequence connected by directed edges; its modeled length is the sum of vertex or edge weights declared by the model.
- **cycle**: a nonempty directed path returning to its starting vertex.
- **topological order**: a permutation of `V` that places each predecessor before its successor.
- **ready set**: vertices whose required dependency contracts are satisfied, not merely vertices with zero static indegree.
- `d(v)`: modeled vertex duration for critical-path analysis.
- `EF(v)`: earliest finish under unlimited resources and the declared duration model.
- `W`: total modeled work; `S`: span or critical-path length; `P`: modeled usable parallel capacity.
- **logical vertex**: semantic transformation; **physical operator**: chosen implementation; **task**: partition-level work; **attempt**: one execution of a task.
- **exchange**: repartitioning or redistribution edge that normally materializes or blocks and creates a stage boundary.
- **artifact contract**: identity, schema, partitions, ordering, snapshot, integrity, security, and availability promised across an edge.
- **commit winner**: the attempt whose isolated output becomes the authoritative task or sink result.

## Mechanisms, Invariants, or Proof Structure

Use this audit for a DAG execution design:

1. Name the selected outputs. Prune only vertices proven irrelevant to those sinks.
2. Define each vertex's logical function, input/output schema, determinism, resources, and effects.
3. Define every edge's data or control meaning, partitioning, ordering, materialization, and availability condition.
4. Verify all referenced vertices exist, reject self-edges, and run cycle detection over the complete selected dependency closure.
5. Produce a deterministic topological order for explanation and digests while preserving runtime concurrency.
6. Translate logical to physical operators and prove each rewrite preserves the declared observable semantics.
7. Insert exchanges and explicit barriers, then construct stages without crossing their contracts.
8. Expand stages into partition tasks and distinguish tasks from attempts and committed outputs.
9. Compute work, width, critical path, data movement, state lifetime, and resource lower bounds with stated assumptions.
10. Choose materialization, cache, and checkpoint boundaries from recovery, reuse, capacity, and governance evidence.
11. Define retry, speculation, cancellation, and commit for pure outputs and external effects.
12. Pin graph/code/config/input/security identities; test adversarial data, failures, plan drift, and replay before production publication.

The structural proof has three parts. First, all dependencies form an acyclic closure, so at least one topological order exists. Second, each scheduled vertex runs only after its edge-specific prerequisites are satisfied. Third, physical rewrites and retries preserve observable semantics. Acyclicity alone proves none of the latter two.

The performance argument also has three parts. The graph supplies parallel branches and a critical path. Partition/data evidence supplies task sizes, skew, and movement. Resource/runtime evidence supplies capacity, queueing, overhead, failures, and placement. Predictive claims require all three and should include uncertainty.

<!-- bijux-verify: {"id":"dag-stage-and-critical-path","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"order=('read_a', 'parse_a', 'read_b', 'parse_b', 'join', 'aggregate', 'publish')\nstage_0=('read_a', 'parse_a', 'read_b', 'parse_b')\nstage_1=('join',)\nstage_2=('aggregate', 'publish')\ncritical_path=('read_b', 'parse_b', 'join', 'aggregate', 'publish') duration=18\ncycle_rejected=True\n","stderr":""}} -->
```python
from heapq import heappop, heappush


def topological_order(parents):
    indegree = {node: len(required) for node, required in parents.items()}
    children = {node: [] for node in parents}
    for node, required in parents.items():
        for parent in required:
            children[parent].append(node)
    ready = []
    for node, degree in indegree.items():
        if degree == 0:
            heappush(ready, node)
    order = []
    while ready:
        node = heappop(ready)
        order.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                heappush(ready, child)
    if len(order) != len(parents):
        raise ValueError("cycle")
    return tuple(order)


parents = {
    "read_a": (),
    "parse_a": ("read_a",),
    "read_b": (),
    "parse_b": ("read_b",),
    "join": ("parse_a", "parse_b"),
    "aggregate": ("join",),
    "publish": ("aggregate",),
}
edge_kind = {
    ("read_a", "parse_a"): "narrow",
    ("read_b", "parse_b"): "narrow",
    ("parse_a", "join"): "exchange",
    ("parse_b", "join"): "exchange",
    ("join", "aggregate"): "exchange",
    ("aggregate", "publish"): "narrow",
}
duration = {
    "read_a": 3,
    "parse_a": 2,
    "read_b": 2,
    "parse_b": 4,
    "join": 7,
    "aggregate": 4,
    "publish": 1,
}

order = topological_order(parents)
stage = {}
finish = {}
critical_parent = {}
for node in order:
    if parents[node]:
        stage[node] = max(
            stage[parent] + (edge_kind[(parent, node)] == "exchange")
            for parent in parents[node]
        )
        critical_parent[node] = max(parents[node], key=lambda parent: finish[parent])
        finish[node] = duration[node] + finish[critical_parent[node]]
    else:
        stage[node] = 0
        finish[node] = duration[node]

sink = max(order, key=lambda node: finish[node])
path = []
while True:
    path.append(sink)
    if sink not in critical_parent:
        break
    sink = critical_parent[sink]
path.reverse()

print(f"order={order}")
for number in range(max(stage.values()) + 1):
    print(f"stage_{number}={tuple(node for node in order if stage[node] == number)}")
print(f"critical_path={tuple(path)} duration={max(finish.values())}")
try:
    topological_order({"x": ("y",), "y": ("x",)})
    rejected = False
except ValueError:
    rejected = True
print(f"cycle_rejected={rejected}")
```

The program is a deterministic structural model. Boolean addition in stage assignment contributes one across an exchange and zero across a narrow edge. It does not model task partitions, concurrent resource demands, transfer duration, spill, queueing, or retries.

## Alternatives and Trade-Offs

**Single MapReduce job versus general DAG.** A two-stage map/shuffle/reduce form is simple and creates a clear materialization boundary. A general DAG avoids writing every logical step to external storage and can share branches, but needs a richer scheduler, recovery model, and plan explanation.

**Eager execution versus graph construction.** Eager operations expose failures near the call site and simplify local reasoning. Deferred graph construction enables global optimization and avoids unused work, but captures code, inputs, and configuration whose late evaluation can surprise users. LSDS-025 treats this boundary directly.

**Fine-grained tasks versus coarse stages.** Fine tasks expose parallelism and reduce individual retry cost but enlarge graph construction, scheduling, serialization, and observability overhead. Coarse tasks reduce control-plane cost but constrain placement, amplify stragglers, and increase retry work.

**Fusion versus materialization.** Fusion reduces intermediate I/O and latency. Materialization shortens lineage, decouples consumers, supports inspection, and can bound recovery. Its cost includes storage, serialization, integrity checks, cleanup, and potential exposure of sensitive data.

**Recompute versus cache.** Recompute saves retained capacity and can exploit newer placement. Cache benefits reuse and long/expensive ancestors. The decision depends on deterministic replay, reuse probability, loss probability, size, serialization, fan-out, and governance—not on a universal rule.

**Static versus adaptive physical graph.** Static plans are easier to digest, approve, compare, and replay. Adaptive plans can respond to observed cardinality and skew, but must record decisions, restrict legal rewrites, preserve semantics, and explain why runtime structure differs from the submitted plan.

**Fail-fast versus partial continuation.** Canceling all descendants after an upstream failure keeps status simple. Independent branches may safely continue and preserve useful work, but partial success needs explicit sink independence, cost limits, publication rules, and user-visible status.

**Lineage recovery versus checkpoint recovery.** Lineage can rebuild missing partitions without eagerly writing every intermediate. Checkpoints bound recovery time and support stateful systems, but consume storage and require consistent cut, version, and retention semantics.

## Failure Modes and Misconceptions

**"A DAG is the order the source code runs."** Host-language calls may construct a graph lazily; optimizers and parallel schedulers choose a different safe order.

**"Any topological order has the same performance."** Orders preserve dependency correctness but interact differently with memory lifetime, locality, fairness, fan-out, and resource availability.

**"Zero indegree means runnable."** It means no static predecessors. Admission can still require input availability, capacity, placement, credentials, rate-limit quota, and policy approval.

**"An acyclic logical plan cannot deadlock."** Runtime resource acquisition, bounded buffers, external locks, and barrier protocols can deadlock even when the logical dependency graph is acyclic.

**"One vertex is one task."** Logical vertices expand by partitions and sometimes by multiple physical operators; failed and speculative attempts further multiply executions.

**"A stage is every row in the graph visualization."** Stage boundaries derive from exchange and barrier semantics, not display layers or topological depth alone.

**"Fusion is always faster."** It can increase critical-path work, resource coupling, retry amplification, code generation size, and diagnostic opacity.

**"Caching makes recomputation impossible."** Caches can evict or disappear. Correctness must tolerate loss unless the artifact is durably committed under an explicit contract.

**"Lineage gives exactly-once effects."** Lineage reconstructs data computation; it does not retract an email, payment, database mutation, or already visible file.

**"The critical path predicts wall time."** It is a lower bound under a declared duration model. Capacity, movement, skew, queueing, control overhead, and failures matter.

**"A succeeded task produced valid input for descendants."** Only the engine's integrity and commit protocol determines which attempt output is authoritative and complete.

**"Adaptive rewrites need no review because results are equivalent."** Equivalence must be proven within guarded conditions, and placement, security, cost, and explainability can change even when values do not.

## Worked Examples

### Example 1

A pipeline reads `orders` and `customers`, validates each independently, exchanges both by customer ID, joins, aggregates by region, and writes a report. The logical graph has two branches and a fan-in. The physical graph contains at least the join exchange and likely another exchange for region aggregation. Calling the report "one job" does not make it one stage. Review edge schemas, key encodings, snapshots, join multiplicity, reducer partitions, and commit separately.

### Example 2

Kahn's algorithm starts with ready vertices `{A,B}`. Removing `A` enables `C`; removing `B` and then `C` enables `D`. Both `(A,B,C,D)` and `(B,A,C,D)` may be valid depending on edges. A lexical heap gives deterministic plan output, while the runtime may execute `A` and `B` simultaneously. Determinism of the explanation is not forced serialization.

### Example 3

Suppose `A -> B -> C -> A` is introduced through a mistaken dependency declaration. No vertex in that component reaches zero indegree, so Kahn's algorithm emits fewer than all vertices and rejects the graph. Reporting the remaining component helps diagnosis. Automatically deleting one edge would invent semantics and is not a safe repair.

### Example 4

Read, parse, filter, and project each have narrow partition-aligned dependencies and compatible resources. Fusing them avoids three intermediate writes. The following join requires redistribution by key, so it starts a new stage. If validation errors must be durably quarantined before customer-visible computation, the error sink/commit may impose an additional boundary even without shuffle.

### Example 5

Three paths to a sink have modeled durations 8, 15, and 11 seconds. Unlimited-resource critical path is at least 15 seconds. Optimizing the 8-second path to 2 seconds leaves the lower bound unchanged; reducing the 15-second path to 10 makes the 11-second path critical. Observed duration still needs task-level distributions and queue/transfer evidence.

### Example 6

An expensive normalized dataset feeds fraud, billing, and analytics branches. Retaining it avoids three computations but holds 2 TiB until the slowest branch finishes and grants three consumer domains access. Compare recomputation work with storage duration, concurrent reads, eviction probability, lineage determinism, access scope, and deletion. A durable reusable dataset needs an owner and manifest, not merely a cache flag.

### Example 7

A task attempt writes partition 17 to an attempt-specific location. A speculative attempt writes a different isolated candidate. The commit coordinator validates expected metadata and selects one winner; the manifest references only that object. Writing both to the final name or allowing last-writer-wins creates ambiguous content and corrupts lineage.

### Example 8

A publish vertex calls a payment API after computing invoices. A timeout leaves the caller unsure whether the payment was accepted. Retrying without a stable invoice/payment idempotency key can double charge. A safe graph separates immutable invoice computation from a reconciled transactional publisher whose request identity and response are auditable.

### Example 9

A million-vertex graph contains one task per tiny block. Each task computes for 10 milliseconds, but graph serialization, scheduler decisions, heartbeats, and metric records dominate. Coarsening partitions reduces control work, though too much coarsening harms parallelism and retry granularity. Measure graph construction, submission, queue, dispatch, useful CPU, and task duration distributions.

### Example 10

A regulated pipeline branches raw records into model training and a quality dashboard. The optimizer proposes sharing a decoded cache across both. Equivalence of decoded values is insufficient: the dashboard service may lack purpose or residency authorization for fields needed only by training. Project and authorize branch-specific data before crossing the boundary, and record reviewers, policy version, deletion, accessibility, and correction routes.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies graph traversal, topological sorting, critical paths, and complexity analysis.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies adjacency representations, heaps, queues, and memory trade-offs for large graphs.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects DAG rewriting to relational plans, exchanges, joins, materialization, and transaction boundaries.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies graph execution to pipelines, lineage, orchestration, data quality, and publication.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies failure models, retries, consensus/commit boundaries, and partial progress.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies readiness, work/span analysis, races, barriers, and scheduling.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects task admission to processes, memory, I/O, isolation, and resource scheduling.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies flow, congestion, locality, and topology costs across data edges.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects graph runs to cluster APIs, tenancy, observability, policy, and incident operations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies least privilege, trust boundaries, artifact integrity, secrets, audit, and data-flow controls.

## References

1. Apache Spark. [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Accessed 2026-09-03.
2. Apache Spark. [Cluster Mode Overview](https://spark.apache.org/docs/latest/cluster-overview.html). Accessed 2026-09-03.
3. Apache Spark. [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html). Accessed 2026-09-03.
4. Apache Beam. [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Accessed 2026-09-03.
5. Apache Beam. [Beam Programming Guide: Runner](https://beam.apache.org/documentation/runtime/model/). Accessed 2026-09-03.
6. Apache Beam. [Runner Capability Matrix](https://beam.apache.org/documentation/runners/capability-matrix/). Accessed 2026-09-03.
7. Apache Flink. [ExecutionPlan API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/streaming/api/graph/ExecutionPlan.html). Accessed 2026-09-03.
8. Apache Flink. [JobGraph API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/runtime/jobgraph/JobGraph.html). Accessed 2026-09-03.
9. Dask. [Task Graphs](https://docs.dask.org/en/stable/graphs.html). Accessed 2026-09-03.
10. Dask. [High Level Graphs](https://docs.dask.org/en/stable/high-level-graphs.html). Accessed 2026-09-03.
11. Michael Isard et al. [Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks](https://www.microsoft.com/en-us/research/publication/dryad-distributed-data-parallel-programs-from-sequential-building-blocks/). EuroSys 2007. Accessed 2026-09-03.
12. Jeffrey Dean and Sanjay Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters](https://research.google.com/archive/mapreduce-osdi04.pdf). OSDI 2004. Accessed 2026-09-03.

## Exercises

### Exercise 1

Run the compact DAG by hand. Derive the deterministic topological order, stage assignment, earliest finishes, critical path, and the assumptions under which 18 units is a lower bound.

### Exercise 2

Prove why successful completion of Kahn's algorithm establishes acyclicity for a finite graph, and explain what it does not prove about runtime safety.

### Exercise 3

Design the physical DAG for two fact sources joined to one dimension, followed by per-region aggregation and two sinks. State exchanges, stage boundaries, reuse/materialization, task identities, and skew controls.

### Exercise 4

Specify retry, speculation, cancellation, and commit semantics for a graph whose terminal vertices write object storage, update a database, and send notifications.

### Exercise 5

Specify evidence and named review for an adaptive DAG optimizer processing health or benefits data across jurisdictions.

## Answers to the Exercises

### Answer 1

Lexical Kahn traversal yields read A, parse A, read B, parse B, join, aggregate, publish. Narrow parse edges remain in stage 0; exchange edges into join add stage 1; the exchange into aggregate adds stage 2; narrow publish remains in stage 2. Earliest finishes are 3, 5, 2, 6, 13, 17, and 18 by dependency order. The predecessor with latest finish at join is parse B, so the critical path is read B, parse B, join, aggregate, publish. Eighteen assumes deterministic vertex durations, unlimited suitable resources, zero edge/queue/control overhead, and no failure. It is a structural lower bound, not a wall-time forecast.

### Answer 2

Kahn's algorithm removes only zero-indegree vertices and their outgoing edges. A finite DAG always contains a zero-indegree vertex; otherwise repeatedly following predecessors must revisit a vertex and form a cycle. Induction removes all vertices of a DAG. Conversely, a directed cycle's vertices retain at least one incoming cycle edge, so if the algorithm cannot emit all vertices, the residual graph contains a cycle. The result does not prove correct edge meaning, semantic equivalence, artifact integrity, resource feasibility, absence of runtime deadlock, retry safety, authorization, or correct publication.

### Answer 3

Read, validate, normalize, and safely filter each fact source in narrow pipelines. Prepare the bounded dimension once and broadcast it only if measured size, per-worker capacity, update snapshot, and authorization permit; otherwise exchange each input by the same dimension key and join. Union compatible enriched facts, exchange by canonical region, partially aggregate before exchange when the accumulator is mergeable, then finalize by region. Let both sinks consume one committed region aggregate; materialize it if sink isolation/retry or reuse justifies the cost. Task identity includes graph/plan/stage/partition and attempt; outputs remain isolated until commit. Profile hot dimension and region keys by records, bytes, CPU, output, and tail duration; salt only mergeable groups with a second merge.

### Answer 4

Pure object partitions use attempt-specific names, expected schema/digest/partition metadata, and one manifest commit winner; canceled or losing attempts remain invisible and are garbage-collected. Database updates use a transaction or stable graph-output idempotency key with an outbox/reconciliation record; ambiguous timeouts are queried before retry. Notifications consume committed outbox events under stable deduplication IDs rather than running inside speculative compute attempts. Cancellation stops admission, requests cooperative termination, preserves committed effects, and marks ambiguous effects for reconciliation. Attempt, winner, request, response, and compensation records are retained under policy.

### Answer 5

Pin logical and physical plan digests, legal rewrite rules, optimizer/runtime/code versions, schemas, purpose and residency policy, input/side-input snapshots, statistics, seeds, resources, identity, and sink contracts. Compare adaptive and fixed reference plans on empty, sparse, skewed, subgroup, malformed, late, and failure cases; verify value/error equivalence, placement authorization, lineage, critical path, movement, state, and recovery. Record every runtime rewrite and guard value. Named review includes clinical or benefits domain owners, data stewards, privacy/legal/records and jurisdiction specialists, affected communities or ethics oversight, fairness/statistics experts, security/identity/key management, platform/runtime/network operators, accessibility, incident recovery, and independent assurance. Performance cannot waive rights, purpose, placement, correction, appeal, retention, or deletion duties.
