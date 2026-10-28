---
module_id: LSDS-021
program: Large-Scale Data Systems Engineering
level: 1
module_number: 21
title: MapReduce Execution Model
status: complete
last_verified: 2026-09-03
---

# MapReduce Execution Model

## One-Page Review

### Governing question

How does a MapReduce runtime turn deterministic record transformations into a distributed batch result while partitioning work, shuffling intermediate data, retrying failed attempts, and committing exactly one logical output per successful task?

### Essential definitions

- An **input split** is a logical range assigned to one map task; a record reader converts it into complete input key/value records.
- A **map function** transforms one input record into zero or more intermediate key/value pairs.
- A **partitioner** maps each intermediate key to exactly one reducer number.
- The **shuffle** transfers each mapper's partition to its destination reducer.
- **sort/group** orders intermediate keys and presents all values equivalent under the grouping comparator as one reducer input group.
- A **reduce function** transforms one grouped key and iterable/multiset of values into zero or more output pairs.
- A **task attempt** is one execution of a logical map or reduce task; failure or speculation can create several attempts.
- An **output committer** makes selected task-attempt outputs and then the job result visible under its storage contract.
- A **straggler** is a slow task that delays stage/job completion relative to peers.

### Central model, mechanism, or theorem

For input multiset `I`, mapper `M`, reducer partition function `p(k)` into `R` reducers, grouping equivalence `~`, and reducer `D`, the job computes intermediate multiset `E = union over x in I of M(x)`. Reducer `r` receives exactly the pairs `(k,v)` in `E` with `p(k)=r`, sorted and grouped so every equivalent key group is processed together. Final logical output is the union of committed reducer outputs, or committed map outputs when `R=0`.

The runtime can re-execute tasks safely only when input identity is stable, user code is deterministic or retry-equivalent, intermediate/output attempt names are isolated, and external side effects are idempotent or deferred to a commit protocol. “Exactly-once output” does not mean each function executed once. It means duplicate attempts do not create duplicate committed task output under the stated committer and storage semantics.

### Critical invariants

- Every complete input record belongs to the intended logical input exactly once, independent of physical split boundaries.
- Mapper output key/value encodings and comparators agree on deterministic identity and ordering.
- All intermediate values for one grouping-equivalent key reach one reducer.
- The partitioner always returns a valid reducer number and is compatible with grouping.
- Map output is durable enough for the job's recovery policy or is reproducible from stable input.
- Reducers do not begin final group processing before required map outputs are available under the runtime contract.
- Failed/speculative attempts cannot publish competing final files or uncontrolled external effects.
- Output commit is bound to job attempt, task attempt, destination, schema, and input snapshot.
- Counters, logs, and samples are observability evidence, not automatic proof of data correctness.

### Common failures

Frequent failures are splitting records at arbitrary bytes, using nondeterministic serialization or hash partitioning, changing comparator semantics between workers, assuming reducer values have meaningful order, using a combiner as a required computation, performing non-idempotent API calls inside map/reduce, retaining all values for a hot key in memory, choosing reducer count from cluster cores alone, overlooking `M*R` shuffle connectivity and spill files, treating task success as job commit, trusting speculation with side effects, and assuming retries mean exactly-once execution.

### Compact example

Three records produce eight word/count pairs. A stable two-way partitioner sends `blue` to reducer 0 and `green,red` to reducer 1. Sort/group gives `blue:[1,1,1]`, `green:[1,1,1]`, and `red:[1,1]`; reducers emit counts 3, 3, and 2. Maps may finish in any order, and an attempt may run twice, but only committed attempt output belongs to the result.

### Connections

[LSDS-008](008-serialization-across-workers.md) supplies deterministic encodings. [LSDS-014](014-read-and-write-pipelines.md) supplies spills and backpressure. [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) supplies input layout. [LSDS-022](../ROADMAP.md) deepens map-side and reduce-side processing.

## Governing Question

MapReduce exposes two small user functions and hides a large distributed protocol. Input is enumerated and divided. Map attempts parse records and buffer intermediate pairs. Buffers spill, partition, sort, combine optionally, and merge. Reducers fetch partitions from every successful mapper, merge and group them, execute reduce calls, write attempt output, and participate in a job-level commit.

The abstraction works because the runtime controls data movement and replay. It schedules near input replicas where possible, monitors attempts, re-executes failed work, speculates on slow work, and delays authoritative publication until the job protocol accepts outputs. User code must fit these assumptions.

The simple signature hides important semantics. Input splits are not records. Values in a reduce group are not generally ordered. A combiner may run zero, one, or many times. A task attempt can execute repeatedly. Map outputs are often temporary local state. Reducer output becomes meaningful only through the output committer.

The governing question is how to reason from the pure key/value model through the concrete execution graph so correctness, cost, recovery, and observability remain explicit.

## Why This Matters

MapReduce established a durable pattern for large batch processing: move computation to partitions, materialize a repartitioning boundary, group by key, and recover through replay. Modern SQL, dataflow, and table engines use more general DAGs, but splits, shuffle, keyed grouping, stages, attempts, stragglers, and commit protocols remain foundational.

The model scales embarrassing parallel work and keyed aggregation, but shuffle can dominate network and disk. A mapper emitting many records creates intermediate amplification. Skew can send one reducer a disproportionate group. Small input files create excessive maps and planning. Too few reducers underuse the cluster; too many create tiny outputs.

Failure semantics affect application design. A map that charges a credit card or sends an email can repeat after a lost heartbeat even if the first attempt succeeded. A reducer that writes directly to a shared filename can race a speculative copy. The runtime's retry tolerance applies to managed dataflow artifacts, not arbitrary external side effects.

Understanding the execution model also prevents false claims. A counter matching expected input count does not prove correct keys. Successful tasks do not prove the job committed. Sorted intermediate keys do not imply deterministic ordering among values. Framework reliability does not validate business logic or governance.

## Prerequisites and Retrieval

Recall partition functions from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md), task graphs from [LSDS-005](005-distributed-task-graphs.md), serialization from [LSDS-008](008-serialization-across-workers.md), failure assumptions from [LSDS-009](009-cluster-failure-assumptions.md), and work/state accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve blocks, locality, and stable ranges from [LSDS-011](011-distributed-block-storage.md); metadata/commit identity from [LSDS-012](012-metadata-servers-and-namespace.md); read/write pipelines from [LSDS-014](014-read-and-write-pipelines.md); recovery ambiguity from [LSDS-015](015-failure-detection-and-re-replication.md); immutable object output from [LSDS-016](016-object-storage-semantics.md); and analytical file geometry from [LSDS-019](019-small-file-pathologies.md) and [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md).

You should understand key/value records, multisets, equivalence relations, deterministic functions, sorting, hashing, serialization, files/blocks, local disks, network transfer, retries, idempotency, speculative execution, and atomic publication.

## Learning Objectives

After completing this module, you should be able to:

- express a batch computation as map, partition, group, and reduce transformations;
- distinguish input files, blocks, splits, records, map tasks, and attempts;
- explain map buffering, partitioned spills, merge, shuffle, sort, and grouping;
- state partitioner, sort comparator, and grouping comparator compatibility;
- distinguish unordered grouped values from secondary-sort designs;
- reason about map-only jobs, combiners, reducer counts, and output files;
- calculate intermediate amplification, shuffle bytes, partition skew, and task waves;
- design deterministic/retry-equivalent user functions without uncontrolled side effects;
- explain failure replay, speculative execution, and output commit semantics;
- identify locality, small-file, straggler, hot-key, and slow-start trade-offs;
- specify validation, counters, provenance, security, and governance evidence; and
- recognize when a multi-stage DAG, streaming engine, database, or service is a better fit.

## Core Exposition

### Programming model

The logical model consumes input `(k1,v1)` pairs. `map(k1,v1)` emits zero or more `(k2,v2)` pairs. The framework groups all intermediate values for equivalent `k2`; `reduce(k2, values)` emits zero or more `(k3,v3)` results.

Inputs and outputs are multisets unless the application imposes stronger semantics. Duplicate input records yield duplicate mapper work. Repeated intermediate values remain repeated. A reducer such as sum may intentionally collapse multiplicity; a distinct operation must do so explicitly.

Key/value types need stable serialization. Intermediate keys also need consistent sort and grouping comparison across every task. Schema and code/config versions are part of job identity.

### Input enumeration and snapshots

Before maps run, the job enumerates input paths/table files and creates splits. Correctness begins with a stable logical input snapshot. A mutable prefix listing can include a hybrid of concurrent writes; an immutable table manifest or frozen path set is safer.

Record the exact file versions, lengths, schema, partition spec, encryption/key context, and job submission identity. If a retry reads a replaced file under the same path, replay no longer computes the same job.

Access controls can change during a long job. Authorization failure should be distinguishable from missing/corrupt input. Never silently skip inaccessible records and call the result complete.

### InputSplit versus RecordReader

An input split describes logical work, often a byte range plus locality hints. It need not equal a storage block, file, or record. The `InputFormat` chooses splits; a `RecordReader` converts each split into complete records.

For newline text, a nonzero split may skip the partial first line and read beyond its nominal end to finish the last record. Two readers must coordinate through deterministic boundary rules so no record is duplicated or omitted.

Unsplittable compression can force one file into one split. Many tiny files can create too many splits unless combined. Splitting a format without independent synchronization points can corrupt parsing.

### Map task lifecycle

The runtime launches one logical map task per input split in common implementations. An attempt initializes code/config/cache, opens its split, iterates records, invokes the mapper, reports progress/counters, and closes resources.

Mapper setup/cleanup may also repeat. Per-attempt local caches and temporary files need unique identity and bounds. Large initialization cost makes tiny maps inefficient.

Map-only jobs set reducer count to zero. Their committed map outputs become final results; no keyed global grouping occurs. Output commit rules still apply.

### Intermediate buffering and spill

Mapper emissions enter a bounded memory buffer containing serialized keys, values, and metadata. At a threshold, the runtime partitions and sorts records, optionally combines them, compresses them, and spills runs to local disk.

Later spills merge into partitioned map output plus an index. Buffer size trades memory against spill frequency. Too small causes repeated disk/merge work; too large risks pressure, garbage collection, or container failure.

Intermediate bytes can greatly exceed input. Track records/bytes before and after combine/compression, spill count, spilled records, local disk, merge passes, and peak memory.

### Partition function

For `R>0`, every intermediate key maps to reducer `p(k)` in `[0,R)`. Equal grouping keys must reach the same reducer. A common hash partitioner requires stable hash/serialization semantics; language-randomized hashes are unsafe across processes unless controlled.

Partition balance depends on data distribution, not only hash quality. One popular key always goes to one reducer. Salting can distribute an associative aggregate and requires a second merge stage to restore the logical key.

Reducer count changes partition identity and number of output files. Do not treat partition number as durable business identity across job configurations.

### Shuffle topology

Each successful map output contains up to `R` partitions. Each reducer fetches its partition from every successful mapper. With `M` maps and `R` reducers, potential map-reducer relationships are `M*R`, though empty partitions and batching change actual transfers.

Map output is often local ephemeral disk. If its worker fails after map completion but before reducers fetch it, the map task must rerun elsewhere from stable input. This is why map completion is not durable job progress in the same sense as final output.

Shuffle overlaps map completion and reducer copy/merge according to scheduler policy. Fetch retries, checksums, authentication, compression, connection limits, and backpressure protect the network and disks.

### Sort and merge

Map spill runs are sorted by partition and key. Reducers merge fetched segments, spilling/merging when memory is insufficient. The final merged stream is sorted under the configured sort comparator.

External merge sort turns bounded memory and local disk into scalable ordering. Cost includes bytes written/read across spill levels, comparisons, compression CPU, and temporary storage. Slow disks can dominate despite modest user-function CPU.

Comparator consistency is an invariant: antisymmetry, transitivity, and agreement across serialized forms. A comparator that changes with locale, clock, or process can corrupt grouping/order.

### Grouping and reduce invocation

The grouping comparator defines which adjacent sorted keys form one reducer call. By default, keys that compare equal are grouped. The representative key passed to reduce should not be assumed to preserve all fields ignored by grouping.

The iterable of values may stream from merged segments. Materializing it into a list can exhaust memory for hot keys. Process incrementally where the algorithm permits.

Values have no application-level order unless the sort key includes a secondary component and the grouping comparator groups only the primary portion. Accidental mapper/fetch order is not a contract.

### Reduce task lifecycle

A reduce attempt copies map partitions, merges/sorts them, invokes reduce once per group, writes attempt-specific output, and asks the committer to accept it. Shuffle, sort, and reduce are distinct phases with different bottlenecks.

Reducers may begin copying before every map finishes, but cannot complete groups until the required map-output set is known and available. Slow maps can therefore delay every reducer.

Reducer number often corresponds to one output part, including empty parts depending on output format. Choose `R` from shuffle volume, key distribution, desired parallelism/task duration, and downstream file geometry.

### Combiner semantics

A combiner can aggregate map output locally before shuffle. The runtime may invoke it zero, one, or many times over arbitrary subsets, including during spill/merge. Correctness cannot require a particular invocation count.

Safe combiners usually implement associative and commutative partial aggregation with compatible input/output types and a mergeable state. Sum of integer counts is safe under overflow policy; arithmetic mean represented as a scalar is not, but `(sum,count)` is mergeable.

Floating-point addition is not bitwise associative. If reproducibility matters, define stable numerical aggregation, ordering, precision, or tolerance rather than asserting algebra that the representation lacks.

### Data locality

When compute and replicated storage share nodes, the scheduler can prefer a host containing the input block, then the rack, then remote placement. Locality saves network and can delay launch while waiting for a suitable slot.

Waiting too long underutilizes compute; launching remotely consumes network. Locality matters primarily for map input. Shuffle is inherently networked by reducer partition.

With disaggregated object storage, host locality disappears. Region placement, network bandwidth, request concurrency, caching, and file pruning become the relevant controls.

### Failure and replay

If an attempt crashes, times out, or loses its worker, the scheduler can launch another attempt for the same logical task. Stable input and deterministic/retry-equivalent functions should reproduce managed output.

Loss of a completed map's local intermediate data triggers map replay. Reduce attempt loss can require refetch and recomputation of its reduce output. The framework bounds attempts and eventually fails the job rather than retrying forever.

Classify deterministic bad records separately from transient infrastructure. Blind retry of a poison record wastes capacity. Skipping records changes semantics and must be explicit, counted, quarantined, and governed.

### Speculative execution

Speculation runs a duplicate attempt for a suspected straggler and accepts an appropriate winner. It helps when slowness is attempt-specific and wastes resources when the input/key is intrinsically heavy or the cluster is saturated.

Both attempts execute user code. External writes, emails, database increments, audit events, random identifiers, and clock-dependent logic can duplicate or diverge. Disable speculation or make effects retry-safe and commit-mediated.

Reducer speculation is especially expensive because it duplicates shuffle fetch, sort, and output work. Measure tail benefit against resource amplification.

### Output commit

Attempts write to isolated temporary destinations. Task commit selects one successful attempt for a logical task. Job commit publishes the complete job according to `OutputCommitter` and storage semantics. Abort cleans candidates under bounded assumptions.

Atomic filesystem rename can support a directory commit pattern; object stores may implement rename as copy/delete and need manifest or multipart-aware committers. A `_SUCCESS` marker is meaningful only under the exact committer contract.

After ambiguous commit response, inspect job history and destination manifest/version. Do not rerun blindly into the same mutable path. Final provenance binds job ID, input snapshot, code/config, task outputs, schema, and checksums.

### Side effects and determinism

Prefer pure user functions whose only authoritative output flows through the framework. Reading current time, randomness, mutable remote state, unordered maps, locale, or changing lookup data can make attempts differ.

Distribute immutable reference data with a content digest or join it as versioned input. Seed randomness from stable job/task/record identity if stochastic algorithms require reproducibility.

If an external effect is unavoidable, write an idempotent intent keyed by stable logical record and job operation, then finalize through a transactional downstream system after job commit. Attempt ID is not the same as logical effect ID.

### Stragglers and skew

Stragglers arise from slow hardware, network, local disk, noisy neighbors, garbage collection, oversized splits, hot keys, data-dependent code, or repeated fetch failure. Duration percentiles and phase metrics distinguish causes.

Speculation treats anomalous attempts. Split redesign, skew-aware partitioning, hot-key salting, sampling, compression changes, or algorithm changes treat intrinsic work. Increasing timeout only hides symptoms.

One reduce group larger than memory requires streaming aggregation or a different multi-stage plan. One reducer owning most shuffle cannot be fixed by adding reducers unless the key is decomposed.

### Cost model

Let `B_in`, `B_map`, `B_shuffle`, and `B_out` be input, mapper-emitted, transferred intermediate, and final bytes. Map amplification is `B_map/B_in`; shuffle compression ratio is `B_shuffle/B_map`; output ratio is `B_out/B_in` under declared serialization scopes.

Potential mapper-reducer edges are `M*R`. Ideal task waves are `ceil(M/S_m)` and `ceil(R/S_r)` for map/reduce slots `S_m,S_r`, ignoring skew, overlap, failures, and cluster sharing.

Track CPU-record cost, serialization, spills, local disk bytes, merge passes, network, fetch retries, task setup, locality, speculative duplicates, and committed versus attempted outputs. Bytes alone do not predict time.

### Job validation

Validate input manifest count/bytes/versions and rejected records. Use counters for map input/output, combine input/output, reduce groups/records, spill, shuffle, and output. Reconcile them with domain invariants.

Counts can cancel errors. Add keyed totals, checksums/multiset digests, min/max/null distributions, partition coverage, and samples appropriate to consequence. Validate the committed output snapshot, not attempt directories.

Test a sequential reference implementation on small adversarial data, then compare distributed results across split sizes, reducer counts, retry, speculation, and worker order.

### Security and governance

Job credentials should be scoped and time-bounded. Intermediate spill/shuffle may contain plaintext derived data; encrypt transport/local disks where required and clean attempt state. Logs, counters, filenames, and sample records can leak sensitive values.

MapReduce moves records across partition boundaries. A reducer can combine tenants or classifications in one output. Preserve authorization, residency, retention, consent, and provenance through keys, partitions, output policy, and named review.

Do not place secrets in job configuration or distributed cache without approved handling. Audit submitter, service identity, code/config digest, inputs, outputs, accesses, exceptions, and cleanup.

### When the model fits

MapReduce fits bounded, replayable batch transformations with independent record mapping and keyed group processing, especially when intermediate materialization and simple failure replay are acceptable.

It is awkward for iterative algorithms that repeatedly reload state, interactive queries with strict latency, cyclic graphs, low-latency streams, fine-grained mutable state, or transactions spanning external services. DAG engines can fuse stages/cache intermediates; databases can execute optimized relational plans; stream processors manage unbounded time/state.

Choose based on workload, not historical prestige. The map-shuffle-reduce mental model remains valuable even when another runtime implements it.

## Definitions and Notation

- `I` is the stable multiset of input records `(k1,v1)`.
- `M(x)` is the finite multiset of intermediate `(k2,v2)` pairs emitted for input record `x`.
- `E` is the union/multiset sum of `M(x)` over `I`.
- `R` is reducer count and `p(k)` returns one integer in `[0,R)` when `R>0`.
- `~` is grouping equivalence on intermediate keys.
- `D(k,V)` is reducer output for representative key `k` and grouped value multiset/stream `V`.
- `M_tasks` and `R_tasks` are logical map/reduce task counts; attempts may exceed them.
- `B_in`, `B_map`, `B_shuffle`, and `B_out` are serialized byte measures with declared scopes.
- `S_m` and `S_r` are effective concurrent map/reduce execution capacities.
- `a(t)` is a task attempt for logical task `t`; `commit(a(t))` selects visible managed output.

Partitioner compatibility requires `k1 ~ k2` to imply `p(k1)=p(k2)`. Sort and grouping comparators must make grouping-equivalent keys adjacent. Reducer value iteration order is unspecified unless encoded by an explicit secondary-sort key/comparator design.

## Mechanisms, Invariants, or Proof Structure

Use this MapReduce audit:

1. Pin immutable input membership, exact versions, schema, code/config, and reference data.
2. Prove InputFormat/RecordReader split boundaries cover complete records once.
3. Specify mapper output types, determinism/retry equivalence, and intermediate amplification.
4. Prove serialization, partition, sort, and grouping semantics agree across workers.
5. Bound map buffers, spills, compression, local disk, shuffle connections, and fetch retries.
6. Select reducer count and skew strategy from sampled keys, bytes, task duration, and output geometry.
7. Treat combiners as optional repeated partial aggregation and grouped values as unordered unless designed otherwise.
8. Isolate attempts and keep external side effects idempotent or behind a commit protocol.
9. Commit one output per logical task and one job manifest; resolve ambiguity before rerun/cleanup.
10. Validate committed domain results and provenance under retry, speculation, failure, and adversarial skew.

The fixture executes a minimal deterministic map, stable partition, sort/group, and reduce pipeline. It does not simulate spills, network, attempt replay, or output commit.

<!-- bijux-verify: {"id":"mapreduce-word-count","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_records=3 intermediate_pairs=8 reducers=2\nreducer_0=(('blue', 3),)\nreducer_1=(('green', 3), ('red', 2))\nfinal=(('blue', 3), ('green', 3), ('red', 2))\n","stderr":""}} -->
```python
records = ("red blue red", "blue green", "green green blue")
reducers = 2

intermediate = tuple(
    (word, 1)
    for record in records
    for word in record.lower().split()
)


def stable_partition(key: str) -> int:
    return sum(key.encode("utf-8")) % reducers


partitions = tuple(
    tuple(sorted(pair for pair in intermediate if stable_partition(pair[0]) == reducer))
    for reducer in range(reducers)
)


def reduce_partition(pairs: tuple[tuple[str, int], ...]) -> tuple[tuple[str, int], ...]:
    keys = sorted({key for key, _ in pairs})
    return tuple((key, sum(value for current, value in pairs if current == key)) for key in keys)


outputs = tuple(reduce_partition(partition) for partition in partitions)
final = tuple(sorted(pair for output in outputs for pair in output))

print(
    f"input_records={len(records)} intermediate_pairs={len(intermediate)} "
    f"reducers={reducers}"
)
for reducer, output in enumerate(outputs):
    print(f"reducer_{reducer}={output}")
print(f"final={final}")
```

Changing mapper completion order cannot change the count. Repeating a mapper attempt would duplicate results if both attempts were admitted; the runtime must select one logical map output before reducers treat the map as complete.

The full proof additionally covers stable input, record boundaries, spill integrity, complete shuffle partitions, comparator compatibility, one committed attempt per task, job-level publication, and domain validation.

## Alternatives and Trade-Offs

Map-only jobs avoid shuffle and cannot perform global keyed grouping. One reducer provides global key order under comparator and serializes the entire reduce stage. Multiple reducers scale and produce partition-local order.

More maps improve parallelism and increase setup, spill files, scheduler state, and shuffle fan-out. Combined input splits reduce small-file task count and preserve per-file open work.

More reducers decrease average partition size and increase connections, output files, empty partitions, and commit work. Fewer reducers reduce overhead and can create long tasks or memory pressure.

Combining reduces shuffle for mergeable aggregates and can add CPU/spill work or break correctness for non-associative state. Map-side aggregation with bounded tables is more controllable but can consume memory.

Hash partitioning balances diverse keys probabilistically and destroys range order. Range partitioning supports globally partitioned order and requires representative sampling/boundaries. Custom partitioning encodes domain load knowledge and can become stale.

Speculation reduces attempt-specific tails and duplicates resource/side-effect work. Skew-aware algorithm changes address intrinsic heavy keys.

Intermediate compression saves disk/network and costs CPU. It often helps I/O-bound jobs and can hurt CPU-bound jobs or incompressible encrypted data.

Locality-aware scheduling saves input network and may wait for a slot. Immediate remote launch uses idle compute and consumes shared bandwidth.

MapReduce materializes a simple fault boundary and writes intermediate/final storage. General DAG engines can pipeline/fuse/cache stages and have more complex recovery. SQL engines add declarative optimization; streaming engines add time/state.

## Failure Modes and Misconceptions

- **“A split is a record or block.”** It is logical work interpreted by a record reader.
- **“Byte ranges can be parsed independently.”** Record and compression boundaries need format-specific synchronization.
- **“Every map runs once.”** Failed and speculative attempts can repeat.
- **“Framework retries make side effects exactly once.”** Only managed committed output has the stated commit semantics.
- **“Mapper order affects reduce output.”** Correct grouped computation cannot depend on arrival order unless order is explicitly encoded.
- **“Reducer values are sorted.”** Keys are sorted/grouped; values require secondary-sort design for order.
- **“A combiner is a mini-reducer that always runs.”** It is optional and repeatable over arbitrary subsets.
- **“Average can use average as a combiner.”** Carry mergeable `(sum,count)` state.
- **“Hashing guarantees balance.”** A hot key remains indivisible under ordinary grouping.
- **“More reducers always go faster.”** Fan-out, setup, tiny output, and commit overhead grow.
- **“Reducer count should equal cores.”** Base it on shuffle distribution, duration, capacity, and downstream geometry.
- **“Completed map output is durable final state.”** Worker loss can require map replay.
- **“Reducers start only after every map finishes.”** Fetch can overlap, while complete grouping still depends on all required maps.
- **“Task success means job success.”** Job-level output commit can still fail or be ambiguous.
- **“A success marker proves correct data.”** Validate exact committed manifest and domain invariants.
- **“Speculation fixes skew.”** It duplicates intrinsically heavy work.
- **“Counters prove correctness.”** Miskeyed records can preserve totals.
- **“MapReduce is the right abstraction for every distributed workload.”** Iteration, interaction, streaming, and transactions may need another engine.

## Worked Examples

### Example 1

**Situation:** A text split begins halfway through a line. **Reasoning:** Its record reader skips the partial leading record while the preceding split reads beyond its nominal end to finish it, producing one complete record under the format boundary rule.

### Example 2

**Situation:** A mapper emits `(word,1)` for eight tokens. **Reasoning:** Stable partitioning sends each equal word to one reducer; grouping and integer sum produce exact counts independent of map arrival order.

### Example 3

**Situation:** A mapper dies after reducers fetched its local output. **Reasoning:** If the worker/output is unavailable, the logical map reruns from pinned input; reducers refetch the selected attempt's partition and discard invalid prior segments.

### Example 4

**Situation:** Average values are combined locally. **Reasoning:** Emitting only local averages weights partitions equally and is wrong. Emit `(sum,count)`, combine both by addition, and divide once at final reduction with defined numeric policy.

### Example 5

**Situation:** One customer owns 45% of intermediate bytes. **Reasoning:** Ordinary partitioning sends that key to one reducer. Use streaming reduction if possible or salt into partial groups and merge in another stage while preserving key semantics.

### Example 6

**Situation:** Two reducer attempts write the same destination filename. **Reasoning:** They race and can corrupt/overwrite. Write attempt-isolated files; let the output committer select one logical task result and publish the job manifest.

### Example 7

**Situation:** A mapper calls a billing API, then its heartbeat is lost. **Reasoning:** Replay can bill twice. Emit stable billing intents as data and apply them afterward through an idempotent transactional service keyed by logical operation.

### Example 8

**Situation:** Ten thousand maps and two thousand reducers produce sparse shuffle. **Reasoning:** Potential connectivity is 20 million map-reducer relationships. Sample partition density and tune reducers, batching, compression, and algorithm rather than focusing only on payload.

### Example 9

**Situation:** Job commit response is lost after output appears. **Reasoning:** Query job history and exact output manifest/version, schema, count, and digest. Record success if intended commit exists; do not rerun blindly into the path.

### Example 10

**Situation:** Reducers group sensitive records from several tenants. **Reasoning:** Key design and output partitioning must preserve approved access/residency boundaries; encrypt shuffle/spill, scope credentials, retain provenance, and obtain privacy/security/domain review.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hashing, sorting, external merge, heaps, and streaming aggregation. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies processes, files, buffers, virtual memory, local disks, scheduling, and failure cleanup.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replay, determinism, at-least-once execution, leases, speculation, commits, and failure detectors. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies shuffle fan-out, congestion, bandwidth, locality, retries, and backpressure.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes batch transforms, partitions, file formats, table snapshots, quality checks, and lineage. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies group-by, sorting, partitioned aggregation, joins, cost models, and transactional publication.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies cluster scheduling, containers, credentials, observability, quotas, and cost. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies least privilege, intermediate-data protection, audit, tenant isolation, and safe side effects.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies idempotency, operation resources, retries, and ambiguous outcomes for external effects. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies workload boundaries, hazards, verification, and socio-technical review.

## References

- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google.com/archive/mapreduce-osdi04.pdf), checked 2026-09-03. Original primary paper on the map/reduce model, partitioning, scheduling, locality, shuffle, failure replay, backup tasks, and commit behavior.
- Google Research, [*MapReduce Publication Record*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), checked 2026-09-03. Official bibliographic record and abstract for the original OSDI 2004 work.
- Apache Hadoop, [*MapReduce Tutorial*](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), checked 2026-09-03. Official map, reduce, shuffle, sort, partitioner, combiner, split, task, attempt, compression, counter, speculation, and job configuration semantics.
- Apache Hadoop, [*InputFormat API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/InputFormat.html), checked 2026-09-03. Official logical split creation, RecordReader, and locality responsibility contract.
- Apache Hadoop, [*OutputCommitter API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/OutputCommitter.html), checked 2026-09-03. Official task/job setup, commit, recovery, and abort interface.
- Apache Hadoop, [*Partitioner API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/Partitioner.html), checked 2026-09-03. Official intermediate key/value to reducer-partition interface.
- Apache Hadoop, [*Reducer API*](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/Reducer.html), checked 2026-09-03. Official shuffle, sort, secondary-sort, grouping, and reduce lifecycle.
- Apache Hadoop, [*HDFS Architecture Guide*](https://hadoop.apache.org/docs/stable1/hdfs_design.html), checked 2026-09-03. Official block, replica placement, streaming access, locality, integrity, and failure-recovery context.
- Apache Hadoop, [*S3A Committers: Architecture and Implementation*](https://hadoop.apache.org/docs/current3/hadoop-aws/tools/hadoop-aws/committer_architecture.html), checked 2026-09-03. Official object-store task/job committer lifecycle, attempt identity, abort, and multipart behavior.
- Apache Hadoop, [*YARN Architecture*](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html), checked 2026-09-03. Official separation of resource management, application coordination, and per-node execution in modern Hadoop deployments.

## Exercises

### Exercise 1

Trace word count for records `red blue red`, `blue green`, and `green green blue` with two reducers and stable partition `sum(UTF-8 bytes) mod 2`. Give intermediate count, reducer groups, and output.

### Exercise 2

A job has 8,000 maps, 400 reducers, 160 concurrent map slots, and 80 concurrent reduce slots. Compute potential map-reducer relationships and ideal map/reduce waves. State omitted costs.

### Exercise 3

Design a correct average calculation with an optional combiner, including overflow/floating-point and empty-input policy.

### Exercise 4

Design retry-safe processing when the desired outcome includes an external service mutation that cannot participate in the framework's output committer.

### Exercise 5

Specify validation and named review for a MapReduce job aggregating regulated records across tenants, with speculation and object-store output.

## Answers to the Exercises

### Answer 1

The mapper emits eight pairs: red twice, blue three times, and green three times. Byte sums are blue 424, green 529, red 315, so reducer 0 receives `blue:[1,1,1]` and emits `(blue,3)`; reducer 1 receives `green:[1,1,1]` and `red:[1,1]` and emits `(green,3),(red,2)`. Sort order is lexical within each reducer under the stated comparator. Map completion order does not affect counts; duplicate attempts must not both become selected logical map output.

### Answer 2

Potential relationships are `8,000*400=3,200,000`. Ignoring failures, skew, setup, locality, cluster sharing, speculative copies, and overlap, maps require `ceil(8,000/160)=50` waves and reducers require `ceil(400/80)=5` waves. This does not predict duration: map sizes, shuffle density/bytes, spill/merge, reducer slow start, network/disk, hot keys, fetch retries, output commit, and stage overlap matter. Measure actual nonempty partitions and phase percentiles.

### Answer 3

Map each numeric observation to `(key,(value,1))`. A combiner may sum partial pairs as `(sum of sums, sum of counts)` zero, one, or many times; the reducer performs the same merge and emits `sum/count` only when count is positive. Define integer width/overflow or use an exact wider accumulator. For floating point, specify accepted tolerance, compensated/pairwise scheme, decimal arithmetic, or deterministic order because addition is not bitwise associative. Define NaN/null rejection and empty-group behavior explicitly; validate total count and reference samples.

### Answer 4

Keep map/reduce pure and emit a committed intent dataset containing stable logical operation ID, target, payload digest, source/job identity, and precondition. After the job manifest commits, a separate dispatcher reads exact intent versions and calls the service with an idempotency key or transactional compare-and-set. It records durable pending/succeeded/conflicted/failed state and resolves timeouts by querying the service before retry. If the service provides neither idempotency nor outcome lookup/transactional condition, exactly-once effect is unprovable; redesign the service or accept and document compensation/manual reconciliation. Never key effects by task-attempt ID.

### Answer 5

Pin an approved input manifest with tenant, schema, consent/purpose, residency, retention, and exact versions. Prove partition/group keys cannot mix tenants where physical isolation is required; otherwise enforce row/column policy through governed output. Use deterministic code/config/reference digests, scoped credentials, encrypted shuffle/spill/output, attempt-isolated names, an object-store-aware committer, and idempotent external effects. Validate keyed multiset/count/aggregate invariants, rejected records, partition coverage, checksums, provenance, speculation/retry equivalence, and committed manifest—not counters alone. Named review includes data owners/stewards, affected community or research-ethics/IRB where applicable, privacy/legal/records/compliance, security/key management, storage/MapReduce/platform operators, accessibility, incident recovery, and independent assurance. Retain cleanup and erasure evidence for attempts, caches, replicas, backups, logs, and keys.
