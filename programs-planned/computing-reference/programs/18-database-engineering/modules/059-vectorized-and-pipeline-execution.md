---
module_id: DBE-059
program: Database Engineering
level: 2
module_number: 59
title: Vectorized and Pipeline Execution
status: complete
last_verified: 2026-08-30
---

# Vectorized and Pipeline Execution

## One-Page Review

### Governing question

How can a query engine process batches through fused or scheduled pipelines so that it preserves SQL semantics and resource ownership while exploiting caches, branch prediction, SIMD, compression, parallel cores, and bounded backpressure?

### Essential definitions

A **vector** is a typed sequence of values plus representation metadata such as validity, encoding, and ownership. A **batch** or **data chunk** is a same-cardinality set of vectors representing rows. **Vectorized execution** invokes operators or expression kernels on batches rather than one tuple at a time. A **selection vector** identifies active row positions without immediately copying values. A **validity bitmap** records which slots are non-NULL. A **pipeline** is a connected operator region that can move batches from a source through operators to a sink without full intermediate materialization. A **pipeline breaker** completes or materializes an input boundary before downstream progress. **Operator fusion** executes several logical operations inside one control loop. **Push execution** sends produced batches downstream; **pull execution** requests them upstream. A **morsel** is a bounded unit of source work scheduled dynamically. **Data-centric compilation** generates specialized code around pipelines and data flow.

### Central model, mechanism, or theorem

Let a batch expose logical rows at positions selected by S and validities V. A vector kernel must be observationally equivalent to applying the scalar SQL operation once to each selected logical row, preserving order and multiplicity unless the operator explicitly changes them. Filters refine S according to TRUE, rejecting FALSE and UNKNOWN; projections compute aligned outputs only for live positions. Pipeline composition is correct when each stage preserves its local semantics, schemas, representations, and ownership. Batching amortizes dispatch over b rows, but batch size trades call overhead against cache footprint, latency, overproduction, memory, and cancellation. No fixed b or execution paradigm is universally optimal.

### Critical invariants

- All vectors in a batch have the same logical cardinality and valid index domain.
- Values, validity, offsets, lengths, dictionaries, and selections describe the same logical rows.
- Kernels process exactly the live selection and implement SQL NULL, type, collation, overflow, error, and volatility rules.
- A selection may reorder or repeat only when the operator's semantics permit it; otherwise order and occurrence identity are preserved.
- Borrowed buffers remain live until every consumer completes; mutation occurs only under exclusive ownership or copy-on-write rules.
- Pipeline breakers own and govern all retained state, spill, and replay.
- Scheduling never loses or duplicates a morsel; shared build state is published only after complete synchronization.
- Backpressure, cancellation, error, and early stop propagate across every queued or running pipeline task.
- Performance claims name hardware, data, encoding, batch size, compilation, concurrency, and measurement boundary.

### Common failures

Failures include reading garbage behind NULL bits; ignoring a selection vector; misaligning columns after compaction; flattening encodings needlessly; retaining a dictionary child after its owner is released; mutating shared batches; assuming vectorization automatically means SIMD; choosing batches too large for cache or latency; producing a full batch after limit; fusing volatile expressions illegally; treating every join or aggregate as one pipeline; publishing a hash build before completion; losing morsels during cancellation; oversubscribing cores/NUMA memory; excluding compilation from latency; and benchmarking different algorithms while claiming an execution-model comparison.

### Compact example

The executable processes nine rows in batches of four. Separate score and active validity vectors implement SQL `score >= 7 AND active IS TRUE`. Three selection vectors retain positions `(1)`, `(0)`, and `(0)`, producing `(2,70)`, `(5,80)`, and `(9,100)`. An independent row oracle matches exactly. Three UNKNOWN and three FALSE predicates are rejected. This establishes one finite logical-equivalence case, not CPU speed, SIMD, arbitrary encodings, or parallel correctness.

### Connections

Retrieve [Hash and Sort Aggregation](056-hash-and-sort-aggregation.md), [External Sorting and Spilling](057-external-sorting-and-spilling.md), and [Iterator and Volcano Execution](058-iterator-and-volcano-execution.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to pipeline profiling, query optimization, parallel execution, and distributed databases.

## Governing Question

What representation, control-flow, ownership, scheduling, and semantic contracts let batched/vectorized pipelines reduce execution overhead without changing the query, hiding unbounded state, or turning hardware-specific observations into universal claims?

## Why This Matters

An iterator can spend several indirect calls, branches, tuple-field lookups, and expression dispatches for every row. When data is memory-resident and operations are simple, that machinery can cost more than the arithmetic. Batching makes one operator call cover many values, exposes contiguous typed data to optimized kernels, and can preserve compressed or dictionary representations. Fusing a scan, filter, and projection can keep relevant columns and intermediate values near the CPU rather than materializing full tuples.

The optimization is not “use arrays.” SQL values carry NULL, type, collation, decimal, timestamp, nested-value, and error semantics. A batch may be flat, constant, dictionary encoded, lazy, sliced, or selected. A kernel that assumes contiguous non-null values can return plausible but wrong output. A filter typically produces a selection rather than a copied batch; every later expression must honor it. Nested offsets and child buffers require exact bounds and lifetime rules.

Pipelines reveal physical control. Scan/filter/project can stream as one region. Hash join build, full sort, many aggregates, exchanges, and window boundaries break or reshape that flow. Parallelism schedules source morsels, build tasks, probes, and sinks with dependencies. A limit must stop queued work; an error must cancel sibling tasks; backpressure must bound batches in flight. Without these contracts, higher throughput comes from uncontrolled memory and overproduction.

Performance depends on the interaction of workload and machine. Larger batches amortize dispatch and may improve SIMD opportunity, yet consume cache, increase first-row delay, perform unused work after early stop, and postpone cancellation. Data-centric compilation can eliminate generic dispatch and specialize expressions, but compilation time and code cache matter. Research comparing vectorized and compiled engines finds different strengths rather than one universal winner. The engineer's task is to preserve semantics, expose capabilities, and measure the correct boundary.

## Prerequisites and Retrieval

You should understand iterator execution, SQL bags and NULL, physical plans, row/column layouts, CPU caches and branches, SIMD basics, memory ownership, joins and aggregation, sorting/spill, parallel scheduling, cancellation, and experimental design.

Retrieve: vector, batch, data chunk, cardinality, flat/constant/dictionary/sequence/lazy encoding, validity bitmap, selection vector, compaction, decoding, unified view, kernel, SIMD lane, branch mask, pipeline source/operator/sink, breaker, fusion, materialization, morsel, driver/task, exchange, backpressure, work stealing, NUMA locality, compilation, specialization, code cache, and deoptimization/fallback.

DBE-058 established row-at-a-time pull and lifecycle. This chapter changes granularity and control placement while keeping its semantic and ownership obligations. DBE-060 will show how to profile batch cardinalities, pipeline stages, stalls, memory, I/O, and CPU behavior without double-counting.

## Learning Objectives

After this module, you can:

1. define logical batch semantics independently of flat, dictionary, constant, or lazy representation;
2. implement SQL NULL-aware selection and projection over batches and compare with a row oracle;
3. reason about selection, validity, offsets, nested values, encoding propagation, and buffer lifetimes;
4. identify pipeline sources, streaming operators, breakers, and sinks in a physical plan;
5. compare pull-vector, push-vector, fused compiled, bytecode, and hybrid execution;
6. analyze batch-size trade-offs across dispatch, cache, SIMD, latency, memory, and cancellation;
7. specify morsel scheduling, NUMA placement, build/probe dependencies, backpressure, and early stop;
8. diagnose flattening, compaction, materialization, skew, overproduction, and code-generation regressions;
9. construct semantic, encoding-metamorphic, fault, resource, and performance tests; and
10. make evidence-bounded execution-model decisions for transactional, analytical, mixed, and extension-heavy workloads.

## Core Exposition

**Begin with logical rows, not buffers.** A batch of cardinality c represents rows 0 through c−1 across columns. Each column has one logical type and c value slots, even if physical storage is constant, dictionary indexed, compressed, lazy, nested, or sliced. A validity structure says which slots contain SQL values. Null slots may have unspecified payload bytes; kernels must not interpret those bytes as values.

A selected batch adds an ordered list or bitmap S of live row indices. A filter can refine S without copying columns. A projection may emit a new vector aligned with S, retain dictionary references, or compact to consecutive output positions. Whatever representation it chooses, downstream sees the same logical output sequence. Repeating, omitting, or permuting selection indices changes multiplicity/order and is legal only for an operator that specifies that transformation.

**Representations enable and constrain optimization.** Flat fixed-width vectors offer contiguous loads. Constant vectors allow one computation when a deterministic function's arguments are constant. Dictionary vectors pair indices with a child vector, enabling filtered subsets and repeated values without copying. Sequence vectors encode arithmetic progressions. Lazy vectors defer loading. Nested lists typically use offsets/lengths plus child values; structs use aligned children. A generic decoded view simplifies kernels but may hide indirection and materialization cost.

Apache Arrow's columnar specification illustrates a portable representation boundary: typed arrays, lengths, buffers, and validity bitmaps define logical slots, while variable and nested types add offsets and child arrays. Arrow is an interchange format, not a complete query-execution policy. An engine's internal vectors may intentionally use different encodings, mutable buffers, string layouts, or selection structures.

**SQL predicates are masks with three-valued semantics.** A comparison involving NULL is usually UNKNOWN. `WHERE` retains only TRUE. Boolean `AND`/`OR` can sometimes short-circuit or compute masks compositionally, but volatile/erroring expressions constrain reordering. A vector engine may evaluate only selected rows, yet it must match the scalar evaluation contract, including which errors/effects are observable under the language and optimizer rules.

Selections can be sparse or dense. A dense bitmap supports bitwise operations and SIMD-friendly scans; an index vector makes subsequent kernels touch only live rows. Compaction copies survivors into dense output, improving later locality but spending bandwidth. Keeping a selection avoids copies but adds indirection and may retain large base buffers for few rows. Engines can adapt based on selectivity, downstream reuse, encoding, cache, and ownership.

**The executable tests one exact batch contract.** It slices nine rows into batches of at most four, preserves separate score and active validity, constructs local selection positions for predicate TRUE, and projects only those positions. The row oracle independently applies the same explicitly coded SQL behavior. Counters distinguish UNKNOWN, FALSE, and TRUE. This is a semantic test, not a throughput benchmark.

<!-- bijux-verify: {"id":"null-aware-vector-pipeline","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"batch_size=4\ninput_rows=9\ninput_batches=3\nselection_vectors=((1,), (0,), (0,))\noutput=((2, 70), (5, 80), (9, 100))\nrow_oracle=((2, 70), (5, 80), (9, 100))\nequivalent=True\ntrue_predicates=3\nfalse_predicates=3\nunknown_predicates=3\nevidence=null_aware_batch_equivalence\n","stderr":""}} -->
```python
def sql_predicate(score, score_valid, active, active_valid):
    if not score_valid or not active_valid:
        return None
    return score >= 7 and active is True


def vector_pipeline(identifiers, scores, score_validity, active, active_validity, size):
    output = []
    selections = []
    counts = {True: 0, False: 0, None: 0}
    for start in range(0, len(identifiers), size):
        stop = min(start + size, len(identifiers))
        selection = []
        for local, absolute in enumerate(range(start, stop)):
            decision = sql_predicate(
                scores[absolute],
                score_validity[absolute],
                active[absolute],
                active_validity[absolute],
            )
            counts[decision] += 1
            if decision is True:
                selection.append(local)
        selections.append(tuple(selection))
        for local in selection:
            absolute = start + local
            output.append((identifiers[absolute], scores[absolute] * 10))
    return tuple(output), tuple(selections), counts


identifiers = tuple(range(1, 10))
scores = (4, 7, 0, 9, 8, 7, 2, 0, 10)
score_validity = (True, True, False, True, True, True, True, False, True)
active = (True, True, True, False, True, False, True, True, True)
active_validity = (True, True, True, True, True, False, True, True, True)

output, selections, counts = vector_pipeline(
    identifiers, scores, score_validity, active, active_validity, 4
)
oracle = tuple(
    (identifier, score * 10)
    for identifier, score, score_valid, flag, flag_valid in zip(
        identifiers, scores, score_validity, active, active_validity
    )
    if sql_predicate(score, score_valid, flag, flag_valid) is True
)
print("batch_size=4")
print(f"input_rows={len(identifiers)}")
print("input_batches=3")
print(f"selection_vectors={selections}")
print(f"output={output}")
print(f"row_oracle={oracle}")
print(f"equivalent={output == oracle}")
print(f"true_predicates={counts[True]}")
print(f"false_predicates={counts[False]}")
print(f"unknown_predicates={counts[None]}")
print("evidence=null_aware_batch_equivalence")
```

The model excludes arbitrary SQL boolean short-circuiting, types/collations/overflow, strings/nested data, dictionary/lazy encodings, buffer reuse, SIMD, compilation, parallel scheduling, backpressure, spill, errors, and performance.

**A pipeline is a scheduling and materialization region.** Identify a source that produces work, operators that transform batches, and a sink that consumes or stores them. A scan can source morsels. Filters and projections transform. A result collector, exchange, hash-table build, or aggregate state can be a sink. After a breaker completes, its produced state or materialized output may source another pipeline. A physical plan tree therefore becomes a dependency graph of pipelines, not merely one chain.

For a hash join, build-side scan/filter feeds a hash-build sink. Only after build publication may probe-side scan/filter drive probe/output. A full sort consumes batches into bounded in-memory/external state; sorted output starts another region. Partial aggregation can reduce inside worker pipelines and exchange/merge later. Window partitions create boundaries according to ordering/frame needs. Correct pipeline decomposition follows operator semantics, not visual adjacency alone.

**Push and pull choose where control resides.** Pull-vector lets parents request a batch and supports natural downstream demand. Push-vector lets sources/drivers run a batch through operators toward a sink, often matching task schedulers and fused loops. Push needs explicit stop/backpressure signals; pull needs careful task parallelization and can retain call layering. Hybrids are common: a driver pulls source work, pushes chunks through a pipeline, and coordinates breakers/tasks externally.

**Batch size is a policy with several objectives.** If per-call overhead is h and per-row useful work is w, idealized control cost per row is `w + h/b`. This suggests larger b, but omits cache capacity, vector temporaries, selection density, branch behavior, memory bandwidth, startup, overproduction, cancellation, and tail waste. A batch should keep the active working set compatible with relevant caches and kernels while satisfying latency/resource goals. Fixed sizes simplify kernels; adaptive sizes may help sparse, variable-width, remote, or early-stop work but complicate testing and allocation.

SIMD is not synonymous with vectorized execution. Vectorization at the database layer means batch-oriented control. A compiler may auto-vectorize a flat arithmetic loop; a hand-written kernel may use SIMD intrinsics; dictionary indirection, variable strings, branches, exceptions, and sparse selection can inhibit lanes. Conversely, compiled data-centric loops can also use SIMD. Measure instruction count, IPC, branch misses, cache/TLB misses, bandwidth, and time together.

**Fusion reduces boundaries but increases coupling.** Fusing scan, filter, and projection can keep fields in registers/cache and avoid intermediate batches. It may also inflate code size, duplicate generated variants, complicate debugging, and reduce reuse of specialized vector kernels. A selective filter may benefit from materializing a compact selection before an expensive expression. Common subexpressions need one evaluation under effect rules. Fusion decisions should consider semantics, kernel maturity, code cache, compilation budget, and observed data.

Data-centric compilation generates code organized around pipeline flow instead of calling generic operators for every row. Neumann's work demonstrates this design direction; later apples-to-apples research found vectorization and compilation both efficient with workload/hardware-dependent strengths. Compilation cost must be included for one-shot queries and amortized explicitly for prepared/repeated work. Cache invalidation, schema changes, parameters, code security, fallback, and observability are production requirements.

PostgreSQL 18 documents JIT support for expression evaluation and tuple deforming rather than claiming a fully compiled data-centric engine. DuckDB's current internals documentation describes push-based vectorized `DataChunk` execution and its execution-format documentation describes flat, constant, dictionary, sequence, and unified views with a default fixed vector size. Velox currently exposes multiple vector encodings and vectorized expression evaluation. These are versioned product facts, not definitions of all vector engines.

**Parallel pipelines schedule bounded work.** Divide source input into morsels, enqueue them under a task/query, and let workers claim work. Small morsels improve load balance and cancellation granularity but add scheduling overhead. Large morsels improve sequential locality but create stragglers. NUMA-aware scheduling prefers data and build state local to workers while allowing work stealing when imbalance outweighs locality.

Exactly-once here means within the operator execution: each morsel's row occurrences contribute once to the intended attempt. A retry after failure may restart the whole query unless the engine implements durable attempt identities. Task completion must not publish a pipeline breaker early. A hash build needs a barrier or dependency counter before probes observe it. Parallel sinks need partitioned state, synchronization, or deterministic reduction contracts.

**Backpressure governs batches in flight.** A downstream exchange, client, disk, or aggregate can consume slower than producers. Bounded queues plus credits, blocked-task suspension, or cooperative drivers prevent unbounded memory. Cancellation and limit must revoke queued work and prevent new source claims while safely draining/releasing owned batches. One consumer cannot mutate shared buffers still read by another.

**Verification needs representation metamorphism.** Run the same logical inputs as flat, constant, dictionary, sliced, lazy, nested, and selected vectors; compare results and errors with a scalar oracle. Vary batch boundaries, including empty and partial tails. Poison payload behind NULLs to catch invalid reads. Repeat selection indices only for operators that support them. Change dictionary order without changing logical values. Inject cancellation between stages, allocation failure, malformed offsets at trust boundaries, worker loss, and backpressure. Confirm buffers are neither reused early nor retained indefinitely.

Performance experiments must hold algorithms, data structures, semantics, data, compiler settings, and parallel framework constant when isolating execution models. Report compilation and warm-up, cold/warm cache, batch size/distribution, encodings/selectivity, threads/NUMA placement, memory/spill, CPU counters, first/total latency, and repeated-run statistics. Throughput on one analytical query does not establish transaction latency, extension ergonomics, or universal superiority.

## Definitions and Notation

- **c**: logical row cardinality of a batch.
- **b**: chosen target batch size; final or filtered batches may contain fewer live rows.
- **S**: ordered selection of live indices in `[0,c)`.
- **Vj**: validity bitmap or logical validity predicate for column j.
- **h**: idealized fixed dispatch/control overhead per batch.
- **w**: idealized useful per-row work for a particular kernel and input.
- **Vector**: typed logical sequence with length, validity, representation, buffers, and ownership.
- **Batch/data chunk**: equal-cardinality vectors forming rows by aligned position.
- **Flat encoding**: values stored directly by position in a conventional contiguous representation.
- **Constant encoding**: one physical value represents every logical position, with validity semantics.
- **Dictionary encoding**: indices select positions in a referenced child/base vector.
- **Selection vector**: ordered indices of rows active for later processing.
- **Compaction**: copying or rewriting selected logical rows into dense positions.
- **Kernel**: implementation processing one or more vectors/selections into vector or state output.
- **Pipeline**: schedulable region from source through nonbreaking operators to sink.
- **Breaker**: dependency/materialization boundary between pipeline regions.
- **Morsel**: bounded source range or work unit assigned to a worker.
- **Fusion**: executing multiple operations within one loop/code region without a full intermediate boundary.
- **Backpressure**: feedback/credits that bound production by downstream capacity.

The approximation `w + h/b` isolates dispatch amortization only. It is not a complete cost model or latency prediction.

## Mechanisms, Invariants, or Proof Structure

**Batch well-formedness.** For every column, logical length equals c. Every selected index is in range. Validity has at least c logical bits. Variable/nested offsets are monotone and bounded by child/data length. Dictionary indices address the referenced child. Buffers remain live. At untrusted boundaries, validate these before kernels derive pointers or lengths.

**Filter correctness.** Assume S represents the input sequence. Evaluate predicate once per selected logical row under SQL semantics, obtaining TRUE/FALSE/UNKNOWN. Construct S' by retaining exactly TRUE positions in S order. Then S' is an ordered subsequence, preserves occurrence identity/multiplicity, and is observationally equivalent to scalar `WHERE`. Vector masks and short-circuit decompositions must implement the same effect/error contract.

**Projection correctness.** For each position in S', evaluate each required expression under the same row environment and align outputs at the corresponding logical output position. Encoded/borrowed outputs are valid only if decoding yields that value throughout the consumer lifetime. Induction over expressions and positions gives equivalence to scalar projection, conditional on kernel/type correctness.

**Pipeline composition.** If each stage consumes the exact logical output of its predecessor and implements its local transformation, composition implements the stage sequence. Fusion removes physical boundaries but not logical sequencing/effect constraints. A breaker establishes a dependency: downstream source becomes ready only after its required upstream state is complete and safely published.

**Morsel invariant.** Pending, running, completed, or cancelled ownership partitions the declared morsel set. A transition moves one morsel atomically between states. Completion records all its contributions before publication; cancellation prevents further claims and cleans partial private state. Work stealing changes worker ownership, not logical coverage. Shared reductions require their own merge correctness.

**Backpressure invariant.** In-flight batches/bytes/tasks remain below configured query, tenant, and global bounds. A producer without credit must suspend or cooperatively perform other eligible work; it cannot allocate indefinitely. Stop/error wakes blocked parties and causes ownership-aware release.

**Evidence separation.** The executable proves finite scalar/batch equivalence only. Symbolic review checks invariants. Sources substantiate research and versioned product descriptions. Hardware, compiler, scheduler, memory, and production performance require controlled target measurements.

## Alternatives and Trade-Offs

**Tuple iterators** minimize batch buffering and naturally support early demand, but pay per-row control and often weak locality.

**Vector pull** amortizes calls and exposes typed arrays while preserving demand direction. It can overproduce up to a batch and still needs scheduler machinery for parallel pipelines.

**Vector push/drivers** map naturally to pipeline tasks and sinks. They require explicit backpressure, stop propagation, and careful multi-input dependencies.

**Data-centric compilation** can fuse pipelines and remove generic dispatch. It adds compile/optimization latency, code memory, invalidation, security, debugging, and fallback needs.

**Vectorized interpreted kernels** reuse tested primitives and avoid per-query code explosion. Generic decoding and kernel boundaries can add instructions/indirection, especially for cache-resident simple queries.

**Bytecode or micro-operation engines** choose an intermediate granularity and can specialize common sequences. Dispatch and representation remain costs; they may offer smaller code footprint than native compilation.

**Selection retention** avoids copies and favors selective pipelines. **Compaction** improves dense downstream locality and releases base buffers sooner. Choose using selectivity, downstream expense, encoding, lifetime, and memory pressure.

**Encoding-aware execution** can compute directly on constants/dictionaries/compression. It multiplies kernel variants and correctness cases. A unified decoded view simplifies extensions but may sacrifice opportunities.

**Fixed batches** simplify allocation and testing. **Adaptive batches** respond to width, selectivity, latency, device, or cache but make scheduling/capacity less predictable.

**Morsel scheduling** dynamically balances work and can respect NUMA. Static partitions reduce scheduler overhead and can preserve locality, but suffer skew and stragglers.

## Failure Modes and Misconceptions

1. **“Vectorized means SIMD.”** Batching enables but does not guarantee SIMD.
2. **“A vector is just an array.”** Validity, encoding, selection, nested offsets, ownership, and type semantics are part of it.
3. **“NULL payload is zero.”** Payload behind invalid slots may be unspecified and must be masked.
4. **“Selection is a set.”** Order and duplicate positions can matter; its exact contract is sequence-like unless specified otherwise.
5. **“Flattening is harmless.”** It spends bandwidth, loses compression/laziness, and can extend or shorten lifetimes.
6. **“Largest batch wins.”** Cache, latency, tail work, memory, and cancellation can reverse the result.
7. **“Push has automatic backpressure.”** It needs an explicit bounded protocol.
8. **“Fusion is always faster.”** Code size, compilation, branches, reuse, and selectivity create counterexamples.
9. **“One plan is one pipeline.”** Breakers and build/probe dependencies create a graph.
10. **“All workers may probe while build finishes.”** Only an explicitly concurrent algorithm permits it; ordinary build publication needs synchronization.
11. **“Work stealing makes locality irrelevant.”** It trades balance against NUMA/cache locality.
12. **“Compiled excludes vectorized.”** Compiled code can process batches/SIMD; categories overlap at mechanism boundaries.
13. **“Zero-copy means zero cost.”** Indirection, retained parents, cache misses, validation, and lifetime coordination remain.
14. **“Fast microkernels prove query speed.”** Joins, materialization, memory bandwidth, scheduling, compilation, and sinks may dominate.

## Worked Examples

### Example 1

**Situation:** A flat score vector has validity `1101`; the third payload contains 9 from reused memory but its validity is zero. A kernel compares all payloads without masking and accepts it. **Conclusion:** logical values are payload plus validity; invalid payload must never drive SQL results.

### Example 2

**Situation:** A filter over eight rows yields selection `(1,5,7)`. Projection reads physical positions `(0,1,2)` instead, returning three plausible wrong rows. **Conclusion:** every downstream kernel must honor the current selection or receive correctly compacted input.

### Example 3

**Situation:** A dictionary vector uses indices `(2,0,2)` over base `("red","blue","green")`. Flattening yields `("green","red","green")`; direct dictionary-aware equality with `"green"` can compare dictionary entries once then map indices. **Conclusion:** encoding-aware execution can reduce work but must preserve index validity, NULL, and base lifetime.

### Example 4

**Situation:** Dispatch overhead is 200 ns per call and useful work 20 ns per row. The simplified contribution is 220 ns/row at b=1 and 21.56 ns/row at b=128. But a wider working set now misses cache and raises real cost to 35 ns/row. **Conclusion:** amortization math identifies one force, not the optimum.

### Example 5

**Situation:** `LIMIT 1` sits above a push pipeline with batches of 2,048. If the first row qualifies, 2,047 rows may already have been evaluated. A stop signal prevents later batches but cannot recover completed work. **Conclusion:** batch size and cooperative stop affect latency/overproduction.

### Example 6

**Situation:** Hash join decomposes into build and probe pipelines. Four build tasks finish, but the scheduler releases probe after only three publish their partitions. Probe misses matches. **Conclusion:** a pipeline breaker includes a complete dependency/publication protocol, not just an in-memory hash table.

### Example 7

**Situation:** Two workers share a mutable output vector. Both reserve overlapping positions because cardinality updates are unsynchronized. Use worker-private batches or atomic/nonoverlapping reservations and merge under a defined order policy. **Conclusion:** buffer ownership is part of parallel correctness.

### Example 8

**Situation:** A sparse selection keeps 10 rows from a million-row base vector. Zero-copy dictionary output avoids ten copies but retains the entire base buffer across a slow exchange. Compacting ten rows frees nearly all memory. **Conclusion:** copy avoidance can increase peak retention; optimize the complete lifetime.

### Example 9

**Situation:** A compiled plan runs in 4 ms after 20 ms compilation; a vector plan runs in 7 ms without compilation. One execution favors vector at 7 versus 24 ms. Ten equivalent executions can favor cached compiled code at about 60 versus 70 ms, subject to invalidation and parameters. **Conclusion:** report and model compilation amortization.

### Example 10

**Situation:** A benchmark compares vector hash join with compiled nested loop on different layouts and claims vectorization wins. Algorithm and representation confound the result. An apples-to-apples experiment holds algorithms, structures, data, parallel framework, and semantics constant. **Conclusion:** execution-model evidence requires controlled comparability.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies bitmaps, arrays, dictionaries, hash tables, heaps, buffer layouts, and compressed representations.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies cache-aware analysis, batching, SIMD-aware kernels, external memory, and reproducible benchmarking.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies work stealing, queues, barriers, cancellation, backpressure, ownership, and memory models.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) supplies IR, specialization, vectorization, code generation, optimization budgets, and deoptimization.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains caches, TLBs, branches, SIMD lanes, prefetching, memory bandwidth, and NUMA.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) contributes scheduling, virtual memory, asynchronous I/O, affinity, and resource accounting.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) extends batches and pipelines through columnar files, shuffles, vectorized transformations, and bounded streaming.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) contributes workload admission, multi-tenant quotas, observability, rollout, and hardware-aware scheduling.

## References

1. Peter Boncz, Marcin Zukowski, and Niels Nes, [“MonetDB/X100: Hyper-Pipelining Query Execution”](https://www.cidrdb.org/cidr2005/papers/P19.pdf), CIDR 2005. Primary vectorized execution and CPU-efficiency study.
2. Thomas Neumann, [“Efficiently Compiling Efficient Query Plans for Modern Hardware”](https://www.vldb.org/pvldb/vol4/p539-neumann.pdf), *PVLDB* 4(9), 2011. Primary data-centric compilation design and evaluation.
3. Timo Kersten et al., [“Everything You Always Wanted to Know About Compiled and Vectorized Queries But Were Afraid to Ask”](https://www.vldb.org/pvldb/vol11/p2209-kersten.pdf), *PVLDB* 11(13), 2018. Controlled comparison of vectorized and compiled execution.
4. Viktor Leis et al., [“Morsel-Driven Parallelism: A NUMA-Aware Query Evaluation Framework for the Many-Core Age”](https://doi.org/10.1145/2588555.2610507), SIGMOD 2014. Primary dynamic scheduling and NUMA-aware pipeline framework.
5. DuckDB Foundation, [Overview of DuckDB Internals](https://duckdb.org/docs/current/internals/overview), retrieved 2026-08-30. Current push-based vectorized execution description.
6. DuckDB Foundation, [Execution Format](https://duckdb.org/docs/lts/internals/vector), retrieved 2026-08-30. Current vector/data-chunk cardinality and flat, constant, dictionary, sequence, unified, string, and nested formats.
7. Apache Arrow Project, [Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html), retrieved 2026-08-30. Official typed array, validity, buffer, variable-width, nested, and dictionary layout specification.
8. Meta Platforms, [Velox Vectors](https://facebookincubator.github.io/velox/develop/vectors.html), retrieved 2026-08-30. Current vector type, size, buffer, and encoding documentation.
9. Meta Platforms, [Velox Expression Evaluation](https://facebookincubator.github.io/velox/develop/expression-evaluation.html), retrieved 2026-08-30. Current vectorized expression compilation/evaluation and encoding behavior.
10. PostgreSQL Global Development Group, [PostgreSQL 18: Just-in-Time Compilation](https://www.postgresql.org/docs/18/jit.html), retrieved 2026-08-30. Current JIT scope and configuration documentation.

## Exercises

### Exercise 1

Specify the well-formedness conditions for a selected dictionary-encoded nullable vector of c logical rows. Explain which layer owns each check at a trusted internal boundary versus an untrusted interchange boundary.

### Exercise 2

For a 10-row batch with selection `(0,2,3,7,9)`, predicate results TRUE, UNKNOWN, FALSE, TRUE, TRUE in selection order. Derive the output selection and prove that it is an ordered scalar-`WHERE` equivalent.

### Exercise 3

A vector pipeline is slower after a release. Profiles show the same rows and algorithm, but batch size changed from 1,024 to 8,192, dictionary inputs are flattened, and one sparse selection retains large parents. Give a disciplined diagnosis and correction plan.

### Exercise 4

Compare vector interpretation and data-centric compilation for (a) a one-shot selective dashboard query, (b) a repeated cache-resident aggregation, and (c) extension-heavy nested types. State what must be measured.

### Exercise 5

Design a parallel hash-join pipeline scheduler with morsels, NUMA-aware build/probe state, backpressure, limit/cancellation, failure cleanup, and reproducible evidence. Identify pipeline boundaries and publication invariants.

## Answers to the Exercises

### Answer 1

Require batch cardinality c; a selection whose ordered indices are all in `[0,c)` with duplicate policy explicit; a validity domain of at least c positions; a dictionary-index vector of logical length c (or compatible selected view); every valid selected dictionary index in the child range; child type compatible with the logical type; NULL semantics distinguishing index validity from child validity; and live immutable/shared or exclusively owned buffers for selection, validity, indices, and child through consumption. Internal constructors may establish these by types and invariants, with assertions/fuzzing at debug/test boundaries. Untrusted Arrow/IPC/plugin input needs checked lengths, offsets/indices, integer overflow, buffer sizes/alignment, schema/type, recursion limits, and ownership before pointer access; validation cannot be skipped because the format is columnar.

### Answer 2

Pair selection positions with predicate outcomes: `(0,T),(2,U),(3,F),(7,T),(9,T)`. SQL `WHERE` retains only TRUE, giving `(0,7,9)`. It is a subsequence of the original selection in the same order. Every selected input position is evaluated once; TRUE positions occur exactly once in output, FALSE/UNKNOWN positions occur zero times, and no unselected position appears. Therefore order and accepted multiplicity match scalar iteration over selection followed by SQL predicate filtering.

### Answer 3

Reproduce with identical data, concurrency, hardware, compiler, and cache state; confirm semantics and row/error counts against the previous version. Separate changes: benchmark 1,024 versus 8,192 while recording first/total latency, batches, tail fill, IPC, branch/cache/TLB misses, bandwidth, and peak memory. Measure flattening frequency/bytes/CPU and test encoding-aware/unified kernels. Track selection density and retained parent bytes/lifetime; compare compaction after high selectivity. Inspect fused temporaries and per-thread working set against caches/NUMA. Correct the causal issue—restore/tune batch size, preserve supported encodings, or compact sparse long-lived outputs—and rerun single/concurrent tail distributions. Do not attribute all regression to “vectorization.”

### Answer 4

The one-shot selective dashboard emphasizes planning/compilation and first-row latency, early stop, batch overproduction, parameter variation, and cache state; vector interpretation or lightweight specialization may win. Repeated cache-resident aggregation can amortize compilation and benefit from fewer instructions/fused loops, while vector kernels may hide latency and exploit SIMD; measure compile plus N executions, code cache, instructions, IPC, caches, SIMD, and concurrency. Extension-heavy nested types favor mature encoding-aware vector APIs and reusable kernels unless compilation supports those types without fallback/code explosion; measure flatten/decoding, extension coverage, errors, code size, compilation, and maintenance. In all cases hold algorithms/data structures/semantics constant and report rows, types/encodings, batch sizes, hardware, memory, and first/total latency.

### Answer 5

Build-side scan/filter is a pipeline ending in worker-private or partitioned hash-build sinks. A barrier combines/publishes complete immutable probe-visible state; probe-side scan/filter/join/output is a dependent pipeline. Partition source into bounded morsels carrying query/attempt/NUMA identity. Schedule locally first, allow measured stealing, and atomically transition each morsel pending→running→completed/cancelled so coverage is neither lost nor duplicated. Reserve memory for build and bounded queues; spill or reject under policy. Probe cannot start against ordinary state until all required build partitions are complete and publication has release/acquire synchronization. Downstream credits bound output; limit revokes source claims and cancels queued/running work cooperatively. Errors cancel siblings, close I/O, discard unpublished state, and idempotently clean spill/queues. Evidence includes per-morsel ownership, rows/hashes/matches, build barrier, partition reconciliation, duplicate/missing checks, queue peaks, NUMA/steal counters, cancellation latency, cleanup, memory/spill, and deterministic semantic comparison under varied schedules; performance results separately report hardware and distributions.
