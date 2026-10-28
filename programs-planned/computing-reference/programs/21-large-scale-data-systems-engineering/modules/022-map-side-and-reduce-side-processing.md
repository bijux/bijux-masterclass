---
module_id: LSDS-022
program: Large-Scale Data Systems Engineering
level: 1
module_number: 22
title: Map-Side and Reduce-Side Processing
status: complete
last_verified: 2026-09-03
---

# Map-Side and Reduce-Side Processing

## One-Page Review

### Governing question

Which parts of a large batch computation can run independently near the input, which require records to be regrouped across workers, and how should engineers move work across that boundary without changing semantics or merely moving the bottleneck?

### Essential definitions

- A **map-side operation** uses one record, one input split, bounded task-local state, or an explicitly versioned side input without first gathering all records for a global key.
- A **reduce-side operation** consumes a group whose completeness is established by partitioning and shuffle.
- **selection/filtering** removes records; **projection** removes fields; both can reduce downstream work when semantics permit early execution.
- **partial aggregation** converts a subset of values into a mergeable accumulator before shuffle.
- A **side input** is bounded auxiliary data materialized for many tasks; it is not mutable shared state.
- A **map-side join** avoids a general shuffle only when one input is replicated safely or inputs already share compatible partitioning and ordering.
- A **reduce-side join** tags and shuffles both relations by join key so one reducer can see the required group.
- A **holistic aggregate** has no generally bounded exact summary, unlike distributive or algebraic aggregates.
- **operator pushdown** moves safe work earlier to reduce bytes/records while preserving results.

### Central model, mechanism, or theorem

An operation may move before the shuffle when it is homomorphic over partition union or otherwise requires only local information plus stable bounded reference state. For aggregation, choose accumulator type `A`, lift `eta: V -> A`, associative merge `oplus: A x A -> A`, identity `e`, and finish `phi: A -> O`. Then any partitioning/retry tree is correct when `oplus` is associative, commutative if order is unspecified, identity-safe, and representation semantics such as overflow are defined.

Filtering and projection should move map-side only when they do not remove fields/records needed for later keys, joins, ordering, audit, or error handling. Cross-record operations—global grouping, arbitrary joins, exact global distinct, or global ordering—normally require shuffle unless storage layout, replicated side data, or multi-stage algebra supplies equivalent information.

### Critical invariants

- Operator placement is justified by information dependencies, not by performance preference alone.
- Early filter/projection preserves every field and record needed for downstream keys, conditions, lineage, and validation.
- Partial accumulators are closed under merge and encode enough information for the final result.
- Side inputs are immutable, size-bounded, versioned, authorized, and identical in logical content across attempts.
- Prepartitioned/map-side joins prove compatible key encoding, partition count/boundaries, sort/group order, and snapshot alignment.
- Reduce-side grouping places all required records for one logical key together under the declared comparator.
- Hot keys and large groups are bounded, streamed, salted through a correct second stage, or rejected explicitly.
- Attempt replay cannot duplicate external effects or corrupt local/global aggregate state.
- Optimizations are validated by result equivalence plus end-to-end cost, not shuffle bytes alone.

### Common failures

Frequent failures are treating any local cache as a side input, broadcasting a table that does not fit every worker, filtering before a left/outer join incorrectly, projecting away join or audit columns, using scalar averages as partials, assuming floating-point addition is reproducible, running exact distinct in unbounded mapper memory, calling a map-side join on merely similarly named partitions, relying on combiner invocation, materializing all reduce values, sending every record to one reducer for global order, and reducing shuffle only to increase spills, CPU, skew, output files, or stale-reference errors.

### Compact example

Seven keyed values across two map partitions would shuffle seven raw pairs. Local sum aggregation emits five accumulators: map A emits `a:5,b:1`; map B emits `a:4,b:6,c:8`. Reducers merge them to `a:9,b:7,c:8`. The optimization saves two pairs in this toy input and remains correct because integer sum under defined overflow is mergeable. Replacing local values by their average would be wrong; `(sum,count)` is the correct accumulator for mean.

### Connections

[LSDS-007](007-narrow-and-wide-transformations.md) supplies dependency width. [LSDS-021](021-mapreduce-execution-model.md) supplies split, shuffle, grouping, and commit semantics. [LSDS-023](../ROADMAP.md) deepens partitioners and combiners. [LSDS-024](../ROADMAP.md) generalizes placement into DAG stages.

## Governing Question

Every distributed batch plan has an information boundary. Before exchange, a task sees only its split, its local state, and bounded explicit reference inputs. After exchange, a task can see all records routed to one key or partition. The boundary determines which answers are even computable, not just how fast they run.

Map-side code is attractive because it exploits locality and parallelism while avoiding network transfer. Parsing, validation, field derivation, filtering, projection, sampling, and many partial aggregates fit naturally. Yet a local view cannot know that a key is globally unique, that no matching row exists elsewhere, or that a value is the global maximum without mergeable evidence.

Reduce-side code pays materialization, serialization, sort/group, network, and skew costs to establish coordination. That cost buys a guarantee: all intermediate records for a grouping key reach one logical reducer. Correct algorithms spend that guarantee where needed and avoid it where algebra or physical layout makes it redundant.

The governing question is how to place each transformation at the earliest correct point, prove equivalence, and measure whether the supposed optimization improves the whole pipeline.

## Why This Matters

Intermediate data can exceed input by orders of magnitude. Early filtering and projection reduce serialization, spill, network, sort, merge, disk, and reducer work. Local combination can turn millions of events per key per mapper into one accumulator. A replicated dimension can avoid shuffling a much larger fact table.

But aggressive pushdown changes semantics easily. Filtering the right side of a left join before or after the join can differ depending on predicate placement. Dropping nulls before an aggregate changes count denominators. Normalizing a key with nondeterministic locale can send retries to different reducers. A stale broadcast table makes each map internally consistent but globally wrong.

Resource trade-offs are coupled. A hash-map combiner reduces network while consuming mapper memory and delaying emission. Broadcast join removes shuffle and multiplies reference memory/network by worker count. More local work can reduce reducer pressure and lengthen maps, blocking pipeline progress or speculation.

The same principles survive beyond MapReduce. Query optimizers push predicates/projections, dataflow runners lift combiners, databases choose broadcast versus repartition joins, and streaming systems perform per-key/window aggregation. Understanding the information proof prevents cargo-cult tuning.

## Prerequisites and Retrieval

Recall partitioning from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md), locality from [LSDS-004](004-data-locality.md), task graphs from [LSDS-005](005-distributed-task-graphs.md), stages/dependencies from [LSDS-006](006-stages-tasks-and-dependencies.md), narrow/wide transformations from [LSDS-007](007-narrow-and-wide-transformations.md), and serialization from [LSDS-008](008-serialization-across-workers.md).

Retrieve failure/replay assumptions from [LSDS-009](009-cluster-failure-assumptions.md), work/state accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md), read/write pipelines from [LSDS-014](014-read-and-write-pipelines.md), file/layout behavior from [LSDS-019](019-small-file-pathologies.md) and [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), and the complete map/shuffle/reduce runtime from [LSDS-021](021-mapreduce-execution-model.md).

You should understand multisets, predicates, projections, joins, group-by, monoids, associativity, commutativity, identity, sorting, hashing, bounded memory, deterministic serialization, retries, and immutable snapshots.

## Learning Objectives

After completing this module, you should be able to:

- classify operators by local versus cross-partition information requirements;
- push filtering, projection, parsing, and derivation safely to the map side;
- design mergeable accumulators for sum, count, mean, variance, top-k, and sketches;
- recognize holistic exact operations that need unbounded state or repartitioning;
- distinguish optional combiner execution from explicit in-mapper aggregation;
- select broadcast/replicated, partitioned merge, or reduce-side joins from evidence;
- preserve outer-join, null, duplicate, and skew semantics;
- design secondary ordering and multi-stage global results;
- quantify record/byte reduction, memory, CPU, spill, fan-out, and skew trade-offs;
- handle side-input versioning, task replay, and output commit safely;
- validate optimized and reference plans for result equivalence; and
- identify security, governance, and accessibility implications of placement.

## Core Exposition

### Information determines placement

Ask what information an operator requires. A pure per-record transform needs only its record. A split-local operation can use bounded state from records already seen in that split but cannot know the global remainder. A keyed global operation needs every record for the key or a lossless mergeable summary of each subset.

Map-side placement is correct when processing partitions independently and merging their outputs is equivalent to processing the whole input. Some operations commute with union directly; others need a richer accumulator. If no bounded sufficient summary exists, exact computation requires gathering or external state.

Physical colocation can supply information without a new shuffle, but it must be proven. “Both datasets are partitioned by customer” is incomplete without matching hash/version, reducer count, boundaries, serialization, and snapshot.

### Per-record map-side work

Parsing, schema validation, normalization, projection, deterministic derivation, tokenization, decompression, and policy classification commonly run per record. Emit valid data and structured reject streams separately rather than silently dropping errors.

Keep code deterministic across attempts. Locale, timezone, floating-point mode, library version, reference dictionaries, and Unicode normalization affect keys and values. Pin them in job identity.

Bound output expansion. Tokenization, graph adjacency expansion, or exploding arrays can turn one input into millions of pairs. Measure emitted records/bytes per input and quarantine adversarial records.

### Filter pushdown

A selection `sigma_p` commutes with partition union for a deterministic per-record predicate: filter each partition, then union. Push it before serialization and shuffle to avoid moving rejected records.

Predicate semantics include nulls, errors, time zones, collations, authorization, and side-input version. A filter depending on aggregate rank, global existence, or cross-record state is not per-record.

Join placement matters. A predicate on the preserved side of an outer join can often push safely; a predicate on the nullable generated side can turn an outer join into an inner join if placed incorrectly. Prove with relational semantics and adversarial null/unmatched cases.

### Projection pushdown

Carry only fields needed for downstream partition keys, join conditions, ordering, aggregation, output, provenance, authorization, and validation. Columnar readers can avoid decoding/uncompressing unreferenced columns as well as reducing shuffle serialization.

Do not remove stable record IDs, event time, schema version, tenant/classification, source position, or error context when later correctness depends on them. The smallest payload is not correct if it becomes unauditable.

Rename/type conversion should preserve canonical key encoding. Projecting a decimal into binary float or timestamp into local text can change equality and partitioning.

### Partial aggregation algebra

Define accumulator `A`, lift `eta`, merge `oplus`, identity `e`, and finish `phi`. Runtimes may construct arbitrary aggregation trees through local combining, spills, retries, and reducer merging.

Associativity makes parenthesization irrelevant mathematically. Commutativity makes unspecified order irrelevant. Identity handles empty partials. Closure ensures every merged value remains valid `A`. Serialization must preserve `A` across workers.

Machine arithmetic can violate mathematical laws. Integer overflow, floating-point rounding, decimal context, NaN, and nondeterministic tie-breaking need explicit policies and tests.

### Distributive, algebraic, and holistic aggregates

Distributive aggregates such as count, min, max, and bounded integer sum merge fixed-size results of the same form. Algebraic aggregates use fixed-size tuples: mean uses `(sum,count)`; variance can use mergeable count/mean/second-moment state with numerical care.

Holistic aggregates such as exact median or arbitrary exact quantiles have no generally bounded fixed-size summary. They need all values, external sorting, domain-bounded histograms, or approximation sketches.

Approximate distinct, quantiles, and heavy hitters can use mergeable sketches with accuracy/confidence/seed/version metadata. A sketch is not an exact result; measure error on representative and adversarial distributions.

### Combiner versus in-mapper aggregation

A framework combiner is an optimization the runtime may invoke zero, one, or multiple times over mapper/spill subsets. Job correctness must be unchanged if it never runs. Its types and merge semantics must be compatible with mapper output and reducer input.

In-mapper aggregation explicitly maintains a bounded local table and emits partials at thresholds/end. It gives more control and can exhaust memory or make retries expensive. Eviction must emit a correct partial, allowing the same key to appear multiple times.

Combining is most effective when many repeated keys occur within each mapper. If every key is unique per split, it adds CPU with little reduction.

### Aggregate examples

Sum/count use additive state. Mean carries both. Weighted mean carries `(weighted_sum, weight_sum)`. Set union is mergeable and unbounded unless represented by a bounded approximate filter/sketch or domain bitset.

Top-k keeps at most `k` candidates per partition, then merges candidate sets and trims to `k`, with a total deterministic tie-breaker. If ranking depends on a later global normalization, preserve sufficient components.

Variance formulas differ in numerical stability. A mergeable online state is safer than subtracting nearly equal `sum(x^2)/n - mean^2` for large values. Validate against high-precision reference data.

### Side inputs

A small reference table can be distributed to every mapper through a versioned cache/artifact. Each attempt loads and validates the same digest, schema, authorization, and effective-time snapshot, then performs local lookups.

“Small” means it fits memory alongside runtime, buffers, code, and skew on every active worker. Distribution cost is roughly reference bytes times workers/cache misses, not reference bytes once. Startup and cache churn matter.

Never read a mutable service independently from every mapper and call it one join snapshot. Results can vary by time, retry, authorization, and endpoint. Export/pin a snapshot or use a transactional source.

### Broadcast map-side join

Replicate the smaller relation and stream the larger relation through map lookups. This avoids shuffling the large side and works for inner/left enrichment when duplicate/reference semantics and memory are defined.

Build the reference as `key -> collection` if keys are nonunique; silently taking one row changes a many-to-many join. For left joins, emit unmatched facts with null/absent dimension according to schema. For full outer joins, unmatched reference rows require additional accounting.

Protect sensitive reference data copied to every worker. Scope distribution, encrypt/cache safely, and clean it after attempts.

### Partitioned map-side merge join

Two large inputs can join map-side if they are co-partitioned and sorted compatibly. Pair corresponding partitions and perform a streaming merge by key. This saves a new shuffle but may require an earlier job to establish layout.

Compatibility includes partition function implementation/version, partition count or range boundaries, key serialization/comparator, sort order, duplicate grouping, null policy, and snapshot alignment. Similar directory names prove none of these.

Skew remains: a partition or duplicate key can be huge. Validate manifests and per-partition bounds before declaring the fast path safe.

### Reduce-side join

Tag rows by source and emit join key. Shuffle brings all rows for the key to one reducer; reducer separates sources and computes inner/left/right/full/semi/anti semantics.

Many-to-many keys produce Cartesian multiplicity `|L_k|*|R_k|`. Materializing both groups can exhaust memory. Stream one side only when ordering/group structure permits, spill bounded groups, or detect/reject explosive keys.

Reduce-side join is general and pays shuffle for both sides. Projection/filtering and local preaggregation can reduce payload if they preserve multiplicity and join conditions.

### Skewed joins

Sample key frequencies and bytes. A hot key can dominate one reducer even when record counts look balanced because values vary in size or output expansion.

For a small side, replicate only hot-key matches and salt the large side. For aggregating joins, partial results can merge. For raw many-to-many output, salting may replicate records and cannot remove inherent result size.

Treat hot-key policy as versioned plan logic. Thresholds based on stale samples can move the bottleneck or omit data.

### Distinct and deduplication

Exact global distinct requires all equal identities to meet or a preexisting unique partition guarantee. Mappers can locally deduplicate to reduce shuffle while reducers still establish global uniqueness.

Task-local sets can be unbounded. Spill sorted runs, cap hash tables with correct emission, or use probabilistic filters only as acceleration—not authority—because false positives can drop real records.

Deduplication identity must include the domain's stable event/version semantics. Equality of serialized bytes is not always business equality.

### Ordering

Mapper-local order is not global. Reducers receive keys sorted within partitions. Multiple reducer outputs are not one globally sorted stream unless range partition boundaries and comparators establish nonoverlap and an ordered manifest combines them.

Secondary sort embeds `(group_key, order_key, tie_breaker)` in the sort key while grouping by `group_key`. Reducer values then arrive in the designed order under framework semantics. Tie-breakers must be deterministic and total.

Sending everything to one reducer establishes simple global order and sacrifices scalability. Range partitioning plus sampling handles large output with boundary/skew risk.

### Multi-stage processing

Some operations need two shuffles. Hot-key salting performs partial aggregation by `(key,salt)`, then merges by `key`. Global top-k computes local top-k and then global top-k. Total ordering samples boundaries, repartitions by range, then writes ordered partitions.

Materialize stage outputs with immutable manifests and validation. A later stage must not list a partially committed prefix. Preserve operation IDs and lineage across stages.

A DAG engine can express these dependencies without treating each map/reduce pair as an unrelated job, but information boundaries remain.

### Resource accounting

Let raw intermediate records/bytes be `N_raw,B_raw` and map-side optimized emissions be `N_map,B_map`. Reduction fractions are `1-N_map/N_raw` and `1-B_map/B_raw`; both matter because accumulator records can be larger.

Add mapper CPU/memory/spill, side-input distribution, serialization, reducer skew, output expansion, task duration, speculative duplication, and end-to-end latency. A 90% record reduction with 10x larger accumulator bytes may not save network.

Measure by key-frequency/size percentiles, not averages. Separate attempted, spilled, shuffled, fetched, and committed bytes.

### Failure and replay

Map-side caches and accumulators are attempt-local. After failure they rebuild from the exact input split and side-input version. Do not checkpoint them as shared mutable authority without a designed protocol.

Reducer grouping may replay after lost worker or speculative execution. External effects remain unsafe. Managed outputs use attempt isolation and job commit from LSDS-021.

If a side-input download or checksum fails, fail the attempt rather than silently use an older cache. Record its digest in output provenance.

### Validation

Build a simple reference plan that shuffles raw records and computes exact results for representative samples. Compare optimized plan outputs by exact keyed multiset or domain-appropriate tolerances.

Test empty groups, duplicates, nulls, missing join sides, nonunique dimensions, extreme hot keys, overflow, NaN, tie scores, adversarial hashes, changed side input, retry, speculation, and partition mismatch.

Counters include filter accepts/rejects, raw/combined pairs and bytes, accumulator evictions, side-input bytes/cache, join matches/unmatched/multiplicity, key/skew percentiles, shuffle/spill, and committed outputs. Counters supplement result validation.

### Security and governance

Pushdown can remove data before audit if required provenance fields are discarded. Define what rejected/filtered records must be counted, sampled, quarantined, or retained.

Broadcast increases the number of machines holding reference data. Reduce-side grouping can co-locate records across tenants. Partition keys and spill filenames can reveal identities. Apply least privilege, encryption, domain separation, retention, and cleanup.

For regulated decisions, an optimized aggregate or approximate sketch must not silently change accuracy/fairness. Name domain, privacy/legal/records, security, accessibility, affected-community/ethics, operations, and independent reviewers as consequence requires.

## Definitions and Notation

- `P_i` is input partition/split `i`; `union_i P_i` is the input multiset.
- `f` is a per-record map-side transform or predicate.
- `A` is partial-accumulator type, `eta` lifts values, `oplus` merges accumulators, `e` is identity, and `phi` finalizes output.
- `L_k` and `R_k` are left/right relation multisets for join key `k`.
- `S` is immutable side-input snapshot with byte size `B_S` and digest/version.
- `N_raw,B_raw` are raw emitted records/bytes; `N_map,B_map` are post-map-side-optimization emissions.
- `rho_N=1-N_map/N_raw` and `rho_B=1-B_map/B_raw` are record/byte reduction fractions when denominators are positive.
- `H` is the set of hot keys selected by a versioned skew policy.
- `s` is source snapshot and `J` is committed job/output identity.

The algebraic law is about mathematical accumulator values plus representation policy. A runtime may reorder merges; correctness requires defined behavior under that order or an explicitly deterministic execution strategy.

## Mechanisms, Invariants, or Proof Structure

Use this operator-placement audit:

1. Pin input/side-input snapshots, schema, key encoding, policy, and code/config identity.
2. State each operator's required information: record, split, bounded side input, complete key group, or global dataset.
3. Push deterministic filters/projections only after proving downstream join/null/lineage/error equivalence.
4. Define accumulator lift/merge/identity/finish, numeric bounds, serialization, and optional-combine correctness.
5. Choose join strategy from exact size, memory, partition/sort compatibility, multiplicity, skew, and snapshot evidence.
6. Bound local tables, side-input copies, output expansion, spills, group memory, and hot keys.
7. Add stages when salting, global order/top-k, exact distinct, or mergeable partials require another information boundary.
8. Keep attempt state isolated and external effects idempotent or commit-mediated.
9. Compare optimized output with a reference plan on adversarial data and committed manifests.
10. Measure total CPU/memory/disk/network/latency/cost, security exposure, and governance—not shuffle reduction alone.

The fixture compares raw shuffle pairs with explicit map-side sum accumulation across two splits. It models algebraic equivalence, not framework combiner invocation or distributed failure.

<!-- bijux-verify: {"id":"map-side-partial-sum","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_records=7 raw_shuffle_pairs=7 local_shuffle_pairs=5 saved_pairs=2\nmap_0=(('a', 5), ('b', 1))\nmap_1=(('a', 4), ('b', 6), ('c', 8))\nfinal=(('a', 9), ('b', 7), ('c', 8))\n","stderr":""}} -->
```python
partitions = (
    (("a", 3), ("b", 1), ("a", 2)),
    (("a", 4), ("c", 7), ("b", 6), ("c", 1)),
)


def local_sum(records: tuple[tuple[str, int], ...]) -> tuple[tuple[str, int], ...]:
    keys = sorted({key for key, _ in records})
    return tuple(
        (key, sum(value for current, value in records if current == key))
        for key in keys
    )


partials = tuple(local_sum(partition) for partition in partitions)
all_partials = tuple(pair for partial in partials for pair in partial)
final = local_sum(all_partials)

raw_count = sum(len(partition) for partition in partitions)
local_count = len(all_partials)
print(
    f"input_records={raw_count} raw_shuffle_pairs={raw_count} "
    f"local_shuffle_pairs={local_count} saved_pairs={raw_count - local_count}"
)
for index, partial in enumerate(partials):
    print(f"map_{index}={partial}")
print(f"final={final}")
```

If every mapper saw unique keys, local and raw pair counts would match. If arithmetic overflowed or local state evicted, emitted partials would still need to merge under the same defined law.

The proof of an optimized production plan includes semantic equivalence, bounded resources, stable reference versions, failure/retry behavior, committed output identity, and downstream/governance compatibility.

## Alternatives and Trade-Offs

Raw reduce-side grouping is simple and moves all values. Partial aggregation adds local CPU/memory and often reduces shuffle dramatically for repeated keys.

Framework combiners are optional and runtime-controlled. In-mapper aggregation is explicit and needs bounds/eviction. Runner-native combine transforms expose algebra and enable broader optimization.

Broadcast join avoids large-side shuffle and replicates reference bytes/memory/security exposure. Reduce-side join handles large arbitrary inputs and pays shuffle/skew. Prepartitioned merge join is efficient and requires strong layout compatibility.

Filter/projection pushdown reduces work and can hide rejects/provenance or alter outer-join/null behavior. Retain required audit streams and prove semantics.

Exact distinct/quantiles require potentially large state or sort. Approximate sketches bound resources and introduce quantified error and version compatibility.

Hash partitioning balances diverse keys; range partitioning supports ordered outputs; skew-aware routing treats hot keys specially and complicates plans.

One-stage simplicity reduces intermediate commits and can leave hot/global operations serial. Multi-stage decomposition adds materialization/lineage/latency and enables scalable partial merging.

Map-side side inputs improve locality and create per-worker startup/copy costs. Remote service lookups avoid broadcast and introduce latency, rate limits, mutable snapshots, and retry side effects.

Materializing reduce groups simplifies code and risks memory. Streaming iterators bound memory and restrict algorithms requiring random access.

## Failure Modes and Misconceptions

- **“Map side is always faster.”** Extra CPU, memory, spills, side-input copies, or lost pruning can dominate.
- **“Any operation can move before shuffle.”** Local information may be insufficient for global semantics.
- **“Filters always push through joins.”** Outer joins, nulls, nondeterminism, and side-specific predicates can change results.
- **“Projection means keep only output fields.”** Keys, conditions, provenance, policy, and validation fields may be needed first.
- **“Associative on paper means safe in code.”** Overflow and floating-point rounding change representation behavior.
- **“Average is a valid partial average.”** Merge `(sum,count)` or a defined weighted state.
- **“The combiner runs once per mapper.”** It may run zero, once, or repeatedly over subsets.
- **“In-mapper aggregation emits one record per key.”** Bounded eviction can emit multiple correct partials.
- **“Broadcast data is loaded once.”** It is distributed/cached across workers and attempts.
- **“A mutable API is a side input.”** Independent calls do not establish one versioned snapshot.
- **“A key-value map is enough for a join dimension.”** Nonunique keys require collections and multiplicity.
- **“Matching partition folder names prove co-partitioning.”** Function, count/bounds, encoding, sort, and snapshot must match.
- **“Reduce-side join handles any key safely.”** Many-to-many output and hot groups can be intrinsically enormous.
- **“A bloom filter can perform exact deduplication.”** False positives can drop valid records.
- **“Reducer output files are globally sorted.”** Only partition-local order is automatic.
- **“Shuffle bytes are the optimization objective.”** End-to-end correctness, latency, cost, and exposure decide.
- **“Counters prove equivalent results.”** Offset errors can preserve counts; compare keyed outputs/invariants.
- **“Optimization is governance-neutral.”** Placement changes copies, grouping domains, rejects, precision, and auditability.

## Worked Examples

### Example 1

**Situation:** A mapper projects 80 of 100 columns away before shuffle. **Reasoning:** This is safe only if the retained 20 include every partition/join/order/aggregate/output/provenance/policy field; columnar pushdown can also avoid decoding the others.

### Example 2

**Situation:** Each map sees thousands of repeated product IDs. **Reasoning:** Emit mergeable per-product partial sums/counts at bounded thresholds. Measure byte reduction because accumulator records may be wider than raw values.

### Example 3

**Situation:** A mean combiner emits one scalar mean per mapper. **Reasoning:** Reducer averaging those scalars weights mappers equally. Carry `(sum,count)` with defined precision and calculate mean after global merge.

### Example 4

**Situation:** A 200-MiB dimension is broadcast to 4,000 workers. **Reasoning:** Logical size is small relative to facts, yet worst-case distribution/cache memory approaches 800,000 MiB before sharing/compression. Validate worker memory, cache locality, startup, authorization, and alternatives.

### Example 5

**Situation:** Two large datasets say `partition=17` in their paths. **Reasoning:** Verify exact partition function/version/count, key encoding, comparator/sort, file boundaries, and snapshots before a map-side merge join; otherwise repartition.

### Example 6

**Situation:** A left join filters dimension status to active. **Reasoning:** Decide whether inactive matches should become unmatched rows or be removed after join. Those meanings differ; place predicate from the intended relational expression.

### Example 7

**Situation:** One join key creates 20 million by 5,000 matches. **Reasoning:** The 100-billion-row output is intrinsic. Salting redistributes computation but not output size; revisit domain semantics, preaggregation, or explicit rejection.

### Example 8

**Situation:** Exact global top 100 over a billion rows is required. **Reasoning:** Compute deterministic local top 100s, then merge candidates in another stage. Any globally top item must be locally top 100 in its partition under the same total order.

### Example 9

**Situation:** An optimized job shuffles 95% fewer records but runs slower. **Reasoning:** Inspect accumulator CPU/memory, spills, serialized byte width, hot keys, map duration, speculation, and downstream output. Optimize end-to-end.

### Example 10

**Situation:** Broadcast enrichment contains regulated attributes. **Reasoning:** Pin digest/effective version, minimize fields, scope/decrypt only on approved workers, clean caches, retain provenance, test access boundaries, and obtain privacy/security/domain review.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hash tables, heaps/top-k, external sorting, probabilistic structures, and bounded streaming algorithms. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies relational algebra, predicate/projection pushdown, joins, grouping, cost models, and null semantics.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partitions, retries, immutable snapshots, deterministic replay, and commits. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies shuffle/broadcast fan-out, congestion, locality, compression, and backpressure.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes batch joins, aggregations, deduplication, table layouts, quality checks, and lineage. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies schedulers, worker memory, distributed artifacts, observability, quotas, and cost ownership.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies versioned side-input exports, idempotent effects, and ambiguity resolution. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies least privilege, data minimization, intermediate/cache protection, domain isolation, and audit.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies approximation, quantiles, numerical trade-offs, sketches, and validation. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies trade studies, invariants, hazard review, evidence, and named stakeholders.

## References

- Apache Hadoop, [*MapReduce Tutorial*](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), checked 2026-09-03. Official mapper, reducer, combiner, partition, shuffle, grouping, secondary sort, input, output, compression, and counter semantics.
- Apache Hadoop, [*Mapper API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/Mapper.html), checked 2026-09-03. Official record mapping, setup/cleanup, local aggregation pattern, key grouping, and task behavior.
- Apache Hadoop, [*Reducer API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/Reducer.html), checked 2026-09-03. Official shuffle, sort, group iteration, secondary sort, and reduce lifecycle.
- Apache Hadoop, [*ChainMapper API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/chain/ChainMapper.html), checked 2026-09-03. Official chaining of map-side mapper transformations and type/configuration boundaries.
- Apache Hadoop, [*MultipleInputs API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/input/MultipleInputs.html), checked 2026-09-03. Official support for distinct input formats and mapper classes in one job, relevant to tagged heterogeneous joins.
- Apache Hadoop, [*TotalOrderPartitioner API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/partition/TotalOrderPartitioner.html), checked 2026-09-03. Official range-partition file and total-order partition mechanism.
- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google.com/archive/mapreduce-osdi04.pdf), checked 2026-09-03. Original map/reduce model, local combination, partitioning, ordering, locality, backup tasks, and execution trade-offs.
- Apache Beam, [*Basics of the Beam Model*](https://beam.apache.org/documentation/basics/), checked 2026-09-03. Official current per-element, group-by-key, associative/commutative combine, hot-key decomposition, and bounded/unbounded context.
- Apache Beam, [*Combine*](https://beam.apache.org/documentation/transforms/java/aggregation/combine/), checked 2026-09-03. Official current accumulator combination and partial-aggregation optimization semantics.
- Apache Beam, [*Execution Model*](https://beam.apache.org/documentation/runtime/model/), checked 2026-09-03. Official current shuffle, key colocation, bundle retry, ordering, and runner execution boundaries.

## Exercises

### Exercise 1

For the two mapper partitions in the compact example, calculate raw and locally combined pairs and final sums. Explain why result equivalence does not imply a fixed combiner invocation count.

### Exercise 2

Design mergeable accumulator states for mean and population variance. State numeric, empty-input, NaN, and reproducibility policies.

### Exercise 3

Choose among broadcast, prepartitioned merge, and reduce-side join for a 40-TiB fact table and a 6-GiB dimension with 2,000 workers, 8-GiB containers, duplicate dimension keys, and uncertain partition compatibility.

### Exercise 4

Prove or reject pushing a predicate on the right relation below a left outer join for two intended queries: retaining unmatched facts, and retaining only rows with an active match.

### Exercise 5

Specify validation and named review for optimizing a regulated cross-tenant aggregate with local sketches and broadcast reference data.

## Answers to the Exercises

### Answer 1

Raw emission has seven pairs. Partition 0 combines `a:3,a:2` into `a:5` and keeps `b:1`, emitting two; partition 1 emits `a:4,b:6,c:8`, three. Five partial pairs save two versus raw. Reducer merge yields `a:9,b:7,c:8`. The equality follows from integer addition's defined associative/commutative merge and identity, not from the framework running one combiner per mapper. It may combine spill subsets repeatedly or not at all; the reducer must accept raw singleton accumulators and already merged accumulators equivalently.

### Answer 2

Mean state is `(n,sum)` with lift `(1,x)`, componentwise addition, identity `(0,0)`, and finish `sum/n` for positive `n`. Population variance can use mergeable `(n,mean,M2)`: when merging A and B, `delta=mean_B-mean_A`, `n=n_A+n_B`, `mean=mean_A+delta*n_B/n`, and `M2=M2_A+M2_B+delta^2*n_A*n_B/n`; finish `M2/n`. Define exact integer/decimal or floating precision, overflow, negative-zero, NaN/infinity reject/propagate policy, empty result, and tolerance. Merge order can change floating bits; require a stable tree/higher precision if bitwise reproducibility is mandatory and validate against high-precision reference cases including large offsets with small variance.

### Answer 3

Six GiB cannot safely fit in every 8-GiB container beside runtime, code, buffers, skew, and deserialized expansion; 2,000 uncached copies also create about 12,000 GiB of logical distribution. Broadcast is infeasible without a much smaller projected/filtered unique representation and measured headroom. Prepartitioned merge is unproven because compatibility is uncertain; verify or build matching partition function/count/bounds, encoding, sort, duplicate semantics, and snapshots first. Default to a reduce-side tagged join with early safe projection/filtering, explicit `key -> collection` multiplicity, sampled hot-key handling, bounded spill, and output-size guards. If repeated workload justifies it, establish a reusable co-partitioned layout in an earlier committed stage.

### Answer 4

For “retain every left fact and attach active right rows,” filter right rows to active before the left join; facts with only inactive matches become unmatched and remain with null right fields. Filtering `right.status=active` after the left join removes those null-generated rows under ordinary three-valued WHERE semantics and no longer preserves all facts. For “retain only facts with at least one active match,” prefiltering right then using an inner/semi join is equivalent under defined duplicate semantics; a left join followed by the right predicate also behaves like an inner join. State null status behavior and whether duplicate active matches multiply facts. Predicate placement follows the intended relational expression, not a blanket pushdown rule.

### Answer 5

Pin exact input and broadcast snapshots, schema, tenant/classification, purpose/consent, residency, retention, code/config, sketch algorithm/version/seed/error parameters, and output policy. Prove local accumulator merge laws and cross-tenant grouping authorization; bound sketch error by group and protected class, broadcast memory/copy exposure, hot keys, and spill. Compare exact reference aggregates on stratified/adversarial samples; measure false/error distributions, counters, retries, speculation, committed output, and lineage. Minimize/encrypt broadcast and shuffle data, scope workers, clean caches/attempts, and prevent statistics/log leakage. Named review includes data owners/stewards, affected communities or research-ethics/IRB where applicable, domain/fairness experts, privacy/legal/records/compliance, security/key management, runtime/platform operators, accessibility, incident recovery, and independent assurance. Performance gains cannot silently relax accuracy, fairness, or lawful-use requirements.
