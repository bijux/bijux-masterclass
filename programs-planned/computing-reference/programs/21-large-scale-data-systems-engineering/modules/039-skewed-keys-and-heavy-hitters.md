---
module_id: LSDS-039
program: Large-Scale Data Systems Engineering
level: 1
module_number: 39
title: Skewed Keys and Heavy Hitters
status: complete
last_verified: 2026-09-03
---

# Skewed Keys and Heavy Hitters

## One-Page Review

### Governing question

How can a distributed data system detect, explain, and safely mitigate keys or partitions that dominate records, bytes, memory, CPU, state, network, output, or elapsed time without weakening grouping, join, ordering, retry, privacy, or approximation guarantees?

### Essential definitions

- A **heavy hitter** is an item whose frequency or weight exceeds a declared threshold, commonly $f_x>\phi N$ for total weight $N$ and fraction $\phi$.
- **key-frequency skew** is unequal row multiplicity across keys; **partition skew** is unequal workload across execution destinations.
- **byte skew** arises from variable-width rows or states; **compute skew** from unequal per-record/group work; **output skew** from result multiplicity.
- A **straggler** is a task whose completion controls a stage tail; skew is one cause among locality, failure, throttling, contention, and heterogeneous resources.
- **skew factor** often compares a partition maximum or upper quantile with a median, but requires an absolute floor to avoid classifying tiny differences as incidents.
- A **candidate detector** returns keys that might be heavy; an **exact verification pass** counts candidates against authoritative data.
- A **false positive** is a reported non-heavy key; a **false negative** is an omitted true heavy key under the declared threshold.
- **salting** adds a subkey to split one natural key; correctness usually requires a second aggregation or controlled opposite-side replication.
- **Count-Min Sketch** estimates nonnegative frequencies with hashed counters and one-sided collision error under stated width/depth assumptions.
- **Misra–Gries/Space-Saving summaries** retain bounded candidate sets for frequent-item discovery, with algorithm-specific count/error guarantees.

### Central model, mechanism, or theorem

For partition workload $w_0,\ldots,w_{P-1}$, define $w_{max}=\max_j w_j$ and robust baseline $m=median(w_j)$. A practical skew trigger may require both $w_{max}\ge T$ and $w_{max}/\max(m,m_0)\ge \gamma$, where $T$ is an absolute work threshold, $m_0$ prevents division by a near-zero baseline, and $\gamma$ is a relative factor. Repeat this model separately for rows, serialized/expanded bytes, CPU, spill, state, output, and duration.

With $k-1$ counters, Misra–Gries processes an insertion-only stream by incrementing a tracked item, adding into a free counter, or decrementing all counters when full. Every item with frequency greater than $N/k$ remains a candidate, but candidate counters are not necessarily exact; a second pass verifies. For Count-Min with suitable independent hashes, width about $e/\epsilon$ and depth about $\ln(1/\delta)$ give a nonnegative point estimate that does not underestimate and exceeds true frequency by at most roughly $\epsilon N$ with probability at least $1-\delta$ under the standard model. State exact parameter rounding, hash assumptions, update model, and query scope.

Detection does not determine remediation. A decomposable aggregation can salt a hot key and re-aggregate partial states. An inner join can split one hot group and replicate the smaller opposite group so every pair has exactly one owner. A full outer join needs additional unmatched-row coordination. An arbitrary per-group function may be inherently unsplittable. The mitigation proof belongs to the operator's semantics.

### Critical invariants

- Key normalization, equality, hash, null/NaN/collation rules, weight definition, snapshot/window, and threshold are pinned.
- Metrics distinguish input rows, encoded/expanded bytes, group/state size, CPU, spill, network, output, duration, retries, and placement.
- Detector algorithm, parameters, seeds, merge/version contract, error type, and candidate/verified status are recorded.
- No exact claim is made from a sample or approximate summary without an exact verification path.
- Every original record or required pair is assigned to exactly one semantic output owner after salting/splitting.
- Partial aggregation combines only through valid algebra; join replication preserves multiplicity and outer unmatched ownership.
- Adaptive skew plans use immutable plan/partition/skew generations and cannot mix pre- and post-split output.
- Memory, disk, network, replication, number of hot keys, salt fan-out, tasks, metadata, and output are bounded.
- Retry/speculation accepts one logical contribution; slow-task speculation does not duplicate expensive work or results.
- Sensitive key identities, frequencies, sketches, salts, samples, and diagnostics follow access, privacy, retention, and deletion policy.

### Common failures

Common failures include diagnosing only total shuffle bytes; using mean rather than tails/median; dividing by a zero median; calling any slow task “key skew”; assuming uniform hashing splits a repeated key; increasing partitions without treating hot groups; selecting salts from stale global statistics; independently salting both join sides and losing cross-salt pairs; replicating both sides and duplicating pairs; salting an outer join without unmatched ownership; combining a non-associative aggregate; treating sketch estimates as exact counts; ignoring false-positive/false-negative mode; merging incompatible sketch seeds; placing raw identifiers in metric labels; speculating tasks whose bottleneck is shared output; and retaining sensitive hot-key lists indefinitely.

### Compact example

Partition row counts `(120,20,18,16,14,12,10,10)` have median 15 and maximum-to-median factor 8. A trigger requiring at least 64 rows and factor 4 flags the 120-row partition; a ratio-only trigger would also flag `(8,2,2,2)` despite negligible work. In a 24-item stream with 12 `hot`, 6 `warm`, and six singleton keys, a Misra–Gries summary with three counters retains `hot` and `warm` as candidates. Exact verification against threshold $N/4=6$ classifies only `hot` because the definition uses strictly greater than.

### Connections

[LSDS-003](003-range-hash-and-consistent-partitioning.md) supplies partition functions, [LSDS-023](023-partitioners-and-combiners.md) supplies grouping algebra, [LSDS-031](031-shuffle-architecture.md) through [LSDS-034](034-hash-based-shuffle.md) expose exchange tails, and [LSDS-035](035-broadcast-joins.md) through [LSDS-038](038-distributed-aggregation.md) provide operator-specific mitigation constraints. [LSDS-040](../ROADMAP.md) integrates these controls into wide-transformation cost design.

## Governing Question

Distributed stages finish when their slowest required tasks finish. Equal partition counts do not imply equal work: one destination may receive most records, one key may have huge values, one join group may produce a Cartesian explosion, or one worker may host several heavy buckets. Averages make such tails disappear on dashboards while users wait for the maximum.

A heavy hitter is a data property relative to a metric and scope. “Customer 42 is heavy” is incomplete without saying whether it contributes 8% of rows, 30% of bytes, 70% of CPU, or a million-by-million join product, and over which snapshot/window. A skewed partition is an execution property: several medium keys can collide or placement can concentrate work without any globally heavy key.

Detection ranges from exact counts to samples and streaming summaries. Exact pre-counting can cost another scan/shuffle. Samples can miss concentrated or newly emerging keys. Bounded summaries produce candidates and error intervals, not omniscience. Runtime partition statistics arrive late but reflect the actual intermediate data.

Mitigation is semantic. Summation can distribute one key through partial states. A join must cover every pair. A sort can split between keys easily but not within one equality group if the consumer requires the whole group. An arbitrary group UDF may truly require one worker. No generic “skew optimization” proves all of these.

The governing question is how to measure the right work dimensions, select detection evidence with explicit error, choose a semantics-preserving split or fallback, and operate it safely under stale statistics, failures, sensitive keys, and bounded resources.

## Why This Matters

One hot destination can waste an otherwise idle cluster. Ninety-nine tasks finish in seconds while one spills for an hour. Adding workers or partitions does not help if a single key remains indivisible. Autoscaling may increase cost without shortening the critical path.

Skew causes cascading failures. A large build partition exceeds memory, recursive spill fills disk, retries repeat the same deterministic placement, speculative copies double storage/network pressure, and downstream sinks see an output burst. What begins as a tail problem becomes an availability problem.

Wrong remediation corrupts data. Naive join salting omits pairs. Replication can duplicate pairs. Outer joins can emit an unmatched row once per salt. Partial aggregation can change non-associative results. Adaptive splitting after output escapes can mix generations.

Heavy-hitter detection also has security implications. A rare disease code, high-value account, or targeted user can be inferred from top-key dashboards or sketches. Metric labels with raw keys create high-cardinality telemetry and a secondary data store. Approximation does not provide privacy by itself.

A disciplined system treats skew as a measured, multidimensional, operator-specific control problem. It knows when a key is actually the cause, what accuracy the detector provides, what semantics a split must preserve, and what new costs the remedy creates.

## Prerequisites and Retrieval

Retrieve partitioning, locality, serialization, failures, and scale accounting from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve integrity, metadata, and lifecycle from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review grouping and combining in [LSDS-023](023-partitioners-and-combiners.md), attempt identity and tracing in [LSDS-027](027-task-retry-and-speculation.md) through [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md), and shuffle/join/aggregation mechanics in [LSDS-031](031-shuffle-architecture.md) through [LSDS-038](038-distributed-aggregation.md). You should understand distributions, quantiles, hashes, streaming summaries, confidence/error, multiset joins, monoids, spill, backpressure, snapshots, retries, and commit protocols.

## Learning Objectives

After this module, you should be able to:

1. distinguish key-frequency, byte, compute, state, output, partition, placement, and infrastructure skew;
2. define heavy-hitter and skew thresholds with units, scope, strictness, absolute floor, and robust baseline;
3. compute exact frequencies and interpret samples, Misra–Gries, Space-Saving, and Count-Min evidence;
4. state false-positive, false-negative, additive-error, confidence, hash, and update-model contracts;
5. merge distributed detector state or verify candidates without double counting attempts;
6. design semantics-preserving aggregation salting, join splitting/replication, and range-boundary repair;
7. recognize inherently indivisible group work and use resource/failure alternatives;
8. version adaptive skew plans and bound replication, salts, tasks, memory, disk, network, and output;
9. validate detection and mitigation using adversarial distributions and fault injection; and
10. protect key identities, counts, sketches, samples, telemetry, and retained plans throughout their lifecycle.

## Core Exposition

### Define the metric and scope

Frequency can mean row count, positive integer weight, bytes, revenue, requests, or state updates. A key heavy by count may be cheap; a key with ten multi-gigabyte objects may be heavy by bytes. Define the numerator and total $N$, plus the snapshot, time window, tenant, partition epoch, and preprocessing filters.

Top-$k$ asks for the largest $k$ items; threshold heavy hitters asks for all $x$ with $f_x>\phi N$. These are related but not identical when estimates overlap or ties cross $k$. “Frequent” should name strict `>` versus `>=` semantics.

Execution skew uses actual work $w_j$. Record separate vectors for rows, encoded and expanded bytes, CPU, allocation, spill, network, output, blocked time, and duration. A composite score can support ranking, but retain the components for diagnosis.

### Use robust partition summaries

Mean is distorted by the very tail being diagnosed. Median and upper quantiles provide robust baselines. Maximum-to-median ratio is intuitive, but median can be zero when many partitions are empty. Clamp the denominator or condition on nonempty partitions and report emptiness separately.

Use a dual threshold: an absolute minimum $T$ and relative factor $\gamma$. A 10-byte partition versus 1-byte median has factor 10 but no operational consequence. A 500 GiB maximum versus 200 GiB median has factor 2.5 and may still be unacceptable.

Track maximum/median, p95/median, coefficient of variation or Gini when useful, and share of total held by top partitions. Thresholds are service/resource decisions, not universal constants.

### Separate cause from symptom

A slow task might read equal bytes from a throttled disk, lose locality, suffer GC, wait for output, share a noisy worker, or retry. Correlate destination counts/bytes/groups with CPU, spill, I/O, network, placement, failures, and downstream backpressure.

If the same logical partition is slow across retries and workers, data shape is likely. If slowness follows a host, infrastructure is likely. If many tasks block on one sink, upstream salting will not repair the bottleneck.

Trace plan, exchange, partition, attempt, worker, source blocks, output, and resource timelines. Do not “fix skew” before proving which resource owns the tail.

### Exact detection

Exact frequency counting groups every normalized key and sums weights. It provides definitive candidates but may require the same expensive shuffle that is being planned. A smaller projected key/weight scan can reduce bytes, and existing statistics/indexes may help if snapshot-compatible.

Two-pass detection is often practical: a bounded first pass generates candidates, then a second pass counts only candidates exactly. The second pass must use the identical snapshot, normalization, weight definition, and threshold denominator.

Exact runtime map-output statistics identify skewed partitions after producers finish. They may not reveal keys unless separately instrumented, but can support partition splitting. Late evidence must feed an effect-free adaptive boundary.

### Sampling

Uniform row sampling estimates frequent keys cheaply, but a key near threshold can be missed. Clustered storage, unequal partition samples, filters, time bursts, and weighted items complicate inference. Use inclusion probabilities and confidence intervals rather than scaling raw sample counts blindly.

Samples underrepresent rare but huge rows when diagnosing bytes. Byte-weighted or stratified sampling may answer a different question. Adversarial or correlated input can defeat naive assumptions.

Record sample design, fraction, seed, strata, snapshot, estimator, uncertainty, and minimum detectable frequency. A sample produces evidence for planning, not an exact correctness oracle.

### Misra–Gries candidates

Maintain at most $k-1$ `(item,counter)` entries. For each insertion: increment if tracked; add with one if space exists; otherwise decrement every counter and remove zeros. Each all-counter decrement can be paired with $k$ distinct stream items, bounding discarded mass.

Every item with true frequency greater than $N/k$ remains in the final candidate set. Stored counters underestimate true frequency by bounded discarded mass; they are not exact. Count candidates in a second pass for exact classification.

The summary is useful because memory depends on $k$, not domain cardinality. Weighted, deletion, mergeable, and distributed variants require their own proofs; do not assume the simplest insertion algorithm transfers unchanged.

### Space-Saving candidates

Space-Saving tracks a bounded set. A hit increments its counter; on a miss at capacity, replace a minimum-count item and initialize the new estimate using the displaced count plus incoming weight, retaining an error term. It often gives strong practical top-$k$ estimates.

Reported estimate and error interval matter. A candidate's lower bound can support no-false-positive reporting; an upper bound can support no-false-negative reporting under a threshold, depending on the implementation guarantee.

Merging summaries is not the same as concatenating their displayed top items. Use the library's specified merge and compatible sizes/versions/weight models, then test guarantees.

### Count-Min Sketch

Create a $d\times w$ counter table with one hash per row. A nonnegative update of item $x$ increments one cell per row. Query returns the minimum addressed counter. Collisions add mass, so the standard estimate never undercounts in an insertion-only exact-counter model.

With standard independence assumptions, $w=\lceil e/\epsilon\rceil$ and $d=\lceil\ln(1/\delta)\rceil$ yield additive error approximately $\epsilon N$ with failure probability at most $\delta$ for a point query. Union bounds for many queries require adjusted confidence. Counter overflow, conservative updates, deletions, and weak/adversarial hashes alter the contract.

Count-Min does not retain key identities. Candidate discovery needs a separate dictionary/sample/heap or queries for known keys. Merge tables only when dimensions, hash functions/seeds, counter semantics, normalization, and generation match; merge by cellwise addition.

### Exact verification and gray zones

Given candidate intervals $[L_x,U_x]$ and threshold $\tau$, classify definitely heavy when $L_x>\tau$, definitely non-heavy when $U_x\le\tau$, and uncertain otherwise. Exact-count uncertain candidates if the optimization requires no false decisions.

No-false-negative mode may include extra candidates and apply a harmless mitigation with bounded overhead. No-false-positive mode avoids unnecessary replication but can miss heavy work. Choose from consequence, not convenience.

Keep threshold denominator exact or bounded. An uncertain $N$ widens classification. Version candidates with snapshot/window and discard stale lists when distribution changes.

### Distributed detector merging

Exact maps merge by key addition, but can be as large as domain. Count-Min tables merge cellwise under identical hash identity. Some frequent-item summaries expose specific merge algorithms; use those rather than inventing one from output rows.

Partial detector states are non-idempotent for counts. Accept one attempt per input partition. Speculative duplicates inflate estimates and can create false hot keys. Tree merging bounds coordinator fan-in.

Record processed weight per summary and reconcile it against input evidence. A missing partition can create false negatives; a duplicated partition can create false positives. Checksums and complete manifests precede classification.

### Turn detected keys into a skew plan

A skew plan maps natural keys or partitions to strategies, salt counts, ownership, replication, resource class, and fallback. It includes detector evidence, confidence, snapshot, plan/partition generation, hash/normalization, and expiration.

Choose salt count from measured work and target per-task capacity, then cap it. $s_x=\lceil w_x/C\rceil$ is a starting estimate for key work $w_x$ and target $C$, not a guarantee because output and per-row costs vary.

Limit total hot keys and replication. Thousands of false-positive keys each salted 100 ways can overwhelm scheduler and metadata even if individual tasks shrink.

### Salt decomposable aggregation

For associative mergeable aggregation, route each record `(x,v)` to `(x,salt)` across $s_x$ subkeys, compute partial states, remove salt, and merge states for $x$. Every input record has one salt owner, so no multiplicity is lost or duplicated.

This distributes input transition and state building. The second-stage merge still has one logical key, but sees $s_x$ compact states instead of raw rows. It does not help a non-combinable collection whose state remains all values.

Salt selection can be deterministic from stable record identity for replay, or attempt-scoped with exact ownership. Avoid process randomness that changes coverage under retry unless output is fully fenced and regenerated.

### Split skewed joins

For an inner hot key with groups $A_x$ and $B_x$, partition one group into $s$ disjoint subsets and replicate the complete other group to each. Each pair belongs to exactly one subset cross complete group, preserving $|A_x||B_x|$.

Replicate the smaller group when possible, but consider row width, expanded build memory, residual predicates, and output. Independently salting both groups matches only equal salts and omits cross-salt pairs. Replicating both creates duplicates unless a grid scheme assigns each block pair uniquely.

Left/right outer, semi, and anti joins constrain splittable sides. Replicated preserved rows can emit unmatched multiple times. Require designated ownership or reconciliation. Full outer often needs more coordination or a different fallback. Validate the engine's exact supported orientation.

### Split sort and general group operations

Range partitions can move boundaries to distribute many distinct heavy ranges. A single repeated key cannot be divided if downstream requires one contiguous group. Sort-merge joins can split the hot group with join-specific replication.

An arbitrary `groupByKey().apply(f)` may need every value together and expose no mergeable state. Options are a larger resource class, spillable group iterator, domain-specific decomposition, approximation, workload isolation, or explicit rejection. Pretending it decomposes is incorrect.

For ordered group functions, split ranges only when order/reconciliation semantics are proven. Stable global rank or first/last can require boundary metadata.

### Address byte and compute skew

Frequency sketches miss wide rows. Track serialized and expanded bytes by key/partition using bounded summaries or sampled widths. One key with few enormous blobs may require streaming large-record paths, projection, compression, or separate routing.

Compute weights can be learned from operator timing/counters. A regex, model inference, decompression, or external call may vary by record. Weighted heavy-hitter summaries can track integral cost proxies, but feedback loops and noise need smoothing/versioning.

Output skew may be predictable from join frequency products or aggregate state growth. Admit downstream capacity before splitting upstream work into a larger synchronized burst.

### Adaptive runtime handling

Runtime producer statistics are more accurate than stale catalogs. After blocking/hybrid exchange materialization, an adaptive planner can split eligible skewed partitions, coalesce tiny ones, change parallelism, or choose a different join strategy before consumer effects commit.

Adaptation creates a new plan/skew generation with explicit input ranges and output owners. Consumers cannot mix old unsplit and new split contributions. Reuse immutable exchange blocks when the new plan can address subranges safely.

Thresholds must combine actual work and relative imbalance. Record why a partition was split, how many subpartitions resulted, what was replicated, and whether tail improved.

### Speculation, retry, and feedback

Speculating a data-bound straggler repeats the same hot work and can double network/disk/output pressure. Speculation helps only if another worker or transient condition can run it faster and commit fencing prevents duplicate results.

Retries keep the same skew plan or coherently advance the whole dependent generation. Do not choose a different random salt mapping for one producer while consumers retain old routing. Accepted attempt manifests define exact input coverage.

Feed observed distributions into future planning with snapshot/time/tenant context and expiration. A yesterday-heavy key can disappear; a new campaign can emerge. Feedback is evidence, not a permanent hard-coded exception.

### Observability

Record per-partition rows, encoded/expanded bytes, groups, state/build sizes, input/output pairs, CPU, allocation, spill, network, blocked time, duration, locality, worker class, retry, and failure. Report median, p95/p99, maximum, absolute values, ratios, and top-share.

For detectors record algorithm/version, threshold, strictness, total weight, dimensions, seeds/hash identity, counters/capacity, sample design, merge tree, error bounds/confidence, candidates, verification, and false-decision policy.

For mitigation record key via controlled digest/token, salt count, split ranges, replicated side/bytes, new tasks, plan generation, fallback, output owners, before/after tails, and overhead. Keep raw sensitive keys out of general telemetry and bound label cardinality.

### Validation and fault injection

Generate uniform, Zipf-like, one-hot, many-hot, adversarial-hash, wide-row, expensive-record, high-output, empty, and rapidly changing distributions. Compare detector candidates/intervals with exact counts. Test thresholds exactly below/at/above strict boundaries.

Property-test Misra–Gries inclusion for items above $N/k$, Count-Min non-underestimation/additive error under its model, compatible sketch merges, and exact verification. Vary partitions, order, merge trees, seeds, counter widths, and overflow.

Differentially compare mitigated and unmitigated operator output multisets for aggregation and every supported join type. Inject missing/duplicate detector partitions, corrupt state, stale lists, worker loss, speculation, cancellation, adaptive plan switch, disk/memory/network limits, auth failure, and sink retry. No mixed generation or partial result may commit.

### Security, privacy, and governance

Heavy-key lists can expose popular or rare people, diagnoses, accounts, locations, attacks, or business events. Tokenize or use access-controlled digests where operationally sufficient; remember dictionary attacks can reverse low-entropy keys. Keep mapping services and seeds protected.

Apply least privilege, tenant/region isolation, encrypted transport/storage, authenticated sketches/manifests, redacted logs, bounded telemetry, and audited access. Candidate verification may require raw keys and therefore a narrower execution boundary.

Retention covers samples, exact counts, sketches, candidate lists, skew plans, salts, replicated join groups, spill, traces, dashboards, and keys. Expire distribution evidence, honor holds explicitly, and verify deletion. Approximation is not differential privacy; formal privacy requires a defined mechanism, budget, and composition analysis.

## Definitions and Notation

- $f_x$: true frequency or nonnegative weight of key $x$ in the declared scope.
- $N=\sum_x f_x$: total stream weight.
- $\phi$: heavy-hitter fraction; a strict heavy hitter satisfies $f_x>\phi N$.
- $w_j$: measured workload of execution partition $j$ in one named unit.
- $T,\gamma,m_0$: absolute threshold, relative skew factor, and baseline floor.
- $k$: Misra–Gries parameter using at most $k-1$ counters.
- $\epsilon,\delta$: Count-Min additive-error fraction and point-query failure probability under its model.
- $s_x$: salt/subpartition count for natural key $x$.
- **candidate interval** $[L_x,U_x]$: algorithm-supported lower and upper bounds on $f_x$.
- **skew generation**: immutable detector evidence, threshold, split/replication map, ownership, and plan identity.

## Mechanisms, Invariants, or Proof Structure

1. Freeze key/weight normalization, scope, snapshot/window, units, and strict threshold semantics.
2. Measure multidimensional partition work and distinguish data skew from host, locality, retry, or sink effects.
3. Select exact, sampled, candidate-summary, sketch, or runtime detection with explicit error/coverage contract.
4. Merge only compatible complete accepted detector states; verify uncertain candidates exactly when required.
5. Map each confirmed workload to operator semantics and decide whether it is decomposable or indivisible.
6. Choose bounded salts/splits/replication/resources/fallback and assign every input/pair/unmatched result one owner.
7. Publish one skew generation before effects; fence retry, speculation, and adaptive replacement.
8. Admit memory, disk, network, task/metadata, detector, replication, state, and output costs.
9. Differentially validate results and detector guarantees under adversarial distributions and failures.
10. Measure before/after tails and overhead, expire evidence, and delete sensitive artifacts after references/holds end.

Misra–Gries inclusion follows from decrement events: each full decrement accounts for $k$ distinct occurrences, so at most $N/k$ such events occur. An item occurring more than $N/k$ times cannot have all occurrences canceled and must remain a candidate. Its stored counter need not equal its true count, which motivates verification.

Correct aggregation salting follows because input rows are partitioned disjointly among salts and valid partial states merge to the natural-key state. Correct one-sided join splitting follows because $A_x=\biguplus_i A_{x,i}$, so $A_x\times B_x=\biguplus_i(A_{x,i}\times B_x)$. Outer joins add unique unmatched ownership; independent two-side salts do not satisfy this equality.

No detector proof establishes operational benefit. A statistically heavy key might be cheap, while a non-heavy wide or expensive key dominates. Mitigation effectiveness requires before/after resource and tail measurements.

## Alternatives and Trade-Offs

**Exact counting** gives definitive frequencies but costs scan/state/shuffle. **Sampling** is cheap and early but uncertain near thresholds and sensitive to design. **Runtime partition statistics** are exact for actual intermediates but arrive late and may hide key identities.

**Misra–Gries/Space-Saving** retain candidates with bounded memory. Their stored estimates and merge properties differ. **Count-Min** answers point frequencies with one-sided collision error but needs an external candidate source.

**No-false-negative reporting** protects against missed hot keys while spending extra mitigation. **No-false-positive reporting** avoids unnecessary overhead while accepting misses. **Exact verification** resolves the gray zone at extra cost.

**More ordinary partitions** helps multi-key imbalance, not a repeated key. **Aggregation salting** is cheap for compact mergeable states. **Join replication** distributes products while adding network/memory. **Larger workers/spill** preserve one-group semantics at infrastructure cost.

**Static skew lists** plan early and can exploit domain knowledge but become stale. **Adaptive splitting** uses actual data but requires materialization, plan fencing, and engine support. **Fail-fast limits** are appropriate when required output or state exceeds service guarantees.

## Failure Modes and Misconceptions

1. **“The mean partition is healthy.”** Tail tasks, not means, close the stage.
2. **“A high max/median ratio is always serious.”** Add an absolute work threshold and denominator floor.
3. **“Every straggler is key skew.”** Host, locality, GC, retry, throttling, and sinks can dominate.
4. **“Heavy by rows means heavy by cost.”** Bytes, CPU, state, and output require separate measurement.
5. **“A good hash spreads a hot key.”** Equality sends repeated keys together unless semantics-aware splitting intervenes.
6. **“More partitions fixes every tail.”** An indivisible group remains large and overhead rises.
7. **“Sketch estimates are exact.”** State error type, bounds, confidence, and query scope.
8. **“Count-Min finds key names.”** It estimates queried items; candidate discovery is separate.
9. **“A Misra–Gries counter is the frequency.”** It is a candidate summary; verify for exact classification.
10. **“Top-k and threshold heavy hitters are identical.”** Ties and overlapping intervals differ.
11. **“Merge any summaries by unioning their outputs.”** Use the algorithm's compatible state merge.
12. **“Salt both join sides.”** Independent salts omit cross-salt pairs.
13. **“Replicate both sides.”** Unowned replication duplicates pairs.
14. **“Outer joins split like inner joins.”** Preserved unmatched rows need exactly-one ownership.
15. **“Any group function can re-aggregate.”** Only sufficient mergeable state permits it.
16. **“Speculation fixes data skew.”** It commonly duplicates the same deterministic bottleneck.
17. **“Yesterday's hot-key list is permanent truth.”** Distribution evidence has snapshot and expiry.
18. **“Hashed telemetry is anonymous.”** Low-entropy keys are vulnerable to dictionary inference.

## Worked Examples

### Example 1

Counts `(120,20,18,16,14,12,10,10)` have median 15 and max/median 8. An absolute 64-row and relative 4-times policy flags only material imbalance.

### Example 2

Counts `(8,2,2,2)` have ratio 4 but only 14 rows. A ratio-only alert wastes effort; the absolute threshold suppresses it.

### Example 3

A key is 20% of rows but contains tiny records and a constant-time sum. Another is 0.5% of rows but has 5 MiB blobs. Frequency and byte skew choose different remediation.

### Example 4

For $N=10^9$, $\epsilon=0.001$, and $\delta=10^{-6}$, standard Count-Min sizing gives width about 2,719 and depth about 14; the point error allowance is roughly one million weight with the stated confidence/model.

### Example 5

A Misra–Gries summary with $k-1=99$ counters must retain every item above 1% of an insertion-only stream as a candidate. It can retain additional items and its counters require verification.

### Example 6

A sum key with 600 million values is salted 100 ways. Local states each summarize about six million values, then 100 states merge. The same technique cannot make `collect_list` bounded.

### Example 7

A join hot key has 10 million left rows and 20 right rows. Splitting left 100 ways and replicating 20 right rows produces 2,000 routed right rows and preserves 200 million pairs.

### Example 8

If both sides in Example 7 independently choose 100 salts, only about 1/100 of cross-salt combinations meet. Equality of salt is not equality of natural-key pair ownership.

### Example 9

A full outer join replicates a preserved build row across 20 splits. If no probe match exists, naive tasks emit 20 unmatched rows. A designated owner or global reconciliation must emit exactly one.

### Example 10

This fixture computes a robust partition trigger and demonstrates candidate generation followed by exact verification.

<!-- bijux-verify: {"id":"heavy-hitter-detection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"median=15.0 maximum=120 skew_factor=8.0 flagged=True\nitems=24 threshold=6 candidates=('hot', 'warm') verified=('hot',)\n","stderr":""}} -->
```python
from collections import Counter
from statistics import median

partition_rows = (120, 20, 18, 16, 14, 12, 10, 10)
baseline = median(partition_rows)
skew_factor = max(partition_rows) / baseline
flagged = max(partition_rows) >= 64 and skew_factor >= 4
print(
    f"median={baseline:.1f} maximum={max(partition_rows)} "
    f"skew_factor={skew_factor:.1f} flagged={flagged}"
)

stream = ["hot"] * 12 + ["warm"] * 6 + [f"x{i}" for i in range(1, 7)]
k = 4
counters = {}
for item in stream:
    if item in counters:
        counters[item] += 1
    elif len(counters) < k - 1:
        counters[item] = 1
    else:
        counters = {key: count - 1 for key, count in counters.items() if count > 1}

exact = Counter(stream)
threshold = len(stream) // k
candidates = tuple(sorted(counters))
verified = tuple(sorted(item for item in candidates if exact[item] > threshold))
print(
    f"items={len(stream)} threshold={threshold} "
    f"candidates={candidates} verified={verified}"
)
```

The fixture validates one deterministic insertion-only candidate trace, exact verification, strict threshold, and skew arithmetic. It is not a proof for weighted/deletion/merged summaries, a statistical benchmark, or a distributed mitigation simulation.

## Cross-Program Connections

- **Algorithms Engineering:** Streaming summaries, probabilistic bounds, adversarial hashing, sampling, and exact verification underlie detection.
- **Data Structures Engineering:** Counter maps, sketches, heaps, histograms, spill, and compact candidate state determine memory and merge behavior.
- **Database Systems Engineering:** Cardinality statistics, join multiplicity, aggregation algebra, adaptive plans, and physical properties determine legal repairs.
- **Data Engineering:** Real distributions, evolving hot entities, partitions, incremental pipelines, and quality rules shape detector scope and expiry.
- **Distributed Systems Engineering:** Attempts, immutable exchanges, adaptive generations, speculation, backpressure, and commit fencing preserve coverage.
- **Platform Engineering:** Scheduling, heterogeneous resources, network/storage quotas, autoscaling, telemetry, and workload isolation influence tails.
- **Security Engineering:** Key-frequency evidence can identify people and attacks, requiring constrained observability, privacy analysis, and deletion.
- **Systems Engineering:** Skew couples data, algorithms, runtime, infrastructure, sinks, costs, and governance; local tuning can move the bottleneck.

## References

1. J. Misra and David Gries, [Finding Repeated Elements](https://www.cs.utexas.edu/~misra/scannedPdf.dir/FindRepeatedElements.pdf), *Science of Computer Programming* 2(2), 1982.
2. Richard M. Karp, Scott Shenker, and Christos H. Papadimitriou, [A Simple Algorithm for Finding Frequent Elements in Streams and Bags](https://www.cs.umd.edu/~samir/498/karp.pdf), *ACM TODS* 28(1), 2003.
3. Graham Cormode and S. Muthukrishnan, [The Count-Min Sketch and Its Applications](https://umaal.org/teaching/cscix32-spring-2024/lectures/countmin_sketch.pdf), *Journal of Algorithms* 55(1), 2005.
4. Ahmed Metwally, Divyakant Agrawal, and Amr El Abbadi, [Efficient Computation of Frequent and Top-k Elements in Data Streams](https://www.cs.emory.edu/~cheung/Courses/584/Syllabus/papers/Frequency-count/2005-Metwally-Top-k-elements.pdf), 2005.
5. Apache DataSketches, [Frequent Items Sketches Overview](https://datasketches.apache.org/docs/Frequency/FrequentItemsOverview.html), accessed 2026-09-03.
6. Apache Spark, [Performance Tuning: Adaptive Skew Join](https://spark.apache.org/docs/latest/sql-performance-tuning.html), accessed 2026-09-03.
7. Apache Spark, [PySpark DataFrame.freqItems](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.freqItems.html), accessed 2026-09-03.
8. Apache Spark, [Tuning: Reduce-Task Memory and Parallelism](https://spark.apache.org/docs/latest/tuning.html), accessed 2026-09-03.
9. Apache Flink, [Adaptive Batch: Load Balancing and Skewed Join Optimization](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/adaptive_batch/), accessed 2026-09-03.
10. Apache Flink, [Table Configuration: Skewed Join Optimization](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/config/), accessed 2026-09-03.
11. Apache Flink, [AdaptiveSkewedJoinOptimizationStrategy API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/table/runtime/strategy/AdaptiveSkewedJoinOptimizationStrategy.html), accessed 2026-09-03.
12. Fuheng Zhao et al., [SpaceSaving±: An Optimal Algorithm for Frequency Estimation and Frequent Items in the Bounded-Deletion Model](https://vldb.org/pvldb/vol15/p1215-zhao.pdf), *PVLDB* 15(6), 2022.

## Exercises

### Exercise 1

Partition bytes are `(0,0,0,64,80,96,128,2048)` MiB. Compute the ordinary median, explain the denominator problem, and evaluate a trigger with $T=512$ MiB, $m_0=64$ MiB, and $\gamma=8$.

### Exercise 2

For an insertion-only stream of $N=50$ million items, design standard Count-Min dimensions for $\epsilon=0.0005$ and $\delta=10^{-5}$. Compute approximate width, depth, cells, and additive error allowance; state assumptions and limitations.

### Exercise 3

Prove why Misra–Gries with $k-1$ counters includes every item with frequency greater than $N/k$, and explain why a second pass remains necessary for exact reporting.

### Exercise 4

A hot inner-join key has 3 million left rows averaging 120 bytes and 2,000 right rows averaging 400 bytes. Design a 50-way split, compute required pair count and one-sided replicated logical bytes, then describe outer-join changes.

### Exercise 5

Design a privacy-aware runtime skew controller for tenant-scoped healthcare aggregations and joins. Include metrics, detector error, candidate verification, plan identity, admission, retry, validation, retention, and oversight.

## Answers to the Exercises

### Answer 1

Sorted values are unchanged; the ordinary median is $(64+80)/2=72$ MiB despite three empty partitions. The maximum is 2,048 MiB and the denominator is $\max(72,64)=72$, giving factor about 28.44. It exceeds both 512 MiB and factor 8, so it is flagged. If the median were zero, $m_0$ would prevent division by zero and ratio inflation. Also report three empty destinations and nonempty quantiles; the baseline choice is policy, not a universal theorem.

### Answer 2

Standard sizing gives $w=\lceil e/0.0005\rceil\approx5{,}437$ and $d=\lceil\ln(10^5)\rceil=12$, or about 65,244 counters. The additive allowance is $\epsilon N=25{,}000$ weight for one queried item with failure probability at most $10^{-5}$ under independent suitable hashes, insertion-only nonnegative updates, exact non-overflowing counters, and the standard analysis. Count-Min does not retain item names, estimates can overcount through collisions, many simultaneous queries need adjusted confidence, and adversarial keys/weak hashes, deletions, merges, or conservative updates require their own contract.

### Answer 3

Each full decrement cancels one occurrence from $k$ distinct items: the incoming untracked item plus the $k-1$ tracked items. Therefore at most $\lfloor N/k\rfloor$ full decrements occur. An item appearing more than $N/k$ times cannot have all occurrences canceled, so it remains tracked. Its stored counter is its uncanceled residual, not the true frequency, and non-heavy items may remain. An exact second pass over the same snapshot counts candidates and applies the strict threshold without false positives.

### Answer 4

Partition the three million left rows disjointly into 50 groups of about 60,000 and replicate all 2,000 right rows to each. Required inner output is $3{,}000{,}000\times2{,}000=6$ billion pairs. One-sided replicated right payload is $50\times2{,}000\times400=40{,}000{,}000$ bytes, versus 800,000 bytes once, so added copies cost about 39.2 MB decimal before headers/compression. Each pair has one owner because each left row has one salt. For left outer with left split, each left row remains uniquely owned and can emit unmatched after seeing complete right. If preserved rows are replicated, designate unmatched ownership. Full outer needs matched tracking/reconciliation for the replicated right group or a different strategy.

### Answer 5

Scope every key/weight and statistic by tenant, authorized region, snapshot/window, and purpose. Measure rows, encoded/expanded bytes, state/build, CPU, spill, network, output, and duration with robust tails; use protected tokens rather than raw patient/clinic keys. Pin detector/version/hash/seed/threshold/error mode, merge only complete accepted summaries, and exactly verify gray-zone candidates in a restricted boundary. Publish an immutable skew generation with salts, split ownership, replicated side, limits, and fallback before effects. Admit aggregate memory/disk/network/task/output and cap hot keys/fan-out. Fence attempts and keep snapshot/routing stable across retry. Differentially validate unsplit versus split results including nulls, duplicates, joins, outer unmatched ownership, missing/duplicate summaries, failures, and sink commit. Encrypt and audit states/plans/spill, restrict cross-tenant/region access, set expiry and holds, verify deletion, and involve data owners, platform, security, privacy/legal/records, clinical governance, regional authorities, and affected tenant representatives.
