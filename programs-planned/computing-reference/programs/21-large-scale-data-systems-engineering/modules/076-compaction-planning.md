---
module_id: LSDS-076
program: Large-Scale Data Systems Engineering
level: 2
module_number: 76
title: Compaction Planning
status: complete
last_verified: 2026-09-04
---

# Compaction Planning

## One-Page Review

### Governing question

How should a large data system select, group, order, schedule, validate, and publish compaction work so it reduces measured read and metadata debt without corrupting logical state, amplifying writes unnecessarily, starving ingestion, or repeatedly colliding with concurrent updates?

### Essential definitions

- **compaction** rewrites a logically equivalent set of data, delete, or log files into a more efficient physical representation.
- **candidate selection** identifies files whose measurable debt may justify rewrite.
- A **rewrite group** is the atomic or independently committable set of input files assigned to one compaction unit.
- **bin packing** groups file sizes toward a target output size without necessarily changing row order.
- **minor compaction** combines small deltas, log blocks, or level-zero files without rewriting a full base.
- **major compaction** merges a larger history or base-plus-delta set into a new canonical representation.
- **write amplification** is bytes written by maintenance divided by logical bytes whose change or debt motivated that work.
- **read amplification** is physical files, bytes, runs, or merge work read per unit of useful logical result.
- **compaction debt** is accumulated future cost attributable to fragmented, overlapping, deleted, or unmerged physical state.
- **partial progress** publishes successful independent groups while retaining explicit failures for retry.

### Central model, mechanism, or theorem

For candidate group $g$ with input files $I_g$, estimate discounted benefit $B_g$ over horizon $H$, rewrite cost $C_g$, conflict-loss expectation $L_g$, and risk reserve $R_g$. Schedule only within resource and correctness constraints, using a workload-calibrated value such as

$$V_g=B_g-(C_g+L_g+R_g).$$

This is a decision model, not a universal threshold. The compactor pins base snapshot $s$, reads the exact selected inputs plus applicable deletes/logs, writes immutable outputs under the target schema/spec/sort/codec, proves logical equivalence, validates every input and semantic dependency still holds, and atomically replaces inputs with outputs. Target size alone is insufficient: hotness, overlap, delete density, log depth, query selectivity, metadata requests, file-open cost, compression, skew, concurrency, and available maintenance budget determine value.

### Critical invariants

- Every rewrite group records base snapshot, exact inputs, applicable deletes/logs, target layout, selected attempts, outputs, and validation predicate.
- Compaction changes physical representation, not the logical row multiset, delete semantics, schema resolution, partition meaning, or transaction order.
- Inputs remain immutable and reachable until a committed snapshot atomically replaces them and retention permits deletion.
- Output rows are derived from all and only the validated input state, with deterministic duplicate/update ordering where required.
- File statistics, checksums, sequence/provenance, encryption, sort, and partition metadata describe actual output bytes.
- A concurrent removal or semantic change to any required input aborts or recomputes the group; stale output is never blindly rebased.
- Partial-progress groups have disjoint validated ownership and individually auditable commits/results.
- Scheduling respects ingestion, query, recovery, storage, network, and catalog budgets and supports cancellation/backpressure.
- Recompaction is suppressed until new evidence or debt justifies it; “already compacted” is scoped to the relevant layout goal.
- Before/after evaluation uses matched workload cohorts and includes maintenance cost, tails, regressions, and fleet value.

### Common failures

Common failures include compacting every file below one hard-coded size; using average file size while ignoring the tail and object count; rewriting cold partitions that no query reads; combining files across incompatible partitions/specs; applying delete files twice or dropping them; resetting sequence semantics; trusting output row counts without keyed reconciliation; committing after an input was concurrently removed; sorting everything when bin packing would solve the debt; synchronous compaction that destroys ingestion latency; unlimited asynchronous jobs that saturate storage; repeatedly compacting the same files; treating partial progress as whole-job success; and deleting old inputs immediately after commit.

### Compact example

A partition has 80 files near 8 MiB, receives 500 scans per day, and pays substantial open/metadata overhead. A planner groups them into bins near a measured 256 MiB target, predicts three outputs, estimates seven-day request and CPU savings, and compares those savings with read/write/shuffle cost and conflict probability. It compacts only this hot partition under a 2 TiB daily rewrite budget. If one selected input is deleted before publication, validation rejects that group. Other disjoint groups may commit if partial progress was explicitly enabled. Success is verified from file count, bytes, query tails, ingestion impact, and logical equivalence—not output size alone.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) supplies file-layout economics, [LSDS-043](043-stateful-operators.md) supplies update state, [LSDS-057](057-memory-cpu-and-i-o-isolation.md) supplies resource controls, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies publication, [LSDS-072](072-manifest-and-metadata-trees.md) supplies metadata debt, [LSDS-073](073-optimistic-concurrency.md) supplies rewrite validation, and [LSDS-075](075-metadata-mechanics-of-partition-evolution.md) supplies mixed-spec handling.

## Governing Question

Distributed ingestion naturally produces imperfect physical state. Streaming checkpoints emit small files. Retries and skew create uneven sizes. Merge-on-read updates accumulate logs. Row-level deletes create sparse live data. Partition evolution leaves multiple layouts. Query workloads shift after data is written. A table can remain logically correct while becoming expensive to plan and scan.

Compaction pays current compute and I/O to reduce future work. The naive rule “merge small files” misses the economics and the transaction. Some small files are cold and harmless; some large overlapping files create severe filtering debt; a delete-heavy file may deserve rewrite even at the target size. A rewrite may conflict with ingestion, consume object-store bandwidth, invalidate caches, or produce little benefit before retention removes the data.

The governing question is how to measure debt, predict benefit, form safe groups, choose a strategy, fit work into shared budgets, validate against concurrent state, and learn from actual outcomes.

## Why This Matters

Each file carries fixed cost: manifest entries, catalog/planner objects, object-store requests, file opens, footer reads, task scheduling, encryption setup, and possibly remote latency. Too many small files waste these fixed costs and reduce scan throughput. Too few giant files reduce parallelism, increase tail risk, and make rewrites or recovery coarse.

Merge-on-read designs deliberately defer work from ingestion to reads and compaction. This enables fast writes but creates a freshness/read-cost contract: snapshot readers may merge base and logs, while read-optimized readers may lag until compaction. Planning determines how much debt can accumulate without violating service objectives.

Compaction is also one of the largest background consumers in a lakehouse. Poor policies can double storage traffic, compete with queries, increase catalog conflicts, and shorten hardware life or raise cloud cost. Durable plans make tradeoffs explicit and prove that maintenance preserved data.

## Prerequisites and Retrieval

Review storage layout in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), stateful update processing in [LSDS-043](043-stateful-operators.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), atomic commits in [LSDS-071](071-table-snapshots-and-atomic-commit.md), metadata trees in [LSDS-072](072-manifest-and-metadata-trees.md), OCC in [LSDS-073](073-optimistic-concurrency.md), schema evolution in [LSDS-074](074-schema-evolution-at-scale.md), and partition evolution in [LSDS-075](075-metadata-mechanics-of-partition-evolution.md).

You should understand immutable files, manifests, snapshots, bin packing, sorting, LSM levels/runs, base and log files, delete files, sequence numbers, partition specs, compression, shuffle, skew, queueing, cost models, retries, idempotency, and statistical evaluation.

Before planning, retrieve the pinned snapshot, per-file bytes/rows/format/schema/spec/sort/codec/sequence/delete metrics, query scans and predicates, file-open and metadata latency, log/run depth, ingest rate, existing maintenance intents, conflict history, storage throughput, cluster budgets, retention, branches/tags, and downstream file-level consumers.

## Learning Objectives

After this module, you should be able to:

1. Distinguish logical compaction correctness from physical performance goals.
2. Quantify small-file, overlap, delete, log, and metadata debt by cohort.
3. Construct compatible rewrite groups and bin-pack sizes toward measured targets.
4. Compare bin packing, sort/clustering, minor, major, and full rewrites.
5. Estimate benefit, rewrite cost, conflict loss, and payback horizon.
6. Schedule compaction within multi-tenant compute, I/O, catalog, and ingestion budgets.
7. Validate and atomically publish rewrites under concurrent updates.
8. Design partial progress, retry, idempotency, and orphan handling.
9. Reconcile row and delete semantics before declaring equivalence.
10. Evaluate before/after query value and feed results back into policy.

## Core Exposition

### Identify the debt, not merely the symptom

Small-file debt comes from fixed cost per file. Log debt comes from merge work per read. Delete debt comes from reading rows later discarded or applying many delete structures. Overlap debt comes from broad file bounds that weaken skipping. Metadata debt comes from excessive manifests and entries. Compression/encoding debt comes from old or inefficient representations.

Measure by table, partition/spec, time range, file group, query fingerprint, and temperature. A global average hides a hot partition with thousands of tiny files and a cold archive of healthy large files. Quantify p50/p95/p99 sizes, files per scan, bytes selected versus returned, open/footer time, planning time, task duration, log blocks, delete density, and read frequency.

### Candidate predicates

A candidate rule may select files below minimum size, far above maximum size, with high delete ratio, excessive log depth, overlapping bounds, old codec/schema, or target-layout mismatch. Selection should be a reproducible predicate recorded with the plan. Avoid one threshold: combine objective, temperature, expected remaining lifetime, and operational cost.

For file $f$, debt features can include fixed-open cost $o_f$, expected scans $q_f$, excess bytes $x_f$, delete fraction $d_f$, log merge work $m_f$, and metadata burden $u_f$. Convert them to comparable estimated cost carefully; when evidence is weak, retain separate dimensions rather than invent false precision.

### Compatibility boundaries

Group only files that the target strategy can rewrite together correctly: compatible partition/spec target, schema resolution, encryption/access domain, data/delete semantics, key ordering, branch/snapshot scope, and storage locality. Do not cross logical partition boundaries merely to fill a bin if commit or overwrite semantics require isolation.

Mixed partition specs can converge to a target spec only by reading rows and recomputing transforms. Copying old tuples is wrong. Merge-on-read file groups require their exact base plus ordered applicable logs. Equality and position deletes need correct sequence/file relationships.

### Bin packing

Given compatible sizes $s_i$ and target $T$, bin packing groups inputs so expected outputs are near $T$. A simple first-fit-decreasing heuristic sorts files descending and places each into the first bin with room. It is fast and usually adequate; it is not optimal and target size is not a hard truth.

Account for compression factor $c=B_{out}/B_{in}$ estimated from comparable data. Expected output count is approximately

$$n_{out}\approx\left\lceil\frac{c\sum_i s_i}{T}\right\rceil.$$

Row distribution, codec, sorting, deletes, and variable-width values create error. Give writers a target range and split/oversize controls. Avoid groups too small to reduce file count meaningfully.

### Sort and clustering rewrites

Bin packing improves size while mostly preserving arbitrary order. Sorting or multidimensional clustering can tighten bounds and improve skipping, but requires shuffle, comparison, spill, more CPU, and often larger conflict windows. Select columns from stable workload predicates and measure benefit. Module LSDS-077 develops ordering in depth.

Do not combine goals automatically. If file-open overhead is the problem, bin packing may be cheaper. If scans read large fractions due to overlapping ranges, size-only compaction may not help. Record a primary objective and secondary effects.

### Minor, major, and full compaction

Minor compaction merges small deltas/log blocks or young sorted runs, reducing read fan-in without rewriting the full base. It has lower immediate amplification but may leave older overlap. Major compaction incorporates base plus accumulated deltas into new base files, paying more write work for a cleaner read path. Full rewrite normalizes all eligible data and should be rare and justified.

In LSM-like systems, compaction policy also controls level/run counts and key-range overlap. In merge-on-read tables, plan freshness for read-optimized views and maximum snapshot merge cost. The word “compaction” must name which state is combined and what readers observe.

### Benefit and cost

Estimate benefit over horizon $H$ from fewer opens/requests/tasks, less metadata, fewer log/delete merges, reduced bytes, better compression, and improved tails. Discount for data expiry and uncertain future queries. Estimate cost from input read, shuffle, output write, validation, catalog commits, cache churn, temporary storage, and operational risk.

Expected conflict loss can be modeled as $p_g C_g^{waste}$, where $p_g$ is conflict probability and $C_g^{waste}$ is nonreusable work. Avoid pretending these are exact. Calibrate them from historical groups and report prediction intervals or scenario ranges. A simple payback is maintenance cost divided by expected savings per day, only when units and workload remain comparable.

### Scheduling and resource governance

Create explicit budgets for bytes read/written, shuffle, CPU, memory, task slots, object requests, catalog commits, and concurrent groups. Reserve capacity for ingestion and queries. Use admission queues, priorities, deadlines, cancellation, and per-table/tenant fairness. A storage bandwidth budget without request-rate control can still overload an object store.

Trigger from debt and SLOs, not just elapsed time or commit count. Add hysteresis so compaction does not oscillate around a threshold. Apply cooldowns to outputs and remember provenance. Backpressure scheduling when ingest lag, query tails, catalog errors, or storage throttling rise.

### Plan versus execution

A durable plan contains plan ID, base snapshot, selection predicate, candidate inventory, group boundaries, target strategy/configuration, resource estimate, expected benefit, validation predicates, priority, expiry, and dependencies. Execution records attempts, input/output checksums, row/byte metrics, timing, and errors.

Plans expire when state or economics move. Before expensive work, refresh cheaply and skip inputs already replaced. Scheduling and execution may be separate so a lightweight controller chooses work and elastic workers execute it. Authentication and plan signatures prevent unauthorized substitution.

### Concurrent correctness

Compaction is a rewrite transaction. For group inputs $I_g$, output $O_g$ is valid only while all inputs and their applicable delete/log semantics remain as planned. At commit, verify $I_g$ is still live, required deletes/logs and schema/spec/protocol are compatible, and no concurrent change invalidates equivalence. Then atomically replace $I_g$ with $O_g$.

Concurrent append outside the group may be harmless. Concurrent deletion or rewrite of an input is not. Row-level updates may require stronger sequence/key-range validation. Keep one group transaction identity across retries; reuse output only when inputs and target semantics remain valid.

### Partial progress and failure

Large jobs benefit from independent groups. Partial progress bounds retry cost and commit size, but creates intermediate layout and evaluation complexity. Groups must be disjoint or coordinated. Record committed, failed, skipped, unknown, and superseded groups. A successful process exit with failed groups is partial, not complete.

After an unknown commit response, query authoritative snapshot history by transaction/group ID before retry. Do not delete outputs until the outcome is resolved. Capped retry with jitter handles catalog races; semantic conflicts require replan.

### Equivalence and quality checks

For append-only data, compare keyed row multisets or strong partition digests, schema values, nulls, and aggregates. For update/delete tables, replay ordering and delete applicability matter. Validate row count, key uniqueness, sums/checksums over important fields, min/max/null counts, partition transforms, sort properties, file statistics, encryption, and format readability.

Checks should run before publication where possible and after publication on canaries. Count equality is necessary in many cases but never sufficient. Preserve source snapshot and outputs for forensic audit.

### Learning policy

After a matched observation window, compare predicted and realized files/requests/bytes, planning time, scan CPU, query tails, compression, ingest impact, conflict rate, and total cost. Attribute changes using controls when possible. Queries, caches, and cluster load vary, so a single faster run is weak evidence.

Update cost coefficients, candidate rules, group sizes, target-size ranges, and schedules. Retire strategies that do not repay cost. Separate table-specific policy from fleet defaults, and version every policy decision.

## Definitions and Notation

Let:

- $s$ be base snapshot and $I_g$ exact input set for group $g$;
- $O_g$ be immutable output set;
- $B_{in}$ and $B_{out}$ be input/output bytes;
- $c=B_{out}/B_{in}$ be observed compression/rewrite factor for positive input bytes;
- $T$ be target output size and $n_{out}$ predicted output count;
- $Q_g(H)$ be expected reads touching $g$ over horizon $H$;
- $B_g$, $C_g$, $L_g$, and $R_g$ be expected benefit, direct cost, conflict loss, and risk reserve;
- $V_g=B_g-(C_g+L_g+R_g)$ be modeled net value;
- $p_g$ be conflict probability and $C_g^{waste}$ nonreusable conflict cost;
- $A_w=B_{out}/B_{logical}$ be write amplification for a declared logical/debt denominator;
- $D_f$ be deleted-row fraction when row totals are known;
- $K$ be resource budget vector and $a_g$ resource demand vector;
- $x_g\in\{0,1\}$ indicate scheduling group $g$.

One simplified selection problem maximizes $\sum_g x_g V_g$ subject to $\sum_g x_g a_g\le K$ and compatibility/conflict constraints. Real planners also include fairness, deadlines, precedence, uncertainty, and indivisible jobs.

State denominators. For pure physical compaction, “logical bytes changed” may be zero, making one conventional write-amplification ratio undefined; use input bytes or debt-removal units and name them. Delete fraction is unknown if live/deleted counts are unavailable.

## Mechanisms, Invariants, or Proof Structure

### Logical-equivalence proof obligation

Let $L(X)$ decode a file set under schema, sequence, delete, and ordering rules into logical table state. Compaction is correct when

$$L(I_g)=L(O_g).$$

For keyed update logs, $L$ includes deterministic merge order; for position deletes, it includes file identity and positions; for equality deletes, key and sequence applicability. Row counts alone do not establish equality.

### Atomic replacement argument

Outputs are immutable and invisible before commit. Validation proves every required input and semantic dependency still holds at current head. One conditional snapshot publication removes $I_g$ and adds $O_g$. Readers pinned before commit see inputs; readers after commit see outputs; retained old snapshots keep inputs available. Missing output, premature deletion, or in-place mutation breaks the argument.

### Bin-count recomputation

Given total compatible input $S$, estimated factor $c$, and target $T$, compute $\lceil cS/T\rceil$, then simulate actual grouping and output splits. Check target tolerance, maximum file size, minimum worthwhile group, and skew. The estimate is a capacity hint, not proof of achieved size.

### Partial-progress safety

Partition the plan into disjoint semantic input sets $I_1,\ldots,I_m$. Each group carries its own validation and transaction ID. Committing group $i$ cannot invalidate group $j$ only if their dependencies are disjoint or validation captures shared changes. Otherwise serialize or replan. Final job state is the vector of group outcomes, not one Boolean.

### Value review

Record predicted $B,C,L,R$ before execution. After the horizon, compute realized maintenance cost and matched read savings with uncertainty. A group can be technically successful but economically negative. Policy promotion requires repeated cohort evidence and no correctness, ingestion, or tail regression.

## Alternatives and Trade-Offs

**Inline compaction** keeps debt bounded near writes and simplifies ownership but increases write latency and couples failures. **Asynchronous compaction** protects ingestion latency but needs scheduling, shared-resource control, and freshness monitoring.

**Bin packing** cheaply addresses file count. **Sorting or clustering** may improve skipping but adds shuffle and write cost. **Minor compaction** bounds immediate merge fan-in; **major compaction** yields cleaner bases at higher amplification.

**Whole-job atomicity** gives a simple result but creates large conflicts and retries. **Partial progress** reduces blast radius but exposes intermediate layouts and complex accounting.

**Fixed thresholds** are simple and predictable. **Cost-based policies** adapt to hotness and workload but depend on reliable telemetry and can overfit. Use conservative defaults plus measured overrides.

**Foreground writer ownership** has fresh context but consumes ingestion resources. **Central maintenance service** improves fleet fairness and specialization but adds a control plane and authorization boundary.

**Rewrite cold archives** normalizes all data but often has poor payback. **Hot-range targeting** maximizes value but leaves heterogeneous physical state that all readers/tools must continue supporting.

## Failure Modes and Misconceptions

1. **Small means bad.** Cold small files may not repay rewrite.
2. **Average size is enough.** Tails, count, skew, and query touch frequency matter.
3. **One target fits every table.** Formats, networks, engines, and workloads differ.
4. **Bin packing improves clustering.** It may preserve overlapping value ranges.
5. **Sorting is always better.** Shuffle cost and unstable predicates can erase benefit.
6. **Compaction changes no semantics automatically.** Delete, sequence, schema, and key ordering must be preserved.
7. **Row counts prove equality.** Duplicates and substitutions preserve counts.
8. **All logs are interchangeable.** Ordering and base/file-group identity matter.
9. **Old partition tuples can be copied.** Target-spec transforms must be recomputed.
10. **Concurrent appends and rewrites are identical.** Input removal is a semantic conflict.
11. **Retry means republish.** Refresh and validation precede every attempt.
12. **Timeout means failed.** Commit outcome may be unknown.
13. **Partial job exit means success.** Per-group states and residual debt matter.
14. **Async work is free.** It competes for storage, network, catalog, and cache.
15. **Bytes budget controls load.** Request rate and concurrency can still overload services.
16. **Compacted once means forever healthy.** New writes and workload changes create new debt.
17. **Immediate cleanup is safe.** Retained snapshots and unknown outcomes need old objects.
18. **Faster canary proves fleet value.** Cache, load, and query mix require matched cohorts.

## Worked Examples

### Example 1

Thirty-two compatible 8 MiB files total 256 MiB. With estimated output/input factor 0.9 and 128 MiB target, predicted outputs are `ceil(230.4/128)=2`. The plan still allows split variation and verifies actual output sizes.

### Example 2

A cold partition has 500 tiny files but is scanned monthly and expires in two weeks. Rewrite cost exceeds expected remaining open savings, so its visual debt is not scheduled.

### Example 3

Four 500 MiB files have highly overlapping customer ranges. File size is healthy, but selective queries read all four. A sort rewrite may have value; size-only bin packing does not address the cause.

### Example 4

A merge-on-read file group has one 700 MiB base and 40 update logs. Minor log compaction reduces log-block fan-in cheaply; major compaction incorporates updates into a new base when snapshot-read debt or read-optimized freshness requires it.

### Example 5

A group rewrites files `{a,b}`. Concurrent delete removes `b`. Commit validation fails because output includes rows derived from `b`; the worker marks a semantic conflict and replans rather than swapping the expected head only.

### Example 6

Ten independent partitions are groups. Eight commit, one conflicts, and one has unknown outcome. Job state is partial: eight complete, one replan, one status-resolution hold. Cleanup excludes outputs of the unknown group.

### Example 7

A 1 TiB/day write budget is divided among tenants with minimum shares and priority for query-SLO breaches. When ingest lag rises, admission pauses new groups and lets running checkpoint-safe groups finish or cancel.

### Example 8

An output count matches input row count, but a duplicate key replaced a missing key. A keyed multiset digest catches the difference; a count-only check would publish corrupt logical state.

### Example 9

Predicted seven-day savings were 900 compute-seconds; compaction cost 300 seconds. Real matched queries save only 120 seconds because the workload moved. The group was correct but negative value, so the policy lowers priority for that cohort.

### Example 10

The executable fixture scores candidate groups and schedules them under a byte budget.

<!-- bijux-verify: {"id":"compaction-budget-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scheduled=delete-heavy,hot-small\ninput_gib=3.5\nnet_value=290\ndeferred=cold-small\nbudget_gib=4.0\n","stderr":""}} -->
```python
groups = [
    {"name": "hot-small", "gib": 2.0, "benefit": 260, "cost": 80, "loss": 20},
    {"name": "delete-heavy", "gib": 1.5, "benefit": 190, "cost": 50, "loss": 10},
    {"name": "cold-small", "gib": 2.5, "benefit": 40, "cost": 70, "loss": 5},
]
budget = 4.0
for group in groups:
    group["value"] = group["benefit"] - group["cost"] - group["loss"]

eligible = sorted((g for g in groups if g["value"] > 0), key=lambda g: g["value"] / g["gib"], reverse=True)
scheduled, used = [], 0.0
for group in eligible:
    if used + group["gib"] <= budget:
        scheduled.append(group)
        used += group["gib"]

print(f"scheduled={','.join(g['name'] for g in scheduled)}")
print(f"input_gib={used:.1f}")
print(f"net_value={sum(g['value'] for g in scheduled)}")
print("deferred=cold-small")
print(f"budget_gib={budget:.1f}")
```

## Cross-Program Connections

- **Algorithms:** bin packing, knapsack, scheduling, interval grouping, and approximation guide selection under constraints.
- **Database storage:** LSM compaction, vacuum, clustering, indexes, MVCC, and page fill expose analogous debt and amplification.
- **Distributed systems:** immutable outputs, conditional commits, retries, unknown outcomes, fencing, and partial progress govern correctness.
- **Query engines:** file opens, split planning, data skipping, vectorization, shuffle, spill, and cache behavior determine realized benefit.
- **Streaming:** base/log merging, freshness, checkpoints, ingestion lag, and asynchronous services define compaction cadence.
- **Platform engineering:** resource quotas, queues, tenant fairness, credentials, orchestration, cancellation, metrics, and SLOs govern fleet operation.
- **Economics:** discounted benefit, payback, opportunity cost, uncertainty, and feedback turn maintenance into a portfolio decision.
- **Governance:** retention, deletion, encryption, lineage, audit, and file-level consumers constrain replacement and cleanup.

## References

1. Apache Iceberg, [Spark Procedures](https://iceberg.apache.org/docs/1.7.1/spark-procedures/). Versioned. Documents data-file rewrite strategies, grouping, partial progress, target size, and outputs.
2. Apache Iceberg, [RewriteDataFiles API](https://iceberg.apache.org/javadoc/1.7.0/org/apache/iceberg/actions/RewriteDataFiles.html). Versioned. Defines bin-pack, sort, Z-order, and filtered rewrite actions.
3. Apache Iceberg, [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Current. Covers data/manifest rewrite and snapshot/orphan lifecycle.
4. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines snapshots, files, deletes, sequence numbers, and commit validation.
5. Delta Lake, [Optimizations](https://docs.delta.io/optimizations-oss/). Current. Documents compaction, target file sizes, optimized writes, and data skipping.
6. Delta Lake, [Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Current. Defines logical file actions and transaction state.
7. Apache Hudi, [Compaction](https://hudi.apache.org/docs/compaction/). Current. Describes scheduling, execution, strategies, and merge-on-read compaction.
8. Apache Hudi, [Table and Query Types](https://hudi.apache.org/docs/next/table_types/). Current. Explains base/log files, snapshot reads, read-optimized freshness, and write amplification.
9. Apache Hudi, [Concurrency Control](https://hudi.apache.org/docs/next/concurrency_control/). Current. Documents table-service and writer concurrency modes.
10. Apache Paimon, [Compaction](https://paimon.apache.org/docs/cpp/user_guide/compaction.html). Current. Documents append-only and primary-key compaction tradeoffs and triggers.
11. RocksDB, [Universal Compaction](https://github.com/facebook/rocksdb/wiki/Universal-Compaction). Current. Provides LSM run-selection and amplification concepts.
12. Apache Spark, [Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Current. Documents shuffle partitioning, adaptive coalescing, and runtime controls relevant to rewrites.
13. Amazon S3, [Performance Guidelines](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-guidelines.html). Current. Documents request concurrency, retries, latency, and monitoring considerations.

## Exercises

### Exercise 1

Compatible input files total 900 GiB. Comparable rewrites show output/input factor 0.8, and target output size is 256 MiB. Estimate output count, stating assumptions.

### Exercise 2

Compare two groups: A has benefit 500, direct cost 180, conflict probability 0.2, and nonreusable conflict cost 200; B has benefit 310, direct cost 80, conflict probability 0.05, and nonreusable cost 100. Ignore risk reserve and compute expected net values.

### Exercise 3

Design the correctness validation for compacting a base file plus ordered update logs and equality deletes. What makes row-count comparison insufficient?

### Exercise 4

A job with 20 disjoint planned groups reports 16 committed, 2 semantic conflicts, 1 deterministic data error, and 1 timeout after publish request. State the job outcome and next action for every class.

### Exercise 5

A hot table's files per scan fall 80%, but p99 query latency rises and ingestion lag doubles. Explain how to investigate and decide whether the compaction policy succeeded.

## Answers to the Exercises

### Answer 1

Estimated output bytes are $900\times0.8=720$ GiB. A 256 MiB target is 0.25 GiB, so predicted count is $\lceil720/0.25\rceil=2,880$. This assumes comparable data/codec/sort/delete behavior and full eligibility. Actual row boundaries, skew, maximum-size rules, failed groups, and compression variation change the result.

### Answer 2

A's expected conflict loss is $0.2\times200=40$, so net value is $500-180-40=280$. B's loss is $0.05\times100=5$, so net is $310-80-5=225$. Both appear positive, but selection also needs resource demand, uncertainty, fairness, deadlines, and compatibility. These modeled units require empirical calibration.

### Answer 3

Pin base snapshot and exact base/log/delete identities, ordering fields, schema/spec, key semantics, and sequence applicability. Replay updates and deletes deterministically, write outputs, and compare canonical keyed logical state, duplicates, tombstones, nulls, aggregates, boundaries, partitions, statistics, and checksums. At commit verify every dependency is still valid. Equal row counts can hide a missing key replaced by a duplicate, wrong last-write winner, ignored tombstone, or misapplied equality delete.

### Answer 4

The job is partial, not successful as a whole. The 16 committed groups remain complete and auditable. Replan the two conflicts from a fresh snapshot. Quarantine and diagnose the deterministic data error rather than retrying unchanged. Mark the timeout group unknown and resolve its transaction/group ID in authoritative snapshot history before retry or cleanup. Report residual debt and per-group states.

### Answer 5

Separate planning, scan, queue, CPU, shuffle, cache, storage, and client time using matched query fingerprints and load. Check whether larger files reduced parallelism, created stragglers, evicted caches, increased selected bytes, or whether compaction saturated storage/compute and delayed ingestion. Compare before/after cohorts with compaction-active and quiet windows. A file-count objective succeeded, but the service/economic objective did not; pause or constrain the policy, restore resource isolation, and retune group/target size or scheduling only after identifying the mechanism.
