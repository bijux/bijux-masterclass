---
module_id: LSDS-061
program: Large-Scale Data Systems Engineering
level: 2
module_number: 61
title: Distributed Logical and Physical Plans
status: complete
last_verified: 2026-09-04
---

# Distributed Logical and Physical Plans

## One-Page Review

### Governing question

How should a distributed query engine transform a declarative request into typed logical operators, choose executable physical algorithms and data properties, divide the result into network-connected fragments, and prove that optimization preserves semantics under failures, skew, and changing runtime evidence?

### Essential definitions

- A **logical plan** states relational meaning through operators such as scan, filter, project, join, aggregate, and sort without fully committing to execution algorithms.
- A **physical plan** selects algorithms, layouts, partition counts, execution modes, and resource-sensitive implementations.
- A **physical property** describes required or delivered distribution, ordering, grouping, uniqueness, locality, or execution convention.
- An **exchange** moves or repartitions data and usually forms a boundary between independently scheduled fragments or stages.
- A **fragment** is a connected physical-plan region executable under one placement/distribution contract.
- A **memo** stores equivalent expressions and their properties so an optimizer can explore alternatives without materializing every plan tree.
- **cardinality estimation** predicts row counts; **cost estimation** maps a candidate and estimates to comparable resource/latency quantities.
- **predicate/projection pushdown** delegates filtering or column selection toward a data source when connector semantics support it.
- A **blocking operator** must receive substantial or complete input before producing its final output; a **pipeline breaker** separates streaming pipelines.
- An **adaptive plan change** replaces a not-yet-fixed physical choice using runtime evidence while preserving an explicit semantic and recovery boundary.

### Central model, mechanism, or theorem

Let logical expression $e$ require physical properties $p$. An optimizer seeks

$$P^*(e,p)=\arg\min_{P\in\mathcal{I}(e,p)} C(P\mid S,R),$$

where $\mathcal{I}(e,p)$ contains physical implementations semantically equivalent to $e$ and satisfying $p$, $S$ is statistical evidence, and $R$ is resource/topology context. Child property requirements are derived from each physical operator. If a child does not deliver them, an enforcer such as hash exchange, broadcast, gather, or sort is inserted. This is conditional optimization: correctness depends on equivalence and property proofs; optimality is only relative to enumerated candidates, cost model, statistics, and current context.

### Critical invariants

- Parsing, binding, analysis, logical rewrite, physical selection, fragmentation, scheduling, and execution remain distinguishable stages.
- Every expression has resolved types, attributes, nullability, scope, correlation, and function semantics before unsafe rewrites.
- Rewrites preserve bag/set semantics, three-valued logic, ordering obligations, determinism, security filters, and side-effect boundaries.
- Every physical operator declares required child properties and delivered output properties.
- Join or grouped-aggregation peers meet on compatible partitioning, key equality, hash/range semantics, and partition counts.
- Exchange serialization preserves types, null representation, collation, time-zone/encoding rules, and stable row ownership.
- Fragment retries do not duplicate externally visible effects or combine incompatible attempt outputs.
- Statistics and costs carry provenance, timestamp, uncertainty, and model/version identity.
- Adaptive changes occur only at declared safe boundaries and preserve completed-work and recovery contracts.
- Explain, runtime metrics, and incident evidence identify the same logical, physical, fragment, operator, and attempt lineage.

### Common failures

Common failures include calling parsed syntax a logical plan; losing aliases or correlation during rewrite; pushing a filter across an outer join incorrectly; assuming SQL rows are ordered without a final ordering contract; joining locally when inputs are partitioned on different keys; broadcasting underestimated data; treating exchanges as free; using stale uniform statistics under skew; confusing estimated rows with actual rows; trusting connector pushdown despite semantic mismatch; changing partition counts without compatible hash ownership; retrying a side-effecting sink; comparing plan text whose generated IDs changed; and declaring one plan globally optimal when the search space, cost model, statistics, or runtime resources were incomplete.

### Compact example

Customers are hash-partitioned by `customer_id`, while orders arrive in arbitrary source partitions. A local per-partition join returns no rows even though both customer IDs exist, because matching rows are on different workers. Hash-repartitioning orders by `customer_id` establishes co-partitioning; then local joins return both results. The exchange is not merely a performance decision—it supplies a physical property required for correctness of that local algorithm.

### Connections

[LSDS-031](031-shuffle-architecture.md) defines exchange partition ownership, [LSDS-041](041-logs-as-distributed-input.md) establishes durable distributed inputs, [LSDS-054](054-data-local-task-placement.md) connects fragments to placement, [LSDS-055](055-work-stealing-and-speculation.md) constrains attempts, and [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md) traces scheduler delay after plans become resource demand.

## Governing Question

SQL and other declarative languages describe results, not machine steps. A distributed engine must resolve names and types, establish logical semantics, rewrite equivalent expressions, choose scans and join/aggregate algorithms, decide where data moves, divide work into fragments, assign parallelism, and create a recoverable execution graph. Each choice affects correctness, latency, memory, network, scheduling, and failure recovery.

The words “query plan” often collapse several artifacts. An analyzed logical plan differs from an optimized logical plan; a physical operator tree differs from distributed fragments; scheduled tasks and runtime adaptive replacements differ again. Debugging becomes unreliable when an `EXPLAIN` captured before execution is treated as the exact attempt graph that ran.

The governing question is how to give each representation a precise contract, prove semantic equivalence and physical-property satisfaction, expose uncertainty, and retain lineage through distribution and adaptation so operators can understand both chosen and rejected alternatives.

## Why This Matters

A logically valid query can become wrong if a rewrite mishandles nulls, nondeterminism, correlation, security policy, or outer-join preservation. A semantically correct physical tree can become wrong when local joins receive incompatible partitions, partial aggregates are merged with the wrong algebra, exchange attempts are duplicated, or range boundaries disagree. Distribution turns “implementation detail” into a correctness contract.

Performance also depends on representation. Join order changes intermediate size; broadcast avoids repartition but risks memory failure; partitioned aggregation scales but shuffles; pushdown saves bytes but delegates semantics; vectorization raises throughput but changes memory shape; materialization improves retry isolation but adds I/O. Cardinality error early in a tree compounds into bad algorithms, parallelism, and resource requests.

Plans are also the bridge between query engineering and platform operation. They explain why stages exist, where exchanges occur, what data volume moves, why memory is requested, which fragments can retry, and which nodes need locality. A durable plan lineage lets runtime measurements improve statistics and allows regressions to be attributed to data, configuration, software, or resource changes.

## Prerequisites and Retrieval

Review exchange ownership in [LSDS-031](031-shuffle-architecture.md), durable distributed inputs in [LSDS-041](041-logs-as-distributed-input.md), streaming recovery boundaries in [LSDS-047](047-checkpoint-barriers.md), resource models in [LSDS-051](051-cluster-resource-models.md), placement in [LSDS-054](054-data-local-task-placement.md), attempt semantics in [LSDS-055](055-work-stealing-and-speculation.md), and scheduler diagnosis in [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md).

You should understand relational algebra, SQL bags and nulls, schemas and types, joins and aggregation, sorting, hashing, partitioning, iterators or vector batches, DAGs, statistics, dynamic programming, networks, storage scans, retries, and distributed failure.

## Learning Objectives

After this module, you should be able to:

1. distinguish parse, bind, analyze, logical, optimized logical, physical, fragmented, scheduled, and runtime plans;
2. state semantic obligations for relational rewrites under bags, nulls, order, correlation, and nondeterminism;
3. model required and delivered distribution, ordering, grouping, locality, and execution properties;
4. insert exchanges or sorts when child properties do not satisfy an operator;
5. explain join, aggregation, scan, and materialization alternatives and their resource trade-offs;
6. relate cardinality/statistics uncertainty to cost, memory, parallelism, and algorithm choice;
7. divide a physical plan into fragments and define exchange and retry contracts;
8. constrain connector pushdown and adaptive execution by semantic capability and safe boundaries;
9. connect plan lineage to explain output, runtime metrics, regressions, and scheduler demand; and
10. validate plan correctness and performance with differential, metamorphic, fault, and workload testing.

## Core Exposition

### Separate the plan lifecycle

Parsing produces syntax. Binding resolves catalogs, columns, functions, and scopes. Analysis establishes types, coercions, nullability, grouping validity, correlation, and privileges. Logical rewriting applies semantic transformations. Physical planning selects implementations and properties. Fragmentation inserts network boundaries and execution topology. Scheduling creates attempts on resources. Runtime adaptation may replace future work.

Persist identities and generations at every transition. A textual SQL digest is not enough because session settings, catalog snapshots, function versions, roles, and parameter types affect meaning. Conversely, generated operator IDs alone make equivalent plans impossible to compare across compilations.

### Give logical operators explicit semantics

A logical scan identifies a relation snapshot and projected attributes. Filter applies a three-valued predicate. Project computes named expressions. Join declares join type and condition. Aggregate declares grouping keys and algebraic functions. Sort declares keys, direction, null placement, and scope. Limit without a total order selects an unspecified subset.

Use stable attribute identities rather than names alone; aliases and duplicate column names otherwise collide. Record whether duplicates are preserved, whether expressions are deterministic, and whether evaluation can fail or cause effects. These facts constrain equivalence rules.

### Preserve null and outer-join behavior

Classical two-valued relational identities do not automatically hold under SQL nulls and bags. Moving a predicate from above a left outer join into its right input can retain rows that the original post-join predicate removed, or remove null-extended rows depending on predicate null rejection.

Classify predicates by referenced attributes, null behavior, determinism, and failure semantics. Prove the rewrite for the exact join type. Test empty inputs, null keys, duplicate rows, and predicates yielding true, false, unknown, or error.

### Preserve bags, order, and determinism

SQL commonly uses bag semantics: duplicates matter unless an operator removes them. Projection or join rewrites that silently assume sets can change multiplicity. Ordering exists only where the language or an internal required property declares it; storage or partition arrival order is not a promise.

Nondeterministic functions, sequences, timestamps, random values, and failure-prone expressions constrain duplication and movement. Evaluating an expression before versus after a filter may change call count or visible errors. Mark volatility and side effects in operator metadata.

### Rewrite logical plans deliberately

Useful rewrites include constant folding, predicate simplification, projection pruning, predicate pushdown, subquery decorrelation, join reordering, common-subexpression handling, and aggregate simplification. Rule order can matter when one rule exposes another or causes cycles.

Separate normalization from exploration. Record rule identity, before/after fingerprints, proof obligation, and reason a rule did not apply. Bound search by time, memo size, or transformation count, but expose when the optimizer stopped early.

### Represent equivalence in a memo

A memo groups logically equivalent expressions and records alternatives without copying entire trees. Optimization can request a group under required physical properties, derive child requirements, cost implementations, and retain the best known candidate for that property context.

Memo equivalence must be sound. Security predicates, snapshots, correlation bindings, function semantics, and output schemas participate in identity. Cost dominance is only comparable when alternatives deliver compatible properties and semantics.

### Define physical properties

Distribution may be singleton, arbitrary, round-robin, hash-partitioned on expressions, range-partitioned on ordered keys, replicated, or source-local. Ordering specifies key expressions, direction, null placement, and whether it is local or global. Other properties include grouping, uniqueness, partition count, execution convention, locality, and rewindability.

An operator declares requirements on each child and what it delivers. A local merge join needs compatible ordering and partitioning; a local hash join needs co-location by equality keys or a replicated side. A global limit or final ordered result often needs gather/merge behavior.

### Use enforcers when properties are absent

If a child lacks a required property, insert an enforcer. Hash exchange repartitions by keys. Broadcast replicates rows. Gather creates singleton distribution. Range exchange plus local sort can support global order when boundaries agree. Sort enforces collation but may spill.

Enforcers consume CPU, memory, network, serialization, buffers, and failure/retry state. Cost them explicitly. Removing an exchange is safe only if delivered properties truly satisfy the consumer through the relevant snapshot and partition semantics.

### Choose scan implementations and pushdown

A scan may read files, row stores, column stores, indexes, materialized views, or connector-provided partitions. Choose columns, predicates, partitions, snapshot, batch size, and locality. Metadata pruning and statistics can avoid reads without delegating row semantics.

Connector pushdown needs a capability contract for types, nulls, collation, time zones, overflow, functions, security, snapshots, and error behavior. A connector may accept part of a predicate and return a residual. Verify actual pushed operations rather than inferring them from SQL text.

### Choose join algorithms and distribution

Nested-loop joins support general conditions and can exploit indexed probes; hash joins suit equality and require build memory; merge joins exploit compatible ordering and can stream. Distributed choices add broadcast, repartition both sides, co-located/bucketed join, or gather.

Broadcast cost depends on build bytes times destinations and per-worker memory, not only row count. Repartition cost depends on both sides, key serialization, skew, network, and downstream parallelism. Co-location is valid only when partition functions, expressions, counts, versions, and ownership align.

### Plan aggregation in stages

Distributive and algebraic aggregates can use partial aggregation near input, exchange by grouping keys, and final combination. Average becomes partial sum and count; variance needs a numerically appropriate mergeable state. Holistic aggregates may require more state or approximation.

With no grouping keys, final aggregation commonly needs singleton or tree reduction. With keys, hash partitioning co-locates equal groups. Partial aggregation helps only when it reduces rows enough to offset local state and compute; high-cardinality groups may not.

### Plan ordering, limits, and windows

Global sort requires a distributed ordering strategy: sampling or known boundaries, range partitioning, local sort, and ordered merge, or gather for small results. Local sorts alone do not create global order. `LIMIT` may push partial limits toward sources, but final semantics depend on whether order is required.

Window functions require partitioning by window keys and ordering within each partition. Several windows can share properties if compatible; otherwise each may add exchange or sort. Large or skewed partitions create memory and single-task risks.

### Estimate cardinality with provenance

Base statistics include row count, bytes, null fraction, distinct values, min/max, histograms, heavy hitters, and correlations. Derived estimates need predicate selectivity, join overlap, group cardinality, and expression models. Independence and uniformity assumptions are convenient and often wrong.

Attach source, snapshot/time, sample, freshness, uncertainty, and fallback to estimates. Detect impossible estimates such as negative rows or group counts above input where semantics forbid them. Surface estimates beside actuals so errors become evidence rather than hidden optimizer folklore.

### Build a scoped cost model

Cost can include CPU, memory peak, bytes read, network bytes, serialization, spill I/O, startup, latency, and monetary or energy terms. Combining them needs calibrated weights or a lexicographic/service-class objective. A scalar is not meaningful without units and context.

Account for parallel critical path rather than summing all task time as latency. Include skew and straggler risk, resource limits, concurrency, and exchange buffering. Costs rank enumerated candidates; they do not prove an absolute runtime.

### Search join order without claiming omniscience

Join-order space grows rapidly. Dynamic programming can optimize bounded subsets; memo/rule search shares alternatives; heuristics restrict shapes or use greedy choices. Outer, semi, anti, lateral, correlated, and non-equality joins constrain legal reordering.

Use time and memory budgets with a deterministic fallback. Record enumerated alternatives and cutoff. A bad estimate may make exhaustive search choose badly; search breadth cannot compensate for an invalid model.

### Fragment at exchange and materialization boundaries

An exchange commonly separates producer and consumer fragments. Each fragment has input channels, output partitioning, parallelism, placement needs, memory/spill contract, and attempt semantics. Blocking materialization can form a stage boundary and recovery checkpoint.

Define whether consumers stream from producers or wait for completion, how backpressure propagates, who owns buffers, and when output becomes committed. Fragment DAGs must remain acyclic unless the engine explicitly supports iterative execution with a different protocol.

### Map fragments to stages and tasks

Parallelism derives from source partitions, exchange partitions, operator limits, resource bounds, and expected skew. Too little parallelism creates long tasks; too much creates scheduling, file, connection, and coordination overhead. One fragment may produce many attempts across retries or speculation.

Carry logical and physical operator lineage into stage/task metrics. Scheduler delay is distinct from operator time, and a ready worker is not proof that its partition has useful work. Resource requests should reflect peak concurrent operators within the fragment pipeline.

### Make exchange semantics explicit

Specify partition function and version, key expression/type, null handling, partition count, serialization schema, compression, ordering, checksums, flow control, and attempt identity. Hash-compatible producers and consumers must agree exactly; “both hash” is insufficient.

Choose how speculative or retried producer output is selected and garbage-collected. Consumers must not merge duplicate winning and losing attempts. Durable shuffle improves retry isolation but adds write/read cost; pipelined exchange reduces latency but couples failures.

### Address skew as a plan property

Skew creates unequal partitions, long tails, memory failure, and network hotspots. Estimate heavy hitters and observe actual partition bytes/rows. Remedies include salting hot keys, splitting heavy hitters, adaptive partition coalescing/splitting, broadcast, or a specialized skew join.

Preserve semantics when salting or replicating: aggregates need correct recombination and joins must not multiply matches accidentally. Measure tail tasks and largest partition, not only total shuffle bytes.

### Adapt only across safe boundaries

Runtime row counts, partition sizes, and completed shuffle maps can justify changing join strategy, partition count, or skew handling. Adaptation needs a point where prior output is stable and downstream work can be replaced without mixing incompatible layouts.

Version adaptive decisions and retain the original and replacement plans. Avoid oscillation and repeated sunk cost. If a broadcast candidate grew beyond memory, prefer a bounded fallback before every worker fails independently.

### Preserve security and governance semantics

Row filters, column masks, privilege checks, purpose restrictions, and audit expressions are semantic operators, not optional performance hints. Tag them so rewrites cannot remove, duplicate, reorder across unsafe boundaries, or delegate to an untrusted connector.

Plan displays may expose literals, object names, statistics, or predicates. Redact according to viewer authority while retaining secure internal evidence. Cache keys must include security context and relevant policy generations.

### Explain estimates and actual execution

Expose analyzed and physical plans, fragment graph, exchanges, required/delivered properties, estimates, costs, and rule decisions. Runtime explain should add actual rows/bytes, timing, memory, spill, network, retries, skew, and blocked/scheduled time without pretending instrumentation is free.

Use stable semantic fingerprints plus generation-specific IDs. Diff normalized plans while preserving important property, schema, and policy changes. An estimate/actual ratio is diagnostic; zero estimates and censored failed attempts need special handling.

### Validate plans and regressions

Differentially execute equivalent plans against trusted baselines. Use metamorphic relations such as safe predicate forms, join-order variants, and repartition changes. Generate nulls, duplicates, empty inputs, extreme values, skew, correlated data, and nondeterministic expressions.

Inject lost exchange partitions, duplicate attempts, spill failure, stale statistics, worker loss, and adaptive fallback. For performance, use representative data scale and concurrency, then gate plan-shape or outcome regressions cautiously: a different plan can be better, and the same plan can regress under changed data.

## Definitions and Notation

Let logical expression $e$ have schema $\sigma(e)$ and semantics $\llbracket e\rrbracket_D$ over database snapshot $D$. Expressions $e_1\equiv e_2$ when their observable results match for every allowed input and context, including multiplicity, null/error behavior, required order, security, and effects.

Let required physical property vector be $p=(d,o,g,l,x)$ for distribution, ordering, grouping/uniqueness, locality, and execution convention. Physical plan $P$ delivers $\delta(P)$. Satisfaction $\delta(P)\succeq p$ means the delivered guarantees are at least those required; it is not arbitrary numeric ordering.

For statistics $S$ and resource context $R$, cost $C(P\mid S,R)$ may be a vector or calibrated scalar. The candidate set $\mathcal{I}(e,p)$ contains only implementations proved equivalent to $e$ and satisfying $p$. Estimated rows $\hat n_v$ and actual rows $n_v$ at operator $v$ should retain units, scope, attempt, and snapshot.

For hash exchange on key $k$, owner may be $h_v(k)\bmod q$, where $h_v$ is a versioned type-aware hash and $q>0$ partition count. Co-partitioned local equality joins require compatible key expressions/types, null rules, hash version, $q$, and epoch/ownership—not merely equal labels.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Resolve text, parameters, session/catalog/security context, snapshots, names, scopes, types, nullability, correlation, volatility, and effects.
2. Build a logical plan whose operators state bag, null, ordering, and error semantics with stable attributes.
3. Apply only equivalence rules proven for those semantics; record rule identity, fingerprints, and search bounds.
4. Enumerate physical implementations under explicit required properties, statistics provenance, resource context, and cost-model generation.
5. Derive child properties and insert exchange, sort, materialization, or other enforcers when delivered guarantees do not satisfy them.
6. Fragment the plan with versioned channel, partition, schema, buffering, commit, retry, and failure contracts.
7. Assign parallelism/resources/placement and preserve lineage through stages, tasks, attempts, and adaptive replacements.
8. Validate exchange ownership, aggregation merging, skew treatment, side effects, security operators, and recovery behavior.
9. Compare estimates, chosen/rejected alternatives, and actual runtime outcomes with stable normalized fingerprints.
10. Differentially and metamorphically test edge data and inject distributed failures before canarying optimizer or runtime changes.

Logical equivalence is necessary but insufficient for replacing a physical subtree: the replacement must also deliver properties expected by its parent. If it does not, a correct enforcer may restore them, with its cost included.

A local equijoin over partition pairs is complete only when every pair of equal join keys is routed to the same pair-processing partition, or one side is replicated appropriately. Otherwise matching rows can reside in different fragments and disappear from the result.

Cost-based selection proves neither global nor future optimality. It selects the cheapest candidate among explored, semantically valid, property-satisfying alternatives under a particular statistical and resource model. Record each qualification.

## Alternatives and Trade-Offs

- **Tree plans:** simple traversal and display; duplicate shared subexpressions and alternatives.
- **Memo/group representation:** shares equivalence and property search; adds identity, lifecycle, and debugging complexity.
- **Rule-only optimization:** predictable local transformations; interactions and global choices are hard.
- **Cost-based optimization:** compares broad alternatives; depends on statistics, calibration, and bounded search.
- **Broadcast join:** avoids repartitioning a large side; multiplies build transfer/memory and fails on underestimation.
- **Repartition join:** handles two large sides; pays shuffle, skew, serialization, and coordination cost.
- **Co-located join:** minimizes movement; requires exactly compatible, current partition contracts.
- **Hash join:** fast equality lookup; build memory and skew can spill or fail.
- **Merge join:** streams ordered equality inputs; obtaining compatible order/distribution may dominate.
- **Partial aggregation:** reduces exchange volume; high-cardinality groups may add state without reduction.
- **Pipelined exchange:** lowers latency and storage; couples producer/consumer failure and backpressure.
- **Materialized exchange:** isolates retries and supports adaptation; adds I/O and stage latency.
- **Connector pushdown:** reduces data movement; delegates semantics and observability across a trust boundary.
- **Static planning:** reproducible and simple; stale estimates cannot be corrected during execution.
- **Adaptive planning:** uses actual evidence; safe boundaries, sunk work, and lineage become more complex.
- **More partitions:** increases parallelism and skew options; increases scheduling, files, buffers, and metadata.

## Failure Modes and Misconceptions

- **“The AST is the logical plan.”** binding, typing, scope, privileges, and semantic analysis are still missing.
- **“Relational identities always apply to SQL.”** bags, nulls, order, errors, volatility, and outer joins constrain them.
- **“Physical properties are optimization hints.”** local algorithms can require them for correctness.
- **“Hash partitioned means compatible.”** keys, types, hash version, null rules, count, and epoch must agree.
- **“Local sort creates global order.”** partitions also need compatible range/order and ordered consumption.
- **“Removing an exchange is always faster.”** it may violate properties or reduce useful parallelism.
- **“Row count determines broadcast safety.”** serialized bytes, worker count, memory, and concurrency matter.
- **“Statistics are facts.”** they are scoped, sampled, time-sensitive estimates with assumptions.
- **“Exhaustive search guarantees the best runtime.”** models, candidates, future load, and data can be wrong.
- **“Pushdown preserves SQL automatically.”** connector types, nulls, collation, time zones, and errors may differ.
- **“Partial aggregation always helps.”** high cardinality can preserve nearly every row and add state.
- **“More partitions always run faster.”** scheduler, connection, buffer, file, and coordination overhead rises.
- **“Pipelining is strictly better.”** materialization can isolate retries and enable adaptation.
- **“Retrying a fragment is harmless.”** exchange outputs and external effects need attempt-commit rules.
- **“Average partition size captures skew.”** one heavy hitter can dominate tail time and memory.
- **“EXPLAIN is what ran.”** scheduling, attempts, and adaptive changes may produce a different runtime graph.
- **“A plan-text diff proves regression.”** generated IDs differ, while unchanged text can hide data/statistics drift.
- **“Security filters are ordinary predicates.”** their trust, ordering, audit, and non-removal obligations are stronger.

## Worked Examples

### Example 1

A filter on the right table appears above a left outer join. Pushing it into the right scan changes whether unmatched left rows survive when the predicate would be unknown on null-extended columns. The optimizer classifies null rejection and proves the exact transformation instead of applying an inner-join rule by shape.

### Example 2

Two scans each deliver hash distribution on `user_id`, but one uses 64 partitions and an older hash for strings while the other uses 128 and a new hash. Their labels look alike, yet local join is incomplete. Repartitioning under one versioned contract restores co-location.

### Example 3

A build input is estimated at 20 MiB and broadcast to 200 workers, but actual serialized size is 2 GiB. Network and aggregate receiver memory explode. A size guard at a materialized boundary changes to repartition join before consumers commit.

### Example 4

`AVG(price)` is planned as local `(sum,count)`, hash exchange by group key, then final `sum(sum)/sum(count)`. Averaging local averages would be wrong when partitions have different counts. The merge state encodes the aggregate algebra.

### Example 5

Each worker sorts its local rows by timestamp and emits them arbitrarily. Concatenation is not globally ordered. A range exchange with compatible boundaries plus local sort and ordered merge delivers the final property required by `ORDER BY`.

### Example 6

One hot key owns 45% of join rows. Total shuffle is balanced in aggregate across stages, but one partition spills and dominates latency. Heavy-hitter splitting replicates only the matching small-side key range and recombines results without duplicate multiplication.

### Example 7

A connector reports that it accepted a timestamp predicate, but it interprets session time zone differently. Pushdown returns a different boundary set. Capability negotiation either supplies compatible semantics or retains the predicate as an engine-side residual and treats source pruning only as advisory.

### Example 8

A producer fragment is speculated. Both attempts write exchange partition 7. The exchange service commits one attempt ID atomically, consumers read only that manifest, and losing output is collected. Concatenating both attempts would duplicate rows.

### Example 9

An optimizer upgrade chooses the same normalized join tree, yet runtime doubles because a source partition grew and statistics remained stale. Estimate-versus-actual lineage attributes the change to data/statistics rather than declaring the unchanged plan proof of engine health.

### Example 10

The fixture shows why arbitrary source partitions require a hash exchange before local equality joins.

<!-- bijux-verify: {"id":"join-repartition-property","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"local_join_rows=0\nredistributed_rows=2\nmatches=((1, 'Ada', 10), (2, 'Lin', 20))\n","stderr":""}} -->
```python
customers = (((2, "Lin"),), ((1, "Ada"),))
orders = (((101, 1, 10),), ((102, 2, 20),))

def local_join(left_parts, right_parts):
    output = []
    for left, right in zip(left_parts, right_parts):
        names = {customer_id: name for customer_id, name in left}
        output.extend((customer_id, names[customer_id], amount)
                      for _, customer_id, amount in right if customer_id in names)
    return tuple(sorted(output))

before = local_join(customers, orders)
repartitioned = [[], []]
for source in orders:
    for row in source:
        repartitioned[row[1] % 2].append(row)
after = local_join(customers, tuple(tuple(part) for part in repartitioned))

print(f"local_join_rows={len(before)}")
print(f"redistributed_rows={len(after)}")
print(f"matches={after}")
```

The example assumes customer partitions already use `customer_id % 2`. Production exchanges must version type-aware hashes, null behavior, counts, ownership epochs, schemas, and attempt commits.

## Cross-Program Connections

- **Database systems:** relational algebra, SQL semantics, indexes, statistics, join order, and transactions define plan meaning.
- **Algorithms:** dynamic programming, memoization, graph search, hashing, sorting, sampling, sketches, and bin packing shape alternatives.
- **Distributed systems:** partition ownership, exchange, retries, speculation, manifests, backpressure, and partial failure make plans executable.
- **Data engineering:** files, partitions, skew, shuffle, stage boundaries, connectors, and schema evolution drive physical behavior.
- **Platform engineering:** fragment resources, placement, scheduler delay, isolation, network, storage, and autoscaling constrain execution.
- **Reliability engineering:** materialization, attempt commit, adaptive fallback, fault injection, canary, and rollback protect outcomes.
- **Security and governance:** privileges, row filters, masks, purpose, snapshots, redacted plans, and audit constrain optimization.
- **Performance engineering:** estimates, costs, actual metrics, critical path, spill, network, skew, and concurrency explain latency.

## References

1. Apache Calcite. [Relational Algebra.](https://calcite.apache.org/docs/algebra.html) Current relational-expression, trait, convention, rule, and planner construction concepts.
2. Apache Calcite. [Adapters.](https://calcite.apache.org/docs/adapter.html) Current adapter, schema, table, calling-convention, and pushdown architecture.
3. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current caching, partitioning, join hints, statistics, adaptive execution, coalescing, and skew behavior.
4. Apache Spark. [EXPLAIN.](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-explain.html) Current parsed, analyzed, optimized logical, physical, formatted, cost, and code-generation display modes.
5. Trino. [Optimizer.](https://trino.io/docs/current/optimizer.html) Current statistics, cost-based choices, join enumeration/distribution, pushdown, and property-based optimizations.
6. Trino. [EXPLAIN.](https://trino.io/docs/current/sql/explain.html) Current distributed-plan, fragment, stage, cost, and graph explanation forms.
7. PostgreSQL. [Using EXPLAIN.](https://www.postgresql.org/docs/current/using-explain.html) Current estimated/actual plan trees, scans, joins, sorts, aggregation, costs, rows, and instrumentation.
8. PostgreSQL. [Planner/Optimizer.](https://www.postgresql.org/docs/current/planner-optimizer.html) Current path generation, cheapest-path selection, plan creation, and join search overview.
9. DuckDB. [EXPLAIN: Inspect Query Plans.](https://duckdb.org/docs/stable/guides/meta/explain.html) Current logical/physical plan inspection and analyzed runtime profiling.
10. Apache DataFusion. [EXPLAIN Usage.](https://datafusion.apache.org/user-guide/explain-usage.html) Current initial/final logical and physical plans, optimizer passes, statistics, and metrics display.
11. Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets.](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) Primary account of distributed execution trees, columnar nested data, aggregation, and interactive scale.
12. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary account of logical/physical planning, distributed operators, partitioning, and production query execution.
13. Meta Engineering. [Presto: Interacting with Petabytes of Data at Facebook.](https://engineering.fb.com/2013/11/06/core-infra/presto-interacting-with-petabytes-of-data-at-facebook/) Primary architecture account of coordinators, workers, stages, tasks, operators, connectors, and pipelined execution.

## Exercises

### Exercise 1

For `SELECT k, SUM(v) FROM T GROUP BY k ORDER BY k`, design a distributed physical plan. State child requirements, delivered properties, exchanges, local/global ordering, and the merge algebra.

### Exercise 2

Analyze whether `WHERE R.x > 10` can move from above `L LEFT JOIN R ON L.id=R.id` into the right input. Cover output semantics, null-extension, bags, and safe alternative rewrites.

### Exercise 3

Compare broadcast, repartition, and co-located physical plans for joining a 4 TiB fact table with an estimated 40 MiB dimension whose estimate is uncertain. Specify evidence, guards, failure behavior, and adaptive boundary.

### Exercise 4

Design an exchange contract safe under producer retry and speculation. Include partitioning, schema, ordering, flow control, integrity, attempt selection, consumer visibility, and garbage collection.

### Exercise 5

Design validation for an optimizer release that adds connector predicate pushdown and adaptive skew joins. Include semantic, distributed-failure, performance, security, observability, canary, and rollback evidence.

## Answers to the Exercises

### Answer 1

Scan `T` with projected `k,v`; optionally compute local partial state `(sum,count-not-needed-for-SUM)` grouped by `k`. Hash exchange partial rows by a versioned representation of `k` with common partition count. Each consumer performs final `SUM` per key, delivering hash grouping but not global order. To satisfy `ORDER BY k`, use compatible range exchange followed by local sort and ordered merge, or gather and sort when bounded enough. `SUM` partial states merge by addition with SQL null/empty-input rules preserved. Requirements include matching key type/collation/null semantics, exchange attempt commit, memory/spill bounds, and a final global ordering contract.

### Answer 2

Moving the predicate only into `R` while retaining a left join is generally not equivalent: rows in `L` with no surviving right match become null-extended and remain in the rewritten result, whereas the original post-join predicate evaluates unknown and removes them. If the predicate is null-rejecting and the original filter eliminates every null-extended row, the optimizer can often transform the combination into an inner join and push the predicate into `R`, subject to volatility/error and bag proofs. Test duplicate matches, null `R.x`, null join keys, empty inputs, and failure-prone expressions. Preserve attribute identity and security provenance.

### Answer 3

Broadcast reads the fact locally and replicates the dimension, avoiding fact shuffle, but 40 MiB times worker count plus deserialized/hash-table memory and concurrency must fit. Repartition shuffles both sides by join key and is robust to a larger dimension but expensive for 4 TiB. Co-location is cheapest only if fact and dimension share exact current key/hash/count/epoch contracts. Use fresh bytes, rows, distinct/heavy hitters, uncertainty, worker memory, destinations, network, and concurrent broadcasts. Materialize or otherwise measure the dimension at a safe boundary; broadcast only below a hard serialized/deserialized guard, otherwise switch once to repartition. Version the replacement, discard incompatible downstream attempts, and preserve a deterministic retry path.

### Answer 4

Define key expressions/types, hash/range implementation and version, null behavior, partition count, ownership epoch, serialization schema, compression, checksums, optional order, buffer limits, backpressure, and encryption. Key outputs by query, fragment, producer partition, consumer partition, and attempt. A coordinator or durable manifest atomically selects one complete verified attempt per producer partition; consumers see only committed manifests and never concatenate competing attempts. Partial outputs remain invisible, reads verify integrity, cancellation stops obsolete producers, and losing/orphan objects are collected after consumer/recovery retention. Specify pipelined failure coupling or materialized durability explicitly.

### Answer 5

Build differential and metamorphic suites covering nulls, duplicates, empty inputs, overflow, time zones, collations, outer/semi/anti joins, correlation, volatility, errors, row filters, masks, and connector residuals. Compare pushdown with engine evaluation and trusted results. Generate uniform/correlated/skewed data and inject stale estimates, heavy hitters, worker loss, duplicate attempts, truncated exchanges, spill failure, connector failure, and adaptive fallback. Capture normalized logical/physical/fragment plans, rule decisions, capability versions, estimates/actuals, partition tails, network, memory, spill, retries, and security audit. Replay production-shaped workloads, shadow planning, canary bounded tenants, and gate on correctness first, then SLO/cost and no privacy or fairness regression. Roll back optimizer/capability generation while reconciling active queries under a declared continue-or-cancel policy.
