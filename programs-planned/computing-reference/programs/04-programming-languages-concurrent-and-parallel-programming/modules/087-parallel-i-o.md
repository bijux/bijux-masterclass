---
module_id: CONPAR-087
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 87
title: Parallel I/O
status: complete
last_verified: 2026-08-29
---

# Parallel I/O

## One-Page Review

### Governing question

How can many ranks map distributed state into a durable, portable, restartable global representation with correct offsets, metadata, coordination, completion, consistency, and failure publication while using the storage system efficiently?

### Essential definitions

- A **logical dataset** is the application-defined global array, mesh, table, graph, or checkpoint state independent of current rank layout.
- A **file view** selects the ordered file regions visible to one rank using displacement, elementary type, file type, and data representation.
- An **explicit offset** names a position directly; **individual/shared file pointers** carry mutable position state.
- **independent I/O** is issued per rank; **collective I/O** is coordinated by all ranks in the file communicator and may aggregate/reorder accesses.
- **two-phase I/O** redistributes request data among aggregators, then performs larger aligned storage operations.
- A **hyperslab/subarray** selects a multidimensional region without changing the global dataset definition.
- **chunking** stores a dataset in independently addressable blocks; chunk shape affects metadata, filtering, sharing, and access amplification.
- **checkpoint epoch** is one logically consistent recoverable application state.
- A **commit marker/manifest** identifies a fully validated checkpoint; data files existing is not sufficient.
- **durability** means data has reached the storage boundary promised by the API/system, which differs from write-buffer completion.
- **restart portability** means a checkpoint can be read under a different rank count, placement, endianness/representation, and decomposition subject to its contract.

### Central model, mechanism, or theorem

Define a canonical bijection `phi(global_id,field,epoch)->(object,byte region)` independent of rank. For one epoch, each rank's owned IDs map to nonoverlapping intended regions; their union equals the declared dataset. All collective operations and metadata changes occur in compatible order. Buffers, file views, datatypes, and requests remain valid through completion. After data completion, synchronization/durability actions, size/checksum/schema checks, and global validation pass before an atomic/recoverable manifest publishes the epoch. Performance tuning may change aggregators, chunks, striping, packing, or file count but not phi or the commit contract.

### Critical invariants

Stable global IDs—not current ranks—define layout; offsets/counts/extents use checked wide arithmetic; intended write regions neither overlap nor leave undeclared holes; collective calls and metadata operations match in order; file views and datatypes describe the same basic sequence as memory buffers; incomplete nonblocking/split I/O protects buffers and file-handle state; no file view changes with pending operations; completion, visibility, synchronization, and durability are distinguished; metadata/schema/checksums bind the same epoch; restart ignores incomplete epochs; and a read-back/reference validation gates publication.

### Common failures

Teams name files by rank and cannot restart at another P, calculate byte offsets in element units, use 32-bit products, overlap views, rely on shared pointers for deterministic layout, call collective HDF5/MPI operations on only some ranks, mix metadata orders, assume requested collective mode was used, choose chunks that many ranks rewrite, create millions of files, treat close/write completion as power-loss durability, overwrite the last good checkpoint in place, publish a manifest before all ranks finish, or benchmark bytes without validating contents and restart.

### Compact example

A row-major `4 x 6` array of eight-byte elements is split into a `2 x 2` rank grid. Each rank owns a `2 x 3` block. Rank 0's file-element offsets are `[0,1,2,6,7,8]`; rank 1's `[3,4,5,9,10,11]`; rank 2's `[12,13,14,18,19,20]`; rank 3's `[15,16,17,21,22,23]`. Together they cover exactly 24 elements and 192 bytes without overlap, despite noncontiguous row segments.

### Connections

[Domain Decomposition](084-domain-decomposition.md) supplies stable global ownership and restart remapping. [Collective Communication](083-collective-communication.md) supplies ordering and aggregation semantics. [Communication-Computation Overlap](086-communication-computation-overlap.md) supplies asynchronous lifetime/progress reasoning. The [program roadmap](../ROADMAP.md) next diagnoses node-level load imbalance that can make collective I/O wait for late ranks.

## Governing Question

For one logical dataset or checkpoint epoch, can every byte and metadata item be traced from a stable global entity to one canonical region, completed and made visible/durable under stated semantics, independently validated, and safely discovered by a future restart with a different decomposition?

Parallel I/O is a distributed transaction over data layout and storage semantics. Bandwidth matters only after the representation and publication protocol are correct.

## Why This Matters

Large simulations, training jobs, graph analytics, and scientific instruments cannot funnel all state through one rank. They must write/read in parallel while preserving a global representation useful to analysis and restart. Storage has different bottlenecks from networks: metadata servers, object count, small/unaligned operations, lock contention, striping, chunk ownership, caches, and burst buffers.

I/O errors often stay latent. A file can have the expected size while blocks are transposed, duplicated, stale, or from mixed epochs. An apparently successful checkpoint can be unrecoverable after rank count changes. A crash between data and metadata updates can publish partial state.

MPI-IO provides views, explicit offsets, collective/independent and nonblocking/split operations. HDF5 and related formats add typed datasets, dimensions, selections, chunking, filters, and metadata rules. Durable engineering derives a canonical layout above these APIs and validates the exact persisted artifact.

## Prerequisites and Retrieval

Retrieve:

- stable IDs, ownership generations, canonical/global versus local order, migration, and restart redistribution from [Domain Decomposition](084-domain-decomposition.md);
- collective order, pairwise type signatures, nonblocking/persistent lifetimes, and aggregation from [Collective Communication](083-collective-communication.md);
- request, completion, progress, protected buffer, and flow-control reasoning from [Communication-Computation Overlap](086-communication-computation-overlap.md); and
- numeric representation, device/host transfer, and reproducibility policy from [Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md).

Retrieval prompt: record dataset/schema/field/epoch/global-ID definitions; dimensions/order/data representation; canonical byte/object mapping; memory and file datatypes/views/selections; per-rank regions/counts; collective/metadata call order; access mode/pointers; aggregators/chunks/striping/files; request/buffer/file-handle lifetime; completion/sync/durability semantics; checksum/manifest/commit protocol; restart P/remap; quotas/security; validation oracle; and target library/filesystem versions.

## Learning Objectives

After completing this module, a learner can:

1. derive canonical rank-independent layouts for distributed arrays and irregular records;
2. compute checked explicit offsets, file views, subarrays, hyperslabs, and nonoverlap/coverage proofs;
3. distinguish independent, collective, shared-pointer, nonblocking, and split collective operations;
4. explain two-phase aggregation, striping, chunking, metadata, and file-count trade-offs;
5. preserve buffer, datatype, view, file-handle, and collective-order lifetimes;
6. distinguish operation completion, visibility, consistency, synchronization, and durability;
7. design recoverable multi-epoch checkpoint publication and restart at a different rank count;
8. validate schemas, sizes, regions, checksums, conservation, read-back, and restart results;
9. benchmark verified bandwidth, metadata rate, skew, aggregation, tails, and resource pressure; and
10. scope privacy, retention, scientific, operational, and high-stakes review claims.

## Core Exposition

### Define the logical dataset first

State the global object independent of storage and ranks: dimensions, coordinate/order convention, fields and basic types, units, schema version, entity IDs, epoch/time, missing values, endianness/data representation, compression/filter semantics, and invariants. A checkpoint additionally includes solver/control state, random streams, mesh/topology, partition-independent identities, and external-side-effect position needed for a correct restart.

Choose a canonical mapping. A row-major M-by-N array maps `(i,j)` to element offset `i*N+j`; byte offset adds a checked header displacement and multiplies by encoded element size. A structure with multiple fields might use separate datasets or a versioned record layout. An irregular mesh can store globally indexed arrays plus connectivity offsets, or sharded records referenced by a manifest. Current rank-local order is never the only durable key.

Use checked `MPI_Offset`/wide arithmetic for products and additions. Validate dimensions nonnegative, `start+count<=extent`, multiplication without overflow, encoded element size, alignment, and final declared size. Do not use native struct padding as a portable format without an explicit compatible representation.

### File views and memory layouts

An MPI file view consists of a byte displacement, elementary datatype (etype), filetype, data representation, and info hints. It makes a repeating/noncontiguous set of file regions visible to one process. The application buffer datatype describes memory order; the visible file etype sequence must match the buffer's basic sequence.

For a block-decomposed array, `MPI_Type_create_subarray` can describe one global subarray filetype while the memory buffer is contiguous local data. Commit the type, set the view collectively, perform access, complete every pending operation, then free/change only when legal. A view displacement is bytes; file offsets in data-access calls are measured in etypes relative to the view, not universally raw bytes.

Prove intra-rank filetype regions do not overlap for writing and prove cross-rank intended regions are disjoint unless the application explicitly uses supported atomic/ordered semantics. Compare the union against the dataset. Holes can be intentional padding/reserved regions but must be declared; unplanned holes can contain stale data.

Explicit-offset operations are easiest to reproduce and reason about. Individual pointers can express sequential access per rank but are reset by setting a view and depend on program history. Shared file pointers introduce coordination and uncertain ordering; ordered collective access defines rank order but often does not match a stable global layout after rank changes.

### Executable file-layout model

This exact-integer Python model maps four `2 x 3` rank blocks into a canonical row-major `4 x 6` array of eight-byte elements and checks global coverage. It does not perform I/O, call MPI/HDF5, encode values, prove durability, or establish performance.

<!-- bijux-verify: {"id":"parallel-subarray-layout","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rank=0 element_offsets=[0, 1, 2, 6, 7, 8] byte_offsets=[0, 8, 16, 48, 56, 64]\nrank=1 element_offsets=[3, 4, 5, 9, 10, 11] byte_offsets=[24, 32, 40, 72, 80, 88]\nrank=2 element_offsets=[12, 13, 14, 18, 19, 20] byte_offsets=[96, 104, 112, 144, 152, 160]\nrank=3 element_offsets=[15, 16, 17, 21, 22, 23] byte_offsets=[120, 128, 136, 168, 176, 184]\ncovered_elements=24\nunique_elements=24\nexpected_elements=24\ncoverage_exact=True\nfile_bytes=192\n","stderr":""}} -->
```python
global_rows, global_columns = 4, 6
process_rows, process_columns = 2, 2
local_rows = global_rows // process_rows
local_columns = global_columns // process_columns
element_bytes = 8
all_offsets = []
rank = 0
for process_row in range(process_rows):
    for process_column in range(process_columns):
        row_start = process_row * local_rows
        column_start = process_column * local_columns
        offsets = []
        for row in range(row_start, row_start + local_rows):
            for column in range(column_start, column_start + local_columns):
                offsets.append(row * global_columns + column)
        all_offsets.extend(offsets)
        print(
            f"rank={rank} element_offsets={offsets} "
            f"byte_offsets={[offset * element_bytes for offset in offsets]}"
        )
        rank += 1
print(f"covered_elements={len(all_offsets)}")
print(f"unique_elements={len(set(all_offsets))}")
print(f"expected_elements={global_rows * global_columns}")
print(f"coverage_exact={sorted(all_offsets) == list(range(global_rows * global_columns))}")
print(f"file_bytes={global_rows * global_columns * element_bytes}")
```

### Independent and collective access

Independent I/O lets ranks issue arbitrary counts/times and can work well for already large aligned disjoint regions. Thousands of small/strided independent operations can overload metadata/locking and fragment storage traffic. Collective I/O requires every rank in the file communicator to participate in compatible order, even ranks with zero data (using legal zero-count selections).

Collective access exposes the global pattern to the implementation. Two-phase I/O commonly assigns aggregators: ranks exchange pieces so aggregators issue fewer large contiguous/aligned filesystem operations, then redistribute on reads. This adds network copies and aggregator memory but can drastically improve storage efficiency. Aggregator count/buffer size are target-specific hints, not semantic requirements.

Measure whether the requested high-level collective route actually remained collective. Libraries may fall back because of datatype conversion, filters, selections, or layout. HDF5 exposes causes for some collective-I/O fallback. Record effective mode, not just requested configuration.

All ranks must order collective file operations consistently. Conditional data does not permit conditional collective calls; use zero selections/counts where the API permits or separate communicators/files. Metadata creation, extension, close, and property changes often have collective rules in high-level libraries; follow the exact version's documentation.

### Chunking, striping, and file count

Chunked datasets support subset access, compression/filters, and extendibility. Chunk dimensions should fit dominant access patterns and target transfer sizes. If many ranks update one compressed chunk, the library may coordinate ownership and read-modify-write, adding communication and metadata. Align partition and chunk boundaries where reasonable, but do not corrupt the logical layout to satisfy one current machine.

Filesystem/object striping distributes a file across storage targets. Stripe count and size interact with aggregator count, access size, alignment, concurrency, and contention from other jobs. Too few targets bottleneck; too many waste metadata/lock resources and hurt small jobs. Treat hints as recorded deployment configuration and benchmark on representative systems.

One-file-per-rank avoids shared-file coordination and can write locally, but object count, metadata operations, cleanup, transfer, and analysis become unmanageable at scale; restart P changes need a manifest and many-to-many reads. A shared canonical file simplifies consumption but can concentrate metadata/locking. File-per-node/aggregator or bounded shards plus a canonical manifest are intermediate designs.

Small variables and attributes can dominate metadata. Batch them, avoid repeatedly opening/closing objects, and use collective metadata modes only with the required call discipline. A metadata cache improves performance but introduces consistency rules; mismatched collective metadata assumptions can corrupt behavior.

### Nonblocking and split collective I/O

MPI provides nonblocking collective file operations returning requests and split collective begin/end routines. Initiation may permit progress but does not guarantee effective overlap. Buffers remain protected; all ranks call collectives in the same file-handle order; blocking and nonblocking collective forms do not match; and pending operations must complete before illegal view/handle changes.

Split collective implementations may do the work in begin or end, and split collective operations on the same handle have restrictions. Independent useful work between begin/end must not touch protected buffers or depend on data. Apply the weak-progress and measurement method from the preceding module.

Pipeline I/O with multiple buffers can overlap serialization/compression, transfers, and computation. Bound the depth by memory, pinned buffers, requests, storage queue limits, and checkpoint semantics. Do not let epoch e+1 overwrite a buffer or object until epoch e's write and validation/retention policy release it.

### Completion, consistency, and durability

Separate at least five events: the API initiation returned; the request/operation completed and the user buffer is reusable; other handles/readers can observe data under consistency rules; buffered data is synchronized/flushed according to the API; the storage system has made the promised durability guarantee against named failures. These are not interchangeable.

MPI-IO consistency depends on file handles, atomic mode, overlapping/conflicting access, program order, and synchronization. `MPI_File_sync` is the MPI mechanism that ensures previously written data is transferred to the storage device under its semantics; filesystem caches, burst buffers, object stores, and power-loss domains still require deployment-specific interpretation. Closing a handle is not a universal distributed transaction for application metadata and data.

Avoid concurrent overlapping writes. If an algorithm needs shared updates, aggregate in memory or assign region ownership. Atomic mode can cost substantially and may not give high-level object atomicity when one library call becomes multiple MPI operations. Prefer immutable epoch outputs plus commit metadata.

### Recoverable checkpoint publication

Never overwrite the only known-good checkpoint in place. Write a new unique epoch directory/object set, preferably with immutable data object names. Include schema, input/model/code/config digests, global dimensions/IDs, units/representation, expected objects/sizes/regions, per-object/partition checksums, checkpoint time/iteration, random/control state, and restart compatibility.

Protocol: agree/freeze a consistent application epoch; write data and metadata to unpublished names; complete requests and close/sync as required; each rank reports status/checksums; globally validate counts, sizes, coverage, conservation and optionally read-back; write/atomically publish a small final manifest or pointer only after success. A restart enumerates only valid committed manifests and ignores orphan/incomplete objects.

“Atomic publish” depends on storage: POSIX rename semantics, object-store conditional update, or a catalog transaction differ. State the mechanism and failure model. Keep the prior committed epoch until the new one is verified and retention policy permits deletion. Cleanup of orphans is a separate recoverable operation.

Restart must work at different P/placement. Readers use the canonical layout and new decomposition to select needed regions, not old rank filenames. Reconstruct topology, solver/preconditioner or accelerator caches only when portable; otherwise rebuild from durable logical state. Verify after redistribution before resuming external effects.

### Irregular data and evolving schemas

Variable-length records need offsets plus payload or bounded shards. Compute global offsets with checked scans of encoded lengths, then write disjoint ranges. Validate monotonic offsets, final payload size, record IDs, and checksums. Avoid native pointers, addresses, or rank-local indices.

Schema evolution is explicit. Store format version and field metadata; readers reject unsupported major versions or apply reviewed migrations. Optional fields have defaults and provenance. Units, coordinate reference frames, endianness, floating format, compression/filter versions, and missing-value semantics belong in the schema.

Indexes/manifests can become a single bottleneck. Partition their construction and merge deterministically, but preserve one authoritative committed root. Validate referential integrity and bound parser allocations; untrusted or corrupted lengths/counts can cause overflow or denial.

### Verification, security, and operations

Test one/many/prime/non-power ranks; zero-data ranks; uneven, strided, sparse, and huge counts; 32-bit overflow boundaries; rank reorder and changed-P restart; collective/independent/fallback modes; contiguous/chunked/compressed data; varied aggregators/stripes/shards; nonblocking/split progress; partial ranks, short writes, full disk/quota, permission failure, process/node failure, corrupted/truncated objects, incomplete manifests, and prior-checkpoint fallback.

Use coordinate/global-ID encoded values so transposes and offset errors are visible. Independently compute coverage, no overlap, sizes, checksums, schema and referential integrity. Read back with a different rank count and reader implementation where possible; compare scientific invariants, conservation/error, solver state, random replay, and continued trajectory against a controlled checkpoint/restart reference.

Measure logical and physical bytes, useful bandwidth, operation size/distribution/alignment, metadata operations/rate, aggregator network bytes/memory, queue depth, cache/burst behavior, compression ratio/CPU, rank arrival and I/O skew, open/view/write/sync/close/read/restart phases, tails, failures, and instrumentation. Include shared-system variability.

Encrypt sensitive data at rest/in transit according to policy; minimize replicated metadata; redact traces/paths; enforce access controls, retention, secure deletion limitations, key management, and audit. Checksums detect accidental corruption but are not authentication unless keyed/signed within a reviewed trust design.

## Definitions and Notation

- `D`: logical global dataset; `G`: stable global entity IDs.
- `e`: checkpoint/data epoch.
- `phi_e(id,field)`: canonical object and byte-region mapping.
- `R_r`: regions rank r intends to access.
- `disp`: file-view byte displacement.
- `etype`: elementary file datatype; `filetype_r`: visible pattern for rank r.
- `M`: memory datatype/selection.
- `O`: encoded object/file set; `S_exp`: expected encoded size.
- `Q_io`: nonblocking I/O request set.
- `A`: aggregator set; `d`: bounded pipeline depth.
- `H_obj`: per-object/data checksum; `H_manifest`: committed manifest digest.
- `C_e`: commit marker/manifest for epoch e.
- `Obs`: persisted/restarted result contract.

An operation's completion does not alone imply committed epoch publication or every failure-domain durability guarantee.

## Mechanisms, Invariants, or Proof Structure

### Layout proof

Show phi is total and injective for required `(id,field)` values; intended rank regions cover the declared dataset and are pairwise disjoint; checked offsets/extents remain in object bounds; memory basic sequence equals the file view/selection sequence.

### Collective and lifetime proof

All file-communicator members call collective data and metadata operations in compatible order, with legal zero selections where needed. Buffers, datatypes, views, property arrays, requests, and handles remain valid/protected; pending operations complete before view changes/close/reuse.

### Consistency and commit proof

No conflicting write is unordered. Completion, sync, close, storage durability boundary, global validation, and manifest publication occur in the declared order. Any crash prefix exposes either the previous committed epoch or no new commit, never a trusted partial new epoch.

### Restart proof

Reader validates manifest/schema/digests/sizes, maps new ownership through stable IDs/canonical layout, reads every required region exactly once, reconstructs derived state, validates global invariants, and resumes only after the same epoch is established everywhere.

### Performance evidence proof

Compare independent/collective/effective modes, aggregators, chunks, stripes, shards, and pipelines with identical logical bytes and validated restart. Include metadata, redistribution, sync/close, read/restart, tails, and resource usage; do not infer universal performance from one filesystem.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| explicit offsets | deterministic direct layout | manual arithmetic/layout |
| file views/subarrays | declarative noncontiguous mapping | datatype/etype complexity |
| independent I/O | flexible rank-local schedule | small/random request pressure |
| collective/two-phase I/O | aggregation and global optimization | collective order and redistribution |
| shared/ordered pointer | simple streams/rank order | mutable/global order and scalability |
| contiguous dataset | simple, high-throughput scans | weak subset/filter/extension flexibility |
| chunked dataset | subsets, filters, extension | metadata and shared-chunk amplification |
| one file per rank | simple isolated writes | object/metadata/restart/analysis explosion |
| shared file | canonical consumption | locking/metadata/coordination pressure |
| bounded sharded manifest | scalable compromise | manifest and shard management |
| immutable epoch + commit | recoverable publication | extra storage and cleanup |

Choose a canonical representation first, then tune physical layout and coordination for measured workloads and systems.

## Failure Modes and Misconceptions

- **“Rank order is a file format.”** stable global identities define durable layout.
- **“Offsets are always bytes.”** view displacements are bytes; access offsets are etype-relative.
- **“64-bit types eliminate overflow.”** checked products/additions are still required.
- **“Expected file size proves correctness.”** permutations/duplicates can preserve size.
- **“Collective mode is automatic.”** all ranks/order and effective fallback matter.
- **“Zero-data ranks may skip collectives.”** use legal zero selections/counts.
- **“One file per rank scales indefinitely.”** metadata/object/restart costs can dominate.
- **“More stripes always improve bandwidth.”** concurrency and request size determine benefit.
- **“Chunks should equal rank blocks.”** restart/access/filter patterns can differ.
- **“Compression only saves bytes.”** chunk sharing and metadata/CPU change the path.
- **“Nonblocking I/O guarantees overlap.”** progress and independent work remain empirical.
- **“Write completion means durable checkpoint.”** synchronization, failure domain, validation, and commit remain.
- **“Atomic mode makes a high-level transaction.”** one call may map to multiple lower operations.
- **“Close publishes the epoch.”** a recoverable global manifest protocol is needed.
- **“A checkpoint is correct if it reads.”** restart state and continued trajectory must validate.
- **“Checksums provide authenticity.”** ordinary hashes detect corruption, not trusted authorship.

## Worked Examples

### Example 1

**Byte/etype confusion.** A view etype is double. Rank passes offset 64 expecting bytes and starts at element 64 (byte 512). Use view-relative element offset 8 or an explicit byte-based design. **Conclusion:** document units at every boundary.

### Example 2

**Overflow.** `nx*ny*nz*8` is computed in 32-bit before assignment to `MPI_Offset`, wrapping. Promote/check each multiplication first. **Conclusion:** a wide destination cannot repair narrow intermediate arithmetic.

### Example 3

**Transposed subarray.** Global C row-major order is described as Fortran order. File size and counts match, but coordinate-encoded read-back reveals transposition. **Conclusion:** validate semantic positions, not sizes.

### Example 4

**Conditional collective.** Empty rank 7 skips `H5Dwrite` configured collective while others call it. The group hangs or violates rules. Rank 7 participates with an empty selection. **Conclusion:** data absence does not remove collective membership.

### Example 5

**Shared compressed chunk.** Eight ranks update one filtered chunk, causing ownership coordination and read-modify-write. Repartition/chunk alignment or collective aggregation reduces amplification. **Conclusion:** physical chunks create write-sharing costs.

### Example 6

**File storm.** One million ranks each create a checkpoint file; raw writes finish quickly but metadata creation and later cleanup/restart collapse. Bounded shards/aggregators plus a manifest reduce object count. **Conclusion:** include lifecycle metadata cost.

### Example 7

**Requested versus effective collective.** HDF5 is set collective, but datatype conversion forces fallback. Query causes and compare complete verified routes. **Conclusion:** record actual I/O mode.

### Example 8

**Partial checkpoint.** A node fails after data writes but before global validation. Because the manifest is absent, restart ignores the orphan epoch and uses the previous commit. **Conclusion:** publish last.

### Example 9

**Changed-P restart.** A 64-rank checkpoint stores canonical global rows; 96 ranks calculate new subarray views and read their new ownership. Rank-local caches rebuild. **Conclusion:** canonical layout decouples restart from old P.

### Example 10

**Clinical genomics checkpoint.** Persisted state must bind pseudonymized sample/variant/reference-build/cohort/model/schema/consent/epoch identities, units and missingness, deterministic/bounded numeric policy, encryption/keys/access/retention, audit, failure/restart, independent statistical validation, and publication gates. Named genomics/bioinformatics, clinical genetics, biostatistics, privacy/security, storage/HPC, operations, data governance, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** a fast readable checkpoint does not establish scientific, consent, privacy, or clinical validity.

## Cross-Program Connections

- **Storage systems:** caches, striping, object stores, metadata, durability, and atomic publication define mechanisms.
- **Databases:** schemas, transactions, manifests, checksums, migrations, and recovery recur.
- **Distributed systems:** epochs, two-phase publication, partial failure, idempotence, and consensus boundaries recur.
- **Data engineering:** partitioned columnar layouts, chunks, compression, catalogs, and schema evolution align.
- **Numerical computing:** representation, precision, conservation, random state, and restart trajectory constrain formats.
- **Security/privacy:** access, encryption, key management, retention, audit, and secure-deletion limits govern data.
- **Networks:** two-phase I/O redistributes data and competes with application traffic.
- **Algorithms:** prefix sums map variable records; aggregation and external-memory access shape cost.
- **Testing:** fault prefixes, changed-P read-back, coordinate encodings, and independent readers expose defects.
- **Operations:** quotas, full filesystems, orphan cleanup, catalog health, bandwidth/tails, and restore drills sustain systems.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: File Views*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node363.htm>
3. MPI Forum, *MPI-5.0: Data Access Routines*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node365.htm>
4. MPI Forum, *MPI-5.0: Split Collective Data Access Routines*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node376.htm>
5. MPI Forum, *MPI-5.0: File Consistency*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node385.htm>
6. MPI Forum, *MPI-5.0: Nonblocking Collective File Operations*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node389.htm>
7. MPI Forum, *MPI-5.0: Type Matching for I/O*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node390.htm>
8. HDF Group, *Collective Calling Requirements in Parallel HDF5 Applications*, HDF5 1.16 documentation; retrieved 2026-08-29. <https://support.hdfgroup.org/documentation/hdf5/latest/collective_calls.html>
9. HDF Group, *Collective Metadata I/O*, current documentation; retrieved 2026-08-29. <https://support.hdfgroup.org/documentation/hdf5/latest/collective_metadata_io.html>
10. HDF Group, *HDF5 Dataset Transfer Properties and Collective-I/O Causes*, current documentation; retrieved 2026-08-29. <https://support.hdfgroup.org/documentation/hdf5/latest/group___d_x_p_l.html>

## Exercises

### Exercise 1

Derive canonical element and byte regions for a row-major `9 x 10` float64 array split by row over four ranks using quotient/remainder. Prove coverage and give expected file size.

### Exercise 2

A rank owns columns 2–4 of every row in a `5 x 8` row-major array. Give its ordered element offsets, explain a subarray/file-view representation, and distinguish byte displacement from etype offsets.

### Exercise 3

Diagnose a checkpoint that has correct object sizes but fails after restart at a new P: files are named by old rank, connectivity stores old local indices, one rank skipped a collective metadata call, and the manifest was written before sync. Give a repair and validation plan.

### Exercise 4

Design a benchmark matrix comparing independent, collective/two-phase, one-file-per-rank, shared-file, and bounded-shard HDF5 layouts for uneven compressed data. Include fairness, effective-mode evidence, failure/restart, and system metrics.

### Exercise 5

Transfer the checkpoint protocol to a multi-hospital federated pathology model containing sensitive images and optimizer state. Specify canonical identities/schema, consistency/durability/privacy/failure invariants, validation, publication and retention, and named human reviewers without claiming review.

## Answers to the Exercises

### Answer 1

For 9 rows and P=4, `q=2,r=1`: row counts `[3,2,2,2]`, starts `[0,3,5,7]`, ends `[3,5,7,9]`. With 10 columns, rank element half-open regions are `[0,30)`, `[30,50)`, `[50,70)`, `[70,90)`. Byte regions multiply by 8: `[0,240)`, `[240,400)`, `[400,560)`, `[560,720)`. Consecutive starts equal prior ends, regions are disjoint, first starts zero, last ends 90/720, proving exact coverage. Expected raw payload is `9*10*8=720` bytes, excluding any declared header/container metadata.

### Answer 2

Columns 2,3,4 across rows yield element offsets `[2,3,4,10,11,12,18,19,20,26,27,28,34,35,36]`. A 2-D subarray uses global sizes `[5,8]`, subsizes `[5,3]`, starts `[0,2]`, row-major order; committed as filetype with a double etype and view displacement for any header. The view displacement is an absolute byte count. A subsequent explicit MPI-IO offset is counted in etypes relative to the view. Byte offset for global element k in the raw no-header layout is `8*k`; conflating these units shifts data.

### Answer 3

The format encodes decomposition rather than logical state, contains nonportable connectivity, violates metadata collective order, and can publish nondurable partial data. Define stable global vertex/cell/field IDs and a canonical or manifest-sharded schema; translate connectivity to global IDs; make all file-communicator ranks follow collective data/metadata order with empty selections as needed. Write a unique unpublished epoch, complete requests, sync/close under documented semantics, gather status/checksums, validate coverage/referential integrity/conservation/solver state, read back at a different P, then publish the manifest atomically while retaining the prior commit. Fault-test every prefix and ensure absent/invalid manifests are ignored.

### Answer 4

Use identical logical dataset, compression/filter, schema, input, rank placement, checkpoint cadence, validation, and restart workload. Sweep P, unevenness, rank arrival skew, chunk shape/sharing, aggregators/buffer sizes, stripe settings, shard count, and request size; include zero-data ranks. Record requested/effective collective mode and fallback causes, logical/physical/network bytes, compression CPU/ratio, open/metadata/data/sync/close/read/restart time distributions, bandwidth/tails, metadata operations, aggregator memory, queue/stripe use, object count, and interference. Inject full/quota/permission/rank failures and restart at changed P. Accept a candidate only with exact schema/coverage/checksums, scientific invariants, and a committed recoverable epoch; report target filesystem/library versions and variability.

### Answer 5

Canonical keys include pseudonymized institution/case/slide/tile/model/optimizer-parameter IDs, stain/scanner/preprocessing/label/schema/model/consent/training epoch, units, missingness, and representation. Store immutable bounded shards for image-derived/model state plus a final signed/authenticated manifest under a reviewed trust design. Prove unique/nonoverlapping regions, checked lengths, collective order, protected buffers, schema/referential integrity, optimizer/random replay, encrypted authorized placement, key/retention/audit controls, and no mixed or partial epoch. Complete/sync according to named storage guarantees, globally checksum and independently validate, changed-P/institution restart-test, then publish; keep the prior epoch and ignore orphans. Test corruption, truncation, missing hospital/rank, quota, key loss/rotation, rollback, revoked consent policy, and restore drills. Named pathology, oncology as applicable, ML/statistics, bioinformatics/data engineering, privacy/security, storage/HPC, operations, data governance, quality/regulatory, ethics, accessibility/human-factors, and independent clinical validation reviewers are required. No external review, consent determination, clinical validity, or approval is claimed.
