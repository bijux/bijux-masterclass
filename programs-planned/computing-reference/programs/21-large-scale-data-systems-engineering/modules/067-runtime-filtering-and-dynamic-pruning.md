---
module_id: LSDS-067
program: Large-Scale Data Systems Engineering
level: 2
module_number: 67
title: Runtime Filtering and Dynamic Pruning
status: complete
last_verified: 2026-09-04
---

# Runtime Filtering and Dynamic Pruning

## One-Page Review

### Governing question

How should a distributed query engine derive filters from runtime evidence and push them into scans, splits, exchanges, or operators so irrelevant work is safely pruned without losing rows under nulls, outer/anti joins, incomplete build state, retries, or connector semantic differences?

### Essential definitions

- A **runtime filter** is a query-scoped predicate summary derived during execution rather than solely during static planning.
- A **dynamic filter** commonly summarizes join build-side values to reduce probe-side work.
- **dynamic partition pruning** uses runtime values to exclude storage partitions or splits whose partition transforms cannot match.
- An **exact value set** answers membership without false positives or false negatives but may grow with distinct values.
- A **Bloom filter** is a compact approximate membership structure with possible false positives and, under its valid contract, no false negatives.
- A **range filter** records bounds such as minimum and maximum; it is safe only under compatible ordered type/comparison semantics.
- **filter completeness** means every selected build contribution in the declared scope is represented.
- **pruning granularity** is the unit skipped: catalog partition, manifest, file, stripe, row group, page, split, exchange partition, batch, or row.
- **late arrival** occurs when a filter becomes usable after target work has already been scheduled, read, or decoded.
- **selectivity** is the fraction of candidate work retained; pruning benefit also depends on granularity, timing, and target cost.

### Central model, mechanism, or theorem

For join predicate $k_P(p)=k_B(b)$ and a completed build-key set $K_B$, a safe probe prefilter $F$ satisfies

$$F(x)=\text{false}\Longrightarrow x\notin K_B.$$

Thus it may keep nonmatching keys but must never reject a key that could form a qualifying pair in the target join semantics. Exact sets implement precise membership; compatible Bloom filters provide one-sided approximation; min/max ranges keep values within an enclosing interval. Safety additionally depends on join type, residual predicates, null rules, build snapshot/attempt completeness, and where the filter is applied. Benefit is empirical: bytes/work avoided minus build, merge, distribution, wait, memory, and false-positive costs.

### Critical invariants

- Every filter identifies query, join/operator, build side, build snapshot, logical partitions, selected attempts, epoch, type/encoding, algorithm, parameters, and completeness.
- A pruning rejection cannot be a false negative under the exact target semantics and scope.
- Incomplete monotone filters are not used for negative pruning unless the relevant partition/scope is proven complete.
- Join type and preserved side determine which input may be filtered; outer, anti, and null-aware joins are not treated like inner joins.
- Type coercion, collation, time zone, decimal normalization, floating special values, hash, null, and residual semantics match the eventual join.
- Distributed partial filters merge only when algorithms/parameters/types/seeds/epochs are compatible and every selected build partition contributes once.
- Split/file/row-group pruning uses trusted metadata for the same snapshot and distinguishes unknown from impossible.
- Waiting for a filter, filter size, coordinator aggregation, transport, scan queues, and retained build state have bounded policies.
- Retry, speculation, adaptation, cancellation, and connector pushdown cannot mix stale or losing-attempt filters into a new epoch.
- Metrics distinguish work considered, skipped before scheduling, skipped before read, read before filter, false positives, and final matches.

### Common failures

Common failures include pruning from a partially built filter; using a Bloom positive as proof of a match; applying an inner-join rule to a preserved outer side; filtering anti-join rows without exact completeness; forgetting null-aware semantics; merging Bloom bitmaps with different sizes, hash counts, seeds, or encodings; comparing timestamps under different time zones; sending millions of exact keys through the coordinator; waiting longer for a filter than the scan it saves; claiming file pruning after files were already read; trusting stale min/max metadata; counting rows rejected after decode as bytes avoided; reusing a filter after adaptive join replacement; and exposing sensitive key sets or cardinalities through telemetry.

### Compact example

A completed build contains 10,000 distinct keys. A Bloom filter budget of 10 bits per key uses 100,000 bits, or 12,500 bytes. The near-optimal number of hashes is about $10\ln2$, rounded to 7, giving estimated false-positive probability about 0.0082 under the ideal model. A negative can safely reject an ordinary inner-join probe key if all semantic and completeness preconditions hold; a positive still requires the exact join.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) defines storage layout, [LSDS-061](061-distributed-logical-and-physical-plans.md) places filters, [LSDS-063](063-exchange-operators.md) distributes summaries, [LSDS-064](064-distributed-hash-and-merge-joins.md) supplies join semantics, [LSDS-065](065-partial-and-final-aggregation.md) supplies mergeable-state reasoning, and [LSDS-066](066-vectorized-execution-at-cluster-scale.md) applies filters to batches.

## Governing Question

Static optimization knows literals and catalog metadata before execution. Runtime filtering exploits facts learned only after work starts: the small side of a join produced 700 keys, actual key range is narrow, one build partition completed, or a materialized stage reveals which partitions can match. Sending this evidence toward a large probe scan can avoid I/O, decompression, network, and join work.

But a runtime filter is an optimization, not the join result. It must be conservative: retaining extra rows is acceptable, rejecting a true match is wrong. That condition becomes subtle when the build is incomplete, attempts race, nulls have special meaning, the probe side is preserved by an outer/anti join, a connector coerces types differently, or metadata describes a different snapshot.

The governing question is how to prove one-sided safety and scope, publish complete compatible summaries, choose granularity and timing, bound control state, and show actual work avoided rather than merely high row-rejection percentages late in the pipeline.

## Why This Matters

Large fact scans often dominate query latency and cost. If runtime dimension keys eliminate most partitions or row groups, pruning can save orders of magnitude of storage and network work. Dynamic filters also reduce hash probes, exchange traffic, and downstream state. The technique is especially valuable when static predicates do not reveal values until a join input runs.

The risk is silent data loss. A filter built from only some tasks can report absent for a key that appears later. A Bloom filter implemented with mismatched hashes can develop false negatives relative to its consumer. A preserved outer row must remain even when no build key exists. Null-aware anti semantics can depend on whether any build null exists. Stale file statistics can exclude real values.

Operationally, filter creation itself costs memory, CPU, control messages, and latency. A huge exact set can overwhelm the coordinator. A filter arriving after scan completion saves nothing. Waiting for a slow build may lengthen critical path. Design therefore balances safe applicability with timely, bounded evidence.

## Prerequisites and Retrieval

Review storage layouts in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), shuffle in [LSDS-031](031-shuffle-architecture.md), distributed plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator/worker state in [LSDS-062](062-coordinator-and-worker-architecture.md), exchange in [LSDS-063](063-exchange-operators.md), join semantics in [LSDS-064](064-distributed-hash-and-merge-joins.md), mergeable state in [LSDS-065](065-partial-and-final-aggregation.md), and vector filtering in [LSDS-066](066-vectorized-execution-at-cluster-scale.md).

You should understand join types and nulls, sets, hashing, Bloom filters, min/max statistics, partition transforms, columnar files, snapshots, tasks/attempts, manifests, false positives/negatives, control-plane bounds, and query-plan adaptation.

## Learning Objectives

After this module, you should be able to:

1. state the one-sided safety condition for a runtime pruning filter;
2. determine applicability for inner, outer, semi, anti, and null-aware joins;
3. design exact-set, Bloom, range, and composite runtime filter contracts;
4. aggregate distributed build filters with completeness and attempt proofs;
5. translate runtime predicates into partition/file/stripe/row-group/page/split pruning;
6. choose wait, size, timeout, granularity, and fallback policies by expected value;
7. preserve type, null, snapshot, connector, security, retry, and adaptive semantics;
8. distinguish early avoided I/O from late row rejection in telemetry;
9. validate false-negative safety, modeled false positives, failure, and performance; and
10. roll out filtering with shadow decisions, canaries, kill switches, and epoch-aware rollback.

## Core Exposition

### Start from the join semantics

Identify join type, equality keys, residual predicate, preserved side, null behavior, correlation, and snapshot. For an inner equality join, rejecting a probe key absent from the complete build keys is safe. A left semi join can use the same filter to remove impossible left candidates before exact match evaluation.

For outer and anti joins, ask whether the target side's unmatched rows must be preserved. A filter may skip join lookup but cannot discard a preserved row. Null-aware anti joins need special global evidence and cannot inherit ordinary anti rules mechanically.

### State one-sided safety

A pruning structure is sound when every rejected candidate is guaranteed unable to contribute to the logical result at that location. False positives retain extra work but are corrected by the exact operator. False negatives remove required work and are correctness defects.

Write the implication for each target: key, partition, file, or row group. Include residual predicates only if the summary models them soundly. A filter on equality keys alone cannot prove a positive residual match.

### Require build completeness

An exact set or Bloom filter grows as build keys arrive. Before completion, a currently absent key may appear later. Therefore negative decisions from an incomplete global filter are unsafe unless the consumer's relevant build partition is complete or the plan supplies another proof.

Publish completeness over explicit logical build partitions and selected attempts. A timeout can stop waiting and proceed unfiltered; it must not convert incomplete into complete. Empty complete build and missing filter are different states.

### Identify filter lineage

Key every filter by query/plan epoch, logical join, build side and snapshot, build partition set, selected task attempts, key expression/type, algorithm/version/parameters, and generation. Consumers validate lineage before use.

A retried or speculative build may create multiple summaries. Merge only selected compatible attempt contributions once. After adaptive join replacement, old filter identity cannot silently target a differently typed or preserved input.

### Use exact value sets

An exact set provides precise membership under its equality/hash contract and can support discrete partition pruning. It is effective for small distinct build domains. Size depends on distinct encoded keys, not build rows.

Bound entries and bytes, include null presence separately where semantics need it, and choose a fallback before exhaustion. Distributed sets can union after compatible local deduplication. Do not route millions of raw duplicate keys through a coordinator.

### Size Bloom filters deliberately

For $n$ inserted keys, $m$ bits, and $k$ independent ideal hashes, estimated false-positive probability is $(1-e^{-kn/m})^k$, minimized near $k=(m/n)\ln2$. Real hashes, correlations, implementation, and saturation affect observations.

Version bit length, hash count, hash functions/seeds, key canonicalization, and type/null rules. Compatible Bloom filters merge by bitwise OR for union. Different parameters cannot be padded or ORed informally without proof.

### Interpret Bloom answers correctly

Under a correct complete Bloom contract, “definitely absent” safely prunes an ordinary membership candidate; “possibly present” retains work. The final join still evaluates exact keys and residual predicates. False positives cost performance, not correctness.

Do not use Bloom presence as proof for semi output or Bloom absence from an incomplete build as proof for anti output. Monitor saturation and observed pass-to-match ratio, but ground truth requires the exact operator.

### Use range filters with type semantics

Minimum/maximum filters are compact and helpful when build values occupy a narrow ordered range. A probe value below min or above max cannot equal a build key, subject to compatible comparison, type coercion, collation, time zone, NaN, and null semantics.

Incomplete min/max ranges expand as values arrive, so early exclusion outside current bounds is unsafe globally. Multi-interval/range sets improve precision at more size and merge cost. Heavy gaps inside one min/max interval become false positives.

### Combine summaries conservatively

A filter may combine range, Bloom, and exact values: reject when any sound complete component proves impossibility; retain otherwise. Components must describe the same scope and key semantics. A consumer must not intersect summaries from disjoint build partitions as if each were complete globally.

For distributed union, exact sets union, Bloom bitmaps OR, minimum takes min, and maximum takes max. Completeness occurs only after every required logical build partition contributes a selected attempt or is proven empty.

### Target probe rows and vector batches

Row/batch filtering happens late but saves hash probes, residual evaluation, output, and downstream work. A vectorized kernel applies the summary only to active valid keys and produces a selection vector. It never replaces exact join evaluation for retained rows.

Measure candidates, rejected, retained, exact matches, and false-positive survivors. Late filtering may still be valuable even when no scan bytes are saved, but report its actual layer.

### Prune exchange partitions

If build evidence proves certain probe hash/range partitions cannot contain matches under a compatible distribution, the engine can avoid producing, transmitting, or consuming them. The proof must connect filter semantics to the exchange's versioned ownership function.

Do not confuse “no build keys observed in partition” with complete empty partition. Attempt selection and exchange epoch matter. Preserved-side rows may still need downstream processing even if join lookup is unnecessary.

### Prune scan splits dynamically

Before scheduling a split, compare filter constraints with partition metadata, file statistics, or manifest transforms. If intersection is impossible under trusted snapshot metadata, omit the split. If metadata is missing, truncated, corrupted, or semantically incomparable, retain it.

Track splits considered, skipped before assignment, already assigned, canceled before read, partially read, and completed. Canceling active reads has cost and connector-specific safety; late filters may apply only to future splits.

### Translate partition transforms

Tables may partition by identity, bucket, truncate, year/month/day/hour, or other transforms. Translate a runtime key predicate only through the exact transform specification. Hidden partitioning can let the engine derive partition predicates without exposing physical columns to SQL.

Transform pruning is usually conservative: many source values map to one partition. Hash/bucket versions and counts, time-zone/date interpretation, truncation, null handling, and snapshot evolution must match. Partition-spec changes may coexist across files.

### Use file and row-group metadata

Min/max, null counts, dictionaries, Bloom filters, and page indexes can prove that a file, stripe, row group, or page cannot match. Trust only metadata covered by integrity and same-snapshot semantics. Truncated statistics may remain conservative but less selective.

Columnar formats differ in type encoding and index granularity. A runtime filter may first prune manifests/files, then row groups, then rows. Count savings at each boundary without double counting.

### Push filters into connectors

Negotiate connector support for exact sets, ranges, Bloom structures, partition transforms, types, collation, time zone, nulls, snapshots, cancellation, and telemetry. A connector can accept all, part, or none and return residual responsibility.

Treat external sources as semantic boundaries. If the connector cannot prove conservative rejection, use the filter inside the engine only. Scoped credentials and query identity protect filter contents in transit.

### Decide whether to wait

Waiting for a selective filter may save a huge scan; waiting for a slow or nonselective build may extend critical path. Estimate target bytes/work, filter ready time, target startup/read rate, expected selectivity, and overlap. Use a bounded wait followed by unfiltered progress where safe.

Policies can delay only expensive partitions, start small splits, or apply late filters to remaining work. Avoid a global barrier when independent targets can proceed. Record why a scan waited and how much was subsequently saved.

### Bound filter state and control traffic

Limit distinct keys, serialized bytes, coordinator aggregation, merge CPU, broadcast destinations, retained generations, and per-query/filter counts. Use tree aggregation or exchange service rather than funneling every key through one coordinator.

On bounds, choose a declared fallback: Bloom, range, coarser partition summary, disabled filtering, or plan adaptation. Never truncate an exact set and continue labeling negative membership exact.

### Handle outer joins

For a left outer join, build-side-derived filtering of the preserved left/probe input cannot discard nonmatches; those rows must appear null-extended. The filter may optimize lookup or target a non-preserved input under a proven alternate plan, but not erase preserved rows.

Right/full outer joins require symmetric reasoning. Match tracking and unmatched emission wait for complete relevant inputs. Apply a filter only at a plan location where rejected rows truly cannot contribute to required matched or preserved output.

### Handle semi and anti joins

For a left semi join, a complete build filter can safely discard left keys definitely absent, while possible presence requires exact evaluation. For ordinary left anti join, definite absence can identify a candidate that likely qualifies, but residuals, build completeness, and output timing still matter.

Null-aware `NOT IN`-like semantics may make one build null affect all probe results. Carry exact null-presence/completeness state and implement the dialect's three-valued logic. A Bloom bitmap alone is insufficient.

### Preserve composite-key semantics

Canonicalize the full key tuple with field boundaries, types, null components, collation, and coercions. Hashing concatenated ambiguous bytes can collide semantically beyond the Bloom filter's intended approximation. Range summaries on tuples require lexicographic semantics matching the join.

Partial filters on a subset of equality keys can still be conservative for inner join if absence on that component proves no full match. They may be less selective and require correct null/coercion rules.

### Integrate dynamic filters with security

Build keys may be sensitive, and filter size/bits/ranges can leak cardinality or domain information. Authorize target consumers, encrypt transport/storage, expire filters with the query, and redact explain/metrics. Do not push a filter across a trust boundary that may infer protected values without policy approval.

Row-level security and masks affect which build keys the query is permitted to observe. Generate filters after security semantics and bind them to the same principal/policy snapshot. Cross-tenant caches are generally unsafe without a stronger proof.

### Recover retries and failures

Filter fragments are attempt-scoped. Coordinator or tree aggregation selects complete build contributions under the query epoch. If a selected build task is retried, either replace its contribution in a rebuildable structure or create a new filter generation; non-invertible OR cannot remove losing bits.

False-positive leftovers from a losing Bloom contribution preserve correctness but can hide lineage and degrade results; stricter generation rebuild is easier to reason about. Never omit the winning contribution. On filter-service failure, proceed unfiltered if the join itself remains sound.

### Adapt without stale application

Runtime filtering may trigger partition pruning, join distribution changes, or scan replanning. Each decision captures target snapshot and work state. A new plan/exchange epoch invalidates incompatible filters and consumers.

Bound adaptations and avoid repeatedly canceling near-complete scans. Retain a no-filter correctness path. Rollback disables pruning without needing to reconstruct rows already unsafely skipped—hence correctness must be proven before actuation.

### Observe effectiveness by stage

Correlate query/join/build attempts/filter generation/target scan or exchange. Emit build rows/distinct/nulls, construction/merge/publish time, bits/entries/range, saturation, bytes, completeness, wait, consumers, and rejection/match counts.

For target work, report partitions/files/row groups/pages/splits/bytes/rows considered and skipped before each irreversible cost. Measure false-positive retained rows against exact matches, target latency, critical path, CPU/memory/network saved, and control cost. “90% filtered” after full read is not 90% I/O saved.

### Validate safety and value

Differentially compare filtering disabled/enabled under identical snapshots. Generate empty/incomplete builds, duplicates, null/composite keys, type coercions, outer/semi/anti/null-aware joins, residuals, hash collisions, saturated Bloom filters, range gaps, partition-spec evolution, and stale/missing metadata.

Property-test no false negatives for supported key encodings and compatible merges. Inject task retry/speculation, lost contribution, late arrival, coordinator restart, connector error, filter corruption, cancellation, and adaptive replacement. Shadow prune decisions, canary, and kill-switch on any result mismatch.

## Definitions and Notation

Let build bag be $B$, probe bag $P$, build-key function $k_B$, probe-key function $k_P$, and complete selected build key set $K_B=\{k_B(b):b\in B\text{ contributes}\}$. Runtime filter $F$ is safe for ordinary inner equality rejection when $F(x)=0\Rightarrow x\notin K_B$ under compatible key semantics.

For Bloom filter with $m>0$ bits, $n>0$ inserted distinct keys, and $k>0$ ideal hashes, estimated false-positive probability is $p=(1-e^{-kn/m})^k$ and near-optimal $k=(m/n)\ln2$. These formulas assume idealized independent uniform hashing.

Let target candidates be $C$, retained candidates $R$, exact matching candidates $M\subseteq R$, with false-positive survivors $R\setminus M$. Filter retention is $|R|/|C|$ for $|C|>0$, but scan benefit depends on work skipped before scheduling/read/decode.

Let logical build partitions be $L$. Completeness vector $c_l$ records a selected complete contribution for each $l\in L$. A global negative decision is enabled only when every required $c_l=1$, unless the target is provably scoped to a completed subset.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Fix join type/preserved side, keys/coercions, residuals, null behavior, snapshot, security, and target plan location.
2. Write the no-false-negative implication for rows, exchange partitions, splits, files, or metadata units.
3. Choose exact, Bloom, range, composite, partition-transform, or metadata summary with versioned types/parameters.
4. Build and merge selected attempt-scoped contributions; publish explicit logical-partition completeness and epoch.
5. Bound keys/bits/ranges, memory, merge/distribution, wait, coordinator state, consumers, and retained generations with safe fallback.
6. Negotiate connector/storage semantics and treat missing, stale, truncated, or incomparable metadata as unknown rather than absent.
7. Apply only to future/eligible work, preserve outer/anti/null-aware semantics, and invalidate filters on incompatible adaptation.
8. Correlate construction, publication, wait, target work state, pruning granularity, false positives, outcomes, security, and cost.
9. Differential/property test no false negatives and join equivalence across types, nulls, partitions, filters, and merge orders.
10. Fault-inject attempts/completeness/transport/connectors, shadow decisions, canary with kill switch, and roll back by generation.

For a complete sound membership summary, rejecting a key reported absent preserves an inner equality join because no build row with that key exists. The implication does not authorize emitting a positive match, discarding preserved outer rows, or operating on incomplete state.

Bitwise OR merges compatible Bloom filters for set union: every bit set by any selected build key remains set. This preserves no-false-negative behavior under the same hash/size/seed/encoding contract, while false positives may increase as occupancy rises.

Late filter benefit is bounded by remaining avoidable work. Rows rejected after a file is read cannot be credited as file I/O savings. Stage-specific counters make the cost claim falsifiable.

## Alternatives and Trade-Offs

- **No runtime filter:** simplest correctness and no wait/state; may scan and shuffle irrelevant data.
- **Exact set:** precise membership and partition lists; memory/control size grows with distinct keys.
- **Bloom filter:** compact and mergeable with one-sided error; false positives and parameter compatibility matter.
- **Min/max range:** tiny and effective on clustered values; gaps and unordered semantics reduce value.
- **Multiple ranges:** better gap precision; more state, merge, and transport.
- **Partition-value list:** excellent for small discrete domains; cardinality can explode.
- **Row-level filtering:** saves join/downstream CPU; often too late to save storage I/O.
- **Split/file pruning:** saves expensive reads; depends on timely trusted metadata and translation.
- **Wait for completion:** maximizes potential pruning; delays probe critical path.
- **Start immediately:** no filter wait; late arrival may save little.
- **Tree filter aggregation:** scales coordinator pressure; adds merge levels and publication delay.
- **Coordinator aggregation:** simple authority; key/bitmap cardinality can bottleneck.
- **Connector pushdown:** prunes near source; crosses semantic, security, and telemetry boundaries.
- **Engine-side filter:** controlled semantics; source bytes may already be paid.
- **Rebuild on retry:** clean lineage; spends build/merge time again.
- **Monotone over-approximation:** keeps extra losing bits safely in some joins; degrades precision and complicates audit.

## Failure Modes and Misconceptions

- **“Runtime filter is the join.”** retained rows still require exact key/residual evaluation.
- **“Bloom positive means present.”** false positives are permitted.
- **“Bloom has no false negatives automatically.”** incompatible hashes, encoding, corruption, or incomplete build break the premise.
- **“A partial filter can only improve.”** negative absence can become false when later keys arrive.
- **“Timeout implies completion.”** it only ends waiting; proceed unfiltered.
- **“Empty filter means empty build.”** missing, failed, incomplete, and complete-empty states differ.
- **“Inner-join pruning applies to outer joins.”** preserved rows cannot be discarded.
- **“Anti joins benefit symmetrically.”** completeness, residuals, output timing, and null awareness differ.
- **“Null is just another hashed key.”** ordinary equality and null-aware semantics require explicit treatment.
- **“OR any Bloom bitmaps.”** size, hashes, seeds, encodings, type, and epoch must match.
- **“Min/max is safe for every type.”** collation, time zone, NaN, coercion, and truncation matter.
- **“Partition names reveal semantics.”** transforms, counts, versions, and spec evolution define mapping.
- **“Metadata absence means value absence.”** missing/untrusted statistics mean unknown.
- **“Rows filtered equals bytes saved.”** timing/granularity determine avoided cost.
- **“Exact sets scale until memory fills.”** control, serialization, broadcast, and coordinator load also bind.
- **“Old filters remain conservative after adaptation.”** sides, types, epochs, and targets may change.
- **“Filter telemetry is harmless.”** keys, ranges, cardinalities, and occupancy can leak data.
- **“Performance tests prove correctness.”** enabled/disabled differential results and no-false-negative properties are required first.

## Worked Examples

### Example 1

Three of four build tasks have published exact key sets. Key 9 is absent so far but appears in the fourth. Pruning probe key 9 before fourth-task completion loses matches. The consumer waits, proceeds unfiltered, or uses a proven partition-local completion boundary.

### Example 2

A complete Bloom filter reports probe key 17 may be present. The row remains and the hash join finds no exact key because this was a false positive. Correctness holds; observed false-positive work informs sizing.

### Example 3

A left outer join preserves fact rows. A build-derived filter says fact key 91 is absent. Discarding the fact row is wrong because it must appear with null-extended dimension fields. The engine may skip lookup but must retain outer output.

### Example 4

A null-aware anti join sees a build-side null in the last completing partition. An earlier ordinary Bloom summary lacked null state. Emitting probe rows before exact global null/completeness evidence violates three-valued semantics.

### Example 5

Runtime dates map through an Iceberg day transform and exclude most manifests. Older files use a month partition spec. The planner translates through each file's declared spec rather than applying current day partition IDs universally.

### Example 6

A range `[100,120]` arrives after 80% of a fact file is decoded. It rejects most remaining rows but cannot claim that completed file bytes were pruned. Metrics separate late row rejection from early split/file savings.

### Example 7

Two Bloom fragments use 1,000,000 bits but different seeds. Bitwise OR is not a compatible union. The aggregator rejects the contribution pair and falls back to no filter or rebuilds under one contract.

### Example 8

An exact set exceeds its 8 MiB bound. Truncating it would make “absent” unsound. Policy converts from all selected keys into a parameterized Bloom filter, publishes only after complete rebuild/merge, or disables filtering.

### Example 9

A filter waits 12 seconds to save a scan that normally finishes in 4 seconds. Critical path regresses despite high pruning. A bounded 500 ms wait then unfiltered/late application wins for that workload; thresholds remain empirical.

### Example 10

The fixture computes an idealized Bloom configuration from distinct-key count and bits per key.

<!-- bijux-verify: {"id":"bloom-filter-sizing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bits=100000\nmemory_bytes=12500\nhashes=7\nestimated_fpr=0.0082\n","stderr":""}} -->
```python
import math

distinct_keys = 10_000
bits_per_key = 10
bits = distinct_keys * bits_per_key
hashes = round(bits_per_key * math.log(2))
false_positive_rate = (1 - math.exp(-hashes * distinct_keys / bits)) ** hashes

print(f"bits={bits}")
print(f"memory_bytes={bits // 8}")
print(f"hashes={hashes}")
print(f"estimated_fpr={false_positive_rate:.4f}")
```

The model assumes ideal independent uniform hashes and a complete compatible filter. Production design validates real keys, occupancy, hash implementation, serialization, and observed false-positive work.

## Cross-Program Connections

- **Probabilistic data structures:** Bloom filters, hashing, false-positive models, sketches, and saturation shape summaries.
- **Database systems:** join types, nulls, residuals, dynamic filters, partitions, indexes, snapshots, and plans define safety.
- **Distributed systems:** tasks, attempts, completeness, epochs, aggregation, retries, partial failure, and late messages define lineage.
- **Data engineering:** manifests, partition transforms, files, row groups, page indexes, schemas, and scan bytes determine pruning.
- **Platform engineering:** coordinator memory, RPC, exchange, connector capabilities, cancellation, isolation, and telemetry host filters.
- **Reliability engineering:** safe fallback, no-false-negative tests, corruption, kill switches, canaries, and rollback bound risk.
- **Security and governance:** build keys, ranges, cardinality, row policy, connector trust, encryption, expiry, and redaction protect data.
- **Performance engineering:** selectivity, granularity, timing, wait, build/merge cost, false positives, critical path, and full cost establish value.

## References

1. Trino. [Dynamic Filtering.](https://trino.io/docs/current/admin/dynamic-filtering.html) Current collection, coordinator/worker distribution, split pruning, connector support, join applicability, statistics, and configuration.
2. Trino. [Optimizer.](https://trino.io/docs/current/optimizer.html) Current dynamic filtering, pushdown, statistics, join, and connector optimization overview.
3. Trino. [Pushdown.](https://trino.io/docs/current/optimizer/pushdown.html) Current predicate, projection, aggregate, join, limit, top-N, and connector-pushdown boundaries.
4. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current adaptive execution, join conversion, skew, partitioning, statistics, and file-scan tuning context.
5. Apache Spark. [Configuration.](https://spark.apache.org/docs/latest/configuration.html) Current SQL/runtime configuration surface, including dynamic partition-pruning and execution controls where supported.
6. Apache Iceberg. [Partitioning.](https://iceberg.apache.org/docs/latest/partitioning/) Current hidden partitioning, transforms, evolution, pruning, and query semantics.
7. Apache Parquet. [Page Index.](https://parquet.apache.org/docs/file-format/pageindex/) Current column/offset indexes, min/max/null metadata, page skipping, and boundary order.
8. Apache ORC. [ORC Specification v1.](https://orc.apache.org/specification/ORCv1/) Current stripes, row indexes, Bloom filter indexes, type encodings, statistics, and predicate-related metadata.
9. Velox. [Operators.](https://facebookincubator.github.io/velox/develop/operators.html) Current hash join dynamic filters, scan pushdown, split skipping, operator, pipeline, and exchange architecture.
10. Bloom. [Space/Time Trade-offs in Hash Coding with Allowable Errors.](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/p422-bloom.pdf) Primary Bloom-filter paper defining compact membership with allowable false positives.
11. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary account of distributed query operators, filtering, partitioning, and production execution.
12. Meta Engineering. [Presto: Interacting with Petabytes of Data at Facebook.](https://engineering.fb.com/2013/11/06/core-infra/presto-interacting-with-petabytes-of-data-at-facebook/) Primary account of distributed coordinator/worker, stage, task, split, connector, and pipeline architecture.
13. Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets.](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) Primary account of distributed columnar scans, serving trees, and interactive pruning-oriented execution.

## Exercises

### Exercise 1

For 2 million distinct keys and 12 bits per key, compute Bloom bit/byte size, near-optimal integer hash count, and idealized false-positive probability. State assumptions and correctness interpretation.

### Exercise 2

Construct an applicability table for build-derived filtering of left/probe input under inner, left outer, right outer, full outer, left semi, ordinary left anti, and null-aware anti joins.

### Exercise 3

Design distributed filter aggregation for 1,000 build tasks with retry and speculation. Include exact/Bloom/range states, completeness, attempts, bounds, tree merge, epochs, and fallback.

### Exercise 4

Design multi-level dynamic pruning for an Iceberg table with evolving partition specs and Parquet row groups. Cover transforms, snapshots, metadata trust, late filters, connector behavior, and metrics.

### Exercise 5

Design a validation and rollout campaign for runtime filtering across mixed connectors. Include semantics, property tests, failures, security, performance, shadowing, canarying, kill switch, and rollback.

## Answers to the Exercises

### Answer 1

$m=2{,}000{,}000\times12=24{,}000{,}000$ bits, or 3,000,000 bytes. Near-optimal $k=12\ln2\approx8.32$, so compare supported integers around 8; with $k=8$, ideal $p=(1-e^{-8/12})^8\approx0.00314$. This assumes complete insertion of distinct keys, independent uniform compatible hashes, no corruption, and consistent encoding. A negative is safe only because the implemented filter has no false negatives under those premises and the join/target allows pruning; a positive is not proof of membership.

### Answer 2

For inner join, complete build absence can discard the probe row. Left semi likewise discards definite nonmatches but exact join proves positives. Left outer preserves the left/probe row, so it cannot be discarded; lookup may be skipped and null-extended output retained. Right outer does not preserve left/probe, so pruning may be safe for matched output if build/right completeness and semantics align, though role naming must be checked. Full outer preserves it, so no discard. Ordinary left anti ultimately keeps definite absences, but exact completeness, residuals, and output timing are required; a filter is not the whole anti join. Null-aware anti additionally requires global build-null state and dialect three-valued logic. For every row, key coercions, nulls, snapshot, and residual location can narrow applicability.

### Answer 3

Each logical build task emits an attempt-scoped summary tagged with query/join epoch, key type/encoding, algorithm/version, and parameters. A fenced selector chooses one complete attempt per task. Tree nodes merge exact sets by union, compatible Bloom bitmaps by OR, and ranges by min/max; they track a bitmap/range of covered logical tasks, not message count. Publish global completeness only after all 1,000 selected contributions or proven-empty partitions arrive. Bound entries/bits/bytes, tree fan-in, merge CPU, coordinator root state, time, generations, and distribution. On exact-set overflow rebuild/convert soundly to one Bloom contract or disable; never truncate. On retry after publication, create a replacement generation or use a rigorously conservative rebuild path. Timeout releases consumers unfiltered. Consumers reject stale/incompatible epochs.

### Answer 4

Bind filter and table metadata to one snapshot. For each manifest/data file, translate values through that file's partition spec—identity, bucket, truncate, or temporal transforms with exact versions/counts/time semantics—because several specs can coexist. Prune manifests/files only when transformed domains cannot intersect. For remaining Parquet files, apply trustworthy column/page indexes and min/max/null metadata with compatible physical/logical types; unknown/truncated/incomparable metadata retains work. Push through the connector only under a negotiated conservative contract. A late filter affects unscheduled splits, may cancel unread work safely, and filters rows for already-open files. Measure units considered/skipped at manifest, file, row-group/page, split, byte, and row layers plus work already read, wait, false positives, and final matches without double counting.

### Answer 5

Differentially run filters disabled/enabled over inner/outer/semi/anti/null-aware joins with empty/incomplete builds, duplicates, null/composite/coerced keys, residuals, saturated/collision-heavy Bloom filters, ranges with gaps/NaN/time zones/collations, partition evolution, and missing/stale metadata. Property-test no false negatives for every supported encoding/hash/merge/version. Inject retries, speculation, lost contributions, late arrival, coordinator restart, corruption, connector rejection/error, cancellation, and adaptive replacement. Verify tenant-scoped authorization, encrypted transport, expiry, and redacted keys/ranges/cardinality. Measure stage-specific avoided partitions/files/pages/splits/bytes/rows, wait, build/merge/transport memory/CPU, false-positive work, critical path, and cost. Shadow prune decisions against executed truth, canary low-risk queries/connectors, kill-switch on any mismatch or lineage/bound violation, and roll back filter/plan epochs while allowing the unfiltered exact join path.
