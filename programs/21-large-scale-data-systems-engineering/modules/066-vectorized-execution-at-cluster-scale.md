---
module_id: LSDS-066
program: Large-Scale Data Systems Engineering
level: 2
module_number: 66
title: Vectorized Execution at Cluster Scale
status: complete
last_verified: 2026-09-04
---

# Vectorized Execution at Cluster Scale

## One-Page Review

### Governing question

How should a distributed query engine process typed columnar batches across scans, operators, exchange, spill, UDFs, and heterogeneous workers so vectorization improves useful throughput without violating SQL semantics, memory bounds, ownership, recovery, or fairness?

### Essential definitions

- **vectorized execution** applies an operator kernel to a batch of values rather than interpreting one row at a time.
- A **column vector** stores values of one logical field plus type, length, validity, and encoding metadata.
- A **record batch** is a set of equal-length vectors representing rows under one schema.
- A **validity bitmap** marks null versus present values independently of the physical value buffer.
- A **selection vector** identifies active row positions without immediately copying survivors.
- A **dictionary vector** stores indices into shared values; a **constant vector** represents one repeated value; a **lazy vector** defers loading or computation.
- A **kernel** is a typed batch implementation of an expression or operator action.
- **SIMD** executes one instruction over several machine lanes; vectorized execution may benefit from SIMD but does not require it.
- **zero-copy** means a boundary reuses buffers without copying payload, subject to compatible layout and lifetime ownership.
- **materialization** converts encoded, lazy, or selected data into a concrete representation required by a consumer.

### Central model, mechanism, or theorem

For a batch with logical length $n$, a kernel evaluates only active positions $S\subseteq\{0,\ldots,n-1\}$ and combines input validity with operator-specific null rules. A useful cost model is

$$T(n)=T_{setup}+n_aT_{value}+T_{decode}+T_{materialize},$$

where $n_a=|S|$. Batching amortizes setup, dispatch, bounds checks, virtual calls, and transport headers, while columnar layout improves locality and opportunities for SIMD. Larger batches are not unconditionally better: live bytes, cache misses, cancellation latency, network head-of-line blocking, spill, and concurrent-task memory rise. Cluster-scale correctness requires one versioned schema/encoding contract, explicit buffer ownership and lifetime, bounded batches and queues, compatible kernels or fallback on every worker, and identical semantic results across batch partitions.

### Critical invariants

- Every vector has a resolved logical/physical type, nonnegative bounded length, validity contract, encoding, buffer sizes, and ownership.
- All vectors in a record batch represent the same logical row count or a declared nested child relationship.
- Selection positions are in range, follow declared uniqueness/order semantics, and are not mistaken for physical compaction.
- Null, overflow, decimal, floating, collation, time-zone, error, and nondeterministic-expression behavior matches scalar semantics.
- Dictionary, constant, lazy, run-length, and nested encodings are consumed directly only by kernels that declare support.
- Buffer reference/lifetime rules prevent use-after-free, mutation of shared immutable data, leaks, and accounting gaps.
- Exchange/spill serialization validates schema, offsets, lengths, alignment, endianness, encoding, integrity, and protocol version.
- Batch memory, decompression/decoding workspace, operator state, queues, spill, and concurrent tasks fit governed worker/tenant limits.
- Worker instruction-set or accelerator differences choose compatible implementations without changing query semantics.
- Retries, speculation, and adaptive batch changes preserve row multiplicity, order properties, attempt identity, and output commit.

### Common failures

Common failures include calling columnar storage vectorized execution; assuming vectorization implies SIMD; reading value bytes where validity says null; treating a selection vector as compacted storage; retaining a borrowed buffer after its owner releases it; claiming zero-copy across incompatible layouts; forcing dictionary expansion before every kernel; overflowing offsets or `length * width`; using huge batches that exhaust memory under concurrency; allowing UDF fallback to change null or error semantics; mixing workers whose kernels round or overflow differently; measuring rows/s while network, spill, and tail latency regress; and serializing process-local pointers or unversioned native layouts across workers.

### Compact example

A five-position vector contains `(3, null, 8, 1, 10)`. A filter kernel selects non-null values at least 5, producing positions `(2,4)` without copying the values. A projection doubles only those positions, producing `(16,20)`. The logical batch length remains five while active cardinality is two; validity and selection, not sentinel values, define semantics.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) defines analytical storage layout, [LSDS-061](061-distributed-logical-and-physical-plans.md) selects execution conventions, [LSDS-062](062-coordinator-and-worker-architecture.md) negotiates worker capabilities, [LSDS-063](063-exchange-operators.md) moves batches, [LSDS-064](064-distributed-hash-and-merge-joins.md) uses vector kernels, and [LSDS-065](065-partial-and-final-aggregation.md) defines vectorized state updates.

## Governing Question

Row-at-a-time interpretation repeatedly dispatches operators, resolves types, branches on nulls, and touches fields that may not be needed. Vectorized engines pass batches through typed kernels, amortizing overhead and processing adjacent values with cache-friendly loops. Columnar formats can avoid unpacking unrelated fields, and modern compilers or handwritten kernels may use SIMD.

At cluster scale, however, the batch crosses more than an inner loop. It originates in compressed files or connectors, may remain dictionary/lazy encoded, flows through filters and joins, enters exchange, spills, crosses language/runtime boundaries, and runs on workers with different CPUs or versions. Each boundary introduces layout, ownership, memory, compatibility, and failure contracts.

The governing question is how to preserve scalar language meaning while optimizing representation and batch size end to end. Throughput gains matter only if they survive network, scheduling, memory concurrency, skew, UDFs, and tail behavior.

## Why This Matters

Vectorization can multiply useful scan, expression, join, and aggregation throughput, reducing CPU cost and sometimes energy per query. It also changes resource shape: fewer calls but larger transient buffers, different cache behavior, broader failure granularity, more off-heap/native memory, and stronger incentives for zero-copy sharing.

Representation bugs are dangerous. A bad validity offset can attach nullness to the wrong rows. Dictionary indices can refer beyond their dictionary. A sliced vector can outlive its parent buffer. A native kernel can differ from scalar overflow behavior. One worker using a different instruction implementation can make distributed results nondeterministic.

Optimization also migrates bottlenecks. Faster compute can expose storage, exchange, decompression, allocator, or downstream limits. A local benchmark over warm fixed-width arrays does not prove a cluster win over strings, nested values, skew, cold caches, concurrency, spill, retries, and mixed worker hardware.

## Prerequisites and Retrieval

Review analytical storage layouts in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), shuffle and serialization in [LSDS-031](031-shuffle-architecture.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), physical plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator/worker protocols in [LSDS-062](062-coordinator-and-worker-architecture.md), exchange in [LSDS-063](063-exchange-operators.md), joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), and aggregation in [LSDS-065](065-partial-and-final-aggregation.md).

You should understand arrays, bitmaps, offsets, alignment, CPU caches, branches, SIMD, schemas/types, SQL nulls, buffers, reference ownership, compression, exchange, spill, memory accounting, retries, and performance measurement.

## Learning Objectives

After this module, you should be able to:

1. distinguish storage columnarity, vectorized kernels, SIMD, code generation, and pipeline fusion;
2. specify flat, constant, dictionary, lazy, run-length, variable-length, and nested vector contracts;
3. implement selection and validity semantics equivalent to scalar evaluation;
4. choose batch sizes by setup, cache, memory, cancellation, network, and concurrency evidence;
5. design explicit buffer ownership, slicing, zero-copy, materialization, and memory accounting;
6. preserve schema and encoding across scan, operator, exchange, spill, UDF, and language boundaries;
7. dispatch compatible kernels across heterogeneous worker instruction sets and versions;
8. integrate vectorized joins, aggregation, filtering, backpressure, spill, retries, and adaptation;
9. instrument useful throughput, decode/materialization, memory, stalls, tails, and fallback; and
10. validate semantic equivalence, buffer safety, compatibility, failure, and performance.

## Core Exposition

### Distinguish related execution techniques

Columnar storage groups values by field on disk; vectorized execution processes batches; SIMD uses hardware lanes; code generation specializes expression loops; operator fusion removes intermediate materialization. They reinforce one another but remain independent choices.

A vectorized engine may execute portable scalar instructions inside a tight loop. A row engine may use SIMD within one expression. State which layer supplies each benefit so benchmark attribution and fallback are honest.

### Define a vector contract

A vector declares logical type, physical representation, length, optional offset/slice, validity, encoding, buffers, children, ownership, mutability, alignment, and version. Validate lengths and sizes before access. Zero length is valid and must not require dereferencing absent buffers.

Logical type includes precision, scale, time-zone behavior, collation, nesting, and dictionary domain where relevant. Physical width alone cannot distinguish an integer from encoded decimal or timestamp semantics.

### Represent nulls independently

A validity bitmap commonly uses one bit per logical position. Value bytes at a null position may be unspecified and must not be interpreted. Slicing adjusts bitmap offset; kernels must handle non-byte-aligned starts correctly.

Compose null rules per expression. Arithmetic may be null-propagating, `IS NULL` is not, and three-valued Boolean logic needs true/false/unknown behavior. Fast paths for no-null batches must verify that fact rather than infer it from a missing unchecked pointer.

### Use selection vectors safely

A filter can return indices of passing positions, a bitmap, or a compacted batch. Selection avoids copying and allows later kernels to skip rejected rows. It also creates indirect access and may reduce locality when sparse or unordered.

Declare whether positions are sorted, unique, and relative to the base or current slice. Composing selections maps through prior positions. Operators that require dense contiguous input must materialize explicitly and charge the copy.

### Support multiple vector encodings

Flat vectors store each value directly. Constant vectors represent repetition. Dictionary vectors store indices into a base vector. Run-length encodings store value/count runs. Lazy vectors defer loading or expression evaluation. Encodings can save CPU, memory, and I/O when kernels propagate them.

Each kernel advertises supported encodings and either evaluates directly, unwraps safely, or requests materialization. Avoid combinatorial specialized code by sharing decoding adapters, but measure the cost. Nested dictionaries require validated index composition and lifetime.

### Represent variable-length values

Strings and binary values commonly use an offset buffer plus data bytes. Validate monotone offsets, terminal offset within data size, integer overflow, and slice base. Large-value representations may use views or external buffers with different ownership.

Filtering only offsets/indices can avoid copying bytes. Projection that transforms strings may allocate variable output unpredictably. Bound total bytes, not just row count, when choosing batch and exchange limits.

### Represent nested data

Lists use parent validity and offsets into a child vector; structs use aligned child lengths; maps add key/value constraints. Parent selection can create noncontiguous child ranges. Materialization must preserve empty versus null collections and child nulls.

Recursive schemas and deeply nested values need depth and size limits. Kernels should project only required paths and preserve parent-child ownership. Validate offset arithmetic before allocating or accessing untrusted input.

### Choose batch size empirically

Small batches pay setup, dispatch, virtual call, transport header, and branch overhead repeatedly. Large batches amortize overhead but increase live memory, cache pressure, latency to first output, cancellation delay, imbalance, and retry work.

Choose by bytes and value shape as well as rows. Coordinate scan batch, operator output, exchange page, spill block, and UDF batch instead of letting each expand independently. Test concurrency because one excellent single-query batch may exhaust a worker across many tasks.

### Understand cache behavior

Column vectors let a kernel stream through needed values, but working set includes validity, selections, dictionaries, hash state, outputs, and concurrent operators. A batch larger than useful cache can increase misses. Variable-length indirection and dictionaries may produce random access.

Measure cache misses, memory bandwidth, branch behavior, cycles per value, and NUMA locality rather than assuming contiguous equals fast. Prefetch and software pipelining require architecture-specific evidence.

### Use SIMD without changing semantics

SIMD kernels process several fixed-width values per instruction and often use masks for validity and comparisons. Handle tails beyond a full lane, unaligned inputs, and exceptional values. Do not read beyond validated buffers even if hardware tolerates speculative aligned loads.

Integer overflow, decimal rounding, floating NaN/signed zero, division errors, and Boolean unknown must match the language contract. A scalar fallback and SIMD path need differential tests on every supported instruction set.

### Fuse expressions and pipelines selectively

Fusion combines filter/project or neighboring operators into one loop, reducing virtual dispatch and intermediate batches. Code generation can specialize types and constants. Excessive fusion creates large code, compilation latency, instruction-cache pressure, and difficult fallback.

Blocking operators, exchange, spill, and shared reuse form natural boundaries. Attribute CPU and rows to fused subexpressions so observability does not disappear. Cache compiled code using semantic/session/version-safe keys.

### Vectorize filtering and projection

Evaluate predicates over active positions and produce a selection/bitmap. Apply projection only to survivors when legal, but preserve expression error and volatility ordering required by the language. Some eager-versus-lazy evaluation changes whether an error occurs.

Allocate outputs after estimating surviving rows/bytes or grow under strict bounds. Constant folding and dictionary-aware comparison can avoid value decoding, provided collation, type, and null semantics are compatible.

### Vectorize hash joins

Hash build kernels derive keys for batches, update buckets, and retain every duplicate row. Probe kernels hash active non-null ordinary-equality keys, gather matches, apply residuals, and may expand one input position into many output rows. Output size can exceed batch size sharply.

Bound match expansion and output buffers; resume a probe position across output batches without duplicating or skipping matches. Dictionary keys can accelerate repeated hashes but must not turn dictionary identity into value equality incorrectly.

### Vectorize aggregation

Aggregation kernels map active rows to group state and update several states per batch. Group IDs can avoid repeated hash lookup after grouping. Null/filter/distinct/order semantics remain those defined by the aggregate contract.

State updates may scatter randomly and become memory-bandwidth limited. Separate fast fixed-size states from variable states, bound new groups, and spill consistently. Vectorization does not make holistic or giant hot-group state bounded.

### Decode storage selectively

Parquet, ORC, and other columnar sources use dictionary, run-length, bit-packed, delta, and compressed encodings. Predicate and projection pruning can avoid pages/columns. Decode only selected ranges or keep compatible encodings into kernels where supported.

Separate decompression from semantic decode and record both. File statistics and dictionaries require trust/validation. Corruption, malformed lengths, or decompression bombs must fail within resource and integrity limits.

### Cross exchange boundaries

Exchange pages need versioned schema, field order/identity, physical types, validity, offsets, dictionaries, nested children, compression, checksum, and attempt identity. Process-local pointers or allocator metadata never cross. Negotiate protocol and maximum uncompressed size.

Columnar exchange can avoid row conversion, but partitioning often gathers selected rows into destination-specific batches. Account for scatter/gather and copy. Receiver credits must bound decoded and decompressed memory, not only wire bytes.

### Spill vectorized state

Spill batches or operator states in a stable self-describing format with query/operator/partition/attempt identity, schema/version, lengths, checksums, and completion manifests. Large batches improve sequential I/O but increase recovery/cancellation granularity.

Async spill owns buffers until durable completion; upstream must not reuse or mutate them. Copy-on-write or immutable references make ownership explicit. Bound pending writes and account memory held by I/O libraries.

### Cross language and process boundaries

A standard memory interface can share schema and buffers between runtimes, but zero-copy requires compatible devices, address spaces, alignment, ownership callbacks, and lifetime. Foreign runtimes may copy, retain, or mutate unless the contract forbids it.

Propagate errors and cancellation across the boundary. Account native/off-heap buffers to the query and worker, not only managed heap. Validate foreign schemas and offsets as untrusted input.

### Handle UDFs explicitly

Scalar UDF calls per row destroy batching overhead. Vector UDFs accept and return batches, but must declare type/null/error/determinism, supported encodings, memory ownership, batch limits, and side effects. Sandbox/resource controls remain.

Fallback can materialize and cross a language boundary; expose it in the plan and metrics. A UDF must not retain borrowed input after return unless it acquires ownership. Retry of effectful UDFs requires a separate commit contract.

### Negotiate heterogeneous workers

Workers advertise CPU architecture, instruction extensions, accelerator/device support, vector protocol, kernel/library versions, and semantic compatibility. Planning selects a portable baseline or variants with the same result contract. Placement must not strand fragments on incompatible workers.

Dispatch should check operating-system enablement as well as hardware claims. A worker upgrade that changes vector state or exchange encoding needs version negotiation or draining. Performance heterogeneity can create stragglers even when semantics match.

### Keep memory accounting complete

Charge value/validity/offset/index buffers, selections, dictionaries, lazy loaders, decoded temporaries, outputs, hash/aggregate state, exchange, spill queues, compiled code, and allocator fragmentation. Shared buffers need an ownership/accounting policy that avoids both omission and arbitrary double charging.

Reserve before allocation and return on actual release. Native allocations and pinned/device memory count. Memory arbitration may request spill or batch reduction, but cannot revoke buffers still used by another asynchronous component.

### Integrate backpressure and fairness

Downstream credit limits how many output batches remain live. When blocked, kernels yield instead of accumulating. Cooperative scheduling should bound rows/time per driver turn so one fast vectorized pipeline does not monopolize a worker.

Batch size influences fairness and cancellation latency. Tenant CPU accounting includes decode, compilation, native kernels, and retries. Faster kernels may increase source or exchange load, so admission and dependency envelopes still apply.

### Adapt batch and representation

Observe value widths, selectivity, cache/memory pressure, output expansion, spill, and downstream credit. Adjust future batch row targets within min/max byte/row bounds. Change at batch boundaries and preserve selection/order/state continuity.

Adapt dictionary preservation versus flattening, fusion, and kernel variant only when semantics match. Add hysteresis to avoid representation thrash. Record policy/model generation and chosen reasons for regression diagnosis.

### Observe the full pipeline

Correlate query/plan/operator/kernel/version, fragment/task/attempt/worker, input encoding, batch, exchange/spill, and fallback. Emit rows, active positions, batches, logical/physical bytes, null density, selectivity, materializations, copies, decode/decompress, allocations, peak live memory, CPU, stalls, and tail.

Separate useful output from processed and retried work. Report scalar/SIMD/UDF fallback, instruction set, compilation, skew, backpressure, and errors. Sample low-level counters responsibly and retain semantic failure evidence.

### Validate semantics and safety

Differentially compare scalar and vector paths for every type/operator/kernel. Partition identical input into different batch sizes and encodings; output must remain semantically equivalent. Generate empty batches, all-null, sparse selections, slices, dictionary chains, malformed offsets, nested data, extremes, NaN, overflow, and output expansion.

Use sanitizers/fuzzing where available for native memory and interface boundaries. Inject worker loss, retry, spill failure, exchange corruption, cancellation, mixed versions, and feature fallback. Benchmark cold/warm, realistic strings/nesting/skew, concurrency, memory limits, network, spill, and full query tails.

## Definitions and Notation

Let batch $B=(\sigma,n,V,S)$ have schema $\sigma$, logical length $n\ge0$, field vectors $V$, and active selection $S\subseteq\{0,\ldots,n-1\}$. Without an explicit selection, all positions are active. Each vector $v$ has validity function $\eta_v(i)$ and encoding $e_v$.

A kernel $K_{\tau,e,a}$ is specialized by logical/physical type $\tau$, supported encoding $e$, and architecture/implementation $a$, but must implement common semantic function $\llbracket K\rrbracket$. Fallback $K_0$ and optimized $K_a$ are equivalent when outputs/errors/effects match under the language's defined tolerance and ordering.

Let setup cost be $c_0$, active-position cost $c_v$, decode/materialization cost $c_d$, and batch active cardinality $n_a=|S|$. Approximate time $T=c_0+n_ac_v+c_d$ explains amortization but omits caches, branches, bandwidth, downstream blocking, concurrency, and output expansion.

Peak governed memory includes live input $M_i$, output $M_o$, temporaries $M_t$, operator state $M_s$, exchange/spill queues $M_q$, foreign/native/device allocations $M_f$, and allocator overhead $M_a$. Shared ownership must define attribution; physical safety still requires actual total live bytes below capacity.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Fix scalar semantics for types, nulls, overflow, errors, volatility, ordering, duplicates, and effects.
2. Define vector schema, length, validity, encoding, offsets/children, selection, ownership, mutability, alignment, and version.
3. Implement encoding- and architecture-aware kernels with verified scalar fallback, tails, bounds, and output expansion.
4. Choose byte/row batch limits across scans, operators, exchange, spill, UDFs, and concurrency using cache/memory evidence.
5. Negotiate schemas/encodings/capabilities at storage, exchange, process, language, and heterogeneous-worker boundaries.
6. Account and bound every buffer, decode workspace, shared lifetime, async I/O, operator state, queue, and native/device allocation.
7. Propagate credit/cancellation/fairness and preserve attempt, partition, order, state, and commit semantics through retry.
8. Adapt future batches/encodings/kernels only at safe boundaries with hysteresis and generation evidence.
9. Observe useful versus processed work, materialization, copies, memory, CPU/hardware counters, backpressure, fallback, tails, and cost.
10. Differential/property/fuzz test representations, fault-inject distributed boundaries, benchmark realistic concurrency, canary, and roll back.

Batch partition invariance requires concatenated vector results to equal scalar evaluation in logical row order, except where order is unspecified. It assumes stateful operators carry correct state across batch boundaries and nondeterministic/effectful expression evaluation follows its contract.

Selection-vector filtering is correct when it contains exactly positions whose predicate evaluates true; false and unknown are excluded. Subsequent kernels must dereference original positions or a correctly composed selection, not treat selection ordinal as base position.

Zero-copy improves copy cost only when producer and consumer layouts are compatible and lifetime/ownership keeps buffers valid. It is not proof of lower end-to-end time or memory: shared retention can increase peak lifetime.

## Alternatives and Trade-Offs

- **Row-at-a-time interpretation:** simple and responsive; repeated dispatch and poor column locality.
- **Vectorized kernels:** amortized overhead and cache-friendly loops; larger live buffers and representation complexity.
- **SIMD specialization:** high fixed-width throughput; architecture variants, tails, and semantic edge cases.
- **Code generation/fusion:** removes dispatch/materialization; compilation and instruction-cache cost plus harder observability.
- **Flat vectors:** simple direct access; duplicate constants/dictionaries and copies.
- **Dictionary/constant/lazy vectors:** avoid decode/copy/work; indirect access and lifetime/compatibility complexity.
- **Selection vectors:** cheap filtering; sparse indirection and composition cost.
- **Physical compaction:** dense downstream access; copies variable-width/nested data.
- **Large batches:** amortize setup and transport; memory, cache, tail, cancellation, and retry granularity worsen.
- **Small batches:** low latency and memory; dispatch/header overhead rises.
- **Zero-copy interfaces:** reduce payload copies; constrain layout, ownership, mutability, and lifetime.
- **Stable serialization:** portable and recoverable; encode/decode and copy cost.
- **Portable kernels:** uniform compatibility; may leave hardware performance unused.
- **ISA-specific kernels:** exploit workers; dispatch/testing/straggler complexity.
- **Vector UDFs:** preserve batching; cross-runtime ownership, security, and failure remain.
- **Scalar UDF fallback:** broad compatibility; can dominate CPU and materialization.

## Failure Modes and Misconceptions

- **“Columnar storage means vectorized execution.”** representation on disk does not choose operator granularity.
- **“Vectorized means SIMD.”** batching can help without hardware lanes.
- **“Null has a sentinel value.”** validity, not payload bytes, defines nullness.
- **“Selection length is batch length.”** logical base length and active cardinality differ.
- **“Dictionary identity is value identity.”** different dictionaries can encode equal values at different indices.
- **“Lazy is free.”** deferred I/O/computation can move latency and lifetime unpredictably.
- **“Zero-copy means no allocation.”** metadata, ownership, decoding, and retained buffers still cost.
- **“More rows per batch is faster.”** cache, concurrency, output expansion, cancellation, and spill can reverse it.
- **“Wire bytes bound memory.”** decompression, decoding, dictionaries, and outputs amplify them.
- **“Aligned loads may read padding freely.”** only validated owned ranges are safe.
- **“SIMD and scalar corner cases naturally match.”** nulls, overflow, NaN, signed zero, and errors need differential tests.
- **“Fusion always helps.”** code size, compilation, instruction cache, and fallback may dominate.
- **“Vectorized joins have bounded output.”** duplicate matches can expand one probe position enormously.
- **“Native memory is outside query accounting.”** it still competes for worker capacity.
- **“UDF return releases every input.”** borrowed buffers may be illegally retained.
- **“All workers can run the same binary path.”** ISA, devices, libraries, and protocol versions differ.
- **“Rows per second proves a cluster gain.”** network, memory, spill, fairness, energy, and tail outcomes matter.
- **“Different batch sizes are purely performance.”** state, order, volatility, and bugs can make them semantic boundaries.

## Worked Examples

### Example 1

A vector's null position contains stale bytes `42`. A kernel that skips validity adds 42 to a sum. The correct kernel tests validity and never interprets null payload, while a no-null fast path runs only after validated metadata proves all positions present.

### Example 2

A slice starts at bit offset 3 in a shared validity bitmap. Reading byte-aligned from zero attaches nulls to the wrong rows. Slice metadata retains logical offset and buffer lifetime; kernels compute bit positions correctly or materialize deliberately.

### Example 3

A filter selects positions `(9,40,901)` from a 1,024-row string vector. Passing three indices avoids copying strings, but a dense SIMD consumer may choose compaction. Metrics charge the copy and compare sparse-gather cost rather than declaring either universally faster.

### Example 4

One-million repeated country codes use a 200-value dictionary. A compatible equality/grouping kernel processes indices and dictionary values once. A consumer with incompatible collation materializes canonical values; comparing raw indices would be wrong across dictionaries.

### Example 5

A 64,000-row batch of wide nested values occupies far more than a fixed-width batch and exceeds worker memory under 20 concurrent tasks. Byte and child-value limits shrink the batch while retaining enough rows to amortize setup.

### Example 6

An SIMD division kernel processes full lanes correctly but forgets the three-value tail and returns stale output. Differential tests vary lengths around lane multiples, with null and zero divisors, and compare exact error/result semantics to scalar fallback.

### Example 7

A join probe position has 100,000 duplicate matches. The kernel emits bounded output pages and resumes at the exact build-row offset. Allocating the entire expansion as one batch would violate memory; restarting at zero would duplicate rows.

### Example 8

An exchange frame is 10 MiB compressed but expands to 400 MiB plus offsets. Receiver credit based only on wire bytes admits several frames and OOMs. Credit uses maximum validated decoded footprint and rejects oversized uncompressed declarations.

### Example 9

A Python vector UDF retains an input array after returning. Without ownership transfer, the worker reuses its buffer and corrupts later reads. The interface either copies, transfers/reference-counts ownership, or forbids retention and detects violation.

### Example 10

The fixture applies validity and a selection vector before a projection without compacting the base batch.

<!-- bijux-verify: {"id":"selection-vector-kernel","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"batch_size=5\nselected_positions=(2, 4)\nprojected_values=(16, 20)\n","stderr":""}} -->
```python
values = (3, 999, 8, 1, 10)
valid = (True, False, True, True, True)

selected = tuple(
    position
    for position, (value, is_valid) in enumerate(zip(values, valid))
    if is_valid and value >= 5
)
projected = tuple(values[position] * 2 for position in selected)

print(f"batch_size={len(values)}")
print(f"selected_positions={selected}")
print(f"projected_values={projected}")
```

The placeholder `999` is never read as a logical value because validity is false. Production kernels additionally validate offsets, schemas, encodings, selections, memory ownership, output bounds, and architecture equivalence.

## Cross-Program Connections

- **Computer architecture:** caches, SIMD, branches, memory bandwidth, alignment, NUMA, and instruction sets shape kernels.
- **Algorithms and data structures:** bitmaps, dictionaries, offsets, selections, hashing, sorting, batching, and sketches shape representations.
- **Database systems:** SQL types, nulls, expressions, joins, aggregates, operators, and plans define semantics.
- **Distributed systems:** exchange, attempts, compatibility, backpressure, retries, partial failure, and commit extend vector boundaries.
- **Data engineering:** Parquet/ORC encodings, schemas, nested data, compression, spill, and skew determine workloads.
- **Platform engineering:** worker capabilities, native memory, scheduling, isolation, heterogeneous fleets, and telemetry host execution.
- **Reliability and security:** bounds checking, ownership, fuzzing, malformed inputs, sandboxed UDFs, canary, and rollback protect service.
- **Performance engineering:** amortization, cycles/value, cache misses, materialization, full-query tails, concurrency, and cost test value.

## References

1. Apache Arrow. [Columnar Format.](https://arrow.apache.org/docs/format/Columnar.html) Current array, validity, variable/nested, dictionary, run-end, buffer, alignment, and physical-layout specification.
2. Apache Arrow. [C Data Interface.](https://arrow.apache.org/docs/format/CDataInterface.html) Current cross-runtime schema/array, ownership, release callback, device, and zero-copy interface contracts.
3. DuckDB. [Execution Format.](https://duckdb.org/docs/stable/internals/vector.html) Current vector size, flat/constant/dictionary/sequence vectors, selection vectors, validity masks, and unified format.
4. DuckDB. [Storage.](https://duckdb.org/docs/stable/internals/storage.html) Current row groups, column segments, compression, block, checkpoint, and buffer-management context.
5. Apache DataFusion. [Architecture.](https://datafusion.apache.org/contributor-guide/architecture.html) Current Arrow-native logical/physical plans, execution plans, record-batch streams, optimizer, and operator architecture.
6. Apache Spark. [Apache Arrow in PySpark.](https://spark.apache.org/docs/latest/api/python/tutorial/sql/arrow_pandas.html) Current Arrow-optimized columnar transfer, Pandas UDF, batch, type, and fallback behavior.
7. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current columnar caching, batch-size, compression, vectorized reader, partitioning, and adaptive context.
8. Apache ORC. [ORC Specification v1.](https://orc.apache.org/specification/ORCv1/) Current stripes, streams, indexes, types, run-length, dictionary, bit, integer, decimal, and timestamp encodings.
9. Apache Parquet. [Encodings.](https://parquet.apache.org/docs/file-format/data-pages/encodings/) Current plain, dictionary, run-length/bit-pack, delta, byte-stream, and null-related encodings.
10. Velox. [Vectors.](https://facebookincubator.github.io/velox/develop/vectors.html) Current flat, constant, dictionary, sequence, lazy, row, array, map, decoded, ownership, and memory-pool vector concepts.
11. Velox. [Operators.](https://facebookincubator.github.io/velox/develop/operators.html) Current driver, pipeline, operator, blocking, memory, spill, dynamic filter, and exchange architecture.
12. Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets.](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) Primary account of columnar nested representation and distributed interactive execution.
13. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary account of vectorized operators, distributed execution, repartitioning, aggregation, and production workloads.

## Exercises

### Exercise 1

Specify a vector contract for nullable `LIST<DECIMAL(18,2)>` including parent validity, offsets, child validity/data, slices, bounds, ownership, selection, and exchange versioning.

### Exercise 2

Design scalar, portable vector, and SIMD differential tests for a nullable decimal division expression. Include batch boundaries, selections, overflow, division by zero, rounding, errors, and heterogeneous workers.

### Exercise 3

Choose batch-size policy for narrow integers, wide strings, and nested records under 32 concurrent tasks. Cover setup, cache, bytes, output expansion, exchange credit, cancellation, spill, and adaptation.

### Exercise 4

Design a zero-copy Arrow-style boundary between a native engine and a managed-language UDF. Specify schema, ownership, retention, mutability, accounting, cancellation, errors, and fallback.

### Exercise 5

Design a production evaluation for vectorizing scan, filter, hash join, and aggregation across a heterogeneous cluster. Include correctness, memory safety, failures, workload mix, metrics, canary, and rollback.

## Answers to the Exercises

### Answer 1

The parent declares logical list-of-decimal type, length, slice offset, optional validity bitmap, and offsets of length at least logical range plus one. Validate normalized offsets are monotone, nonnegative, and terminal offset fits child length without integer overflow. Child declares decimal precision/scale, physical width, its validity and data buffers. A null list is distinct from an empty valid list; child null elements are independent. Selection positions refer to parent logical positions and map through parent offsets. Buffers are immutable borrowed or reference-counted/owned with release callbacks; slices retain owners. Exchange fixes field identity/order, endianness/alignment rules, decimal encoding, validity/offset representation, protocol/schema version, maximum lengths/bytes, checksums, and attempt identity.

### Answer 2

Use scalar semantics as an independently reviewed oracle for decimal coercion, output precision/scale, rounding, null propagation, overflow, and division-by-zero error. Generate lengths zero and around every SIMD lane/batch boundary; all-null/no-null/mixed validity; base slices with unaligned bitmap offsets; dense/sparse/reordered selections as permitted; minimum/maximum magnitudes, scale boundaries, zero divisors, and overflow. Compare result validity/values and error timing/category for portable and every supported SIMD path. Partition the same data into different batches and run on heterogeneous workers; semantics must match. Use bounds/memory sanitizers for tails and malformed buffers, and verify fallback is invoked rather than silently changing behavior.

### Answer 3

Use both row and decoded-byte targets with hard maximum uncompressed/value/child sizes. Narrow integers can use larger batches until setup gains flatten or cache/concurrency pressure rises. Wide strings use smaller byte-bounded batches and account offsets/data plus projected output. Nested records include child cardinality/depth and may split before one parent batch becomes huge. Model 32 tasks' simultaneous input, output, temporaries, state, exchange credit, and spill queues with failure headroom. Bound output expansion and time per cooperative turn; smaller batches improve cancellation and fairness. Receiver credit uses decoded footprint. Adapt future batches from observed widths, selectivity, cache/memory pressure, output expansion, and blocked/spill time with hysteresis and min/max bounds.

### Answer 4

Pass validated Arrow-compatible schema/array descriptors and buffers with explicit device/address-space, alignment, validity/offset/nesting, maximum size, and release callbacks. The engine retains ownership until the UDF releases; the UDF may not retain after return unless it acquires a reference or copy. Inputs are immutable; output uses separately owned buffers. Charge shared/native buffers and UDF temporaries to the query until actual release. Propagate cancellation and structured errors, sandbox CPU/memory/time, reject malformed returned offsets/types, and never log sensitive values. If layout/type/device is incompatible, perform an explicit bounded copy/materialization and expose fallback metrics. Effectful UDF retries need a separate commit contract.

### Answer 5

Differentially compare scalar and vector plans over every type/operator using empty/all-null, slices, selections, dictionaries/lazy/nested values, malformed offsets, extreme strings/decimals/floats, duplicate join expansion, high-cardinality/hot aggregates, and varied batch partitioning. Fuzz native/interface boundaries with sanitizers. Inject worker loss, retry/speculation, exchange corruption, spill failure, cancellation, slow consumers, native OOM, UDF failure, mixed versions, and unsupported ISA fallback. Benchmark representative cold/warm scans and concurrent interactive/batch queries across worker types, measuring useful versus processed rows/bytes, cycles/value, cache/memory bandwidth, decode/materialization/copies, peak total native/managed/device memory, network, spill, backpressure, scheduler turns, tails, energy, and cost. Canary bounded worker pools/query classes, freeze on correctness/security/memory/fairness regression, and roll back plan/kernel/protocol generations while draining incompatible attempts.
