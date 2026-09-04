---
module_id: LSDS-084
program: Large-Scale Data Systems Engineering
level: 2
module_number: 84
title: Lineage-Based Recompute
status: complete
last_verified: 2026-09-04
---

# Lineage-Based Recompute

## One-Page Review

### Governing question

How can a distributed runtime reconstruct only lost derived partitions from stable inputs and a versioned dependency graph, while stopping at verified materializations, handling wide dependencies and evolving plans, and preventing nondeterminism or external side effects from turning recomputation into a different computation?

### Essential definitions

- **execution lineage** is the machine-readable derivation recipe for an output partition, including logical operator, parent partitions, code/config, and input versions.
- A **lineage node** represents a logical dataset/partition version, not one physical attempt.
- A **narrow dependency** lets one child partition depend on a bounded small set of parent partitions.
- A **wide dependency** may require many or all parent partitions, commonly across a shuffle.
- A **materialization boundary** is a complete durable result that can replace its upstream lineage during recovery.
- A **recompute closure** is the least backward dependency set needed to rebuild a required lost output.
- **lineage truncation** makes a checkpoint/materialization the new recovery root and retires older derivation state when safe.
- A **determinism envelope** lists the inputs, code, configuration, environment, order, seeds, and external versions that must remain stable.
- **recovery amplification** compares recomputed work with the directly lost work.
- **provenance lineage** explains data origin/governance; it may lack the partition-level executable detail required for recovery.

### Central model, mechanism, or theorem

Let dependency DAG $G=(V,E)$ map each logical output partition $v$ to parent partitions $parents(v)$ and a versioned deterministic transformation $f_v$. For required lost target set $T$, verified available materializations $A$, and stable roots $S$, define the least closure

$$R(T,A)=T\cup\bigcup_{v\in R\setminus(A\cup S)}parents(v).$$

Nodes in $A\cup S$ are reusable boundaries and are not recomputed; unavailable descendants in $R$ are scheduled in topological order. The reconstruction proof requires exact logical identities, complete parent mapping, stable root versions, compatible code/config, and deterministic transformation semantics. A cached object without integrity or a path reread at “latest” is not a boundary.

### Critical invariants

- Logical dataset and partition IDs are stable across attempts and bind graph/plan version.
- Each lineage edge names exact parent partition versions and dependency type, including shuffle mapping where required.
- Root inputs are immutable/pinned or have a replay contract that reproduces the same records and ordering semantics.
- Reused materializations are complete, checksummed, schema/partition compatible, and retained for the entire recovery.
- Recompute never crosses a valid boundary unnecessarily and never stops at an unverified cache entry.
- Transform code, closure captures, configuration, runtime semantics, locale/time zone, seeds, and referenced external data are versioned.
- Wide dependencies recover every required map output or equivalent durable shuffle partition before reduce output commits.
- Stateful cycles/iterations are represented by explicit epochs/checkpoints rather than an unbounded cyclic recovery graph.
- External effects occur behind idempotent/transactional commit boundaries, not inside replayable transformations.
- Lineage and boundary garbage collection preserves every live consumer, retry, branch, audit, and recovery horizon.

### Common failures

Common failures include recording dataset-level but not partition-level dependencies; treating a mutable path as a stable root; omitting code/config/runtime identity; assuming closures are deterministic despite current time, randomness, locale, unordered reductions, or remote lookups; stopping at an incomplete local cache; expanding a narrow loss through an entire graph unnecessarily; under-expanding a wide shuffle dependency; confusing logical plan edges with the executed adaptive plan; retaining lineage forever without checkpoints; truncating it before boundary verification; recomputing an external API side effect; and calling governance lineage executable when it cannot identify exact parent partitions or transformation semantics.

### Compact example

`report` depends on `join`; `join` depends on `left` and `right`; both branches derive from `filter`, then `parse`, then stable `raw`. `left` is durably materialized while `report`, `join`, and `right` are lost. Backward traversal reuses `left` and `raw`, and recomputes `parse`, `filter`, `right`, `join`, and `report`. It does not rebuild `left` merely because its ancestors appear in the graph. If the join's executed partition mapping changed under adaptive execution, the lineage must reference that executed version, not regenerate today's preferred plan.

### Connections

[LSDS-031](031-shuffle-architecture.md) supplies wide-dependency materialization, [LSDS-043](043-stateful-operators.md) supplies epoch state, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies replay safety, [LSDS-068](068-adaptive-query-execution.md) supplies executed-plan identity, [LSDS-081](081-task-level-failure-recovery.md) supplies recovery regions, and [LSDS-083](083-coordinator-failure.md) supplies durable graph recovery.

## Governing Question

Replication makes recovery fast but stores extra copies of every derived byte. For coarse-grained deterministic transformations, a system can instead store the recipe and rebuild only missing partitions from surviving data. This trades steady-state storage and network cost for failure-time compute.

Lineage is useful only when executable and exact. “Table B came from table A” helps governance but cannot tell a scheduler which input splits, shuffle buckets, code artifact, schema, seed, or configuration reproduce partition 27. Recovery lineage is a versioned dependency graph at the runtime's logical partition granularity.

The governing question is how to capture that graph, calculate the minimum safe closure, ensure replay equivalence, choose materialization cuts, and operate lineage depth and retention under failure and plan evolution.

## Why This Matters

Lineage recovery lets runtimes cache aggressively in memory without synchronously replicating every derived partition. A lost executor can trigger parallel recomputation of its partitions rather than full dataset reload. This is especially valuable for iterative and interactive workloads with large reusable working sets.

The tradeoff worsens with long chains, wide dependencies, expensive sources, skew, nondeterminism, or frequent faults. Losing a tiny final partition can require terabytes of upstream shuffle. Checkpoints and durable exchanges cap this amplification but cost storage, I/O, and write-path latency.

Lineage is also correctness-bearing metadata. Corrupt or stale edges can silently produce plausible wrong output. It requires integrity, access control, compatibility, recovery tests, and garbage collection coordinated with the data it references.

## Prerequisites and Retrieval

Review shuffle in [LSDS-031](031-shuffle-architecture.md), state in [LSDS-043](043-stateful-operators.md), reprocessing in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), adaptive plans in [LSDS-068](068-adaptive-query-execution.md), task recovery in [LSDS-081](081-task-level-failure-recovery.md), and coordinator recovery in [LSDS-083](083-coordinator-failure.md).

You should understand DAGs, topological order, partitions, narrow/wide dependencies, shuffles, lazy evaluation, immutable inputs, content hashes, determinism, caching, checkpoints, retries, epochs, idempotency, reference counting, and reachability.

For diagnosis retain logical dataset/partition IDs, graph and executed-plan versions, parent mapping/dependency types, root snapshots/offsets, code/config/container/runtime digests, schema/partitioner/serializer, randomness/time/locale settings, materialization inventory/checksums, loss target, computed closure, attempts, output digests, and cleanup history.

## Learning Objectives

After this module, you should be able to:

1. Distinguish executable partition lineage from governance provenance and attempt history.
2. Model logical partition derivations, narrow dependencies, wide dependencies, and boundaries.
3. Compute a minimal safe backward recompute closure and topological schedule.
4. Prove when a root input or materialized intermediate is reusable.
5. Define and test a determinism envelope for transformations and reductions.
6. Handle shuffle, adaptive plans, stateful epochs, and iterative computations.
7. Choose cache, replication, checkpoint, and lineage truncation from recovery economics.
8. Fence external side effects from replayable computation.
9. Retain and garbage-collect lineage with consumers, retries, and recovery horizons.
10. Measure lineage depth, closure size, amplification, recovery time, and equivalence.

## Core Exposition

### Logical lineage representation

Represent each dataset version with stable identity, schema, partitioner, number of partitions, transformation kind, code/config/runtime digest, and parents. At partition level record a dependency function: child partition to exact parent partitions or shuffle buckets. Attempts and physical locations are separate inventories.

Use canonical serialization and integrity checks. A recovered coordinator must load the same graph. Changes to optimizer rules or user code create a new graph/version even if human names match. Content addressing helps deduplicate equivalent artifacts but does not replace semantic version metadata.

### Narrow and wide dependencies

A narrow map or filter partition often depends on one parent partition, so loss follows one chain. Union can depend on a known parent segment. A join/group/repartition has a wide dependency: one reduce bucket may need outputs from every mapper or from a versioned subset defined by the executed exchange.

Wide edges are natural stage/materialization boundaries. Durable shuffle can stop recompute at map outputs; lost map blocks require their source lineage and then affected reducers. Never infer dependency breadth solely from operator name—partitioner, pruning, broadcast, skew splitting, and adaptive execution alter it.

### Backward closure and scheduling

Begin from required unavailable targets. For each node, stop if a verified compatible materialization or stable root exists; otherwise add exact parents. Iterate to fixed point. Remove nodes whose output became available during planning, then topologically schedule remaining nodes with resource and locality constraints.

Deduplicate shared ancestors across targets. Prioritize nodes that unlock many descendants, but preserve fairness and capacity limits. Recheck boundaries before consumption because caches can be evicted or workers lost while the closure runs.

### Root-input replay

A file root binds immutable snapshot and file identity, not a mutable directory listing. A log root binds topic/partition, start/end offsets, retention, and decoding schema. A database root binds snapshot/read timestamp or exported snapshot. An API root needs a versioned captured response or replay guarantee.

If a root expired, was overwritten, or now decodes differently, lineage cannot reproduce the output. Fail explicitly, restore a retained snapshot, or start a new computation whose changed semantics are recorded. Do not silently read current data.

### Determinism envelope

Capture code and dependency artifacts, configuration, environment variables that affect semantics, runtime/compiler/library versions, locale, time zone, floating-point mode, partitioning, comparator, serialization, random seed, and external reference-data version. Ban or capture wall clock and mutable remote lookups.

Order-sensitive floating-point aggregation can vary when recovery changes reduction order. Define whether bitwise or tolerance-based equivalence is required, and use deterministic combine/order when exact output identity matters. Stable seeds derive from logical partition/epoch, not attempt start time.

### Materialization validation

An available boundary has logical partition identity, producer graph/code digest, schema/partitioner/serializer, complete marker or atomic manifest, length/record count where meaningful, checksum, storage generation, encryption/key metadata, and retention lease. Validate before pruning ancestors from the closure.

Memory cache is opportunistic; disk cache may share node failure; replicated cache needs owner and quorum semantics; checkpoint/shuffle in durable storage survives broader domains. Partial or stale objects remain unavailable even if paths exist.

### Shuffle and adaptive execution

Lineage for a shuffle includes map-output identity, bucket mapping, partitioner/hash/comparator/serializer, number of partitions, and executed exchange version. If one reduce bucket is lost and all map outputs survive, rerun only that reducer. If map output is missing, recompute its producer then affected reducers.

Adaptive coalescing, skew splitting, join switching, or pruning changes executed dependencies. Persist the chosen plan/epoch or enough deterministic decision input to reproduce it. Recovery must not splice partitions from incompatible pre- and post-adaptive layouts.

### Iteration and state

Logical cycles are represented as acyclic epoch/superstep versions: $X_{i+1}=F(X_i,input_i)$. Checkpoint selected epochs and retain inputs between them. Without truncation, iterative lineage grows with iteration count and a late loss can replay the entire history.

Fine-grained mutable state is poorly represented by coarse lineage unless updates are deterministic and input logs retained. Use state checkpoints and logs for streaming/operator state. Treat accumulator/metric side channels as attempt-aware rather than recovery roots.

### Checkpoint placement and economics

Checkpoint when expected avoided recompute and recovery-tail value exceed write, storage, commit, and runtime interference costs. Consider lineage depth, fan-out, source cost, wide stages, reuse frequency, failure rate/domain, state size, checkpoint bandwidth, and required RTO.

Replicate hot expensive partitions, checkpoint stable wide cuts or iteration epochs, and leave cheap narrow derivations to lineage. Avoid synchronized checkpoint storms. Validate checkpoints before truncating parents; retain prior recovery roots through a safety window.

### Side effects and nondeterministic boundaries

Keep replayable transformations pure. For external effects, emit deterministic intents with stable IDs and publish through a transactional/idempotent sink after logical winner selection. Lineage may recompute the intent many times while only one effect becomes visible.

If a transformation calls a changing service, capture its response as a versioned input or move the call behind a durable boundary. Logging “the service was called” does not reproduce the response. Secrets should be referenced through versioned policy without embedding them in lineage.

### Retention and garbage collection

Lineage, roots, shuffle, checkpoints, cached artifacts, code packages, and schemas have linked lifetimes. Compute reachability from active jobs, consumers, retries, branches, audits, and recovery windows. Release a parent only when every descendant has a valid alternative root and no required explanation depends on it.

Use leases for active recovery, tombstones for deletions, and delayed idempotent cleanup. Deleting a checkpoint before confirming downstream materialization can make an otherwise successful result unrecoverable. Retain provenance longer if governance requires it, but label it non-executable after runtime artifacts expire.

### Observability and verification

Measure graph nodes/edges/depth, narrow/wide edges, root and boundary coverage, materialized bytes, cache hits, closure nodes/partitions/bytes, shared-ancestor deduplication, recompute CPU/I/O/shuffle, amplification, output equality, recovery latency, checkpoint cost, stale/missing boundary failures, and unrecoverable roots. Segment by dataset/operator, plan/code version, failure domain, cache state, and input cohort.

Delete selected partitions at every graph depth; evict boundaries during planning; corrupt checksums; expire a root; change locale/time/seed/library; lose shuffle maps/reducers; trigger adaptive changes; replay an iteration; and duplicate external effects. Compare outputs with a retained reference under the declared equality relation.

## Definitions and Notation

Let:

- $G=(V,E)$ be a versioned logical partition lineage DAG;
- $parents(v)$ be exact parent partitions of node $v$;
- $T$ be required unavailable target partitions;
- $A$ be verified available materializations and $S$ stable roots;
- $R(T,A)$ be the least backward recompute closure;
- $f_v$ be the deterministic transformation and $d_v$ its semantic digest;
- $c(v)$ be recompute cost in bytes, CPU-seconds, or a declared composite;
- $C_R=\sum_{v\in R\setminus(A\cup S)}c(v)$ be closure cost;
- $C_L$ be cost of directly lost outputs;
- $A_R=C_R/C_L$ be recovery amplification when $C_L>0$;
- $p_f$ be failure probability over a stated horizon;
- $C_m$ and $C_s$ be materialization write and retained-storage costs.

Node count, bytes, CPU, and wall time are not interchangeable. Expected-value checkpoint decisions do not replace tail-RTO constraints. A cache hit is reusable only after semantic/integrity validation, and a zero-cost root assumes retained accessible input.

## Mechanisms, Invariants, or Proof Structure

### Closure-minimality proof

Backward traversal adds a parent only when a required unavailable child cannot be derived without it and stops at every verified boundary/root. Any valid reconstruction must supply each such child's exact parents or an equivalent materialization; therefore removing an added unavailable node breaks a derivation path. Nodes outside the closure are neither targets nor required ancestors before a boundary, so recomputing them is unnecessary under the recorded graph.

### Replay-equivalence proof

For stable roots and boundaries, prove by topological induction. Base nodes equal their recorded versions. If all exact parents of $v$ equal the originals and deterministic $f_v$ runs under matching digest/environment, reconstructed $v$ equals the original under the declared relation. Thus every target does. Nondeterminism or missing version identity invalidates the inductive step.

### Materialization-cut proof

A validated materialization $a$ equals the original logical node and is complete for its partition identity. Replacing the entire upstream subgraph needed only to derive $a$ with that stored value preserves every descendant by replay equivalence. Partial coverage creates multiple roots and must be represented partition by partition, not assumed table-wide.

### Checkpoint-value argument

Materialization is economically favorable when its write/storage/interference cost is below expected avoided recovery and repeated-use cost, subject to hard durability/RTO constraints. The estimate must include failure correlation, closure fan-out, cache survival, and checkpoint failure. A lower mean cost can still violate recovery tails.

### Adversarial verification

Test missing/corrupt root, cache eviction, partial checkpoint, narrow/wide dependency, lost map/reducer, shared ancestors, skew split, adaptive version mismatch, deep lineage, iteration checkpoint, nondeterministic time/random/order/lookup, code/schema drift, external-effect replay, concurrent cleanup, and coordinator recovery. Require declared-equivalent output or explicit unrecoverability.

## Alternatives and Trade-Offs

**Lineage recomputation** stores compact recipes and parallelizes recovery but consumes failure-time compute and requires determinism. **Replication** spends steady resources for faster failover. **Checkpointing** caps lineage at durable cuts but adds I/O and latency. Hybrid policies fit mixed costs.

**Fine-grained lineage** minimizes closure but increases metadata volume and coordination. **Dataset/stage lineage** is compact but may recompute excess partitions. Granularity should match scheduler and storage identities.

**Narrow transformations** localize recovery. **Wide transformations** expand parent dependencies but durable shuffle can create a cut. Recomputing shuffle may be cheaper than retaining it for cold jobs; hot iterative workloads differ.

**Bitwise determinism** simplifies verification and content addressing but can cost performance. **Semantic tolerance** may be appropriate for floating-point analytics but complicates downstream caching, tests, and audit.

**Durable remote checkpoints** survive nodes but cost network/storage. **Local checkpoints** truncate lineage cheaply but lose fault tolerance with the host unless replicated. Label the guarantee precisely.

## Failure Modes and Misconceptions

1. **Lineage is an audit label.** Recovery needs executable partition derivations.
2. **Dataset name is a version.** Inputs and plans need immutable identities.
3. **Path existence proves a boundary.** Completeness and checksum are required.
4. **Cache is durable.** Its failure domain and eviction policy matter.
5. **Recompute means rerun the whole job.** Backward closure can be partition-local.
6. **One lost partition needs one parent.** Wide dependencies can require many.
7. **Operator name defines dependency shape.** Executed partitioning defines it.
8. **Today's optimizer can rebuild yesterday's graph.** Adaptive plan identity must persist.
9. **Pure-looking code is deterministic.** Time, random, locale, order, and lookups leak in.
10. **Stable seed per attempt is enough.** Retries need logical-partition seeds.
11. **Floating-point results are naturally identical.** Reduction order changes bits.
12. **Checkpoint completes when bytes exist.** Complete metadata/validation must commit.
13. **Local checkpoint provides durable recovery.** Host loss can remove it.
14. **Truncation is immediate.** Preserve parents until the new root is proven and retained.
15. **Lineage handles mutable state automatically.** Checkpoint/log semantics are often needed.
16. **Recomputed side effects are harmless.** They may duplicate externally.
17. **Low storage cost makes lineage free.** Recovery CPU, I/O, and tails remain.
18. **Governance retention preserves recovery.** Code, inputs, and partition maps may be gone.

## Worked Examples

### Example 1

Lost mapped partition depends only on input split 7. With immutable split and matching code digest, one partition recomputes; unrelated splits remain untouched.

### Example 2

Reduce bucket 4 is lost but all durable map blocks survive. Only bucket 4 reruns. If map block 17 is missing, its lineage runs and every reducer requiring it is invalidated.

### Example 3

Two lost outputs share parsed input partition `p9`. Closure deduplicates `p9` and computes it once, then fans out to both descendants.

### Example 4

Checkpoint covers 70 of 100 partitions. Recovery stops at those 70 but follows lineage for the other 30; table-level “checkpointed” is too coarse.

### Example 5

Transformation reads `/latest/rates.csv`. A retry next day changes output. Pinning the file version or capturing the response converts it to a stable root.

### Example 6

Random sampling seeds from attempt ID; retry selects different rows. Seeding from dataset/partition/epoch reproduces the logical sample.

### Example 7

Adaptive execution coalesces 200 shuffle buckets into 40. Recovery uses the recorded 40-bucket map, not the optimizer's current 60-bucket choice.

### Example 8

Iteration 1,000 loses state with no checkpoint since 0. A checkpoint at 900 bounds replay to 100 epochs, trading periodic write cost for recovery tail.

### Example 9

Replay recomputes an email intent three times with stable ID `invoice-8`; winner publication sends or deduplicates one email rather than calling SMTP inside the map.

### Example 10

The executable fixture computes a minimal closure around verified `left` and `raw` materializations.

<!-- bijux-verify: {"id":"lineage-closure","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"target=report\nrecompute=filter,join,parse,report,right\nreuse=left,raw\nwork_units=105\n","stderr":""}} -->
```python
parents = {
    "raw": [],
    "parse": ["raw"],
    "filter": ["parse"],
    "left": ["filter"],
    "right": ["filter"],
    "join": ["left", "right"],
    "report": ["join"],
}
cost = {"parse": 20, "filter": 15, "left": 25, "right": 25, "join": 40, "report": 5}
available = {"raw", "left"}
target = "report"
recompute = set()
stack = [target]
while stack:
    node = stack.pop()
    if node in available or node in recompute:
        continue
    recompute.add(node)
    stack.extend(parents[node])

print(f"target={target}")
print(f"recompute={','.join(sorted(recompute))}")
print(f"reuse={','.join(sorted(available))}")
print(f"work_units={sum(cost[node] for node in recompute)}")
```

## Cross-Program Connections

- **Data structures:** DAG traversal, topological sorting, reachability, memoization, and reference counts implement lineage.
- **Functional programming:** pure functions, immutable values, referential transparency, and controlled effects enable replay.
- **Build systems:** dependency graphs, content hashes, action caches, and hermetic inputs mirror recomputation semantics.
- **Distributed systems:** partitions, retries, epochs, durable logs, and failure domains define availability.
- **Database systems:** materialized views, incremental maintenance, WAL/checkpoints, and snapshot identity offer related tradeoffs.
- **Machine learning:** iterative state, random seeds, nondeterministic kernels, and expensive checkpoints stress recovery.
- **Governance:** provenance, audit, retention, and right-to-delete overlap with but do not equal executable lineage.
- **Economics:** storage, network, recovery compute, failure probability, reuse, and tail value determine materialization.

## References

1. Apache Spark, [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Current. Documents lazy transformations, persistence, partitioning, and automatic recovery.
2. Zaharia et al., [Resilient Distributed Datasets](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf). NSDI 2012. Introduces coarse-grained lineage recovery and checkpoint tradeoffs.
3. Apache Spark, [RDD Checkpoint API](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.checkpoint.html). Current. Documents reliable checkpointing and removal of parent references.
4. Apache Spark, [Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming-programming-guide.html). Current. Discusses lineage growth and checkpoint interval tradeoffs.
5. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents persistence cleanup, shuffle tracking, retries, and recovery-related controls.
6. Ray, [Task Fault Tolerance](https://docs.ray.io/en/latest/ray-core/fault_tolerance/tasks.html). Current. Documents task lineage reconstruction and retry semantics.
7. Dask Distributed, [Resilience](https://distributed.dask.org/en/stable/resilience.html). Current. Documents recomputation from task graphs after worker/data loss.
8. Apache Flink, [Task Failure Recovery](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/task_failure_recovery/). Version 2.3. Defines dependency-sensitive restart scopes.
9. Apache Beam, [Execution Model](https://beam.apache.org/documentation/runtime/model/). Current. Defines bundles, co-failure, retry, and output discard.
10. Apache Hadoop, [MapReduce Tutorial](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html). Current. Documents map/reduce dependencies, attempts, and recovery.
11. Google Cloud Dataflow, [Exactly-once in streaming](https://cloud.google.com/dataflow/docs/concepts/exactly-once). Current. Discusses retries, deduplication, state, and side effects.
12. Bazel, [Remote Caching](https://bazel.build/remote/caching). Current. Documents content-addressed/action-cache reuse and hermeticity implications.
13. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/). Current. Defines job/run/dataset provenance events, useful for contrasting governance and executable lineage.

## Exercises

### Exercise 1

Given target T with parents J and K; J is durably available; K depends on M and N; M depends on stable root R; N is available. Compute the recompute closure and reusable boundaries.

### Exercise 2

Design the determinism envelope for a distributed sampling and floating-point aggregation pipeline that joins daily exchange rates.

### Exercise 3

A lost reduce bucket has 1,000 map parents; 990 durable shuffle blocks survive and 10 are missing. Describe the exact recovery and validation sequence.

### Exercise 4

Design a checkpoint policy for a 2,000-iteration algorithm with growing lineage, skewed checkpoint sizes, and a ten-minute recovery SLO.

### Exercise 5

Design fault-injection evidence proving a lineage engine recomputes the minimum safe closure and preserves results and external effects.

## Answers to the Exercises

### Answer 1

T is unavailable, so include T. Its J parent is a verified boundary and stops; include unavailable K. K's M and N parents are examined: N is available and stops; include M, whose parent R is a stable root and stops. Recompute set is `{M,K,T}` in topological order M, K, T; reusable boundaries are `{R,J,N}`. If any boundary fails identity/integrity validation, expand through its parents instead.

### Answer 2

Pin input snapshots/files and the exact dated exchange-rate version; record graph/executed-plan, schema, partitioner/hash/comparator/serializer, code/container/library/runtime/compiler versions, configuration, locale, time zone, numeric mode, and join semantics. Derive sampling seeds from logical dataset/partition/epoch, not attempts. Specify reduction tree/order or a tolerance-based equivalence with error bounds. Capture null/NaN and decimal/currency rounding policy. Ban uncaptured wall clock and mutable service lookups, and hash output partitions for replay comparison.

### Answer 3

Verify the 990 blocks by map logical identity, attempt/epoch winner, shuffle/exchange version, bucket mapping, length, checksum, completeness, and retention. For each missing block, traverse only that mapper's lineage to stable inputs/boundaries, deduplicate shared ancestors, and recompute the same map-output partition under matching code/partitioner/serializer. Commit and validate replacement blocks. Then rerun the lost reduce bucket using all 1,000 compatible blocks; no other reduce bucket reruns unless it consumed a missing block whose former partial result cannot be preserved. Fence old attempts and winner-commit the reduce output.

### Answer 4

Measure per-epoch lineage/recompute cost, checkpoint bytes/time/interference, restore bandwidth, failure rate/domain, and tail recovery. Choose candidate cuts at stable iteration epochs and partition checkpoint work to avoid a single synchronized spike. Set the interval so worst credible replay after the latest completed checkpoint plus restore fits ten minutes; adapt for growing/skewed state, perhaps checkpointing expensive partitions more often. Retain at least the prior verified checkpoint and input epochs until the new one reloads and commits, monitor oldest lineage and modeled/rehearsed recovery, and reduce interval or increase bandwidth when the SLO margin erodes.

### Answer 5

Build a versioned DAG with narrow, wide, shared-parent, adaptive, and checkpointed branches plus a stable-ID external intent. Retain a failure-free reference. Delete individual target, parent, shuffle, and cache partitions; corrupt a boundary; expire one root; change seeds/locale/library; and race cleanup/coordinator recovery. Assert the engine's recorded closure equals an independently computed backward closure, reusable boundaries validate, unrelated nodes do not execute, tasks run topologically, and output equals the declared reference relation. Verify one external effect per identity. Report closure nodes/bytes/CPU, shared-parent deduplication, amplification, boundary hits/failures, and recovery latency.
