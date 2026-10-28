---
module_id: LSDS-064
program: Large-Scale Data Systems Engineering
level: 2
module_number: 64
title: Distributed Hash and Merge Joins
status: complete
last_verified: 2026-09-04
---

# Distributed Hash and Merge Joins

## One-Page Review

### Governing question

How should a distributed query engine choose and execute hash or merge joins so SQL multiplicity, null, outer-row, and ordering semantics remain correct while partitioning, memory, spill, skew, failures, and adaptive decisions are bounded?

### Essential definitions

- An **equi-join** matches rows using equality predicates; a **theta join** may use arbitrary comparison predicates.
- The **build side** of a hash join is inserted into a keyed structure; the **probe side** looks up matches.
- A **broadcast join** replicates one side to every participating worker; a **partitioned join** redistributes both sides by compatible join keys.
- A **co-located join** uses an already compatible distribution contract and avoids a new repartition exchange.
- A **grace hash join** partitions inputs so individual build partitions can fit memory, recursively repartitioning or spilling when necessary.
- A **merge join** advances through inputs ordered compatibly on join keys and handles equal-key runs as groups.
- A **semi join** returns qualifying rows from one side without multiplying them by all matches; an **anti join** returns rows with no qualifying match.
- **null-safe equality** is a distinct predicate under which null may match null; ordinary SQL equality yields unknown for null operands.
- A **dynamic filter** derives runtime information from one side to prune the other without changing final join semantics.
- **join skew** is unequal rows, bytes, matches, memory, or work across keys or partitions.

### Central model, mechanism, or theorem

For compatible hash-partitioned inputs $R$ and $S$ on join key $k$, destination $p(x)=h_v(k(x))\bmod q$ gives local partitions $R_i,S_i$. For ordinary equality,

$$R\bowtie_k S=\bigcup_{i=0}^{q-1}(R_i\bowtie_k S_i),$$

provided equal non-null keys use the same type-aware hash/count/epoch and each selected input row appears in exactly one partition. Local hash join must retain every build row for a duplicate key and emit the Cartesian product of equal-key runs. Merge join requires compatible key ordering and likewise expands equal runs. The identity supplies correctness of partitioned local joins; it does not guarantee balance, memory fit, failure recovery, or low cost.

### Critical invariants

- Join type, predicate, output schema, duplicate semantics, null behavior, correlation, and residual conditions are fixed before physical selection.
- Partitioned peers agree on key expressions/types, hash/comparator version, null policy, partition count, and ownership epoch.
- Every matching pair appears exactly once; duplicates are neither collapsed nor multiplied beyond relational semantics.
- Ordinary equality never matches null to null, while null-safe equality follows its separately declared contract.
- Outer joins emit each preserved unmatched row exactly once after all possible matches for its scope are known.
- Hash build memory, merge equal-key runs, buffers, spill, dynamic filters, and retry state have explicit bounds.
- Broadcast selection accounts for decoded/hash-table bytes on every destination and concurrent joins.
- Spill partitions and sorted runs carry query, join, side, partition, attempt, schema, integrity, and retention identity.
- Retried or speculative attempts cannot make two versions of the same join partition visible downstream.
- Adaptive strategy changes occur before dependent consumers commit to incompatible distribution or restart them under a new epoch.

### Common failures

Common failures include choosing a build side by row count while rows are huge; representing one build row per key and losing duplicates; matching nulls under ordinary equality; emitting an outer unmatched row before the other side is complete; calling two distributions compatible because both say “hash”; broadcasting underestimated data to hundreds of workers; assuming repartition balances hot keys; spilling only the build side without aligning probe partitions; allowing recursive repartition to repeat on an unsplittable heavy key; merge-joining inputs with different collation or null order; using a Bloom filter as an exact anti-join test; mixing speculative outputs; and changing broadcast to partitioned after downstream tasks consumed the old layout.

### Compact example

The build side contains two rows for key 1, and the probe side contains two rows for key 1. An inner equality hash join must emit four pairs, not one or two. Each side also contains a null key, but those rows do not match under ordinary SQL equality. A bucket maps key 1 to a list of both build rows, and every probe duplicate iterates the entire list.

### Connections

[LSDS-031](031-shuffle-architecture.md) supplies shuffle mechanics, [LSDS-053](053-fair-and-capacity-scheduling.md) constrains resources, [LSDS-061](061-distributed-logical-and-physical-plans.md) selects physical properties, [LSDS-062](062-coordinator-and-worker-architecture.md) executes tasks, and [LSDS-063](063-exchange-operators.md) establishes compatible distribution and attempt visibility.

## Governing Question

Joins combine data sets and often dominate distributed SQL cost. A local algorithm is only one layer. The engine must preserve the logical join type, arrange input distribution, choose build/probe or sort/merge roles, allocate memory, handle duplicates and nulls, recover attempts, and manage skew. An algorithm that is correct on one machine can return incomplete or duplicated results when partition boundaries disagree.

Hash and merge joins represent different resource shapes. Hash joins need a build structure and support fast equality probes, but memory and skew can force spill. Merge joins can stream ordered inputs and support some inequality patterns, but obtaining compatible global partitioning and local order may cost large sorts. Neither is universally superior.

The governing question is how to prove semantic and distribution preconditions, estimate full distributed cost, detect violated estimates at runtime, and change strategy only at safe boundaries while retaining explainable evidence.

## Why This Matters

A wrong join can silently corrupt every downstream aggregate. Duplicate-key mishandling undercounts; an accidental null match invents relationships; an early outer-row emission duplicates or contradicts later matches; incompatible hash versions omit pairs; retry output can double results. These errors may survive plausibility checks because most keys are simple.

Performance failures are similarly nonlinear. A dimension estimated at 50 MiB may decode into gigabytes per worker. One hot key can create a partition larger than all others combined. A hash table can consume several times serialized input due to object, pointer, bucket, and allocator overhead. Merge input may already be ordered—or sorting may dominate the query.

Join strategy also affects platform behavior: exchange volume, task count, memory requests, spill I/O, object-store calls, scheduler delay, and recovery scope. A useful design connects logical semantics to physical property proofs and then to measurable resource and failure behavior.

## Prerequisites and Retrieval

Review partitioned shuffle in [LSDS-031](031-shuffle-architecture.md), resource scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), distributed plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator/worker state in [LSDS-062](062-coordinator-and-worker-architecture.md), and exchange contracts in [LSDS-063](063-exchange-operators.md).

You should understand SQL inner/outer/semi/anti joins, bags, three-valued logic, hash tables, sorting and merging, partitioning, cardinality estimates, memory accounting, spill, skew, Bloom filters, retries, and adaptive execution.

## Learning Objectives

After this module, you should be able to:

1. state duplicate, null, residual-predicate, and preserved-row semantics for each join type;
2. prove when partitioned local joins compose into a complete distributed result;
3. implement and audit duplicate-preserving hash build/probe logic;
4. implement and audit equal-run and outer-row behavior in merge joins;
5. compare broadcast, repartition, co-located, singleton, and indexed/nested-loop strategies;
6. size hash memory, merge buffers, network, sort, spill, and parallelism with uncertainty;
7. design grace partitioning and detect unsplittable heavy keys;
8. apply dynamic filtering, skew mitigation, and adaptive changes without semantic shortcuts;
9. preserve attempt, spill, exchange, and output correctness under failure; and
10. validate joins with differential, metamorphic, adversarial, fault, and performance testing.

## Core Exposition

### Fix logical semantics first

Record join type, equality keys, residual predicate, output attributes, preserved side, correlation, and whether equality is ordinary or null-safe. SQL inputs are bags unless `DISTINCT` applies. Two identical rows remain two rows, and duplicate matches multiply.

For a composite key, ordinary equality matches only when every component comparison is true. A null component makes ordinary equality unknown, not true. Residual predicates apply to candidate pairs at the declared logical position and can change outer-join preservation.

### Distinguish join families

Inner join emits matching pairs. Left, right, and full outer joins additionally preserve unmatched rows from designated sides using null extension. Semi join emits each qualifying left row according to left multiplicity without one output per right match. Anti join emits left rows for which no qualifying match exists.

Existence-based joins often short-circuit after a proven match, but null-aware forms such as SQL `NOT IN` require special three-valued reasoning. Never substitute an ordinary anti join solely from surface syntax.

### Preserve duplicate multiplicity in hash join

Build hash tables map a key to all relevant build rows or a structure representing their full multiplicity. On probe, every qualifying build row pairs with the probe row and passes residual predicates. Overwriting a prior row for the same key converts bag semantics into an accidental key constraint.

If a declared uniqueness constraint proves at most one build row, an optimized representation is safe for that snapshot. Retain constraint provenance and validation. Corrupt or stale uniqueness metadata can become wrong results, not merely bad performance.

### Handle nulls deliberately

Ordinary equi-join can omit null-key rows from the hash table because they cannot match, while preserved-side outer semantics still need them. Null-safe equality needs a canonical null hash/equality rule. Composite keys distinguish a null component from an entirely null key only through their exact tuple semantics.

Merge comparison also needs a null order for traversal, but sort adjacency does not imply join equality. Keep ordering comparison and equality predicates separate when their semantics differ.

### Complete outer joins only after evidence

A left hash outer join tracks whether each probe-side preserved row found any residual-qualified build match, then emits one null-extended row if none did. If the build side is preserved, unmatched build rows need visited state and can be emitted only after the complete relevant probe partition finishes.

In distributed execution, “complete relevant partition” depends on committed exchange inputs, not one producer finishing. Retry and speculation must not cause unmatched rows to be emitted from a losing attempt.

### Prove distributed co-location

Partitioned equality join is complete when equal eligible keys from both sides route to the same destination and each row has one selected assignment. Compatibility includes expressions, coercions, resolved types, hash version/seed, null policy, partition count, and ownership epoch.

Co-location inherited from storage also requires current bucket/table contracts and snapshot ownership. If any property is uncertain, insert a compatible exchange rather than trusting names like `bucketed_by=id`.

### Choose a broadcast join

Broadcast one side when its measured or conservatively bounded decoded build state fits every destination under concurrency and fault headroom. Network transmission grows with destinations, and each worker constructs or receives its own representation. The other side remains source-distributed.

Broadcast is attractive for a small dimension against a large fact table because it avoids fact repartition. Guard before fan-out, cap simultaneous broadcasts, backpressure slow receivers, and retain a safe fallback if runtime size exceeds the bound.

### Choose a repartition join

Hash-repartition both sides on compatible equality keys when neither can be broadcast safely and no compatible distribution exists. Each destination builds one side and probes the other. Network approaches moved bytes from both sides, subject to locality, compression, and prior distribution.

Partition count controls parallelism, per-task state, channels, and files. It does not solve key skew automatically. Size memory and spill for upper partition quantiles and known heavy hitters, not the mean alone.

### Use co-located joins cautiously

If tables share compatible bucket or partition layout, local joins can avoid network movement. Validate partition count, function version, key transformations, schema/type, null rules, snapshot, and mapping of storage partitions to tasks.

Evolution can break compatibility: one table may have been rewritten under new buckets, or only some files follow the advertised layout. Metadata must prove file-level or snapshot-level guarantees. A false co-location claim omits matches.

### Consider singleton and indexed nested loops

Non-equality or correlated joins may use nested loops, sometimes with a parameterized index lookup. Broadcasting a small outer side to workers that probe a remote index can be effective, but creates request amplification, dependency load, and snapshot consistency requirements.

Singleton nested loop is a correctness fallback, not necessarily an operationally safe one. Bound input cardinality and runtime. Reject or warn when an unconstrained Cartesian product would exceed policy.

### Build hash tables with bounded memory

Account for key/value payload, row references, bucket arrays, load factor, hash values, null/visited flags, alignment, allocator fragmentation, vector batches, and operator buffers. Serialized input size is not hash-table memory. Measure implementation-specific amplification.

Reserve memory before build growth, spill before hard exhaustion, and coordinate with worker-wide arbitration. Multiple concurrent joins, exchanges, and aggregations compete. An operator's local limit cannot assume the rest of the fragment is empty.

### Implement grace hash partitioning

Partition both build and probe inputs by a first hash into aligned spill partitions. Process each pair when the build partition fits; recursively repartition oversized pairs using a different hash/bit range. Store schema, hash generation, side, partition, attempt, counts, checksums, and completion manifest.

Recursion does not fix one unsplittable key whose equal rows all belong together. Detect lack of reduction and switch to a heavy-key method, external representation, merge, or controlled failure. Avoid repartition loops that consume I/O indefinitely.

### Keep probe and build spill aligned

If build partition 7 spills, matching probe rows for partition 7 must be buffered/spilled for later processing under the same mapping. Probing an incomplete in-memory subset loses matches. Hybrid hash joins retain selected build partitions in memory and spill aligned remainder.

Memory reclamation and asynchronous spill require ownership rules. Do not free a page while a hash entry or output still references it. Bound spill queues and include storage failure in query recovery.

### Execute merge joins over equal runs

With compatibly sorted inputs, compare current keys. Advance the smaller key for inner equality. When keys equal, collect or revisit the full run on each side and emit their Cartesian product subject to residual predicates. Large duplicate runs may need spill.

Outer merge joins emit a preserved run only after proving no match. Semi joins emit preserved rows once according to left multiplicity; anti joins emit unmatched left runs. Comparator, collation, direction, null order, and equality must be consistent across producers.

### Obtain compatible order and ranges

Local sort is insufficient if matching keys reside in different workers. Use compatible range partitioning so equal keys share a partition, then sort locally, or hash partition and sort each hash partition. Range boundaries must not split an equal-key run unless the algorithm replicates/coordinates it correctly.

If both inputs already share order and distribution, merge can stream. Otherwise account for exchange and external sort costs. “Merge join uses little memory” ignores sorting and equal-run buffers.

### Compare full costs

Broadcast network is roughly build bytes times destination count; repartition moves eligible bytes of both sides; co-location minimizes join exchange; merge may add two sorts. Refine with compression, locality, output size, decoded memory, spill, startup, skew, critical path, and failures.

Cardinality and byte estimates need provenance and uncertainty. Cost each legal build orientation. A smaller row count may have larger rows or worse duplicates. Output cardinality can dominate even when both inputs are small.

### Select build and probe roles

For inner hash join, building the smaller bounded side usually reduces memory, but source pipeline, dynamic filters, output order, and spill behavior matter. Outer joins constrain role and unmatched tracking but do not eliminate all implementation choices.

Expose selected orientation and estimates in explain output. At runtime measure actual build rows/bytes, distinct keys, bucket distribution, memory, and time before deciding the estimate was sound.

### Apply dynamic filters safely

A build-side set, range, or Bloom filter can prune probe scans or exchange. Exact filters may prove absence; Bloom filters can yield false positives but must not yield false negatives under their contract. Therefore Bloom “not present” can prune, while “present” still requires the join.

Do not use a probabilistic filter alone to decide anti-join output. Time out or proceed without late filters rather than blocking indefinitely. Associate filters with query/join/build attempt/snapshot and discard stale or losing-attempt filters.

### Diagnose skew by work

Measure input rows/bytes, distinct keys, match count, output rows, build memory, probe comparisons, spill, CPU, and elapsed time per partition and key sample. A hot key produces quadratic-looking output multiplicity when both sides have duplicates; salting cannot remove required output work.

Separate distribution skew from inherent result skew. Better partitioning can distribute a hot key only by replicating one side and splitting the other, with a proof that each pair appears once. If output itself is enormous, admission or query redesign may be required.

### Mitigate heavy keys

Detect heavy keys from statistics or blocking exchange manifests. Route non-hot keys normally. For a hot equality key, split one side across subpartitions and replicate the matching subset of the other side, then union outputs. Choose replication direction by bounded size.

Outer, semi, and anti joins complicate unmatched-row ownership; designate one subpartition to emit preserved unmatched rows or use a separate proof. Null keys follow declared equality. Test duplicates exhaustively.

### Adapt at safe boundaries

Runtime build size can switch planned broadcast to repartition before broadcast consumers commit. Measured partition sizes can split skew or coalesce small partitions. A materialized exchange provides evidence and replayable input for a new strategy.

Create a new plan/exchange epoch, cancel incompatible downstream attempts, and retain prior data until replacement commits. Bound adaptation count and consider sunk work. Never mix hash output from one strategy with merge consumers expecting another property.

### Recover failures and attempts

Spill files, sorted runs, build state, dynamic filters, and exchange manifests are attempt-scoped unless explicitly durable/shared. On worker loss, restart from the nearest committed exchange/materialization boundary. Pipelined consumers may also need restart.

Select one successful join-task attempt downstream. External indexed lookups require retry-safe reads and consistent snapshots; output sinks require their own commit protocol. Charge failed/speculative work to resource accounting.

### Observe join execution

Correlate logical join, physical algorithm/orientation, distribution, exchange, partition, task/attempt, worker, and adaptive epoch. Emit estimated/actual input and output rows/bytes, distinct/null/heavy keys, build memory, buckets, probe rates, sort/run sizes, network, spill, blocked time, dynamic-filter selectivity, retries, and tail.

Preserve rejected strategies and reasons where feasible. Aggregate dashboards should not hide one failing partition or all permanently spilled queries. Redact keys and statistics under data-governance policy.

### Validate semantics and performance

Differentially compare hash, merge, and trusted reference joins. Generate empty inputs, duplicates, all-null/composite keys, NaN where supported, outer unmatched rows, residual predicates, extreme output multiplicity, skew, and uniqueness claims. Metamorphic partition-count changes should not change results.

Inject stale statistics, broadcast overflow, spill-full/corruption, worker loss, duplicate attempts, late dynamic filters, adaptive cancellation, and mixed hash/comparator versions. Gate correctness first, then memory bounds, spill, network, critical-path latency, fairness, recovery, and cost.

## Definitions and Notation

Let input bags be $R$ and $S$, join-key functions $k_R,k_S$, and residual predicate $\theta(r,s)$. For ordinary equality, pair $(r,s)$ matches when $k_R(r)=k_S(s)$ evaluates true and $\theta$ evaluates true; unknown does not match.

Let hash version $h_v$, partition count $q>0$, and owner $p(x)=h_v(k(x))\bmod q$. Partitions $R_i=\{r:p(r)=i\}$ and $S_i=\{s:p(s)=i\}$ are compatible only under common key/type/null/hash/count/epoch contracts.

For key $a$, multiplicities $m_R(a)$ and $m_S(a)$ contribute $m_R(a)m_S(a)$ inner-join pairs before residual filtering. This product explains why a single hot duplicate key may dominate required output work.

Let build serialized bytes be $B$, decoded hash amplification $\alpha$, destinations $w$, and per-worker available join memory $M_j$. A broadcast safety check needs $\alpha B$ plus buffers and concurrent operators below each worker's governed budget; total replicated state approaches $w\alpha B$. These are estimates with measured uncertainty, not universal thresholds.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Fix join type, keys, residuals, bag multiplicity, null/null-safe behavior, preserved sides, correlation, and output schema.
2. Enumerate legal hash, merge, broadcast, repartition, co-located, and nested/indexed alternatives with build orientation.
3. Prove input distribution/order compatibility or insert versioned exchange and sort enforcers.
4. Cost bytes, decoded memory, network replication, sort, spill, output, parallelism, skew, and critical path with estimate provenance.
5. Implement duplicate/null/outer/semi/anti semantics and bound hash state, merge runs, buffers, filters, and recursion.
6. Identify spill/sort/exchange/task attempts, validate manifests, and expose only selected compatible output.
7. Measure heavy keys and distinguish remediable partition skew from inherent output multiplicity.
8. Apply dynamic filters or adaptive changes only with sound pruning and safe plan/exchange epochs.
9. Observe estimates, actuals, resources, tails, retries, rejected strategies, security, fairness, and cost.
10. Differential/metamorphic test edge data, fault-inject distributed states, canary optimizer/runtime changes, and retain rollback.

The partitioned-join identity follows because every matching non-null key pair maps to the same unique $i$, local join emits that pair with full multiplicity, and no other partition can emit it. It fails if routing, attempt selection, or local bag semantics fails.

For equal key $a$, a correct inner join emits the Cartesian product of its two runs, yielding $m_R(a)m_S(a)$ candidates. Replacing either run with one representative is valid only under a proven uniqueness or existence-only semantic.

A Bloom filter with no false negatives can safely prune keys reported absent, but reported presence is inconclusive. It cannot by itself prove a match for semi join or absence of match for anti join; exact join evaluation remains.

## Alternatives and Trade-Offs

- **Broadcast hash join:** avoids large-side shuffle; replicates build network/memory and risks estimate failure.
- **Repartition hash join:** handles two large inputs; moves both and remains sensitive to hot keys.
- **Co-located hash join:** minimizes exchange; demands exact current storage/plan compatibility.
- **Grace hash join:** bounds memory through partition/spill; adds I/O and cannot split one equal hot key normally.
- **Merge join:** streams compatible order and handles ranges; sort/exchange and duplicate-run memory can dominate.
- **Indexed nested loop:** efficient for selective probes; amplifies remote calls and dependency coupling.
- **Singleton nested loop:** broad semantic fallback; limited parallelism and explosive Cartesian work.
- **Exact dynamic filter:** strong pruning; construction/transfer state may be large.
- **Bloom dynamic filter:** compact with safe false positives; cannot replace exact join semantics.
- **Static strategy:** deterministic and simple; cannot correct runtime estimate error.
- **Adaptive strategy:** uses actual size/skew; requires materialization, epochs, restart, and sunk-cost control.
- **Many partitions:** smaller average build state; more tasks, channels, files, and scheduling overhead.
- **Few partitions:** lower coordination; larger state and less skew flexibility.
- **Heavy-key splitting:** distributes work; replicates one side and complicates outer/existence semantics.
- **Aggressive spill:** protects memory; raises disk/object-store traffic and critical path.
- **Large in-memory build:** high probe throughput; increases failure, contention, and eviction risk.

## Failure Modes and Misconceptions

- **“A join key is unique because it usually is.”** only enforced snapshot-valid constraints permit collapsing duplicates.
- **“Null equals null in a hash bucket.”** ordinary SQL equality does not match them.
- **“Outer unmatched rows can stream immediately.”** completeness of possible matches must be established first.
- **“Both inputs say hash partitioned.”** key/type/hash/null/count/epoch compatibility is still required.
- **“Broadcast cost is small-side bytes.”** destinations, decoded memory, concurrency, and retries multiply it.
- **“Smaller row count is the build side.”** row width and hash amplification may reverse the choice.
- **“Repartition solves skew.”** equal hot keys still meet at one normal hash destination.
- **“Recursive grace hashing always converges.”** one equal heavy key remains indivisible.
- **“Merge join uses constant memory.”** sorting and duplicate runs can spill.
- **“Sorted inputs are compatible.”** comparison, direction, null order, ranges, and equality must agree.
- **“Bloom present means matching.”** false positives require exact evaluation.
- **“Bloom absent makes anti join output safe immediately.”** filter completeness/attempt and residual semantics matter.
- **“Salting a hot key is mechanical.”** replication and unmatched ownership must prevent lost or duplicate pairs.
- **“Adaptive change is a local flag.”** downstream distribution and attempts require a new safe epoch.
- **“Task success means output is selected.”** speculative/retried attempts need commit selection.
- **“Input size predicts join cost.”** output multiplicity, skew, memory, spill, and dependency calls can dominate.
- **“Same plan text means same performance.”** data, statistics, resources, and concurrency change outcomes.
- **“A fast join is correct.”** semantic and distributed fault tests precede benchmarks.

## Worked Examples

### Example 1

Build has three rows for account 7 and probe has two. An inner equality join emits six candidate pairs before residual filtering. A hash map storing only the last build row emits two and silently undercounts.

### Example 2

Both sides contain a null key. Ordinary `=` emits no null/null pair; null-safe equality may emit one under its language contract. Hash bucket adjacency does not choose the semantics.

### Example 3

A left outer join probes a build partition that is still receiving exchange input. Emitting a null-extended row now is premature because a later build row may match. The task waits for the committed relevant build partition or uses a protocol that can retract, which batch SQL usually avoids.

### Example 4

A 100 MiB serialized dimension expands by 3.5 times in a hash table and broadcasts to 80 workers. Rough replicated build state is 28 GiB before buffers and concurrency. A per-worker 350 MiB check and fleet/concurrency budget are both required.

### Example 5

Two 4 TiB inputs lack compatible distribution. Repartition hash join moves both eligible projections and predicates, then builds the smaller partition locally. Projection/filter pushdown may save more than changing the local hash implementation.

### Example 6

Grace hash partition 12 remains 40 GiB after two different repartitions because one key owns almost all rows. More recursion adds I/O without reduction. Heavy-key split replicates the smaller matching run or the query is rejected if inherent output exceeds policy.

### Example 7

Two range-partitioned inputs use different collations for strings. Local merge can advance past values the other comparator considers equal. A canonical comparator/order exchange is required even though both inputs are “sorted.”

### Example 8

A Bloom dynamic filter reports key 42 may exist. The probe row cannot be emitted by a semi join until exact join evaluation finds a qualifying residual match. The filter saves scans on definite absence only.

### Example 9

Runtime materialization shows a planned broadcast side is 20 times its estimate. Before broadcast consumers start, the coordinator creates a repartition epoch and schedules compatible producers/consumers. It does not append repartition output to partially consumed broadcast tasks.

### Example 10

The fixture preserves duplicate multiplicity and ordinary SQL null behavior in a small hash inner join.

<!-- bijux-verify: {"id":"duplicate-preserving-hash-join","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"match_count=4\nmatches=((1, 'A', 'x'), (1, 'A', 'y'), (1, 'B', 'x'), (1, 'B', 'y'))\nnull_matches=0\n","stderr":""}} -->
```python
build = ((1, "A"), (1, "B"), (None, "N"), (2, "C"))
probe = ((1, "x"), (1, "y"), (None, "z"), (3, "w"))

buckets = {}
for key, value in build:
    if key is not None:
        buckets.setdefault(key, []).append(value)

matches = tuple(sorted(
    (key, build_value, probe_value)
    for key, probe_value in probe
    if key is not None
    for build_value in buckets.get(key, ())
))
print(f"match_count={len(matches)}")
print(f"matches={matches}")
print(f"null_matches={sum(1 for row in matches if row[0] is None)}")
```

Production code additionally handles composite types, residual predicates, all join types, vector batches, memory/spill, partition compatibility, attempts, and output commit.

## Cross-Program Connections

- **Algorithms:** hashing, external partitioning, sorting, merging, Bloom filters, sampling, heavy hitters, and dynamic programming shape joins.
- **Database systems:** bags, nulls, outer/semi/anti semantics, constraints, indexes, statistics, and join order define correctness.
- **Distributed systems:** exchange ownership, epochs, attempts, manifests, retries, backpressure, and partial failure define execution.
- **Data engineering:** partitions, bucketing, skew, spill, object storage, schemas, and large intermediate results determine cost.
- **Platform engineering:** worker memory, network, disks, scheduling, isolation, autoscaling, and observability constrain choices.
- **Reliability engineering:** broadcast guards, spill recovery, attempt commit, adaptive fallback, fault injection, canary, and rollback bound risk.
- **Security and governance:** snapshots, connector authority, sensitive keys/statistics, tenant limits, and audit constrain planning and telemetry.
- **Performance engineering:** cardinality, bytes, amplification, critical path, output multiplicity, skew, and concurrency explain runtime.

## References

1. Trino. [Optimizer.](https://trino.io/docs/current/optimizer.html) Current statistics, cost-based optimization, join enumeration/distribution, pushdown, and dynamic filtering overview.
2. Trino. [Optimizer Properties.](https://trino.io/docs/current/admin/properties-optimizer.html) Current join reordering, broadcast limits, partitioned/broadcast distribution, colocated joins, spill, and optimizer controls.
3. Trino. [SELECT.](https://trino.io/docs/current/sql/select.html) Current join syntax and inner, outer, cross, lateral, and `UNNEST` semantics.
4. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current broadcast/shuffle join hints, partitioning, adaptive conversion, and skew join behavior.
5. Apache Spark. [JOIN.](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-join.html) Current inner, outer, semi, anti, cross, and join-criteria syntax.
6. PostgreSQL. [Using EXPLAIN.](https://www.postgresql.org/docs/current/using-explain.html) Current nested-loop, hash, merge join, estimates, actuals, sort, and instrumentation examples.
7. PostgreSQL. [Planner/Optimizer.](https://www.postgresql.org/docs/current/planner-optimizer.html) Current path generation, cheapest paths, plan creation, and join-order search overview.
8. Apache DataFusion. [EXPLAIN Usage.](https://datafusion.apache.org/user-guide/explain-usage.html) Current logical/physical plans, optimizer passes, repartitioning, statistics, and operator metrics.
9. DuckDB. [EXPLAIN: Inspect Query Plans.](https://duckdb.org/docs/stable/guides/meta/explain.html) Current physical plan and analyzed runtime inspection, including hash joins.
10. Apache Calcite. [Relational Algebra.](https://calcite.apache.org/docs/algebra.html) Current logical join types, correlation, hints, traits, and planner expression concepts.
11. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary account of distributed hash/merge joins, repartitioning, broadcast, sorting, and production execution.
12. Meta Engineering. [Presto: Interacting with Petabytes of Data at Facebook.](https://engineering.fb.com/2013/11/06/core-infra/presto-interacting-with-petabytes-of-data-at-facebook/) Primary coordinator/worker, stage/task/operator, exchange, and pipelined query architecture account.
13. Dean and Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters.](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) Primary partition, shuffle, sort, locality, backup-task, and failure-recovery account relevant to repartitioned joins.

## Exercises

### Exercise 1

Compute inner-join output multiplicity for keys with counts `R: {a:3,b:2,null:4}` and `S: {a:5,b:0,null:6}` under ordinary equality and null-safe equality. State assumptions.

### Exercise 2

Design a distributed full outer hash join. Specify partition compatibility, duplicate/null behavior, match tracking, unmatched ownership, spill, attempts, and output commit.

### Exercise 3

Compare broadcast hash, repartition hash, co-located hash, and merge join for a 10 TiB fact input and uncertain 80 MiB dimension. Include network, memory, sort, skew, recovery, and adaptive guards.

### Exercise 4

Design grace hash join for a 120 GiB build side with 8 GiB governed memory per task. Cover fan-out, memory amplification, aligned probe spill, recursive skew detection, integrity, and failure.

### Exercise 5

Design a join validation campaign for a new adaptive skew algorithm. Include semantics, distributions, statistics, failures, security, performance, canarying, and rollback.

## Answers to the Exercises

### Answer 1

Under ordinary equality, key `a` contributes $3\times5=15$, `b` contributes $2\times0=0$, and null contributes zero, for 15 pairs before residual filtering. Under a null-safe equality that treats all null keys equal, null contributes $4\times6=24$, for 39 total. This assumes bags, one scalar key, no residual predicate, and no additional nonmatching rows that affect outer semantics. It does not imply those outputs fit memory or one partition.

### Answer 2

Hash-repartition both sides under identical key/type/hash/null/count/epoch contracts. For ordinary equality, keep null-key rows out of match buckets but retain them for preservation. Each local task stores every build duplicate with a visited flag, probes every duplicate, emits every residual-qualified pair once, marks matched build rows, emits each unmatched preserved probe row once after its relevant build partition is complete, then emits unvisited build rows after the selected probe partition completes. Spill aligned build/probe partitions with complete checksummed manifests and recurse consistently. Null-safe equality instead uses a canonical null bucket. Task attempts are isolated; downstream selects one complete output attempt per logical join partition, so losing attempts cannot duplicate matched or unmatched rows.

### Answer 3

Broadcast avoids moving 10 TiB but replicates the dimension's actual serialized and decoded hash state to every worker; guard measured materialized bytes, amplification, destinations, concurrent joins, and headroom. Repartition moves eligible projections of both sides and tolerates a large dimension but incurs major network/spill and hot-key risk. Co-location wins only with exact current compatible buckets and snapshots. Merge is attractive if both inputs already share compatible distribution/order or if range predicates require it; otherwise two distributed sorts may dominate. Use fresh row/byte/distinct/heavy-key statistics and uncertainty. Materialize the dimension at a safe boundary, broadcast below hard per-worker and fleet limits, otherwise create a new repartition epoch before consumers start. Recovery favors committed exchanges; pipelining widens restart.

### Answer 4

Estimate decoded hash amplification and reserve buffers/spill headroom, so target build partitions are materially below 8 GiB rather than simply choosing $120/8=15$. Select a fan-out from upper-size/skew evidence, hash both build and probe into identical partitions, and commit checksummed side/partition/attempt manifests. Process fitting partitions; recursively repartition oversized pairs with a different hash/bit range while measuring reduction. If one key prevents reduction, stop recursion and invoke heavy-key handling, merge/external representation, or bounded failure. Bound writers, files, disk/object quota, and concurrent partitions. On failure, expose only selected complete attempts, reuse durable committed spill where compatible, clean losing data after recovery retention, and report bytes, passes, skew, and integrity.

### Answer 5

Differentially compare adaptive skew, ordinary repartition hash, merge, and a trusted reference across inner/outer/full/semi/anti and null-safe variants. Generate empty inputs, duplicates, null/composite keys, residuals, heavy keys on either/both sides, inherent huge output, uniqueness metadata, incompatible hashes/counts, and stale estimates. Metamorphically vary input order, partition count, worker count, and retry without changing results. Inject spill exhaustion/corruption, producer/consumer loss, duplicate attempts, delayed dynamic filters, adaptation cancellation, and coordinator failover. Assert one selected output, exact multiplicity/unmatched ownership, memory/retry bounds, snapshot/security policy, and redacted telemetry. Measure network, replication, memory, spill, task tail, output rate, recovery, fairness, and cost. Shadow choices, canary bounded queries, freeze on correctness/security/resource-bound regression, and roll back by plan/exchange epoch while retaining required manifests.
