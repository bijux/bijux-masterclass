---
module_id: LSDS-023
program: Large-Scale Data Systems Engineering
level: 1
module_number: 23
title: Partitioners and Combiners
status: complete
last_verified: 2026-09-03
---

# Partitioners and Combiners

## One-Page Review

### Governing question

How should a batch system route intermediate keys and reduce intermediate volume so every logical group remains complete, reducer load is acceptable, optional partial aggregation is correct under arbitrary execution, and output partition meaning is explicit?

### Essential definitions

- A **partitioner** maps each intermediate key/value and reducer count to one reducer number in `[0,R)`.
- A **hash partitioner** derives a reducer from a stable key hash modulo or otherwise mapped to `R`.
- A **range partitioner** assigns ordered key intervals using `R-1` boundaries, enabling partition-ordered output.
- A **grouping key** is the key portion whose equivalent records must reach one reduce call.
- A **hot key** contributes disproportionate records, bytes, CPU, or output to one logical group.
- **salting/fanout** adds a supplementary shard to a hot grouping key for partial work, followed by a merge stage that removes the shard.
- A **combiner** optionally merges mapper-local or spill-local values before shuffle.
- A **mergeable accumulator** has lift, associative merge, identity, and finalization operations with defined representation semantics.
- **partition skew** is imbalance in records, bytes, CPU, spill, or completion time across reducer partitions.

### Central model, mechanism, or theorem

For `R>0`, partitioner `p(k,v,R)` must return one integer in `[0,R)`. If grouping comparator says `k1 ~ k2`, correctness requires `p(k1,v1,R)=p(k2,v2,R)` for all relevant values: one logical group cannot be split across reducers. Load of reducer `r` is not merely its record count; model bytes, per-record CPU, per-group state, output multiplicity, and external limits.

A combiner is correct only if replacing any subset of mapper values by its accumulator leaves the final result unchanged, because it may run zero, once, or repeatedly. With lift `eta`, identity `e`, associative merge `oplus`, and finish `phi`, reducer output for values `V` is `phi(fold(oplus,e,map(eta,V)))`. Commutativity is required when execution order is unspecified. Partitioning decides where; combination decides how much state moves.

### Critical invariants

- Key serialization, hash, equality, sort, grouping, and partition semantics are deterministic and compatible across workers.
- Every grouping-equivalent key reaches the same reducer under the configured `R`.
- The partitioner returns only valid partition numbers, including adversarial keys and values.
- Range boundaries are ordered, versioned, sampled from representative data, and interpreted by the same comparator.
- Reducer sizing uses record, byte, CPU, group-state, and output distributions rather than average keys alone.
- Hot-key salting preserves logical identity through an explicit second-stage merge.
- Combiner correctness does not depend on invocation count, batch boundaries, or mapper order.
- Accumulator types, overflow, floating precision, null/NaN, tie, and empty behavior are explicit.
- Optimization evidence covers mapper cost, spill, shuffle, skew, reducer tails, output layout, and retries.

### Common failures

Frequent failures are using process-randomized hash, partitioning on fields ignored by grouping, returning a negative/out-of-range reducer, changing `R` while treating partition numbers as stable identity, sampling range boundaries from unrepresentative data, measuring only record balance, salting without a merge stage, expecting a combiner to run, reusing the final reducer for an incompatible accumulator type, combining scalar averages or order-sensitive operations, allowing unbounded in-mapper state, hiding overflow, and celebrating shuffle reduction while hot-reducer duration or output-file fragmentation worsens.

### Compact example

Twelve pairs across three maps contain hot key `hot` nine times plus `alpha:2`, `beta:2`, and `gamma:3`. Local integer-sum combination emits six pairs, saving six. A stable byte-sum partitioner with three reducers sends nothing to reducer 0, `beta` and `hot` to reducer 1, and `alpha` and `gamma` to reducer 2. Combination halves pair count but does not fix the empty partition or hot-key concentration; routing and aggregation require separate evidence.

### Connections

[LSDS-003](003-range-hash-and-consistent-partitioning.md) supplies partition functions. [LSDS-021](021-mapreduce-execution-model.md) supplies shuffle/grouping. [LSDS-022](022-map-side-and-reduce-side-processing.md) supplies placement and accumulator algebra. [LSDS-024](../ROADMAP.md) generalizes exchanges across a DAG.

## Governing Question

Partitioners and combiners are small interfaces with system-wide consequences. A partitioner is called for each intermediate record and determines the reducer, shuffle route, load distribution, and often final output file. A combiner can replace many intermediate values with fewer accumulator records before that transfer.

The partitioner carries a correctness obligation: every key considered equal by reduce grouping must go to one reducer. It also carries performance obligations: avoid overload, produce useful output geometry, preserve range contracts when claimed, and remain stable across retries. An apparently uniform hash can still concentrate one intrinsically hot key.

The combiner carries an algebraic obligation: arbitrary partial combination must not change the answer. The runtime controls when and how it runs. Performance depends on mapper-local key repetition, accumulator width, CPU/memory, spills, and skew.

The governing question is how to design and test these interfaces together without confusing correctness, balance, reduction, ordering, and durable partition identity.

## Why This Matters

Shuffle is expensive because records are serialized, buffered, spilled, transferred, fetched, merged, sorted, and grouped. A useful combiner can reduce every downstream step. A good partitioner can spread independent groups across reducers and create output that downstream jobs reuse.

Poor design produces long tails. Ten reducers can each receive the same number of records while one receives values ten times larger. A single hot group can occupy most of a reducer's memory or CPU. Range boundaries learned from old uniform data can collapse under a seasonal or adversarial distribution.

Correctness bugs can be silent. If grouping ignores a secondary field but partitioning includes it, one logical group splits across reducers and yields multiple incomplete outputs. If a floating combiner changes merge order, retries can change low bits. If scalar averages combine, results are systematically wrong while counters look plausible.

Output partitioning becomes an interface. Downstream readers may assume reducer files cover disjoint hash buckets or ordered key ranges. Changing reducer count or hash/boundary version invalidates that assumption unless metadata records the new layout.

## Prerequisites and Retrieval

Recall range, hash, and consistent partitioning from [LSDS-003](003-range-hash-and-consistent-partitioning.md), locality from [LSDS-004](004-data-locality.md), task graphs/stages from [LSDS-005](005-distributed-task-graphs.md) and [LSDS-006](006-stages-tasks-and-dependencies.md), wide dependencies from [LSDS-007](007-narrow-and-wide-transformations.md), and serialization from [LSDS-008](008-serialization-across-workers.md).

Retrieve scale accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md), read/write spills from [LSDS-014](014-read-and-write-pipelines.md), file/output geometry from [LSDS-019](019-small-file-pathologies.md) and [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), MapReduce execution from [LSDS-021](021-mapreduce-execution-model.md), and map/reduce placement plus accumulator laws from [LSDS-022](022-map-side-and-reduce-side-processing.md).

You should understand hashes, ordered ranges, modulo, equivalence relations, comparators, multisets, monoids, distributions/percentiles, sampling, external sorting, task retry, and immutable output manifests.

## Learning Objectives

After completing this module, you should be able to:

- state the partitioner contract and grouping-compatibility theorem;
- implement deterministic hash, field, range, composite, and lookup partitioning;
- explain why reducer count changes partition identity and output layout;
- sample, choose, validate, and version range boundaries;
- diagnose skew by records, bytes, CPU, group state, output, and duration;
- mitigate hot keys with partial aggregation, fanout/salting, or domain redesign;
- define combiner-safe accumulator algebra and representation policies;
- distinguish framework combiners, explicit local aggregation, and runner combines;
- calculate pair/byte reduction, imbalance, fanout, and multi-stage costs;
- test adversarial hashes, comparators, samples, retry trees, and numeric cases;
- preserve provenance, security boundaries, and downstream compatibility; and
- choose when no combiner or a different partition strategy is safer.

## Core Exposition

### Partitioner contract

For each intermediate `(key,value)` and reducer count `R`, the partitioner returns one integer in `[0,R)`. It normally runs in map attempts before records are written into reducer-specific spill segments.

If `R=0`, the job is map-only and no reduce partitioner is needed. If `R=1`, every key goes to reducer zero; many frameworks may bypass custom partition logic. Test supported counts explicitly.

Partition code must be deterministic for stable serialized key/value and job configuration. It must not depend on process seed, clock, locale, mutable remote state, iteration order, or attempt identity.

### Grouping compatibility

Sort defines adjacency; grouping defines which adjacent keys share one reduce call. Partitioning must be no finer than grouping: `k1 ~ k2` implies the same partition. Otherwise equivalent keys can never be reunited within a job.

With composite key `(customer,timestamp)`, secondary sort might sort the entire tuple but group only by customer. The partitioner must use customer, not the full tuple. Including timestamp silently splits customer groups.

Test the invariant property-wise across random and adversarial keys plus every supported `R`, and test canonical serialization/equality/comparator semantics together.

### Stable hash partitioning

Hash partitioning aims to spread distinct keys while keeping equal keys together. Use a specified hash algorithm/seed over canonical bytes and a defined mapping to nonnegative partition range.

Language object hashes may be process-randomized, platform-dependent, or inconsistent with custom equality. Signed minimum values can defeat naive absolute value. Normalize through an unsigned/remainder-safe operation.

Modulo changes most assignments when `R` changes. That is acceptable within one job, but output partition number is not durable identity unless layout metadata includes `R` and hash version.

### Hash quality and adversaries

A uniform hash over diverse keys balances key count probabilistically. Load also depends on key frequency and value size. One repeated key remains one hash bucket.

Poor hashes preserve patterns in prefixes, low bits, or structured numbers. Adversarial inputs can target collisions or reducer overload. Security-sensitive externally chosen keys may require a keyed hash, secret rotation, and denial-of-service controls.

Benchmark avalanche/distribution on real serialized keys and crafted cases. Record algorithm, seed/key version, byte encoding, and collision/load metrics.

### Field and composite partitioning

Sometimes only selected fields define grouping. Parse structured keys unambiguously; delimiter splitting without escaping can collapse distinct tuples. Prefer typed canonical encoding.

Composite partitioning can first isolate tenant/region for policy, then hash within an allowed pool. Ensure every partition destination satisfies residency/access constraints and capacity.

Values can influence partitioning only if grouping compatibility remains true for all values of an equal key. In most keyed reductions, using mutable/value fields is unsafe.

### Range partitioning

Given ordered boundaries `b1 < ... < b_(R-1)`, assign keys to intervals such as `(-inf,b1)`, `[b1,b2)`, ..., `[b_(R-1),+inf)`. Concatenating reducer outputs in partition order can produce total key order when each reducer sorts with the same comparator.

Boundary equality/inclusivity must be exact and consistent. The partition file is versioned job input protected by digest, comparator/schema version, and `R`.

Range partitions enable ordered scans and downstream pruning but expose distribution shifts. An ordered hotspot can overload one range while hash would spread distinct keys.

### Sampling range boundaries

Exact quantiles require examining all keys, defeating the purpose. Sample input splits/records, sort samples, weight them appropriately, and select approximate quantile boundaries.

Sampling must represent partitions, seasons, tenants, file sizes, and key weights. Taking the first records of each already sorted split biases boundaries. Record sampling method, seed, rate, snapshot, exclusions, and confidence/validation.

Duplicate hot keys cannot be divided across ranges without changing grouping. Repeated boundaries need special handling; adding reducers cannot split one logical group.

### Lookup and policy partitioning

A versioned lookup can map keys to fixed shards, owners, or jurisdictions. It enables stable/custom placement and risks a large or mutable control table. Distribute an immutable digest and reject unknown keys according to explicit policy.

Consistent hashing minimizes movement as worker/shard membership changes, but MapReduce reducers are usually dense task numbers for one job. A logical bucket layer can decouple durable bucket identity from current reducer count: map many virtual buckets onto reducers, then record the mapping.

Policy routing must not leak restricted keys through filenames/counters/logs. Validate every target against authorization and residency.

### Reducer count

Choose `R` using total shuffle bytes, key/byte/CPU distributions, target task duration, concurrent reducer capacity, output file targets, and downstream reuse. `R=cluster cores` is merely a rough starting guess.

Too few reducers create long groups, spills, underutilization, and large outputs. Too many create connections, empty/tiny files, scheduler/commit overhead, and per-task startup.

Potential map-reducer relationships are `M*R`. Empty partitions reduce payload, not necessarily all metadata/connection planning. Measure actual fetch topology.

### Measuring skew

For reducer load `L_r`, report max/median, max/mean, coefficient/quantiles, and tail duration across records, bytes, groups, largest group, CPU, spill, fetch, and output. One scalar can hide the real bottleneck.

Sample mapper emissions before full run or use prior runs, but validate online. Data distributions drift. Detect hot keys without logging sensitive raw identities—use approved hashed identifiers or protected diagnostics.

Distinguish partition skew from attempt-specific slowness. Speculation may help a slow machine; it duplicates intrinsic hot partition work.

### Hot-key strategies

First combine mergeable values locally. This can collapse millions of repeated events per mapper to one accumulator, but every mapper can still emit one hot-key partial to the same reducer.

Salt hot key `k` into `(k,s)` across `S` shards, aggregate partials, then shuffle/merge by `k` in a second stage. The algorithm requires mergeable results and deterministic/balanced salt. Random salt needs stable seeding under replay.

For nonmergeable or inherently huge output, salting moves work without shrinking it and may replicate a join side. Revisit product semantics, isolate the group, stream/spill it, or enforce explicit limits.

### Partition evolution and downstream contracts

If output is a reusable bucketed/range layout, record partitioner algorithm/version, canonical key encoding, `R`, boundaries/virtual mapping, comparator, snapshot, and file manifest.

Changing any component creates a new layout version. Downstream map-side joins must match exactly or repartition. Do not infer compatibility from filenames such as `part-00017`.

Range outputs also need min/max/exclusivity validation. Empty partitions can remain represented in metadata without empty physical files if the consumer contract supports it.

### Combiner execution model

The framework can run a combiner as map output spills or merges. It may not run, may process a key in several batches, and may run again on prior combined output. It is not a guaranteed pre-reducer stage.

Therefore reducer input types must accept mapper raw values and combiner outputs, or the framework must expose a distinct typed accumulator contract. Reusing a reducer class is safe only when its input/output algebra matches.

Combiner side effects, counters, ordering assumptions, and cleanup cannot be semantically required. Attempts and spills can duplicate their execution.

### Accumulator algebra

Define `A`, `eta`, `oplus`, `e`, and `phi`. Closure keeps combined outputs in `A`. Associativity permits arbitrary tree grouping. Commutativity permits arbitrary order. Identity permits empty partitions and neutral initial state.

For count, `A` is integer and merge is addition. For mean, `A=(sum,count)`. For top-k, `A` is a bounded candidate set and merge unions/trims using a deterministic total order.

If an operation is order-sensitive, encode order and use a designed secondary sort or deterministic merge protocol; do not pretend it is a combiner.

### Numeric semantics

Fixed-width integer addition can overflow, so specify checked failure, saturation, modular arithmetic, or a wider/exact type. Different policies are different computations.

Floating addition is not associative. Parallel merge trees can produce different low bits. Use higher precision, compensated/pairwise schemes, deterministic trees, interval/error bounds, or tolerances appropriate to consequence.

Define null, missing, NaN, infinity, negative zero, decimal scale/rounding, and empty groups. Version accumulator encoding to prevent old/new merger incompatibility.

### Combiner effectiveness

Let raw mapper output be `N_raw,B_raw` and post-combine output be `N_comb,B_comb`. Pair and byte reductions can differ because accumulators are wider. Track combine input/output records plus serialized bytes.

Effectiveness depends on repeated keys within each combine scope. Globally frequent keys spread one record per mapper after local combine; unique local keys see no reduction.

Combiner CPU, hash tables, sort comparisons, serialization, and spill can outweigh network savings for cheap networks or low repetition. Test no-combine, framework combine, and bounded explicit aggregation.

### Bounded local aggregation

An in-mapper table gives explicit control. Bound it by bytes and entries. When evicting, emit the current accumulator; later occurrences create another partial that reducers merge.

Least-recently-used eviction is not inherently optimal for aggregation and can be nondeterministic. Correctness must be independent of eviction choice. Metrics expose evictions, flushes, peak bytes, and partials per key.

Never retain all distinct keys based on an average-cardinality assumption. Adversarial cardinality must spill or degrade safely.

### Combiner and partition interaction

Combination normally occurs within a mapper before or during partitioned spill. It can be scoped per partition/key batch, but it cannot combine the same key across mappers until reducer-side merge.

If combiner grouping differs from reducer grouping, prove both are compatible with partitioning and accumulator semantics. Partial aggregation on a finer key can later merge to a coarser group only with an explicit transformation.

Changing the partitioner does not change the mathematical aggregate when groups remain complete, but it changes resource distribution and output layout.

### Range order and total order

Hash partitions have no useful global interval order. Range partitions plus per-reducer sorting can establish total order across the ordered output manifest.

Sampled boundaries must use the same raw comparator as mapper sort. Locale/version differences can route a key into one interval but sort it outside expected bounds.

Validate adjacent outputs: maximum of partition `r` must be less than or equal to minimum of `r+1` under the declared duplicate/inclusivity policy. Validate all records lie within recorded bounds.

### Adaptive and skew-aware partitioning

Static MapReduce partitioning is chosen before shuffle. Modern engines may split skewed partitions or coalesce small ones at runtime. Adaptation must preserve grouping/ordering and output identity.

Sampling or mapper statistics can build a second-stage plan. Avoid changing routing mid-stage independently on workers; equal keys could diverge. A coordinator publishes one versioned plan before affected exchange.

Adaptive output partition counts can improve tasks and break downstream bucket compatibility. Record the realized layout, not only requested configuration.

### Failure and replay

Partitioner determinism ensures a retried map emits each record to the same reducer under unchanged job config. If a mutable lookup or random seed changes, reducers can fetch incompatible attempts.

Combiner arbitrary execution and attempt replay require pure/retry-equivalent code. Local partial state rebuilds from the split. External effects remain prohibited or idempotent/commit-mediated.

Boundary/sample/lookup files are job inputs with digests and authorization. A missing or mismatched artifact should fail the attempt, not silently fall back to another partition plan.

### Testing

Property-test valid range, determinism, and grouping compatibility across reducer counts and adversarial key encodings. Distribution-test hash/range/custom partitioners on real weighted data and drift scenarios.

For combiners, compare no-combine results with many random merge trees, singleton batches, empty identity, repeated combining, eviction, retry, and changed ordering. Test overflow, NaN, ties, and serialization round trips.

Integration-test output range/bucket manifests, empty reducers, hot keys, speculative attempts, task loss, boundary artifact failure, object-store commit, and downstream map-side join compatibility.

### Observability and governance

Record partitioner/combiner class and digest, reducer count, key/schema/comparator versions, range/lookup artifact digest, accumulator version, input snapshot, code/config, and output manifest.

Metrics include per-reducer records/bytes/groups/CPU/spill/fetch/output/duration; largest key; combine input/output records/bytes; local table peak/evictions; salt/fanout; retries/speculation; and committed output.

Partitioning determines where sensitive data moves and co-resides. Review residency, tenant isolation, access, encryption, diagnostics, retention, lineage, accessibility, and whether approximate/numerically variable combination is acceptable.

## Definitions and Notation

- `R` is reducer count; valid partition IDs are integers in `[0,R)` for `R>0`.
- `p(k,v,R)` is the partitioner and `~` is reducer grouping equivalence.
- `L_r` is the multidimensional load vector for reducer `r`.
- `b_1...b_(R-1)` are ordered range boundaries under comparator `c`.
- `H` is the hot-key set and `S_k` is fanout count for hot key `k`.
- `A` is accumulator type; `eta`, `oplus`, `e`, and `phi` are lift, merge, identity, and finish.
- `N_raw,B_raw` and `N_comb,B_comb` are pre/post-combine records and serialized bytes.
- `rho_N=1-N_comb/N_raw` and `rho_B=1-B_comb/B_raw` are reduction fractions when denominators are positive.
- `M` is mapper count, making `M*R` the potential map-reducer relation count.

Correctness requires `k1 ~ k2` to imply equal partitions for all relevant values/configuration. Balance is a separate empirical property of `L_r`; valid routing does not imply even work.

## Mechanisms, Invariants, or Proof Structure

Use this partitioner/combiner audit:

1. Pin input, canonical key/value encoding, hash/comparator/grouping, code/config, and reducer count.
2. Prove partition result range, determinism, and grouping-equivalent-key compatibility.
3. Choose hash/range/field/lookup/virtual strategy from ordering, policy, reuse, and distribution requirements.
4. Sample representative weighted load and validate record/byte/CPU/group/output skew plus drift/adversaries.
5. Define accumulator lift/merge/identity/finish, closure, numeric/null/tie rules, and encoding version.
6. Prove output equality for zero/one/repeated combination and arbitrary merge trees.
7. Bound local accumulator memory, spills, side artifacts, hot keys, fanout, and output expansion.
8. Add an explicit merge stage for salted logical keys and record realized partition layout.
9. Test retry/speculation, corrupt/missing boundary artifacts, empty partitions, commit, and downstream compatibility.
10. Measure end-to-end cost and review security, residency, governance, and reproducibility.

The fixture uses a stable byte-sum partitioner only for transparent arithmetic and integer sum as a safe accumulator. It intentionally exposes an empty partition and hot-key concentration.

<!-- bijux-verify: {"id":"partition-and-combine","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"raw_pairs=12 combined_pairs=6 saved_pairs=6 reducers=3\npartition_0=()\npartition_1=(('beta', 2), ('hot', 9))\npartition_2=(('alpha', 2), ('gamma', 3))\nfinal=(('alpha', 2), ('beta', 2), ('gamma', 3), ('hot', 9))\n","stderr":""}} -->
```python
maps = (
    (("hot", 1), ("hot", 1), ("hot", 1), ("hot", 1), ("alpha", 2)),
    (("hot", 1), ("hot", 1), ("hot", 1), ("beta", 2)),
    (("hot", 1), ("hot", 1), ("gamma", 3)),
)
reducers = 3


def combine(records: tuple[tuple[str, int], ...]) -> tuple[tuple[str, int], ...]:
    keys = sorted({key for key, _ in records})
    return tuple(
        (key, sum(value for current, value in records if current == key))
        for key in keys
    )


def partition(key: str) -> int:
    return sum(key.encode("utf-8")) % reducers


partials = tuple(combine(records) for records in maps)
combined = tuple(pair for partial in partials for pair in partial)
reducer_inputs = tuple(
    tuple(pair for pair in combined if partition(pair[0]) == reducer)
    for reducer in range(reducers)
)
outputs = tuple(combine(records) for records in reducer_inputs)
final = tuple(sorted(pair for output in outputs for pair in output))

raw_pairs = sum(len(records) for records in maps)
print(
    f"raw_pairs={raw_pairs} combined_pairs={len(combined)} "
    f"saved_pairs={raw_pairs - len(combined)} reducers={reducers}"
)
for reducer, output in enumerate(outputs):
    print(f"partition_{reducer}={output}")
print(f"final={final}")
```

The combiner halves pair count but cannot split `hot`; partition 0 remains empty. A production hash should be specified and stronger, while hot-key mitigation needs mergeable fanout plus another stage.

The complete proof covers every key, comparator/group invariant, arbitrary combiner schedule, representation semantics, weighted load distribution, attempt replay, committed output, and downstream layout contract.

## Alternatives and Trade-Offs

Hash partitioning needs no sample and balances diverse keys probabilistically. Range partitioning enables ordered intervals and needs representative boundaries. Lookup/policy partitioning expresses ownership and adds control-state management.

Modulo hash is simple and remaps heavily when `R` changes. Virtual buckets provide stable logical layout and an extra mapping layer. Consistent hashing minimizes movement and may not match dense per-job reducer tasks.

More reducers lower average load and increase fanout, tasks, empty/tiny files, and commit work. Fewer reducers simplify output and risk long/skewed tasks.

Framework combiners are optional and simple. Explicit bounded in-mapper aggregation controls flushing and memory. Runner-native typed combines can optimize across stages but require engine support.

Exact arithmetic preserves reproducibility and costs memory/CPU. Floating arithmetic is fast and merge-order sensitive. Approximate sketches bound state and introduce quantified error.

Hot-key salting parallelizes mergeable work and adds a second shuffle. Isolating a hot key into a dedicated reducer is simpler and does not add capacity within that group.

Static partitioning is predictable and can become stale. Adaptive skew handling responds to runtime data and complicates deterministic output/downstream reuse.

Total-order range output supports merge scans and requires sampling, boundaries, comparator consistency, and skew handling. Hash output supports equality distribution without global order.

## Failure Modes and Misconceptions

- **“Valid partition numbers prove a correct partitioner.”** Grouping-equivalent keys must also colocate.
- **“Use the full composite key everywhere.”** Secondary-sort grouping may use only the primary key.
- **“Object hash is stable.”** Language/runtime hashes can be randomized or platform-specific.
- **“Absolute value makes signed hashes safe.”** Minimum signed values and remainder rules need explicit handling.
- **“Uniform hashes eliminate skew.”** One hot logical key remains indivisible.
- **“Equal record counts mean balanced reducers.”** Bytes, CPU, group state, output, and duration can differ.
- **“More reducers split hot keys.”** Equality grouping still sends one key to one reducer.
- **“Range partitioning guarantees balance.”** Samples and future distributions can be skewed.
- **“The first rows are a representative sample.”** Sorted/clustered splits make this badly biased.
- **“Partition numbers are durable business shards.”** Reducer count and algorithm changes remap them.
- **“Salting solves any hot join.”** It can replicate data and cannot shrink intrinsic output.
- **“A combiner is a required stage.”** It may run zero or many times.
- **“The reducer can always serve as combiner.”** Input/output accumulator types and semantics may differ.
- **“Associative mathematics guarantees machine reproducibility.”** Overflow and floating rounding still matter.
- **“Average of averages computes average.”** It ignores unequal counts unless weighted state is retained.
- **“Combining fewer records always saves bytes.”** Accumulators can be wider.
- **“Unbounded in-mapper hash maps are efficient.”** High cardinality can exhaust memory.
- **“Lower shuffle bytes proves a better job.”** Measure CPU, spill, skew, duration, outputs, and governance.

## Worked Examples

### Example 1

**Situation:** Grouping compares only `customer` while sorting uses `(customer,time)`. **Reasoning:** Partition only by customer; partitioning by full tuple splits one customer and invalidates grouping. Full tuple remains the secondary-sort key.

### Example 2

**Situation:** A language hash changes between worker processes. **Reasoning:** Equal serialized keys can route differently across attempts. Specify a stable algorithm/seed over canonical bytes and test vectors across runtimes.

### Example 3

**Situation:** Four reducers have equal record counts but byte totals 2, 2, 2, and 80 GiB. **Reasoning:** The last partition dominates transfer/spill/duration. Sample and route by weighted bytes or isolate/split mergeable heavy keys.

### Example 4

**Situation:** Range boundaries came from the first thousand records of sorted files. **Reasoning:** The sample covers low keys and creates poor quantiles. Sample across splits with weights/randomization and validate the resulting load before full execution.

### Example 5

**Situation:** `hot` appears billions of times and sum is required. **Reasoning:** Combine per mapper, then salt remaining partials across bounded shards, sum by `(hot,salt)`, and sum those results by `hot` in a second stage.

### Example 6

**Situation:** A combiner computes scalar mean. **Reasoning:** Different spill batches have different counts; mean of means is wrong. Emit `(sum,count)`, merge components, and finalize once.

### Example 7

**Situation:** Every key appears once in each map. **Reasoning:** A sum combiner emits the same number of records and possibly larger typed values. Disable it if measured CPU/bytes do not improve.

### Example 8

**Situation:** Top-10 ties are resolved by iterator arrival. **Reasoning:** Retries/merge trees change arrival. Define a total rank such as `(score,stable_id)` and use it for local and final trim.

### Example 9

**Situation:** Downstream assumes `part-00005` is the same bucket after reducer count changes. **Reasoning:** That is false for modulo hashing. Record layout algorithm/version/count or introduce stable virtual buckets.

### Example 10

**Situation:** A custom partitioner routes sensitive tenants by jurisdiction. **Reasoning:** Version and protect the mapping, fail closed on unknowns, validate all destinations, minimize diagnostic key exposure, and review residency/security/operations together.

## Cross-Program Connections

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies hashing, sampling, approximation, weighted distributions, top-k, and adversarial analysis. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hash tables, heaps, external merge, bounded accumulators, and probabilistic sketches.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies hash/range partitioning, grouping, secondary sort, aggregation algebra, histograms, and skew-aware plans. [Data Engineering](../../19-data-engineering/ROADMAP.md) consumes partition layouts, aggregate pipelines, joins, output files, validation, and lineage.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies deterministic replay, consistent hashing, partitions, versioned control state, and commits. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies shuffle fanout, congestion, compression, hot spots, and backpressure.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies scheduler capacity, metrics, configuration distribution, adaptive execution, quotas, and cost. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies keyed hashing, tenant placement, residency, least privilege, diagnostic protection, and audit.

[Programming Languages: Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies associativity, deterministic parallel reduction, races, and representation effects. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies invariants, trade studies, hazards, verification, and named review.

## References

- Apache Hadoop, [*Partitioner API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/Partitioner.html), checked 2026-09-03. Official intermediate key/value and reducer-count to partition contract.
- Apache Hadoop, [*HashPartitioner API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/partition/HashPartitioner.html), checked 2026-09-03. Official default-style hash partition implementation surface.
- Apache Hadoop, [*TotalOrderPartitioner API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/partition/TotalOrderPartitioner.html), checked 2026-09-03. Official split-point partition file and total-order range partition behavior.
- Apache Hadoop, [*InputSampler API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/partition/InputSampler.html), checked 2026-09-03. Official interval, random, and split sampling mechanisms for total-order partitions.
- Apache Hadoop, [*MapReduce Tutorial*](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), checked 2026-09-03. Official partitioner, combiner, comparator, map output, shuffle, reducer-count, and tuning semantics.
- Apache Hadoop, [*Job API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/Job.html), checked 2026-09-03. Official partitioner, reducer, combiner, sort/group comparator, attempts, and job configuration surface.
- Apache Hadoop, [*JobContext API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/JobContext.html), checked 2026-09-03. Official retrieval of reducer count and distinct combiner/reducer grouping comparators.
- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google.com/archive/mapreduce-osdi04.pdf), checked 2026-09-03. Original partition function, local combining, ordering, skew, and execution context.
- Apache Beam, [*Combine*](https://beam.apache.org/documentation/transforms/java/aggregation/combine/), checked 2026-09-03. Official current associative/commutative keyed accumulator and partial-combination guidance.
- Apache Spark, [*RDD Programming Guide*](https://spark.apache.org/docs/latest/rdd-programming-guide), checked 2026-09-03. Official current partitioned key operations, reduce/aggregate by key, shuffle, spill, and partition ordering guidance.

## Exercises

### Exercise 1

Run the compact example by hand: show local combined pairs, partition assignments under byte-sum modulo three, final sums, and why the observed reduction does not prove balance.

### Exercise 2

Prove the partitioner requirement for secondary sort on composite key `(account,event_time,event_id)` when reducers group only by account. Give a failing counterexample.

### Exercise 3

Design and validate range boundaries for one billion weighted records with seasonal skew, duplicate hot keys, and 100 reducers.

### Exercise 4

Specify combiner-safe accumulators for weighted mean and deterministic top 20, including empty, numeric, tie, serialization, and retry behavior.

### Exercise 5

Specify named review and evidence for a jurisdiction-aware partitioner and approximate combiner over regulated records.

## Answers to the Exercises

### Answer 1

Map partials are `(alpha,2),(hot,4)`; `(beta,2),(hot,3)`; and `(gamma,3),(hot,2)`, six pairs versus twelve raw. Byte sums modulo three route beta and hot to partition 1, alpha and gamma to partition 2, and nothing to partition 0. Final sums are alpha 2, beta 2, gamma 3, hot 9. Pair count falls 50%, but load is not balanced: partition 0 is empty and partition 1 contains the hot key. Serialized bytes, CPU, spill, and duration could be even more skewed.

### Answer 2

The sort key may compare all three fields to order events per account, while grouping relation equates keys with the same account. Therefore partitioning must use a canonical account representation: any two keys with equal account must route together. Counterexample: `(A,10,e1)` and `(A,11,e2)` hash differently when the full tuple is used and land on reducers 2 and 7; neither reducer sees account A's complete group. Partition by account, sort by the full tuple with a stable total comparator, group by account, and define duplicate event ties.

### Answer 3

Pin the exact input snapshot and sample across all files/splits, periods, tenants, and size weights using a recorded seeded method rather than leading rows. Estimate weighted key quantiles under the production comparator and choose 99 strictly ordered boundaries, handling duplicate hot keys that cannot be split without semantic salting. Simulate assignments and report per-reducer records, bytes, CPU proxy, largest group, output, max/median, and uncertainty. Oversample seasonal extremes and run drift scenarios. Version/digest boundaries with comparator, encoding, sample, `R=100`, and effective interval rules. Canary the plan on representative data; isolate/salt mergeable hot keys through an explicit second stage rather than repeating equal boundaries.

### Answer 4

Weighted mean accumulator is `(weighted_sum,weight_sum)` with lift `(x*w,w)`, componentwise merge, identity `(0,0)`, and finish division only for permitted nonzero total weight. Define negative/zero weights, decimal/floating precision, overflow, NaN/infinity, and tolerance. Top-20 accumulator is at most 20 `(score,stable_id,payload_ref)` candidates under one total order; merge unions and trims to 20, identity empty. Define duplicate ID policy, score NaN, ascending/descending and tie order. Both encodings carry version and round-trip deterministically; arbitrary merge trees, repeated combination, singleton/empty batches, eviction, task retry, and no-combiner execution must match a reference result.

### Answer 5

Pin schema/key encoding, jurisdiction mapping snapshot/digest, lawful residency rules, reducer destinations, unknown-key policy, code/config, input snapshot, and approximate accumulator algorithm/version/seed/error bounds. Property-test valid routing and grouping compatibility; test every jurisdiction destination, fail closed, drift, adversarial keys, retries, and mapping loss. Compare approximate results to exact stratified/adversarial references by jurisdiction and affected groups; report error distribution, skew, raw/combined bytes, and committed output. Protect keys/mapping/diagnostics, encrypt shuffle/spill, scope identities, preserve lineage, retention, deletion, and accessibility. Named review includes data owners/stewards, jurisdictional privacy/legal/records/compliance, affected communities or research ethics where relevant, domain/fairness/statistics experts, security/key management, runtime/platform/residency operators, accessibility, incident recovery, and independent assurance. Performance or average accuracy cannot waive placement or rights constraints.
