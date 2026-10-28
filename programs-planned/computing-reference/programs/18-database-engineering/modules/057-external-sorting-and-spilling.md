---
module_id: DBE-057
program: Database Engineering
level: 2
module_number: 57
title: External Sorting and Spilling
status: complete
last_verified: 2026-08-30
---

# External Sorting and Spilling

## One-Page Review

### Governing question

How can a database execution engine impose a correct total order when the input and intermediate state exceed memory, while bounding resources, preserving every row occurrence, surviving failures, and exposing enough evidence to diagnose the resulting I/O?

### Essential definitions

An **external sort** orders data using bounded internal memory and secondary storage. A **run** is a sequence already sorted by the complete comparator. **Run generation** fills a memory budget, sorts a batch, and writes a run. A **k-way merge** keeps a buffered frontier from up to k runs and repeatedly emits the least next record. **Fan-in** is the number of runs merged at once. A **merge pass** reads one generation of runs and writes the next. **Spill** materializes operator state or records outside its preferred memory tier. A **memory grant** is a bounded allocation policy, not a correctness assumption. A **blocking operator** normally consumes all relevant input before ordinary output. A **top-N sort** retains only candidates needed for a limit when the semantics permit it.

### Central model, mechanism, or theorem

Let N records occupy n = ceiling(N/B) blocks, memory hold M records or m = floor(M/B) blocks, and k input buffers participate in a merge. Generate R approximately ceiling(N/M) sorted runs, then reduce them through ceiling(log base k of R) merge passes. Each completed full-data pass reads and writes the represented data. In the standard comparison-based external-memory model, sorting has transfer complexity Theta((N/B) log base (M/B) (N/B)) in the usual regime; multiway merge sort attains the bound up to constants. Correctness is separate: run generation must preserve the input bag, each run must be ordered, and every merge must preserve the union bag while producing an ordered output.

### Critical invariants

- The comparator is total for physical execution: keys, direction, NULL placement, collation, coercion, and any deterministic tie policy are fixed.
- Every input row occurrence belongs to exactly one live run or output position; none is lost, duplicated, or applied twice.
- Each sealed run is monotone under the same comparator and carries trustworthy length, format, and ownership metadata.
- A merge frontier contains at most one current candidate per nonempty input run; emitting one advances only its owner.
- Memory accounting includes tuples, keys, pointer arrays, heap/loser-tree state, per-run buffers, decompression, and allocator overhead.
- Temporary storage respects quota, integrity, isolation, cancellation, and cleanup policy.
- A spill changes physical placement, never SQL order, multiplicity, snapshot, or visibility semantics.
- Output order is claimed only for the full required key; stability is not a substitute for an explicit tie-breaker.

### Common failures

Failures include comparing runs under different collations; sorting a key prefix but claiming total order; treating equal-key arrival order as guaranteed; losing a row at buffer boundaries; reopening or deleting a run too early; selecting excessive fan-in and starving buffers; assuming one pass from nominal memory; counting payload but not overhead; allowing several concurrent operators to multiply a per-node budget; exhausting temporary space; leaking sensitive spill files; confusing OS swap with deliberate spill; trusting a sorted flag without monotonicity and permutation evidence; and tuning memory globally from one isolated query.

### Compact example

Eleven integer records with a three-record memory capacity create four initial runs. With merge fan-in two, the first pass produces two runs and the second produces one. Initial run writes account for 11 record occurrences; the two merge passes each read and write 11, for 55 modeled spill-I/O record occurrences. The executable checks monotonicity and bag equality, including a duplicate 3. This finite record-count model does not predict byte-level I/O, engine memory overhead, filesystem behavior, or arbitrary SQL comparison.

### Connections

Retrieve [Logical and Physical Plans](051-logical-and-physical-plans.md), [Single-Node Sort-Merge Joins](055-single-node-sort-merge-joins.md), and [Hash and Sort Aggregation](056-hash-and-sort-aggregation.md). Continue to iterator execution, vectorized pipelines, optimizer cost models, and parallel query through the Database Engineering [roadmap](../ROADMAP.md).

## Governing Question

What ordering, ownership, resource, and lifecycle arguments make a bounded-memory external sort observationally equivalent to an ideal in-memory sort, and what evidence distinguishes a healthy spill from a correctness or capacity failure?

## Why This Matters

Sorting supports `ORDER BY`, merge join, duplicate elimination, grouping, window functions, index construction, clustering, and ordered exchange. The relational result is a bag unless an order is explicitly required, but physical operators often require or benefit from ordered input. For a large relation, materializing all sortable rows in RAM is unsafe. Refusing every larger-than-memory query is also unacceptable. External sorting makes the operator scale by converting an unbounded-memory demand into bounded memory plus controlled sequential I/O.

That conversion is not free or automatic. A query can contain several sorts, hashes, windows, and workers, each with its own allowance. Increasing a nominal per-operation limit may multiply across nodes and sessions. Temporary files share finite capacity and I/O bandwidth with other work. A sort that spills one byte is not necessarily unhealthy, while a nonspilling sort can still destabilize a host through concurrency. Production engineering therefore reasons about grants, admission, actual peak memory, run counts, pass counts, temporary bytes, device latency, cleanup, and workload concurrency together.

Correctness is more subtle than “call merge sort.” SQL ordering may combine ascending and descending components, explicit or default NULL placement, locale-sensitive text comparison, numeric coercion, timestamps, and expressions. Equal requested keys do not define a unique row order. If pagination, replication, tests, or materialization require repeatability, a unique stable key must be part of the semantic order. An implementation described as stable only preserves a particular input sequence; parallel scans, exchanges, and prior operators may not preserve that sequence.

Spilling is a general execution pattern. Hash joins partition overflowing state; hash aggregates batch groups; window operators materialize partitions; exchanges buffer; and recursive algorithms checkpoint frontiers. External sorting provides a disciplined case study in making placement adaptive while holding logical semantics invariant. It also demonstrates why temporary state needs real storage-engine qualities: format versioning, checks, ownership, quotas, encryption policy, cancellation, and crash cleanup.

## Prerequisites and Retrieval

You should understand bags and row occurrences; comparison sorting; priority queues; pages and block I/O; SQL `ORDER BY`, NULL, and collation semantics; physical plans; merge joins and sort aggregation; iterators; memory allocation; temporary storage; concurrency; and fault handling.

Retrieve these terms before continuing: sort key, total preorder, total tie order, comparator compatibility, stability, run, run generation, replacement selection, k-way merge, fan-in, merge pass, input/output buffer, priority queue, loser tree, memory grant, blocking operator, spill threshold, temporary file, top-N heap, incremental sort, materialization, rewind, random access, and external-memory I/O model.

DBE-055 used sorted inputs for merge join, and DBE-056 contrasted hash aggregation with ordered streaming. This chapter supplies the generic bounded-memory sorting substrate. DBE-058 will place the blocking sort behind an iterator interface; DBE-059 will examine batches and pipeline breakers; DBE-060 will profile the complete operator pipeline.

## Learning Objectives

After this module, you can:

1. specify a complete physical comparator for SQL rows, including NULL, collation, direction, and tie requirements;
2. derive initial run count, feasible merge fan-in, pass count, and idealized transfer volume from explicit assumptions;
3. prove run generation and k-way merge preserve order and bag identity;
4. implement and test a bounded external-merge model with duplicates and multiple passes;
5. distinguish full sort, top-N, incremental sort, index order, distribution, and hash alternatives;
6. account for memory beyond payload and for concurrency beyond one plan node;
7. design spill manifests, integrity checks, cancellation, failure cleanup, and restart policy;
8. interpret sort method, memory, disk, run/pass, and temporary-I/O evidence without overclaiming;
9. diagnose skewed widths, bad cardinality estimates, slow temporary storage, and quota exhaustion; and
10. construct correctness, performance, resource-isolation, and fault-injection gates for a production sorter.

## Core Exposition

**Freeze semantics before choosing an algorithm.** A logical ordering is an ordered list of expressions, directions, NULL placement rules, collations or operator classes, and type/coercion decisions. The engine comparator must implement that definition consistently in memory, in run files, during merge, and after serialization. If only `(event_time DESC)` is requested, rows sharing a timestamp may appear in any relative order permitted by the database. Add a unique key such as `event_id DESC` when a deterministic total row order is required. Stability without an explicit source-order contract does not create SQL semantics.

**Separate the abstract record from its representation.** A sort record may carry the full row, key plus row locator, abbreviated key plus original datum, or encoded vector references. The choice changes width, comparison cost, later random fetches, and spill format. Abbreviated keys may reject most comparisons cheaply, but equality or ambiguity must fall back to the authoritative comparator. Variable-width values, collation keys, null bitmaps, alignment, pointer arrays, allocator fragmentation, metadata, and buffers all consume memory. Therefore `records × declared row width` is not a safe grant calculation.

**Run generation bounds the working set.** Read records until the owned memory budget would be exceeded, sort that batch internally, verify or assume-by-construction monotonicity, and write a sealed run. A run header or manifest should bind comparator/format version, query or operator ownership, sequence, count, byte length, minimum/maximum key where safe, and integrity evidence. The final partial batch is a legal run. If all input fits, an engine can remain in memory and emit directly.

Replacement selection historically used a heap to produce runs whose expected length can exceed memory for favorably random inputs: after emitting the minimum, an arriving record stays in the current run only if it does not precede the last output; otherwise it is frozen for the next run. Its run length is data-dependent and its implementation is more complex. Modern engines may prefer batch quicksort plus balanced merging because CPU/cache behavior, cheap logical tapes, parallel run generation, and predictable ownership matter more than minimizing tape-drive changes. Algorithm history is not a mandate for current hardware.

**Multiway merge reduces runs.** Give each input run a nontrivial read buffer, give the output a write buffer, place one current record per nonempty input into a priority queue or loser tree, and repeatedly emit the least. Refill the owner buffer and update only that frontier entry. The comparator must break internal ties sufficiently to produce a legal sequence, but need not invent a user-visible order not demanded by SQL.

Fan-in k is constrained by memory for k input buffers, output buffering, frontier state, file/tape metadata, decompression, and safety reserve; it may also be constrained by file descriptors and asynchronous I/O policy. Larger k can reduce merge passes but makes each buffer smaller, potentially harming sequentiality and request efficiency. Smaller k improves per-run buffering but may add a complete read/write pass. An optimal value is a system decision based on memory, storage, record encoding, run count, and concurrency—not simply the largest file-descriptor limit.

**Model transfers, then measure reality.** Suppose N records occupy n blocks and memory provides m blocks, with m at least two. About `R = ceiling(n/m)` initial runs arise under fixed-size batch generation. A merge can use roughly `k ≤ m - 1` buffered input streams when one block is reserved for output, though practical engines reserve additional space. The number of merge passes is `p = ceiling(log_k R)` when balanced groups reduce by at most k each pass. Run generation writes about n blocks; materialized merge passes each read and write about n blocks. If the original input scan and final consumer read are counted, totals change, so every formula must name its boundary.

Aggarwal and Vitter's external-memory model counts block transfers rather than treating CPU operations as the only scarce resource. In the conventional single-disk comparison regime, external sorting requires and can achieve `Theta(n log_m n)` block transfers up to standard parameterization and constants. This asymptotic result explains multiway merging; it does not predict elapsed time on SSDs, object stores, compressed data, parallel devices, caches, or a contended database host.

**The finite executable exposes the invariants.** It chunks eleven integer occurrences into three-record batches, sorts each batch, and performs balanced two-way merge passes. `heapq.merge` is used only after every input run is asserted monotone. A `Counter` checks bag identity so the duplicate value 3 cannot be silently collapsed or replicated. Modeled I/O counts record occurrences at algorithm boundaries; they are not physical block requests or bytes.

<!-- bijux-verify: {"id":"bounded-external-merge-sort","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=(9, 1, 5, 3, 7, 3, 2, 8, 6, 4, 0)\nmemory_records=3\nfan_in=2\ninitial_runs=((1, 5, 9), (3, 3, 7), (2, 6, 8), (0, 4))\nmerge_pass_1=((1, 3, 3, 5, 7, 9), (0, 2, 4, 6, 8))\nmerge_pass_2=((0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9),)\nmerge_passes=2\nsorted_output=(0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9)\nsorted=True\npermutation=True\nmodeled_spill_io_occurrences=55\nevidence=finite_external_merge_invariants\n","stderr":""}} -->
```python
from collections import Counter
from heapq import merge


def monotone(run):
    return all(left <= right for left, right in zip(run, run[1:]))


def external_merge_sort(values, memory_records, fan_in):
    if memory_records < 1 or fan_in < 2:
        raise ValueError("memory_records >= 1 and fan_in >= 2 are required")
    runs = [
        tuple(sorted(values[index:index + memory_records]))
        for index in range(0, len(values), memory_records)
    ]
    initial = tuple(runs)
    history = []
    io_occurrences = len(values)  # initial run writes
    while len(runs) > 1:
        next_runs = []
        for index in range(0, len(runs), fan_in):
            group = runs[index:index + fan_in]
            assert all(monotone(run) for run in group)
            output = tuple(merge(*group))
            assert monotone(output)
            assert Counter(output) == sum((Counter(run) for run in group), Counter())
            next_runs.append(output)
            io_occurrences += 2 * len(output)  # modeled read plus write
        runs = next_runs
        history.append(tuple(runs))
    output = runs[0] if runs else ()
    return initial, tuple(history), output, io_occurrences


values = (9, 1, 5, 3, 7, 3, 2, 8, 6, 4, 0)
initial, history, output, io_occurrences = external_merge_sort(values, 3, 2)
print(f"input={values}")
print("memory_records=3")
print("fan_in=2")
print(f"initial_runs={initial}")
for number, runs in enumerate(history, start=1):
    print(f"merge_pass_{number}={runs}")
print(f"merge_passes={len(history)}")
print(f"sorted_output={output}")
print(f"sorted={monotone(output)}")
print(f"permutation={Counter(output) == Counter(values)}")
print(f"modeled_spill_io_occurrences={io_occurrences}")
print("evidence=finite_external_merge_invariants")
```

**Spill is a lifecycle, not a write call.** Reserve or check temporary capacity before committing work that cannot finish without it. Create files under operator/query ownership with restrictive permissions and the deployment's encryption policy. Write framed records and metadata so truncation, corruption, incompatible versions, and wrong ownership are detected. Do not publish a run until its contents and metadata are complete. Cancellation and failure must stop producers, close readers, release buffers, and remove all unneeded files. Process death needs startup or background orphan reclamation tied to trustworthy liveness/generation information.

Whether a run must survive process failure depends on the recovery contract. Ordinary query scratch is usually disposable: abort the query and remove it. A resumable index build or data pipeline may persist runs, but then manifests, checksums, source snapshots, software compatibility, and idempotent restart become durable protocol state. Accidentally relying on disposable scratch for recovery creates silent gaps; retaining every failed query's scratch creates capacity and privacy hazards.

**Pipeline behavior matters.** A conventional full sort is blocking: it consumes its child before returning the least record. It has high startup cost even when the final output is streamed. A final merge can sometimes be performed on demand rather than materialized, reducing a write/read cycle when the consumer needs only forward access. Rewind, mark/restore, backward scan, parallel sharing, or random access may require materialization. The operator contract therefore changes physical storage choices.

**Parallelism creates runs and contention.** Workers can generate sorted runs independently; a leader or merge tree combines them. This increases CPU and scan bandwidth but adds per-worker memory, buffers, temporary writers, and final fan-in. Range partitioning can concatenate correctly ordered partitions only when boundaries, comparator semantics, and skew are controlled. Otherwise local sorts do not imply global order. A parallel merge must preserve every worker occurrence and propagate cancellation/errors across the tree.

**Observe decisions and consequences.** Capture required and presorted keys, estimated and actual rows/width, memory grant and peak, sort method, top-N/full/incremental choice, initial run count, merge fan-in/pass count if available, temporary bytes and read/write blocks, storage location, worker contribution, startup/total time, output rows, cancellation, disk-full events, and cleanup lag. PostgreSQL 18 documents per-operation `work_mem`, reports sort methods and disk use through execution plans, and implements large sorts with temporary files and balanced k-way merging. DuckDB's current documentation identifies sorting as a blocking operator with out-of-core support and also documents limitations when multiple blocking operators or nonspillable states interact. These are product observations, not universal guarantees.

**Test semantics independently of performance.** Generate duplicates, NULLs, variable-width values, collation-sensitive strings, ascending/descending mixtures, very small budgets, empty/singleton input, and enough runs for several merge passes. Compare the output bag and full comparator order against an independent oracle. Vary chunk boundaries and fan-in. Inject short writes, corrupted frames, disk-full, cancellation during every lifecycle state, worker loss, and restart. Assert no orphaned owned bytes after the cleanup horizon. Then benchmark warm/cold, compressed/uncompressed, narrow/wide, uniform/skewed, single/concurrent, and local/remote-temporary-storage scenarios without converting one machine's result into a theorem.

## Definitions and Notation

- **N**: number of input row occurrences; duplicates count separately.
- **B**: records per transfer block in a simplified fixed-width model.
- **n = ceiling(N/B)**: number of input blocks in that model.
- **M**: records available to the sort after all owned overhead; not host RAM.
- **m = floor(M/B)**: memory capacity in blocks.
- **R**: number of initial sorted runs.
- **k**: merge fan-in, the maximum input runs merged in one group.
- **p**: number of merge passes needed to reduce R runs to one.
- **Comparator**: procedure defining physical order over complete sort records.
- **Total preorder**: reflexive, transitive, total relation that may equate distinct records.
- **Tie-breaker**: additional key that refines equal requested keys when deterministic total order is required.
- **Stable sort**: sort preserving the input relative order of records that compare equal.
- **Run**: immutable or sealed comparator-monotone sequence participating in merge.
- **Spill**: movement of live operator data to a lower storage tier to remain within a resource bound.
- **Grant**: memory amount made available under a resource/admission policy.
- **Top-N**: bounded candidate selection for the first N records under an order, when full sorted output is unnecessary.
- **Incremental sort**: sorting within groups already ordered on a required key prefix.
- **Pass boundary**: the point at which every represented record has been read from one run generation and written to the next.
- **Bag equality**: equality of value multiplicities, stronger than set equality and independent of sequence.
- **Monotonicity**: for output sequence x1 through xN, `xi <= xi+1` under the comparator for every adjacent pair.

Unless explicitly stated, formulas assume fixed-width records, balanced merging, local block storage, full materialization of each intermediate pass, no compression, no overlap, and one operator. They are models, not latency guarantees.

## Mechanisms, Invariants, or Proof Structure

**Run-generation proof.** Partition the input occurrence sequence into disjoint batches. Internal sorting returns a permutation of each batch and orders it. Writing each result once yields runs that are individually monotone. Because batches partition the input, the bag union of all runs equals the input bag. Inductively maintain ownership: every accepted occurrence is in the current memory batch, exactly one sealed run, or a terminal failure path—not two.

**Merge proof.** Assume k input runs are monotone. The frontier contains the first unconsumed record of each nonempty run. Any unconsumed record behind a frontier record is greater than or equal to that frontier by run monotonicity. Therefore the minimum frontier record is a global minimum of all unconsumed records. Emit it and advance only its owning run; the invariant is restored. Induction gives monotone output. Each input cursor advances exactly once per occurrence, so the output bag equals the bag union of inputs.

**Multi-pass composition.** The first pass groups disjoint runs and replaces each group by its ordered bag-equivalent merge. Thus the next generation has the same total bag. Applying the merge argument at each generation preserves the original bag and produces monotone runs. When one run remains, it is ordered and bag-equal to input. This is a proof under reliable storage, a consistent comparator, and correct implementation—not proof that arbitrary run bytes satisfy those assumptions.

**Pass-count derivation.** One pass maps at most k input runs to one output per group, leaving at most `ceiling(R/k)` runs. After p passes, at most `ceiling(R/k^p)` remain. Requiring one yields `k^p >= R`, so `p >= ceiling(log_k R)`. Uneven final groups do not invalidate the bound. A final on-demand merge may avoid materializing the last output, changing I/O accounting but not logical pass depth.

**Resource invariant.** At every instant, charge every allocation and buffered byte to the operator or its shared owner. Enforce `charged <= grant + explicitly governed reserve`; do not omit allocator, comparator, decompression, or asynchronous-I/O buffers. A safe transition spills or rejects before an allocation violates the policy. The grant may adapt, but already accepted rows remain owned exactly once.

**Storage invariant.** A run becomes merge-visible only after its metadata and data are complete according to the chosen durability level. Readers validate owner, format, comparator identity, bounds where used, framing, and integrity. Intermediate input runs are deleted or recycled only after the consumer no longer needs them and failure semantics allow it. Cleanup is idempotent.

**Verification layers.** Structural checks confirm chapter and annotations. The executable checks one finite integer model. Independent recomputation checks run/pass counts and modeled I/O. Mathematical review checks the induction and assumptions. Source review checks current product claims. Engine experiments would measure actual plans and I/O but are not performed here. Production correctness still depends on the target engine, types, locale, storage, concurrency, and failures.

## Alternatives and Trade-Offs

**In-memory full sort** avoids spill I/O and is often simplest when the complete representation safely fits its grant. It remains blocking and can be unsafe under underestimated width or concurrency.

**External multiway merge sort** provides predictable bounded memory and mostly sequential transfer. It adds serialization, temporary capacity, merge CPU, startup latency, and failure lifecycle. Compression trades CPU for fewer bytes and can change optimal buffer sizes.

**Top-N heap or bounded selection** can use memory proportional to N rather than input size and avoid full output when `ORDER BY ... LIMIT N` semantics allow early candidate rejection. Large N, ties, offset, percent, or downstream need for complete order can erase the advantage. The optimizer must not use it when discarded rows are semantically required.

**Incremental sort** exploits an existing prefix order, sorting one prefix group at a time. It may return rows earlier and reduce memory/spill, especially with a limit. A huge prefix group still spills; wrong cardinality estimates can make the choice poor.

**Index-provided order** can avoid an explicit sort, especially for selective or early-stop queries. Scanning a large fraction through an index can cause expensive nonsequential base-row access; covering and clustering change the comparison. The index order must match expressions, direction, NULLs, collation, and snapshot semantics.

**Radix or distribution sorting** can reduce comparison work for suitable fixed encodings. It needs type-specific order-preserving representations, careful variable-width/locale handling, and partition-skew control. It does not remove external placement or bag-preservation obligations.

**Replacement selection** may generate longer runs than fixed batches under some distributions. It adds heap operations, frozen-state logic, data-dependent behavior, and less cache-friendly processing. Predictable batch sorting and balanced merging can be preferable on modern systems.

**Hashing instead of sorting** can implement equality joins, grouping, or duplicate elimination without global order. It cannot satisfy `ORDER BY` and may suffer recursive partition spill or skew. Hash and sort are alternative physical structures only when their logical outputs and downstream properties match.

**Remote or shared temporary storage** offers elasticity and worker accessibility but adds latency, request granularity, cost, credentials, rate limits, and partial-failure semantics. Local NVMe is fast but finite and host-scoped. Tiering requires explicit locality, encryption, cleanup, and retry policy.

## Failure Modes and Misconceptions

1. **“Equal sort keys imply deterministic order.”** They imply equivalence under the requested comparator. Add a unique tie-breaker for reproducibility.
2. **“Stable sort guarantees repeatability.”** Only relative to a stable, defined input order; parallel and relational inputs often lack one.
3. **“The input is sorted because metadata says so.”** Validate provenance and, at trust boundaries, monotonicity under the exact comparator.
4. **“A spill means memory is too low.”** A bounded, planned spill may protect workload stability; judge latency, bytes, passes, and concurrency.
5. **“No spill means memory is safe.”** Many nonspilling nodes and sessions can exceed host capacity.
6. **“Row width times row count is enough.”** Keys, pointers, encoding, buffers, allocator fragmentation, and variable states add material overhead.
7. **“Maximum fan-in minimizes time.”** It minimizes idealized passes only while buffers remain effective and other constraints hold.
8. **“Temporary files need no integrity or security.”** They can contain sensitive rows and can be truncated, confused, leaked, or exhausted.
9. **“OS swap is equivalent to operator spill.”** Swap is opaque page eviction; deliberate spill has record structure, ownership, and algorithmic access.
10. **“Sorting removes duplicates.”** Sorting preserves occurrences; duplicate elimination is a separate semantic operator.
11. **“Local worker order is global order.”** It is global only with ordered range boundaries or a correct merge/exchange.
12. **“Disk bytes in a plan equal total I/O.”** Cache, read/write direction, final materialization, compression, amplification, and concurrent traffic matter.
13. **“Disk-full can be retried blindly.”** Retry needs released capacity, idempotent ownership, and a defined source snapshot; otherwise it can loop or diverge.
14. **“Increasing the global memory knob fixes the query.”** It can multiply across operations and sessions; fix estimates, access paths, limits, concurrency, or per-workload policy with measurement.

## Worked Examples

### Example 1

**Situation:** 10,000 fixed-size blocks must be sorted with 100 usable memory blocks. Fixed-batch generation creates `R = ceiling(10000/100) = 100` runs. If practical buffering permits fan-in 9, `p = ceiling(log_9 100) = 3` because 9² is 81 and 9³ is 729. Materialized run generation writes 10,000 blocks; three merge passes each read and write 10,000, totaling 70,000 block transfers within this boundary. **Conclusion:** derive pass count from usable memory and fan-in, and state what input/final reads are excluded.

### Example 2

**Situation:** The query orders by `(score DESC)` and many rows have score 100. A stable sorter preserves whatever input order it received, but a parallel scan can interleave those rows differently on each run. Ordering by `(score DESC, submission_id ASC)` creates a unique tie order if `submission_id` is unique and immutable. **Conclusion:** determinism comes from the semantic key, not from an implementation's stability label.

### Example 3

**Situation:** Four initial runs contain the integer occurrences shown in the executable, including two 3s. A buggy verifier compares sets and would accept losing one 3 because both outputs have the same distinct values. Comparing `Counter` multiplicities rejects the loss. Adjacent monotonicity alone would not detect it. **Conclusion:** external-sort correctness requires both full order and bag identity.

### Example 4

**Situation:** A 64 MiB grant sorts rows advertised as 100 bytes, suggesting about 671,000 rows. The implementation also retains 24-byte tuple references, average 40-byte transformed collation keys, heap/array capacity, per-run buffers, and allocator overhead. The safe batch is much smaller. **Conclusion:** charge the physical representation and buffers, not merely logical payload width.

### Example 5

**Situation:** A plan has three simultaneous sort-like operators and four workers; each can approach 64 MiB. A naive capacity review sees “64 MiB,” but the plan can plausibly demand hundreds of MiB before other operators and sessions. Raising the limit to 256 MiB may destabilize the service. **Conclusion:** admission and memory policy must model plan-node, worker, and session multiplicity.

### Example 6

**Situation:** Input is already ordered by `(tenant_id)` and the query needs `(tenant_id, event_time)`. Incremental sort can finish one tenant group at a time. Most tenants have 1,000 rows, but one has 100 million. The common case stays in memory; the heavy tenant still spills. **Conclusion:** prefix order reduces scope, while group skew determines the remaining worst case.

### Example 7

**Situation:** A `LIMIT 20` query needs the best 20 rows from ten million. A top-N structure retains 20 candidates plus ties/policy state rather than writing a full sorted result. If the query instead uses a large offset or a downstream merge join needs every ordered row, discarding noncandidates is invalid. **Conclusion:** bounded selection is powerful only when the complete consumer semantics permit it.

### Example 8

**Situation:** Temporary storage becomes full after two of four output runs are sealed. Publishing those runs as if the pass completed would leave an ambiguous generation. The operator marks the pass failed, closes all handles, preserves no output as authoritative, releases input/output files according to abort policy, and reports quota evidence. **Conclusion:** a run-generation manifest needs an atomic completeness boundary and idempotent cleanup.

### Example 9

**Situation:** Two workers locally sort hash-partitioned rows. Concatenating worker outputs is not globally sorted because worker 1 can contain keys 1 and 100 while worker 2 contains 2 and 99. A k-way merge is correct; range partitioning can permit concatenation only if verified disjoint ordered boundaries and comparator agreement hold. **Conclusion:** local order plus arbitrary partitioning does not establish global order.

### Example 10

**Situation:** A plan reports an external merge and 40 GiB of temporary data after a deployment. Diagnosis compares actual rows and widths with estimates, required keys and presorted prefix, grant, run/pass evidence, concurrent operators, device latency, and cleanup. The cause is a tenfold width underestimate from a new projected JSON value, not merely “slow disks.” Projection pruning or corrected statistics/representation may beat a global memory increase. **Conclusion:** diagnose the causal chain from semantics through estimates, representation, algorithm, and storage.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies heaps, tournament structures, buffer-aware layouts, B+ bulk loading, immutable sorted runs, and compaction.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies comparison lower bounds, external-memory analysis, cache-aware algorithms, adversarial input design, and empirical methodology.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual memory, page cache, asynchronous I/O, filesystems, quotas, cancellation, and crash cleanup.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains cache locality, memory bandwidth, SIMD comparison, storage queues, and NUMA effects.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) extends sorted runs to distributed shuffle, partition files, merge stages, skew handling, checkpointing, and reproducible pipelines.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) adds distributed range partitioning, external state, retries, stragglers, and tiered storage.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes temporary-data confidentiality, key and permission policy, multi-tenant isolation, secure deletion limits, and audit evidence.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) contributes ephemeral/local versus network storage, capacity alarms, bandwidth contention, and cost-aware placement.

## References

1. Alok Aggarwal and Jeffrey Scott Vitter, [“The Input/Output Complexity of Sorting and Related Problems”](https://www.cse.wustl.edu/~angelee/archive/cse341/fall14/papers/AggarwalVi88.pdf), *Communications of the ACM* 31(9), 1988. Primary external-memory transfer bounds and optimal sorting variants.
2. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993. Primary survey of database sorting, merging, hashing, execution, and resource trade-offs.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Using `EXPLAIN`](https://www.postgresql.org/docs/18/using-explain.html), retrieved 2026-08-30. Current plan properties, sort/incremental-sort examples, startup cost, and measurement caveats.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Resource Consumption](https://www.postgresql.org/docs/18/runtime-config-resource.html), retrieved 2026-08-30. Current per-operation work memory and concurrent multiplication warning.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Executor](https://www.postgresql.org/docs/18/executor.html), retrieved 2026-08-30. Current blocking sort behavior in the executor model.
6. PostgreSQL Global Development Group, [`tuplesort.c` source](https://doxygen.postgresql.org/tuplesort_8c_source.html), retrieved 2026-08-30. Current generalized in-memory/external sort, balanced k-way merge, prereading, parallel runs, and access-mode implementation notes.
7. PostgreSQL Global Development Group, [`logtape.c` source](https://doxygen.postgresql.org/logtape_8c_source.html), retrieved 2026-08-30. Current logical-tape buffering, block recycling, preallocation, and cleanup implementation.
8. DuckDB Foundation, [Tuning Workloads](https://duckdb.org/docs/current/guides/performance/how_to_tune_workloads), retrieved 2026-08-30. Current out-of-core spill behavior, blocking operators, temporary directory, and limitations.
9. DuckDB Foundation, [Order Preservation](https://duckdb.org/docs/current/sql/dialect/order_preservation), retrieved 2026-08-30. Current order-preservation and sort-stability qualifications.
10. SQLite Project, [Temporary Files Used By SQLite](https://www.sqlite.org/tempfiles.html), retrieved 2026-08-30. Official description of transient indices and temporary storage used for `ORDER BY`, grouping, and set operations.

## Exercises

### Exercise 1

Define the two independent properties that establish a final external-sort result's logical correctness. Explain why checking only adjacent order is insufficient for SQL bags.

### Exercise 2

A fixed-width input occupies 8,100 blocks. A sorter has 90 usable blocks and chooses fan-in 8 after reserving overhead. Derive the initial run count, merge-pass count, and modeled transfers from initial run writing through fully materialized merge output. State the assumptions.

### Exercise 3

A production sort unexpectedly creates many runs even though `estimated_rows × estimated_width` is below its memory grant. Give a diagnosis sequence that can distinguish estimation error, representation overhead, concurrent grant pressure, and an inappropriate plan shape.

### Exercise 4

Compare full external sort, top-N, incremental sort, and index-provided order for `SELECT ... WHERE tenant_id = ? ORDER BY event_time DESC, event_id DESC LIMIT 50`. Identify the evidence needed before choosing.

### Exercise 5

Design a multi-tenant spill service used by parallel database workers. Specify its ownership, integrity, quota, confidentiality, cancellation, crash cleanup, and observability contracts, and explain how it prevents one tenant's sort from corrupting or starving another.

## Answers to the Exercises

### Answer 1

The output must be monotone under the exact complete comparator, and its bag of row occurrences must equal the input bag. Adjacent order detects inversions but not loss, duplication, or accidental duplicate elimination. Set equality is also insufficient because it ignores multiplicity. A practical oracle compares full ordered rows with an independent trustworthy sort or checks both adjacent comparator results and an identity-sensitive multiset digest/reconciliation.

### Answer 2

Fixed-batch generation gives `R = ceiling(8100/90) = 90` initial runs. Since 8² = 64 and 8³ = 512, `p = ceiling(log_8 90) = 3` merge passes. Initial run writing costs about 8,100 block transfers. Each fully materialized merge pass reads and writes 8,100 blocks, or 16,200; three cost 48,600. Total from initial run writing through final materialized output is 56,700 block transfers. This assumes fixed-width records, balanced grouping, sufficient effective buffers, no compression/cache/overlap, unchanged data volume, and excludes reading original input plus any later reading of final output.

### Answer 3

First confirm the exact required keys, top-N/full/incremental mode, presorted properties, and actual rows/width versus estimates. Then inspect physical record representation: projected payload, transformed/abbreviated keys, pointers, null maps, buffers, allocator overhead, and variable-width outliers. Compare granted, requested, and peak memory, including whether admission reduced the grant and how many plan nodes/workers/sessions were concurrent. Inspect initial runs, fan-in, passes, temporary bytes, and storage latency. Finally test alternative projection pruning, corrected statistics, earlier filtering, prefix/index order, top-N eligibility, or workload-specific grant/admission. Change global memory only after concurrency math and controlled reproduction.

### Answer 4

An exact matching index on `(tenant_id, event_time DESC, event_id DESC)` can filter and stop after 50, but assess coverage, clustering/base fetches, selectivity, maintenance cost, collation/NULL compatibility, and snapshot behavior. If rows arrive ordered by tenant or event-time prefix, incremental sort may bound work per prefix group, but inspect largest groups and estimates. Top-N is appropriate when only 50 final candidates are needed and no downstream consumer requires all ordered rows; measure scan volume and candidate comparison cost. Full external sort is the general fallback and may win for a large fraction read sequentially. Compare actual plans, rows, widths, startup/total latency, memory, temporary I/O, cold/warm behavior, and concurrent workload—not operator names alone.

### Answer 5

Issue an unforgeable operation/tenant/generation identity and make every run belong to exactly one live generation. Frame records with format/comparator version, sequence, count/length, and authenticated integrity where the threat model requires it; publish a run only after completion. Enforce per-operation, tenant, and global byte/I/O/file limits through reservation and fair admission. Use least-privilege storage paths/credentials, encryption according to data classification, and prevent cross-tenant names or metadata from selecting another run. Propagate cancellation to writers/readers, close handles, and make deletion idempotent. On process death, reclaim only generations whose leases/epochs prove they are orphaned; resumable work additionally binds source snapshot and manifest. Emit charged/peak bytes, run/pass counts, read/write/error latency, quota denials, cancellations, cleanup age, and orphan bytes by tenant without exposing row data. These contracts isolate capacity and namespace, detect substitution/corruption, and turn partial failures into abort/retry rather than cross-tenant data use.
