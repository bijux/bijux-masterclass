---
module_id: DE-033
program: Data Engineering
level: 1
module_number: 33
title: Dataframe Transformation Pipelines
status: complete
last_verified: 2026-09-02
---

# Dataframe Transformation Pipelines

## One-Page Review

### Governing question

How should a team design dataframe transformations so labeled-column convenience does not obscure row identity, schema and missing-value semantics, join multiplicity, mutation, execution planning, memory pressure, determinism, or atomic publication?

### Essential definitions

- A **dataframe** is a tabular programming abstraction with named columns, row collections, types, and library-specific index, null, ordering, and execution semantics.
- A **logical plan** describes relational/dataframe operations before execution; a **physical plan** chooses scans, projections, joins, aggregations, exchanges, and materialization.
- An **eager** API executes an operation immediately; a **lazy** API records operations for optimization and executes them at a terminal action such as collect or write.
- **row identity** is the domain key or occurrence identity of a record; a positional or labeled dataframe index is not automatically that identity.
- A **schema contract** fixes column names/order where relevant, logical and physical types, nullability, units, time zones, categorical domains, nested shape, and evolution policy.
- **missingness** is a declared domain state represented through library/type-specific null sentinels or validity metadata; it is not interchangeable with zero, empty text, false, or absence of a row.
- **cardinality validation** checks expected one-to-one, one-to-many, many-to-one, or many-to-many key multiplicity at a join boundary.
- **vectorized execution** applies operations to columnar arrays or batches rather than dispatching general-purpose user code once per row.
- A **user-defined function (UDF)** is custom code invoked through a dataframe engine; it can restrict optimization, portability, serialization, typing, and observability.
- **peak live memory** is the maximum simultaneous memory occupied by inputs, outputs, intermediates, copies, shuffle/build state, runtime overhead, and serialization buffers.
- **semantic equivalence** means outputs agree under a declared contract for rows, multiplicities, types, missingness, order if promised, errors/quarantine, and publication.

### Central model, mechanism, or theorem

For input dataframe $D$ and declared transformation stages $T_1,\ldots,T_n$, the candidate output is

$$
O=T_n\circ T_{n-1}\circ\cdots\circ T_1(D;S,\theta),
$$

where $S$ is the schema/semantic contract and $\theta$ includes library/runtime versions, configuration, locale/time zone, source cut, and reference generations. Pipeline notation does not make stages commutative: filtering before version resolution, joining before pre-aggregation, or coercing before validation can change meaning.

If join key $k$ appears $a_k$ times on the left and $b_k$ times on the right, an equality join can emit $a_kb_k$ pairs. A claimed many-to-one enrichment therefore needs $b_k\leq1$ for every permitted key and a declared null-key policy. Some dataframe libraries match missing keys differently from SQL, so the equality relation itself belongs to the contract.

A first memory envelope is

$$
M_{peak}\geq M_{input}+M_{output}+M_{live\ intermediates}+M_{join/shuffle}+M_{conversion}.
$$

File size or final-frame size alone is not a safe capacity estimate.

### Critical invariants

- Every frame boundary declares source generation, row meaning, domain identity, schema, null semantics, ordering promise, and owner.
- Input parsing uses explicit schema and invalid-value policy; inference is evidence for discovery, not a production contract.
- Index/position is never treated as domain identity unless the contract explicitly establishes and validates that mapping.
- Transform functions make mutation/alias behavior explicit and do not depend on version-specific view-versus-copy accidents.
- Filters define how nullable booleans behave; invalid and unknown records are retained, quarantined, or rejected deliberately.
- Joins name keys, expected cardinality, missing-key behavior, overlapping columns, unmatched policy, and fanout evidence.
- Deduplication uses authoritative identity and total winner ordering before payload columns or keys are discarded.
- Aggregations define input grain, null/empty behavior, units, numeric type, rounding, and output grain.
- Eager/lazy/optimizer changes preserve the declared semantic equivalence relation and are inspected through actual plans where available.
- UDFs are isolated, deterministic where required, typed, tested, observable, and used only when native expressions cannot express the contract safely.
- Peak memory, spill, partition/skew, serialization, and retry costs fit the operating envelope at representative scale.
- Candidates write to isolated generations and pass schema, key, reconciliation, security, and performance gates before atomic/conditional publication.

### Common failures

Common failures include relying on inferred `object`/string/numeric types; assuming every null sentinel behaves alike; treating an auto-generated index as a primary key; positional assignment after filtering; chained mutation whose behavior changes across versions; row-wise UDFs for expressible operations; joining on every same-named column by accident; allowing missing keys to match without policy; trusting a many-to-many join because row counts look plausible; dropping duplicates on payload; sorting without a stable tie-breaker; group aggregation that drops missing groups silently; converting time zones after truncating timestamps; collecting a lazy/distributed result to one process unexpectedly; assuming Arrow interchange is always zero-copy; measuring only steady-state frame memory; caching mutable/intermediate state without lineage; writing partitions directly into a trusted path; and claiming parity because totals match.

### Compact example

Six order occurrences enter a finite reference transformation. One invalid amount is quarantined, one older version is superseded, and one authoritative rejected order is excluded. Refund events are aggregated to order grain before enrichment. The candidate has customer `c1` with two accepted orders, 1,700 gross cents, 300 refunds, and 1,400 net cents; `c2` has one order, 800 gross, 100 refunds, and 700 net. Shuffling input order leaves the canonical output unchanged, and the source collections remain unchanged because each stage returns new values.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) defines schema fidelity, [DE-011](011-grain-and-the-meaning-of-a-row.md) defines row meaning, [DE-031](031-extract-transform-load-and-extract-load-transform.md) locates transformation, and [DE-032](032-sql-transformation-pipelines.md) provides graph, fanout, validation, and publication foundations. DE-034 next treats partitioned processing in depth; later modules address incremental models, merges, backfills, corrections, determinism, and batch testing.

## Governing Question

How can dataframe code remain semantically correct, reproducible, resource-bounded, and operable as it moves from an analyst’s notebook to a production pipeline?

Dataframes make column transformations concise. That is their strength and their trap. A few chained calls can parse input, filter rows, join reference data, aggregate, and write output while leaving grain, identity, missingness, execution order, materialization, and resource use implicit. The result may look tabular and plausible even when a join multiplied measures or a type conversion erased evidence.

“Dataframe” is not one universal semantic system. pandas, Polars, Spark, Dask, Arrow-backed tools, and other engines differ in eagerness, index behavior, nullable types, join rules, expression languages, distributed execution, mutation, ordering, optimizer guarantees, and interoperation. API similarity does not prove equivalent results.

A production pipeline must therefore put a contract around the library. It binds exact inputs, schema and domain semantics, deterministic code/config/runtime, candidate materialization, validation, resource evidence, lineage, and publication. The dataframe is a transformation mechanism inside that system—not the source of truth about business meaning.

## Why This Matters

Dataframe code often begins where exploration is appropriate. Automatic type inference, interactive inspection, convenient index alignment, implicit copies, and whole-frame collection help a person learn a dataset quickly. The same behaviors become hazards when data grows, schemas evolve, library versions change, or a task retries unattended.

Types affect meaning. A nullable integer may become floating point when a missing value appears. Text that looks numeric may be parsed differently by locale or error policy. A timestamp may lose its zone or precision. A categorical domain may gain an unknown value. These changes alter equality, grouping, ordering, serialization, and downstream contracts.

Joins amplify risk. A dataframe API may accept a many-to-many merge without complaint; several libraries offer cardinality validation only when requested. pandas currently warns that rows with null keys match each other, unlike usual SQL join behavior. A pipeline ported between dataframe and SQL can therefore change output even if the join type and column names look identical.

Execution mode affects operations. An eager engine creates intermediates immediately. A lazy engine may fuse expressions, reorder filters, prune columns, or choose streaming execution. A distributed engine introduces partitions, shuffles, serialization, retries, and task nondeterminism. Optimizations can reduce cost dramatically, but their plans and semantic assumptions require review.

Memory failures arrive nonlinearly. A 4 GB file can require much more than 4 GB after decoding strings, building object metadata, copying columns, hashing a join side, sorting, or converting between Arrow and another representation. A process killed for memory may leave partial output or trigger an unsafe retry. Capacity and publication are correctness concerns.

Finally, mutable notebook state weakens provenance. A cell can run out of order, a global frame can change in place, and a later cell can produce an output no clean run reproduces. Production functions should accept explicit inputs, return explicit outputs, record runtime identity, and write only isolated candidates until gates pass.

## Prerequisites and Retrieval

Retrieve business questions and output contracts; source owners, snapshots, manifests, partitions and retention; row/event/entity identity; schemas and writer metadata; column names/order, logical/physical types, nullability, units, decimal precision/rounding, encodings, collations, categorical domains, nested values and time zones; invalid/quarantine policy; duplicate/version/delete/late-data rules; reference generations; current code/notebooks/functions; dependency lockfiles and runtime/container; dataframe library and extension versions; eager/lazy/distributed mode; index and alignment use; mutation/copy settings; join cardinalities and unmatched/null-key policy; aggregation rules; UDFs and native alternatives; input/output formats and compression; Arrow/interchange boundaries; memory/CPU/disk/network limits; partition/skew statistics; plan/explain output; orchestrator/retry/concurrency; candidate/publish/rollback protocol; tests/reconciliations; security classification and credentials; lineage/metrics/logging; SLOs; cost; incident history; and disaster-recovery evidence.

Distinguish dataframe index from business key; row label from row identity; row position from order; schema inference from schema contract; physical dtype from business logical type; null sentinel from domain meaning; missing key from unmatched row; equality from library-specific join matching; eager call order from lazy physical execution; logical plan from materialized frame; expression from UDF; vectorization from superficial method chaining; view from copy; Copy-on-Write from immutability; in-memory size from peak live memory; zero-copy capability from an observed zero-copy path; local parallelism from distributed partitioning; `collect` from durable publication; cache from authoritative checkpoint; and successful write from trusted dataset.

Prepare a boundary contract:

| Field | Required content |
|---|---|
| Identity | Stable stage name, owner, code/config/runtime version, consumers |
| Input | Exact generation/manifest, schema, grain, key, expected volume/skew |
| Semantics | Filters, missingness, duplicate/version winner, join, aggregation, time, units |
| Execution | Library/backend/version, eager/lazy/distributed mode, plan, UDFs, mutation policy |
| Resources | Estimated/observed rows, bytes, peak memory, CPU, spill, shuffle, duration, cost |
| Output | Schema/grain/key/order, format, partitioning, compression, candidate identity |
| Gates | Parse/schema, invalid/quarantine, cardinality, reconciliation, security, performance |
| Publication | Atomic/conditional mechanism, receipt, prior generation, rollback and retention |
| Evidence | Input/output digests, metrics, plan, dependency lock, tests, lineage and limitations |

Use representative samples to discover edge cases, then freeze adversarial fixtures and production-scale measurements. A sample that fits memory and contains no null keys cannot establish full-run join or capacity behavior.

## Learning Objectives

After completing this module, you should be able to:

1. define dataframe stages through explicit input, output, schema, grain, and execution contracts;
2. distinguish domain identity and deterministic ordering from index labels and physical row position;
3. control parsing, nullable dtypes, missing-value semantics, time zones, decimals, and categories;
4. design filters, deduplication, joins, aggregations, reshapes, and windows without hidden multiplicity;
5. compare eager, lazy, local, and distributed dataframe execution using logical and physical evidence;
6. manage mutation, aliasing, Copy-on-Write, caches, and function boundaries reproducibly;
7. prefer optimizer-visible vectorized expressions and govern unavoidable UDFs;
8. estimate and measure peak memory, conversion, spill, shuffle, skew, and retry costs;
9. test semantic equivalence across library/runtime/plan changes and dataframe-SQL boundaries; and
10. build, validate, publish, observe, and recover dataframe output generations safely.

## Core Exposition

### Define the frame before touching the API

A dataframe stage is a typed transformation contract. State the authoritative input generation, one-row meaning, occurrence/business keys, permitted duplicates, schema, missing-value meanings, expected count/cardinality ranges, output grain, ordering promise, and invalid-data disposition.

Write the contract independently of pandas, Polars, Spark, or another library. Then map it to concrete dtypes and operations. This prevents a convenient library default from becoming an accidental domain rule.

Separate raw-preservation from typed working frames. Raw source evidence may retain original bytes/text and writer metadata. A typed stage either converts successfully or emits a structured reject with source identity, field, raw value, rule/version, and reason. Silently coercing invalid text to missing loses the distinction between absent and malformed.

Functions should communicate boundaries. A function named by domain responsibility takes explicit frames/configuration and returns a new frame plus evidence or rejects. Avoid relying on global notebook variables, ambient current time, mutable registries, or hidden I/O.

### Treat index and position as representation details

Some dataframe libraries expose a labeled index; others emphasize explicit columns or distributed rows. An automatically generated range index describes current representation, not stable business identity. Filtering, concatenating, resetting, sorting, partitioning, serialization, and library conversion can change it.

Keep domain keys as explicit columns at governed boundaries. If an index is used for performance or alignment, derive it from validated keys and record whether it is unique. Do not discard the columns that make identity portable unless the output format and consumer contract preserve the index explicitly.

Position is not order. “First row” after file discovery, parallel scan, hash join, group-by, repartition, or optimizer rewrite is undefined unless the contract imposes a total order. A stable winner uses authoritative fields and a unique tie-breaker; final output sorting uses explicit keys.

Alignment can be helpful and dangerous. Labeled arithmetic may align by index rather than by physical position, creating missing values or combining the wrong entities when labels differ. Positional arrays may ignore labels and combine unrelated rows. Choose and validate the intended key relation.

### Make schema acquisition explicit

Input inference samples data and chooses physical representations. A later file can introduce a larger integer, decimal scale, unexpected category, invalid timestamp, different zone, or mixed string/numeric field. File order and sample size can influence the inferred result.

Supply explicit reader schemas where the format permits. For schema-bearing formats, validate writer schema, logical annotations, nullability, field IDs/names, and compatibility rather than assuming the reader mapping is lossless. Record the library/backend conversion.

Validate before narrowing. Check integer ranges before downcast; decimal precision/scale before conversion; timestamp zone and ambiguity before localization; strings before categorical enumeration; and nested shape before explode/normalize. Preserve original identity in rejects.

Enumerate output columns and dtypes. A wildcard-like “all columns” selection can propagate new sensitive fields, reorder positional output, or make UDF behavior change. Additive source evolution should not silently mutate a stable published contract.

### Model missingness as domain semantics

Libraries use different sentinels and validity mechanisms. pandas documentation currently distinguishes `numpy.nan`, `NaT`, and nullable `NA` representations by dtype, with possible coercion of ordinary integer/boolean arrays when missingness appears. Arrow uses validity bitmaps in its columnar representation. Other engines have their own rules.

Map each domain state: unknown, not observed, not applicable, redacted, invalid, unmatched join, not-yet-arrived, and deleted. One nullable column may be insufficient; a value plus status/reason can preserve distinctions.

Test equality, sorting, grouping, arithmetic, boolean filtering, filling, serialization, and conversion for missing values. A nullable mask may reject, retain, or error on unknown depending on library/API. A group-by may drop missing group keys unless configured otherwise. An aggregate may skip missing values or return missing for empty/all-missing groups.

Do not fill missing with zero/empty/false merely to satisfy a dtype. Fill only under an approved domain rule, often at a presentation boundary. Retain a quality signal where imputation or defaulting affects interpretation.

### Define filter and quarantine semantics

Break validation into parseable, valid, accepted, and rejected predicates. A record may parse correctly yet violate a business invariant. A rejected record should keep source occurrence identity and reason; aggregate counts alone are insufficient for remediation or replay.

Boolean filters need a policy for missing predicate values. If `is_eligible` is unknown, does the pipeline deny, quarantine, preserve for later enrichment, or treat it as false? Write that choice before the library converts or rejects a nullable mask.

Preserve reconciliation:

$$
N_{input}=N_{accepted}+N_{quarantined}+N_{intentionally\ excluded}
$$

for occurrence-preserving stages, with explicit adjustments for explosion, deduplication, and aggregation. Record reason counts and representative bounded samples without leaking sensitive values.

Push filters toward scans only when doing so preserves parsing, quarantine, security, and audit needs. A lazy optimizer may apply safe predicate pushdown automatically; inspect the logical/physical plan and keep transformations optimizer-visible.

### Resolve identity before dropping duplicates

`drop_duplicates`-style operations remove equal projections according to chosen columns and keep rules. They do not infer entity identity or source authority. “Keep last” depends on order, and order may be physical or incomplete.

Define an identity key and winner tuple. For entity current state, the tuple may include source epoch/version, effective time, correction priority, ingestion sequence, and occurrence ID. Sort or rank by the complete tuple, retain rank one, and separately detect conflicting equal-authority records.

Keep tombstones and rejected versions in the resolution logic when they affect current state. Filtering to active records before selecting the latest can resurrect an older state. This is another example of noncommuting stages.

After resolution, assert key uniqueness and reconcile input occurrences into winners, superseded rows, conflicts, and invalid rows. Do not erase losing evidence before the replay/audit retention boundary.

### Specify joins as contracts

Name left/right grain, key columns and types, expected cardinality, matching equality, null-key policy, unmatched policy, overlapping-column ownership, output grain, and fanout bounds. Never accept the default intersection of same-named columns as an implicit key.

For each key $k$, let left and right multiplicities be $a_k,b_k$. An inner equality join produces $a_kb_k$ pairs when keys match under the library relation. A left join adds unmatched left rows under library-specific missing representation. Validate one-side uniqueness before joining and measure match/fanout afterward.

pandas 3.0 documentation offers `validate` cardinality modes and explicitly warns that null keys on both sides match one another, unlike usual SQL behavior. That is a product/version fact. Do not assume Polars, Spark, SQL, or future versions share it. If missing identifiers must never match, quarantine or split them before the join and test the behavior.

Use merge indicators or equivalent evidence to count left-only, right-only, and matched identities. Resolve overlapping columns explicitly; suffixes prevent name collision but do not establish which value is authoritative.

Pre-aggregate fact-like many sides to the intended join grain. A customer-level summary should not join raw orders to raw refunds and then aggregate unless the cross-product is intended. Assert the aggregate key before enrichment.

### Aggregate from a declared bag

An aggregation’s input is the frame after filters, version resolution, explode, and joins. State this grain and trace multiplicity. Define group keys, missing-key inclusion, measures, null/empty behavior, units, type/overflow, decimal rounding, and output ordering.

Preserve mergeable state where useful: count and sum for means; numerator and denominator for rates; sum, count and sum of squares under numerically appropriate algorithms for variance. Do not average averages or sum percentages without valid weights.

Beware categorical grouping options that emit unobserved categories or change defaults across versions. A grouped result may use keys as an index in one library/configuration and explicit columns in another. Normalize the published schema.

Reconcile additive components before and after aggregation. Compare key sets and group counts as well as grand totals; offsetting fanout and omission can leave a total unchanged.

### Make reshaping and explosion auditable

Exploding a list changes grain from one parent to one element occurrence. Empty lists, null lists, null elements, and repeated equal elements need separate rules. Retain parent and element position/identity if round-trip or deduplication matters.

Pivoting requires a unique value per output coordinate or an explicit aggregation. If duplicates exist, a pivot that aggregates is a semantic operation, not formatting. New category values can add columns and break stable interfaces.

Concatenation aligns schemas by name, position, or configured mode. Canonicalize names, types, units, nullability, and provenance before union. Distinguish vertical occurrence addition from horizontal key alignment.

After reshape, state the new grain and key. Validate conservation relations: exploded element count, parent coverage, allocation sums, and pivot/unpivot round-trip within declared missing/aggregation limits.

### Control ordering and windows

Sort only by explicit typed keys. Locale/collation, missing placement, stability, and categorical ordering can differ. If downstream semantics choose a winner, include a unique authoritative tie-breaker; if sorting is presentation only, say so.

Window calculations need partition key, ordering, frame, minimum observations, missing behavior, and edge policy. Rolling time windows also need time zone, closed-boundary convention, duplicate timestamps, and whether absent periods are materialized.

Distributed/lazy engines may repartition or reorder rows. A prior sort does not necessarily remain a final output guarantee after group, join, concat, or exchange. Apply final canonical ordering only when the contract promises it; avoid expensive global sorting merely for visual neatness.

Canonical comparison sorts by declared key and normalizes types/missingness. Physical file or partition row order should not enter a digest unless it is a promised semantic dimension.

### Prefer native expressions over row-wise UDFs

Native column expressions expose types and operation structure to planners. Engines can vectorize, fuse, push predicates/projections, generate code, parallelize, and inspect lineage. General Python or language UDFs often create per-row dispatch, serialization, opaque null handling, and optimizer barriers.

Use a UDF when the required algorithm is not safely expressible through native operations and the value exceeds its cost. Define input/output schema, null/error policy, deterministic dependencies, batch versus scalar interface, resource limits, side-effect prohibition, and version.

Never perform remote calls, mutable global access, unseeded randomness, current-time lookup, or per-row database queries inside a transformation UDF. External enrichment belongs behind a bounded, cached/versioned input contract.

Test UDFs independently on empty, null, malformed, extreme, Unicode, timezone, and batch-boundary cases. Compare against a reference oracle. Measure serialization and fallback paths at representative scale.

### Understand eager and lazy execution

An eager API materializes each operation as invoked, which supports inspection and simple debugging but can allocate many intermediates. A lazy API builds a plan and executes at collect/sink, enabling projection/predicate pushdown, common-subplan reuse, streaming, or other optimizations.

Polars documents eager and lazy modes, recommends lazy execution for many pipelines, and exposes `explain` to inspect plans; its current examples show projection and predicate pushdown. Spark DataFrames are distributed named-column datasets backed by an optimized SQL execution engine. Dask DataFrame is lazy and triggers work with `compute` or persists distributed state with `persist`. These descriptions do not make the engines interchangeable.

In lazy code, a transformation call may not validate data or contact storage yet. Errors, costs, and side effects occur at terminal execution. Do not report success after plan construction. Capture the optimized plan and terminal job/write receipt.

Optimization must preserve semantics under the engine’s rules. Custom UDFs, volatile functions, row-order assumptions, or side effects can limit safe reordering. Keep pure expressions and explicit boundaries so the planner and reviewer have the same model.

### Treat mutation and aliasing as versioned behavior

Dataframe APIs have varied between mutable objects, views, shallow/deep copies, and copy-on-write. Code that mutates a slice or derived object can update a parent, fail, warn, or allocate depending on library and version.

pandas documentation states that Copy-on-Write is the default/only mode in pandas 3.0 and changes historical chained-assignment behavior. Pinning pandas 3.0 makes that claim usable for one runtime; it does not justify assumptions about older pandas or another library.

Prefer transformation functions that do not mutate caller-owned inputs and that return a clearly owned output. Make intentional mutation local and direct. Avoid chained assignment. Test that sources remain unchanged where the contract promises it.

Copy-on-Write is not functional immutability and does not eliminate memory peaks. A deferred copy may occur at mutation time. Caches, extension arrays, third-party libraries, and conversions have their own ownership rules. Measure the exact workload.

### Build an honest memory model

Start from decoded column buffers, validity bitmaps, offsets, variable-width payloads, categorical dictionaries, indexes, object/reference overhead, and runtime metadata. Add input and output, simultaneously live intermediates, hash/sort state, group tables, shuffle buffers, conversion copies, decompression, serialization, cache, and allocator fragmentation.

For stages $j$, a rough bound is

$$
M_{peak}\approx\max_t\left(\sum_{j\in L(t)}M_j+M_{runtime}(t)\right),
$$

where $L(t)$ is the set of live buffers at time $t$. This is an estimate to validate through measurement, not a universal formula.

Measure resident set size, engine-reported allocations, spill, garbage-collection/allocator behavior, and per-stage row/byte changes. Run representative string cardinality, null density, skew, and join cases. Mean row width hides worst groups and hot keys.

Push projections and filters to scans when semantically safe. Use appropriate columnar formats and encodings. Free/checkpoint intermediates only under clear ownership. If the dataset cannot fit safely with recovery headroom, move to bounded batches, lazy streaming, partitioned/distributed execution, or another engine—without changing the contract silently.

### Treat interchange as a semantic and memory boundary

Apache Arrow specifies a language-neutral columnar memory format with validity metadata and layouts designed for analytical access and possible zero-copy sharing. Compatibility still depends on type mapping, chunks, nulls, offsets, dictionaries, extension types, ownership, alignment, and consumer support.

Arrow’s pandas integration documentation states that zero-copy conversion is possible only in limited cases and that conversion can otherwise create two in-memory representations. Therefore, “Arrow-backed” is not proof of zero-copy or low peak memory. Measure buffer sharing and resident memory for the exact versions/types.

At every interchange, compare schema and values: signedness/width, decimals, timestamps and zones, duration units, strings/binary, categories/dictionaries, nested lists/structs/maps, null versus NaN, metadata, index preservation, and column order. Round-trip fixtures must include edge types.

Record producer/consumer library versions and options. A zero-copy view also creates lifetime/ownership obligations: the producer buffer must remain alive and immutable as required while consumers access it.

### Choose local or distributed execution by evidence

Local in-memory dataframes minimize orchestration and serialization and can be fastest when data and peak working state fit comfortably. Local out-of-core/lazy engines can scan larger-than-memory data with supported streaming operators. Distributed frames add capacity and parallelism but also partitioning, shuffles, skew, serialization, scheduler overhead, retries, and more failure modes.

Do not choose distributed execution from source file size alone. Estimate decoded and peak live state, join build sides, group cardinality, skew, and output. Benchmark representative operations under concurrency and recovery.

API compatibility is incomplete. Dask’s pandas-like syntax, Spark’s named columns, and local pandas expressions can have different supported operations, indexes, ordering, dtypes, nulls, group semantics, and execution. Port through a semantic test suite, not a mechanical syntax translation.

DE-034 develops partitioned processing. At this boundary, record partition keys, sizes, skew, cross-partition operations, global ordering/aggregation needs, and whether local stages are independently composable.

### Make deterministic replay possible

Bind input generations/manifests, code revision, dependency lock/container digest, library/backend versions, configuration, time zone/locale, categorical/reference data, random seeds, thread/partition settings where material, and output writer options.

Replace ambient “now” with a passed evaluation time. Replace unseeded sampling/randomness with an explicit seed when randomness is intended. Avoid filesystem listing order and hash/set iteration as semantic order. Canonicalize output for comparison.

Floating aggregation can vary with reduction order. Decide whether exact decimal/integer arithmetic, tolerance, stable summation, or documented nondeterminism is appropriate. Do not claim byte identity when only tolerance-based semantic equivalence is required.

Re-execution should not mutate original inputs or append duplicate output. Use isolated attempt generations and logical run identity. Resolve unknown writer outcomes before retrying.

### Test functions, stages, plans, and products

Unit tests exercise pure stage functions with small frames and independently derived outputs. Include empty frames, singletons, duplicate labels/keys, nulls and NaNs, invalid casts, extreme values, tied versions, unmatched and many-to-many joins, all-missing groups, empty lists, nested values, boundary timestamps, Unicode, and categorical drift.

Property/metamorphic tests assert invariants: shuffling input does not change canonical output; adding an invalid record increases quarantine only; duplicating an obsolete version does not change winners; adding a refund changes net exactly once; partition recombination matches whole-frame execution for composable stages.

Contract tests compare exact output schema, including logical type, nullability, metadata and column order where consumers rely on it. Data assertions check keys, nulls, domains, relationships, fanout and reconciliations. Differential tests compare dataframe and SQL/reference implementations on the same cut.

Plan tests inspect whether filters/projections push down, UDFs create barriers, joins choose safe strategies, collect points are bounded, and distributed exchanges match expectations. Avoid brittle text snapshots of entire plans; assert risk-bearing properties and measure resource behavior.

Production-scale tests measure peak memory, spill, CPU, serialization, network/shuffle, skew, duration, retries, output size, and cost. Finite tests support a stated envelope; they do not prove arbitrary future inputs.

### Separate candidate creation from publication

Write output to an attempt/generation-specific path or table. Include an exact file/object manifest, schema, counts, partition coverage, digests, code/runtime/input identity, and writer receipt. Do not let workers concurrently mutate a shared trusted directory.

Validate the complete candidate: readable files, exact membership, schema, key uniqueness, no unexpected duplicates, quarantine accounting, join/reconciliation controls, business questions, sensitive-data policy, and representative performance. A successful `to_parquet`, `write`, `collect`, or task return is not a publication gate.

Publish through a verified atomic rename/snapshot commit/catalog transaction or conditional pointer update. Compare the expected prior generation so a late attempt cannot overwrite a newer one. Readers resolve one committed manifest/snapshot, never infer completeness from a directory listing.

Retain the previous valid generation and replay inputs for rollback. On timeout, query the writer job, candidate manifest, and publication receipt by run/attempt identity before retry. Cleanup must not delete active, published, or retained rollback generations.

### Observe, secure, and evolve the pipeline

Record per-stage input/output/reject counts; key/null/duplicate/cardinality distributions; fanout and unmatched counts; additive controls; schema changes; plan; rows/bytes; peak memory; spill; CPU; shuffle/network; duration; output files/partitions; and cost. Dimension evidence by code/runtime/input and candidate generation.

Keep sensitive values out of logs, exceptions, samples, notebook displays, memory dumps, and artifacts. Use least-privilege source, staging, candidate, and publish credentials. Ensure local spill/temp/cache files are encrypted, access-controlled, and deleted under policy. Test tenant separation after joins and reshapes.

Pin dependencies and review release notes before upgrades, especially changes to nullable dtypes, string defaults, Copy-on-Write, grouping, joins, sorting, serialization, Arrow mappings, and optimizer plans. Re-run semantic, round-trip, plan, memory, and performance suites on the same cut.

Classify schema evolution as compatible, breaking, or semantic. Dual-run and compare high-risk changes. Do not let an upstream added column enter stable output automatically. Deprecate old schemas/generations with consumer evidence and explicit retention.

For incidents, preserve input manifest, code/config/runtime, plan, logs, candidate, rejects, metrics, and publication state. Reproduce in isolation, distinguish data defect from library/runtime/resource change, and strengthen the failed invariant. Recovery drills must demonstrate rebuild and publication within the required envelope.

## Definitions and Notation

Let:

- $D$ be an input dataframe whose rows form a bag of occurrences;
- $S=(g,k,c,n,t,o)$ be a contract containing grain $g$, key $k$, column/type schema $c$, null semantics $n$, time semantics $t$, and ordering promise $o$;
- $T_i$ be a declared transformation stage;
- $\theta$ include library/backend/runtime versions, configuration, source/reference cuts, locale/time zone, and execution settings;
- $m_D(r)$ be occurrence multiplicity of visible row value $r$ in $D$;
- $a_x,b_x$ be multiplicities of join key $x$ in left/right frames;
- $Q$ be a quarantine relation retaining source identity, field, raw value or protected reference, rule/version, and reason;
- $L(t)$ be buffers live at time $t$; and
- $G_r$ be an isolated candidate generation for logical run $r$.

The pipeline candidate is

$$
O=T_n\circ\cdots\circ T_1(D;S,\theta).
$$

Stage order matters. For general filter $F$ and version resolver $V$,

$$
F(V(D))\ne V(F(D))
$$

when the newest record is a deletion/rejection filtered by $F$. For conversion $C$ and validation $A$, $A(C(D))$ may lose the raw distinction that $C$ collapsed.

For matching key relation $\sim$, equality-join pair multiplicity is

$$
m_{L\Join R}(l,r)=m_L(l)m_R(r)\quad\text{when }l.k\sim r.k.
$$

The relation $\sim$ must include the library’s missing-key behavior. A many-to-one claim requires $b_x\leq1$ for each permitted right key after its null policy.

For an occurrence-preserving classification stage,

$$
N_D=N_A+N_Q+N_X,
$$

where $A,Q,X$ are disjoint accepted, quarantined, and intentionally excluded occurrences. Deduplication and explosion need separate conservation equations mapping source occurrences to winner/loser or parent/element identities.

A conservative memory model is

$$
M_{peak}=\max_t\left(\sum_{j\in L(t)}M_j+M_{runtime}(t)\right).
$$

This quantity must be measured because ownership, encoding, copies, allocator behavior, plan, skew, and conversion alter it.

Semantic replay requires

$$
T(D;S,\theta)\approx T(D;S,\theta)
$$

under a declared equivalence $\approx$ and identical controlled inputs. It does not promise identical physical buffers, partitions, or row order unless those are part of $S$.

## Mechanisms, Invariants, or Proof Structure

A dataframe pipeline review should:

1. bind exact input generations, row grain/identity, schema, missing/time/unit semantics, and output contract;
2. pin library/backend/runtime, options, dependencies, reference data, and execution mode;
3. validate explicit parsing and reconcile accepted, quarantined, and excluded occurrences;
4. keep domain keys explicit and reject reliance on incidental index/position/order;
5. prove filter, version, join, aggregate, reshape, window, and UDF semantics at every grain change;
6. inspect lazy/distributed logical and physical plans and terminal execution receipts;
7. estimate and measure input/output/intermediate/join/shuffle/conversion peak resources and skew;
8. compare independent oracles, metamorphic properties, schema/key/reconciliation/security gates, and cross-engine results;
9. write one complete isolated candidate generation and publish it conditionally/atomically; and
10. retain source, runtime, plan, metrics, lineage, gates, receipt, and prior generation for replay and rollback.

The executable reference below uses only immutable Python records so the repository verifier needs no optional dataframe package. It models the semantic contract that a pandas/Polars/Spark implementation must match: explicit parsing/quarantine, authoritative version resolution, refund pre-aggregation, many-to-one enrichment, customer aggregation, canonical order, and source nonmutation. It does not verify any dataframe library API, optimizer, dtype, null, memory, distributed, writer, or publication behavior.

<!-- bijux-verify: {"id":"dataframe-contract-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_occurrences=5\nquarantined_occurrences=1\nsuperseded_occurrences=1\nunmatched_refund_orders=1\ncustomers=((\u0027c1\u0027, 2, 1700, 300, 1400), (\u0027c2\u0027, 1, 800, 100, 700))\ngross_cents=2500\nrefund_cents=400\nnet_cents=2100\ninput_order_stable=True\nsources_unchanged=True\n","stderr":""}} -->
```python
from collections import defaultdict
import random

ORDERS = (
    ("x1", "o1", "c1", 1, "accepted", "1000", "2026-08-01T00:00:01Z"),
    ("x2", "o1", "c1", 2, "accepted", "1200", "2026-08-01T00:00:02Z"),
    ("x3", "o2", "c1", 1, "rejected", "700", "2026-08-01T00:00:03Z"),
    ("x4", "o3", "c1", 1, "accepted", "500", "2026-08-01T00:00:04Z"),
    ("x5", "o4", "c2", 1, "accepted", "800", "2026-08-01T00:00:05Z"),
    ("x6", "o5", "c3", 1, "accepted", "bad", "2026-08-01T00:00:06Z"),
)
REFUNDS = (
    ("r1", "o1", 200),
    ("r2", "o1", 100),
    ("r3", "o2", 50),
    ("r4", "o4", 100),
)

def transform(order_seed, refund_seed):
    order_snapshot = ORDERS
    refund_snapshot = REFUNDS
    source_orders = list(ORDERS)
    source_refunds = list(REFUNDS)
    random.Random(order_seed).shuffle(source_orders)
    random.Random(refund_seed).shuffle(source_refunds)

    valid = []
    quarantine = []
    for row in source_orders:
        if row[5].isdecimal():
            valid.append((*row[:5], int(row[5]), row[6]))
        else:
            quarantine.append((row[0], "amount_text", "invalid_integer"))

    winners = {}
    for row in valid:
        key = row[1]
        authority = (row[3], row[6], row[0])
        if key not in winners or authority > winners[key][0]:
            winners[key] = (authority, row)

    refunds_by_order = defaultdict(int)
    for _, order_id, cents in source_refunds:
        refunds_by_order[order_id] += cents

    summaries = defaultdict(lambda: [0, 0, 0, 0])
    matched_refund_orders = set()
    for _, row in winners.values():
        _, order_id, customer_id, _, status, gross, _ = row
        if status != "accepted":
            continue
        refunded = refunds_by_order[order_id]
        if order_id in refunds_by_order:
            matched_refund_orders.add(order_id)
        values = summaries[customer_id]
        values[0] += 1
        values[1] += gross
        values[2] += refunded
        values[3] += gross - refunded

    customers = tuple(
        (customer, *summaries[customer]) for customer in sorted(summaries)
    )
    unmatched = len(set(refunds_by_order) - matched_refund_orders)
    return {
        "valid": len(valid),
        "quarantined": len(quarantine),
        "superseded": len(valid) - len(winners),
        "unmatched": unmatched,
        "customers": customers,
        "sources_unchanged": ORDERS == order_snapshot and REFUNDS == refund_snapshot,
    }

first = transform(7, 107)
second = transform(91, 191)
print(f"valid_occurrences={first['valid']}")
print(f"quarantined_occurrences={first['quarantined']}")
print(f"superseded_occurrences={first['superseded']}")
print(f"unmatched_refund_orders={first['unmatched']}")
print(f"customers={first['customers']}")
print(f"gross_cents={sum(row[2] for row in first['customers'])}")
print(f"refund_cents={sum(row[3] for row in first['customers'])}")
print(f"net_cents={sum(row[4] for row in first['customers'])}")
print(f"input_order_stable={first == second}")
print(f"sources_unchanged={first['sources_unchanged']}")
```

The single unmatched refund order is `o2`: its current order state is rejected, so its refund does not enrich accepted orders. That count is evidence, not necessarily an error; the domain must decide whether refunds for rejected orders are valid, late, or quarantined.

The following pandas-shaped implementation is schematic. It shows explicit schema checks, null-key rejection, stable winner order, cardinality validation, and new-frame assignment, but exact calls and dtypes must be reviewed against the pinned pandas version and production backend. Its result must be compared with the executable oracle above.

<!-- bijux-verify: {"id":"pandas-dataframe-shape","mode":"schematic","language":"python","toolchain":"none","reason":"The repository verifier intentionally does not install or execute optional pandas and Arrow dependencies; production evidence must run this pattern against pinned library versions and the actual input/output backends."} -->
```python
required = {
    "record_id", "order_id", "customer_id", "source_version",
    "status", "gross_cents", "ingested_at",
}
assert set(orders.columns) == required
assert orders["order_id"].notna().all()

current = (
    orders.sort_values(
        ["order_id", "source_version", "ingested_at", "record_id"],
        kind="stable",
    )
    .drop_duplicates("order_id", keep="last")
    .loc[lambda frame: frame["status"].eq("accepted")]
)
refunds_by_order = (
    refunds.groupby("order_id", as_index=False, dropna=False)
    .agg(refund_cents=("refund_cents", "sum"))
)
order_net = current.merge(
    refunds_by_order,
    on="order_id",
    how="left",
    validate="one_to_one",
    indicator=True,
)
order_net = order_net.assign(
    refund_cents=lambda frame: frame["refund_cents"].fillna(0),
    net_cents=lambda frame: frame["gross_cents"] - frame["refund_cents"],
)
```

Even this concise pattern needs surrounding evidence: explicit reader casts and reject capture; authority of the winner tuple; refund identity uniqueness; meaning of rejected-order refunds; integer/decimal overflow and null rules; exact pandas version/Copy-on-Write behavior; peak memory; serialization; candidate completeness; and publication.

## Alternatives and Trade-Offs

**Notebook versus module.** A notebook accelerates exploration and visual inspection but permits hidden state and out-of-order execution. A module with pure functions, explicit inputs, tests, and a command/job entry point supports reproducibility. Keep notebooks as consumers of versioned functions and immutable samples where possible.

**Eager versus lazy.** Eager operations provide immediate feedback and easy intermediate inspection. Lazy plans can prune, push down, fuse, stream, and optimize globally, but errors appear at execution and plans can change with versions/statistics. Capture explain plans and terminal receipts.

**Mutable versus functional style.** In-place mutation can reduce explicit names and sometimes memory, while making aliasing, retries, tests, and lineage harder. Returning owned frames makes boundaries clear but can allocate. Copy-on-Write changes the cost/behavior again. Favor clarity and measure the pinned runtime.

**Index keys versus explicit columns.** Indexes can accelerate alignment and express labeled operations in some libraries. Explicit columns travel across file formats, distributed engines, SQL, and Arrow more predictably. Use an index as an implementation detail derived from validated columns unless it is part of a durable interface.

**Native expressions versus UDFs.** Expressions are optimizable, vectorizable, typed, and portable within the engine. UDFs provide arbitrary algorithms at serialization, opacity, resource, and portability cost. Isolate and batch unavoidable UDFs.

**Local versus distributed frames.** Local execution has low coordination overhead and simple debugging. Distributed execution expands capacity but adds partitions, shuffles, skew, retries, and nondeterminism. Decide from peak working set and measured operation shape, not raw file size.

**Dataframe versus SQL.** Dataframes integrate naturally with application code and specialized libraries; SQL exploits database locality, governance, and optimizers. Both need the same grain, type, join, test, and publication contracts. Differential tests can protect a migration or hybrid boundary.

**Wide chained expression versus named stages.** Fluent chains show dataflow concisely. Named functions/stages expose grain and checks. Break at risk-bearing semantic boundaries, not every method call; preserve enough plan visibility for optimization.

**Arrow interchange versus native conversion.** Arrow can reduce serialization and enable shared columnar representations, but type compatibility and zero-copy conditions are limited. Native conversions may be simpler and safer for edge types. Measure correctness and peak memory.

**Collect versus streaming/sink.** Collecting provides a complete local object and supports arbitrary operations, but can exhaust one process. Streaming/lazy sinks bound memory for supported operators, while global sort, window, join, or UDF stages may block. Inspect actual plans and fallback.

**Fail-fast versus quarantine.** Fail-fast protects strict outputs and simplifies reasoning; quarantine preserves valid progress and evidence for record-level defects. Schema-wide ambiguity, corrupt source boundaries, or violated authority usually warrants blocking. Declare thresholds and publication consequences.

**Exact versus tolerance-based comparison.** Keys, integer counts, decimals, and categorical outputs often require exact equality. Floating reductions or approximate algorithms may require justified tolerances plus bounds and stable reference state. Never use tolerance to hide population or unit errors.

## Failure Modes and Misconceptions

- **“A dataframe is just a table.”** Index, order, missingness, mutation, execution, and distribution semantics differ across libraries and SQL systems.
- **“The index is the key.”** An index may be generated, duplicated, reset, omitted on write, or repartitioned. Validate domain identity explicitly.
- **“Row order is preserved.”** Scans, joins, groups, partitions, and optimizers can reorder occurrences. Use a declared total order where meaning depends on it.
- **“Inference found the schema.”** It found a representation for sampled/current values. Production schema needs an explicit contract and evolution policy.
- **“Null is one value.”** NaN, NaT, nullable NA, Arrow null, SQL null, absent row, and domain unknown have different behavior and meaning.
- **“Dataframe joins behave like SQL.”** Matching and ordering are library/version specific; pandas currently matches null keys to one another.
- **“Many-to-many is acceptable because the API allows it.”** It may be correct, but measures and output grain need explicit multiplicity semantics.
- **“Drop duplicates keeps the latest.”** Only an authoritative total order can define latest; physical `last` is accidental.
- **“Fill missing with zero.”** Zero is observed absence of quantity; missing can mean unknown, invalid, redacted, or unmatched.
- **“Chained assignment updates the intended frame.”** View/copy/Copy-on-Write rules vary. Use clear owned transformations and pin versions.
- **“Method chaining is vectorized.”** A chain can still contain row-wise UDFs, Python callbacks, or repeated materializations.
- **“Lazy means streaming.”** A lazy plan defers work; some operators or engine paths still materialize large state.
- **“Distributed means it scales.”** Shuffle, skew, serialization, driver collection, and scheduler overhead can dominate or fail.
- **“Arrow means zero-copy.”** Zero-copy requires compatible types/layout/chunks/nulls/ownership; conversions can duplicate memory.
- **“The file is 4 GB, so 8 GB RAM is enough.”** Decoding, objects, intermediates, joins, sorts, conversion, and allocator overhead determine peak memory.
- **“Garbage collection frees memory immediately.”** references, caches, allocators, native buffers, and fragmentation can retain memory.
- **“A source frame was not mutated.”** Aliases, extension buffers, UDF side effects, or older library behavior may contradict intent; test it.
- **“The local sample passed.”** It may omit null keys, hot groups, large strings, type extremes, cross-partition cases, and memory peaks.
- **“Equal totals prove parity.”** Missing and duplicated rows can offset. Compare identities, multiplicities, components, schema, and slices.
- **“Collect succeeded, so output is published.”** Collection is computation; trusted visibility requires complete candidate validation and atomic/conditional commit.
- **“Retry is harmless.”** A previous write may have completed after timeout. Resolve candidate/job/publication identity first.
- **“Caching makes a frame authoritative.”** A cache lacks source manifest, contract, completeness, retention, and publication semantics unless designed otherwise.
- **“Upgrading only changes performance.”** Nullable types, string defaults, copy behavior, joins, grouping, writers, and plans can change results.
- **“A UDF can call an API per row.”** This creates unbounded latency, side effects, partial failure, nondeterminism, and rate-limit coupling.

## Worked Examples

### Example 1

A CSV reader infers integer `customer_id` from the first file and string from a later file containing leading zeros. Concatenation coerces values and `0012` may become indistinguishable from `12`. The repair defines customer ID as string, preserves raw text, validates format without numeric conversion, quarantines invalid values, and tests leading zeros across every input shard.

### Example 2

A developer filters a frame and assigns to the resulting slice, expecting the parent to change. Under one pandas version the code warns or mutates through a view; under pandas 3.0 Copy-on-Write the derived object cannot update the parent through the historical chained pattern. The pipeline replaces it with one explicit `.loc`/assignment boundary or a returned owned frame, pins the version, and tests source nonmutation and output values.

### Example 3

Left and right frames each contain two missing join keys. A pandas merge can produce four missing-to-missing pairs, while a SQL equality join usually produces none. The contract says missing entity IDs cannot match, so the pipeline quarantines missing keys before both implementations, validates many-to-one cardinality on nonmissing keys, and compares unmatched counts.

### Example 4

An order frame contains two versions and a refund frame contains three events for that order. Joining first creates six pairs and corrupts both gross and refund sums. The safe path resolves one authoritative order version, validates it unique, aggregates three refunds to one order row, validates that key, then enriches. Its output is one row at order grain.

### Example 5

A group-by result unexpectedly omits records whose region is missing. The library’s default excluded null group keys. The team decides unknown region belongs in an explicit governed member, records the mapping reason, configures/normalizes the grouping behavior, and reconciles total input measure to grouped components rather than accepting a smaller grand total.

### Example 6

A row-wise UDF parses timestamps and consults current local time. It is slow, opaque to predicate pushdown, and changes on replay. The replacement uses native timezone-aware parsing with an explicit source zone, passed evaluation time, structured invalid policy, and vectorized expressions. A small independently calculated fixture covers DST gap/fold and precision boundaries.

### Example 7

A Polars lazy scan selects three columns and filters one status before aggregation. `explain` shows projection and predicate pushdown, cutting scan work. The team still validates that rejected records needed for quarantine were not pruned, stores the optimized plan with version/configuration, and measures terminal collection/write rather than timing only plan construction.

### Example 8

An Arrow table with nullable, multi-chunk integer columns converts to pandas. The operator expects zero-copy, but documented zero-copy preconditions are not met and peak resident memory nearly doubles. The capacity model includes both representations, the pipeline rechunks or changes the boundary only after semantic/ownership tests, and a memory gate measures the exact conversion.

### Example 9

A distributed dataframe job groups by `tenant_id`; one tenant owns 70% of rows. Average partition size looks safe, but one hot reduce task spills and times out repeatedly. The team measures key distribution, separates/salts the hot path under a correct recombination proof, sets per-stage spill/memory thresholds, and ensures retries write isolated candidates.

### Example 10

A pandas-to-Spark migration matches row count and revenue total but differs on nullable join keys, timestamp precision, categorical output, and floating reduction order. The acceptance suite compares canonical key multisets, null reasons, types, component sums, boundary times, exact integer/decimal measures, justified floating tolerances, rejects, and output manifests. Only then does it compare performance and publish the new generation.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies bags, null logic, joins, aggregation, types, plans, transactions, and storage. Dataframe APIs can resemble SQL while differing in index, missing-key, ordering, and mutation behavior.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects columnar buffers, validity bitmaps, offsets, dictionaries, hashing, sorting, indexing, memory locality, and ownership. Peak memory and interchange behavior follow concrete representation choices.

[Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) connects eager/lazy evaluation, expression trees, effects, aliasing, type systems, and foreign-function boundaries. A lazy dataframe plan is a program requiring semantic preservation.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects pure functions, dependency injection, modular boundaries, versioned interfaces, immutable artifacts, and change control. Notebook code becomes operable when those properties are explicit.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects independent oracles, property/metamorphic tests, mutation tests, differential testing, performance envelopes, and evidence limits.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects partitions, shuffles, skew, retries, ambiguous writes, conditional publication, and lineage across schedulers, workers, storage, and catalogs.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects pinned runtimes, managed environments, resource quotas, artifact stores, observability, secrets, policy, and self-service safe defaults for dataframe jobs.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements, interfaces, hazards, verification evidence, capacity, configuration control, incident learning, and recovery drills. Memory and semantic failure modes belong in one system model.

## References

1. pandas project, [`DataFrame.merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html). Documents join modes, index/column keys, ordering, suffixes, cardinality validation, and the current warning that null keys match one another. Accessed 2026-09-02.
2. pandas project, [Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html). Documents dtype-dependent missing sentinels, nullable values, propagation, detection, filling, and grouping/operation behavior. Accessed 2026-09-02.
3. pandas project, [Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html). Documents pandas 3.0 Copy-on-Write defaults, ownership behavior, chained-assignment changes, and migration implications. Accessed 2026-09-02.
4. Polars project, [Lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/). Documents eager/lazy execution, terminal collection, explain plans, and projection/predicate pushdown examples. Accessed 2026-09-02.
5. Apache Spark, [Spark SQL and DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html). Defines Spark DataFrames as distributed data organized into named columns and relates them to the optimized SQL engine and Dataset API. Accessed 2026-09-02.
6. Apache Arrow, [Columnar format](https://arrow.apache.org/docs/format/Columnar.html). Specifies columnar layouts, validity representation, buffers, nesting, dictionaries, alignment, and possible zero-copy shared-memory access. Accessed 2026-09-02.
7. Apache Arrow, [pandas integration](https://arrow.apache.org/docs/python/pandas.html). Documents dataframe/index conversion, type mapping, null handling, memory usage, and limited zero-copy conditions. Accessed 2026-09-02.
8. Dask project, [Dask DataFrame](https://docs.dask.org/en/stable/dataframe.html). Documents lazy parallel dataframe collections, `compute`/`persist`, familiar pandas-like operations, and limitations/selection guidance. Accessed 2026-09-02.
9. pandas project, [Scaling to large datasets](https://pandas.pydata.org/docs/user_guide/scale.html). Documents load-less-data, efficient dtypes, chunking, and delegation to other libraries as scaling approaches. Accessed 2026-09-02.

## Exercises

### Exercise 1

A pandas 3.0 left frame contains keys `(1, null, null)` and amounts `(10, 20, 30)`. A right frame contains keys `(1, null, null)` and labels `("A", "U1", "U2")`. Under the documented pandas null-key merge behavior, compute the inner-join row count and sum of repeated left amounts. Compare with ordinary SQL `=` null behavior, then design a safe contract for missing entity identifiers.

### Exercise 2

A 6 GiB decoded input frame, 2 GiB join build table, 5 GiB candidate output, 4 GiB transient hash/shuffle state, and 7 GiB Arrow-to-dataframe conversion coexist at the observed peak; runtime/allocator headroom policy is 25% of live buffers. Compute the minimum envelope implied by this observation. Explain why a 12 GiB worker chosen from file/output size is unsafe and what evidence should replace the guess.

### Exercise 3

An order has occurrences `(version=4,status=accepted,gross=100)` and `(version=5,status=deleted,gross=100)`. A pipeline filters to accepted rows and then keeps maximum version. Another resolves maximum version first and then filters deleted state. Compute each result and explain the noncommutativity. State the evidence that must be retained.

### Exercise 4

A lazy dataframe job appears to finish instantly when its transformation function returns a plan. At `collect`, a row-wise API-calling UDF takes two hours, partially writes files, and is retried. Redesign the expression/UDF boundary, terminal execution, resource gate, candidate write, retry, and publication protocol.

### Exercise 5

A team is migrating a local pandas transformation to distributed Spark. It compares only final row count and floating revenue total and finds them equal. Design a differential validation matrix covering identity, schema/missingness, joins, ordering/windows, aggregation, time, resource behavior, security, and publication. State which evidence can be exact and which may need tolerance or an operating envelope.

## Answers to the Exercises

### Answer 1

Key `1` produces one pair. The two missing left keys each match the two missing right keys under documented pandas behavior, producing four more pairs, for five rows total. Left amount 10 appears once; amounts 20 and 30 each appear twice. Their joined sum is $10+2(20)+2(30)=110$.

Under ordinary SQL equality, null does not equal null, so only key `1` matches: one row and sum 10. A safe entity-key contract declares identifiers nonmissing before the join, quarantines or separately carries missing-key occurrences, validates expected cardinality on nonmissing keys, records unmatched/missing counts, and tests the pinned library. If the domain intentionally matches missing values, it must define the resulting multiplicity and stable synthetic equivalence explicitly.

### Answer 2

Live buffers total $6+2+5+4+7=24$ GiB. Applying 25% headroom gives at least $24\times1.25=30$ GiB. That is only the stated observed/estimated envelope; process/runtime baselines and concurrent workload may require more.

A 12 GiB worker cannot hold even the 24 GiB simultaneous set. Source file size can differ from decoded size, and output size omits join, shuffle, conversion, copies, indexes, allocator fragmentation, and skew. Replace the guess with per-stage live-buffer accounting plus measured resident/engine memory, spill, null/string/cardinality/skew cases, concurrency and retry headroom on representative scale. Then reduce live state or choose streaming/partitioned/distributed execution as semantics permit.

### Answer 3

Filtering accepted first removes version 5 and leaves version 4, so version resolution emits an apparently current accepted order of 100. Resolving first chooses version 5; applying the state policy then emits no active order. Thus $V(F(D))$ resurrects deleted state while $F(V(D))$ does not.

Retain both source occurrences, occurrence IDs, source epoch/version, status/tombstone, event/effective/ingestion times, raw values or governed references, source cut, resolution code/config, winner and loser classifications, and output receipt through the replay/audit horizon. Assert exactly one authoritative winner or an explicit conflict.

### Answer 4

Returning a plan is not completion. Replace the per-row API call with a bounded upstream enrichment dataset: fetch through a separately retryable/idempotent service stage, snapshot/version/cache results under access and freshness rules, then join through native dataframe expressions with cardinality validation. If a UDF remains, batch it, make inputs/outputs typed and deterministic, prohibit side effects, bound concurrency/time/retries, and expose metrics.

The job must execute a terminal sink under a persisted run/attempt identity, capture the optimized and physical plan, and enforce duration, memory, spill, network and external-quota gates. It writes only an isolated candidate manifest; partial files are not trusted. On timeout, look up terminal job and candidate state before retrying. Validate completeness, schema, keys, reconciliations and security, then conditionally/atomically publish with an expected-prior check and receipt. Cleanup retains active/published/rollback generations.

### Answer 5

Compare exact input cuts and canonical business-key multisets; per-key multiplicities; winner identities; rejects; column names/order where contractual; logical types, widths/signedness, decimal scale, timestamp precision/zone, categorical/nested metadata; null versus NaN and missing-key join outcomes; left/right/matched and fanout distributions; explicit total orders, tie winners and window frames; integer/decimal component sums, group keys, empty/all-null groups and both set differences; time boundaries/DST; tenant and sensitive-field propagation; and output file/partition manifests plus publication receipts.

Exact evidence is appropriate for identities, counts, integer/decimal controls, schemas, domain codes, rejects, key sets, and deterministic categorical outputs. Floating reductions or approved approximate algorithms may use justified absolute/relative/error-bound tolerances, with exact population and components still required. Resource evidence uses an operating envelope for peak memory, spill, shuffle, skew, duration, retries and cost under representative concurrency. Security gates and atomic/conditional publication are pass/fail requirements, not offset by matching totals or faster runtime.
